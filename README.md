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
| Contribute a change | [Contributing](CONTRIBUTING.md) and the [issue-linked workflow](docs/DEVELOPMENT.md#git-and-task-workflow); agent work also needs [AGENTS.md](AGENTS.md) and an approved, scoped [task contract](agent-tasks/README.md) |

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
[alembic.ini](alembic.ini) configures migrations. Dependency manifests and locks
are explained in the developer guide. Completed delivery records live in the
[documentary archive](docs/archive/README.md), not the active setup path.

## Why some files stay at the root

These are tool entry points and repository guidance, not stray application code.
Keeping their standard names and locations lets common tools find them.

| File or folder | What it is for |
| --- | --- |
| `.git/` | Git's repository history and metadata; do not move it |
| `.github/` | GitHub workflows and repository instructions |
| `wsgi.py`, `alembic.ini`, `pyproject.toml` | Flask server entry point, migration settings and Python tool settings |
| `requirements.in`, `requirements.lock` | Runtime dependencies and their pinned install |
| `requirements-dev.in`, `requirements-dev.lock` | Test/development dependencies and their pinned install; CI uses the lock |
| `requirements-docs.txt` | Optional document-building tools, not needed to run the app |
| `SECURITY.md`, `CONTRIBUTING.md`, `LICENSE.md` | Security reporting, contribution guidance and reuse status |

## Keep the demo fictional

The app's small UI fixture and the separate
[70-person workbook pack](docs/DATA_INVENTORY.md) serve different purposes.
The pack can be loaded into a separate synthetic database, but the current UI
uses only its original demo. Illustrative role labels grant no permissions.

Use synthetic data for development, tests and demonstrations. Keep controlled
forms, operational workbooks, identifiable workforce data, credentials and
confidential notes out of public files, prompts, logs and PRs. Follow
[data classification](docs/DATA_CLASSIFICATION.md), [security](SECURITY.md) and
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
