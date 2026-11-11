# Documentation

Public guidance and source manifests live here. Governing project binaries and
controlled laboratory sources must be obtained through an approved internal
channel; this index does not approve their release or assistant use.

## Develop and run

- [Developer guide](DEVELOPMENT.md): canonical Python setup, configuration,
  startup, tests, migration checks and issue-first workflow.
- [Local demonstration](BUILDATHON.md): the current synthetic read-only pilot,
  six-screen walkthrough, personas, recovery and limitations.
- [Testing strategy](TESTING.md): required validation layers and control assertions;
  planned coverage is not a claim that every layer is implemented.
- [Operations and gates](OPERATIONS.md): local-only intent, specialist reviews and
  production/deployment gates.
- [Current task contracts](../agent-tasks/README.md): writable scope, acceptance,
  baseline specifications and unresolved approval gates.
- [Fictional examples](../data/examples/README.md): separate roster generator
  and data-quality scenarios, not the app's local demo fixture.

## Authority and product boundaries

- [Source authority](SOURCE_AUTHORITY.md): governing order, conflicts and
  stale-source behavior.
- [Product scope](PRODUCT.md): CLIA and non-CLIA planning, current synthetic
  Non-CLIA baseline and implementation exclusions.
- [Source access and manifest](SOURCE_MANIFEST.md): authorized metadata,
  availability and protected project/laboratory-source requirements.
- [Data classification](../data/DATA_CLASSIFICATION.md): public versus
  controlled data; synthetic fixtures only.

## Design and controls

- [ARCHITECTURE.md](ARCHITECTURE.md): modular Flask/Azure boundaries and gated
  Foundry evaluation.
- [DOMAIN_MODEL.md](DOMAIN_MODEL.md): conceptual entities and invariants,
  not the implemented database schema.
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

- [Architecture one-pager](architecture-one-pager.md): public-safe
  platform-review summary; does not replace governing documents.
- [Knowledge-format comparison](CAT_KB.md),
  [formatted HTML](CAT_KB.html), [PDF](CAT_KB.pdf): advisory material, not approved
  architecture or an assistant corpus. Maintained-source, derivative and release
  decisions must be confirmed before moving, regenerating or removing formats.
  Selecting a maintained source and reconciling differences is a separate task;
  none of these formats is assumed disposable or an approved assistant source.
- [Public presentation framework](../presentations/html-workshop/README.md):
  synthetic audience/presenter examples and portable audience build.

Local training resources are not part of the public baseline. Do not stage
workbooks or interpret this index as permission to publish or upload them.

## History, not setup

- [Documentary archive](archive/README.md): completed task records, original
  path map and non-executable maintenance snapshots.
- [Artifact archive](../artifacts/archive/README.md): dated release provenance;
  distinguishes tracked instructions/manifests from untracked deliverables.
