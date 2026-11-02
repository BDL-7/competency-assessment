"""Stable application-service boundary for web composition."""
from app.services.contracts import (
    Actor, AggregateRepository, AssessmentAccessRecord, AssessmentQueryResult,
    AssessmentQueryScope, AssessmentRecord, CapabilityGrantRecord,
    AssignmentRecord, AuditAppendPort, AuditRecord, ConfigurationRecord,
    DocumentRecord, DraftContent, DraftElementRecord, DraftRecord,
    IdempotencyPort, IdempotencyRecord, NotificationAttemptRecord,
    NotificationEventRecord, NotificationPort, RenewalRecord, RoleScopeRecord,
    ScopedQueryPort, ServiceActor, ServicePrincipalRecord, SignatureRecord,
    UnitOfWork, UnitOfWorkFactory, UserRecord,
    VersionElementRecord, VersionRecord,
)
from app.services.workflow import WorkflowService, build_workflow_service

__all__ = [
    "Actor", "AggregateRepository", "AssessmentAccessRecord", "AssessmentQueryResult",
    "AssessmentQueryScope", "AssessmentRecord", "CapabilityGrantRecord",
    "AssignmentRecord", "AuditAppendPort", "AuditRecord", "ConfigurationRecord",
    "DocumentRecord", "DraftContent", "DraftElementRecord", "DraftRecord",
    "IdempotencyPort", "IdempotencyRecord", "NotificationAttemptRecord",
    "NotificationEventRecord", "NotificationPort", "RenewalRecord", "RoleScopeRecord",
    "ScopedQueryPort", "ServiceActor", "ServicePrincipalRecord", "SignatureRecord",
    "UnitOfWork", "UnitOfWorkFactory", "UserRecord",
    "VersionElementRecord", "VersionRecord", "WorkflowService", "build_workflow_service",
]
