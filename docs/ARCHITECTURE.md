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
