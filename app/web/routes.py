"""Minimal routes for application startup verification."""

from flask import Blueprint, render_template

web_blueprint = Blueprint("web", __name__)


@web_blueprint.get("/")
def home() -> str:
    """Render the application foundation landing page."""

    return render_template("home.html")


@web_blueprint.get("/health")
def health() -> dict[str, str]:
    """Return only the minimum information needed for a health probe."""

    return {"status": "healthy"}
