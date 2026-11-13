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
- The local `instance/test-databases/` inventory had 57 UUID-named databases:
  two match names used by current tracked tests and 55 use a `workflow-` prefix
  not found in current tracked code/history. The requester explicitly approved
  archiving all 57 locally; no database contents were opened.
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
4. Archive only the 57 files in the exact local test-database directory, after
   checking the candidate inventory and confirming no active process uses them.
   Record source paths and hashes in the local receipt and verify the archived
   bytes. The requester authorized the 55 `workflow-` UUID files whose original
   generator is no longer in tracked code. Never expose names/hashes in GitHub.
5. Preserve the two direct `instance/` databases and the untracked
   `docs/buildathon-resources/` unchanged. No database rows are opened.
6. No pre-existing/user files are deleted. Test-created temporary databases are
   removed during fixture teardown. The local archive is ignored by Git and
   retained until the requester explicitly asks for a future deletion review.
7. Supported Python 3.12 full tests, clean temporary schema migration,
   repository/staged verification, documentation links and a loopback demo
   smoke test pass.
8. Independent review checks correctness, data preservation, test cleanup and
   no unintended structural/runtime changes. Human review remains separate.

## Validation and handoff

- Python 3.12.14 preflight passed. The supported interpreter is `tmp/s0-03-py312`.
- Focused persistence/migration tests passed (6); full pytest passed twice (89
  tests each). An intentional failing-test probe confirmed the engine is
  disposed and its exact pytest temporary directory is removed.
- `instance/test-databases/` remained empty during both full-suite runs. The two
  direct `instance/` database hashes were unchanged.
- `pip check` found no broken requirements. An empty synthetic SQLite database
  upgraded twice with 20 application tables and no application rows.
- Repository verification passed for 145 tracked files; 40 README local links
  and heading anchors validated; `git diff --check` passed.
- The guarded local demo smoke test returned HTTP 200 for `/health` and `/`,
  including the synthetic assessment. It bound only to `127.0.0.1`; its
  uniquely named database, manifest and logs were removed after the server
  stopped.
- Restart Manager reported no active process using the 57 archive candidates.
  The local archive contains all 57 with a hash receipt; an independent
  verification found zero mismatches. Database contents were not opened.
- The local archive remains excluded through `.git/info/exclude`. Preserve the
  two direct `instance/` databases and untracked `docs/buildathon-resources/`.
- The two independent reviewer agents could not run (one had no repository
  inspection tools; the alternate reviewer model was unavailable). Manual
  review found no actionable issue, but independent review and human approval
  remain open gates; do not merge.
- Tracked changes are limited to this contract, `README.md`,
  `docs/DEVELOPMENT.md`, `tests/integration/test_persistence.py`, and
  `tests/migration/test_schema_migration.py`. Do not stage the local archive or
  unrelated untracked work.
- Lease expires when #40 merges, closes or is abandoned.
