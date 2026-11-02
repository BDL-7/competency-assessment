"""Framework-neutral workflow records and persistence ports."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Callable, Protocol

from app.domain import CommandResult

@dataclass(frozen=True)
class Actor: user_id: str
@dataclass(frozen=True)
class ServiceActor: principal_id: str

@dataclass(frozen=True)
class DraftContent:
    assessment_context: str; assessment_type: str; process: str
    assessment_method: str; specimen_context: str; testing_context: str
    problem_solving_evidence: str; protocol_outcome: str; comments: str=""
    element_ref: str="SYN-ELEMENT-03"; element_result: str="unsuccessful"
    element_evidence: str="Synthetic evidence"; has_gap: bool=True

@dataclass
class UserRecord: id: str; employee_id: str|None; active: bool=True
@dataclass
class ServicePrincipalRecord: id: str; active: bool=True
@dataclass
class CapabilityGrantRecord:
    principal_id: str; capability: str; starts_at: datetime
    ends_at: datetime|None=None
@dataclass
class RoleScopeRecord:
    id: str; user_id: str; role: str; starts_at: datetime
    ends_at: datetime|None=None; team_id: str|None=None
    assessment_id: str|None=None; configuration_scope: str|None=None
@dataclass
class ConfigurationRecord:
    id: str="SYN-CFG-001"; team_id: str="SYN-TEAM-ALPHA"
    process_id: str="SYN-PROCESS-01"; test_system_id: str="SYN-TEST-SYSTEM-01"
    interval_value: int=12; interval_unit: str="calendar_months"
@dataclass
class AssignmentRecord:
    id: str; employee_id: str; team_id: str; assigned_team_lead_id: str
    assessor_id: str; technical_supervisor_id: str; process_id: str
    configuration_version: str; basis_date: date; due_date: date; state: str="Scheduled"
    lock_version: int=1; interval_value: int=12; interval_unit: str="calendar_months"
    predecessor_id: str|None=None; successor_id: str|None=None
@dataclass
class AssessmentRecord:
    id: str; assignment_id: str; state: str="Assigned"; lock_version: int=1
    current_draft_id: str|None=None; current_version_id: str|None=None
@dataclass
class DraftRecord:
    id: str; assessment_id: str; employee_id: str; assessor_id: str
    technical_supervisor_id: str; configuration_version: str; created_by: str
    updated_by: str; lock_version: int=1; content: DraftContent|None=None
    followup_description: str|None=None
@dataclass
class DraftElementRecord:
    id: str; draft_id: str; element_ref: str; result: str; evidence: str
    has_gap: bool; followup_description: str|None=None
@dataclass(frozen=True)
class VersionRecord:
    id: str; assessment_id: str; number: int; source_draft_id: str
    employee_id: str; assigned_team_lead_id: str; assessor_id: str
    technical_supervisor_id: str; configuration_version: str; content: DraftContent
    followup_description: str|None; created_by: str; supersedes_id: str|None=None
    locked: bool=False; finalized_at: datetime|None=None
@dataclass(frozen=True)
class VersionElementRecord:
    id: str; version_id: str; element_ref: str; result: str; evidence: str
    has_gap: bool; followup_description: str|None
@dataclass(frozen=True)
class SignatureRecord:
    id: str; version_id: str; role: str; signer_user_id: str
    signed_at: datetime; request_id: str
@dataclass(frozen=True)
class DocumentRecord:
    id: str; version_id: str; object_ref: str; kind: str; document_version: str
    sha256: str; actor_id: str; verified_at: datetime
@dataclass(frozen=True)
class RenewalRecord:
    id: str; version_id: str; assignment_id: str; completion_date: date
    interval_value: int; interval_unit: str; next_due_date: date
    configuration_version: str
@dataclass(frozen=True)
class NotificationEventRecord:
    id: str; assignment_id: str; assessment_id: str; trigger: str
    recipient_user_id: str; template_version: str; record_ref: str
    occurrence: datetime; status: str; due_date: date; logical_identity: str
    correlation_id: str
@dataclass(frozen=True)
class NotificationAttemptRecord:
    id: str; event_id: str; ordinal: int; adapter_request_id: str
    attempted_at: datetime; outcome: str; manual_retry_allowed: bool
    failure_category: str|None
@dataclass(frozen=True)
class AuditRecord:
    id: str; actor_id: str; action: str; entity_type: str; entity_id: str
    observed_at: datetime; outcome: str; request_id: str; correlation_id: str
    summary: str; assessment_id: str|None=None; assignment_id: str|None=None
    support_purpose: str|None=None; support_reference: str|None=None
    actor_kind: str="user"
@dataclass(frozen=True)
class IdempotencyRecord:
    operation: str; target: str; actor_id: str; request_id: str
    fingerprint: str; result: CommandResult
@dataclass(frozen=True)
class AssessmentAccessRecord:
    assessment: AssessmentRecord; assignment: AssignmentRecord
    current_version_number: int|None
@dataclass(frozen=True)
class AssessmentQueryScope:
    actor_user_id: str; employee_id: str|None
    own_employee_id: str|None=None; own_assessment_ids: tuple[str,...]=()
    team_ids: tuple[str,...]=(); assessor_assessment_ids: tuple[str,...]=()
    technical_supervisor_assessment_ids: tuple[str,...]=()
    configuration_versions: tuple[str,...]=(); diagnostic: bool=False
@dataclass(frozen=True)
class AssessmentQueryResult:
    outcome: str; correlation_id: str; items: tuple[object,...]=()
    code: str|None=None; message: str|None=None
    @classmethod
    def succeeded(cls,correlation_id:str,items:tuple[object,...])->"AssessmentQueryResult":
        return cls("Succeeded",correlation_id,items)
    @classmethod
    def failed(cls,correlation_id:str)->"AssessmentQueryResult":
        return cls("Failed",correlation_id,(),"DEPENDENCY_UNAVAILABLE","The operation could not be completed.")

class AggregateRepository(Protocol):
    def user_count(self)->int: ...
    def get_user(self,user_id:str)->UserRecord|None: ...
    def add_user(self,record:UserRecord)->None: ...
    def get_service_principal(self,principal_id:str)->ServicePrincipalRecord|None: ...
    def add_service_principal(self,record:ServicePrincipalRecord)->None: ...
    def list_capabilities(self,principal_id:str)->tuple[CapabilityGrantRecord,...]: ...
    def add_capability(self,record:CapabilityGrantRecord)->None: ...
    def list_roles(self,user_id:str)->tuple[RoleScopeRecord,...]: ...
    def add_role(self,record:RoleScopeRecord)->None: ...
    def get_configuration(self,record_id:str)->ConfigurationRecord|None: ...
    def add_configuration(self,record:ConfigurationRecord)->None: ...
    def get_assignment(self,record_id:str)->AssignmentRecord|None: ...
    def add_assignment(self,record:AssignmentRecord)->None: ...
    def put_assignment(self,record:AssignmentRecord)->None: ...
    def get_assessment(self,record_id:str)->AssessmentRecord|None: ...
    def add_assessment(self,record:AssessmentRecord)->None: ...
    def put_assessment(self,record:AssessmentRecord)->None: ...
    def get_draft(self,record_id:str)->DraftRecord|None: ...
    def add_draft(self,record:DraftRecord)->None: ...
    def put_draft(self,record:DraftRecord)->None: ...
    def list_draft_elements(self,draft_id:str)->tuple[DraftElementRecord,...]: ...
    def put_draft_element(self,record:DraftElementRecord)->None: ...
    def get_version(self,record_id:str)->VersionRecord|None: ...
    def list_versions(self,assessment_id:str)->tuple[VersionRecord,...]: ...
    def add_version(self,record:VersionRecord)->None: ...
    def finalize_version_state(self,version_id:str,*,locked:bool,finalized_at:datetime)->None: ...
    def add_version_element(self,record:VersionElementRecord)->None: ...
    def get_signature(self,version_id:str,role:str)->SignatureRecord|None: ...
    def add_signature(self,record:SignatureRecord)->None: ...
    def add_document(self,record:DocumentRecord)->None: ...
    def add_renewal(self,record:RenewalRecord)->None: ...
class IdempotencyPort(Protocol):
    def get(self,operation:str,target:str,actor_id:str,request_id:str)->IdempotencyRecord|None: ...
    def add(self,record:IdempotencyRecord)->None: ...
class AuditAppendPort(Protocol):
    def append(self,record:AuditRecord)->None: ...
class NotificationPort(Protocol):
    def get_event_by_identity(self,identity:str)->NotificationEventRecord|None: ...
    def get_event(self,event_id:str)->NotificationEventRecord|None: ...
    def add_event(self,record:NotificationEventRecord)->None: ...
    def get_attempt(self,event_id:str,request_id:str)->NotificationAttemptRecord|None: ...
    def list_attempts(self,event_id:str)->tuple[NotificationAttemptRecord,...]: ...
    def add_attempt(self,record:NotificationAttemptRecord)->None: ...
class ScopedQueryPort(Protocol):
    def list_assessment_access(self,scope:AssessmentQueryScope)->tuple[AssessmentAccessRecord,...]: ...
class UnitOfWork(Protocol):
    aggregates: AggregateRepository; idempotency: IdempotencyPort
    audits: AuditAppendPort; notifications: NotificationPort; queries: ScopedQueryPort
    def __enter__(self)->UnitOfWork: ...
    def __exit__(self,exc_type:object,exc:object,traceback:object)->bool|None: ...
    def commit(self)->None: ...
    def rollback(self)->None: ...
UnitOfWorkFactory=Callable[[],UnitOfWork]
