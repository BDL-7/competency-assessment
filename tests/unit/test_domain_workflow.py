"""Unit tests for framework-neutral synthetic workflow decisions."""

from datetime import date
from dataclasses import FrozenInstanceError

import pytest

from app.domain import add_calendar_months, is_overdue, validate_assessment_content
from app.services import DraftContent,VersionRecord


def test_add_calendar_months_preserves_approved_scenario_dates() -> None:
    assert add_calendar_months(date(2026, 2, 15), 12) == date(2027, 2, 15)
    assert add_calendar_months(date(2027, 2, 20), 12) == date(2028, 2, 20)


def test_add_calendar_months_clamps_end_of_month() -> None:
    assert add_calendar_months(date(2027, 1, 31), 1) == date(2027, 2, 28)


def test_add_calendar_months_rejects_nonpositive_interval() -> None:
    with pytest.raises(ValueError):
        add_calendar_months(date(2026, 2, 15), 0)


def test_validation_reports_only_missing_scenario_fields() -> None:
    content = {
        "assessment_context": "Synthetic context",
        "assessment_type": "Initial",
        "process": "SYN-PROCESS-01",
        "assessment_method": "Synthetic observation",
        "specimen_context": "Synthetic specimen",
        "testing_context": "Synthetic instrument context",
        "problem_solving_evidence": "Synthetic evidence",
        "protocol_outcome": "Recorded by assessor",
    }

    assert validate_assessment_content(content) == ()
    del content["assessment_method"]
    assert validate_assessment_content(content) == ("assessment_method",)


def test_overdue_is_derived_only_after_due_date_while_active() -> None:
    due = date(2027, 2, 15)
    assert not is_overdue(due_date=due, as_of=date(2027, 2, 14), active=True)
    assert not is_overdue(due_date=due, as_of=due, active=True)
    assert is_overdue(due_date=due, as_of=date(2027, 2, 16), active=True)
    assert not is_overdue(due_date=due, as_of=date(2027, 2, 16), active=False)


def test_issued_version_snapshot_is_structurally_immutable() -> None:
    content=DraftContent("Context","Initial","Process","Method","Specimen","Testing","Evidence","Recorded")
    version=VersionRecord("V","A",1,"D","E","L","R","T","C",content,None,"U")
    with pytest.raises(FrozenInstanceError):
        version.content=content
