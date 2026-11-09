"""In-memory S0-04A ports used only by framework-neutral service tests."""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass,field,replace

from app.services import *

@dataclass
class Store:
    users:dict=field(default_factory=dict);roles:list=field(default_factory=list)
    service_principals:dict=field(default_factory=dict);capabilities:list=field(default_factory=list)
    configurations:dict=field(default_factory=dict);assignments:dict=field(default_factory=dict)
    assessments:dict=field(default_factory=dict);drafts:dict=field(default_factory=dict)
    draft_elements:dict=field(default_factory=dict);versions:dict=field(default_factory=dict)
    version_elements:list=field(default_factory=list);signatures:dict=field(default_factory=dict)
    documents:list=field(default_factory=list);renewals:list=field(default_factory=list)
    events:dict=field(default_factory=dict);attempts:list=field(default_factory=list)
    audits:list=field(default_factory=list);idempotency:dict=field(default_factory=dict)
    last_scope:object|None=None

class FakeUnitOfWork:
    def __init__(self,store:Store,fail_on:set[str]):self.store=store;self.fail_on=fail_on;self.aggregates=self;self.idempotency=self;self.audits=self;self.notifications=self;self.queries=self;self.committed=False
    def __enter__(self):self.snapshot=deepcopy(self.store);return self
    def __exit__(self,typ,exc,tb):
        if typ or not self.committed:self.store.__dict__.update(self.snapshot.__dict__)
        return False
    def commit(self):self.committed=True
    def rollback(self):self.store.__dict__.update(self.snapshot.__dict__)
    def user_count(self):return len(self.store.users)
    def get_user(self,key):return self.store.users.get(key)
    def add_user(self,row):self.store.users[row.id]=row
    def get_service_principal(self,key):return self.store.service_principals.get(key)
    def add_service_principal(self,row):self.store.service_principals[row.id]=row
    def list_capabilities(self,key):return tuple(r for r in self.store.capabilities if r.principal_id==key)
    def add_capability(self,row):self.store.capabilities.append(row)
    def list_roles(self,key):return tuple(r for r in self.store.roles if r.user_id==key)
    def add_role(self,row):self.store.roles.append(row)
    def get_configuration(self,key):return self.store.configurations.get(key)
    def add_configuration(self,row):self.store.configurations[row.id]=row
    def get_assignment(self,key):return self.store.assignments.get(key)
    def add_assignment(self,row):
        if "add_assignment" in self.fail_on:raise RuntimeError("injected write failure")
        self.store.assignments[row.id]=row
    def put_assignment(self,row):self.store.assignments[row.id]=row
    def get_assessment(self,key):return self.store.assessments.get(key)
    def add_assessment(self,row):self.store.assessments[row.id]=row
    def put_assessment(self,row):self.store.assessments[row.id]=row
    def get_draft(self,key):return self.store.drafts.get(key)
    def add_draft(self,row):self.store.drafts[row.id]=row
    def put_draft(self,row):self.store.drafts[row.id]=row
    def list_draft_elements(self,key):return tuple(r for r in self.store.draft_elements.values() if r.draft_id==key)
    def put_draft_element(self,row):self.store.draft_elements[(row.draft_id,row.element_ref)]=row
    def get_version(self,key):return self.store.versions.get(key)
    def list_versions(self,key):return tuple(r for r in self.store.versions.values() if r.assessment_id==key)
    def add_version(self,row):self.store.versions[row.id]=row
    def finalize_version_state(self,version_id,*,locked,finalized_at):
        row=self.store.versions[version_id]
        self.store.versions[version_id]=replace(row,locked=locked,finalized_at=finalized_at)
    def add_version_element(self,row):self.store.version_elements.append(row)
    def get_signature(self,version_id,role):return self.store.signatures.get((version_id,role))
    def add_signature(self,row):self.store.signatures[(row.version_id,row.role)]=row
    def add_document(self,row):self.store.documents.append(row)
    def add_renewal(self,row):self.store.renewals.append(row)
    def get(self,operation,target,actor_id,request_id):return self.store.idempotency.get((operation,target,actor_id,request_id))
    def add(self,row):self.store.idempotency[(row.operation,row.target,row.actor_id,row.request_id)]=row
    def append(self,row):self.store.audits.append(row)
    def get_event_by_identity(self,key):return next((r for r in self.store.events.values() if r.logical_identity==key),None)
    def get_event(self,key):return self.store.events.get(key)
    def add_event(self,row):self.store.events[row.id]=row
    def get_attempt(self,event_id,request_id):return next((r for r in self.store.attempts if r.event_id==event_id and r.adapter_request_id==request_id),None)
    def list_attempts(self,event_id):return tuple(r for r in self.store.attempts if r.event_id==event_id)
    def add_attempt(self,row):self.store.attempts.append(row)
    def list_assessment_access(self,scope):
        if "query" in self.fail_on:raise RuntimeError("injected query failure")
        self.store.last_scope=scope
        rows=[]
        for assessment in self.store.assessments.values():
            assignment=self.store.assignments[assessment.assignment_id]
            allowed=(scope.diagnostic or assignment.configuration_version in scope.configuration_versions
                or assignment.team_id in scope.team_ids
                or assessment.id in scope.assessor_assessment_ids
                or assessment.id in scope.technical_supervisor_assessment_ids
                or (scope.own_employee_id==assignment.employee_id and assessment.id in scope.own_assessment_ids))
            if not allowed:continue
            version=self.store.versions.get(assessment.current_version_id)
            rows.append(AssessmentAccessRecord(assessment,assignment,version.number if version else None))
        return tuple(rows)

class FakeFactory:
    def __init__(self):self.store=Store();self.fail_on=set()
    def __call__(self):return FakeUnitOfWork(self.store,self.fail_on)
