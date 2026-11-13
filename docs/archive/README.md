# Documentary history

Completed plans, delivery records and one-time maintenance evidence live here so they
do not compete with [current setup](../DEVELOPMENT.md) or
[active task contracts](../../agent-tasks/README.md).

These are historical records, not the current execution plan or a replacement
for canonical product, laboratory-policy or architecture guidance. Still-applicable
approved prototype decisions and interface agreements retain their original
authority and limits. Original approvals, limitations, literal file leases and
validation claims are preserved; only relative links are adjusted when needed.
A merged issue does not satisfy an unresolved specialist or operational approval gate. Use
[source authority](../SOURCE_AUTHORITY.md) when sources conflict.

## Retention

Keep these records until the requester explicitly requests deletion. There is
no automatic expiry, scheduled deletion or age-based disposal rule. Before any
future deletion, review unique decisions, approvals, unresolved gates and
references and obtain the applicable human approval. Moving a record here is
not permission to delete it later.

## Completed delivery records

Each task below came from `agent-tasks/` under the same filename. Text is
preserved as recorded; statements such as "pending merge" describe the original
handoff, not a newly verified approval. Do not execute historical commands
without a new approved task.

| Archived record | Issue | Current entry point |
| --- | --- | --- |
| [Synthetic examples](tasks/20-synthetic-buildathon-data.md) | #20 | [Synthetic data inventory](../DATA_INVENTORY.md); local outputs remain ignored |
| [Local knowledge bundle](tasks/22-local-cat-kb-bundle.md) | #22 | [Source access and approval](../SOURCE_MANIFEST.md); the local bundle is not an approved assistant corpus |
| [Workflow safeguards](tasks/25-agent-workflow-safeguards.md) | #25 | [Manual preflight and checks](../DEVELOPMENT.md#tests-and-repository-checks) |
| [Ignore policy](tasks/buildathon-ignore-policy.md) | #17, BR-06 | [Data classification](../DATA_CLASSIFICATION.md) and [current ignore rules](../../.gitignore) |
| [Onboarding](tasks/buildathon-onboarding.md) | #17, BR-01 | [Development](../DEVELOPMENT.md) and [local walkthrough](../BUILDATHON.md) |
| [Presentation repair](tasks/buildathon-presentation.md) | #17, BR-02 | [Reusable public framework](../../presentations/html-workshop/README.md) |
| [Responsive-text repair](tasks/buildathon-responsive-text.md) | #17, BR-05 | [Demo acceptance and limitations](../BUILDATHON.md#demonstration-acceptance-and-limitations) |
| [Application foundation](tasks/s0-03-application-foundation.md) | #9, S0-03 | [Development](../DEVELOPMENT.md); later service/pilot decisions remain indexed below |
| [First-sprint graph](tasks/first-coding-sprint.md) | #13; original Phase 0 plan | [Product](../PRODUCT.md) and [current tasks](../../agent-tasks/README.md); the phase graph is not today's execution queue |
| [Synthetic acceptance scenario](tasks/s0-01-synthetic-scenario.md) | #5, S0-01 | [Workflow](../WORKFLOW.md), [testing](../TESTING.md) and the retained decisions below |
| [Domain/interface agreement](tasks/s0-02-interface-schema-contract.md) | #7, S0-02 | [Architecture](../ARCHITECTURE.md) and the retained agreement below; not the executable SQL schema |
| [Workflow implementation contract](tasks/s0-04a-workflow-vertical-slice.md) | #11, S0-04A | [Current demo](../BUILDATHON.md); historical workflow UI targets are not current UI capabilities |
| [Local pilot delivery](tasks/s0-07-local-pilot-ui.md) | #15, S0-07 | [Local walkthrough](../BUILDATHON.md) for maintained instructions; original visual selections and integration approval remain history |
| [Repository organization](tasks/28-repository-cleanup.md) | #28 | [Documentation](../README.md), [data guide](../DATA_INVENTORY.md) and this archive; not current writable leases |
| [README refinement](tasks/31-readme-experience.md) | #31 | [Main README](../../README.md); original PR validation remains historical |

All rows above originated at `agent-tasks/<same filename>`. Issues #5, #7,
#11, #13, #15, #28 and #31 were confirmed closed during #34; that confirms
task execution status only. No controlled plans, operational data or generated
release packages were added to this archive.

## Retained baselines and open gates

These references remain usable; archiving changes location, not decisions.
Use canonical guidance for current scope and the walkthrough for what the
app actually exposes.

| Retained evidence | Where to find it | What remains limited or unresolved |
| --- | --- | --- |
| Original positive/negative acceptance criteria and prototype assumptions | [Scenario sections 6-10](tasks/s0-01-synthetic-scenario.md#6-positive-acceptance-criteria) | A01-A07/A09 apply only to the synthetic prototype, not production laboratory policy |
| Approved source and supported-answer gate | [Scenario A08 and D09](tasks/s0-01-synthetic-scenario.md#9-prototype-only-assumptions-and-recorded-decisions) and [current AI boundary](../AI_BOUNDARY.md) | No source-owner approval is created by mock guides or this move |
| Production rules and ownership | [Scenario D01-D12](tasks/s0-01-synthetic-scenario.md#10-unresolved-decisions-and-downstream-ownership) | Fields/outcomes, remediation completion, intervals, signed corrections/amendment, notifications, identity, sources, retention/export, form currency and accessibility remain owner decisions |
| Shared interfaces and traceability | [Original interface agreement](tasks/s0-02-interface-schema-contract.md#11-traceability) and [architecture](../ARCHITECTURE.md) | Existing agreements remain the baseline unless explicitly superseded; historical port catalogs are not claims of complete implementation |
| Workflow controls and pending reviews | [Workflow approval record](tasks/s0-04a-workflow-vertical-slice.md#approval-record) | Pending Data/Flask/QA/security/accessibility/integration entries remain pending as recorded; merge status does not complete them |
| Local-only pilot approval | [Pilot integration approval](tasks/s0-07-local-pilot-ui.md#local-only-integration-approval) and [current demo limits](../BUILDATHON.md#demonstration-acceptance-and-limitations) | Specialist operational-use/deployment reviews remain outstanding; local integration was not specialist sign-off |

## Presentation extraction history

[Format audit](presentations/format-audit.md) came from
`presentations/html-workshop/FORMAT_AUDIT.md`. It explains historical source
extraction decisions, not the maintained runtime contract. Use the
[framework README](../../presentations/html-workshop/README.md) and
[content schema](../../presentations/html-workshop/CONTENT_SCHEMA.md) for the
current reusable tools. The active handoff is a reusable prompt, not a completed
task record, and stays with that framework.

## Maintenance snapshots

These scripts encoded one-time operations for an earlier local layout. Their
contents are preserved with a `.txt` suffix so they are not presented as runnable
PowerShell utilities. Their relative-root calculations and destinations are
historical, not maintained automation. Do not restore or run them.

| Snapshot | Original path |
| --- | --- |
| [Earlier reorganization](maintenance/reorganize_repo.ps1.txt) | `scripts/maintenance/reorganize_repo.ps1` |
| [Earlier archive operation](maintenance/archive_superseded_materials.ps1.txt) | `scripts/maintenance/archive_superseded_materials.ps1` |

For dated presentation/release provenance, see the separate
[artifact archive](../../artifacts/archive/README.md). Some entries are pointers
to controlled or unavailable local deliverables, not packages included in Git.
