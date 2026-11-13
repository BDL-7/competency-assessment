"""Export and load linked, explicitly fictional buildathon Excel workbooks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from scripts import buildathon_pack as pack

FILES = {
    "people-and-teams.xlsx": ("team", "employee", "application_user", "role_assignment"),
    "systems-and-assignments.xlsx": (
        "test_system", "process_grouping", "process_grouping_test_system", "assignment",
    ),
    "assessments-and-history.xlsx": (
        "assessment", "assessment_draft", "assessment_draft_element", "assessment_version",
        "assessment_element", "signature", "assessment_document", "renewal",
        "notification_event", "notification_attempt", "audit_event", "idempotency_record",
    ),
}
PROJECTIONS = "future-planning.xlsx"
GUIDE = "competency-demo.txt"
ATTACHMENT = "synthetic-attachment.txt"
OUTPUTS = (*FILES, PROJECTIONS, GUIDE, ATTACHMENT)
MARKER = "SYNTHETIC DEMONSTRATION ONLY; NOT LABORATORY POLICY"
PROJECTION_FIELDS = (
    "id", "team_id", "employee_id", "process_grouping_id", "planned_date", "status", "note",
)


def headers_for(name: str, fixture: dict) -> list[str]:
    rows = fixture["tables"][name]
    return list(rows[0]) if rows else [column.name for column in pack.Base.metadata.tables[name].columns]


def add_sheet(book: Workbook, name: str, fields: list[str], rows: list[dict]) -> None:
    sheet = book.create_sheet(name)
    sheet.append(fields)
    sheet.freeze_panes = "B2"
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(fields))}{len(rows) + 1}"
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="305A7B")
    for row in rows:
        sheet.append([row.get(field) for field in fields])
        for cell in sheet[sheet.max_row]:
            if isinstance(cell.value, str):
                cell.data_type = "s"
    for column in sheet.columns:
        sheet.column_dimensions[column[0].column_letter].width = min(
            40, max(14, len(str(column[0].value)) + 2)
        )


def new_book() -> Workbook:
    book = Workbook()
    sheet = book.active
    sheet.title = "README"
    sheet.append([MARKER])
    sheet.append(["Fictional data only. Linked IDs connect sheets and workbooks."])
    sheet.append(["Reference date", pack.REFERENCE.isoformat()])
    sheet.append(["Never treat synthetic signatures, settings or results as real."])
    sheet.column_dimensions["A"].width = 95
    return book


def generate(directory: Path) -> None:
    pack.validate_pack()
    directory.mkdir(parents=True, exist_ok=True)
    existing = [name for name in OUTPUTS if (directory / name).exists()]
    if existing:
        raise FileExistsError("Refusing to overwrite existing files: " + ", ".join(existing))
    payload = pack.read_json(pack.PACK / "records.json")
    projections = pack.read_json(pack.PACK / "projections.json")
    for filename, names in FILES.items():
        book = new_book()
        for name in names:
            add_sheet(book, name, headers_for(name, payload), payload["tables"][name])
        with (directory / filename).open("xb") as target:
            book.save(target)
        book.close()
    book = new_book()
    add_sheet(book, "projections", list(PROJECTION_FIELDS), projections["projections"])
    with (directory / PROJECTIONS).open("xb") as target:
        book.save(target)
    book.close()
    for source, target in (("demo-guide.txt", GUIDE), ("synthetic-attachment.txt", ATTACHMENT)):
        with (directory / target).open("xb") as output:
            output.write((pack.PACK / source).read_bytes())


def read_sheet(sheet, expected_fields: list[str]) -> list[dict]:
    iterator = sheet.iter_rows()
    first = next(iterator, ())
    fields = [cell.value for cell in first]
    if fields != expected_fields:
        raise ValueError(f"{sheet.title}: column headers do not match the synthetic contract")
    rows = []
    for cells in iterator:
        if all(cell.value is None for cell in cells):
            continue
        if any(cell.data_type == "f" for cell in cells):
            raise ValueError(f"{sheet.title}: formulas are not allowed")
        rows.append(dict(zip(fields, (cell.value for cell in cells), strict=True)))
    return rows


def read_workbook(path: Path, sheets: dict[str, list[str]]) -> dict[str, list[dict]]:
    book = load_workbook(path, read_only=True, data_only=False)
    try:
        if set(book.sheetnames) != {"README", *sheets}:
            raise ValueError(f"{path.name}: unexpected or missing sheets")
        if book["README"]["A1"].value != MARKER:
            raise ValueError(f"{path.name}: missing synthetic marker")
        return {name: read_sheet(book[name], fields) for name, fields in sheets.items()}
    finally:
        book.close()


def read_pack(directory: Path) -> tuple[dict, dict]:
    payload = pack.read_json(pack.PACK / "records.json")
    projection_payload = pack.read_json(pack.PACK / "projections.json")
    table_results = {}
    for filename, names in FILES.items():
        fields = {name: headers_for(name, payload) for name in names}
        table_results.update(read_workbook(directory / filename, fields))
    payload["tables"] = table_results
    projection_payload["projections"] = read_workbook(
        directory / PROJECTIONS, {"projections": list(PROJECTION_FIELDS)}
    )["projections"]
    if pack.text_hash(directory / ATTACHMENT) != pack.text_hash(pack.PACK / ATTACHMENT):
        raise ValueError("Synthetic attachment mismatch")
    pack.validate_app(payload, projection_payload)
    return payload, projection_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("generate", "validate", "load"))
    parser.add_argument("--directory", type=Path, default=ROOT / "data")
    parser.add_argument("--database", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "generate":
            generate(args.directory)
        payload, projections = read_pack(args.directory)
        if args.action == "load":
            if args.database is None:
                raise ValueError("load requires --database pointing to a NEW synthetic .db file")
            result = pack.load_database(args.database, payload, projections)
        else:
            result = {"tables": pack.validate_app(payload, projections),
                      "projections": len(projections["projections"])}
    except (ValueError, OSError) as error:
        parser.exit(1, f"Workbook pack failed: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
