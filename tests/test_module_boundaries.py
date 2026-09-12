"""Import checks for the approved S0-02 package boundaries."""

from __future__ import annotations

import importlib

import pytest


APPROVED_MODULES = (
    "app.web",
    "app.auth",
    "app.domain",
    "app.services",
    "app.data",
    "app.documents",
    "app.notifications",
    "app.reporting",
    "app.audit",
    "app.ai",
)


@pytest.mark.parametrize("module_name", APPROVED_MODULES)
def test_approved_module_imports(module_name: str) -> None:
    """Every approved boundary exists without requiring external services."""

    assert importlib.import_module(module_name) is not None
