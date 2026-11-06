# Documentation

Public guidance and source manifests live here. Governing project binaries and
controlled laboratory sources must be obtained through an approved internal
channel; this index does not approve their release or assistant use.

## Start, develop and demonstrate

- [DEVELOPMENT.md](DEVELOPMENT.md): canonical Python setup, configuration,
  startup, tests, migration checks and issue-first workflow.
- [BUILDATHON.md](BUILDATHON.md): the current synthetic read-only pilot,
  six-screen walkthrough, personas, recovery and limitations.
- [TESTING.md](TESTING.md): required validation layers and control assertions.
- [OPERATIONS.md](OPERATIONS.md): local-only intent, specialist reviews and
  production/deployment gates.
- [Agent task contracts](../agent-tasks/README.md): writable scope, acceptance,
  evidence and human approval; earlier sprint artifacts retain their history.

## Authority and product boundaries

- [SOURCE_AUTHORITY.md](SOURCE_AUTHORITY.md): governing order, conflicts and
  stale-source behavior.
- [PRODUCT.md](PRODUCT.md): approved prototype, follow-on planning and exclusions.
- [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md): authorized metadata/availability.
- [Controlled sources](controlled-sources/README.md): protected domain inputs.
- [Governing project documents](project/README.md): controlled product/technical
  source boundaries.
- [Data classification](../data/DATA_CLASSIFICATION.md): public versus
  controlled data; synthetic fixtures only.

## Design and controls

- [ARCHITECTURE.md](ARCHITECTURE.md): modular Flask/Azure boundaries and gated
  Foundry evaluation.
- [DOMAIN_MODEL.md](DOMAIN_MODEL.md): conceptual entities and invariants.
- [WORKFLOW.md](WORKFLOW.md): canonical sequence, states and open rules.
- [AUTHORIZATION.md](AUTHORIZATION.md): roles, scopes, actions and support access.
- [TERMINOLOGY.md](TERMINOLOGY.md): controlled implementation terms.
- [AI_BOUNDARY.md](AI_BOUNDARY.md): separate read-only assistant and prohibitions.
- [DATA_MIGRATION.md](DATA_MIGRATION.md): staging/lineage/reconciliation controls,
  without authorizing operational migration.
- [ADR 0001](architecture-decisions/0001-platform-admin-support-boundary.md):
  accepted Platform Admin support boundary.
- [ADR 0002](architecture-decisions/0002-parallel-prototype-boundary.md):
  accepted parallel application/assistant boundary.

## Advisory and presentation references

- [Architecture one-pager](project/ca-architecture-one-pager.md): public-safe
  platform-review summary; does not replace governing documents.
- [Knowledge-format comparison](CAT_KB.md),
  [formatted HTML](CAT_KB.html), [PDF](CAT_KB.pdf): advisory material, not approved
  architecture or an assistant corpus. Maintained-source, derivative and release
  decisions must be confirmed before moving, regenerating or removing formats.
- [Public presentation framework](../presentations/html-workshop/README.md):
  synthetic audience/presenter examples and portable audience build.

Local training resources are not part of the public baseline. Do not stage
workbooks or interpret this index as permission to publish or upload them.
