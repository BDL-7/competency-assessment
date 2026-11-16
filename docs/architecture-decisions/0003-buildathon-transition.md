# ADR 0003: Buildathon platform transition

- Status: **Proposed; not accepted**
- Tracking: #56
- Decision owner: architecture owner, with platform and source/privacy review

## Context

The requester requires both CLIA and non-CLIA application workflows, integrated
multi-lab synthetic data and a separate read-only competency assistant. That
scope does not by itself change the approved technical baseline or supply
laboratory-governed rules. Existing public #13 recorded both contexts as
planning; the current scope clarification is documented in [PRODUCT.md](../PRODUCT.md).

The existing application is Flask/SQLAlchemy/Alembic with a small SQLite/mock
pilot. The approved technical direction includes App Service, Entra, Azure SQL,
private Blob and an EDAV OpenAI read-only adapter. Foundry availability has been
reported, but the actual project capabilities, network/region, source access and
processing approvals are unverified. See the
[canonical matrix](../ARCHITECTURE.md#buildathon-stack-and-evidence-matrix).

## Proposed decision

Retain the modular Flask application, SQLAlchemy/Alembic persistence, Entra
identity and app-owned scopes, Azure SQL system of record, private Blob artifacts
and existing platform-control direction. Select a minimal supported Microsoft
Foundry model/agent adapter for the competency assistant only after the decision
owner accepts this ADR and the independent processing/source gates pass.

Do not add orchestration libraries, retrieval services, alternate databases,
containers, Functions, automation products or a replacement UI merely because
they are available. Equipment knowledge remains a separate future pilot; preserve
the current clearly labeled mock placeholder.

## Rationale and alternatives

- Foundry may align with the reported buildathon project and bounded knowledge
  capabilities. Availability alone does not prove audience isolation, supported
  retrieval or operational access; verify these before choosing configuration.
- Retaining EDAV OpenAI remains the approved baseline alternative. Do not remove
  that direction until the architecture owner records a replacement decision.
- Explicit offline mock operation is useful for local development and evaluation
  fixtures, but is not a live integration or a fallback for a failed live call.
- A rewrite or expanded multi-service platform adds complexity without an
  approved requirement and is not proposed.

## Source and control implications

Keep the assistant outside record mutation and consequential decisions. It gets
no scoring, remediation approval, signature, delivery, permission, publication
or equipment-control capability. Filter active permitted sources before context
assembly; return usable source/version/location citations or explicit escalation.

The synthetic registry is not an acquired laboratory corpus. Distinguish
synthetic-demo use, audience and external-processing/upload approval. Individual
assessments, people, signatures and audits are not default retrieval inputs.
Unacquired QMML/NCIRD sources remain unavailable.

## Migration and coexistence

Introduce the minimal read-only adapter contract behind the existing assistant
route, preserving explicit mock mode and current regression behavior. The
existing code has no live EDAV adapter to migrate; do not invent a deployed
coexistence story. Retain the EDAV technical baseline in decision history if
Foundry is accepted. A live failure reports unavailable, never successful mock
output. Version prompts/settings, bound calls and minimize logs.

Application SQL workflow adapters, dataset/UI ownership compatibility and
source-backed CLIA/non-CLIA behavior are separate engineering/domain tasks.
Changing the model provider cannot resolve those gaps.

## Approval and acceptance evidence

| Gate | Current evidence |
| --- | --- |
| Requester scope | Both application workflows and competency assistant requested; not provider/policy approval |
| Architecture decision | Pending named owner acceptance and any required controlled-guide owner action |
| Platform | App registration, SQL, private Blob, Foundry region/network/model/retrieval and controls unconfirmed |
| Sources/privacy | Audience, synthetic use and external processing/upload approvals pending |
| Verification | No live model, retrieval, Azure SQL, Entra or Blob evidence from this documentation task |
| Delivery | Local UI acceptance first; deployment/provisioning and external delivery separately approved |

Before acceptance record owner approval evidence, selected supported capability,
alternatives/rationale, source/control review and validation requirements here.
Before readiness claims record actual approved synthetic integration/evaluation
results. Neither this draft nor passing local tests is human approval.
