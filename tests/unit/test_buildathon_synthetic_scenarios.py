"""Safety and shape checks for the synthetic buildathon scenario catalog."""

import csv
import json
from pathlib import Path

from scripts.generate_users import FIELDNAMES, OUTPUT_PATH, generate_users

CATALOG_PATH = (
    Path(__file__).parents[2]
    / "tests"
    / "fixtures"
    / "synthetic"
    / "edge-cases.json"
)
EXPECTED_USER_COUNT = 70


def test_catalog_is_explicitly_synthetic_and_scenario_only():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["synthetic_only"] is True
    assert catalog["source_basis"] == (
        "purpose-built scenarios; not derived from operational records"
    )
    assert len(catalog["cases"]) == 5
    assert all(case["case_id"].startswith("SYN-EDGE-") for case in catalog["cases"])
    assert all("scenario" in case and "expected_handling" in case for case in catalog["cases"])


def test_catalog_covers_gaps_conflicts_and_projections_without_resolving_them():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    cases = {case["kind"]: case for case in catalog["cases"]}

    assert {"optional_information_missing", "work_in_progress_incomplete",
            "conflicting_candidate_values", "future_projection"} <= cases.keys()
    assert "do not select" in cases["conflicting_candidate_values"]["expected_handling"]
    assert "do not represent it as a completed" in cases["future_projection"]["expected_handling"]


def test_user_generator_writes_varied_fictional_roles(tmp_path):
    roster_path = tmp_path / "users.csv"

    assert generate_users(roster_path) == EXPECTED_USER_COUNT
    with roster_path.open(encoding="utf-8", newline="") as roster_file:
        reader = csv.DictReader(roster_file)
        assert reader.fieldnames == list(FIELDNAMES)
        users = list(reader)

    assert OUTPUT_PATH == Path(__file__).parents[2] / "data" / "users.csv"
    role_counts = {}
    for user in users:
        roles = user["illustrative_demo_roles"]
        role_counts[roles] = role_counts.get(roles, 0) + 1
    assert role_counts == {
        "employee": 36,
        "team_lead": 8,
        "assessor": 10,
        "technical_supervisor": 5,
        "employee;assessor": 4,
        "team_lead;assessor": 3,
        "squad_admin": 2,
        "platform_admin": 1,
        "assessor;technical_supervisor": 1,
    }

    assert len(users) == EXPECTED_USER_COUNT
    assert len({user["synthetic_user_id"] for user in users}) == EXPECTED_USER_COUNT
    assert {user["identity_type"] for user in users} == {"human"}
    assert {user["synthetic_only"] for user in users} == {"true"}
    assert len({user["illustrative_demo_roles"] for user in users}) > 1
    assert {role for user in users for role in user["illustrative_demo_roles"].split(";")} == {
        "employee",
        "team_lead",
        "assessor",
        "technical_supervisor",
        "squad_admin",
        "platform_admin",
    }


def test_user_generator_is_repeatable(tmp_path):
    roster_path = tmp_path / "users.csv"

    generate_users(roster_path)
    first_generation = roster_path.read_bytes()
    generate_users(roster_path)

    assert roster_path.read_bytes() == first_generation
