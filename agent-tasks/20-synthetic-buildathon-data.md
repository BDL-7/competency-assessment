# Synthetic Buildathon Dataset

## Contract

- Task: #20; owner: Orchestrator; requester approved a separate, purpose-built
  synthetic dataset direction.
- Goal: provide a local-only, reproducible roster of 70 fictional users with
  varied illustrative roles, alongside a schema-neutral edge-case catalog,
  without using HIR/MIST as data sources or changing application behavior.
- Business reason: create test scenarios that better exercise data-quality and
  workflow gaps than the existing one-assessment demo, while avoiding
  operational-data exposure and preserving the existing regression fixture.
- Required context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`,
  `docs/PRODUCT.md`, `data/DATA_CLASSIFICATION.md`,
  `docs/DATA_MIGRATION.md`, `docs/BUILDATHON.md`, and issue #20.
- Source of truth: the current product, authorization, workflow, and data
  classification documents. HIR/MIST are not canonical format or value
  sources.
- Dependencies: owner approval remains required before using role counts as
  policy, loading roster data into the application, or adding any schema,
  taxonomy, projection, or required-field semantics.
- Approved assumptions: the requester directed that a synthetic user roster
  be prepared locally and Git-ignored, with varied roles. The roster is a
  fictional UI/demo aid only, separate from the existing S0-07 demo; its role
  mix is illustrative and does not encode permissions or policy. It must not
  use HIR/MIST content.
- Allowed files:
  - `agent-tasks/20-synthetic-buildathon-data.md`
  - `data/README.md`
  - `data/synthetic/buildathon/README.md`
  - `data/synthetic/buildathon/generate_users.py`
  - `data/synthetic/buildathon/edge-cases.json`
  - `tests/unit/test_buildathon_synthetic_scenarios.py`
  - local ignored output `data/synthetic/buildathon/users.csv`
- Review-only files: controlled sources, `data/migration/` workbooks,
  `data/authoritative/` workbooks, and `data/reference/` workbooks.
- Prohibited actions: copying, anonymizing, sampling, transforming, or
  inferring values, taxonomies, or distributions from HIR/MIST; changing the
  S0-07 demo; adding application schema/workflow/authorization behavior;
  representing a projection as a completed event; adding CLIA workflow/rules;
  using production data; migration execution; cloud provisioning or deployment.
- Expected outputs: a clearly labeled synthetic edge-case catalog, a
  deterministic 70-person local roster, and focused tests.
- Acceptance criteria:
  - Every catalog entry is explicitly fictional and is not an operational
    person/assessment record.
  - Cases describe missing/incomplete information and conflicting candidate
    values without silently resolving them.
  - Projected activity is distinguished from completed activity and does not
    claim signatures or events occurred.
  - The roster uses fictional identities and varied, explicitly illustrative
    labels from the existing role vocabulary; no permissions are granted.
  - The generated roster is Git-ignored and not loaded into the application.
  - The current demo and unrelated worktree changes remain untouched.
- Validation commands:
  - `.venv\Scripts\python.exe -m pytest tests\unit\test_buildathon_synthetic_scenarios.py`
  - `.venv\Scripts\python.exe data\synthetic\buildathon\generate_users.py`
  - `git check-ignore -v -- data/synthetic/buildathon/users.csv`
  - `.venv\Scripts\python.exe scripts\verify_repository.py`
  - `git diff --check`
- Security/privacy: use synthetic placeholders only; do not inspect or repeat
  controlled workbook contents or identifiable workforce data.
- Definition of done: catalog, local roster, tests, and local-use limitations
  are complete; validation results and unresolved owner decisions are
  recorded. This contract does not authorize loading the roster into the app.
- Handoff: report exact changed files, validation results, unresolved gates,
  and the next responsible owner.
- Stop conditions: missing owner approval for population distribution,
  conflicting authority, required-field or projection semantics needing
  laboratory judgment, or any possibility of using operational data.
- Human approval gate: owner approval is required before selecting population
  counts/distributions, adding schema/taxonomy, or resolving laboratory or
  required-field rules.
- Path lease owner and expiry: Orchestrator; expires when issue #20 is merged
  or closed.
