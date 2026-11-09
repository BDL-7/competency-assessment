"""Shared pytest fixtures for the application-foundation tests."""

from __future__ import annotations

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create an isolated testing application with mock identity disabled."""

    return create_app(
        "testing",
        test_config={
            "SECRET_KEY": "synthetic-test-secret",
            "MOCK_AUTH_ENABLED": False,
        },
    )


@pytest.fixture
def client(app):
    """Return Flask's in-process HTTP client for the isolated app."""

    return app.test_client()
