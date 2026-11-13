# Task #45: Synthetic buildathon pack

- Owner Agent: Orchestrator / implementation and integration.
- Goal: Actual connected synthetic app files, fictional chatbot text documents,
  evaluation examples and one exact-path inventory.
- Business Reason: A clean checkout must supply usable demonstration inputs,
  not only a roster generator and descriptions of missing data.
- Required Context: AGENTS.md; docs/SOURCE_AUTHORITY.md; docs/PRODUCT.md;
  docs/DEVELOPMENT.md; docs/BUILDATHON.md; docs/AI_BOUNDARY.md;
  docs/SOURCE_MANIFEST.md; data/DATA_CLASSIFICATION.md.
- Source-of-Truth Files: Existing app/data/models.py, app/data/demo.py and public
  workflow/authorization guidance; controlled sources are not dataset inputs.
- Dependencies: Existing SQLAlchemy/Alembic stack. Supported Python 3.12 CI.
- Approved Assumptions: Requester approved 70 fictional humans, 5 labs of 14,
  2 separate service identities, existing synthetic configuration values only,
  5 historical years and 5 separate projected years, UTF-8 text chatbot files,
  no upload. Synthetic guidance is not laboratory policy or an approved corpus.
- Allowed Files:
  - agent-tasks/45-buildathon-data-pack.md
  - data/README.md
  - data/examples/README.md
  - data/examples/buildathon/app/records.json
  - data/examples/buildathon/app/projections.json
  - data/examples/buildathon/app/invalid-cases.json
  - data/examples/buildathon/app/synthetic-attachment.txt
  - data/examples/buildathon/chatbot/demo-guide.txt
  - data/examples/buildathon/chatbot/source-registry.json
  - data/examples/buildathon/chatbot/evaluations.json
  - scripts/buildathon_pack.py
  - tests/unit/test_buildathon_pack.py
- Review-Only Files: All other paths; controlled documents/workbooks remain
  unopened. Preserve unrelated docs/buildathon-resources/.
- Prohibited Actions: Operational data use, new schema/policy/UI actions,
  live model/cloud integration, upload, deployment, actual notifications.
- Expected Outputs: Tracked synthetic pack, explicit validator/new-DB loader,
  repeatable checks and index stating usable versus missing.
- Acceptance Criteria: Exact category coverage; 70 humans/2 service identities/
  5 teams; linked records; separate projections; explicit invalid-case failures;
  source hashes/citations; unchanged old demo; clean-checkout setup instructions.
- Validation Commands: Python 3.12 manual preflight; targeted pytest;
  scripts/buildathon_pack.py validate; scripts/verify_repository.py and --staged;
  git diff --check; required CI.
- Security and Privacy Considerations: Fictional SYN identifiers only; app
  assessment records excluded from chatbot upload set. No source publication.
- Definition of Done: Outputs and acceptance checks pass, independent review
  completed, exact changes/results/limitations and human gates reported.
- Handoff Format: Changed paths, validation, untested platform behavior and gates.
- Stop Conditions: Unapproved model extension, source/policy ambiguity,
  overlapping lease, or unsafe Git/index state.
- Human Approval Gate: Requester authorized implementation and contract-only
  bootstrap commit/push before draft PR; real-source ingestion/deployment
  remain unapproved. AI review is not human approval.
- Path Lease Owner and Expiry: This task exclusively holds the listed paths
  until PR handoff; no parallel writers authorized.

## Validation environment

Python 3.12 is unavailable locally. Requester authorized implementation and
available local checks, with supported-version CI required before claiming
validation complete. Do not silently substitute versions in reported evidence.
