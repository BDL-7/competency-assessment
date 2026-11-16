"""Rollback-by-default SQL support transaction, without an aggregate adapter."""

import logging
from types import TracebackType

from sqlalchemy.orm import Session, sessionmaker

from app.data.repositories import (
    SqlAuditRepository, SqlIdempotencyRepository, SqlNotificationRepository, SqlScopedQueries,
)
from app.services.contracts import (
    AuditAppendPort, IdempotencyPort, NotificationPort, ScopedQueryPort,
)

logger = logging.getLogger(__name__)


class SqlSupportUnitOfWork:
    """Own one transaction for the four schema-compatible support ports."""

    idempotency: IdempotencyPort
    audits: AuditAppendPort
    notifications: NotificationPort
    queries: ScopedQueryPort

    def __init__(self, factory: sessionmaker[Session]) -> None:
        self._factory = factory
        self._session: Session | None = None

    def __enter__(self) -> "SqlSupportUnitOfWork":
        if self._session is not None:
            raise RuntimeError("The support transaction is already active.")
        session = self._factory(autobegin=False, close_resets_only=False)
        session.begin()
        self._session = session
        self.idempotency = SqlIdempotencyRepository(session)
        self.audits = SqlAuditRepository(session)
        self.notifications = SqlNotificationRepository(session)
        self.queries = SqlScopedQueries(session)
        return self

    def _active_session(self) -> Session:
        if self._session is None:
            raise RuntimeError("Enter the support transaction before using it.")
        return self._session

    def commit(self) -> None:
        self._active_session().commit()

    def rollback(self) -> None:
        self._active_session().rollback()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        session = self._active_session()
        try:
            if exc_type is not None:
                logger.error("SQL support transaction failed (%s).", exc_type.__name__)
            session.rollback()
        finally:
            session.close()
            self._session = None
