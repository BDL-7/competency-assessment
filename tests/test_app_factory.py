"""Tests for explicit, secure application configuration."""

from __future__ import annotations

import pytest
from flask import Flask

from app import create_app
from app.config import ConfigurationError


@pytest.mark.parametrize("profile", ["development", "testing", "production"])
def test_factory_supports_each_explicit_profile(profile: str) -> None:
    """Every approved profile creates a Flask app when safely configured."""

    app = create_app(
        profile,
        test_config={
            "SECRET_KEY": "synthetic-explicit-secret",
            "MOCK_AUTH_ENABLED": False,
        },
    )

    assert isinstance(app, Flask)
    assert app.config["APP_ENV"] == profile


def test_factory_rejects_unknown_profile() -> None:
    """A misspelled profile must not silently select another environment."""

    with pytest.raises(ConfigurationError):
        create_app("prototype")


def test_production_requires_explicit_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    """Production startup fails closed when no secret is configured."""

    monkeypatch.delenv("APP_SECRET_KEY", raising=False)

    with pytest.raises(ConfigurationError):
        create_app("production")


def test_overrides_cannot_relabel_an_explicit_production_profile() -> None:
    """A configuration override must not downgrade production safety checks."""

    with pytest.raises(ConfigurationError):
        create_app(
            "production",
            test_config={
                "APP_ENV": "testing",
                "SECRET_KEY": "synthetic-production-secret",
                "MOCK_AUTH_ENABLED": True,
                "MOCK_USER_ID": "synthetic-user-001",
                "MOCK_DISPLAY_NAME": "Synthetic User",
            },
        )


@pytest.mark.parametrize("unsafe_flag", ["DEBUG", "TESTING"])
def test_overrides_cannot_enable_unsafe_production_flags(unsafe_flag: str) -> None:
    """Explicit overrides must not weaken the production profile."""

    with pytest.raises(ConfigurationError):
        create_app(
            "production",
            test_config={
                "SECRET_KEY": "synthetic-production-secret",
                "MOCK_AUTH_ENABLED": False,
                unsafe_flag: True,
            },
        )


def test_environment_can_select_an_approved_profile(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """APP_ENV selects an approved profile when no argument is supplied."""

    monkeypatch.setenv("APP_ENV", "testing")

    app = create_app(
        test_config={
            "SECRET_KEY": "synthetic-environment-secret",
            "MOCK_AUTH_ENABLED": False,
        }
    )

    assert app.config["APP_ENV"] == "testing"
