# Task #56: Buildathon integration contracts

- Owner Agent: Orchestrator / Engineering Lead.
- Goal: reconcile the requested CLIA and non-CLIA delivery target, actual
  implementation, shared integration contracts and proposed platform selection.
- Required Context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`,
  `docs/DEVELOPMENT.md`, `agent-tasks/README.md`, public workflow/domain/
  architecture/AI/data/testing guidance and retained public task decisions.
- Source of Truth: current public authority hierarchy and executable source.
  No protected documents, operational sources or private archives are inputs.
- Dependencies: #54 / PR #55, reviewed commit `d351ff3`; the requester approved
  dependent issue branches while all PRs continue to target `dev`, without merge.
- Approval: requester approved the implementation plan and reaffirmed both CLIA
  and non-CLIA workflows as the required target. This approves scope
  reconciliation, not unspecified laboratory rules or Foundry adoption.
- Allowed Files:
  - `agent-tasks/56-buildathon-integration-contracts.md`
  - `agent-tasks/README.md`
  - `docs/PRODUCT.md`
  - `docs/WORKFLOW.md`
  - `docs/DOMAIN_MODEL.md`
  - `docs/ARCHITECTURE.md`
  - `docs/OPERATIONS.md`
  - `docs/AI_BOUNDARY.md`
  - `docs/TESTING.md`
  - `docs/README.md`
  - `docs/DATA_INVENTORY.md`
  - `docs/architecture-decisions/0003-buildathon-transition.md`
- Review-Only Files: all others; source authority/manifest, authorization rules
  and historical decisions are not rewritten. Protected roots remain excluded
  from traversal, reads, hashing, generation or other mutation.
- Prohibited: runtime/schema/dependency/policy changes; invented CLIA rules;
  marking proposed architecture accepted; source ingestion/publication;
  real-data generation; external calls, resource changes, deployment or merge.
- Expected Outputs: one canonical stack/status matrix, source-linked workflow
  difference/gap matrix, app-owned synthetic interface requirements and an
  explicitly proposed architecture ADR.
- Acceptance: both workflows remain required, not merely labels; present
  non-CLIA-only behavior is reported accurately; exact unresolved governed
  differences and owners are explicit; model/port/data/UI integration gaps are
  distinguished from policy questions; no live or implemented claims invented.
- Validation: Python 3.12 selected-task preflight; permitted relative links;
  protected-path-aware repository/staged checks; whitespace; existing CI.
- Independent Review: public documentation review for authority shifts,
  contradictory current-state claims and missing control gates.
- Human Gates: laboratory/source owners resolve exact CLIA governed rules;
  architecture owner accepts any Foundry selection; platform/privacy/source
  approvals and local UI acceptance remain separate. Drafting is not acceptance.
- Lease: Orchestrator exclusively owns these paths from contract creation
  through PR handoff, revocation or abandonment. No parallel writers.
- Stop: conflicting authority, missing policy evidence, unsafe source access,
  overlapping lease or a necessary out-of-scope edit.
- Handoff: exact changed paths, validation, proposed/implemented distinctions,
  independent review and unresolved decisions. No merge.

This initial commit contains only the contract. Dependency commits from #54
remain visible in this dev-target PR until the prerequisite is integrated.

## Handoff

- Draft PR #57 targets `dev`; dependency PR #55 is not merged.
- Updated the twelve Allowed Files only, including proposed ADR 0003.
  Both executable workflows are the current target. Existing non-CLIA/mock/
  read-only limits, missing SQL service adapters, dataset/UI compatibility and
  exact CLIA rule-evidence gaps remain explicit.
- The canonical stack matrix distinguishes baseline, proposed selection,
  implementation and required evidence. Foundry adoption remains unaccepted.
- Python 3.12 task preflight passed; the affected inventory-link test passed;
  89 local links/anchors across the twelve public documents passed. Safe
  repository verification and whitespace checks passed. Staged checks and
  final-head CI precede handoff completion.
- Independent documentation review found no material defects and confirmed
  scope/authority distinctions. It did not run live integrations or provide
  human approval.
- No application, schema, dependency, source-access or controlled policy changes.
  Remaining rule/platform/source decisions have named owner roles in the
  workflow matrix and ADR; they cannot be filled with invented defaults.
