"""Alembic environment for the application-owned schema."""

from __future__ import annotations

import os
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, event, pool
from sqlalchemy.engine import make_url

from app.data import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

environment_url = os.getenv("DATABASE_URL")
if environment_url:
    config.set_main_option("sqlalchemy.url", environment_url.replace("%", "%%"))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        dialect_opts={"paramstyle": "named"}, compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section, {})
    database_url = section["sqlalchemy.url"]
    parsed_url = make_url(database_url)
    if parsed_url.get_backend_name() == "sqlite" and parsed_url.database not in {None, ":memory:"}:
        Path(parsed_url.database).parent.mkdir(parents=True, exist_ok=True)

    connectable = engine_from_config(
        section, prefix="sqlalchemy.", poolclass=pool.NullPool, future=True
    )
    if connectable.dialect.name == "sqlite":
        @event.listens_for(connectable, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
            del connection_record
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
