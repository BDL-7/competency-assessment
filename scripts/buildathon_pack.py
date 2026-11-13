"""Generate, validate and load the explicitly fictional buildathon pack."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alembic import command
from alembic.config import Config
from flask import Flask
from sqlalchemy import Date, DateTime, create_engine, event, select
from sqlalchemy.exc import IntegrityError

from app.data.database import configure_database
from app.data.demo import initialize_demo
from app.data.models import Base
from scripts.generate_users import generate_users

PACK = ROOT / "tests" / "fixtures" / "synthetic"
REFERENCE = date(2026, 11, 13)
TABLES = (
    "team", "employee", "application_user", "test_system", "process_grouping",
    "process_grouping_test_system", "assignment", "assessment", "role_assignment",
    "assessment_draft", "assessment_draft_element", "assessment_version",
    "assessment_element", "signature", "assessment_document", "renewal",
    "notification_event", "notification_attempt", "audit_event", "idempotency_record",
)
EXPECTED_COUNTS = dict(zip(TABLES, (
    5, 70, 72, 5, 5, 5, 25, 25, 175, 50, 50, 50, 50,
    40, 25, 20, 25, 25, 25, 0,
)))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def text_hash(path: Path) -> str:
    """Hash canonical UTF-8/LF text independent of Git checkout line endings."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def stamp(year: int, day: int = 20) -> str:
    return f"{year}-02-{day:02}T12:00:00+00:00"


def seed_snapshot(directory: Path) -> dict:
    """Reuse the actual old demo rather than author a competing assessment form."""
    app = Flask("app")
    app.config.update(
        DATABASE_URL=f"sqlite:///{directory / 'seed.db'}",
        PILOT_DEMO_ENABLED=True, APP_ENV="testing",
    )
    resources = configure_database(app)
    engine = resources["engine"]
    try:
        initialize_demo(app)
        with engine.connect() as connection:
            return {
                name: [
                    {
                        key: value.isoformat() if isinstance(value, (date, datetime)) else value
                        for key, value in row.items()
                    }
                    for row in connection.execute(
                        select(Base.metadata.tables[name]).order_by(
                            Base.metadata.tables[name].c.id
                        )
                    ).mappings()
                ]
                for name in TABLES
            }
    finally:
        engine.dispose()


def generate_app() -> tuple[dict, dict]:
    with tempfile.TemporaryDirectory(prefix="synthetic-pack-") as directory_name:
        directory = Path(directory_name)
        generate_users(directory / "people.csv")
        with (directory / "people.csv").open(newline="", encoding="utf-8") as source:
            roster = list(csv.DictReader(source))
        seed = seed_snapshot(directory)
    tables = {name: [] for name in TABLES}
    fixed_created = "2021-01-01T00:00:00+00:00"
    seed_people = [row["id"] for row in seed["employee"]]
    # The demo's participant identifiers, not roster labels, define these scopes.
    ordered_people = (
        "SYN-EMP-001", "SYN-LEAD-001", "SYN-ASR-001", "SYN-TS-001",
        "SYN-ADM-001", "SYN-PLAT-001", "SYN-OUT-001",
    )
    projections = []
    artifact = PACK / "synthetic-attachment.txt"
    artifact_hash = text_hash(artifact)
    for lab in range(1, 6):
        prefix = f"SYN-L{lab}"
        people = roster[(lab - 1) * 14:lab * 14]
        people_map = dict(zip(ordered_people, [p["synthetic_user_id"] for p in people]))
        for person in people:
            identifier = person["synthetic_user_id"]
            tables["employee"].append(dict(
                id=identifier, team_id=f"{prefix}-TEAM",
                display_label=person["display_name"], is_active=True,
                role_context=person["illustrative_demo_roles"],
                source_lineage="Synthetic roster labels only; not authorization",
                created_at=fixed_created,
            ))
            tables["application_user"].append(dict(
                id=identifier, identity_provider_subject=identifier,
                employee_id=identifier, is_mock_identity=True, is_active=True,
                created_at=fixed_created,
            ))
        config_ids = {
            "SYN-TEAM-ALPHA": f"{prefix}-TEAM",
            "SYN-PROCESS-01": f"{prefix}-PROCESS",
            "SYN-TEST-SYSTEM-01": f"{prefix}-SYSTEM",
            "SYN-MAP-001": f"{prefix}-MAP",
            "SYN-CFG-001": f"{prefix}-CONFIG",
        }

        def clone(row: dict, identifiers: dict, year: int) -> dict:
            result = {}
            for key, value in row.items():
                if isinstance(value, str):
                    if value in identifiers:
                        value = identifiers[value]
                    elif key.endswith("_at") or key in ("basis_date", "due_date", "starts_at"):
                        original_year = int(value[:4])
                        value = f"{year + original_year - 2027:04}" + value[4:]
                result[key] = value
            # SQL defaults in the original demo use wall-clock time; freeze them.
            if "created_at" in result:
                result["created_at"] = stamp(year, 18)
            if "updated_at" in result:
                result["updated_at"] = stamp(year, 18)
            return result

        for name in ("team", "test_system", "process_grouping", "process_grouping_test_system"):
            for row in seed[name]:
                copied = clone(row, config_ids, 2021)
                copied["created_at"] = fixed_created
                if "display_label" in copied:
                    copied["display_label"] = f"Synthetic Lab {lab} {name.replace('_', ' ')}"
                tables[name].append(copied)
        for year in range(2022, 2027):
            ids = {**config_ids, **people_map}
            for name in TABLES:
                for row in seed[name]:
                    if row["id"] not in ids and row["id"] not in seed_people:
                        ids[row["id"]] = f"{prefix}-{year}-{row['id'][4:]}"
            for name in (
                "assignment", "assessment", "role_assignment", "assessment_draft",
                "assessment_draft_element", "assessment_version", "assessment_element",
            ):
                tables[name].extend(clone(row, ids, year) for row in seed[name])
            assessment = tables["assessment"][-1]
            assignment = tables["assignment"][-1]
            assignment["created_at"] = f"{year - 1}-02-15T00:00:00+00:00"
            assessment["created_at"] = stamp(year, 16)
            version = tables["assessment_version"][-1]
            version_id = ids["SYN-ASMV-002"]
            assert version["id"] == version_id
            finalized = year < 2026
            if finalized:
                assessment["lifecycle_state"] = "Finalized"
                assessment["lock_version"] = 7
                version["is_locked"] = True
                version["finalized_at"] = stamp(year)
                for role, signer, day in (
                    ("testing_personnel", people_map["SYN-EMP-001"], 19),
                    ("technical_supervisor", people_map["SYN-TS-001"], 20),
                ):
                    tables["signature"].append(dict(
                        id=f"{prefix}-{year}-SIGN-{role}", assessment_version_id=version_id,
                        signature_role=role, signer_user_id=signer, signed_at=stamp(year, day),
                        authentication_context="synthetic_fixture_not_legal_signature",
                        request_identity=f"{prefix}-{year}-REQ-{role}", created_at=stamp(year, day),
                    ))
                tables["renewal"].append(dict(
                    id=f"{prefix}-{year}-RENEWAL", finalized_assessment_version_id=version_id,
                    assignment_id=assignment["id"], completion_date=f"{year}-02-20",
                    interval_value=12, interval_unit="calendar_months",
                    next_due_date=f"{year + 1}-02-20",
                    configuration_version_snapshot=config_ids["SYN-CFG-001"],
                    created_at=stamp(year),
                ))
            tables["assessment_document"].append(dict(
                id=f"{prefix}-{year}-DOCUMENT", assessment_version_id=version_id,
                private_object_ref="synthetic-fixture:synthetic-attachment.txt",
                document_kind="synthetic_example", document_version="SYN-1",
                sha256=artifact_hash, uploaded_by_user_id=people_map["SYN-ASR-001"],
                verified_at=stamp(year), created_at=stamp(year),
            ))
            event_id = f"{prefix}-{year}-EVENT"
            tables["notification_event"].append(dict(
                id=event_id, assignment_id=assignment["id"], assessment_id=assessment["id"],
                trigger_name="completed" if finalized else "testing_personnel_signature_required",
                recipient_user_id=people_map["SYN-EMP-001"], template_version="SYN-1",
                record_ref=assessment["id"], scheduled_occurrence=stamp(year),
                status_context=assessment["lifecycle_state"], date_context=f"{year}-02-15",
                idempotency_identity=event_id, event_status="not_delivered_prototype",
                correlation_id=event_id, created_at=stamp(year),
            ))
            tables["notification_attempt"].append(dict(
                id=f"{event_id}-ATTEMPT", notification_event_id=event_id,
                attempt_ordinal=1, adapter_request_ref=f"{event_id}-REQUEST",
                attempted_at=stamp(year), outcome="not_delivered_prototype",
                retry_eligible=False, failure_category="synthetic_non_delivery",
                created_at=stamp(year),
            ))
            tables["audit_event"].append(dict(
                id=f"{prefix}-{year}-AUDIT", actor_user_id=people_map["SYN-ASR-001"],
                action="synthetic_fixture", entity_type="assessment", entity_id=assessment["id"],
                assessment_id=assessment["id"], assignment_id=assignment["id"],
                observed_at=stamp(year), outcome="synthetic",
                request_identity=f"{prefix}-{year}-AUDIT-REQUEST", correlation_id=event_id,
                change_summary="Fictional imported snapshot; not a replay of actual activity",
            ))
        for year in range(2027, 2032):
            projections.append(dict(
                id=f"{prefix}-{year}-PROJECTION", team_id=f"{prefix}-TEAM",
                employee_id=people_map["SYN-EMP-001"],
                process_grouping_id=f"{prefix}-PROCESS",
                planned_date=f"{year}-02-15", status="projected",
                note="Planning only; not an assignment, completed record or notification",
            ))
    for number in (1, 2):
        tables["application_user"].append(dict(
            id=f"SYN-SERVICE-{number:03}",
            identity_provider_subject=f"SYN-SERVICE-{number:03}",
            employee_id=None, is_mock_identity=True, is_active=True,
            created_at=fixed_created,
        ))
    metadata = dict(
        dataset_id="SYN-BUILDATHON-PACK-1", synthetic_only=True,
        reference_date=REFERENCE.isoformat(),
        basis="Purpose-built; existing synthetic demo and roster, not operational sources",
        limitation="Snapshot fixtures, not legally valid signatures or event replay",
    )
    return (
        {**metadata, "tables": tables},
        {**metadata, "projections": projections},
    )


def convert_rows(name: str, rows: list[dict]) -> list[dict]:
    table = Base.metadata.tables[name]
    converted = []
    for row in rows:
        if set(row) - set(table.columns.keys()):
            raise ValueError(f"{name}: unknown columns")
        result = dict(row)
        for column in table.columns:
            value = row.get(column.name)
            if value is None:
                if not column.nullable and column.default is None:
                    raise ValueError(f"{name}.{column.name}: required")
            elif isinstance(column.type, DateTime):
                result[column.name] = datetime.fromisoformat(value)
            elif isinstance(column.type, Date):
                result[column.name] = date.fromisoformat(value)
        converted.append(result)
    return converted


def insert_records(engine, payload: dict) -> None:
    with engine.begin() as connection:
        for name in TABLES:
            for row in convert_rows(name, payload["tables"][name]):
                connection.execute(Base.metadata.tables[name].insert(), row)


def foreign_keys(connection, _record) -> None:
    connection.execute("PRAGMA foreign_keys=ON")


def validate_app(payload: dict, projections: dict) -> dict[str, int]:
    if payload.get("synthetic_only") is not True or projections.get("synthetic_only") is not True:
        raise ValueError("Synthetic-only markers required")
    if set(payload.get("tables", {})) != set(TABLES):
        raise ValueError("Unexpected or missing tables")
    if payload.get("reference_date") != REFERENCE.isoformat() or projections.get("reference_date") != REFERENCE.isoformat():
        raise ValueError("Reference date mismatch")
    tables = payload["tables"]
    counts = {name: len(rows) for name, rows in tables.items()}
    if (counts["employee"], counts["application_user"], counts["team"]) != (70, 72, 5):
        raise ValueError("Expected 70 humans, 72 identities and 5 teams")
    if counts["assignment"] != 25 or counts["assessment_version"] != 50:
        raise ValueError("Expected 25 assignments and 50 issued versions")
    if counts != EXPECTED_COUNTS:
        raise ValueError("Missing or unexpected fixture category counts")
    for name, rows in tables.items():
        ids = [row["id"] for row in rows]
        if len(set(ids)) != len(ids) or any(not item.startswith("SYN-") for item in ids):
            raise ValueError(f"{name}: duplicate or non-synthetic ID")
        for row in rows:
            for key, value in row.items():
                if value and (key.endswith("_at") or key in ("signed_at", "observed_at")):
                    if date.fromisoformat(value[:10]) > REFERENCE:
                        raise ValueError(f"{name}: future completed event")
    if any(not row["is_mock_identity"] for row in tables["application_user"]):
        raise ValueError("Only mock identities permitted")
    if sum(row.get("employee_id") is None for row in tables["application_user"]) != 2:
        raise ValueError("Expected two separate service identities")
    if any(
        sum(employee["team_id"] == team["id"] for employee in tables["employee"]) != 14
        for team in tables["team"]
    ):
        raise ValueError("Expected 14 humans per team")
    assignments = {row["id"]: row for row in tables["assignment"]}
    versions = {row["id"]: row for row in tables["assessment_version"]}
    signatures = tables["signature"]
    for assessment in tables["assessment"]:
        version = versions[assessment["current_version_id"]]
        assignment = assignments[assessment["assignment_id"]]
        if version["assessment_id"] != assessment["id"]:
            raise ValueError("Assessment version ownership mismatch")
        for field in ("employee_id", "assigned_team_lead_id", "assessor_id", "technical_supervisor_id"):
            if assignment[field] != version[field]:
                raise ValueError("Assessment participant mismatch")
        if assessment["lifecycle_state"] not in ("Finalized", "Awaiting Testing Personnel signature"):
            raise ValueError("Unsupported fixture lifecycle state")
        signed = [s for s in signatures if s["assessment_version_id"] == version["id"]]
        finalized = assessment["lifecycle_state"] == "Finalized"
        if finalized:
            if not version["is_locked"] or not version["finalized_at"] or len(signed) != 2:
                raise ValueError("Finalization requires a locked version and two signatures")
            by_role = {s["signature_role"]: s for s in signed}
            if set(by_role) != {"testing_personnel", "technical_supervisor"}:
                raise ValueError("Signature roles incorrect")
            if (
                by_role["testing_personnel"]["signer_user_id"] != version["employee_id"]
                or by_role["technical_supervisor"]["signer_user_id"] != version["technical_supervisor_id"]
                or by_role["testing_personnel"]["signed_at"] > by_role["technical_supervisor"]["signed_at"]
            ):
                raise ValueError("Signature participants or sequence incorrect")
        elif signed or version["is_locked"]:
            raise ValueError("Pending fixtures must remain unsigned and unlocked")
        if version["followup_required"] and not version["followup_description"]:
            raise ValueError("Current version requires documented follow-up")
    for row in tables["renewal"]:
        completion = date.fromisoformat(row["completion_date"])
        if (
            row["interval_value"] != 12 or row["interval_unit"] != "calendar_months"
            or row["next_due_date"] != completion.replace(year=completion.year + 1).isoformat()
        ):
            raise ValueError("Renewal must match the existing synthetic 12-month setting")
    for name in ("assessment", "assessment_version"):
        years = {int(row["created_at"][:4]) for row in tables[name]}
        if years != set(range(2022, 2027)):
            raise ValueError("Historical coverage must be 2022 through 2026")
    projected = projections.get("projections", [])
    if len(projected) != 25 or {int(p["planned_date"][:4]) for p in projected} != set(range(2027, 2032)):
        raise ValueError("Expected 25 projections covering 2027 through 2031")
    for item in projected:
        if item["status"] != "projected" or date.fromisoformat(item["planned_date"]) <= REFERENCE:
            raise ValueError("Future plans must be explicitly projected")
        if set(item) != {"id", "team_id", "employee_id", "process_grouping_id", "planned_date", "status", "note"}:
            raise ValueError("Unexpected projection fields; no completion/signature events allowed")
        for key, table in (("team_id", "team"), ("employee_id", "employee"), ("process_grouping_id", "process_grouping")):
            if item[key] not in {row["id"] for row in tables[table]}:
                raise ValueError(f"Unmatched projection {key}")
    if len({item["id"] for item in projected}) != len(projected):
        raise ValueError("Duplicate projection ID")
    expected_hash = text_hash(PACK / "synthetic-attachment.txt")
    if any(row["sha256"] != expected_hash for row in tables["assessment_document"]):
        raise ValueError("Attachment hash mismatch")
    engine = create_engine("sqlite://")
    event.listen(engine, "connect", foreign_keys)
    try:
        Base.metadata.create_all(engine)
        insert_records(engine, payload)
    except IntegrityError as error:
        raise ValueError(f"Relational integrity failed: {error.orig}") from error
    finally:
        engine.dispose()
    return counts


def validate_corpus() -> int:
    registry = read_json(PACK / "source-registry.json")
    if registry.get("synthetic_only") is not True:
        raise ValueError("Synthetic corpus marker required")
    if registry["upload_files"] != [source["file"] for source in registry["sources"]]:
        raise ValueError("Upload allowlist must exactly match registered text sources")
    sources = {}
    for source in registry["sources"]:
        path = PACK / source["file"]
        if path.parent != PACK or path.suffix != ".txt":
            raise ValueError("Only explicit chatbot text sources may be uploaded")
        content = path.read_text(encoding="utf-8")
        if "SYNTHETIC DEMONSTRATION ONLY" not in content:
            raise ValueError("Missing synthetic source warning")
        if source["sha256"] != text_hash(path):
            raise ValueError("Corpus hash mismatch")
        if source["approval_status"] != "synthetic_demo_only_not_laboratory_approved":
            raise ValueError("Synthetic sources must not claim laboratory approval")
        sources[source["source_id"]] = (source, content)
    evaluations = read_json(PACK / "evaluations.json")["cases"]
    required = {"supported", "unsupported", "conflicting", "retired", "inaccessible",
                "insufficient", "prompt_injection", "prohibited_action", "individual_record"}
    if {case["kind"] for case in evaluations} != required:
        raise ValueError("Missing chatbot evaluation categories")
    for case in evaluations:
        if case["kind"] == "supported":
            source, content = sources[case["source_id"]]
            if not source["active"] or case["location"] not in content or case["supporting_quote"] not in content:
                raise ValueError("Supported citation not found in active source")
        elif case["expected_outcome"] not in ("escalate", "refuse"):
            raise ValueError("Unsafe expected chatbot outcome")
    return len(evaluations)


def validate_pack() -> dict:
    counts = validate_app(
        read_json(PACK / "records.json"),
        read_json(PACK / "projections.json"),
    )
    cases = read_json(PACK / "invalid-cases.json")["cases"]
    for case in cases:
        payload = read_json(PACK / "records.json")
        payload["tables"][case["table"]][case["row"]][case["field"]] = case["value"]
        try:
            validate_app(payload, read_json(PACK / "projections.json"))
        except ValueError as error:
            if case["expected_error"] not in str(error):
                raise ValueError(f"Wrong rejection for {case['id']}: {error}") from error
        else:
            raise ValueError(f"Invalid case accepted: {case['id']}")
    return {"tables": counts, "invalid_cases_rejected": len(cases),
            "chatbot_fixture_cases": validate_corpus()}


def load_database(path: Path, payload: dict | None = None, projections: dict | None = None) -> dict:
    """Create only a new explicit SQLite target; never reset an existing file."""
    if (payload is None) != (projections is None):
        raise ValueError("Both records and projections are required")
    if payload is None:
        result = validate_pack()
        payload = read_json(PACK / "records.json")
    else:
        result = {"tables": validate_app(payload, projections)}
    path = path.resolve()
    if path.suffix != ".db" or not path.parent.is_dir():
        raise ValueError("Choose a .db file in an existing dedicated directory")
    if os.getenv("DATABASE_URL"):
        raise ValueError("Unset DATABASE_URL before loading")
    # Exclusive creation closes the check/create race and refuses unknown databases.
    with path.open("xb"):
        pass
    engine = create_engine(f"sqlite:///{path}")
    event.listen(engine, "connect", foreign_keys)
    try:
        config = Config(str(ROOT / "alembic.ini"))
        config.set_main_option("script_location", str(ROOT / "migrations"))
        config.set_main_option("sqlalchemy.url", str(engine.url).replace("%", "%%"))
        command.upgrade(config, "head")
        insert_records(engine, payload)
    finally:
        engine.dispose()
    return result


def generate() -> None:
    records, projections = generate_app()
    write_json(PACK / "records.json", records)
    write_json(PACK / "projections.json", projections)
    registry_path = PACK / "source-registry.json"
    registry = read_json(registry_path)
    for source in registry["sources"]:
        source["sha256"] = text_hash(PACK / source["file"])
    write_json(registry_path, registry)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("generate", "validate", "load"))
    parser.add_argument("--database", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "generate":
            generate()
        if args.action == "load":
            if args.database is None:
                raise ValueError("load requires --database pointing to a NEW synthetic .db file")
            result = load_database(args.database)
        else:
            result = validate_pack()
    except (ValueError, OSError) as error:
        parser.exit(1, f"Buildathon pack failed: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
