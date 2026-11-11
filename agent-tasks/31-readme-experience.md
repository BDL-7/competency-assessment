# README Navigation and First-Run Experience

## Contract

- Task: #31; owner: Orchestrator integration.
- Goal: make the main README a clear, engaging entry point without changing
  product scope or application behavior.
- Business reason: help developers, evaluators and contributors understand
  what exists, try the local pilot and find the right deeper guidance.
- Required context: `AGENTS.md`, `.github/copilot-instructions.md`,
  `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`, `agent-tasks/README.md`,
  `docs/DEVELOPMENT.md`, `docs/BUILDATHON.md`, `data/README.md`,
  `CONTRIBUTING.md` and the current README.
- Source of truth: public canonical guidance for approved scope and controls;
  current application code and tests for implemented behavior.
- Dependencies: current `dev`, Git/GitHub, existing validation tools and CI.
- Approved assumptions: the requester authorized implementation/publication
  and a contract-only bootstrap commit before draft-PR creation. GitHub needs
  a differing commit; the README commit follows verification of the PR's
  `dev` target. No merge is authorized.
- Allowed files (exclusive serialized Orchestrator lease):
  - `README.md`
  - `agent-tasks/31-readme-experience.md`
- Review-only: every other path, including controlled/untracked inputs,
  ignored local resources and runtime state. No other active task may edit
  either leased path.
- Prohibited: runtime/schema/policy changes, repository reorganization,
  controlled-source access/publication, operational data, new dependencies,
  deployment, merge or promotion to `main`.
- Expected outputs: revised README, evidence recorded here and a draft PR
  targeting `dev` linked to #31.
- Acceptance criteria:
  - Opening identifies the tool, intended audience and prototype maturity.
  - Both CLIA and non-CLIA planning are visible; executable CLIA workflows,
    compliance, validation and production readiness are not implied.
  - One primary local-start route uses the maintained Python 3.12 installation
    and dedicated synthetic setup instructions, not duplicated command blocks.
  - Current read-only UI, mock guides, service-only behavior and future plans
    remain distinct; read-only business records do not imply zero audit writes.
  - Navigation serves evaluators, developers and contributors; layout and
    fictional-example boundaries use plain language and avoid clutter.
  - Links/anchors and capability claims have evidence; legal, authority,
    publication and operational gates remain discoverable.
- Validation: manual task preflight; README link/anchor and factual checks;
  working-tree/staged repository verification; `git diff --check`; existing
  CI. No application changes require additional local regression testing.
- Independent review: a read-only reviewer checks the final two-file diff
  for factual regressions, missing safeguards and unclear onboarding before
  handoff. AI review does not satisfy human approval.
- Security/privacy: use public tracked content only; stage these two paths
  explicitly, never broad staging. Leave local controlled inputs untouched.
- Definition of done: acceptance met, validation and exact files reported,
  independent review complete, draft PR targets `dev`; requester reviews next.
- Handoff: issue/PR, exact files, validation limitations, unresolved decisions.
- Stop conditions: authority conflict, overlapping lease, sensitive exposure,
  unapproved scope expansion or weakened controls.
- Human approval: README implementation/publication and bootstrap exception
  approved on 2026-11-11; merging and operational use remain unapproved.
- Lease expiry: #31 merged, closed or abandoned.

## Validation and handoff

Pending README implementation, independent review and CI.
