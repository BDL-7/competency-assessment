# Repository Organization and Developer Onboarding

## Contract

- Task: #28; owner: Orchestrator integration.
- Goal: implement the requester-approved repository cleanup without changing
  application behavior, schema, laboratory policy or local source materials.
- Business reason: give developers a clear run/test path, accurate product
  framing, understandable fictional examples and discoverable documentary history.
- Required context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`,
  `docs/PRODUCT.md`, `agent-tasks/README.md`, `docs/DEVELOPMENT.md`,
  `data/DATA_CLASSIFICATION.md` and the approved session cleanup proposal.
- Source of truth: public canonical guidance and issue #13 for both-context
  planning; existing implementation/tests for current capability claims.
- Dependencies: current `dev`, Git/GitHub, existing pinned test environment and
  Python 3.12 CI. No package or platform changes.
- Approved assumptions: the requester approved implementation of the session
  proposal on 2026-11-11. Optional guide consolidations and mechanical reference
  updates are included; knowledge-format source selection/regeneration is not.
  The requester also approved a contract-only bootstrap commit before draft-PR
  creation because GitHub requires a differing commit.
- Allowed files (exclusive serialized Orchestrator integration lease):
  - `agent-tasks/28-repository-cleanup.md`
  - `README.md`, `CONTRIBUTING.md`, `.gitignore`
  - `agent-tasks/README.md`
  - `agent-tasks/20-synthetic-buildathon-data.md`
  - `agent-tasks/22-local-cat-kb-bundle.md`
  - `agent-tasks/25-agent-workflow-safeguards.md`
  - `agent-tasks/buildathon-ignore-policy.md`
  - `agent-tasks/buildathon-onboarding.md`
  - `agent-tasks/buildathon-presentation.md`
  - `agent-tasks/buildathon-responsive-text.md`
  - `agent-tasks/s0-03-application-foundation.md`
  - `data/README.md`
  - `data/authoritative/README.md`, `data/migration/README.md`,
    `data/reference/README.md`
  - `data/synthetic/buildathon/README.md`
  - `data/synthetic/buildathon/generate_users.py`
  - `data/synthetic/buildathon/edge-cases.json`
  - `data/examples/README.md`, `data/examples/generate_users.py`,
    `data/examples/edge-cases.json`
  - `docs/README.md`, `docs/PRODUCT.md`, `docs/DEVELOPMENT.md`,
    `docs/BUILDATHON.md`, `docs/SOURCE_MANIFEST.md`
  - `docs/controlled-sources/README.md`, `docs/project/README.md`
  - `docs/project/ca-architecture-one-pager.md`,
    `docs/architecture-one-pager.md`
  - `docs/CAT_KB.md`, `docs/CAT_KB.html` (mechanical source-path references only)
  - `docs/archive/README.md`
  - `docs/archive/tasks/20-synthetic-buildathon-data.md`
  - `docs/archive/tasks/22-local-cat-kb-bundle.md`
  - `docs/archive/tasks/25-agent-workflow-safeguards.md`
  - `docs/archive/tasks/buildathon-ignore-policy.md`
  - `docs/archive/tasks/buildathon-onboarding.md`
  - `docs/archive/tasks/buildathon-presentation.md`
  - `docs/archive/tasks/buildathon-responsive-text.md`
  - `docs/archive/tasks/s0-03-application-foundation.md`
  - `docs/archive/maintenance/reorganize_repo.ps1.txt`
  - `docs/archive/maintenance/archive_superseded_materials.ps1.txt`
  - `scripts/documents/README.md`
  - `scripts/maintenance/reorganize_repo.ps1`
  - `scripts/maintenance/archive_superseded_materials.ps1`
  - `artifacts/README.md`, `artifacts/archive/README.md`
  - `artifacts/archive/2026-08-13-leadership-concept/README.md`
  - `artifacts/archive/2026-08-14-html-release/README.md`
  - `tests/unit/test_buildathon_synthetic_scenarios.py`
- Review-only: every other path, controlled/untracked inputs, ignored local
  workbooks/builders/rosters/releases, runtime state and unrelated work.
- Prohibited: source-content inspection/publication, local-input moves or
  deletion, schema/runtime/policy changes, new dependencies, executing old
  maintenance scripts, knowledge-format regeneration, live AI, deployment,
  merge or weakening repository protections.
- Expected outputs: developer-first README, consolidated guides, relocated
  fictional examples, historical origin/replacement map and updated references.
- Acceptance criteria:
  - Both CLIA and non-CLIA planning is visible without implying CLIA execution,
    compliance, production readiness or changed form/signature rules.
  - The seven-identity app demo stays separate from the 70-person local roster;
    generator fields, population, role mix and five scenarios are unchanged.
  - Active baseline contracts and unresolved gates remain discoverable.
    Archived approval prose and literal historical paths are preserved.
  - Every path move has its live references/tests updated. Old/new local CSV
    and protected paths stay ignored; tracked sources stay eligible.
  - Optional source/tooling introductions retain all distinct handling guidance;
    knowledge formats remain advisory with no maintained source selected.
- Validation: manual preflight; targeted scenario/preflight/verifier pytest;
  before/after path and content reconciliation; tracked-text links/anchors;
  precise ignore checks; working-tree/staged verifier; `git diff --check`;
  existing full Python 3.12 CI and independent review.
- Security/privacy: synthetic/public tracked material only; stage exact leased
  paths, never `git add -A`; do not expose local inputs in logs or GitHub.
- Definition of done: acceptance met, exact files/validation/runtime limitations
  reported, independent review complete, draft PR targets `dev`; human merge
  review and existing specialist operational gates remain separate.
- Handoff: changed files, issue/PR, checks, unresolved decisions and next owner.
- Stop conditions: authority conflict, overlapping lease, sensitive exposure,
  unapproved behavior/schema/policy change or weakened publication control.
- Human approval: implementation and publication requested on 2026-11-11;
  no merge, deployment, source publication or operational approval.
- Lease expiry: when #28 is merged, closed or abandoned.

## Validation and handoff

Implementation evidence is recorded here after validation. Historical results
in archived contracts do not establish current validation or specialist approval.
