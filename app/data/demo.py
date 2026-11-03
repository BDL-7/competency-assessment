"""Explicit creation of the single-record disposable synthetic demo."""

import json
import os
from datetime import UTC, date, datetime
from pathlib import Path

import click
from alembic import command
from alembic.config import Config
from flask import Flask
from sqlalchemy import inspect, select
from sqlalchemy.engine import make_url

from app.data.database import get_session_factory
from app.data.models import (
    ApplicationUser, Assessment, AssessmentDraft, AssessmentDraftElement,
    AssessmentElement, AssessmentVersion, Assignment, Employee, ProcessGrouping,
    ProcessGroupingTestSystem, RoleAssignment, Team, TestSystem,
)

DEMO_VERSION = "S0-07-single-record-v1"
AS_OF = date(2027, 2, 20)
PEOPLE = {
    "SYN-EMP-001": "Testing Person One",
    "SYN-LEAD-001": "Team Lead One",
    "SYN-ASR-001": "Assessor One",
    "SYN-TS-001": "Technical Supervisor One",
    "SYN-ADM-001": "SQUAD Admin One",
    "SYN-PLAT-001": "Platform Admin One",
    "SYN-OUT-001": "Unassigned Observer",
}


def demo_path(application: Flask) -> Path:
    url = make_url(application.config["DATABASE_URL"])
    if url.get_backend_name() != "sqlite" or not url.database or url.database == ":memory:":
        raise ValueError("The local demo requires an explicit file-backed SQLite target.")
    return Path(url.database).resolve()


def register_demo_command(application: Flask) -> None:
    @application.cli.command("init-demo")
    def init_demo() -> None:
        """Create the synthetic demo once; never reset an existing database."""
        try:
            result = initialize_demo(application)
        except (ValueError, RuntimeError) as error:
            raise click.ClickException(str(error)) from error
        click.echo(result)


def initialize_demo(application: Flask) -> str:
    if not application.config["PILOT_DEMO_ENABLED"] or application.config["APP_ENV"] == "production":
        raise ValueError("Enable the local demo in development/testing first.")
    if os.getenv("DATABASE_URL"):
        raise ValueError("Unset DATABASE_URL before setup; use only APP_DATABASE_URL for this demo.")
    path = demo_path(application)
    marker = path.with_suffix(path.suffix + ".synthetic-demo.json")
    expected = {"dataset": DEMO_VERSION, "database": str(path), "as_of": AS_OF.isoformat()}
    if path.exists():
        try:
            owned = json.loads(marker.read_text(encoding="utf-8")) == expected
        except (OSError, ValueError):
            owned = False
        if not owned:
            raise ValueError("Refusing an existing unknown database; choose a new dedicated demo file.")
        factory = get_session_factory(application)
        with factory() as session:
            if session.get(Assessment, "SYN-ASM-001") is None:
                raise ValueError("Owned demo is incomplete; choose a new dedicated demo file.")
        return "Synthetic demo already initialized; no records changed."
    if marker.exists():
        raise ValueError("A stale demo marker exists; choose a new dedicated demo file.")
    path.parent.mkdir(parents=True, exist_ok=True)
    config = Config(str(Path(application.root_path).parent / "alembic.ini"))
    config.set_main_option("script_location", str(Path(application.root_path).parent / "migrations"))
    config.set_main_option("sqlalchemy.url", application.config["DATABASE_URL"].replace("%", "%%"))
    command.upgrade(config, "head")
    factory = get_session_factory(application)
    with factory.begin() as s:
        if "team" not in inspect(s.bind).get_table_names() or s.scalar(select(Team.id).limit(1)):
            raise ValueError("Demo target is not empty.")
        s.add(Team(id="SYN-TEAM-ALPHA", display_label="Synthetic Team Alpha",
                   configuration_owner_ref="SYN-CFG-001"))
        s.flush()
        for key, label in PEOPLE.items():
            s.add(Employee(id=key, team_id="SYN-TEAM-ALPHA", display_label=label))
        s.flush()
        for key in PEOPLE:
            s.add(ApplicationUser(id=key, identity_provider_subject=key,
                                  is_mock_identity=True, employee_id=key))
        s.flush()
        s.add(TestSystem(id="SYN-TEST-SYSTEM-01", display_label="Synthetic test system",
                         owner_ref="SYN-OWNER", approval_ref="SYN-DEMO-ONLY"))
        s.add(ProcessGrouping(id="SYN-PROCESS-01", team_id="SYN-TEAM-ALPHA",
              display_label="Synthetic process grouping", owner_ref="SYN-OWNER",
              applicability="Non-CLIA synthetic prototype", configuration_version="SYN-CFG-001",
              interval_value=12, interval_unit="calendar_months"))
        s.flush()
        s.add(ProcessGroupingTestSystem(id="SYN-MAP-001", process_grouping_id="SYN-PROCESS-01",
                                       test_system_id="SYN-TEST-SYSTEM-01"))
        s.add(Assignment(id="SYN-ASGN-001", employee_id="SYN-EMP-001",
            team_id="SYN-TEAM-ALPHA", process_grouping_id="SYN-PROCESS-01",
            assigned_team_lead_id="SYN-LEAD-001", assessor_id="SYN-ASR-001",
            technical_supervisor_id="SYN-TS-001", interval_value_snapshot=12,
            interval_unit_snapshot="calendar_months", configuration_version_snapshot="SYN-CFG-001",
            basis_date=date(2026, 2, 15), due_date=date(2027, 2, 15),
            scheduling_state="Assigned", created_at=datetime(2026, 2, 15, tzinfo=UTC)))
        s.flush()
        s.add(Assessment(id="SYN-ASM-001", assignment_id="SYN-ASGN-001",
              lifecycle_state="Awaiting Testing Personnel signature",
              current_draft_id="SYN-DRAFT-002", current_version_id="SYN-ASMV-002",
              lock_version=5, created_at=datetime(2027, 2, 16, tzinfo=UTC)))
        s.flush()
        scope_rows = (
            ("SYN-EMP-001", "employee", None, "SYN-ASM-001", None),
            ("SYN-LEAD-001", "team_lead", "SYN-TEAM-ALPHA", None, None),
            ("SYN-ASR-001", "assessor", None, "SYN-ASM-001", None),
            ("SYN-TS-001", "technical_supervisor", None, "SYN-ASM-001", None),
            ("SYN-ADM-001", "squad_admin", None, None, "SYN-CFG-001"),
            ("SYN-PLAT-001", "platform_admin", None, None, "diagnostic"),
            ("SYN-OUT-001", "assessor", None, None, "SYN-UNASSIGNED"),
        )
        for n, (user, role, team, assessment, configuration) in enumerate(scope_rows):
            s.add(RoleAssignment(id=f"SYN-ROLE-{n}", user_id=user, role_name=role,
                team_id=team, assessment_id=assessment, configuration_scope=configuration,
                starts_at=datetime(2026, 1, 1, tzinfo=UTC), approved_by_user_id="SYN-ADM-001"))
        for n in (1, 2):
            when = datetime(2027, 2, 16 + n, 12, tzinfo=UTC)
            content = dict(
                employee_id="SYN-EMP-001", assessor_id="SYN-ASR-001",
                technical_supervisor_id="SYN-TS-001", configuration_version_snapshot="SYN-CFG-001",
                assessment_context="Synthetic Non-CLIA demonstration",
                assessment_type="Initial", process="SYN-PROCESS-01",
                assessment_method="Synthetic observation", specimen_context="Synthetic specimen",
                testing_context="Synthetic instrument context",
                problem_solving_evidence="Synthetic problem-solving evidence",
                protocol_outcome="Recorded by assessor; no calculated competency",
                followup_required=True,
                followup_description="Synthetic follow-up documented" if n == 2 else None,
                created_by_user_id="SYN-ASR-001", created_at=when,
            )
            draft_id = f"SYN-DRAFT-{n:03}"
            version_id = f"SYN-ASMV-{n:03}"
            s.add(AssessmentDraft(id=draft_id, assessment_id="SYN-ASM-001",
                  updated_by_user_id="SYN-ASR-001", **content))
            s.flush()
            s.add(AssessmentDraftElement(id=f"SYN-DE-{n}", assessment_draft_id=draft_id,
                element_ref="SYN-ELEMENT-03", recorded_result="unsuccessful",
                evidence="Synthetic evidence only", has_gap=True,
                followup_description=content["followup_description"]))
            s.add(AssessmentVersion(id=version_id, assessment_id="SYN-ASM-001",
                version_number=n, source_draft_id=draft_id, assigned_team_lead_id="SYN-LEAD-001",
                is_locked=False, **content))
            s.flush()
            s.add(AssessmentElement(id=f"SYN-EL-{n}", assessment_version_id=version_id,
                element_ref="SYN-ELEMENT-03", recorded_result="unsuccessful",
                evidence="Synthetic evidence only", has_gap=True,
                followup_description=content["followup_description"]))
    marker.write_text(json.dumps(expected, indent=2), encoding="utf-8")
    return f"Synthetic demo initialized at {path}. Reference date: {AS_OF}."
