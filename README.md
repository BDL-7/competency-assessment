# Competency Assessment Tracker

Planning and build-preparation repository for the Non-CLIA laboratory
competency assessment tracker and its separate read-only knowledge assistant.

> **Status:** S0-01 and S0-02 are approved. S0-03 provides a runnable, tested
> Flask application foundation. Assessment workflows, physical database schema,
> migrations, Azure resources, and knowledge-assistant behavior are not implemented.

## Intended technical baseline

- Server-rendered Flask application on Azure App Service
- Microsoft Entra ID authentication
- Azure SQL for structured records
- Private Azure Blob Storage for approved artifacts
- Managed identity, Azure Key Vault, and Application Insights
- Minimal-content email notifications with delivery history
- Separate read-only EDAV/OpenAI knowledge assistant
- Continuous audited Platform Admin diagnostic/read access without assessment,
  signature, approval, or ordinary workflow-mutation authority

The application will control records and workflow. AI may explain approved
requirements with citations, but it must not score, approve, sign, notify, or
modify official records.

## Repository map

| Directory | Purpose |
| --- | --- |
| `AGENTS.md` | Bounded agent roles, authority, file leases, stop conditions, and human gates |
| `agent-tasks/` | Reusable task contract and first coding sprint dependency graph |
| `agent-tasks/s0-01-synthetic-scenario.md` | Approved synthetic scenario and observable acceptance criteria |
| `agent-tasks/s0-02-interface-schema-contract.md` | Shared interface, conceptual schema, transaction, authorization, idempotency, and assistant contract |
| `agent-tasks/s0-03-application-foundation.md` | Runnable application-foundation task contract and validation record |
| `app/` | Flask factory, safe configuration, web and mock-identity boundaries, templates, static assets, and empty future module boundaries |
| `tests/` | S0-03 factory, route, configuration, identity, and module-boundary tests |
| `docs/` | Public repository policy and manifests; controlled binaries remain outside public Git |
| `docs/PRODUCT.md` | Approved prototype scope, exclusions, and success conditions |
| `docs/ARCHITECTURE.md` | Approved modular Flask and Azure boundaries for implementation |
| `docs/WORKFLOW.md` | Canonical assessment sequence, states, and deterministic controls |
| `docs/AUTHORIZATION.md` | Role, scope, action, and administrative-support boundaries |
| `docs/AI_BOUNDARY.md` | Separate read-only assistant contract and prohibited capabilities |
| `docs/project/ca-architecture-one-pager.md` | Public-safe Azure AI platform support review summary |
| `docs/architecture-decisions/` | Public-safe records of approved architecture boundaries |
| `data/` | Data classification guidance and future synthetic fixtures |
| `presentations/html-workshop/` | Reusable HTML presentation framework; project content is release-controlled |
| `scripts/documents/` | Build requirements; project-specific builders remain release-controlled |
| `scripts/maintenance/` | Historical repository-maintenance utilities |
| `scripts/verify_repository.py` | Public-repository safety and structure checks |
| `artifacts/archive/` | Historical manifests and reproducible source; large binary renders stay out of normal Git |

## Development prerequisites

- Python 3.12
- Windows PowerShell for the historical maintenance scripts
- A modern browser for the modular HTML presentation
- Microsoft Word or approved LibreOffice tooling if PDF conversion is required

### Run the application foundation

Create a Python environment and install the fully pinned development environment:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.lock
```

`.env.example` documents the supported environment names but is not loaded
automatically. Export local values in the shell, then start Flask:

```powershell
$env:APP_ENV = "development"
$env:APP_SECRET_KEY = "replace-with-a-local-random-value"
$env:APP_MOCK_AUTH_ENABLED = "false"
python -m flask --app wsgi run
```

The startup page is at `http://127.0.0.1:5000/`; the minimal health probe is at
`http://127.0.0.1:5000/health`. Mock identity is disabled by default. When it is
explicitly enabled for local development or tests, its synthetic identity comes
only from server configuration and grants no roles. Production requires
`APP_SECRET_KEY` and rejects mock authentication.

Run all application tests and repository checks:

```powershell
python -m pytest
python scripts\verify_repository.py
```

The S0-03 foundation intentionally contains no assessment, signature, renewal,
notification, persistence, migration, or assistant behavior.

### Build repository documents

Install the separate document-building dependency only when document work is
authorized:

```powershell
python -m pip install -r requirements-docs.txt
```

Authorized internal checkouts may contain project-specific Word builders. When
present, they can be run locally with:

```powershell
python scripts\documents\build_business_value_need.py
python scripts\documents\build_consolidated_documents.py
```

The builders and generated documents are intentionally excluded from the public
baseline. Do not publish them without document-owner and information-security
approval.

The presentation framework can be opened through
`presentations/html-workshop/example.html`. Project-specific deck content and
presenter notes are not included in the public source baseline.

## Controlled inputs

Raw workforce trackers, governed workbooks, controlled forms, project-plan
binaries, and presenter notes are not published to this public repository.
Authorized team members should follow `docs/SOURCE_MANIFEST.md` and
`data/DATA_CLASSIFICATION.md` to obtain and validate those inputs.

Never commit identifiable workforce data, credentials, tokens, connection
strings, private keys, or confidential presenter notes. Use synthetic data for
development, demonstrations, documentation, and automated tests.

## Phase 0 implementation foundation

Phase 0 records the approved product boundary, source authority, terminology,
workflow, authorization, conceptual domain model, migration approach,
application architecture, read-only AI boundary, testing strategy, development
workflow, operations gates, agent contracts, and first-sprint task graph. These
are planning and governance artifacts; they do not authorize application code.

The future first coding sprint will develop one synthetic application workflow
and one bounded read-only assistant path in parallel. Center/quality viewer
access, Power BI, MIST/HIR migration execution, CLIA workflows, production
deployment, and production data remain excluded from that sprint.

Start with [`docs/PRODUCT.md`](docs/PRODUCT.md),
[`docs/SOURCE_AUTHORITY.md`](docs/SOURCE_AUTHORITY.md), and
[`agent-tasks/first-coding-sprint.md`](agent-tasks/first-coding-sprint.md).

## Source authority

When authorized copies are available, authority is:

1. Current Competency Assessment Tracker Project Plan
2. App Architecture and Implementation Guide
3. Controlled forms, laboratory guidance, and approved test-system catalog
4. MIST/HIR workbooks as migration sources and lineage evidence
5. CA Relational Tables workbook as a non-authoritative design reference
6. Presentations as stakeholder communication
7. Generated files and renders as supporting evidence only

See `SECURITY.md` and `CONTRIBUTING.md` before adding project inputs.

Azure AI platform reviewers can start with
[`docs/project/ca-architecture-one-pager.md`](docs/project/ca-architecture-one-pager.md).
It summarizes the proposed services, workflow, support boundary, open platform
questions, and governing-document path without publishing controlled content.

No open-source license has been approved yet; see `LICENSE.md` before reuse.
