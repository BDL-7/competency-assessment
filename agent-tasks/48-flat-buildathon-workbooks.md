# Task #48: Flat local Excel buildathon files

- Owner Agent: Orchestrator / implementation and integration.
- Goal: Generate connected fictional Excel workbooks and chatbot text directly
  under an entirely ignored `data/`, with reproducible public sources outside it.
- Business Reason: Make the actual buildathon files easy to find and edit in
  Excel without committing local data.
- Required Context: AGENTS.md; docs/SOURCE_AUTHORITY.md; docs/PRODUCT.md;
  docs/DEVELOPMENT.md; docs/AI_BOUNDARY.md; docs/SOURCE_MANIFEST.md;
  data/DATA_CLASSIFICATION.md; agent-tasks/45-buildathon-data-pack.md.
- Source-of-Truth Files: Existing tracked fictional pack, roster generator and
  app models. No operational or controlled input may be opened or used.
- Dependencies: Existing demo/migrations and pinned Excel tooling.
- Approved Assumptions: Requester approved tracking public synthetic fixtures,
  source code and docs outside `data/`; generating ignored local workbooks;
  untracking the `data/` tree; and a contract-only bootstrap commit for a draft
  PR. Five linked sheets-based Excel workbooks / text set reuse existing data.
- Allowed Files:
  - agent-tasks/48-flat-buildathon-workbooks.md
  - .gitignore, requirements-dev.in, requirements-dev.lock
  - README.md, docs/README.md, docs/DEVELOPMENT.md, docs/archive/README.md
  - docs/DATA_CLASSIFICATION.md, docs/DATA_INVENTORY.md
  - data/DATA_CLASSIFICATION.md, data/README.md, data/examples/README.md,
    data/examples/generate_users.py, data/examples/edge-cases.json
  - data/examples/buildathon/app/records.json, projections.json,
    invalid-cases.json, synthetic-attachment.txt
  - data/examples/buildathon/chatbot/demo-guide.txt, source-registry.json,
    evaluations.json
  - tests/fixtures/synthetic/records.json, projections.json, invalid-cases.json,
    synthetic-attachment.txt, demo-guide.txt, source-registry.json,
    evaluations.json, edge-cases.json
  - scripts/generate_users.py, scripts/buildathon_pack.py,
    scripts/buildathon_workbooks.py, scripts/verify_repository.py
  - tests/unit/test_buildathon_pack.py, tests/unit/test_buildathon_synthetic_scenarios.py,
    tests/unit/test_buildathon_workbooks.py
  - Locally generated `data/people-and-teams.xlsx`,
    `data/systems-and-assignments.xlsx`, `data/assessments-and-history.xlsx`,
    `data/future-planning.xlsx`, `data/competency-demo.txt`.
- Review-Only Files: All other paths, including controlled/local workbooks.
  Preserve unrelated `docs/buildathon-resources/` and all unknown data files.
- Prohibited Actions: Overwrite unknown local files; alter history; ingest real
  sources; change lab policy, permissions, schema, UI or cloud systems.
- Expected Outputs: Flat ignored files, guarded generation, validated workbook
  load, reproducible tracked sources, migrated guidance and exact file index.
- Acceptance Criteria: All `data/` contents ignored and untracked; 70 humans,
  relationships and existing safety cases preserved; 5-year projections remain
  separate; workbook rows round-trip exactly; existing demo and tests pass.
- Validation Commands: Python 3.12 preflight and targeted tests; repository
  and staged checks; workbook load into isolated new SQLite; CI on 3.12.
- Security and Privacy Considerations: Synthetic inputs only; no chatbot access
  to individual assessment records; Git history still retains earlier commits.
- Definition of Done: Outputs and checks verified, independent review when
  required and handoff lists files, untested behavior and outstanding gates.
- Handoff Format: Exact files and validation results; missing approvals.
- Stop Conditions: Unclear source, file ownership, overwrite risk, unsupported
  schema or unapproved policy change.
- Human Approval Gate: No approval for controlled ingestion, model upload,
  deployment or policy changes.
- Path Lease Owner and Expiry: This task exclusively holds the listed paths
  until PR handoff; no parallel writers.
