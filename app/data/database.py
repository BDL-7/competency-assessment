"""SQLAlchemy engine and session-factory configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Flask
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

DatabaseExtension = dict[str, Engine | sessionmaker[Session]]


def configure_database(application: Flask) -> DatabaseExtension:
    """Configure an engine and session factory without creating schema."""

    configured_url = application.config.get("DATABASE_URL")
    if configured_url:
        database_url = str(configured_url)
    else:
        Path(application.instance_path).mkdir(parents=True, exist_ok=True)
        database_url = f"sqlite:///{Path(application.instance_path) / 'competency-assessment.db'}"

    url = make_url(database_url)
    engine_options: dict[str, Any] = {"future": True, "pool_pre_ping": True}
    if url.get_backend_name() == "sqlite":
        engine_options["connect_args"] = {"check_same_thread": False}

    engine = create_engine(database_url, **engine_options)
    if url.get_backend_name() == "sqlite":
        _enable_sqlite_foreign_keys(engine)

    factory = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    resources: DatabaseExtension = {"engine": engine, "session_factory": factory}
    application.extensions["database"] = resources
    return resources


def get_session_factory(application: Flask) -> sessionmaker[Session]:
    """Return the configured session factory or fail closed."""

    resources = application.extensions.get("database")
    if not isinstance(resources, dict) or "session_factory" not in resources:
        raise RuntimeError("Database has not been configured for this application.")
    factory = resources["session_factory"]
    if not isinstance(factory, sessionmaker):
        raise RuntimeError("Database session factory configuration is invalid.")
    return factory


def _enable_sqlite_foreign_keys(engine: Engine) -> None:
    """Enable SQLite foreign-key enforcement for local and test databases."""

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection: Any, connection_record: Any) -> None:
        del connection_record
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
