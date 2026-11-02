"""Approved synthetic workflow primitives with no Flask or SQL dependencies."""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Mapping


class AssignmentState(StrEnum):
    SCHEDULED = "Scheduled"
    ASSIGNED = "Assigned"


class AssessmentState(StrEnum):
    IN_PROGRESS = "In progress"
    SUBMITTED = "Submitted"
    RETURNED = "Returned"
    AWAITING_TESTING_PERSONNEL = "Awaiting Testing Personnel signature"
    AWAITING_TECHNICAL_SUPERVISOR = "Awaiting Technical Supervisor signature"
    FINALIZED = "Finalized"


class Role(StrEnum):
    EMPLOYEE = "employee"
    TEAM_LEAD = "team_lead"
    ASSESSOR = "assessor"
    TECHNICAL_SUPERVISOR = "technical_supervisor"
    SQUAD_ADMIN = "squad_admin"
    PLATFORM_ADMIN = "platform_admin"


class SignatureRole(StrEnum):
    TESTING_PERSONNEL = "testing_personnel"
    TECHNICAL_SUPERVISOR = "technical_supervisor"


class NotificationTrigger(StrEnum):
    UPCOMING_DUE = "upcoming_due"
    DUE = "due"
    OVERDUE = "overdue"
    SUBMITTED = "submitted"
    TESTING_PERSONNEL_SIGNATURE_REQUIRED = "testing_personnel_signature_required"
    TECHNICAL_SUPERVISOR_SIGNATURE_REQUIRED = "technical_supervisor_signature_required"
    COMPLETED = "completed"


class RejectionCode(StrEnum):
    INVALID_INPUT = "INVALID_INPUT"
    UNAUTHENTICATED = "UNAUTHENTICATED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND_OR_NOT_VISIBLE = "NOT_FOUND_OR_NOT_VISIBLE"
    STALE_VERSION = "STALE_VERSION"
    INVALID_STATE = "INVALID_STATE"
    COMPLETENESS_FAILED = "COMPLETENESS_FAILED"
    FOLLOWUP_REQUIRED = "FOLLOWUP_REQUIRED"
    SIGNATURE_SEQUENCE_INVALID = "SIGNATURE_SEQUENCE_INVALID"
    SIGNATURE_VERSION_MISMATCH = "SIGNATURE_VERSION_MISMATCH"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    POLICY_PENDING = "POLICY_PENDING"
    DEPENDENCY_UNAVAILABLE = "DEPENDENCY_UNAVAILABLE"


@dataclass(frozen=True)
class CommandResult:
    """Safe application-service result returned to routes and tests."""

    outcome: str
    correlation_id: str
    reference_id: str | None = None
    state: str | None = None
    version: int | None = None
    replayed: bool = False
    code: RejectionCode | None = None
    message: str | None = None

    @classmethod
    def succeeded(
        cls,
        correlation_id: str,
        *,
        reference_id: str,
        state: str | None = None,
        version: int | None = None,
        replayed: bool = False,
    ) -> CommandResult:
        return cls(
            outcome="Succeeded",
            correlation_id=correlation_id,
            reference_id=reference_id,
            state=state,
            version=version,
            replayed=replayed,
        )

    @classmethod
    def rejected(
        cls,
        correlation_id: str,
        code: RejectionCode,
        message: str,
        *,
        reference_id: str | None = None,
        state: str | None = None,
        version: int | None = None,
    ) -> CommandResult:
        return cls(
            outcome="Rejected",
            correlation_id=correlation_id,
            reference_id=reference_id,
            state=state,
            version=version,
            code=code,
            message=message,
        )

    @classmethod
    def failed(
        cls,
        correlation_id: str,
        code: RejectionCode,
        message: str,
    ) -> CommandResult:
        return cls(
            outcome="Failed", correlation_id=correlation_id, code=code, message=message
        )


REQUIRED_ASSESSMENT_FIELDS = (
    "assessment_context",
    "assessment_type",
    "process",
    "assessment_method",
    "specimen_context",
    "testing_context",
    "problem_solving_evidence",
    "protocol_outcome",
)


def validate_assessment_content(content: Mapping[str, object]) -> tuple[str, ...]:
    """Return missing synthetic scenario fields without interpreting outcomes."""

    return tuple(
        field_name
        for field_name in REQUIRED_ASSESSMENT_FIELDS
        if not isinstance(content.get(field_name), str)
        or not str(content[field_name]).strip()
    )


def is_overdue(*, due_date: date, as_of: date, active: bool) -> bool:
    """Return the derived overdue condition without changing lifecycle state."""

    return active and as_of > due_date


def add_calendar_months(value: date, months: int) -> date:
    """Apply the approved synthetic calendar-month arithmetic deterministically."""

    if months <= 0:
        raise ValueError("The synthetic interval must be greater than zero.")
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)
