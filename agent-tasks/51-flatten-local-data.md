# Task #51: Remove remaining local data subfolders

- Owner Agent: Orchestrator / integration.
- Goal: All local data files directly under ignored `data/`, no subdirectories.
- Business Reason: Finish the requested flat layout without losing protected
  workbooks or publishing their contents.
- Required Context: AGENTS.md; docs/SOURCE_AUTHORITY.md; docs/PRODUCT.md;
  docs/DATA_CLASSIFICATION.md; docs/DATA_INVENTORY.md; docs/DEVELOPMENT.md.
- Source-of-Truth Files: Existing public source manifest and current workbook/
  roster tooling. Local protected inputs are filename/metadata-only.
- Dependencies: Existing workbook generator and Python 3.12 CI.
- Approved Assumptions: Requester explicitly approved flattening, removing the
  three stale orphaned Python caches, retaining whole-folder ignore and sharing
  data separately, and contract-only bootstrap publication for a dev-target PR.
- Allowed Files:
  - agent-tasks/51-flatten-local-data.md
  - .gitignore
  - docs/DATA_INVENTORY.md
  - docs/DATA_CLASSIFICATION.md
  - Local metadata-only moves:
    data/authoritative/Approved Test Systems.xlsx -> data/Approved Test Systems.xlsx
    data/migration/Tracking System_HIR.xlsx -> data/Tracking System_HIR.xlsx
    data/migration/Tracking System_MIST.xlsx -> data/Tracking System_MIST.xlsx
    data/reference/CA Relational Tables.xlsx -> data/CA Relational Tables.xlsx
    data/synthetic/buildathon/users.csv -> data/users.csv
  - Delete only:
    data/examples/__pycache__/generate_users.cpython-312.pyc
    data/examples/__pycache__/generate_users.cpython-314.pyc
    data/synthetic/buildathon/__pycache__/generate_users.cpython-314.pyc
  - Remove the inventoried data subdirectories only when confirmed empty.
- Review-Only Files: All other files; contents of local governed/operational
  workbooks remain unopened. Preserve unrelated docs/buildathon-resources/.
- Prohibited Actions: Overwrite a destination; read protected contents; publish
  local data; recursive directory deletion; alter historical task contracts.
- Expected Outputs: Flat local data, updated active references and exact status.
- Acceptance Criteria: Eleven local data files retained; original names and
  sizes preserved; no data subfolders, no tracked data, stale cache removed.
- Validation Commands: Task preflight; targeted workbook/roster/pack tests;
  scripts/verify_repository.py and --staged; git diff --check; Git ignore and
  filesystem metadata checks. Supported-version CI required.
- Security and Privacy Considerations: A shared local folder is not an ingestion
  approval. Operational and governed sources stay restricted and must never be
  included with the separately distributed synthetic pack by default.
- Definition of Done: Local layout and repository references verified, CI
  evidence recorded, required review gates and exact files reported.
- Handoff Format: Changed paths, moved/deleted file counts, validation and gates.
- Stop Conditions: Duplicate filename, unexpected file/link type, changing local
  contents, conflicting lease or unclear approval.
- Human Approval Gate: No approval for source ingestion, release or deployment.
- Path Lease Owner and Expiry: This task exclusively holds these paths through
  PR handoff; no parallel writers.

## Handoff

- Moved the five listed local data files without opening their contents or
  overwriting destinations. Eleven data files retain their original names and
  sizes; three approved stale caches were deleted. All eleven inventoried
  subdirectories were removed only after confirming they were empty.
- Empty OneDrive directories had the ReadOnly attribute; it was cleared on
  those directories only before non-recursive removal. No permission/ACL
  changes, recursive deletion or data-root deletion were performed.
- Updated only `.gitignore`, `docs/DATA_CLASSIFICATION.md` and
  `docs/DATA_INVENTORY.md`, plus this contract. The existing generator and
  loader already use root-level paths; no application code edit was needed.
- Local Python 3.14.2: 31 targeted workbook, roster and pack tests passed;
  actual root-level synthetic workbook validation passed. Manual preflight
  reported unsupported local Python; supported Python 3.12 CI is required.
- Filesystem/Git checks: 11 files, zero directories, all files ignored, zero
  tracked data paths; unrelated untracked work preserved.
- Local moves are not delivered by Git. Other checkouts with old ignored
  directories require their own owner-authorized cleanup. No migration/data
  source is approved for ingestion or sharing by this change.
- Human review remains a PR gate; no operational approval is claimed.
