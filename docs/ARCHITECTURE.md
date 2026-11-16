# Application Architecture

## Approved baseline

The system is a server-rendered Python Flask modular monolith on Azure App
Service. Microsoft Entra ID authenticates users. Azure SQL is the structured
system of record. SQLAlchemy provides persistence mapping and Alembic controls
schema changes. Private Azure Blob Storage retains approved artifacts. Managed
identity, Azure Key Vault, Azure Monitor, and Application Insights provide
platform controls. An approved email service delivers minimal-content
notifications. A separate read-only adapter uses EDAV OpenAI.

No alternate application framework, database, cloud platform, SPA,
microservice, Kubernetes, Azure Functions, or public API is part of Phase 0.

## Microsoft Foundry evaluation option

On 2026-11-02 the requester clarified that Microsoft Foundry is newly available
as a platform option for this pilot, not a mandated replacement or an approved
architecture selection. Evaluate it alongside the existing EDAV OpenAI direction
without discarding the Flask, service, domain, and persistence foundation.

The evaluation must distinguish AI capabilities from application hosting,
identity, structured records, artifact storage, and audit responsibilities.
Compare the simplest suitable model/agent and retrieval options for the staged
assistants described in [PRODUCT.md](PRODUCT.md), including reuse, integration
effort, source isolation, cost drivers, and local mock operation. Do not assume
Foundry replaces the application's system-of-record or authorization controls.

Verify current capabilities against official documentation and availability
with Azure/EDAV owners. Source access, tenant/region availability, networking,
data handling, and operational support remain approval questions. A selected
architecture change requires owner approval and an ADR before implementation.
Evaluation does not authorize SDK additions, resource provisioning, document
uploads, external model calls, or deployment.

## Buildathon stack and evidence matrix

This is the canonical active stack matrix. Other guides should link here rather
than maintain competing selections. "Available" is not "approved", "implemented"
or "verified". No live platform evidence was obtained by the documentation task.

| Responsibility | Current implementation | Approved technical baseline | Proposed transition | Availability / selection gate | Required verification |
| --- | --- | --- | --- | --- | --- |
| UI | Read-only Flask pilot with mock identity | Python 3.12 server-rendered Flask modular monolith | Integrated multi-lab CLIA and non-CLIA workflows | Scope requested; exact governed differences need evidence | SQL-backed commands and separate browser journeys |
| Structured records | SQLAlchemy mappings, Alembic, local SQLite fixture/pilot reads | Azure SQL with SQLAlchemy/Alembic | Retain baseline, implement persistent service adapters | Azure SQL availability/access unconfirmed | Actual approved backend migrations, transactions, constraints, concurrency and restart |
| Hosting | Loopback demonstration only | Azure App Service | Retain Web App direction | Web Apps reported available; local acceptance and separate deployment gate | Approved runtime/build/startup and deployed endpoint smoke checks |
| Identity | Trusted server-configured mock subject | Microsoft Entra ID | Resolve trusted subject/tenant to app-owned roles/scopes | Sign-in availability does not establish registration/claims approval | Real approved identities and cross-scope denials |
| Files | Synthetic artifact metadata | Private Azure Blob Storage | Authorized private retrieval | Storage offering unspecified; Blob/network/access approval needed | Synthetic allowed/denied retrieval and visible failure behavior |
| Competency assistant | Deterministic synthetic mock | Read-only EDAV OpenAI adapter direction | Microsoft Foundry model/agent behind the same read-only boundary | Foundry reported available; ADR 0003 remains proposed | Approved sources/audience and actual cited/adversarial evaluations |
| Platform controls | Local configuration gates and audit observations | Managed identity, Key Vault, Monitor/Application Insights | Retain baseline controls | Owner confirmation of identities, network, secrets and telemetry | Least-privilege access and minimized failure/observation evidence |
| Notifications | Logical events/attempt interfaces; no delivering adapter | Separately approved email service | Preserve event boundary; add delivery only when approved | No delivery service selection or external-send approval here | Idempotent event recording separately from actual delivery |
| Developer tools | GitHub/Copilot | Development assistance | No runtime authority | Not a chatbot, identity provider or authorization engine | No product dependence on external authoring tools |

[ADR 0003](architecture-decisions/0003-buildathon-transition.md) records the
proposed transition, not an accepted replacement. Shared SQL support ports now
persist idempotency results, user audit events and non-delivering notification
events/attempts in one explicitly committed transaction, and reuse the pilot's
SQL scope predicate for queries. See [the support-port contract](../agent-tasks/60-shared-sql-persistence.md).
This is not the full workflow unit of work: aggregate writes and missing
identity/configuration/signature mappings remain unimplemented. Service tests
using fake aggregate ports are not proof of persistent workflow mutations.
The multi-lab loader is not yet the
UI setup path, and neither is a live Azure integration.

The SQL support transaction rolls back by default and closes its session;
committed/closed ports cannot silently start another transaction. Existing
database uniqueness constraints protect support-effect identities. Unsupported
actor kinds, replay-only result state, ambiguous timestamps and incomplete
notification context fail explicitly instead of being fabricated. Errors log
categories without SQL parameters or record payloads. Alembic preserves existing
application loggers when configuring migration logging.

Only local synthetic SQLite behavior is verified for these ports. Aggregate
optimistic concurrency, complete finalization atomicity, service-principal
persistence and live Azure SQL remain separate work and evidence gates.

## Future module boundaries

```text
app/
  web/             server-rendered routes, forms, templates, validation
  auth/            Entra identity resolution and authorization policies
  domain/          states, invariants, and domain decisions
  services/        use cases and transaction coordination
  data/            SQLAlchemy models, repositories, and unit-of-work boundary
  documents/       private artifact metadata and controlled retrieval
  notifications/   events, attempts, idempotency, and approved email adapter
  reporting/       role-scoped views and controlled exports
  audit/           append-only security and business events
  ai/              separate read-only assistant adapter
```

Dependency direction is `web -> services -> domain`, with infrastructure
adapters implementing interfaces owned by the application layer. Routes do not
own workflow rules and infrastructure adapters do not bypass services.

## Boundaries and transactions

- Only the controlled Flask application creates or changes official records.
- Each state-changing use case checks authorization and current version inside
  its transaction boundary.
- Finalization coordinates version state, signatures, artifact metadata,
  renewal, notification event, and audit evidence so partial completion is not
  reported as finalized.
- Notification event creation is separate from delivery attempts so a delivery
  failure does not change the assessment result.
- External calls use stable request/correlation identifiers and safe retries.
- Concurrent edits detect stale versions; they do not silently overwrite.
- Blob retrieval is private, short lived, and authorized per request.
- Email contains no assessment result or unnecessary sensitive content.

The exact approved notification execution pattern and Azure network boundaries
are platform-review decisions. Phase 0 does not select another worker product
or create Azure resources.

## Extension gates

Center access, Power BI, operational migration, production deployment and
unapproved enterprise integrations remain outside the transition. CLIA and
non-CLIA are both current delivery targets; see the
[workflow evidence contract](WORKFLOW.md#dual-workflow-evidence-and-integration-contract)
for the exact distinction between requested scope, existing behavior and
unresolved governed rules. Architecture changes still require an accepted ADR.
