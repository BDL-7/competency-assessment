"""Framework-neutral S0-04A application service."""
from __future__ import annotations
import hashlib,json
from dataclasses import asdict
from datetime import UTC,date,datetime
from typing import Callable
from uuid import uuid4

from app.documents import synthetic_artifact_hash
from app.domain import (AssessmentState,AssignmentState,CommandResult,NotificationTrigger,
    RejectionCode,Role,SignatureRole,add_calendar_months,is_overdue,validate_assessment_content)
from app.notifications import MinimalNotification,NonDeliveringNotificationAdapter
from app.reporting import AssessmentSummary
from app.services.contracts import *
from app.services.pilot import effective_scope

def _utc(value:datetime)->datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
def _id(prefix:str)->str:return f"{prefix}-{uuid4().hex}"

def _command_boundary(method):
    def guarded(self,*args,**kwargs):
        try:return method(self,*args,**kwargs)
        except Exception:
            return CommandResult.failed(kwargs.get("correlation_id","unavailable"),RejectionCode.DEPENDENCY_UNAVAILABLE,"The operation could not be completed.")
    return guarded

def _query_boundary(method):
    def guarded(self,*args,**kwargs):
        try:return method(self,*args,**kwargs)
        except Exception:return AssessmentQueryResult.failed(kwargs.get("correlation_id","unavailable"))
    return guarded

class WorkflowService:
    def __init__(self,uow_factory:UnitOfWorkFactory,*,clock:Callable[[],datetime],
                 id_factory:Callable[[str],str]=_id,
                 finalization_fault:Callable[[],None]|None=None)->None:
        self._uow,self._id=uow_factory,id_factory;self._clock=lambda:_utc(clock())
        self._fault=finalization_fault

    @_command_boundary
    def configure_synthetic_scenario(self,actor:Actor,*,request_id:str,correlation_id:str)->CommandResult:
        op,target="configure","SYN-TEAM-ALPHA";fp=self._fp({"scenario":"S0-04A-v1"})
        with self._uow() as u:
            if r:=self._replay(u,op,target,actor,request_id,fp):return r
            if actor.user_id!="SYN-ADM-001":
                return self._reject(u,actor,op,target,request_id,correlation_id,fp,
                    RejectionCode.UNAUTHENTICATED,"Authentication is required.",audit=False)
            if u.aggregates.user_count():
                if e:=self._actor_error(u,actor):return self._reject(u,actor,op,target,request_id,correlation_id,fp,*e)
                return self._reject(u,actor,op,target,request_id,correlation_id,fp,
                    RejectionCode.INVALID_STATE,"Synthetic configuration already exists.")
            now=self._clock()
            users=("SYN-EMP-001","SYN-LEAD-001","SYN-ASR-001","SYN-TS-001","SYN-ADM-001","SYN-PLAT-001","SYN-OUT-001")
            for user in users:u.aggregates.add_user(UserRecord(user,user))
            u.aggregates.add_service_principal(ServicePrincipalRecord("SYN-SVC-001"))
            u.aggregates.add_capability(CapabilityGrantRecord("SYN-SVC-001","notification_events_and_attempts",now))
            u.aggregates.add_configuration(ConfigurationRecord())
            scopes=(("SYN-EMP-001",Role.EMPLOYEE,"SYN-TEAM-ALPHA",None,None),
                ("SYN-LEAD-001",Role.TEAM_LEAD,"SYN-TEAM-ALPHA",None,None),
                ("SYN-ASR-001",Role.ASSESSOR,None,None,None),("SYN-TS-001",Role.TECHNICAL_SUPERVISOR,None,None,None),
                ("SYN-ADM-001",Role.SQUAD_ADMIN,None,None,"SYN-CFG-001"),
                ("SYN-PLAT-001",Role.PLATFORM_ADMIN,None,None,"diagnostic"),
                ("SYN-OUT-001",Role.ASSESSOR,None,"SYN-OTHER-ASM",None))
            for user,role,team,assessment,config in scopes:
                u.aggregates.add_role(RoleScopeRecord(self._id("ROLE"),user,role.value,now,
                    team_id=team,assessment_id=assessment,configuration_scope=config))
            result=CommandResult.succeeded(correlation_id,reference_id=target,state="Configured",version=1)
            self._success(u,op,target,actor,request_id,correlation_id,fp,result,"team",target,"Synthetic configuration created");return result

    @_command_boundary
    def schedule_assignment(self,actor:Actor,*,request_id:str,correlation_id:str,
                            expected_configuration_version:str="SYN-CFG-001")->CommandResult:
        op,target="schedule_assignment","SYN-ASGN-001";fp=self._fp({"configuration":expected_configuration_version})
        with self._uow() as u:
            if r:=self._replay(u,op,target,actor,request_id,fp):return r
            if e:=self._actor_error(u,actor):return self._reject(u,actor,op,target,request_id,correlation_id,fp,*e)
            if not self._scope(u,actor,Role.SQUAD_ADMIN,configuration="SYN-CFG-001"):
                return self._not_visible(u,actor,op,target,request_id,correlation_id,fp)
            cfg=u.aggregates.get_configuration(expected_configuration_version)
            if not cfg:return self._reject(u,actor,op,target,request_id,correlation_id,fp,RejectionCode.INVALID_INPUT,"Configuration is unavailable.")
            row=AssignmentRecord(target,"SYN-EMP-001",cfg.team_id,"SYN-LEAD-001","SYN-ASR-001","SYN-TS-001",cfg.process_id,cfg.id,date(2026,2,15),add_calendar_months(date(2026,2,15),12))
            u.aggregates.add_assignment(row);result=CommandResult.succeeded(correlation_id,reference_id=target,state=row.state,version=1)
            self._success(u,op,target,actor,request_id,correlation_id,fp,result,"assignment",target,"Synthetic assignment scheduled",assignment_id=target);return result

    @_command_boundary
    def release_assignment(self,actor:Actor,*,request_id:str,correlation_id:str,expected_version:int)->CommandResult:
        op,target="release_assignment","SYN-ASGN-001";fp=self._fp({"expected_version":expected_version})
        with self._uow() as u:
            if r:=self._replay(u,op,target,actor,request_id,fp):return r
            if e:=self._actor_error(u,actor):return self._reject(u,actor,op,target,request_id,correlation_id,fp,*e)
            row=u.aggregates.get_assignment(target)
            if not row or not self._scope(u,actor,Role.SQUAD_ADMIN,configuration=row.configuration_version):return self._not_visible(u,actor,op,target,request_id,correlation_id,fp)
            if row.lock_version!=expected_version:return self._reject(u,actor,op,target,request_id,correlation_id,fp,*self._stale())
            if row.state!=AssignmentState.SCHEDULED.value:return self._reject(u,actor,op,target,request_id,correlation_id,fp,*self._invalid())
            row.state=AssignmentState.ASSIGNED.value;row.lock_version+=1
            u.aggregates.put_assignment(row)
            assessment=AssessmentRecord("SYN-ASM-001",row.id);u.aggregates.add_assessment(assessment);now=self._clock()
            for user,role in (("SYN-ASR-001",Role.ASSESSOR),("SYN-TS-001",Role.TECHNICAL_SUPERVISOR),("SYN-EMP-001",Role.EMPLOYEE)):
                u.aggregates.add_role(RoleScopeRecord(self._id("ROLE"),user,role.value,now,assessment_id=assessment.id))
            result=CommandResult.succeeded(correlation_id,reference_id=assessment.id,state=row.state,version=row.lock_version)
            self._success(u,op,target,actor,request_id,correlation_id,fp,result,"assignment",row.id,"Synthetic assignment released",assessment.id,row.id);return result

    @_command_boundary
    def begin_assessment(self,actor:Actor,*,assessment_id:str,request_id:str,correlation_id:str,expected_version:int)->CommandResult:
        op="begin_assessment";fp=self._fp({"expected_version":expected_version})
        with self._uow() as u:
            if r:=self._replay(u,op,assessment_id,actor,request_id,fp):return r
            if e:=self._actor_error(u,actor):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*e)
            ctx=self._authorized(u,actor,assessment_id,Role.ASSESSOR)
            if not ctx:return self._not_visible(u,actor,op,assessment_id,request_id,correlation_id,fp)
            assessment,assignment=ctx
            if assessment.lock_version!=expected_version:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._stale())
            if assessment.state!=AssignmentState.ASSIGNED.value:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._invalid())
            draft=DraftRecord("SYN-DRAFT-001",assessment.id,assignment.employee_id,assignment.assessor_id,assignment.technical_supervisor_id,assignment.configuration_version,actor.user_id,actor.user_id)
            u.aggregates.add_draft(draft);assessment.current_draft_id=draft.id;assessment.state=AssessmentState.IN_PROGRESS.value;assessment.lock_version+=1
            u.aggregates.put_assessment(assessment)
            result=CommandResult.succeeded(correlation_id,reference_id=draft.id,state=assessment.state,version=assessment.lock_version)
            self._success(u,op,assessment.id,actor,request_id,correlation_id,fp,result,"assessment",assessment.id,"Assessment started",assessment.id,assignment.id);return result

    @_command_boundary
    def save_draft(self,actor:Actor,*,assessment_id:str,content:DraftContent,followup_description:str|None,
                   request_id:str,correlation_id:str,expected_draft_version:int)->CommandResult:
        op="save_draft";fp=self._fp({"content":asdict(content),"followup":followup_description,"expected":expected_draft_version})
        with self._uow() as u:
            if r:=self._replay(u,op,assessment_id,actor,request_id,fp):return r
            if e:=self._actor_error(u,actor):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*e)
            ctx=self._authorized(u,actor,assessment_id,Role.ASSESSOR)
            if not ctx:return self._not_visible(u,actor,op,assessment_id,request_id,correlation_id,fp)
            assessment,assignment=ctx
            if assessment.state not in (AssessmentState.IN_PROGRESS.value,AssessmentState.RETURNED.value):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._invalid())
            draft=self._draft(u,assessment)
            if not draft:return self._pointer_failure(u,actor,op,assessment_id,request_id,correlation_id)
            if draft.lock_version!=expected_draft_version:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._stale())
            if content.element_ref!="SYN-ELEMENT-03" or content.element_result!="unsuccessful" or not content.has_gap:
                return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.INVALID_INPUT,"Synthetic element result and follow-up indicators are inconsistent.")
            draft.content=content;draft.followup_description=followup_description;draft.updated_by=actor.user_id;draft.lock_version+=1
            u.aggregates.put_draft_element(DraftElementRecord(self._id("DRAFT-ELEMENT"),draft.id,content.element_ref,content.element_result,content.element_evidence,content.has_gap,followup_description))
            u.aggregates.put_draft(draft)
            if assessment.state==AssessmentState.RETURNED.value:assessment.state=AssessmentState.IN_PROGRESS.value;assessment.lock_version+=1
            u.aggregates.put_assessment(assessment)
            result=CommandResult.succeeded(correlation_id,reference_id=draft.id,state=assessment.state,version=assessment.lock_version)
            self._success(u,op,assessment.id,actor,request_id,correlation_id,fp,result,"assessment",assessment.id,"Draft saved",assessment.id,assignment.id);return result

    @_command_boundary
    def submit_assessment(self,actor:Actor,*,assessment_id:str,request_id:str,correlation_id:str,expected_version:int)->CommandResult:
        op="submit_assessment";fp=self._fp({"expected_version":expected_version})
        with self._uow() as u:
            if r:=self._replay(u,op,assessment_id,actor,request_id,fp):return r
            if e:=self._actor_error(u,actor):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*e)
            ctx=self._authorized(u,actor,assessment_id,Role.ASSESSOR)
            if not ctx:return self._not_visible(u,actor,op,assessment_id,request_id,correlation_id,fp)
            assessment,assignment=ctx
            if assessment.lock_version!=expected_version:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._stale())
            if assessment.state not in (AssessmentState.IN_PROGRESS.value,AssessmentState.RETURNED.value):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._invalid())
            draft=self._draft(u,assessment)
            if not draft:return self._pointer_failure(u,actor,op,assessment_id,request_id,correlation_id)
            if not draft.content or validate_assessment_content(asdict(draft.content)):
                return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.COMPLETENESS_FAILED,"Required synthetic fields are missing.")
            elements=u.aggregates.list_draft_elements(draft.id)
            if len(elements)!=1 or elements[0].element_ref!="SYN-ELEMENT-03" or elements[0].result!="unsuccessful" or not elements[0].has_gap or not elements[0].evidence.strip():
                return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.INVALID_INPUT,"Synthetic element work is inconsistent.")
            number=len(u.aggregates.list_versions(assessment.id))+1;version_id=f"SYN-ASMV-{number:03d}"
            version=VersionRecord(version_id,assessment.id,number,draft.id,assignment.employee_id,
                assignment.assigned_team_lead_id,assignment.assessor_id,assignment.technical_supervisor_id,
                draft.configuration_version,draft.content,draft.followup_description,actor.user_id)
            u.aggregates.add_version(version)
            for element in elements:u.aggregates.add_version_element(VersionElementRecord(self._id("ELEMENT"),version.id,element.element_ref,element.result,element.evidence,element.has_gap,element.followup_description))
            assessment.current_version_id=version.id;assessment.state=AssessmentState.SUBMITTED.value;assessment.lock_version+=1
            self._audit(u,actor,"submit_assessment","assessment",assessment.id,request_id,correlation_id,"Succeeded","Immutable version submitted",assessment.id,assignment.id)
            missing=not draft.followup_description or not draft.followup_description.strip()
            if missing:
                correction=DraftRecord("SYN-DRAFT-002",assessment.id,draft.employee_id,draft.assessor_id,draft.technical_supervisor_id,draft.configuration_version,actor.user_id,actor.user_id,content=draft.content)
                u.aggregates.add_draft(correction)
                for element in elements:u.aggregates.put_draft_element(DraftElementRecord(self._id("DRAFT-ELEMENT"),correction.id,element.element_ref,element.result,element.evidence,element.has_gap,None))
                assessment.current_draft_id=correction.id;assessment.state=AssessmentState.RETURNED.value
                self._audit(u,actor,"return_missing_followup","assessment",assessment.id,request_id,correlation_id,"Rejected","Follow-up documentation required",assessment.id,assignment.id)
                result=CommandResult.rejected(correlation_id,RejectionCode.FOLLOWUP_REQUIRED,"Document the required follow-up before signature.",reference_id=version.id,state=assessment.state,version=assessment.lock_version)
            else:
                assessment.state=AssessmentState.AWAITING_TESTING_PERSONNEL.value
                submitted_event=self._event(u,assignment,assessment,NotificationTrigger.SUBMITTED,"SYN-TS-001",self._clock(),correlation_id)
                personnel_event=self._event(u,assignment,assessment,NotificationTrigger.TESTING_PERSONNEL_SIGNATURE_REQUIRED,"SYN-EMP-001",self._clock(),correlation_id)
                for event in (submitted_event,personnel_event):self._audit(u,actor,"notification_event","notification",event.id,request_id,correlation_id,"Succeeded","Logical notification recorded",assessment.id,assignment.id)
                result=CommandResult.succeeded(correlation_id,reference_id=version.id,state=assessment.state,version=assessment.lock_version)
            u.aggregates.put_assessment(assessment)
            self._store(u,op,assessment.id,actor,request_id,fp,result);u.commit();return result

    @_command_boundary
    def sign_testing_personnel(self,actor:Actor,*,assessment_id:str,version_id:str,request_id:str,correlation_id:str,expected_version:int)->CommandResult:
        op="sign_testing_personnel";fp=self._fp({"version_id":version_id,"expected_version":expected_version})
        with self._uow() as u:
            if r:=self._replay(u,op,assessment_id,actor,request_id,fp):return r
            if e:=self._actor_error(u,actor):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*e)
            ctx=self._authorized(u,actor,assessment_id,Role.EMPLOYEE)
            if not ctx:return self._not_visible(u,actor,op,assessment_id,request_id,correlation_id,fp)
            assessment,assignment=ctx
            if assessment.lock_version!=expected_version:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._stale())
            if assessment.current_version_id!=version_id:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.SIGNATURE_VERSION_MISMATCH,"The signature version does not match the current assessment version.")
            version=u.aggregates.get_version(version_id)
            if not version or version.assessment_id!=assessment.id:return self._pointer_failure(u,actor,op,assessment_id,request_id,correlation_id)
            if assessment.state!=AssessmentState.AWAITING_TESTING_PERSONNEL.value:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.SIGNATURE_SEQUENCE_INVALID,"Testing Personnel signature is not available.")
            u.aggregates.add_signature(SignatureRecord(self._id("SIG"),version.id,SignatureRole.TESTING_PERSONNEL.value,actor.user_id,self._clock(),request_id))
            assessment.state=AssessmentState.AWAITING_TECHNICAL_SUPERVISOR.value;assessment.lock_version+=1
            u.aggregates.put_assessment(assessment)
            event=self._event(u,assignment,assessment,NotificationTrigger.TECHNICAL_SUPERVISOR_SIGNATURE_REQUIRED,"SYN-TS-001",self._clock(),correlation_id)
            self._audit(u,actor,"notification_event","notification",event.id,request_id,correlation_id,"Succeeded","Logical notification recorded",assessment.id,assignment.id)
            result=CommandResult.succeeded(correlation_id,reference_id=version.id,state=assessment.state,version=assessment.lock_version)
            self._success(u,op,assessment.id,actor,request_id,correlation_id,fp,result,"assessment_version",version.id,"Exact version acknowledged",assessment.id,assignment.id);return result

    @_command_boundary
    def finalize(self,actor:Actor,*,assessment_id:str,version_id:str,request_id:str,correlation_id:str,expected_version:int)->CommandResult:
        op="finalize";fp=self._fp({"version_id":version_id,"expected_version":expected_version})
        try:
            with self._uow() as u:
                if r:=self._replay(u,op,assessment_id,actor,request_id,fp):return r
                if e:=self._actor_error(u,actor):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*e)
                ctx=self._authorized(u,actor,assessment_id,Role.TECHNICAL_SUPERVISOR)
                if not ctx:return self._not_visible(u,actor,op,assessment_id,request_id,correlation_id,fp)
                assessment,assignment=ctx
                if assessment.lock_version!=expected_version:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*self._stale())
                if assessment.current_version_id!=version_id:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.SIGNATURE_VERSION_MISMATCH,"The signature version does not match the current assessment version.")
                version=u.aggregates.get_version(version_id)
                if not version or version.assessment_id!=assessment.id:return self._pointer_failure(u,actor,op,assessment_id,request_id,correlation_id)
                if assessment.state!=AssessmentState.AWAITING_TECHNICAL_SUPERVISOR.value or not u.aggregates.get_signature(version.id,SignatureRole.TESTING_PERSONNEL.value):
                    return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.SIGNATURE_SEQUENCE_INVALID,"Testing Personnel must sign first.")
                now=self._clock();completion=now.date()
                u.aggregates.add_signature(SignatureRecord(self._id("SIG"),version.id,SignatureRole.TECHNICAL_SUPERVISOR.value,actor.user_id,now,request_id))
                assessment.state=AssessmentState.FINALIZED.value;assessment.lock_version+=1
                u.aggregates.put_assessment(assessment)
                u.aggregates.finalize_version_state(version.id,locked=True,finalized_at=now)
                metadata={"assessment_id":assessment.id,"version_id":version.id,"version_number":version.number,"kind":"synthetic-summary","finalized_at":now.isoformat()}
                u.aggregates.add_document(DocumentRecord("SYN-ARTIFACT-001",version.id,f"synthetic://metadata/{version.id}","synthetic-summary","1",synthetic_artifact_hash(metadata),actor.user_id,now))
                u.aggregates.add_renewal(RenewalRecord("SYN-RENEWAL-001",version.id,assignment.id,completion,assignment.interval_value,assignment.interval_unit,add_calendar_months(completion,assignment.interval_value),assignment.configuration_version))
                event=self._event(u,assignment,assessment,NotificationTrigger.COMPLETED,"SYN-EMP-001",now,correlation_id)
                for action,kind,key,summary in (("technical_supervisor_signature","assessment_version",version.id,"Exact version signed"),("artifact_retained","assessment_document","SYN-ARTIFACT-001","Synthetic metadata hash retained"),("renewal_scheduled","renewal","SYN-RENEWAL-001","Synthetic renewal scheduled"),("notification_event","notification",event.id,"Completed logical notification recorded"),("finalize","assessment",assessment.id,"Exact version finalized and locked")):
                    self._audit(u,actor,action,kind,key,request_id,correlation_id,"Succeeded",summary,assessment.id,assignment.id)
                if self._fault:self._fault()
                result=CommandResult.succeeded(correlation_id,reference_id=version.id,state=assessment.state,version=assessment.lock_version)
                self._store(u,op,assessment.id,actor,request_id,fp,result);u.commit();return result
        except Exception:
            return CommandResult.failed(correlation_id,RejectionCode.DEPENDENCY_UNAVAILABLE,"The operation could not be completed.")

    @_command_boundary
    def create_scheduled_notification(self,actor:ServiceActor,*,assessment_id:str,trigger:NotificationTrigger,
            occurrence:datetime,request_id:str,correlation_id:str)->CommandResult:
        op="scheduled_notification";occurrence=_utc(occurrence)
        fp=self._fp({"trigger":trigger.value,"occurrence":occurrence.isoformat()})
        with self._uow() as u:
            if r:=self._replay(u,op,assessment_id,actor,request_id,fp):return r
            if e:=self._service_error(u,actor):return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,*e)
            if not self._capability(u,actor,"notification_events_and_attempts"):
                return self._not_visible(u,actor,op,assessment_id,request_id,correlation_id,fp)
            assessment=u.aggregates.get_assessment(assessment_id)
            assignment=u.aggregates.get_assignment(assessment.assignment_id) if assessment else None
            if not assessment or not assignment:return self._not_visible(u,actor,op,assessment_id,request_id,correlation_id,fp)
            allowed=(NotificationTrigger.UPCOMING_DUE,NotificationTrigger.DUE,NotificationTrigger.OVERDUE)
            active=assessment.state!=AssessmentState.FINALIZED.value
            valid=(trigger in allowed and active and ((trigger is NotificationTrigger.UPCOMING_DUE and occurrence.date()<assignment.due_date)
                or (trigger is NotificationTrigger.DUE and occurrence.date()==assignment.due_date)
                or (trigger is NotificationTrigger.OVERDUE and occurrence.date()>assignment.due_date)))
            if not valid:return self._reject(u,actor,op,assessment_id,request_id,correlation_id,fp,RejectionCode.INVALID_STATE,"The scheduled trigger is not valid for the authoritative date and state.")
            event=self._event(u,assignment,assessment,trigger,"SYN-EMP-001",occurrence,correlation_id)
            result=CommandResult.succeeded(correlation_id,reference_id=event.id,state="recorded")
            self._success(u,op,assessment.id,actor,request_id,correlation_id,fp,result,"notification",event.id,"Logical notification recorded",assessment.id,assignment.id);return result

    @_command_boundary
    def record_notification_attempt(self,actor:ServiceActor,*,event_id:str,adapter_request_id:str,
                                    correlation_id:str)->CommandResult:
        op="notification_attempt";fp=self._fp({"event_id":event_id,"adapter_request_id":adapter_request_id})
        with self._uow() as u:
            if r:=self._replay(u,op,event_id,actor,adapter_request_id,fp):return r
            if e:=self._service_error(u,actor):return self._reject(u,actor,op,event_id,adapter_request_id,correlation_id,fp,*e)
            if not self._capability(u,actor,"notification_events_and_attempts"):
                return self._not_visible(u,actor,op,event_id,adapter_request_id,correlation_id,fp)
            event=u.notifications.get_event(event_id)
            if not event:return self._not_visible(u,actor,op,event_id,adapter_request_id,correlation_id,fp)
            now=self._clock();minimal=MinimalNotification(event.id,event.recipient_user_id,event.template_version,event.record_ref,event.trigger,event.logical_identity,event.status,event.due_date)
            observed=NonDeliveringNotificationAdapter().deliver(minimal,adapter_request_id=adapter_request_id,attempted_at=now)
            attempt=NotificationAttemptRecord(self._id("ATTEMPT"),event.id,len(u.notifications.list_attempts(event.id))+1,adapter_request_id,now,observed.outcome,observed.manual_retry_allowed,observed.safe_failure_category)
            u.notifications.add_attempt(attempt);result=CommandResult.succeeded(correlation_id,reference_id=attempt.id,state=attempt.outcome)
            self._success(u,op,event.id,actor,adapter_request_id,correlation_id,fp,result,"notification",event.id,"Non-delivering attempt recorded",event.assessment_id,event.assignment_id);return result

    @_query_boundary
    def list_visible_assessments(self,actor:Actor,*,as_of:date,request_id:str,
            correlation_id:str,purpose:str|None=None,support_reference:str|None=None)->AssessmentQueryResult:
        with self._uow() as u:
            error=self._actor_error(u,actor,allow_platform_read=True)
            if error:
                if u.aggregates.get_user(actor.user_id):
                    self._audit(u,actor,"scoped_read_denied","report","assessment_status",request_id,correlation_id,"Denied","User is inactive")
                    u.commit()
                return AssessmentQueryResult("Rejected",correlation_id,(),error[0].value,error[1])
            effective=[r for r in u.aggregates.list_roles(actor.user_id) if self._role_effective(r)]
            diagnostic=any(r.role==Role.PLATFORM_ADMIN.value and r.configuration_scope=="diagnostic" for r in effective)
            if diagnostic and (not purpose or not purpose.strip() or not support_reference or not support_reference.strip()):
                self._audit(u,actor,"diagnostic_read_denied","report","assessment_status",request_id,correlation_id,"Denied","Diagnostic purpose or reference missing")
                u.commit();return AssessmentQueryResult("Rejected",correlation_id,(),RejectionCode.FORBIDDEN.value,"Diagnostic purpose and reference are required.")
            employee=u.aggregates.get_user(actor.user_id).employee_id
            scope=effective_scope(actor.user_id,employee,tuple(effective),self._clock())
            accesses=u.queries.list_assessment_access(scope)
            rows=tuple(AssessmentSummary(x.assessment.id,x.assignment.id,x.assessment.state,x.assignment.due_date,
                is_overdue(due_date=x.assignment.due_date,as_of=as_of,active=x.assessment.state!=AssessmentState.FINALIZED.value),x.current_version_number) for x in accesses)
            for x in accesses:self._audit(u,actor,"diagnostic_read" if diagnostic else "scoped_read","assessment",x.assessment.id,request_id,correlation_id,"Succeeded","Authorized scoped record read",x.assessment.id,x.assignment.id,purpose.strip() if purpose else None,support_reference.strip() if support_reference else None)
            if not rows:self._audit(u,actor,"scoped_read_denied","report","assessment_status",request_id,correlation_id,"Denied","No visible records")
            u.commit();return AssessmentQueryResult.succeeded(correlation_id,rows)

    def _authorized(self,u:UnitOfWork,actor:Actor,assessment_id:str,role:Role)->tuple[AssessmentRecord,AssignmentRecord]|None:
        assessment=u.aggregates.get_assessment(assessment_id)
        assignment=u.aggregates.get_assignment(assessment.assignment_id) if assessment else None
        user=u.aggregates.get_user(actor.user_id)
        if not assessment or not assignment or not user:return None
        relationship={Role.ASSESSOR:assignment.assessor_id,Role.EMPLOYEE:assignment.employee_id,Role.TECHNICAL_SUPERVISOR:assignment.technical_supervisor_id}.get(role)
        return (assessment,assignment) if relationship==user.employee_id and self._scope(u,actor,role,assessment=assessment.id) else None

    def _draft(self,u:UnitOfWork,assessment:AssessmentRecord)->DraftRecord|None:
        row=u.aggregates.get_draft(assessment.current_draft_id) if assessment.current_draft_id else None
        return row if row and row.assessment_id==assessment.id else None

    def _version(self,u:UnitOfWork,assessment:AssessmentRecord,version_id:str)->VersionRecord|None:
        row=u.aggregates.get_version(version_id)
        return row if assessment.current_version_id==version_id and row and row.assessment_id==assessment.id else None

    def _effective_roles(self,u:UnitOfWork,actor:Actor)->set[str]:
        return {r.role for r in u.aggregates.list_roles(actor.user_id) if self._role_effective(r)}

    def _role_effective(self,row:RoleScopeRecord)->bool:
        now=self._clock();return _utc(row.starts_at)<=now and (row.ends_at is None or _utc(row.ends_at)>now)

    def _scope(self,u:UnitOfWork,actor:Actor,role:Role,*,assessment:str|None=None,team:str|None=None,configuration:str|None=None)->bool:
        now=self._clock()
        for row in u.aggregates.list_roles(actor.user_id):
            if row.role!=role.value or _utc(row.starts_at)>now or (row.ends_at and _utc(row.ends_at)<=now):continue
            if assessment is not None and row.assessment_id==assessment:return True
            if team is not None and row.team_id==team:return True
            if configuration is not None and row.configuration_scope==configuration:return True
        return False

    def _actor_error(self,u:UnitOfWork,actor:Actor,*,allow_platform_read:bool=False)->tuple[RejectionCode,str]|None:
        user=u.aggregates.get_user(actor.user_id)
        if not user:return RejectionCode.UNAUTHENTICATED,"Authentication is required."
        if not user.active:return RejectionCode.FORBIDDEN,"Access is not permitted."
        if not allow_platform_read and Role.PLATFORM_ADMIN.value in self._effective_roles(u,actor):
            return RejectionCode.FORBIDDEN,"Platform administration is read-only."
        return None

    def _service_error(self,u:UnitOfWork,actor:ServiceActor)->tuple[RejectionCode,str]|None:
        if not isinstance(actor,ServiceActor):return RejectionCode.FORBIDDEN,"Access is not permitted."
        principal=u.aggregates.get_service_principal(actor.principal_id)
        if not principal:return RejectionCode.UNAUTHENTICATED,"Authentication is required."
        if not principal.active:return RejectionCode.FORBIDDEN,"Access is not permitted."
        return None

    def _capability(self,u:UnitOfWork,actor:ServiceActor,capability:str)->bool:
        now=self._clock()
        return any(row.capability==capability and _utc(row.starts_at)<=now and
            (row.ends_at is None or _utc(row.ends_at)>now)
            for row in u.aggregates.list_capabilities(actor.principal_id))

    @staticmethod
    def _actor_ref(actor:Actor|ServiceActor)->str:
        return actor.user_id if isinstance(actor,Actor) else actor.principal_id

    def _known(self,u:UnitOfWork,actor:Actor|ServiceActor)->bool:
        if isinstance(actor,Actor):return u.aggregates.get_user(actor.user_id) is not None
        return u.aggregates.get_service_principal(actor.principal_id) is not None

    def _event(self,u:UnitOfWork,assignment:AssignmentRecord,assessment:AssessmentRecord,trigger:NotificationTrigger,recipient:str,occurrence:datetime,correlation_id:str)->NotificationEventRecord:
        occurrence=_utc(occurrence);identity=f"{assessment.id}:{trigger.value}:{recipient}:prototype-v1:{occurrence.isoformat()}"
        if row:=u.notifications.get_event_by_identity(identity):return row
        row=NotificationEventRecord(self._id("EVENT"),assignment.id,assessment.id,trigger.value,recipient,"prototype-v1",assessment.id,occurrence,assessment.state,assignment.due_date,identity,correlation_id)
        u.notifications.add_event(row);return row

    def _replay(self,u:UnitOfWork,op:str,target:str,actor:Actor|ServiceActor,request_id:str,fp:str)->CommandResult|None:
        actor_ref=self._actor_ref(actor);row=u.idempotency.get(op,target,actor_ref,request_id)
        if not row:return None
        if row.fingerprint!=fp:
            self._audit(u,actor,"idempotency_conflict","request",target,request_id,
                row.result.correlation_id,"Denied","Request identity reused with different input")
            u.commit()
            return CommandResult.rejected(row.result.correlation_id,RejectionCode.IDEMPOTENCY_CONFLICT,"The request identity was already used with different input.")
        return CommandResult(row.result.outcome,row.result.correlation_id,row.result.reference_id,row.result.state,row.result.version,True,row.result.code,row.result.message)

    def _store(self,u:UnitOfWork,op:str,target:str,actor:Actor|ServiceActor,request_id:str,fp:str,result:CommandResult)->None:
        u.idempotency.add(IdempotencyRecord(op,target,self._actor_ref(actor),request_id,fp,result))

    def _success(self,u:UnitOfWork,op:str,target:str,actor:Actor,request_id:str,correlation_id:str,fp:str,result:CommandResult,entity_type:str,entity_id:str,summary:str,assessment_id:str|None=None,assignment_id:str|None=None)->None:
        self._audit(u,actor,op,entity_type,entity_id,request_id,correlation_id,"Succeeded",summary,assessment_id,assignment_id);self._store(u,op,target,actor,request_id,fp,result);u.commit()

    def _reject(self,u:UnitOfWork,actor:Actor|ServiceActor,op:str,target:str,request_id:str,correlation_id:str,fp:str,code:RejectionCode,message:str,*,audit:bool=True)->CommandResult:
        result=CommandResult.rejected(correlation_id,code,message)
        if self._known(u,actor):
            if audit:self._audit(u,actor,op,"record",target,request_id,correlation_id,"Denied",message)
            self._store(u,op,target,actor,request_id,fp,result);u.commit()
        return result

    def _not_visible(self,u:UnitOfWork,actor:Actor,op:str,target:str,request_id:str,correlation_id:str,fp:str)->CommandResult:
        return self._reject(u,actor,op,target,request_id,correlation_id,fp,RejectionCode.NOT_FOUND_OR_NOT_VISIBLE,"The record was not found or is not visible.")

    def _pointer_failure(self,u:UnitOfWork,actor:Actor,op:str,target:str,request_id:str,correlation_id:str)->CommandResult:
        self._audit(u,actor,op,"assessment",target,request_id,correlation_id,"Failed","Authoritative child pointer mismatch");u.commit()
        return CommandResult.failed(correlation_id,RejectionCode.DEPENDENCY_UNAVAILABLE,"The operation could not be completed.")

    def _audit(self,u:UnitOfWork,actor:Actor|ServiceActor,action:str,entity_type:str,entity_id:str,request_id:str,correlation_id:str,outcome:str,summary:str,assessment_id:str|None=None,assignment_id:str|None=None,support_purpose:str|None=None,support_reference:str|None=None)->None:
        u.audits.append(AuditRecord(id=self._id("AUDIT"),actor_id=self._actor_ref(actor),
            action=action,entity_type=entity_type,entity_id=entity_id,observed_at=self._clock(),
            outcome=outcome,request_id=request_id,correlation_id=correlation_id,summary=summary,
            assessment_id=assessment_id,assignment_id=assignment_id,support_purpose=support_purpose,
            support_reference=support_reference,actor_kind="service_principal" if isinstance(actor,ServiceActor) else "user"))

    @staticmethod
    def _fp(value:object)->str:return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
    @staticmethod
    def _stale()->tuple[RejectionCode,str]:return RejectionCode.STALE_VERSION,"The record changed; reload and retry."
    @staticmethod
    def _invalid()->tuple[RejectionCode,str]:return RejectionCode.INVALID_STATE,"The operation is not available in the current state."

def build_workflow_service(uow_factory:UnitOfWorkFactory,*,clock:Callable[[],datetime],id_factory:Callable[[str],str]=_id,finalization_fault:Callable[[],None]|None=None)->WorkflowService:
    return WorkflowService(uow_factory,clock=clock,id_factory=id_factory,finalization_fault=finalization_fault)
