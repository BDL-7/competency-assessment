"""Read-only pilot contracts and shared effective-role scope resolution."""

from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Protocol

from app.domain import Role
from app.services.contracts import AssessmentQueryScope, RoleScopeRecord


def effective_scope(
    user_id: str, employee_id: str | None,
    roles: tuple[RoleScopeRecord, ...], now: datetime,
) -> AssessmentQueryScope:
    def utc(value: datetime) -> datetime:
        return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)

    active = tuple(r for r in roles if utc(r.starts_at) <= utc(now)
                   and (r.ends_at is None or utc(r.ends_at) > utc(now)))
    return AssessmentQueryScope(
        actor_user_id=user_id, employee_id=employee_id,
        own_employee_id=employee_id if any(r.role == Role.EMPLOYEE.value for r in active) else None,
        own_assessment_ids=tuple(r.assessment_id for r in active if r.role == Role.EMPLOYEE.value and r.assessment_id),
        team_ids=tuple(r.team_id for r in active if r.role == Role.TEAM_LEAD.value and r.team_id),
        assessor_assessment_ids=tuple(r.assessment_id for r in active if r.role == Role.ASSESSOR.value and r.assessment_id),
        technical_supervisor_assessment_ids=tuple(r.assessment_id for r in active if r.role == Role.TECHNICAL_SUPERVISOR.value and r.assessment_id),
        configuration_versions=tuple(r.configuration_scope for r in active if r.role == Role.SQUAD_ADMIN.value and r.configuration_scope),
        diagnostic=any(r.role == Role.PLATFORM_ADMIN.value and r.configuration_scope == "diagnostic" for r in active),
    )


class PilotAccessError(Exception):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status


class PilotUnavailableError(Exception):
    """A read dependency failed; diagnostics are logged by the adapter."""


@dataclass(frozen=True)
class PilotRow:
    id: str
    employee: str
    team: str
    grouping: str
    state: str
    due_date: date
    overdue: bool


@dataclass(frozen=True)
class PilotVersion:
    number: int
    context: str
    method: str
    outcome: str
    evidence: str
    followup: str
    locked: bool
    signatures: tuple[str, ...]


@dataclass(frozen=True)
class PilotDetail:
    row: PilotRow
    participants: tuple[tuple[str, str], ...]
    versions: tuple[PilotVersion, ...]
    diagnostic: bool = False


class PilotReader(Protocol):
    def list_rows(self, user_id: str, *, purpose: str = "", reference: str = "") -> tuple[PilotRow, ...]: ...
    def detail(self, user_id: str, record_id: str, *, purpose: str = "", reference: str = "") -> PilotDetail: ...
