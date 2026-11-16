"""Schema-compatible SQL support ports; no aggregate mutation or delivery."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Select, and_, or_, select
from sqlalchemy.orm import Session

from app.data import models
from app.domain import CommandResult, RejectionCode
from app.services import contracts


def _write_time(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Persisted event timestamps require an explicit timezone.")
    return value.astimezone(UTC)


def _read_time(value: datetime) -> datetime:
    # SQLite returns naive values for the UTC timestamps stored by these ports.
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def assessment_access_statement(
    scope: contracts.AssessmentQueryScope,
) -> Select[tuple[models.Assessment, models.Assignment]]:
    condition = or_(
        and_(models.Assignment.employee_id == scope.own_employee_id,
             models.Assessment.id.in_(scope.own_assessment_ids)),
        models.Assignment.team_id.in_(scope.team_ids),
        and_(models.Assignment.assessor_id == scope.employee_id,
             models.Assessment.id.in_(scope.assessor_assessment_ids)),
        and_(models.Assignment.technical_supervisor_id == scope.employee_id,
             models.Assessment.id.in_(scope.technical_supervisor_assessment_ids)),
        models.Assignment.configuration_version_snapshot.in_(scope.configuration_versions),
    )
    return (select(models.Assessment, models.Assignment)
            .join(models.Assignment, models.Assessment.assignment_id == models.Assignment.id)
            .where(True if scope.diagnostic else condition)
            .order_by(models.Assignment.due_date, models.Assessment.id))


class SqlScopedQueries:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_assessment_access(
        self, scope: contracts.AssessmentQueryScope,
    ) -> tuple[contracts.AssessmentAccessRecord, ...]:
        records = []
        for assessment, assignment in self._session.execute(assessment_access_statement(scope)):
            number = None
            if assessment.current_version_id is not None:
                number = self._session.scalar(select(models.AssessmentVersion.version_number).where(
                    models.AssessmentVersion.id == assessment.current_version_id,
                    models.AssessmentVersion.assessment_id == assessment.id,
                ))
                if number is None:
                    raise ValueError("Assessment current-version pointer is inconsistent.")
            records.append(contracts.AssessmentAccessRecord(
                assessment=contracts.AssessmentRecord(
                    id=assessment.id, assignment_id=assessment.assignment_id,
                    state=assessment.lifecycle_state, lock_version=assessment.lock_version,
                    current_draft_id=assessment.current_draft_id,
                    current_version_id=assessment.current_version_id,
                ),
                assignment=contracts.AssignmentRecord(
                    id=assignment.id, employee_id=assignment.employee_id,
                    team_id=assignment.team_id,
                    assigned_team_lead_id=assignment.assigned_team_lead_id,
                    assessor_id=assignment.assessor_id,
                    technical_supervisor_id=assignment.technical_supervisor_id,
                    process_id=assignment.process_grouping_id,
                    configuration_version=assignment.configuration_version_snapshot,
                    basis_date=assignment.basis_date, due_date=assignment.due_date,
                    state=assignment.scheduling_state, lock_version=assignment.lock_version,
                    interval_value=assignment.interval_value_snapshot,
                    interval_unit=assignment.interval_unit_snapshot,
                    predecessor_id=assignment.predecessor_assignment_id,
                    successor_id=assignment.successor_assignment_id,
                ),
                current_version_number=number,
            ))
        return tuple(records)


class SqlIdempotencyRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(
        self, operation: str, target: str, actor_id: str, request_id: str,
    ) -> contracts.IdempotencyRecord | None:
        row = self._session.scalar(select(models.IdempotencyRecord).where(
            models.IdempotencyRecord.operation_name == operation,
            models.IdempotencyRecord.target_ref == target,
            models.IdempotencyRecord.actor_user_id == actor_id,
            models.IdempotencyRecord.request_identity == request_id,
        ))
        if row is None:
            return None
        return contracts.IdempotencyRecord(
            operation=row.operation_name, target=row.target_ref,
            actor_id=row.actor_user_id, request_id=row.request_identity,
            fingerprint=row.request_fingerprint,
            result=CommandResult(
                outcome=row.result_type, correlation_id=row.correlation_id,
                reference_id=row.result_ref, state=row.resulting_state,
                version=row.resulting_version,
                code=RejectionCode(row.reason_code) if row.reason_code is not None else None,
                message=row.safe_message,
            ),
        )

    def add(self, record: contracts.IdempotencyRecord) -> None:
        if record.result.replayed:
            raise ValueError("Store the original command result, not a replay response.")
        result = record.result
        self._session.add(models.IdempotencyRecord(
            id=f"IDEMP-{uuid4().hex}", operation_name=record.operation,
            target_ref=record.target, actor_user_id=record.actor_id,
            request_identity=record.request_id, request_fingerprint=record.fingerprint,
            result_type=result.outcome, result_ref=result.reference_id,
            resulting_state=result.state, resulting_version=result.version,
            reason_code=result.code.value if result.code is not None else None,
            safe_message=result.message, correlation_id=result.correlation_id,
        ))
        self._session.flush()


class SqlAuditRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def append(self, record: contracts.AuditRecord) -> None:
        if record.actor_kind != "user":
            raise ValueError("The current audit schema supports user actors only.")
        self._session.add(models.AuditEvent(
            id=record.id, actor_user_id=record.actor_id, action=record.action,
            entity_type=record.entity_type, entity_id=record.entity_id,
            assessment_id=record.assessment_id, assignment_id=record.assignment_id,
            observed_at=_write_time(record.observed_at), outcome=record.outcome,
            request_identity=record.request_id, correlation_id=record.correlation_id,
            change_summary=record.summary, support_purpose=record.support_purpose,
            support_reference=record.support_reference,
        ))
        self._session.flush()


class SqlNotificationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _event(row: models.NotificationEvent) -> contracts.NotificationEventRecord:
        if row.assessment_id is None or row.status_context is None or row.date_context is None:
            raise ValueError("Notification context cannot be represented by the service record.")
        return contracts.NotificationEventRecord(
            id=row.id, assignment_id=row.assignment_id, assessment_id=row.assessment_id,
            trigger=row.trigger_name, recipient_user_id=row.recipient_user_id,
            template_version=row.template_version, record_ref=row.record_ref,
            occurrence=_read_time(row.scheduled_occurrence), status=row.status_context,
            due_date=row.date_context, logical_identity=row.idempotency_identity,
            correlation_id=row.correlation_id,
        )

    @staticmethod
    def _attempt(row: models.NotificationAttempt) -> contracts.NotificationAttemptRecord:
        return contracts.NotificationAttemptRecord(
            id=row.id, event_id=row.notification_event_id, ordinal=row.attempt_ordinal,
            adapter_request_id=row.adapter_request_ref,
            attempted_at=_read_time(row.attempted_at), outcome=row.outcome,
            manual_retry_allowed=row.retry_eligible, failure_category=row.failure_category,
        )

    def get_event_by_identity(self, identity: str) -> contracts.NotificationEventRecord | None:
        row = self._session.scalar(select(models.NotificationEvent).where(
            models.NotificationEvent.idempotency_identity == identity,
        ))
        return self._event(row) if row is not None else None

    def get_event(self, event_id: str) -> contracts.NotificationEventRecord | None:
        row = self._session.get(models.NotificationEvent, event_id)
        return self._event(row) if row is not None else None

    def add_event(self, record: contracts.NotificationEventRecord) -> None:
        self._session.add(models.NotificationEvent(
            id=record.id, assignment_id=record.assignment_id, assessment_id=record.assessment_id,
            trigger_name=record.trigger, recipient_user_id=record.recipient_user_id,
            template_version=record.template_version, record_ref=record.record_ref,
            scheduled_occurrence=_write_time(record.occurrence),
            status_context=record.status, date_context=record.due_date,
            idempotency_identity=record.logical_identity,
            event_status="not_delivered_prototype", correlation_id=record.correlation_id,
        ))
        self._session.flush()

    def get_attempt(
        self, event_id: str, request_id: str,
    ) -> contracts.NotificationAttemptRecord | None:
        row = self._session.scalar(select(models.NotificationAttempt).where(
            models.NotificationAttempt.notification_event_id == event_id,
            models.NotificationAttempt.adapter_request_ref == request_id,
        ))
        return self._attempt(row) if row is not None else None

    def list_attempts(self, event_id: str) -> tuple[contracts.NotificationAttemptRecord, ...]:
        rows = self._session.scalars(select(models.NotificationAttempt).where(
            models.NotificationAttempt.notification_event_id == event_id,
        ).order_by(models.NotificationAttempt.attempt_ordinal))
        return tuple(self._attempt(row) for row in rows)

    def add_attempt(self, record: contracts.NotificationAttemptRecord) -> None:
        self._session.add(models.NotificationAttempt(
            id=record.id, notification_event_id=record.event_id,
            attempt_ordinal=record.ordinal, adapter_request_ref=record.adapter_request_id,
            attempted_at=_write_time(record.attempted_at), outcome=record.outcome,
            retry_eligible=record.manual_retry_allowed, failure_category=record.failure_category,
        ))
        self._session.flush()
