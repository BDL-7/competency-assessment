"""Safe records returned by role-scoped workflow queries."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class AssessmentSummary:
    assessment_id: str
    assignment_id: str
    state: str
    due_date: date
    overdue: bool
    current_version: int | None
