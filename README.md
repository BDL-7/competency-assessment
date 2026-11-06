# Competency Assessment Tracker

A Non-CLIA laboratory competency assessment application and separate read-only
knowledge assistant, built as a server-rendered Flask modular monolith.

> **Current status:** The Flask foundation, synthetic domain/services,
> SQLAlchemy mappings and Alembic migration are implemented. An opt-in local
> read-only pilot shows one synthetic assessment, two issued versions and
> deterministic mock guides. Full workflow web actions, production adapters,
> cloud resources and live AI are not implemented. No deployment is authorized.

## Start here

| Goal | Guide |
| --- | --- |
| Install, configure, start and test the application | [Development](docs/DEVELOPMENT.md) |
| Run the current synthetic local demonstration | [Buildathon walkthrough](docs/BUILDATHON.md) |
| Find authoritative guidance and design documents | [Documentation index](docs/README.md) |
| Open/build the public synthetic presentation | [HTML presentation framework](presentations/html-workshop/README.md) |
| Contribute safely | [Contributing](CONTRIBUTING.md), [Security](SECURITY.md), [Agent contract](AGENTS.md) |

The application requires **Python 3.12**. A modern browser is sufficient for the
public presentation. Word/PDF conversion tools and internal document builders
are optional and are not prerequisites for running the application.

## What the local pilot demonstrates

- Scoped overview, queue search/filter/sort, detail and issued-version history.
- One assessment awaiting Testing Personnel signature; no signatures recorded.
- Explicit participant relationships, role denials and minimized read auditing.
- Competency and equipment-guide mock forms with synthetic citations/escalation.
- A fixed synthetic reference date of **2027-02-20**, not today's date.

Business records are read-only; access auditing still writes minimized
observations. The framework-neutral workflow service is tested separately with
in-memory persistence ports. The local UI does not wire its mutation commands
or a full persistence unit of work.

Editing, signing, exports, production notifications, Blob access, a multi-lab
population, five-year history/projections, CLIA workflows, production identity,
live AI and deployment are not enabled. See the
[pilot contract](agent-tasks/s0-07-local-pilot-ui.md) for existing evidence and
outstanding specialist reviews. Prototype success is not operational approval.

## Repository units

| Unit | Responsibility |
| --- | --- |
| [app/](app/) | Flask composition, approved domain/service/data boundaries, local UI, templates and static assets |
| [migrations/](migrations/) | Application-owned schema history |
| [tests/](tests/) | Domain, service, authorization, SQL persistence, migration, web and presentation regression checks |
| [docs/](docs/) | Current guidance, source manifests and architecture decisions |
| [agent-tasks/](agent-tasks/) | Task contracts, acceptance criteria and approval history |
| [data/](data/) | Classification and protected-source manifests, not public operational rows |
| [presentations/](presentations/) | Public synthetic HTML framework; project content remains release-controlled |
| [scripts/](scripts/) | Repository verifier, internal-builder guidance and historical maintenance utilities |
| [artifacts/](artifacts/) | Generated-output guidance and retained historical evidence |
| [.github/workflows/](.github/workflows/) | Existing repository/application checks; no deployment job |

Root Python manifests, lockfiles, WSGI and Alembic configuration remain at their
existing entry points. Historical maintenance scripts are not setup commands;
do not run them as a general cleanup operation.

## Approved direction and authority

The approved technical direction remains Flask on Azure App Service, Entra ID,
Azure SQL, private Blob Storage, managed identity, Key Vault, monitoring and
minimal-content notifications. A separate read-only EDAV/OpenAI adapter remains
the baseline; Foundry is an evaluation option, not an approved replacement.

AI may explain approved sources with citations but may not score, approve,
sign, deliver official notifications, grant access or change official records.
Administrative membership does not grant assessment or signature authority.

Begin with [Product scope](docs/PRODUCT.md),
[Source authority](docs/SOURCE_AUTHORITY.md) and
[Architecture](docs/ARCHITECTURE.md). The
[first-sprint graph](agent-tasks/first-coding-sprint.md) and earlier contracts
preserve historical planning and approvals; they are not blanket authorization
to implement deferred work. The
[public architecture one-pager](docs/project/ca-architecture-one-pager.md)
is a platform-review summary, not a replacement for governing documents.

## Protected materials and reuse

Controlled forms, project-plan binaries, governed catalogs, operational
workbooks and confidential presenter notes remain outside public Git. Obtain
authorized inputs through [Source manifest](docs/SOURCE_MANIFEST.md) and follow
[Data classification](data/DATA_CLASSIFICATION.md).

Use synthetic data for development, tests and demonstrations. Do not publish
local workbooks, controlled content, credentials or generated releases without
the applicable owner/release approval. Advisory knowledge-format comparisons
are not approved assistant sources.

No open-source license has been approved; see [License status](LICENSE.md)
before external reuse.
