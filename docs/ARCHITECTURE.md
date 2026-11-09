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

Center access, Power BI, migration execution, CLIA behavior, production
deployment, and enterprise integrations remain outside the first coding
sprint. Adding one requires a new approved issue and, where architectural, an
ADR.
