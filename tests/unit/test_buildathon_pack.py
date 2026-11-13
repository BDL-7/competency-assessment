"""Integrity and safe loading checks for the tracked synthetic input pack."""

import hashlib
import re
import pytest
from sqlalchemy import create_engine, select

from app.data.models import Base
from scripts import buildathon_pack as pack


def inputs():
    return (
        pack.read_json(pack.PACK / "records.json"),
        pack.read_json(pack.PACK / "projections.json"),
    )


def test_pack_counts_citations_and_negative_examples():
    result = pack.validate_pack()
    assert result["tables"]["employee"] == 70
    assert result["tables"]["application_user"] == 72
    assert result["tables"]["team"] == 5
    assert result["tables"]["signature"] == 40
    assert result["invalid_cases_rejected"] == 8
    assert result["chatbot_fixture_cases"] == 9


def test_generation_reuses_existing_demo_and_is_reproducible(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    records, projections = pack.generate_app()
    assert (records, projections) == inputs()


@pytest.mark.parametrize("kind", ["future", "duplicate", "mismatched_participant", "bad_signature", "bad_renewal"])
def test_corrupt_completed_data_is_rejected(kind):
    records, projections = inputs()
    if kind == "future":
        records["tables"]["audit_event"][0]["observed_at"] = "2030-01-01T00:00:00+00:00"
    elif kind == "duplicate":
        records["tables"]["employee"][1]["id"] = records["tables"]["employee"][0]["id"]
    elif kind == "mismatched_participant":
        records["tables"]["assessment_version"][1]["assessor_id"] = "SYN-HUMAN-001"
    elif kind == "bad_signature":
        records["tables"]["signature"][0]["signer_user_id"] = "SYN-HUMAN-003"
    else:
        records["tables"]["renewal"][0]["next_due_date"] = "2024-01-01"
    with pytest.raises(ValueError):
        pack.validate_app(records, projections)


@pytest.mark.parametrize("kind", ["completed", "past", "unknown_reference", "duplicate", "extra_field"])
def test_projection_boundary_is_enforced(kind):
    records, projections = inputs()
    item = projections["projections"][0]
    if kind == "completed":
        item["status"] = "completed"
    elif kind == "past":
        item["planned_date"] = "2020-01-01"
    elif kind == "unknown_reference":
        item["employee_id"] = "SYN-MISSING"
    elif kind == "duplicate":
        projections["projections"][1]["id"] = item["id"]
    else:
        item["signed_at"] = "2030-01-01"
    with pytest.raises(ValueError):
        pack.validate_app(records, projections)


def test_loads_real_migration_foreign_keys_and_explicit_scope(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    path = tmp_path / "synthetic-pack.db"
    pack.load_database(path)
    engine = create_engine(f"sqlite:///{path}")
    try:
        tables = Base.metadata.tables
        with engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA foreign_key_check").all() == []
            assert len(connection.execute(select(tables["employee"])).all()) == 70
            assert connection.exec_driver_sql("SELECT version_num FROM alembic_version").scalar_one()
            employee = "SYN-HUMAN-001"
            scopes = connection.execute(
                select(tables["role_assignment"].c.assessment_id).where(
                    tables["role_assignment"].c.user_id == employee,
                    tables["role_assignment"].c.role_name == "employee",
                )
            ).scalars().all()
            visible = connection.execute(
                select(tables["assessment"].c.id)
                .join(tables["assignment"], tables["assessment"].c.assignment_id == tables["assignment"].c.id)
                .where(tables["assignment"].c.employee_id == employee,
                       tables["assessment"].c.id.in_(scopes))
            ).scalars().all()
            assert len(visible) == 5
            outsider_scopes = connection.execute(
                select(tables["role_assignment"].c.assessment_id).where(
                    tables["role_assignment"].c.user_id == "SYN-HUMAN-007"
                )
            ).scalars().all()
            assert set(outsider_scopes) == {None}
    finally:
        engine.dispose()
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(FileExistsError):
        pack.load_database(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before


def test_environment_override_rejected_without_creating_file(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///not-the-pack.db")
    target = tmp_path / "synthetic.db"
    with pytest.raises(ValueError, match="Unset DATABASE_URL"):
        pack.load_database(target)
    assert not target.exists()


def test_corpus_hash_citation_and_upload_allowlist(tmp_path, monkeypatch):
    chatbot = tmp_path
    for name in ("source-registry.json", "demo-guide.txt", "evaluations.json"):
        (chatbot / name).write_bytes((pack.PACK / name).read_bytes())
    monkeypatch.setattr(pack, "PACK", tmp_path)
    assert pack.validate_corpus() == 9
    (chatbot / "demo-guide.txt").write_text("SYNTHETIC DEMONSTRATION ONLY\nChanged source", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        pack.validate_corpus()


def test_unknown_columns_rejected():
    with pytest.raises(ValueError, match="unknown columns"):
        pack.convert_rows("team", [{"id": "SYN-TEAM", "surprise": True}])


def test_text_hash_is_stable_across_windows_and_unix_checkouts(tmp_path):
    path = tmp_path / "synthetic.txt"
    path.write_bytes(b"SYNTHETIC\nExample\n")
    expected = pack.text_hash(path)
    path.write_bytes(b"SYNTHETIC\r\nExample\r\n")
    assert pack.text_hash(path) == expected


def test_inventory_local_links_resolve():
    index = pack.ROOT / "docs" / "DATA_INVENTORY.md"
    targets = re.findall(r"\]\(([^)]+)\)", index.read_text(encoding="utf-8"))
    assert targets
    for target in targets:
        assert (index.parent / target).is_file(), target


def test_missing_category_data_is_not_treated_as_ready():
    records, projections = inputs()
    records["tables"]["audit_event"] = []
    with pytest.raises(ValueError, match="category counts"):
        pack.validate_app(records, projections)
