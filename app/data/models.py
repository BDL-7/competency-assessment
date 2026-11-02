"""Portable SQLAlchemy mappings for the approved synthetic workflow."""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import (
    Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer,
    MetaData, String, Text, UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def restricted_fk(target: str) -> ForeignKey:
    """Create an a retained-evidence foreign key with restricted deletion."""

    return ForeignKey(target, ondelete="RESTRICT")


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s", "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )


class Team(CreatedAtMixin, Base):
    __tablename__ = "team"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    display_label: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    configuration_owner_ref: Mapped[str] = mapped_column(String(128), nullable=False)


class Employee(CreatedAtMixin, Base):
    __tablename__ = "employee"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    team_id: Mapped[str] = mapped_column(restricted_fk("team.id"), nullable=False, index=True)
    display_label: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role_context: Mapped[str | None] = mapped_column(String(200))
    source_lineage: Mapped[str | None] = mapped_column(Text)


class ApplicationUser(CreatedAtMixin, Base):
    __tablename__ = "application_user"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    identity_provider_subject: Mapped[str] = mapped_column(
        String(200), nullable=False, unique=True
    )
    tenant_ref: Mapped[str | None] = mapped_column(String(128))
    is_mock_identity: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    employee_id: Mapped[str | None] = mapped_column(
        restricted_fk("employee.id"), unique=True
    )


class RoleAssignment(CreatedAtMixin, Base):
    __tablename__ = "role_assignment"
    __table_args__ = (
        CheckConstraint(
            "team_id IS NOT NULL OR assessment_id IS NOT NULL OR configuration_scope IS NOT NULL",
            name="explicit_scope_required",
        ),
        Index("ix_role_effective_scope", "user_id", "role_name", "starts_at", "ends_at"),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(restricted_fk("application_user.id"), nullable=False)
    role_name: Mapped[str] = mapped_column(String(64), nullable=False)
    team_id: Mapped[str | None] = mapped_column(restricted_fk("team.id"))
    assessment_id: Mapped[str | None] = mapped_column(restricted_fk("assessment.id"))
    configuration_scope: Mapped[str | None] = mapped_column(String(128))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_by_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    review_due_date: Mapped[date | None] = mapped_column(Date)


class TestSystem(CreatedAtMixin, Base):
    __tablename__ = "test_system"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    display_label: Mapped[str] = mapped_column(String(200), nullable=False)
    owner_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    approval_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_non_clia_applicable: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )


class ProcessGrouping(CreatedAtMixin, Base):
    __tablename__ = "process_grouping"
    __table_args__ = (CheckConstraint("interval_value > 0", name="positive_interval"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    team_id: Mapped[str] = mapped_column(restricted_fk("team.id"), nullable=False, index=True)
    display_label: Mapped[str] = mapped_column(String(200), nullable=False)
    owner_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    applicability: Mapped[str] = mapped_column(String(100), nullable=False)
    configuration_version: Mapped[str] = mapped_column(String(64), nullable=False)
    interval_value: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_unit: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class ProcessGroupingTestSystem(CreatedAtMixin, Base):
    __tablename__ = "process_grouping_test_system"
    __table_args__ = (
        UniqueConstraint("process_grouping_id", "test_system_id"),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    process_grouping_id: Mapped[str] = mapped_column(
        restricted_fk("process_grouping.id"), nullable=False, index=True
    )
    test_system_id: Mapped[str] = mapped_column(
        restricted_fk("test_system.id"), nullable=False, index=True
    )


class Assignment(CreatedAtMixin, Base):
    __tablename__ = "assignment"
    __table_args__ = (CheckConstraint("lock_version > 0", name="positive_lock_version"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    employee_id: Mapped[str] = mapped_column(restricted_fk("employee.id"), nullable=False, index=True)
    team_id: Mapped[str] = mapped_column(restricted_fk("team.id"), nullable=False, index=True)
    process_grouping_id: Mapped[str] = mapped_column(
        restricted_fk("process_grouping.id"), nullable=False
    )
    assigned_team_lead_id: Mapped[str] = mapped_column(
        restricted_fk("employee.id"), nullable=False
    )
    assessor_id: Mapped[str] = mapped_column(
        restricted_fk("employee.id"), nullable=False, index=True
    )
    technical_supervisor_id: Mapped[str] = mapped_column(
        restricted_fk("employee.id"), nullable=False, index=True
    )
    interval_value_snapshot: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_unit_snapshot: Mapped[str] = mapped_column(String(32), nullable=False)
    configuration_version_snapshot: Mapped[str] = mapped_column(String(64), nullable=False)
    basis_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    scheduling_state: Mapped[str] = mapped_column(String(32), nullable=False)
    predecessor_assignment_id: Mapped[str | None] = mapped_column(
        restricted_fk("assignment.id")
    )
    successor_assignment_id: Mapped[str | None] = mapped_column(
        restricted_fk("assignment.id")
    )
    source_lineage: Mapped[str | None] = mapped_column(Text)
    lock_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )


class Assessment(CreatedAtMixin, Base):
    __tablename__ = "assessment"
    __table_args__ = (CheckConstraint("lock_version > 0", name="positive_lock_version"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assignment_id: Mapped[str] = mapped_column(
        restricted_fk("assignment.id"), nullable=False, unique=True
    )
    lifecycle_state: Mapped[str] = mapped_column(String(64), nullable=False)
    # Nullable navigation pointers avoid a physical foreign-key cycle. The
    # authoritative child rows retain non-null restricted assessment FKs.
    current_draft_id: Mapped[str | None] = mapped_column(String(64))
    current_version_id: Mapped[str | None] = mapped_column(String(64))
    lock_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )


class AssessmentDraft(CreatedAtMixin, Base):
    __tablename__ = "assessment_draft"
    __table_args__ = (CheckConstraint("lock_version > 0", name="positive_lock_version"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(
        restricted_fk("assessment.id"), nullable=False, index=True
    )
    lock_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    employee_id: Mapped[str] = mapped_column(restricted_fk("employee.id"), nullable=False)
    assessor_id: Mapped[str] = mapped_column(restricted_fk("employee.id"), nullable=False)
    technical_supervisor_id: Mapped[str] = mapped_column(
        restricted_fk("employee.id"), nullable=False
    )
    configuration_version_snapshot: Mapped[str] = mapped_column(String(64), nullable=False)
    assessment_context: Mapped[str | None] = mapped_column(Text)
    assessment_type: Mapped[str | None] = mapped_column(Text)
    process: Mapped[str | None] = mapped_column(Text)
    assessment_method: Mapped[str | None] = mapped_column(Text)
    specimen_context: Mapped[str | None] = mapped_column(Text)
    testing_context: Mapped[str | None] = mapped_column(Text)
    problem_solving_evidence: Mapped[str | None] = mapped_column(Text)
    protocol_outcome: Mapped[str | None] = mapped_column(Text)
    comments: Mapped[str | None] = mapped_column(Text)
    followup_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    followup_description: Mapped[str | None] = mapped_column(Text)
    created_by_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    updated_by_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )


class AssessmentDraftElement(CreatedAtMixin, Base):
    """Mutable element work owned by one optimistic-concurrency draft."""

    __tablename__ = "assessment_draft_element"
    __table_args__ = (UniqueConstraint("assessment_draft_id", "element_ref"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assessment_draft_id: Mapped[str] = mapped_column(
        restricted_fk("assessment_draft.id"), nullable=False, index=True
    )
    element_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    recorded_result: Mapped[str | None] = mapped_column(String(64))
    evidence: Mapped[str | None] = mapped_column(Text)
    comments: Mapped[str | None] = mapped_column(Text)
    has_gap: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    followup_status: Mapped[str | None] = mapped_column(String(64))
    followup_description: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )


class AssessmentVersion(CreatedAtMixin, Base):
    __tablename__ = "assessment_version"
    __table_args__ = (
        UniqueConstraint("assessment_id", "version_number"),
        CheckConstraint("version_number > 0", name="positive_version_number"),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assessment_id: Mapped[str] = mapped_column(
        restricted_fk("assessment.id"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_draft_id: Mapped[str] = mapped_column(
        restricted_fk("assessment_draft.id"), nullable=False
    )
    employee_id: Mapped[str] = mapped_column(restricted_fk("employee.id"), nullable=False)
    assigned_team_lead_id: Mapped[str] = mapped_column(
        restricted_fk("employee.id"), nullable=False
    )
    assessor_id: Mapped[str] = mapped_column(restricted_fk("employee.id"), nullable=False)
    technical_supervisor_id: Mapped[str] = mapped_column(
        restricted_fk("employee.id"), nullable=False
    )
    configuration_version_snapshot: Mapped[str] = mapped_column(String(64), nullable=False)
    assessment_context: Mapped[str] = mapped_column(Text, nullable=False)
    assessment_type: Mapped[str] = mapped_column(Text, nullable=False)
    process: Mapped[str] = mapped_column(Text, nullable=False)
    assessment_method: Mapped[str] = mapped_column(Text, nullable=False)
    specimen_context: Mapped[str] = mapped_column(Text, nullable=False)
    testing_context: Mapped[str] = mapped_column(Text, nullable=False)
    problem_solving_evidence: Mapped[str] = mapped_column(Text, nullable=False)
    protocol_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    comments: Mapped[str | None] = mapped_column(Text)
    followup_required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    followup_description: Mapped[str | None] = mapped_column(Text)
    created_by_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    supersedes_version_id: Mapped[str | None] = mapped_column(
        restricted_fk("assessment_version.id")
    )
    is_locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    finalized_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AssessmentElement(CreatedAtMixin, Base):
    __tablename__ = "assessment_element"
    __table_args__ = (UniqueConstraint("assessment_version_id", "element_ref"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assessment_version_id: Mapped[str] = mapped_column(
        restricted_fk("assessment_version.id"), nullable=False, index=True
    )
    element_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    recorded_result: Mapped[str] = mapped_column(String(64), nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    comments: Mapped[str | None] = mapped_column(Text)
    has_gap: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    followup_status: Mapped[str | None] = mapped_column(String(64))
    followup_description: Mapped[str | None] = mapped_column(Text)


class Signature(CreatedAtMixin, Base):
    __tablename__ = "signature"
    __table_args__ = (
        UniqueConstraint("assessment_version_id", "signature_role"),
        UniqueConstraint(
            "request_identity", "assessment_version_id", "signature_role", "signer_user_id"
        ),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assessment_version_id: Mapped[str] = mapped_column(
        restricted_fk("assessment_version.id"), nullable=False, index=True
    )
    signature_role: Mapped[str] = mapped_column(String(64), nullable=False)
    signer_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    authentication_context: Mapped[str] = mapped_column(String(200), nullable=False)
    request_identity: Mapped[str] = mapped_column(String(128), nullable=False)


class AssessmentDocument(CreatedAtMixin, Base):
    __tablename__ = "assessment_document"
    __table_args__ = (UniqueConstraint("assessment_version_id", "document_kind"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assessment_version_id: Mapped[str] = mapped_column(
        restricted_fk("assessment_version.id"), nullable=False, index=True
    )
    private_object_ref: Mapped[str] = mapped_column(String(500), nullable=False)
    document_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    document_version: Mapped[str] = mapped_column(String(64), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    uploaded_by_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Renewal(CreatedAtMixin, Base):
    __tablename__ = "renewal"
    __table_args__ = (UniqueConstraint("finalized_assessment_version_id"),)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    finalized_assessment_version_id: Mapped[str] = mapped_column(
        restricted_fk("assessment_version.id"), nullable=False
    )
    assignment_id: Mapped[str] = mapped_column(
        restricted_fk("assignment.id"), nullable=False
    )
    completion_date: Mapped[date] = mapped_column(Date, nullable=False)
    interval_value: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_unit: Mapped[str] = mapped_column(String(32), nullable=False)
    next_due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    configuration_version_snapshot: Mapped[str] = mapped_column(String(64), nullable=False)


class NotificationEvent(CreatedAtMixin, Base):
    __tablename__ = "notification_event"
    __table_args__ = (
        UniqueConstraint(
            "record_ref", "trigger_name", "recipient_user_id",
            "template_version", "scheduled_occurrence",
        ),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    assignment_id: Mapped[str] = mapped_column(
        restricted_fk("assignment.id"), nullable=False, index=True
    )
    assessment_id: Mapped[str | None] = mapped_column(
        restricted_fk("assessment.id"), index=True
    )
    trigger_name: Mapped[str] = mapped_column(String(64), nullable=False)
    recipient_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    template_version: Mapped[str] = mapped_column(String(64), nullable=False)
    record_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    scheduled_occurrence: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status_context: Mapped[str | None] = mapped_column(String(64))
    date_context: Mapped[date | None] = mapped_column(Date)
    idempotency_identity: Mapped[str] = mapped_column(
        String(200), nullable=False, unique=True
    )
    event_status: Mapped[str] = mapped_column(String(32), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False)


class NotificationAttempt(CreatedAtMixin, Base):
    __tablename__ = "notification_attempt"
    __table_args__ = (
        UniqueConstraint(
            "notification_event_id", "attempt_ordinal",
            name="uq_notification_attempt_event_ordinal",
        ),
        UniqueConstraint(
            "notification_event_id", "adapter_request_ref",
            name="uq_notification_attempt_event_request",
        ),
        CheckConstraint("attempt_ordinal > 0", name="positive_attempt_ordinal"),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    notification_event_id: Mapped[str] = mapped_column(
        restricted_fk("notification_event.id"), nullable=False, index=True
    )
    attempt_ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    adapter_request_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    outcome: Mapped[str] = mapped_column(String(32), nullable=False)
    retry_eligible: Mapped[bool] = mapped_column(Boolean, nullable=False)
    failure_category: Mapped[str | None] = mapped_column(String(64))


class AuditEvent(Base):
    __tablename__ = "audit_event"
    __table_args__ = (
        UniqueConstraint("request_identity", "action", "entity_type", "entity_id"),
        Index("ix_audit_entity_time", "entity_type", "entity_id", "observed_at"),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    actor_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    assessment_id: Mapped[str | None] = mapped_column(
        restricted_fk("assessment.id"), index=True
    )
    assignment_id: Mapped[str | None] = mapped_column(
        restricted_fk("assignment.id"), index=True
    )
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    outcome: Mapped[str] = mapped_column(String(32), nullable=False)
    request_identity: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    change_summary: Mapped[str | None] = mapped_column(Text)
    support_purpose: Mapped[str | None] = mapped_column(String(200))
    support_reference: Mapped[str | None] = mapped_column(String(128))


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_record"
    __table_args__ = (
        UniqueConstraint(
            "operation_name", "target_ref", "actor_user_id", "request_identity"
        ),
    )
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    operation_name: Mapped[str] = mapped_column(String(100), nullable=False)
    target_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    actor_user_id: Mapped[str] = mapped_column(
        restricted_fk("application_user.id"), nullable=False
    )
    request_identity: Mapped[str] = mapped_column(String(128), nullable=False)
    request_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False)
    result_type: Mapped[str] = mapped_column(String(32), nullable=False)
    result_ref: Mapped[str | None] = mapped_column(String(128))
    resulting_state: Mapped[str | None] = mapped_column(String(64))
    resulting_version: Mapped[int | None] = mapped_column(Integer)
    reason_code: Mapped[str | None] = mapped_column(String(64))
    safe_message: Mapped[str | None] = mapped_column(String(500))
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
