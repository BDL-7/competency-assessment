# Repository Clarity and Local Test Data

## Contract

- Task: #40; owner: Orchestrator integration.
- Goal: make the app, its local URL and repository folders easier to understand,
  while preventing failed tests from leaving databases in the application
  runtime folder.
- Requester approved the plan on 2026-11-13. Issue #37/#38 has since merged;
  work uses a separate issue branch and PR.
- Required context: `AGENTS.md`, `.github/copilot-instructions.md`,
  `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`, `docs/DEVELOPMENT.md`,
  `docs/BUILDATHON.md`, `agent-tasks/README.md`, current README and test code.
- Source of truth: current public product/development guidance and executable
  application/tests; no private document content is needed.
- Dependencies: latest `dev`, Python 3.12 environment, existing dependencies
  and GitHub CI.
- Exclusive tracked writable paths:
  - This contract.
  - `README.md`
  - `docs/DEVELOPMENT.md`
  - `tests/integration/test_persistence.py`
  - `tests/migration/test_schema_migration.py`
- Local-only writable paths, not to be committed:
  - `.git/info/exclude`: one exact ignore entry for the approved local database
    archive directory.
  - `artifacts/archive/local-test-databases/2026-11-13/`: archive of the exact
    verified test-generated DB files and a local metadata/hash receipt.
- Review-only: every other path, including the untracked
  `docs/buildathon-resources/`, private sources, both root `instance/` DBs,
  generated environments, and all unrelated ignored/untracked work.
- Prohibited: moving `.git`, `.github`, `app`, `tests`, migrations, requirements,
  root tools or private sources into new generic folders; adding `python/` or
  `agents/`; hiding folders; opening DB row content; deleting archived data;
  altering app behavior/schema/lab rules; new dependencies; deployment; merge.
- Issue-first workflow: issue #40, branch `40-repository-clarity`, draft PR #41
  targeting `dev`. Bootstrap commit contains this contract only. Verify PR base
  before implementation changes.

## Findings and design decisions

- `.git` is Git's required repository metadata directory, not a regular source
  folder. `.github` contains GitHub-specific CI and Copilot configuration.
- `.venv`, `__pycache__` and `.pytest-data-temp` are local environment/cache
  output. `agent-tasks/` contains human-readable task contracts. The Flask
  application is the Python package `app/`; `app/ai/mock.py` is deterministic
  mock behavior, not a live agent. Keep these out of new `python/` or
  `agents/` roots.
- `instance/` remains the ignored local runtime-data directory. Two DB files
  directly under it are preserved. Tests currently create per-run SQLite files
  under `instance/test-databases`; old files are archived locally, not deleted.
- The local demo URL is `http://127.0.0.1:5000/`; it is not a deployed URL.
  README will make the URL visible immediately before the single canonical
  synthetic setup walkthrough.
- Root `wsgi.py`, `alembic.ini`, `pyproject.toml`, requirements manifests/locks,
  `SECURITY.md`, `.gitignore`, `.python-version` and GitHub-recognized files
  remain at root because runtime, CI, packaging, security tooling or contributor
  conventions reference them. Explain their purpose rather than moving them.
- All folders remain visible. No VS Code exclusion settings.

## Acceptance criteria

1. README makes the local demo route and exact local URL obvious without
   implying public deployment, CLIA execution, compliance or production status.
2. The developer guide plainly explains the visible tool/environment folders
   and root config/dependency files; no misleading Python/agent directory tree.
3. Both DB test modules use pytest-provided temporary storage and reliably close
   connections; repeated passing and deliberately failing paths leave no DB
   files under `instance/test-databases`.
4. All 57 pre-existing candidates are enumerated privately by metadata, proven
   unused by any process immediately before movement, and match the test DB
   candidate path/naming allowlist. Archive locally with a receipt and verify
   source/destination hashes. Never expose names/hashes in GitHub.
5. Preserve the two direct `instance/` databases and the untracked
   `docs/buildathon-resources/` unchanged. No database rows are opened.
6. No files are deleted. The local archive is ignored by Git and retained until
   the requester explicitly asks for a future deletion review.
7. Supported Python 3.12 full tests, clean temporary schema migration,
   repository/staged verification, documentation links and a loopback demo
   smoke test pass.
8. Independent review checks correctness, data preservation, test cleanup and
   no unintended structural/runtime changes. Human review remains separate.

## Validation and handoff

- Run preflight for this contract using Python 3.12.
- Run targeted migration/persistence tests, then full pytest at least twice.
- Verify no new DB appears in `instance/test-databases`; verify pytest temp
  databases are cleaned after success and failure.
- Run `pip check`, empty synthetic SQLite upgrade, repository verifier,
  staged verifier, README link/anchor checker and `git diff --check`.
- Launch the local synthetic demo using the existing documented guarded setup;
  verify the loopback health/page responds, then stop the server. Do not bind
  publicly or use an unknown DB.
- Verify local DB archive entries against the exact allowlist and hashes; do
  not stage the archive, receipt, untracked resources or private inputs.
- Record exact tracked files, CI, archive count/verification, preserved paths,
  limitations and open gates in this contract and PR.
- Lease expires when #40 merges, closes or is abandoned.
