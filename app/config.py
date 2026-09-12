"""Explicit, environment-backed configuration profiles."""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

from flask import Flask


class ConfigurationError(RuntimeError):
    """Raised when application configuration is missing or unsafe."""


class BaseConfig:
    """Settings shared by every profile.

    Sensitive values intentionally have no source-code fallback.
    """

    DEBUG = False
    TESTING = False
    SECRET_KEY = None
    MOCK_AUTH_ENABLED = False
    MOCK_USER_ID = None
    MOCK_DISPLAY_NAME = None


class DevelopmentConfig(BaseConfig):
    """Local development settings."""

    APP_ENV = "development"
    DEBUG = True


class TestingConfig(BaseConfig):
    """Automated test settings."""

    APP_ENV = "testing"
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production-safe settings."""

    APP_ENV = "production"


CONFIG_PROFILES: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def configure_application(
    application: Flask,
    config_name: str | None = None,
    overrides: Mapping[str, Any] | None = None,
) -> None:
    """Load one named profile, environment values, and explicit overrides."""

    selected_name = (config_name or os.getenv("APP_ENV", "production")).strip().lower()
    try:
        profile = CONFIG_PROFILES[selected_name]
    except KeyError as error:
        allowed_profiles = ", ".join(sorted(CONFIG_PROFILES))
        raise ConfigurationError(
            f"Unknown APP_ENV {selected_name!r}; expected one of: {allowed_profiles}."
        ) from error

    application.config.from_object(profile)
    application.config.update(
        SECRET_KEY=os.getenv("APP_SECRET_KEY"),
        MOCK_AUTH_ENABLED=_read_boolean_environment("APP_MOCK_AUTH_ENABLED", False),
        MOCK_USER_ID=os.getenv("APP_MOCK_USER_ID"),
        MOCK_DISPLAY_NAME=os.getenv("APP_MOCK_DISPLAY_NAME"),
    )
    if overrides:
        application.config.update(overrides)

    # The selected profile is authoritative. An override may supply test
    # values, but it cannot relabel production as a less restrictive profile.
    application.config["APP_ENV"] = selected_name

    _validate_configuration(application)


def _read_boolean_environment(variable_name: str, default: bool) -> bool:
    """Parse a boolean environment value without treating arbitrary text as true."""

    raw_value = os.getenv(variable_name)
    if raw_value is None:
        return default

    normalized_value = raw_value.strip().lower()
    if normalized_value in {"1", "true", "yes", "on"}:
        return True
    if normalized_value in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(
        f"{variable_name} must be one of true, false, 1, 0, yes, no, on, or off."
    )


def _validate_configuration(application: Flask) -> None:
    """Reject unsafe combinations before the application accepts requests."""

    environment_name = application.config["APP_ENV"]
    mock_auth_enabled = application.config["MOCK_AUTH_ENABLED"]

    if not isinstance(mock_auth_enabled, bool):
        raise ConfigurationError("MOCK_AUTH_ENABLED must be a boolean value.")

    if environment_name == "production":
        unsafe_flags = [
            flag_name
            for flag_name in ("DEBUG", "TESTING")
            if application.config.get(flag_name) is not False
        ]
        if unsafe_flags:
            joined_flags = ", ".join(unsafe_flags)
            raise ConfigurationError(
                f"Production requires these flags to remain false: {joined_flags}."
            )
        if _is_missing(application.config.get("SECRET_KEY")):
            raise ConfigurationError("APP_SECRET_KEY is required in production.")
        if mock_auth_enabled:
            raise ConfigurationError("Mock authentication cannot be enabled in production.")

    if mock_auth_enabled:
        if environment_name not in {"development", "testing"}:
            raise ConfigurationError(
                "Mock authentication is allowed only in development or testing."
            )
        if _is_missing_text(application.config.get("MOCK_USER_ID")):
            raise ConfigurationError(
                "APP_MOCK_USER_ID is required when mock authentication is enabled."
            )
        if _is_missing_text(application.config.get("MOCK_DISPLAY_NAME")):
            raise ConfigurationError(
                "APP_MOCK_DISPLAY_NAME is required when mock authentication is enabled."
            )


def _is_missing(value: object) -> bool:
    """Treat absent and whitespace-only configuration values as missing."""

    return value is None or (isinstance(value, str) and not value.strip())


def _is_missing_text(value: object) -> bool:
    """Require mock identity values to be non-empty text."""

    return not isinstance(value, str) or not value.strip()
