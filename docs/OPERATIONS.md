# Operations and Production Gates

## Approved environment intent

| Environment | Data | Purpose |
| --- | --- | --- |
| Development | Synthetic only | Rapid application and assistant development without production secrets or records |
| Test | Synthetic or explicitly approved representative test data | Integration, role, accessibility, migration-rehearsal, and user-acceptance evidence |
| Production | Approved operational data only after authorization | Controlled operation with separate resources, groups, monitoring, backup, deployment approval, and support |

Production deployment is outside the first coding sprint and is not authorized
by Phase 0.

## Local UI-first pilot gate

The requester confirmed on 2026-11-02 that the next pilot goal is to build and
review the UI locally, with no deployment at this stage. Future authorized UI
tasks must extend the existing Flask application using synthetic data and
clearly labeled deterministic mock bot responses, without requiring a final
Foundry selection or cloud resources.

Local validation uses loopback only and must demonstrate the approved user
journeys, scoped data/counts, historical versus projected labeling, typed
errors, and keyboard/accessibility behavior. Report what is implemented,
mocked, deferred, and untested. Supported mutations retain server-side
authorization, CSRF, concurrency, idempotency, and locked-record controls.

No remote hosting, deployment workflow enablement, resource provisioning,
external notifications, or remote AI calls are authorized by this direction.
A local UI calling a remote model still processes data externally and needs
separate approval. Source publication is not deployment; check that a push
cannot trigger deployment before publishing.

Requester acceptance of the local pilot is a prerequisite to a separate
deployment-readiness assessment, not deployment approval. All applicable
platform, security/privacy, records, accessibility, and operational gates remain.

## Platform review gates

Azure/EDAV owners must confirm App Service runtime and deployment, Entra
registration and groups, managed-identity connectivity, Azure SQL access and
backup, private Blob retention and recovery, approved email delivery, Key
Vault, Monitor/Application Insights, EDAV OpenAI integration, network
boundaries, support hours, and incident escalation.

## Operational control gates

Before production, named human authorities approve:

- Security and privacy assessment
- Sensitive workforce data handling and controlled exports
- Records retention and disposition
- Accessibility evidence
- Backup, recovery, and restoration evidence
- Monitoring, alerting, log retention, and incident response
- SQUAD Admin and Platform Admin access and review processes
- Platform Admin support-purpose recording and amendment/repair procedure
- Controlled deployment and rollback
- Authority to operate

Platform Admin access follows ADR 0001: continuous, named, attributable,
least-privilege diagnostic/read access across environments with no assessment,
signature, approval, business-policy, or ordinary workflow-mutation authority.
