"""Persistence boundary integration checks."""

import shutil
from datetime import date
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from flask import Flask
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.data import (
    ApplicationUser, Assessment, AssessmentDraft, AssessmentDraftElement,
    AssessmentElement, AssessmentVersion, Assignment, Employee, ProcessGrouping,
    ProcessGroupingTestSystem, Team, TestSystem as DataTestSystem, configure_database,
    get_session_factory,
)


@pytest.fixture
def isolated_database_directory(tmp_path: Path):
    try:
        yield tmp_path
    finally:
        shutil.rmtree(tmp_path)


@pytest.fixture
def engine_cleanup(isolated_database_directory: Path):
    engines = []
    yield engines.append
    for engine in reversed(engines):
        engine.dispose()


def isolated_database(directory: Path, name: str) -> Path:
    return directory / f"{name}.db"


def test_configured_session_factory_persists_synthetic_records(
    isolated_database_directory: Path, engine_cleanup,
) -> None:
    database_path = isolated_database(isolated_database_directory, "persistence")
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")
    command.upgrade(config, "head")

    application = Flask(__name__)
    application.config["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"
    resources = configure_database(application)
    assert resources["engine"] is not None
    engine_cleanup(resources["engine"])
    factory = get_session_factory(application)

    with factory.begin() as session:
        session.add(Team(
            id="SYN-TEAM", display_label="Synthetic Team", is_active=True,
            configuration_owner_ref="SYN-OWNER",
        ))
        session.flush()
        session.add(Employee(
            id="SYN-EMP", team_id="SYN-TEAM", display_label="Synthetic Employee",
            is_active=True,
        ))
        session.flush()
        session.add(ApplicationUser(
            id="SYN-USER", identity_provider_subject="SYN-SUBJECT",
            is_mock_identity=True, is_active=True, employee_id="SYN-EMP",
        ))

    with factory() as session:
        assert session.get(Team, "SYN-TEAM").display_label == "Synthetic Team"
        assert session.get(ApplicationUser, "SYN-USER").employee_id == "SYN-EMP"


def test_duplicate_synthetic_identity_is_rejected(
    isolated_database_directory: Path, engine_cleanup,
) -> None:
    database_path = isolated_database(isolated_database_directory, "identity")
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")
    command.upgrade(config, "head")
    application = Flask(__name__)
    application.config["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"
    resources = configure_database(application)
    engine_cleanup(resources["engine"])
    factory = get_session_factory(application)

    with factory.begin() as session:
        session.add(ApplicationUser(
            id="SYN-USER-1", identity_provider_subject="SYN-SUBJECT",
            is_mock_identity=True, is_active=True,
        ))

    with pytest.raises(IntegrityError):
        with factory.begin() as session:
            session.add(ApplicationUser(
                id="SYN-USER-2", identity_provider_subject="SYN-SUBJECT",
                is_mock_identity=True, is_active=True,
            ))


def test_draft_element_shape_persists_for_immutable_copy_forward(
    isolated_database_directory: Path, engine_cleanup,
) -> None:
    database_path = isolated_database(isolated_database_directory, "draft-element")
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")
    command.upgrade(config, "head")
    application = Flask(__name__)
    application.config["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"
    resources = configure_database(application)
    engine_cleanup(resources["engine"])
    factory = get_session_factory(application)

    with factory.begin() as session:
        session.add(Team(
            id="SYN-TEAM", display_label="Synthetic Team", is_active=True,
            configuration_owner_ref="SYN-OWNER",
        ))
        session.add(DataTestSystem(
            id="SYN-TEST", display_label="Synthetic Test", owner_ref="SYN-OWNER",
            approval_ref="SYN-APPROVAL", is_active=True, is_non_clia_applicable=True,
        ))
        session.flush()
        for employee_id in ("SYN-EMP", "SYN-LEAD", "SYN-ASR", "SYN-TS"):
            session.add(Employee(
                id=employee_id, team_id="SYN-TEAM", display_label=employee_id,
                is_active=True,
            ))
        session.flush()
        session.add(ApplicationUser(
            id="SYN-USER", identity_provider_subject="SYN-SUBJECT",
            is_mock_identity=True, is_active=True, employee_id="SYN-ASR",
        ))
        session.add(ProcessGrouping(
            id="SYN-PROCESS", team_id="SYN-TEAM", display_label="Synthetic Process",
            owner_ref="SYN-OWNER", applicability="synthetic-non-clia",
            configuration_version="SYN-CONFIG-1", interval_value=12,
            interval_unit="calendar_months", is_active=True,
        ))
        session.flush()
        session.add(ProcessGroupingTestSystem(
            id="SYN-PROCESS-TEST", process_grouping_id="SYN-PROCESS",
            test_system_id="SYN-TEST",
        ))
        session.add(Assignment(
            id="SYN-ASGN", employee_id="SYN-EMP", team_id="SYN-TEAM",
            process_grouping_id="SYN-PROCESS", assigned_team_lead_id="SYN-LEAD",
            assessor_id="SYN-ASR", technical_supervisor_id="SYN-TS",
            interval_value_snapshot=12, interval_unit_snapshot="calendar_months",
            configuration_version_snapshot="SYN-CONFIG-1",
            basis_date=date(2026, 2, 15), due_date=date(2027, 2, 15),
            scheduling_state="Assigned", lock_version=1,
        ))
        session.flush()
        session.add(Assessment(
            id="SYN-ASM", assignment_id="SYN-ASGN", lifecycle_state="In progress",
            current_draft_id="SYN-DRAFT", lock_version=1,
        ))
        session.flush()
        session.add(AssessmentDraft(
            id="SYN-DRAFT", assessment_id="SYN-ASM", lock_version=1,
            employee_id="SYN-EMP", assessor_id="SYN-ASR",
            technical_supervisor_id="SYN-TS",
            configuration_version_snapshot="SYN-CONFIG-1",
            created_by_user_id="SYN-USER", updated_by_user_id="SYN-USER",
        ))
        session.flush()
        draft_element = AssessmentDraftElement(
            id="SYN-DRAFT-ELEMENT", assessment_draft_id="SYN-DRAFT",
            element_ref="SYN-ELEMENT-03", recorded_result="unsuccessful",
            evidence="Synthetic evidence", has_gap=True,
            followup_status="documented", followup_description="Synthetic follow-up",
        )
        session.add(draft_element)
        session.flush()
        session.add(AssessmentVersion(
            id="SYN-VERSION", assessment_id="SYN-ASM", version_number=1,
            source_draft_id="SYN-DRAFT", employee_id="SYN-EMP",
            assigned_team_lead_id="SYN-LEAD", assessor_id="SYN-ASR",
            technical_supervisor_id="SYN-TS",
            configuration_version_snapshot="SYN-CONFIG-1",
            assessment_context="Synthetic context", assessment_type="Synthetic type",
            process="Synthetic process",
            assessment_method="Synthetic method", specimen_context="Synthetic specimen",
            testing_context="Synthetic testing context",
            problem_solving_evidence="Synthetic problem solving",
            protocol_outcome="Assessor-recorded synthetic outcome",
            followup_required=True, followup_description=draft_element.followup_description,
            created_by_user_id="SYN-USER", is_locked=False,
        ))
        session.flush()
        session.add(AssessmentElement(
            id="SYN-ELEMENT", assessment_version_id="SYN-VERSION",
            element_ref=draft_element.element_ref,
            recorded_result=draft_element.recorded_result,
            evidence=draft_element.evidence, comments=draft_element.comments,
            has_gap=draft_element.has_gap, followup_status=draft_element.followup_status,
            followup_description=draft_element.followup_description,
        ))

    with factory() as session:
        mutable = session.get(AssessmentDraftElement, "SYN-DRAFT-ELEMENT")
        immutable = session.get(AssessmentElement, "SYN-ELEMENT")
        assert mutable.assessment_draft_id == "SYN-DRAFT"
        assert immutable.element_ref == mutable.element_ref
        assert immutable.followup_description == mutable.followup_description

    with pytest.raises(IntegrityError):
        with factory.begin() as session:
            session.execute(
                delete(AssessmentDraft).where(AssessmentDraft.id == "SYN-DRAFT")
            )
