# Competency Assessment Tracker

A server-rendered Flask prototype for laboratory competency assessment.
[Product planning](docs/PRODUCT.md) covers both **CLIA and non-CLIA research
and surveillance contexts**; the current executable demonstration uses a
synthetic Non-CLIA scenario.

> **Local prototype, fictional data.** The opt-in pilot provides read-only
> assessment views and deterministic mock guides. It does not implement CLIA
> workflows or production integrations and is not approved for operational use
> or deployment. Including CLIA in planning is not a claim of regulatory compliance.

## Run locally

1. **Prepare the environment:** follow the
   [Python 3.12 installation steps](docs/DEVELOPMENT.md#local-prerequisites-and-installation).
   Install the pinned development dependencies; cloud services and document
   conversion tools are not needed.
2. **Open the demo:** follow the
   [dedicated synthetic setup](docs/BUILDATHON.md#initialize-a-dedicated-synthetic-demo),
   then open `http://127.0.0.1:5000/`. Use a new, dedicated database and keep
   the server on loopback; never reset an unknown database.
3. **Explore and test:** use the
   [six-screen walkthrough](docs/BUILDATHON.md#six-screen-walkthrough) and
   [test commands](docs/DEVELOPMENT.md#tests-and-repository-checks).

Prefer the minimal foundation without demo data? Use
[foundation startup](docs/DEVELOPMENT.md#configuration-and-foundation-startup).
These linked guides are the maintained homes for commands and recovery steps.

## What works today

| Surface | Current behavior |
| --- | --- |
| Local pilot | Scoped overview, searchable work queue, assessment detail and issued-version history: **one assessment, two versions, seven synthetic identities, zero signatures** |
| Mock guides | Competency and equipment-guide forms with deterministic synthetic citations and escalation; no live AI or approved laboratory guidance |
| Workflow services | Synthetic assessment, follow-up, signing, finalization and renewal behavior tested separately through in-memory persistence ports; not exposed as UI actions |
| SQL layer | SQLAlchemy mappings, Alembic schema history and scoped pilot reads; no full SQL-backed workflow mutation unit of work |
| Separate examples | A local generator for 70 fictional people and five data-quality scenarios; not loaded into the app or used to grant permissions |

The pilot uses a fixed synthetic reference date of **2027-02-20**, not today's
date. Business records are read-only, but access auditing writes minimized
observations. Its pending signature is not a completed signature.

Editing, signing, export, production identity/notifications, Blob access and
live AI are not enabled in the UI. Multi-lab coverage, five-year
history/projections and CLIA workflows are not implemented. See the
[pilot contract](agent-tasks/s0-07-local-pilot-ui.md) for evidence and outstanding
specialist reviews; prototype success is not operational approval.

## Find your way

| Work on | Start here |
| --- | --- |
| Application | [app/](app/) - Flask composition, domain/services, SQL persistence, templates and assets |
| Tests and schema | [tests/](tests/), [migrations/](migrations/) and [testing strategy](docs/TESTING.md) |
| Setup, design and controls | [Documentation guide](docs/README.md) |
| Fictional examples and private-input boundaries | [Data guide](data/README.md) |
| Optional presentation tools | [Reusable HTML framework](presentations/html-workshop/README.md); synthetic examples, not the current project pitch |

Root WSGI, Alembic and dependency files remain the application entry points.
The [development guide](docs/DEVELOPMENT.md) explains the direct dependency
manifests, pinned locks and optional tooling. [scripts/](scripts/) contains
manual repository checks; [artifacts/](artifacts/) explains ignored output
destinations. [Documentary history](docs/archive/README.md) is separate from
current setup instructions.

## Product and laboratory context

Start with [scope and exclusions](docs/PRODUCT.md),
[workflow](docs/WORKFLOW.md), [roles](docs/AUTHORIZATION.md) and
[terminology](docs/TERMINOLOGY.md). They distinguish approved prototype rules,
broader planning and unresolved laboratory decisions.

The approved technical direction remains Flask on Azure App Service with Entra
ID, Azure SQL and private Blob Storage. See [architecture](docs/ARCHITECTURE.md)
for the full baseline and gated platform evaluations; these are not all
implemented integrations. The [architecture one-pager](docs/architecture-one-pager.md)
is a public platform-review summary, not governing authority.

AI may explain approved sources with citations, but may not score, approve,
sign, deliver official notifications, grant access or change official records.
Administrative membership does not confer assessment or signature authority.
See [source authority](docs/SOURCE_AUTHORITY.md),
[authorized source access](docs/SOURCE_MANIFEST.md) and the
[read-only assistant boundary](docs/AI_BOUNDARY.md).

## Contribute safely

Use synthetic data for development, tests and demonstrations. Controlled forms,
catalogs, operational workbooks, credentials and confidential notes must not be
published without the applicable approvals. Knowledge-format comparisons are
advisory references, not an approved assistant corpus.

Follow [contributing](CONTRIBUTING.md), [security](SECURITY.md),
[data classification](data/DATA_CLASSIFICATION.md) and the
[issue-linked development workflow](docs/DEVELOPMENT.md#git-and-task-workflow).
Agent work also follows [AGENTS.md](AGENTS.md) and a scoped
[current task contract](agent-tasks/README.md).

No open-source license has been approved. Read the [reuse notice](LICENSE.md)
before using this material outside the project.
