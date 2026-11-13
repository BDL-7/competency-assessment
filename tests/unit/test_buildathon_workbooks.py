"""Verify synthetic workbooks remain readable, linked and safe to load."""

import hashlib

import pytest
from openpyxl import load_workbook
from sqlalchemy import create_engine, text

from scripts import buildathon_pack as pack
from scripts import buildathon_workbooks as workbooks


@pytest.fixture
def generated(tmp_path):
    workbooks.generate(tmp_path)
    return tmp_path


def test_workbooks_round_trip_every_record_and_projection(generated):
    records, projections = workbooks.read_pack(generated)
    assert records == pack.read_json(pack.PACK / "records.json")
    assert projections == pack.read_json(pack.PACK / "projections.json")
    assert {path.name for path in generated.iterdir()} == set(workbooks.OUTPUTS)
    assert len(records["tables"]["employee"]) == 70
    assert len(records["tables"]["application_user"]) == 72
    assert len(projections["projections"]) == 25


def test_generation_never_overwrites_an_existing_file(tmp_path):
    path = tmp_path / "competency-demo.txt"
    path.write_text("existing user content", encoding="utf-8")
    with pytest.raises(FileExistsError, match="competency-demo.txt"):
        workbooks.generate(tmp_path)
    assert path.read_text(encoding="utf-8") == "existing user content"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["competency-demo.txt"]


@pytest.mark.parametrize("kind", ["bad_header", "formula", "missing_marker", "broken_reference"])
def test_bad_workbook_is_rejected(generated, kind):
    path = generated / "people-and-teams.xlsx"
    book = load_workbook(path)
    if kind == "bad_header":
        book["employee"]["A1"] = "unknown"
    elif kind == "formula":
        book["employee"]["A2"] = '=CONCAT("SYN","-HUMAN")'
    elif kind == "missing_marker":
        book["README"]["A1"] = "not synthetic"
    else:
        sheet = book["employee"]
        headers = [cell.value for cell in sheet[1]]
        sheet.cell(2, headers.index("team_id") + 1, "SYN-MISSING")
    book.save(path)
    book.close()
    with pytest.raises(ValueError):
        workbooks.read_pack(generated)


def test_loads_workbook_records_into_new_database_only(generated, tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    records, projections = workbooks.read_pack(generated)
    target = tmp_path / "synthetic.db"
    pack.load_database(target, records, projections)
    engine = create_engine(f"sqlite:///{target}")
    try:
        with engine.connect() as connection:
            assert connection.execute(text("select count(*) from employee")).scalar_one() == 70
            assert connection.execute(text("select count(*) from assessment")).scalar_one() == 25
            assert connection.exec_driver_sql("pragma foreign_key_check").all() == []
    finally:
        engine.dispose()
    before = hashlib.sha256(target.read_bytes()).digest()
    with pytest.raises(FileExistsError):
        pack.load_database(target, records, projections)
    assert hashlib.sha256(target.read_bytes()).digest() == before


def test_future_projections_cannot_be_completed(generated):
    path = generated / workbooks.PROJECTIONS
    book = load_workbook(path)
    sheet = book["projections"]
    fields = [cell.value for cell in sheet[1]]
    sheet.cell(2, fields.index("status") + 1, "completed")
    book.save(path)
    book.close()
    with pytest.raises(ValueError, match="projected"):
        workbooks.read_pack(generated)
