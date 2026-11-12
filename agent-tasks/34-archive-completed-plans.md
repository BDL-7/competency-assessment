# Archive Completed Plans and Delivery Records

## Contract

- Task: #34; owner: Orchestrator integration.
- Goal: separate completed planning/delivery history from the current app's
  working guidance without losing approved baselines or unresolved gates.
- Business reason: remove obsolete phase sequencing and completed task records
  from active onboarding; proactively identify historical documents.
- Required context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`,
  `docs/DEVELOPMENT.md`, `agent-tasks/README.md`, candidate documents and their
  tracked references.
- Authority: current public canonical guides govern current scope; historical
  decisions retain their original authority/limits when archived. Closed issues
  establish completed execution, not specialist or operational approval.
- Dependencies: current `dev`, existing Git/GitHub and repository checks.
- Approval: requester authorized archival on 2026-11-12, explicitly chose
  retention until a later deletion request and approved a contract-only
  bootstrap commit before draft-PR creation. No merge is authorized.
- Exclusive writable paths:
  - This contract.
  - `agent-tasks/README.md`, `README.md`, `docs/README.md`,
    `docs/DEVELOPMENT.md`, `docs/BUILDATHON.md`, `docs/archive/README.md`.
  - Sources under `agent-tasks/` and matching destinations under
    `docs/archive/tasks/`: `first-coding-sprint.md`,
    `s0-01-synthetic-scenario.md`, `s0-02-interface-schema-contract.md`,
    `s0-04a-workflow-vertical-slice.md`, `s0-07-local-pilot-ui.md`,
    `28-repository-cleanup.md`, `31-readme-experience.md`.
  - `presentations/html-workshop/FORMAT_AUDIT.md` and
    `docs/archive/presentations/format-audit.md`.
- Review-only: every other path, controlled sources, private/untracked inputs,
  ignored files, environments, databases and generated outputs.
- Prohibited: private-file inspection/moves, deletion of historical contents,
  automatic expiration/deletion, code/schema/test/policy changes, new packages,
  source release, deployment, merge or weakened approvals.
- Expected outputs: historical records in the existing archive, corrected
  active navigation, origin/replacement map and preserved decision/gate links.
- Acceptance:
  - No completed phase/task contract is presented as current work.
  - Current setup, current pilot limits and outstanding reviews remain easy
    to find. Archiving never marks pending review complete.
  - Historical contents remain unchanged except mechanical relative links
    required by their new locations; literal past leases/commands remain history.
  - Current role/rule/source decisions are not rewritten or expanded.
  - Archive retention explicitly requires a later requester decision before
    deletion; no time-based deletion is configured or promised.
  - Live references work; historical task filenames remain in Git history
    and the archive origin map. No runtime tooling depends on moved files.
- Validation: manual task preflight; before/after content reconciliation;
  tracked Markdown links/anchors; public repository and staged verification;
  whitespace checks; existing Python 3.12 CI.
- Independent review: bounded read-only review of the documentation diff for
  lost requirements, authority shifts, broken links and missing approval gates.
  AI review is not human approval.
- Security/privacy: public tracked material only; stage exact leased paths,
  never broad staging. Private inputs remain untouched.
- Done/handoff: exact files and disposition reasons, validation, limitations,
  independent review and draft PR to `dev`; requester reviews before merge.
- Stop: unclear authority, overlapping lease, sensitive exposure or a necessary
  edit outside the lease. Lease expires when #34 merges, closes or is abandoned.

## Disposition findings

- Seven task/planning records: archive. Issues #5, #7, #11, #13, #15,
  #28 and #31 are closed; documents contain original task leases, sprint
  sequencing or delivery evidence. Their unique acceptance/decision/review
  records remain retained and indexed, not superseded by the move.
- Presentation format audit: archive as historical extraction rationale.
  It records the source implementation's extraction choices, not the current
  content/runtime contract. Current README, content schema and reusable handoff
  remain with the active presentation framework.
- Canonical product, architecture, workflow, authorization, AI/data controls,
  terminology, operations, testing, setup and ADRs: retain. These serve current
  requirements or decision traceability; phase terminology alone is not proof
  of obsolescence.
- Data guides, runtime/configuration/dependencies, tests/migrations, active
  presentation framework and existing archive/artifact provenance: retain.
- Advisory knowledge-format comparison variants: retain pending the separate
  maintained-source/release decision; similar formats are not proof of duplication.
- Coverage: tracked documentation/navigation and candidate dependencies, using
  current reads and the earlier repository audit; not a new full code/binary
  audit or a private-filesystem cleanup.

## Validation and handoff

Pending implementation, independent review and current-head CI.
