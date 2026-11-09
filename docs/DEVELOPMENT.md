# Development Workflow

## Current status

The Flask foundation, synthetic workflow services, SQLAlchemy mappings and
Alembic migration exist. An opt-in read-only local pilot uses the existing
one-record fixture and deterministic mock guides. Full workflow web actions,
production integrations and live AI remain deferred.

The earlier Phase 0 documents describe planning and governance. This guide
does not authorize additional application behavior, policy, resources or
deployment. Use the approved [task contracts](../agent-tasks/README.md).

## Local prerequisites and installation

Run these PowerShell commands from the repository root. Python **3.12** is the
supported runtime used by CI; a different locally installed Python is not a
substitute for supported-version validation.

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.venv\Scripts\python.exe --version
.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.venv\Scripts\python.exe -m pip check
```

Create `.venv` only if it does not already exist. Check an existing environment's
version before using it; do not overwrite or delete another task's environment.
If needed, create a new environment in the ignored `venv` directory and use
`venv\Scripts\python.exe` consistently in place of the paths below. If
`py -3.12` is unavailable, obtain an approved Python 3.12 installation or use an
existing approved 3.12 executable; do not silently select another version.

The `.in` files record direct dependencies; the `.lock` files pin the existing
runtime/test environments. No Azure SDK or production database driver is needed
for this local demonstration. Do not add or upgrade dependencies casually.

## Configuration and foundation startup

[`.env.example`](../.env.example) documents supported variables but **is not
loaded automatically**. Export local values in each new PowerShell session:

```powershell
$env:APP_ENV = "development"
$env:APP_SECRET_KEY = [guid]::NewGuid().ToString()
$env:APP_MOCK_AUTH_ENABLED = "false"
$env:APP_PILOT_DEMO_ENABLED = "false"
.venv\Scripts\python.exe -m flask --app wsgi run --host 127.0.0.1 --no-reload --no-debugger
```

Open `http://127.0.0.1:5000/`; `/health` returns only `{"status":"healthy"}`.
Stop with Ctrl+C. Keep local demonstrations on loopback, not a public interface.
Without opt-in pilot mode these are foundation routes, not workflow pages.
Production rejects mock authentication and pilot mode and requires an explicit
session secret; selecting a production profile is not deployment authorization.

For explicit demo setup, personas, six-page walkthrough and failure recovery,
follow [BUILDATHON.md](BUILDATHON.md).

## Tests and repository checks

Run from the root in a new shell without pilot settings or a `DATABASE_URL`
migration override:

```powershell
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe scripts\verify_repository.py
git diff --check
```

CI uses Python 3.12, installs `requirements-dev.lock`, upgrades an empty
synthetic SQLite database, runs the full pytest suite and verifies public
repository contents. Its separate verification job builds the public portable
presentation. Tests cover both in-memory service ports and actual SQL
persistence/pilot reads; service end-to-end tests are not full workflow UI tests.

For a focused UI change, select `tests\web\test_pilot.py`; for a presentation
change, select `tests\test_presentation_example.py`. Keep the existing full CI
suite. See [TESTING.md](TESTING.md) for control assertions and specialist gates.

### Optional isolated migration check

Alembic reads its `DATABASE_URL` override or `alembic.ini`, not the application's
`APP_DATABASE_URL`. Never point a validation command at an unknown/user database.
Use a new dedicated synthetic file:

```powershell
$env:DATABASE_URL = "sqlite:///instance/schema-check-$([guid]::NewGuid().ToString('N')).db"
.venv\Scripts\python.exe -m alembic upgrade head
.venv\Scripts\python.exe -m alembic upgrade head
Remove-Item Env:DATABASE_URL
```

Both upgrades should succeed without seeding operational data. Dispose of only
the known validation file after use and after its connections close. Schema
downgrade is explicitly unavailable; failure recovery uses a new synthetic target,
not a reset or downgrade. Unset `DATABASE_URL` before pilot `init-demo` so it
cannot redirect setup.

## Existing layout and future boundaries

```text
app/
migrations/
tests/
  unit/
  integration/
  authorization/
  migration/
  end_to_end/
  web/
agent-tasks/
docs/architecture-decisions/
```

Keep the approved module boundaries and current paths. The live assistant and
its `tests/ai_evals/` remain future authorized work, not a missing prerequisite
for the deterministic mock UI. Adding a tool or platform requires an approved
task and, when it changes architecture, an ADR.

## Git and task workflow

1. Create or identify the issue.
2. Branch from current `dev` as `<issue>-<short-slug>`.
3. Create a task contract and acquire exclusive path leases.
4. Agree on shared interfaces before parallel work.
5. Make small coherent commits without generated, controlled, or sensitive
   files.
6. Run task validation and `python scripts/verify_repository.py`; stage only the
   exact approved paths, preserving unrelated local work.
7. Push the issue-linked branch and open a draft pull request targeting `dev`
   with the issue-closing reference.
8. Complete independent review and human gates before merge.

`main` and `dev` are protected. Feature branches remain temporary. Agents do
not modify the same file concurrently; cross-owned edits are serialized.

## Data and secret handling

- Use synthetic fixtures for development, demonstrations, and tests.
- Never commit `.env`, credentials, tokens, connection strings, private keys,
  production configuration, operational exports, or raw MIST/HIR workbooks.
- `.env.example` contains names and safe placeholders only.
- Generated and runtime files remain in ignored locations defined by
  `.gitignore` and repository policy.

## Optional document and presentation tooling

The [public HTML example](../presentations/html-workshop/README.md) opens directly
in a modern browser. Its standard-library Python builder needs no extra package.

Only authorized internal document work requires:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
```

Approved internal checkouts may provide
`scripts\documents\build_business_value_need.py` and
`scripts\documents\build_consolidated_documents.py`. They are intentionally
absent from public Git and generate controlled documents; see the
[builder manifest](../scripts/documents/README.md). Word or approved LibreOffice
conversion tooling is needed only for that work, not application setup.

Do not run `scripts\maintenance` utilities during onboarding. They record
historical moves/archive operations and may change protected local materials.
