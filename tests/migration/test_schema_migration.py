"""Migration checks for the synthetic S0-04A schema."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from flask import Flask
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from app.data import configure_database


APPLICATION_TABLES = {
    "application_user", "assessment", "assessment_document", "assessment_draft",
    "assessment_draft_element", "assessment_element", "assessment_version", "assignment", "audit_event",
    "employee", "idempotency_record", "notification_attempt", "notification_event",
    "process_grouping", "process_grouping_test_system", "renewal", "role_assignment",
    "signature", "team", "test_system",
}


def migration_config(database_path: Path) -> Config:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database_path.as_posix()}")
    return config


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


def test_clean_upgrade_is_repeatable_and_does_not_seed_operational_rows(
    isolated_database_directory: Path, engine_cleanup,
) -> None:
    database_path = isolated_database(isolated_database_directory, "clean")
    config = migration_config(database_path)

    command.upgrade(config, "head")
    command.upgrade(config, "head")

    application = Flask(__name__)
    application.config["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"
    resources = configure_database(application)
    engine = resources["engine"]
    engine_cleanup(engine)
    assert APPLICATION_TABLES <= set(inspect(engine).get_table_names())
    with engine.connect() as connection:
        assert connection.scalar(text("PRAGMA foreign_keys")) == 1
        for table_name in APPLICATION_TABLES:
            assert connection.scalar(text(f'SELECT COUNT(*) FROM "{table_name}"')) == 0


def test_foreign_keys_are_enforced_and_parent_deletion_is_restricted(
    isolated_database_directory: Path, engine_cleanup,
) -> None:
    database_path = isolated_database(isolated_database_directory, "foreign-keys")
    command.upgrade(migration_config(database_path), "head")
    application = Flask(__name__)
    application.config["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"
    engine = configure_database(application)["engine"]
    engine_cleanup(engine)

    with engine.begin() as connection:
        connection.execute(text(
            "INSERT INTO team (id, display_label, is_active, configuration_owner_ref, created_at) "
            "VALUES ('SYN-TEAM', 'Synthetic Team', 1, 'SYN-OWNER', CURRENT_TIMESTAMP)"
        ))
        connection.execute(text(
            "INSERT INTO employee "
            "(id, team_id, display_label, is_active, created_at) "
            "VALUES ('SYN-EMP', 'SYN-TEAM', 'Synthetic Employee', 1, CURRENT_TIMESTAMP)"
        ))

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM team WHERE id = 'SYN-TEAM'"))

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text(
                "INSERT INTO employee "
                "(id, team_id, display_label, is_active, created_at) "
                "VALUES ('SYN-BAD', 'MISSING', 'Synthetic Missing', 1, CURRENT_TIMESTAMP)"
            ))


def test_identity_and_logical_effect_uniqueness_constraints_exist(
    isolated_database_directory: Path, engine_cleanup,
) -> None:
    database_path = isolated_database(isolated_database_directory, "constraints")
    command.upgrade(migration_config(database_path), "head")
    application = Flask(__name__)
    application.config["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"
    engine = configure_database(application)["engine"]
    engine_cleanup(engine)
    inspector = inspect(engine)

    required_unique_columns = {
        "signature": {("assessment_version_id", "signature_role")},
        "assessment_document": {("assessment_version_id", "document_kind")},
        "renewal": {("finalized_assessment_version_id",)},
        "notification_event": {
            (
                "record_ref", "trigger_name", "recipient_user_id",
                "template_version", "scheduled_occurrence",
            )
        },
        "notification_attempt": {
            ("notification_event_id", "attempt_ordinal"),
            ("notification_event_id", "adapter_request_ref"),
        },
        "idempotency_record": {
            ("operation_name", "target_ref", "actor_user_id", "request_identity")
        },
        "process_grouping_test_system": {
            ("process_grouping_id", "test_system_id")
        },
        "assessment_draft_element": {
            ("assessment_draft_id", "element_ref")
        },
    }
    for table_name, required in required_unique_columns.items():
        actual = {
            tuple(constraint["column_names"])
            for constraint in inspector.get_unique_constraints(table_name)
        }
        assert required <= actual

    issued_columns = {
        column["name"]: column for column in inspector.get_columns("assessment_version")
    }
    for required_snapshot_field in {
        "assessment_context", "assessment_type", "process", "assessment_method",
        "specimen_context", "testing_context",
        "problem_solving_evidence", "protocol_outcome",
    }:
        assert issued_columns[required_snapshot_field]["nullable"] is False

    retained_tables = APPLICATION_TABLES - {"team"}
    for table_name in retained_tables:
        for foreign_key in inspector.get_foreign_keys(table_name):
            assert foreign_key["options"].get("ondelete") == "RESTRICT"
