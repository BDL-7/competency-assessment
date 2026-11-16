# Current Tasks

Use this directory to select current work. A file's presence is not approval
or a writable lease. Implementation proceeds through separately approved app
changes, not the historical first-sprint execution sequence.

## Current work

| Contract | Scope |
| --- | --- |
| [Root layout integration (#58)](58-simplify-root-layout.md) | Exact public moves and coupled tooling/docs/tests; no governance export or private cleanup |

The [foundation slice (#54)](54-buildathon-safe-preflight.md) is implemented in
draft PR #55 with passing supported-runtime checks; human review/merge remains
pending. [Integration contracts (#56)](56-buildathon-integration-contracts.md) are
implemented in draft PR #57 with passing CI and independent review; policy and
platform gates remain. Both implementation leases ended at handoff. #58 is based
on the reviewed dependent branch with a separate lease; all PRs target `dev`
without an authorized merge.

## Closed delivery records

These issues and their delivery PRs are closed/merged. Their contracts preserve
historical approval evidence, not active leases. Outstanding specialist and human
gates are not approved by this status summary.

| Contract | Retained scope |
| --- | --- |
| [#34](34-archive-completed-plans.md) | Archival and navigation |
| [#37](37-data-source-inventory.md) | Data-source inventory |
| [#40](40-repository-clarity.md) | Repository clarity and test data isolation |
| [#45](45-buildathon-data-pack.md) | Synthetic pack and evaluation specifications |
| [#48](48-flat-buildathon-workbooks.md) | Flat local workbook generation |
| [#51](51-flatten-local-data.md) | Historical local data-layout work |

The transition targets both CLIA and non-CLIA workflows, integrated multi-lab
synthetic data and a separate read-only competency assistant. Those application
changes need their own exact contracts; #54 does not implement or authorize
unspecified laboratory rules or live platform integrations.

## Requirements and retained decisions

| Need | Start here |
| --- | --- |
| Current scope, controls and implementation guidance | [Documentation guide](../docs/README.md) |
| Current demo and outstanding reviews | [Local walkthrough](../docs/BUILDATHON.md) |
| Original acceptance criteria, prototype decisions, interface agreements and approval evidence | [Archived baselines and open gates](../docs/archive/README.md#retained-baselines-and-open-gates) |

Completed tasks and the old sprint graph are [archived](../docs/archive/README.md),
not current work. Archiving does not revoke still-applicable decisions, approve
pending reviews or make historical feature targets implemented today.
Preflight accepts only a contract filename directly in this directory; it does
not select archived work or establish authorization.

## Contract template

Every implementation or review task uses this contract. It prevents
uncontrolled edits, scope expansion, and conflicting concurrent work.

```text
Task ID:
Owner Agent:
Goal:
Business Reason:
Required Context:
Source-of-Truth Files:
Dependencies:
Approved Assumptions:
Allowed Files:
Review-Only Files:
Prohibited Actions:
Expected Outputs:
Acceptance Criteria:
Validation Commands:
Security and Privacy Considerations:
Definition of Done:
Handoff Format:
Stop Conditions:
Human Approval Gate:
Path Lease Owner and Expiry:
```

## Contract rules

- Goals describe one reviewable outcome.
- Allowed Files are explicit paths, not broad repository ownership.
- Review-Only Files include controlled sources and operational workbooks.
- Assumptions cite an approved decision; an agent cannot create one.
- Stop Conditions include missing authority, sensitive-data exposure, scope
  expansion, interface conflict, and overlapping leases.
- A task reports changed files, validation results, unresolved decisions, and
  the next owner at handoff.
- A task is not complete until required independent and human reviews are
  recorded.
