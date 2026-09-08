# Product Scope

## Purpose

The Competency Assessment Tracker is a controlled Non-CLIA laboratory
application for assignments, due dates, assessment documentation, required
follow-up, signatures, notifications, reporting, audit history, artifacts, and
renewal. A separate read-only knowledge assistant explains supported
requirements from approved sources with citations and SME escalation.

## Approved prototype baseline

These decisions are approved for prototype planning and implementation and may
be revised before MVP or production through a documented decision:

- Build the application and read-only knowledge assistant in parallel.
- Use the approved Non-CLIA form V04 as the provisional prototype baseline.
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

## First coding sprint

The first sprint demonstrates one synthetic end-to-end application path and a
bounded read-only assistant in parallel:

`Configure -> Schedule -> Assign -> Notify -> Assess -> Document evidence ->
Follow up -> Testing Personnel sign -> Technical Supervisor sign -> Finalize
and lock -> Retain artifact metadata -> Audit -> Renew -> Report`

The assistant uses only active approved prototype sources, returns citations,
and escalates unsupported questions. The incomplete QMML/NCIRD corpus limits
coverage but does not authorize invented answers.

## Explicit first-sprint exclusions

- Center/quality viewer access
- Power BI
- Execution of MIST/HIR migration
- CLIA workflows
- Production deployment or production data

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
