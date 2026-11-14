# Task #54: Safe buildathon implementation preflight

- Owner Agent: Orchestrator / Engineering Lead, current implementation session.
- Goal: establish safe publication checks and supported-runtime validation for
  the approved buildathon transition.
- Business Reason: application work must not inspect protected local sources or
  mistake historical task leases and unsupported-runtime tests for approval.
- Required Context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`,
  `docs/DEVELOPMENT.md`, `agent-tasks/README.md`, current verifier and tests.
- Source-of-Truth Files: the public source-authority/product/development guides
  and this task's requester-approved privacy boundary.
- Dependencies: issue #54, branch `54-buildathon-safe-preflight` from current
  `origin/dev`, Python 3.12 and existing pinned dependencies.
- Approved Assumptions: requester approved the implementation plan on
  2026-11-14, including this foundation slice, the surgical root-data ignore
  repair, preservation of existing environments, and a contract-only bootstrap
  commit/push before opening a draft PR targeting `dev`. The requester confirmed
  that no other writer owns the malformed ignore edit.
- Allowed Files:
  - `agent-tasks/54-buildathon-safe-preflight.md`
  - `agent-tasks/README.md`
  - `.gitignore`
  - `scripts/verify_repository.py`
  - `tests/unit/test_repository_verification.py`
- Review-Only Files: all other repository files. Protected sources, root
  `data/`, private archives/builders, credentials and unknown databases are
  excluded from inspection, not inputs to this task.
- Prohibited Actions: root-data traversal/read/hash/write; controlled-source or
  operational-data use; broad untracked/ignored inventories; following links
  into protected locations; blanket staging; unrelated edits; deletion/reset;
  application/schema/policy changes; uploads, external AI calls, deployment or
  merge. Never weaken publication checks to hide prohibited indexed material.
- Expected Outputs: repaired literal root-data ignore rule, fail-closed
  pre-content path checks, safe diagnostics, synthetic regression tests,
  accurate task navigation and Python 3.12 validation evidence.
- Interfaces: retain the verifier's existing command and `--staged` interface.
  Staged validation checks indexed bytes, not dirty working-tree replacements.
  Protected entries are rejected without reading content or revealing their
  descendant names. Application source `app/data/` remains permitted.
- Acceptance Criteria:
  - Root data is ignored using literal nonexistent probe paths, without
    enumerating any real descendants.
  - Protected indexed material fails before content reads; diagnostics identify
    the public boundary rather than private descendant paths.
  - Working-tree reads do not follow symbolic links or junctions.
  - Indexed symlinks, conflicts and unsupported entries fail explicitly.
  - Existing clean-public, staged-byte, required-file and syntax checks remain.
  - Current task navigation does not present closed #34/#37/#40/#45/#48/#51 as
    active leases; their original approval evidence is preserved.
- Validation Commands: selected-task Python 3.12 manual preflight; focused
  `tests/unit/test_repository_verification.py`; dependency integrity check;
  safe working-tree and complete-index verifier; whitespace checks; existing
  Python 3.12 CI. Broader tests only where required for integration.
- Security and Privacy Considerations: synthetic miniature repositories only
  for negative tests. Git metadata checks may determine that a forbidden prefix
  is tracked, but must not enumerate its descendants or open its bytes.
  Public retained archive manifests remain checkable; private builders and
  generated/archive binaries are not content-inspection targets.
- Independent Review: bounded code review of these exact changed paths for
  path-policy bypasses, lost staged coverage, unsafe traversal and regressions.
  Independent AI review is not human acceptance.
- Definition of Done: outputs and focused tests pass on Python 3.12; exact
  staged content and dev-target PR verified; independent review and outstanding
  human gates recorded. The full buildathon plan is not completed by this slice.
- Handoff Format: exact paths, validation/runtime/results, untouched boundaries,
  independent review and human gates, issue and draft PR.
- Stop Conditions: ambiguous authority, overlapping lease, unsafe publication,
  protected-content access, unsupported runtime or required out-of-lease edit.
- Human Approval Gate: requester reviews before merge. CLIA-specific rules,
  Foundry selection/processing, platform integrations, external governance
  transfer and local cleanup remain separately gated in later slices.
- Path Lease Owner and Expiry: Orchestrator exclusively holds the five Allowed
  Files from this contract's creation until PR handoff, revocation or abandonment;
  renew explicitly for later edits. No parallel writers are authorized.

## Bootstrap validation

The existing local environment uses Python 3.14.2 and the no-contract preflight
correctly failed. Python 3.12.10 was installed for the current user, and this
task's manual preflight passed. An isolated session environment restored the
existing development lock without replacing the repository environment or
changing dependency versions. This initial commit contains only this public
task contract; no implementation, protected data or other worktree edits are
staged. Full repository verification follows the safe-checker implementation;
bootstrap review is restricted to the exact contract diff.
