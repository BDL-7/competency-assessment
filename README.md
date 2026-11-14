# Competency Assessment Tracker

A server-rendered Flask prototype for laboratory competency assessments:
the evidence recorded, the follow-up documented and the history retained.
It is intended for Testing Personnel, Assigned Team Leads, Assessors and
Technical Supervisors, with separate responsibilities for each.

[Product planning](docs/PRODUCT.md) covers **both CLIA and non-CLIA laboratories**
in research and surveillance contexts. The executable pilot currently
demonstrates a **synthetic Non-CLIA scenario**, not that full planned scope.

> **For local evaluation only.** Fictional records, read-only assessment views
> and deterministic mock guides. No operational-use or deployment approval;
> no claim of regulatory compliance, validation or production readiness.

[Try the pilot](#try-the-pilot) | [What is built](#what-is-built-and-what-is-not) |
[Find your next step](#find-your-next-step) | [Repository map](#repository-map)

**Local demo address after setup:** [`http://127.0.0.1:5000/`](http://127.0.0.1:5000/)
This loopback address works on your computer; it is not a deployed website.

## Try the pilot

Start here to see the application. No cloud account, live model or document
conversion tools are needed.

1. **Set up Python 3.12.** Follow the
   [installation steps](docs/DEVELOPMENT.md#local-prerequisites-and-installation)
   from the repository root, using the pinned development dependencies.
2. **Initialize and run the demo.** Follow the
   [PowerShell setup](docs/BUILDATHON.md#initialize-a-dedicated-synthetic-demo),
   then open `http://127.0.0.1:5000/`. Use a new, dedicated synthetic database,
   keep the server on loopback and never reset an unknown database.
3. **Follow one assessment.** Use the
   [six-screen walkthrough](docs/BUILDATHON.md#six-screen-walkthrough) to move
   from the overview and work queue to recorded evidence, follow-up and
   issued-version history, then try the two mock guides.

**What to expect:** one assessment, two issued versions, seven synthetic
identities and **zero recorded signatures**. The second version awaits a
signature; you cannot sign it in this UI. Dates are evaluated against the fixed
synthetic reference date **2027-02-20**, not today's date.

Setup commands, identity changes and recovery steps stay in the walkthrough
so there is one maintained set of instructions.

## What is built, and what is not

| Layer | Available today | Boundary |
| --- | --- | --- |
| Local pilot | Scoped overview, searchable work queue, assessment detail and issued history | Business records are read-only; access auditing still writes minimized observations |
| Mock guides | Competency and equipment-guide forms with synthetic citations and unsupported-question escalation | Deterministic examples, not live AI, loaded manuals or approved laboratory guidance |
| Workflow services | Assessment, follow-up, signing, finalization and renewal exercised through in-memory persistence ports | Tested separately; not available as UI actions |
| SQL persistence | SQLAlchemy mappings, Alembic migrations and scoped pilot reads | No complete SQL-backed workflow mutation unit of work |

**Not implemented:** multi-lab coverage, five-year history/projections and CLIA
workflows. Editing, signing, export, production identity and notifications,
Blob access and live AI are not enabled in the UI. The
[walkthrough](docs/BUILDATHON.md#demonstration-acceptance-and-limitations) records
the current boundary and outstanding specialist reviews; the
[original pilot contract](docs/archive/tasks/s0-07-local-pilot-ui.md) retains
its approval and delivery history.

## Find your next step

| If you are here to... | Go to... |
| --- | --- |
| Evaluate the product | [Scope and exclusions](docs/PRODUCT.md), [assessment workflow](docs/WORKFLOW.md) and [roles](docs/AUTHORIZATION.md) |
| Develop the application | [Developer guide](docs/DEVELOPMENT.md) for configuration, foundation-only startup and [tests/checks](docs/DEVELOPMENT.md#tests-and-repository-checks); [architecture](docs/ARCHITECTURE.md) for the technical baseline |
| Contribute a change | [Contributing](.github/CONTRIBUTING.md) and the [issue-linked workflow](docs/DEVELOPMENT.md#git-and-task-workflow); agent work also needs [AGENTS.md](AGENTS.md) and an approved, scoped [task contract](agent-tasks/README.md) |

For terminology, design decisions, optional presentation tooling and deeper
controls, use the [documentation guide](docs/README.md).

## Repository map

| Location | What belongs here |
| --- | --- |
| [app/](app/) | Flask application, domain and services, SQL persistence, templates and assets |
| [tests/](tests/) and [migrations/](migrations/) | Synthetic test coverage and ordered database schema changes |
| [docs/](docs/README.md) and [agent-tasks/](agent-tasks/README.md) | Maintained guidance and current task-specific scope; completed plans are archived |
| [Data inventory](docs/DATA_INVENTORY.md) | Generate flat local workbooks under ignored `data/`; public synthetic source fixtures remain tracked separately |
| [scripts/](scripts/) and [artifacts/](artifacts/) | Manual repository checks and guidance for ignored generated outputs |

At the root, [wsgi.py](wsgi.py) exposes the Flask application;
[migrations/alembic.ini](migrations/alembic.ini) configures migrations via an
explicit `-c` path. Grouped [dependency manifests and locks](scripts/requirements/)
are explained in the developer guide. Completed delivery records live in the
[documentary archive](docs/archive/README.md), not the active setup path.

## Root before and after

Issue #58 relocates public files only. The tracked root changes from nine
directories and seventeen files to **eight directories and nine files**.
The conditional target is **six core directories and eight files** after
separately approved governance transfer and artifact-provenance disposition.
Private remnants and generated caches can keep a local checkout larger.

| Before | After this slice | Why it stays / disposition |
| --- | --- | --- |
| `.github/` | Keep | GitHub workflows, community files and local agent instructions |
| `app/` | Keep | Flask application and runtime assistant package |
| `docs/` | Keep | Canonical guidance, decisions and public presentations |
| `migrations/` | Keep | Alembic environment/configuration and immutable schema history |
| `scripts/` | Keep | Repository checks, synthetic tooling and grouped dependencies |
| `tests/` | Keep | Regression controls and fictional fixtures |
| `.env.example` | Keep | Safe configuration template |
| `.gitattributes` | Keep | Git text/binary and line-ending rules |
| `.gitignore` | Keep | Publication and runtime exclusions |
| `.python-version` | Keep | Supported Python discovery |
| `LICENSE.md` | Keep | Reuse-status entry point |
| `README.md` | Keep | GitHub landing page and navigation |
| `pyproject.toml` | Keep | Python tool settings; not installable dependency metadata |
| `wsgi.py` | Keep | Active Flask import/WSGI entry point; no verified replacement |
| `SECURITY.md` | `.github/SECURITY.md` | GitHub-supported community location |
| `CONTRIBUTING.md` | `.github/CONTRIBUTING.md` | GitHub-supported contribution guidance |
| `requirements.in` | `scripts/requirements/requirements.in` | Unchanged direct runtime dependencies |
| `requirements.lock` | `scripts/requirements/requirements.lock` | Unchanged pinned runtime |
| `requirements-dev.in` | `scripts/requirements/requirements-dev.in` | Unchanged development inputs/includes |
| `requirements-dev.lock` | `scripts/requirements/requirements-dev.lock` | Unchanged reproducible CI/development install |
| `requirements-docs.txt` | `scripts/requirements/requirements-docs.txt` | Optional approved document-tool baseline |
| `alembic.ini` | `migrations/alembic.ini` | Supported explicit configuration path; retained logging |
| `presentations/` | Public files in `docs/presentations/` | Private local remnants untouched |
| `AGENTS.md` | Retain pending approval | Existing safety contract; no exact tool requirement yet justifies a permanent root stub |
| `agent-tasks/` | Retain pending approval | Current leases and approval provenance; external transfer/replacement not authorized |
| `artifacts/` | Retain pending approval | Tracked provenance and private outputs; no blanket deletion |
| `.git/` (local) | Keep | Git requires repository metadata |
| `.venv/` (ignored) | Keep | Existing environment ownership |
| `data/` (ignored) | Keep, untouched | Protected local data; no inspection or generation in this slice |
| `instance/` (ignored) | Keep | Local runtime and owned synthetic/public-build output |
| `tmp/` (ignored) | Unchanged | Owner may have active work/interpreters |
| `__pycache__/` (ignored) | Unchanged | Generated cache; exact cleanup not approved |
| `CAT-KB.zip` (ignored) | Unchanged | Private archive; exact deletion not approved |

The proposed separate AI-development repository is not created or populated.
Local safety/lease controls must work before governance moves. Moving public
files does not approve private cleanup, source release or deployment.

## Keep the demo fictional

The app's small UI fixture and the separate
[70-person workbook pack](docs/DATA_INVENTORY.md) serve different purposes.
The pack can be loaded into a separate synthetic database, but the current UI
uses only its original demo. Illustrative role labels grant no permissions.

Use synthetic data for development, tests and demonstrations. Keep controlled
forms, operational workbooks, identifiable workforce data, credentials and
confidential notes out of public files, prompts, logs and PRs. Follow
[data classification](docs/DATA_CLASSIFICATION.md), [security](.github/SECURITY.md) and
[authorized source access](docs/SOURCE_MANIFEST.md).

Laboratory rules come from [governing sources](docs/SOURCE_AUTHORITY.md), not
demo behavior. AI may not determine competency, approve or sign assessments,
deliver official notifications, grant access or change official records;
see the [read-only assistant boundary](docs/AI_BOUNDARY.md). Administrative
membership does not confer assessment or signature authority. Knowledge-format
comparisons are advisory references, not an approved assistant corpus.

---

**Reuse:** no open-source license has been approved.
Read the [reuse notice](LICENSE.md) before using this material outside the project.
