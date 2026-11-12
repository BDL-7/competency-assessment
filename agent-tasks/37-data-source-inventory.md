# Task 37: App data-source inventory

Task ID: #37
Owner Agent: Orchestrator / Engineering Lead
Goal: Extend the existing data guide with a source inventory and synthetic-data coverage for the Competency-Assessment app and its competency chatbot.
Business Reason: Help buildathon contributors reuse existing synthetic data, understand governed source boundaries, and identify gaps without creating a duplicate inventory document.
Required Context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`, `agent-tasks/README.md`, `data/DATA_CLASSIFICATION.md`, `data/README.md`, `docs/SOURCE_MANIFEST.md`, `docs/AI_BOUNDARY.md`, `docs/BUILDATHON.md`, `docs/DATA_MIGRATION.md`.
Source-of-Truth Files: `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`, `docs/SOURCE_MANIFEST.md`, `docs/AI_BOUNDARY.md`, `docs/ARCHITECTURE.md`, `docs/OPERATIONS.md`, tracked application models/demo, synthetic examples and tests.
Dependencies: Issue #37; issue-linked branch; PR targeting `dev`.
Approved Assumptions: The buildathon's main goal is the app and competency chatbot. Build from tracked synthetic examples and current app fixtures. Treat protected workbook/document details as filename/status-only based on public manifests and requester-provided descriptions. Equipment-manual chatbot documentation is a future add-on; its knowledge base is out of scope.
Allowed Files:
- `data/README.md`
- `agent-tasks/37-data-source-inventory.md` (this task contract)
Review-Only Files: Controlled project documents/forms/guidance; `data/authoritative/`, `data/migration/`, and `data/reference/` workbooks; ignored local workbooks; operational data.
Prohibited Actions: Open or reproduce controlled contents; use operational data or derivatives in examples; generate a new dataset; change application/schema/workflow/policy; ingest assistant sources; execute migration; enable production services or deploy; create a duplicate inventory document.
Expected Outputs: Update the existing data guide with source categories, access/status, existing synthetic coverage, bounded gap candidates, and links to canonical guidance.
Acceptance Criteria:
- Covers governing documents/form, QMML/NCIRD, approved test-system catalog, MIST/HIR, relational reference, app records/configuration, identity/authorization, artifacts, competency assistant corpus, synthetic demo/test data, and planned integrations.
- Distinguishes tracked synthetic data, modeled-only data, controlled sources, and unavailable integrations/corpus.
- Accurately describes the 70-person generator, five-case catalog, one-assessment read-only local demo, and competency mock.
- Does not imply roster labels grant authorization or that local demo has live AI, signatures, Blob, email, production database, or operational records.
- Equipment-manual chatbot knowledge base remains out of scope.
- Only the two Allowed Files are changed; no controlled contents are accessed.
Validation Commands:
- `.venv\Scripts\python.exe scripts\agent_preflight.py --task 37-data-source-inventory.md`
- `.venv\Scripts\python.exe scripts\verify_repository.py --staged`
- `git diff --check`
- Verify relative Markdown targets in `data/README.md`.
Security and Privacy Considerations: Use synthetic data only. Do not copy, anonymize, sample, transform, or infer from MIST/HIR or controlled catalog/form/guidance contents. Do not expose credentials or workforce data.
Definition of Done: Inventory is accurate, links resolve, staged content contains only approved paths, validation results are recorded, and issue/PR target `dev`.
Handoff Format: Report changed files, validation results, source limitations, and unresolved owner/platform gates.
Stop Conditions: Any protected-content access, ambiguous source authority, need to change role/schema/policy/controlled rules, unexpected path changes, or inability to meet the approved path lease.
Human Approval Gate: Owner approval remains required for controlled-source use, catalog release/loading, population distributions/taxonomies, policy-dependent dates/signatures, source ingestion, migration, production integrations, and deployment.
Path Lease Owner and Expiry: Orchestrator; paths leased for issue #37 until its PR is merged or the issue is closed.
