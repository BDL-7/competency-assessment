"""Synthetic identity support for local development and tests only."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SyntheticIdentity:
    """A non-authoritative identity containing no application roles."""

    user_id: str
    display_name: str


class MockIdentityProvider:
    """Resolve one immutable identity supplied by trusted server configuration."""

    def __init__(self, user_id: str, display_name: str) -> None:
        self._identity = SyntheticIdentity(
            user_id=user_id,
            display_name=display_name,
        )

    def resolve(self) -> SyntheticIdentity:
        """Return the configured synthetic identity without granting authority."""

        return self._identity
