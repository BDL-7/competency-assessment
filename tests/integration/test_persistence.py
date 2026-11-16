"""Persistence boundary integration checks."""

import shutil
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta, timezone
from pathlib import Path
from threading import Barrier

import pytest
from alembic import command
from alembic.config import Config
from flask import Flask
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from app.data import (
    ApplicationUser, Assessment, AssessmentDraft, AssessmentDraftElement,
    AssessmentElement, AssessmentVersion, Assignment, Employee, ProcessGrouping,
    ProcessGroupingTestSystem, Team, TestSystem as DataTestSystem, configure_database,
    SqlSupportUnitOfWork, get_session_factory,
)
from app.data import models
from app.data.demo import initialize_demo
from app.domain import CommandResult, RejectionCode
from app.services import contracts


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
    config = Config("migrations/alembic.ini")
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
    config = Config("migrations/alembic.ini")
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
    config = Config("migrations/alembic.ini")
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


@pytest.fixture
def support_factory(isolated_database_directory, engine_cleanup, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    application = Flask("sql-support", root_path=str(Path(__file__).resolve().parents[2] / "app"))
    application.config.update(
        DATABASE_URL=f"sqlite:///{(isolated_database_directory / 'support.db').as_posix()}",
        APP_ENV="testing", PILOT_DEMO_ENABLED=True,
    )
    resources = configure_database(application)
    engine_cleanup(resources["engine"])
    initialize_demo(application)
    return get_session_factory(application)


def support_effects(request="support-request"):
    when = datetime(2027, 2, 20, 7, tzinfo=timezone(timedelta(hours=-5)))
    audit = contracts.AuditRecord(
        id=f"audit-{request}", actor_id="SYN-ASR-001", action="synthetic_support",
        entity_type="assessment", entity_id="SYN-ASM-001", observed_at=when,
        outcome="Succeeded", request_id=request, correlation_id=f"correlation-{request}",
        summary="Synthetic support effect", assessment_id="SYN-ASM-001",
        assignment_id="SYN-ASGN-001", support_purpose="Synthetic support check",
        support_reference="SYN-SUPPORT",
    )
    event = contracts.NotificationEventRecord(
        id=f"event-{request}", assignment_id="SYN-ASGN-001", assessment_id="SYN-ASM-001",
        trigger="submitted", recipient_user_id="SYN-EMP-001", template_version="prototype-v1",
        record_ref="SYN-ASM-001", occurrence=when,
        status="Awaiting Testing Personnel signature", due_date=date(2027, 2, 15),
        logical_identity=f"identity-{request}", correlation_id=f"correlation-{request}",
    )
    attempt = contracts.NotificationAttemptRecord(
        id=f"attempt-{request}", event_id=event.id, ordinal=1, adapter_request_id=request,
        attempted_at=when, outcome="NotDelivered", manual_retry_allowed=False,
        failure_category="synthetic_non_delivery",
    )
    replay = contracts.IdempotencyRecord(
        operation="synthetic_support", target="SYN-ASM-001", actor_id="SYN-ASR-001",
        request_id=request, fingerprint="ab" * 32,
        result=CommandResult.succeeded(f"correlation-{request}",
                                       reference_id=event.id, state="recorded", version=5),
    )
    return audit, event, attempt, replay


def write_support_effects(work, effects):
    audit, event, attempt, replay = effects
    work.audits.append(audit)
    work.notifications.add_event(event)
    work.notifications.add_attempt(attempt)
    work.idempotency.add(replay)


def effect_counts(factory):
    with factory() as session:
        return tuple(session.scalar(select(func.count()).select_from(table)) for table in (
            models.AuditEvent, models.NotificationEvent,
            models.NotificationAttempt, models.IdempotencyRecord,
        ))


@pytest.mark.parametrize("outcome", ["Succeeded", "Rejected", "Failed"])
def test_sql_support_ports_round_trip_canonical_results_and_effects(support_factory, outcome):
    audit, event, attempt, replay = support_effects()
    if outcome == "Rejected":
        replay = replace(replay, result=CommandResult.rejected(
            "synthetic-correlation", RejectionCode.FOLLOWUP_REQUIRED, "Synthetic follow-up",
            reference_id="SYN-ASMV-002", state="Returned", version=5,
        ))
    elif outcome == "Failed":
        replay = replace(replay, result=CommandResult.failed(
            "synthetic-correlation", RejectionCode.DEPENDENCY_UNAVAILABLE, "Synthetic failure",
        ))
    with SqlSupportUnitOfWork(support_factory) as work:
        write_support_effects(work, (audit, event, attempt, replay))
        work.commit()
        with pytest.raises(InvalidRequestError):
            work.notifications.get_event(event.id)
    with SqlSupportUnitOfWork(support_factory) as work:
        assert work.idempotency.get(
            replay.operation, replay.target, replay.actor_id, replay.request_id,
        ) == replay
        assert work.idempotency.get(
            replay.operation, replay.target, "SYN-OUT-001", replay.request_id,
        ) is None
        assert work.notifications.get_event(event.id) == event
        assert work.notifications.get_event_by_identity(event.logical_identity) == event
        assert work.notifications.get_attempt(event.id, attempt.adapter_request_id) == attempt
        assert work.notifications.list_attempts(event.id) == (attempt,)
    with support_factory() as session:
        stored = session.get(models.AuditEvent, audit.id)
        assert stored.actor_user_id == audit.actor_id
        assert stored.observed_at.replace(tzinfo=UTC) == audit.observed_at
        assert stored.change_summary == audit.summary
        assert stored.support_purpose == audit.support_purpose
        assert stored.support_reference == audit.support_reference
    assert effect_counts(support_factory) == (1, 1, 1, 1)


@pytest.mark.parametrize("exit_mode", ["no_commit", "rollback", "exception"])
def test_sql_support_transaction_rolls_back_all_uncommitted_effects(support_factory, exit_mode):
    expected = pytest.raises(ValueError, match="Synthetic failure") if exit_mode == "exception" else nullcontext()
    with expected:
        with SqlSupportUnitOfWork(support_factory) as work:
            write_support_effects(work, support_effects())
            retained_port = work.notifications
            if exit_mode == "rollback":
                work.rollback()
            elif exit_mode == "exception":
                raise ValueError("Synthetic failure")
    assert effect_counts(support_factory) == (0, 0, 0, 0)
    with pytest.raises(InvalidRequestError):
        retained_port.get_event("event-support-request")


@pytest.mark.parametrize("effect", ["event", "attempt"])
def test_duplicate_effect_rolls_back_other_ports_without_logging_payloads(support_factory, caplog, effect):
    audit, event, attempt, replay = support_effects()
    with SqlSupportUnitOfWork(support_factory) as work:
        write_support_effects(work, (audit, event, attempt, replay))
        work.commit()
    new_audit, _, _, new_replay = support_effects("duplicate-attempt")
    with pytest.raises(IntegrityError):
        with SqlSupportUnitOfWork(support_factory) as work:
            work.audits.append(replace(new_audit, summary="do-not-log-synthetic-sentinel"))
            work.idempotency.add(new_replay)
            if effect == "event":
                work.notifications.add_event(replace(
                    event, id="duplicate-event", logical_identity="different-identity",
                ))
            else:
                work.notifications.add_attempt(replace(
                    attempt, id="duplicate-attempt", adapter_request_id="different-request",
                ))
            work.commit()
    assert effect_counts(support_factory) == (1, 1, 1, 1)
    assert "IntegrityError" in caplog.text
    assert "do-not-log-synthetic-sentinel" not in caplog.text


def test_competing_sql_requests_persist_one_result_and_one_atomic_audit(support_factory):
    barrier = Barrier(2)

    def submit(number):
        audit, _, _, replay = support_effects(f"worker-{number}")
        replay = replace(replay, request_id="same-request")
        try:
            with SqlSupportUnitOfWork(support_factory) as work:
                assert work.idempotency.get(
                    replay.operation, replay.target, replay.actor_id, replay.request_id,
                ) is None
                barrier.wait(timeout=20)
                work.audits.append(audit)
                work.idempotency.add(replay)
                work.commit()
            return "committed"
        except IntegrityError:
            return "duplicate"

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = tuple(executor.map(submit, (1, 2)))
    assert sorted(outcomes) == ["committed", "duplicate"]
    assert effect_counts(support_factory) == (1, 0, 0, 1)
    with support_factory() as session:
        audit = session.scalar(select(models.AuditEvent))
        replay = session.scalar(select(models.IdempotencyRecord))
        assert audit.correlation_id == replay.correlation_id


@pytest.mark.parametrize("unsupported", ["service_actor", "replay_result", "naive_timestamp"])
def test_unrepresentable_support_records_fail_without_partial_writes(support_factory, unsupported):
    audit, event, _, replay = support_effects()
    with pytest.raises(ValueError):
        with SqlSupportUnitOfWork(support_factory) as work:
            work.notifications.add_event(event)
            if unsupported == "service_actor":
                work.audits.append(replace(audit, actor_kind="service_principal"))
            elif unsupported == "replay_result":
                work.idempotency.add(replace(replay, result=replace(replay.result, replayed=True)))
            else:
                work.audits.append(replace(audit, observed_at=datetime(2027, 2, 20)))
            work.commit()
    assert effect_counts(support_factory) == (0, 0, 0, 0)


def test_sql_scope_requires_participant_relationship_and_rejects_bad_version_pointer(support_factory):
    allowed = contracts.AssessmentQueryScope(
        actor_user_id="SYN-ASR-001", employee_id="SYN-ASR-001",
        assessor_assessment_ids=("SYN-ASM-001",),
    )
    with SqlSupportUnitOfWork(support_factory) as work:
        rows = work.queries.list_assessment_access(allowed)
        assert len(rows) == 1
        assert rows[0].assessment.id == "SYN-ASM-001"
        assert rows[0].assignment.configuration_version == "SYN-CFG-001"
        assert rows[0].current_version_number == 2
        assert work.queries.list_assessment_access(replace(
            allowed, actor_user_id="SYN-OUT-001", employee_id="SYN-OUT-001",
        )) == ()
        assert work.queries.list_assessment_access(replace(
            allowed, assessor_assessment_ids=(),
        )) == ()
    with support_factory.begin() as session:
        session.get(Assessment, "SYN-ASM-001").current_version_id = "missing-synthetic-version"
    with pytest.raises(ValueError, match="current-version pointer"):
        with SqlSupportUnitOfWork(support_factory) as work:
            work.queries.list_assessment_access(allowed)


def test_nullable_legacy_notification_context_is_not_fabricated(support_factory):
    _, event, _, _ = support_effects()
    with SqlSupportUnitOfWork(support_factory) as work:
        work.notifications.add_event(event)
        work.commit()
    with support_factory.begin() as session:
        session.get(models.NotificationEvent, event.id).date_context = None
    with pytest.raises(ValueError, match="Notification context"):
        with SqlSupportUnitOfWork(support_factory) as work:
            work.notifications.get_event(event.id)
