"""Smoke tests for the two foundation-only HTTP routes."""

from __future__ import annotations


def test_health_returns_only_minimal_status(client) -> None:
    """Health output must not expose configuration or dependency details."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_home_is_rendered_as_html(client) -> None:
    """The home endpoint is a server-rendered page, not a JSON API."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert b"<!doctype html" in response.data.lower()
