# Local CAT-KB Bundle

## Contract

- Task: #22; owner: Orchestrator.
- Goal: make the generated CAT-KB bundle easy to find in a developer's local
  checkout without publishing or tracking the ZIP.
- Business reason: allow local buildathon access to the partial knowledge
  bundle while retaining repository content controls.
- Required context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`,
  `docs/PRODUCT.md`, and the issue #22 description.
- Source of truth: the approved source manifest and existing archive contents.
- Dependencies: an already generated `CAT-KB.zip` bundle.
- Approved assumptions: the archive is stored at repository-root path
  `CAT-KB.zip` locally; Git ignores only this root-level filename. The ZIP is
  not part of the PR, Git history, or public releases.
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
  - `git check-ignore` confirms it is ignored.
  - The ignore pattern is anchored to the repository root.
  - Git index and PR diff contain no ZIP archive.
- Validation commands:
  - `git check-ignore -v -- CAT-KB.zip`
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
