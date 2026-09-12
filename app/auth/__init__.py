"""Authentication boundary for server-resolved application identities."""

from __future__ import annotations

from flask import Flask, g

from app.auth.identity import MockIdentityProvider


def initialize_identity(application: Flask) -> None:
    """Configure the current identity boundary for this application instance."""

    identity_provider = None
    if application.config["MOCK_AUTH_ENABLED"]:
        identity_provider = MockIdentityProvider(
            user_id=application.config["MOCK_USER_ID"],
            display_name=application.config["MOCK_DISPLAY_NAME"],
        )

    application.extensions["identity_provider"] = identity_provider

    @application.before_request
    def resolve_current_identity() -> None:
        # The provider uses only server configuration. Request parameters,
        # cookies, and headers cannot select an identity or a role.
        g.current_identity = (
            identity_provider.resolve() if identity_provider is not None else None
        )


__all__ = ["MockIdentityProvider", "initialize_identity"]
