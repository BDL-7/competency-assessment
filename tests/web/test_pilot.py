"""Local read-only pilot integration and request-boundary tests."""

import re
from datetime import UTC, datetime

import pytest
from sqlalchemy import func, select

from app import create_app
from app.config import ConfigurationError
from app.data.database import get_session_factory
from app.data.models import (
    ApplicationUser, Assessment, AssessmentVersion, AuditEvent, RoleAssignment, Signature,
)


@pytest.fixture
def pilot_app(tmp_path):
    app = create_app("testing", {
        "SECRET_KEY": "synthetic-ui-test", "PILOT_DEMO_ENABLED": True,
        "MOCK_AUTH_ENABLED": True, "MOCK_USER_ID": "SYN-EMP-001",
        "MOCK_DISPLAY_NAME": "Testing Person One",
        "DATABASE_URL": f"sqlite:///{(tmp_path / 'pilot.db').as_posix()}",
    })
    yield app
    app.extensions["database"]["engine"].dispose()


@pytest.fixture
def populated(pilot_app):
    result = pilot_app.test_cli_runner().invoke(args=["init-demo"])
    assert result.exit_code == 0, result.output
    return pilot_app


def token(client, bot="competency"):
    response = client.get(f"/assistants/{bot}")
    assert response.status_code == 200
    return re.search(rb'name="csrf_token" value="([^"]+)"', response.data)[1].decode()


def test_no_http_schema_creation_and_repeat_safe_setup(pilot_app, tmp_path):
    assert pilot_app.test_client().get("/").status_code == 503
    assert not (tmp_path / "pilot.db").exists()
    runner = pilot_app.test_cli_runner()
    assert runner.invoke(args=["init-demo"]).exit_code == 0
    again = runner.invoke(args=["init-demo"])
    assert again.exit_code == 0 and "no records changed" in again.output
    with get_session_factory(pilot_app)() as session:
        assert session.scalar(select(func.count()).select_from(Assessment)) == 1
        assert session.scalar(select(func.count()).select_from(AssessmentVersion)) == 2
        assert session.scalar(select(func.count()).select_from(Signature)) == 0
        assert session.connection().exec_driver_sql("PRAGMA foreign_key_check").all() == []


def test_unknown_database_refused(pilot_app, tmp_path):
    (tmp_path / "pilot.db").write_bytes(b"not-a-demo")
    result = pilot_app.test_cli_runner().invoke(args=["init-demo"])
    assert result.exit_code != 0 and "unknown database" in result.output
    assert (tmp_path / "pilot.db").read_bytes() == b"not-a-demo"


def test_alembic_environment_override_refused(pilot_app, monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///not-the-demo.db")
    result = pilot_app.test_cli_runner().invoke(args=["init-demo"])
    assert result.exit_code != 0 and "Unset DATABASE_URL" in result.output
    assert not (tmp_path / "pilot.db").exists()


def test_read_only_journey(populated):
    client = populated.test_client()
    for path, content in (
        ("/", b"Competency overview"), ("/work", b"1 visible result"),
        ("/assessments/SYN-ASM-001", b"Testing Personnel signature is pending"),
        ("/assessments/SYN-ASM-001/history", b"Version 1"),
        ("/assistants/competency", b"SYNTHETIC MOCK"),
        ("/assistants/manual", b"Equipment manual guide"),
    ):
        response = client.get(path)
        assert response.status_code == 200
        assert content in response.data
        assert b"2027-02-20" in response.data
    assert client.post("/assessments/SYN-ASM-001").status_code == 405
    assert client.get("/health").json == {"status": "healthy"}
    with get_session_factory(populated)() as session:
        assert session.get(Assessment, "SYN-ASM-001").lock_version == 5
        assert session.scalar(select(func.count()).select_from(Signature)) == 0


def test_scope_and_non_disclosure(populated):
    with get_session_factory(populated).begin() as session:
        session.execute(RoleAssignment.__table__.delete().where(RoleAssignment.user_id == "SYN-EMP-001"))
    client = populated.test_client()
    assert b"0 visible results" in client.get("/work").data
    invisible = client.get("/assessments/SYN-ASM-001")
    absent = client.get("/assessments/not-there")
    assert invisible.status_code == absent.status_code == 404
    assert invisible.data == absent.data
    assert b"Synthetic evidence" not in invisible.data


def test_effective_roles_and_participant_relationship(populated):
    factory = get_session_factory(populated)
    with factory.begin() as s:
        role = s.scalar(select(RoleAssignment).where(RoleAssignment.user_id == "SYN-EMP-001"))
        role.ends_at = datetime(2026, 12, 31, tzinfo=UTC)
    assert b"0 visible results" in populated.test_client().get("/work").data
    with factory.begin() as s:
        user = s.get(ApplicationUser, "SYN-EMP-001")
        user.is_active = False
    assert populated.test_client().get("/work").status_code == 403
    with factory() as s:
        assert s.scalar(select(func.count()).select_from(AuditEvent).where(AuditEvent.outcome == "Denied")) > 0


def test_filter_and_page_validation(populated):
    client = populated.test_client()
    assert b"0 visible results" in client.get("/work?q=no-match").data
    for query in ("page=0", "page=999", "page=no", "sort=invalid", "state=invalid"):
        assert client.get(f"/work?{query}").status_code == 400
    assert client.get("/work?sort=person&q=Testing").status_code == 200
    assert b"&lt;script&gt;" in client.get("/work?q=%3Cscript%3E").data


def test_chat_csrf_mock_citations_isolation_and_escalation(populated):
    client = populated.test_client()
    path = "/assistants/competency"
    assert client.post(path, data={"question": "hello"}).status_code == 400
    csrf = token(client)
    assert client.post(path, data={"csrf_token": "非ASCII", "question": "hello"}).status_code == 400
    response = client.post(path, data={"csrf_token": csrf, "question": "What does this demonstration show?"})
    assert response.status_code == 200 and b"SYN-UI-001" in response.data
    assert b"synthetic example" in response.data
    response = client.post("/assistants/manual", data={
        "csrf_token": token(client, "manual"), "question": "What does this demonstration show?"})
    assert b"SYN-UI-001" not in response.data
    assert b"SME" in response.data
    response = client.post("/assistants/manual", data={
        "csrf_token": token(client, "manual"), "question": "Which manual sources are available?"})
    assert b"SYN-UI-002" in response.data and b"No equipment manuals" in response.data
    for question in ("", "x" * 501):
        response = client.post(path, data={"csrf_token": token(client), "question": question})
        assert response.status_code == 400 and b'aria-invalid="true"' in response.data
    response = client.post(path, data={"csrf_token": token(client), "question": "<script>alert(1)</script>"})
    assert b"<script>" not in response.data and b"&lt;script&gt;" in response.data
    with client.session_transaction() as state:
        assert set(state) == {"csrf_token"}


def test_diagnostic_minimized_and_audited(populated):
    reader = populated.extensions["pilot_reader"]
    from app.services.pilot import PilotAccessError
    with pytest.raises(PilotAccessError):
        reader.detail("SYN-PLAT-001", "SYN-ASM-001")
    detail = reader.detail("SYN-PLAT-001", "SYN-ASM-001",
                           purpose="Synthetic investigation", reference="SYN-TICKET")
    assert detail.diagnostic and detail.versions == () and detail.participants == ()
    assert detail.row.employee == "Record status (diagnostic)"
    with get_session_factory(populated)() as s:
        assert s.scalar(select(AuditEvent).where(AuditEvent.support_reference == "SYN-TICKET")) is not None


def test_demo_off_and_production_fail_closed():
    app = create_app("testing", {"SECRET_KEY": "test", "MOCK_AUTH_ENABLED": False})
    assert app.test_client().get("/work").status_code == 404
    assert b"foundation is running" in app.test_client().get("/").data
    with pytest.raises(ConfigurationError):
        create_app("production", {"SECRET_KEY": "test", "PILOT_DEMO_ENABLED": True})


def test_demo_requires_file_target_and_mock_identity():
    for extra in (
        {"MOCK_AUTH_ENABLED": False}, {"DATABASE_URL": "sqlite:///:memory:"},
        {"DATABASE_URL": "not-a-url"}, {"SECRET_KEY": ""}, {"DATABASE_URL": "postgresql://localhost/demo"},
    ):
        config = dict(SECRET_KEY="test", PILOT_DEMO_ENABLED=True, MOCK_AUTH_ENABLED=True,
                      MOCK_USER_ID="SYN-EMP-001", MOCK_DISPLAY_NAME="Synthetic",
                      DATABASE_URL="sqlite:///instance/synthetic-demo.db")
        config.update(extra)
        with pytest.raises(ConfigurationError):
            create_app("testing", config)


def test_lab_atlas_shell_and_working_sample_forms(populated):
    client = populated.test_client()
    overview = client.get("/")
    assert b'Lab Atlas' not in overview.data
    assert b'LAB ATLAS' not in overview.data
    assert b'Assessment tracker' in overview.data
    assert b'<h1>Competency overview</h1>' in overview.data
    assert b'Assessment register' in overview.data
    assert b'class="scope-strip"' in overview.data
    assert overview.data.count(b'id="main-content"') == 1
    assert b'class="attention-card"' in overview.data
    assert b'class="primary-nav"' in overview.data
    detail = client.get("/assessments/SYN-ASM-001")
    assert b'class="dossier-layout"' in detail.data
    assert b'aria-current="page"' in detail.data
    history = client.get("/assessments/SYN-ASM-001/history")
    assert b'class="timeline"' in history.data
    for bot, sample, citation in (
        ("competency", "What does this demonstration show?", b"SYN-UI-001"),
        ("manual", "Which manual sources are available?", b"SYN-UI-002"),
    ):
        csrf = token(client, bot)
        page = client.get(f"/assistants/{bot}")
        assert b'class="sample-form"' in page.data
        response = client.post(f"/assistants/{bot}", data={"question": sample, "csrf_token": csrf})
        assert response.status_code == 200 and citation in response.data
        assert b'No live AI' in response.data
        assert client.post(f"/assistants/{bot}", data={"question": sample, "csrf_token": csrf}).status_code == 400
    foundation = create_app("testing", {"SECRET_KEY": "test", "MOCK_AUTH_ENABLED": False})
    home = foundation.test_client().get("/")
    assert home.data.count(b'id="main-content"') == 1
    assert b'foundation is running' in home.data
