"""Boundary tests for the synthetic development identity provider."""

from __future__ import annotations

import pytest
from flask import g

from app import create_app
from app.config import ConfigurationError


def test_mock_identity_is_disabled_by_default() -> None:
    """Testing mode does not imply that mock authentication is enabled."""

    app = create_app(
        "testing", test_config={"SECRET_KEY": "synthetic-disabled-secret"}
    )

    assert app.extensions["identity_provider"] is None
    with app.test_request_context("/"):
        app.preprocess_request()
        assert g.current_identity is None


@pytest.mark.parametrize("profile", ["development", "testing"])
def test_mock_identity_uses_only_server_configuration(profile: str) -> None:
    """An enabled mock resolves the fixed synthetic identity from app config."""

    app = create_app(
        profile,
        test_config={
            "SECRET_KEY": "synthetic-enabled-secret",
            "MOCK_AUTH_ENABLED": True,
            "MOCK_USER_ID": "synthetic-user-001",
            "MOCK_DISPLAY_NAME": "Synthetic User",
        },
    )

    # Client-controlled headers and query values must not become identity input.
    with app.test_request_context(
        "/?user_id=attacker&role=admin",
        headers={"X-User-Id": "attacker", "X-Role": "admin"},
    ):
        app.preprocess_request()
        assert g.current_identity.user_id == "synthetic-user-001"
        assert g.current_identity.display_name == "Synthetic User"
        assert not hasattr(g.current_identity, "roles")


def test_production_rejects_mock_identity() -> None:
    """Production must fail startup rather than enable synthetic identity."""

    with pytest.raises(ConfigurationError):
        create_app(
            "production",
            test_config={
                "SECRET_KEY": "synthetic-production-secret",
                "MOCK_AUTH_ENABLED": True,
                "MOCK_USER_ID": "synthetic-user-001",
                "MOCK_DISPLAY_NAME": "Synthetic User",
            },
        )


@pytest.mark.parametrize(
    ("user_id", "display_name"),
    [
        (None, "Synthetic User"),
        ("synthetic-user-001", None),
        ("", "Synthetic User"),
        ("synthetic-user-001", ""),
    ],
)
def test_enabled_mock_requires_complete_server_identity(
    user_id: str | None, display_name: str | None
) -> None:
    """Incomplete mock configuration is rejected instead of guessed."""

    with pytest.raises(ConfigurationError):
        create_app(
            "testing",
            test_config={
                "SECRET_KEY": "synthetic-incomplete-secret",
                "MOCK_AUTH_ENABLED": True,
                "MOCK_USER_ID": user_id,
                "MOCK_DISPLAY_NAME": display_name,
            },
        )
