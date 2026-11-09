"""Safety and shape checks for the synthetic buildathon scenario catalog."""

import json
from pathlib import Path


CATALOG_PATH = (
    Path(__file__).parents[2]
    / "data"
    / "synthetic"
    / "buildathon"
    / "edge-cases.json"
)


def test_catalog_is_explicitly_synthetic_and_scenario_only():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    assert catalog["synthetic_only"] is True
    assert catalog["source_basis"] == (
        "purpose-built scenarios; not derived from operational records"
    )
    assert catalog["cases"]
    assert all(case["case_id"].startswith("SYN-EDGE-") for case in catalog["cases"])
    assert all("scenario" in case and "expected_handling" in case for case in catalog["cases"])


def test_catalog_covers_gaps_conflicts_and_projections_without_resolving_them():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    cases = {case["kind"]: case for case in catalog["cases"]}

    assert {"optional_information_missing", "work_in_progress_incomplete",
            "conflicting_candidate_values", "future_projection"} <= cases.keys()
    assert "do not select" in cases["conflicting_candidate_values"]["expected_handling"]
    assert "do not represent it as a completed" in cases["future_projection"]["expected_handling"]
