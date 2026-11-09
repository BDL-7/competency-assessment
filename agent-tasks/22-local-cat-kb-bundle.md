# Local CAT-KB Bundle

## Contract

- Task: #22; owner: Orchestrator.
- Goal: keep generated local-only buildathon assets available in a developer's
  checkout without publishing or tracking them.
- Business reason: allow local access to the partial CAT-KB bundle and
  synthetic user roster while retaining repository content controls.
- Required context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`,
  `docs/PRODUCT.md`, and the issue #22 description.
- Source of truth: the approved source manifest and existing archive contents.
- Dependencies: an already generated `CAT-KB.zip` bundle.
- Approved assumptions: the archive is stored at repository-root path
  `CAT-KB.zip`, and the generated roster at
  `data/synthetic/buildathon/users.csv`; Git ignores only these exact paths.
  Neither file is part of the PR, Git history, or public releases.
- Allowed files:
  - `.gitignore`
  - `agent-tasks/22-local-cat-kb-bundle.md`
- Review-only files: controlled source documents, governed and operational
  workbooks, and the ZIP contents as an artifact (do not expand or add sources
  under this task).
- Prohibited actions: tracking, committing, or pushing the ZIP; broad `*.zip`
  ignore rules; adding controlled or operational data; treating the bundle as
  approved for live assistant ingestion.
- Expected outputs: precise root-specific ignore rule, local copy of the
  existing ZIP in the repository root, and PR targeting `dev`.
- Acceptance criteria:
  - `CAT-KB.zip` exists at the repository root in the local checkout.
  - The generated synthetic roster stays at its documented local path.
  - `git check-ignore` confirms both local-only files are ignored.
  - Ignore patterns are exact and do not hide other ZIP or CSV files.
  - Git index and PR diff contain no ZIP archive.
- Validation commands:
  - `git check-ignore -v -- CAT-KB.zip`
  - `git check-ignore -v -- data/synthetic/buildathon/users.csv`
  - `git ls-files --error-unmatch CAT-KB.zip` must fail because it is not tracked.
  - `git diff --check`
- Security/privacy: keep only the previously generated partial bundle; the
  bundle's own note lists withheld controlled sources and states it is not an
  approved chatbot corpus.
- Definition of done: checks pass, the rule is committed and pushed on the
  issue branch, and the PR base is verified as `dev`.
- Handoff: report exact changed files and confirm the local ignored ZIP is not
  included in the PR.
- Stop conditions: archive missing, archive differs from the previously
  generated artifact, or any controlled/operational file is proposed for
  inclusion.
- Human approval gate: the ZIP remains unapproved for live chatbot use; source
  owners must approve source versions and permitted audience separately.
- Path lease owner and expiry: Orchestrator; expires when issue #22 is merged
  or closed.
