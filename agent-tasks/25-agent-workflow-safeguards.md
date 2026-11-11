# Lightweight Agent Workflow Safeguards

## Contract

- Task: #25; owner: Orchestrator.
- Goal: make existing agent guidance and public-repository checks easier to
  follow without creating another issue-first workflow.
- Business reason: reduce accidental out-of-scope work, unsupported-version
  validation claims, and differences between staged and working-tree content.
- Required context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`,
  `docs/PRODUCT.md`, `agent-tasks/README.md`, `docs/DEVELOPMENT.md`,
  `CONTRIBUTING.md`, and `scripts/verify_repository.py`.
- Source of truth: the existing project governance, data-classification
  guidance, development instructions, and repository verification rules.
- Dependencies: Git, Python, an approved task contract, and GitHub CI.
- Approved assumptions: preflight is explicitly invoked, not a lifecycle hook;
  task selection and approvals remain human decisions. Repository verification
  is a limited safeguard and cannot prove an absence of sensitive material.
- Allowed files:
  - `agent-tasks/25-agent-workflow-safeguards.md`
  - `.github/copilot-instructions.md`
  - `scripts/agent_preflight.py`
  - `scripts/verify_repository.py`
  - `tests/unit/test_agent_preflight.py`
  - `tests/unit/test_repository_verification.py`
  - `docs/DEVELOPMENT.md`
  - `CONTRIBUTING.md`
- Review-only files: controlled sources, operational workbooks, local runtime
  state, existing application behavior, and unrelated worktree changes.
- Prohibited actions: creating a new issue-first workflow, automatic hooks,
  unattended publication or deployment, expanding laboratory policy, changing
  the data classification rules, or staging unrelated files.
- Expected outputs: concise Copilot instructions, manual preflight, staged
  verification, synthetic tests, and usage guidance.
- Acceptance criteria:
  - Instructions link to existing canonical governance and respect human gates.
  - Preflight reports the actual Python version and task selection without
    changing the environment or inferring authorization.
  - Staged verification checks the index content, including partially staged
    changes, without leaking content and while preserving existing rules.
  - Existing verifier behavior and CI remain intact; failures are explicit.
  - Tests use isolated synthetic repositories and leave local files untouched.
- Validation commands:
  - Focused pytest for both new unit-test modules using approved Python 3.12.
  - Existing repository verifier, staged verification, and `git diff --check`.
  - GitHub CI on Python 3.12 if local approved runtime is unavailable.
- Security/privacy: never inspect or publish controlled inputs or identifiable
  data; diagnostics identify paths and problems, not file contents.
- Definition of done: acceptance criteria, validation evidence, and required
  independent review are reported; draft PR targets `dev`.
- Handoff: exact changed files, validation results, runtime limitations, and
  unresolved review gates.
- Stop conditions: unclear data classification, incompatible task ownership,
  need to weaken an existing control, or sensitive-content exposure.
- Human approval gate: repository changes require normal human PR review;
  no policy, deployment, or operational use is authorized.
- Path lease owner and expiry: Orchestrator; expires when issue #25 is closed.

## Validation and review

- The eight focused synthetic tests passed locally on Python 3.14.2. This
  unsupported runtime does not replace the required Python 3.12 CI run.
- The manual preflight correctly reported the local Python 3.14.2 mismatch
  and returned a nonzero status without modifying the environment.
- Both the existing working-tree verifier and the new index verifier passed;
  staged whitespace checks passed.
- Independent review reported no significant findings. It did not establish
  Python 3.12 validation; record CI results in the pull-request handoff.
- Human review and merge remain outstanding. No deployment is authorized.
