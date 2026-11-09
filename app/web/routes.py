"""Server-rendered read-only local pilot and foundation health route."""

import hmac
import secrets
from functools import wraps
from math import ceil

from flask import Blueprint, abort, current_app, g, render_template, request, session

from app.ai.mock import BOTS, answer
from app.services.pilot import PilotAccessError, PilotReader, PilotUnavailableError

web_blueprint = Blueprint("web", __name__)


def pilot_page(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_app.config["PILOT_DEMO_ENABLED"]:
            abort(404)
        if g.current_identity is None:
            return render_template("pilot/error.html", message="A synthetic identity is required."), 401
        try:
            return view(*args, **kwargs)
        except PilotAccessError as error:
            return render_template("pilot/error.html", message=str(error)), error.status
        except PilotUnavailableError as error:
            return render_template("pilot/error.html", message=str(error)), 503
    return wrapped


def reader() -> PilotReader:
    return current_app.extensions["pilot_reader"]


def diagnostic_context() -> dict[str, str]:
    return {"purpose": request.args.get("purpose", ""), "reference": request.args.get("reference", "")}


def rows():
    return reader().list_rows(g.current_identity.user_id, **diagnostic_context())


@web_blueprint.app_context_processor
def pilot_context():
    if "csrf_token" not in session and current_app.config["PILOT_DEMO_ENABLED"]:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return {
        "pilot": current_app.config["PILOT_DEMO_ENABLED"],
        "as_of": current_app.config.get("PILOT_AS_OF"),
        "identity": getattr(g, "current_identity", None),
        "csrf_token": session.get("csrf_token", ""),
        "diagnostic": diagnostic_context(),
    }


@web_blueprint.get("/")
def home() -> str:
    if current_app.config["PILOT_DEMO_ENABLED"]:
        return dashboard()
    return render_template("home.html")


@pilot_page
def dashboard():
    visible = rows()
    return render_template("pilot/dashboard.html", rows=visible,
        overdue=sum(row.overdue for row in visible),
        pending=sum("signature" in row.state for row in visible),
        finalized=sum(row.state == "Finalized" for row in visible))


@web_blueprint.get("/work")
@pilot_page
def work():
    visible = rows()
    query = request.args.get("q", "").strip()
    state = request.args.get("state", "")
    sort = request.args.get("sort", "due")
    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        page = 0
    if len(query) > 200 or sort not in {"due", "person"} or page < 1:
        raise PilotAccessError(400, "Invalid search, sort, or page value.")
    states = sorted({row.state for row in visible})
    if state and state not in states:
        raise PilotAccessError(400, "Select a visible workflow state.")
    filtered = [row for row in visible if (not state or row.state == state)
                and query.casefold() in f"{row.id} {row.employee} {row.team} {row.grouping}".casefold()]
    filtered.sort(key=lambda row: (row.due_date, row.id) if sort == "due" else (row.employee, row.id))
    pages = max(1, ceil(len(filtered) / 10))
    if page > pages:
        raise PilotAccessError(400, "The requested page is not available.")
    return render_template("pilot/work.html", rows=filtered[(page-1)*10:page*10],
        total=len(filtered), q=query, selected_state=state, states=states,
        sort=sort, page=page, pages=pages)


@web_blueprint.get("/assessments/<record_id>")
@pilot_page
def detail(record_id: str):
    record = reader().detail(g.current_identity.user_id, record_id, **diagnostic_context())
    return render_template("pilot/detail.html", record=record)


@web_blueprint.get("/assessments/<record_id>/history")
@pilot_page
def history(record_id: str):
    record = reader().detail(g.current_identity.user_id, record_id, **diagnostic_context())
    return render_template("pilot/history.html", record=record)


@web_blueprint.route("/assistants/<bot>", methods=["GET", "POST"])
@pilot_page
def assistant(bot: str):
    if bot not in BOTS:
        abort(404)
    rows()  # Validate the configured account; source examples contain no record data.
    result = None
    question = ""
    error = None
    status = 200
    if request.method == "POST":
        supplied = request.form.get("csrf_token", "")
        expected = session.get("csrf_token", "")
        if not expected or not hmac.compare_digest(supplied.encode("utf-8"), expected.encode("utf-8")):
            raise PilotAccessError(400, "The form expired. Reload the page and try again.")
        question = request.form.get("question", "").strip()
        if not question or len(question) > 500:
            error, status = "Enter a question between 1 and 500 characters.", 400
        else:
            result = answer(bot, question)
            session["csrf_token"] = secrets.token_urlsafe(32)
    return render_template("pilot/assistant.html", bot=bot, title=BOTS[bot][0],
        sample=BOTS[bot][1], question=question, result=result, error=error), status


@web_blueprint.get("/health")
def health() -> dict[str, str]:
    """Return only the minimum information needed for a health probe."""

    return {"status": "healthy"}
