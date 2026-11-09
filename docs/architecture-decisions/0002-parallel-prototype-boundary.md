# ADR 0002: Parallel application and assistant prototype boundary

- **Status:** Accepted for Phase 0 and prototype planning
- **Date:** 2026-08-25

## Context

The Project Plan includes both the controlled competency application and the
separate read-only knowledge assistant. The approved implementation direction
is to develop bounded vertical slices for both in the first coding sprint while
preserving their distinct authority and data boundaries.

## Decision

The first coding sprint will develop the application workflow and read-only
assistant in parallel after shared interfaces are approved. The application is
the only system of record and the only component allowed to change official
records. The assistant uses only acquired, active, approved, access-permitted
sources; provides citations; and escalates unsupported questions.

The first sprint excludes Center/quality viewer access, Power BI, MIST/HIR
migration execution, CLIA workflows, production deployment, and production
data. Prototype assumptions may be revised before MVP or production through a
documented decision and affected-test review.

## Consequences

- Separate file ownership permits safe parallel implementation.
- The incomplete QMML/NCIRD corpus limits assistant coverage but never permits
  unsupported answers.
- Assistant credentials and interfaces cannot enable scoring, approval,
  signatures, notification delivery, permission changes, publication, or
  record mutation.
- Integrated testing must prove both the application workflow and assistant
  boundary.
- This decision does not authorize the coding sprint or production use.
