# Current Tasks and Baseline Contracts

Use this directory to select an approved task and understand the specifications
it depends on. A file's presence is not approval or a writable lease.

## Current work

| Contract | Scope |
| --- | --- |
| [Repository cleanup (#28)](28-repository-cleanup.md) | Organization and developer onboarding only; no runtime, policy or schema changes |

## Retained baselines and open gates

| Reference | Why it remains here |
| --- | --- |
| [Synthetic scenario](s0-01-synthetic-scenario.md) | Acceptance criteria, prototype-only assumptions and unresolved production/source decisions |
| [Interface contract](s0-02-interface-schema-contract.md) | Shared service/domain/persistence interfaces and traceability, not the physical schema |
| [Workflow slice](s0-04a-workflow-vertical-slice.md) | Current behavior/control contract; recorded review gates must not be inferred complete from merge status |
| [Local pilot](s0-07-local-pilot-ui.md) | Current read-only UI boundary and deferred specialist reviews |
| [First-sprint graph](first-coding-sprint.md) | Baseline dependencies and deferred tracks, not authorization to execute them |

[Completed delivery records](../docs/archive/README.md) retain original approvals,
validation and limitations. Their old paths and commands describe history, not
current onboarding. Preflight accepts only a contract filename directly in this
directory; it does not select archived work or establish authorization.

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
