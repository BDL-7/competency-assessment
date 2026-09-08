# Operations and Production Gates

## Approved environment intent

| Environment | Data | Purpose |
| --- | --- | --- |
| Development | Synthetic only | Rapid application and assistant development without production secrets or records |
| Test | Synthetic or explicitly approved representative test data | Integration, role, accessibility, migration-rehearsal, and user-acceptance evidence |
| Production | Approved operational data only after authorization | Controlled operation with separate resources, groups, monitoring, backup, deployment approval, and support |

Production deployment is outside the first coding sprint and is not authorized
by Phase 0.

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
