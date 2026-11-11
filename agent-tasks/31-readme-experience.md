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

- Publication: issue #31, branch `31-readme-experience`, draft PR #32;
  verified base `dev`. Bootstrap commit contains only this contract, as
  approved by the requester.
- Exact changed files: `README.md` and this contract. No runtime, policy,
  schema, dependency, data or repository-layout changes.
- Editorial comparison: replaced the implementation-first opening with an
  audience/purpose introduction, added a short section navigation, made the
  six-screen assessment journey the primary action, separated available
  behavior from its boundary, and grouped deeper links by reader intent.
  Removed the secondary startup path from the primary demo instructions,
  placing it in developer navigation instead. Detailed architecture and
  optional presentation guidance remain linked rather than repeated.
- Evidence: scope from `docs/PRODUCT.md`; installation and commands from
  `docs/DEVELOPMENT.md` and `docs/BUILDATHON.md`; current pilot from
  `app/__init__.py`, `app/config.py`, `app/web/routes.py`, `app/data/demo.py`,
  `app/ai/mock.py` and the pilot tests. Fixture versus standalone examples,
  source-handling controls and reuse status match their canonical guides.
- Validation: all 38 README local links, including heading anchors, passed;
  README is ASCII; working-tree repository verification passed for 142
  tracked files; whitespace checks passed.
- Preflight selected this contract and correctly returned 1 for the local
  Python 3.14.2 runtime. It is not supported Python 3.12 validation.
  Documentation-only changes add no local application regression run.
- Independent read-only review found no significant issues and confirmed
  local links/anchors and whitespace checks. It did not inspect protected
  inputs, run the full tests or grant human/operational approval.
- Publication validation: staged-content verification is required before
  the README commit; current-head Python 3.12 CI evidence is recorded in
  PR #32 after publication rather than inferred from older runs.
- No unresolved README design or scope decisions. Existing specialist,
  source-owner and operational gates remain unchanged.
- Next owner: requester reviews draft PR #32; no merge or promotion to `main`.
