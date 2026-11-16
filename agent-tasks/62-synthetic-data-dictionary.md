# Task #62: Synthetic data dictionary

- Owner / lease: Orchestrator documentation integration, exclusive until draft
  PR handoff, revocation or abandonment.
- Goal: document every column in the tracked generated synthetic app pack,
  projections, roster, workbook sheets and companion scenario/assistant
  specification datasets; explain type, meaning, values, nullability,
  generation and relationships without creating new data or policy.
- Required context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`,
  `docs/PRODUCT.md`, `docs/DEVELOPMENT.md`, `docs/DATA_CLASSIFICATION.md`,
  `docs/DATA_INVENTORY.md`, applicable current task index and approved public
  pack/schema/generator sources.
- Source of truth: public `app/data/models.py`, `scripts/buildathon_pack.py`,
  `scripts/buildathon_workbooks.py`, `scripts/generate_users.py` and the exact
  tracked `tests/fixtures/synthetic/` JSON/text fixtures. Public historical
  contracts describe provenance, not permission to read root `data/`.
- Dependency / approval: requester explicitly requested the complete dictionary
  and selected `docs/DATA_DICTIONARY.md` as its tracked destination instead of
  protected, ignored root `data/`. Branch from merged `origin/dev`.
- Allowed files: this exact contract, `docs/DATA_DICTIONARY.md`,
  `docs/DATA_INVENTORY.md`, `docs/README.md` and `agent-tasks/README.md`.
- Review-only: every other path, including all generator/schema/fixture source.
  Never open, enumerate, hash, write or move root `data/` or other protected
  sources/unknown databases.
- Prohibited: new data generation, workbook generation, schema/runtime changes,
  inferred laboratory policy/CLIA applicability, external upload, deployment,
  deletion, merge, or blanket staging.
- Expected output: one field-level dictionary covering all current app tables,
  projection records, roster columns, workbook `README` cells, JSON envelope
  and case/source/evaluation records. Distinguish database physical types and
  constraints, JSON representations and observed fixture values; explicitly
  label incomplete/missing data and policy gates.
- Acceptance: programmatically compare dictionary entries against public
  fixture keys, model columns and generator-declared roster/projection fields;
  no missing or invented fields, links resolve, examples contain fictional
  identifiers only. Link from existing inventory/index.
- Validation: selected-task Python 3.12 preflight; bounded field coverage and
  local links; repository working/staged verifier and whitespace; CI.
- Independent review: validate completeness, type/nullable/foreign-key
  distinctions, generation explanations and no false compliance claims.
- Stop: ambiguous source meaning needing owner decision, overlapping lease,
  unsafe source access, or required out-of-scope edit.
- Handoff: exact changed files, validation results, unverified generated local
  outputs and pending policy/source approvals; independent AI review is not
  human acceptance.

Contract-only bootstrap precedes draft PR creation under the previously
approved issue-first publication exception. The PR targets `dev`; no merge is
authorized by this task.

## Documentation handoff

- Changed documentation: `docs/DATA_DICTIONARY.md` (current tracked synthetic
  field dictionary), `docs/DATA_INVENTORY.md` and `docs/README.md` (navigation),
  `agent-tasks/README.md` (current task index), and this contract.
- Read-only comparison confirmed all 223 SQL model columns across 20 tables
  against dictionary field names, physical types, nullability and foreign keys;
  verified three schema-only nullable columns absent from nonempty JSON rows.
  Separate key checks covered projection and roster fields and every observed
  companion JSON envelope, nested case/source and evaluation overlay key.
- Local Markdown links, selected-task Python 3.12 preflight, working-tree
  repository verifier and whitespace check passed. Independent read-only
  review found no significant issue. Staged verification and final-head CI
  remain publication checks; no local protected workbooks were inspected.
- This is not human approval of laboratory rules, source access, assistant
  publication, data migration, deployment or any actual signature/delivery.
