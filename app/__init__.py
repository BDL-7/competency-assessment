"""Flask application factory for the competency assessment tracker."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from flask import Flask

from app.auth import initialize_identity
from app.config import configure_application
from app.web import web_blueprint


def create_app(
    config_name: str | None = None,
    test_config: Mapping[str, Any] | None = None,
) -> Flask:
    """Create and configure one Flask application instance.

    ``config_name`` must identify the development, testing, or production
    profile. When it is omitted, ``APP_ENV`` selects the profile. The optional
    ``test_config`` mapping supports explicit test-only overrides without
    changing process environment variables.
    """

    application = Flask(__name__, instance_relative_config=True)
    configure_application(application, config_name, test_config)

    initialize_identity(application)
    application.register_blueprint(web_blueprint)

    return application
