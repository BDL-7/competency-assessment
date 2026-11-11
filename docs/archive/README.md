# Documentary history

Completed delivery records and one-time maintenance evidence live here so they
do not compete with [current setup](../DEVELOPMENT.md) or
[active task contracts](../../agent-tasks/README.md).

These are historical records, not current product, laboratory-policy or
architecture authority. Their original approvals, limitations, literal file
leases and validation claims are preserved. A merged issue does not satisfy
an unresolved specialist or operational approval gate. Use
[source authority](../SOURCE_AUTHORITY.md) when sources conflict.

## Completed delivery records

Each task below came from `agent-tasks/` under the same filename. Text is
preserved as recorded; statements such as "pending merge" describe the original
handoff, not a newly verified approval. Do not execute historical commands
without a new approved task.

| Archived record | Issue | Current entry point |
| --- | --- | --- |
| [Synthetic examples](tasks/20-synthetic-buildathon-data.md) | #20 | [Fictional examples](../../data/examples/README.md); the old local CSV remains ignored |
| [Local knowledge bundle](tasks/22-local-cat-kb-bundle.md) | #22 | [Source access and approval](../SOURCE_MANIFEST.md); the local bundle is not an approved assistant corpus |
| [Workflow safeguards](tasks/25-agent-workflow-safeguards.md) | #25 | [Manual preflight and checks](../DEVELOPMENT.md#tests-and-repository-checks) |
| [Ignore policy](tasks/buildathon-ignore-policy.md) | #17, BR-06 | [Data classification](../../data/DATA_CLASSIFICATION.md) and [current ignore rules](../../.gitignore) |
| [Onboarding](tasks/buildathon-onboarding.md) | #17, BR-01 | [Development](../DEVELOPMENT.md) and [local walkthrough](../BUILDATHON.md) |
| [Presentation repair](tasks/buildathon-presentation.md) | #17, BR-02 | [Reusable public framework](../../presentations/html-workshop/README.md) |
| [Responsive-text repair](tasks/buildathon-responsive-text.md) | #17, BR-05 | [Demo acceptance and limitations](../BUILDATHON.md#demonstration-acceptance-and-limitations) |
| [Application foundation](tasks/s0-03-application-foundation.md) | #9, S0-03 | [Development](../DEVELOPMENT.md); later service/pilot contracts remain active |

Current scenario/interface specifications, workflow/pilot boundaries and open
decisions remain in the [task index](../../agent-tasks/README.md). No controlled
plans, operational data or generated release packages were added to this archive.

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
