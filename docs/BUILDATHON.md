# Local Buildathon Walkthrough

## Demonstration boundary

This walkthrough uses the existing read-only Flask pilot, not a new application.
It requires no cloud resources, approved-source upload or model connection.
Use [DEVELOPMENT.md](DEVELOPMENT.md) to install the pinned Python 3.12 environment
first. Run commands from the repository root.

The complete fixture is **one assessment, two issued versions and seven
synthetic identities**, with **zero signatures recorded**. Its reference date is
**2027-02-20** and its due date is **2027-02-15**. Version 1 preserves missing
follow-up; version 2 documents synthetic follow-up and awaits Testing Personnel
signature. Future dates are demonstration values, not events that happened today.

This is not a multi-lab dataset, five-year history/projection, CLIA workflow,
laboratory compliance demonstration or valid electronic-signature system.
See [PRODUCT.md](PRODUCT.md) and the
[pilot contract](../agent-tasks/s0-07-local-pilot-ui.md).

## Initialize a dedicated synthetic demo

In a fresh PowerShell session:

```powershell
$env:APP_ENV = "development"
$env:APP_SECRET_KEY = [guid]::NewGuid().ToString()
$env:APP_PILOT_DEMO_ENABLED = "true"
$env:APP_MOCK_AUTH_ENABLED = "true"
$env:APP_MOCK_USER_ID = "SYN-EMP-001"
$env:APP_MOCK_DISPLAY_NAME = "Testing Person One"
$env:APP_DATABASE_URL = "sqlite:///instance/synthetic-pilot.db"
if (Test-Path Env:DATABASE_URL) { Remove-Item Env:DATABASE_URL }
.venv\Scripts\python.exe -m flask --app wsgi init-demo
.venv\Scripts\python.exe -m flask --app wsgi run --host 127.0.0.1 --no-reload --no-debugger
```

The app does not load `.env.example` automatically. `init-demo` alone creates
and migrates a new dedicated SQLite file, seeds the fixture, and writes an adjacent
synthetic ownership manifest. HTTP requests never create or seed schema.
Repeating setup on an owned complete demo reports that no records changed.

Never use an existing unknown database. Setup rejects unknown, incomplete or
incompatible targets rather than resetting them. Choose a new filename if needed;
preserve the original database and manifest. `DATABASE_URL` is Alembic's separate
override and must be unset before demo initialization.

Open `http://127.0.0.1:5000/`. Stop with Ctrl+C. Keep the server on loopback;
do not enable a public binding or debugger.

## Six-screen walkthrough

| Screen | Local path | What to verify |
| --- | --- | --- |
| Overview | `/` | One scoped assessment; one overdue/pending-signature item; zero finalized records; synthetic reference date visible |
| Work queue | `/work` | Search `Testing`, sort by person/due date, filter visible state; no-match search has clear recovery |
| Assessment detail | `/assessments/SYN-ASM-001` | Four separate participant relationships, recorded evidence/follow-up, signature pending, no editing/signing action |
| Issued history | `/assessments/SYN-ASM-001/history` | Version 1's missing follow-up preserved; version 2 current; no finalized lock/signatures |
| Competency guide | `/assistants/competency` | Exact sample returns synthetic citation `SYN-UI-001`; other questions escalate |
| Equipment guide | `/assistants/manual` | Exact sample returns synthetic citation `SYN-UI-002`; no manuals or equipment instructions loaded |

Guide samples are real CSRF-protected POST forms, not live model calls. Input is
limited to 500 characters and the mock retains no conversation. Blank/overlong
questions return explicit errors. These citations are synthetic demonstrations,
not approved laboratory guidance or acquired sources.

The records are read-only, but scoped access writes minimized audit observations.
Do not present this as a database that never changes.

## Review scope with existing personas

Identity is fixed by trusted server configuration, never a browser control.
Stop the server, change `APP_MOCK_USER_ID` and its display label in the same
shell, then restart the same loopback command. Do not reseed or reset the fixture.
Changing a label cannot grant a role.

| Synthetic ID | Existing scope |
| --- | --- |
| `SYN-EMP-001` | Testing Personnel's own record |
| `SYN-LEAD-001` | Assigned Team Lead's team scope |
| `SYN-ASR-001` | Explicit Assessor record scope |
| `SYN-TS-001` | Explicit Technical Supervisor record scope |
| `SYN-ADM-001` | SQUAD Admin's configuration scope |
| `SYN-PLAT-001` | Minimized, audited Platform Admin diagnostics |
| `SYN-OUT-001` | No visible assessments |

For the outsider, the queue is empty and an invisible or absent record returns
the same non-disclosing 404. Platform Admin must provide synthetic support
purpose/reference using the diagnostic form; content and participants are
withheld even after access succeeds. Administrative scope does not grant signing
or other participant authority.

## Demonstration acceptance and limitations

- `/health` returns only `{"status":"healthy"}`.
- Repeating `init-demo` preserves the owned fixture; browsing does not seed it.
- Validate all six pages with keyboard and visible focus, narrow widths and
  200% text. Check table-local scrolling rather than whole-page overflow.
- No record POST action is available; no signatures are recorded.
- Guide samples show their separate synthetic citations and unsupported
  questions escalate. No external AI/email or remote assets are required.
- Run the tests/repository checks in [DEVELOPMENT.md](DEVELOPMENT.md).
- Record current command/browser results; historical task results are not a
  substitute for validation of the demonstration checkout.

Editing, signing, export, production notifications, Blob access, production
identity, approved assistant corpus, live AI, expanded population and deployment
remain deferred. Specialist privacy/accessibility/operational reviews remain
separate gates. Local visual acceptance is not production conformance approval.

Current #17 validation passed all 48 page-layout checks: six screens at
360/390/768/1024px with 16px and 32px root text. A bounded
[responsive-text repair](archive/tasks/buildathon-responsive-text.md) corrected
eight pre-existing enlarged-text overflow cases without clipping content.
The guides also passed synthetic citation/escalation checks and 500-character
questions at 360px/32px text. The browser input bridge did not dispatch Tab/Enter,
so real keyboard activation and visible keyboard-focus verification still need
manual review; programmatic focus alone is not that evidence.

## Public presentation and optional inputs

The [public presentation example](../presentations/html-workshop/README.md)
demonstrates the reusable framework with synthetic publishing-control content;
it is not a completed project pitch deck. Open audience and presenter modes
locally or build the portable audience output with the documented Python tool.

Knowledge-format comparisons and local training workbooks are optional reference
material, not approved AI sources or prerequisites. Their movement, publication
or ingestion needs owner/release approval. Do not copy controlled content or
operational rows into a presentation, workbook summary, prompt or public PR.
