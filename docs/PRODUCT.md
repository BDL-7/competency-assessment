# Product Scope

## Purpose

The Competency Assessment Tracker is a laboratory application prototype whose
delivery target includes both CLIA and non-CLIA research/surveillance workflows.
The requester reaffirmed both executable workflows for the buildathon transition
in issue #56. The current implementation still demonstrates a synthetic
Non-CLIA scenario; that limitation is not the requested final scope.
Neither synthetic demonstrations nor this scope decision establish regulatory
compliance or supply unspecified laboratory rules.

The intended application covers assignments, due dates, assessment documentation,
required follow-up, signatures, notifications, reporting, audit history, artifacts
and renewal. A separate read-only knowledge assistant is intended to explain
supported requirements from approved sources with citations and SME escalation.
These intended capabilities are not all available in the local UI; see the
[current demonstration boundary](BUILDATHON.md#demonstration-boundary).

## Existing prototype baseline

These decisions are approved for prototype planning and implementation and may
be revised before MVP or production through a documented decision:

- Build the application and read-only knowledge assistant in parallel.
- Use the approved Non-CLIA form V04 as the provisional Non-CLIA baseline, not
  as an implicit CLIA rule set.
- The Assessor records outcomes; the application validates approved rules but
  does not calculate competency or make pass/fail decisions.
- An unsuccessful required element needs documented follow-up or remedial
  action before finalization.
- Store Employee/Testing Personnel, Assigned Team Lead, Assessor, and Technical
  Supervisor/final signer as separate relationships.
- Calculate renewal from the approved completion date plus a configured,
  approved interval.
- Demonstrate due, overdue, submitted, signature-required, and completed
  notification events; production cadence remains open.
- Lock finalized records and preserve corrections as superseding amendments.
- Use synthetic or explicitly approved test data only.
- Mock application roles when development Entra access is unavailable.
- Preserve the approved Azure technical direction; identify any unavailable
  external resource as a prototype dependency or explicit stub.

## Existing baseline journey

The first sprint demonstrates one synthetic end-to-end application path and a
bounded read-only assistant in parallel:

`Configure -> Schedule -> Assign -> Notify -> Assess -> Document evidence ->
Follow up -> Testing Personnel sign -> Technical Supervisor sign -> Finalize
and lock -> Retain artifact metadata -> Audit -> Renew -> Report`

The assistant uses only active approved prototype sources, returns citations,
and escalates unsupported questions. The incomplete QMML/NCIRD corpus limits
coverage but does not authorize invented answers.

## Pilot direction recorded on 2026-11-02

The requester confirmed the following planning requirements in issue #13.
This remains one pilot application built on the existing implementation, not
a new application or a general-purpose multi-bot platform.

- Design a configurable synthetic multi-lab demonstration for approximately
  70 human users, counting service identities separately. Propose fictional
  lab counts, test types, test systems, and process-grouping relationships;
  an existing operational inventory is not a prerequisite.
- Cover five years of synthetic history and five years of clearly labeled
  future planning relative to a configurable reference date. Future projections
  are not completed assessments, signatures, or events that already occurred.
- Include CLIA and Non-CLIA research/surveillance contexts in the proposed
  demonstration design. Distinguish regulatory applicability from activity,
  test type, test system, and process grouping. This does not authorize CLIA
  workflow implementation or invent laboratory rules, intervals, or signatures.
- Consider staged competency-knowledge and equipment-manual assistants within
  the same app, with separate source scopes and the read-only controls in
  [AI_BOUNDARY.md](AI_BOUNDARY.md). Manual answers require approved,
  versioned sources and citations; they grant no equipment-control capability.
  Neither bot gains access to individual assessment records by default.
- Build and review the UI locally with synthetic data before considering any
  deployment; see [OPERATIONS.md](OPERATIONS.md).

These are planning requirements, not authorization to generate data, change
schema, implement broader workflows, or deploy. Existing approved behavior and
regression fixtures remain the baseline. Lab counts, population distribution,
taxonomies, schema extensions, and laboratory-policy decisions require the
appropriate task and owner approvals before implementation. The first-sprint
exclusions below remain in force for executable behavior.

## Explicit first-sprint exclusions

These describe the original sprint, not a permanent exclusion of CLIA from the
current delivery target. The transition requirements below supersede that
scope limitation without rewriting historical decisions.

- Center/quality viewer access
- Power BI
- Execution of MIST/HIR migration
- CLIA workflows
- Production deployment or production data

## Current dual-workflow delivery requirements

- Connect the fictional multi-lab dataset to the actual application database/UI.
- Implement separately identifiable CLIA and non-CLIA journeys using evidenced
  applicability and workflow rules, not duplicated labels or a forced common
  signature/renewal policy.
- Reuse shared application controls: scoped authorization, explicit participant
  relationships, immutable versions, concurrency, idempotency and audit evidence.
- Complete the [workflow evidence matrix](WORKFLOW.md#dual-workflow-evidence-and-integration-contract)
  before implementing a rule-dependent difference. Missing public evidence is
  an exact owner action, not permission to infer policy or drop CLIA.
- Require separate passing application/browser evidence for both journeys.
  Until then, dual-workflow delivery remains incomplete.
- Keep the competency assistant read-only and separate from individual records.
  The equipment guide remains its current labeled mock placeholder, not a new
  corpus or integration.

The [canonical stack matrix](ARCHITECTURE.md#buildathon-stack-and-evidence-matrix)
distinguishes the existing app from proposed and live-verified integrations.
The local UI-first/no-deployment boundary remains unchanged.

## Always prohibited

AI may not determine competency or pass/fail, close remediation, approve or
sign an assessment, deliver official notifications, grant access, publish
controlled material, or modify an official record.

Generic HR competency features, self-rating, manager-rating comparisons, peer
or 360 reviews, development plans, talent analytics, workforce ranking,
multi-tenant SaaS, public APIs, a separate SPA, microservices, Kubernetes, and
unapproved enterprise integrations are outside scope.

## Prototype success

The prototype succeeds when the representative application record completes
the approved workflow with role denials, audit evidence, a locked version, and
renewal; and when the separate assistant produces a supported cited answer and
an unsupported-question escalation. Prototype success is not production
approval.
