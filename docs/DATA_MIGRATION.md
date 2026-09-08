# Data Migration and Reconciliation Approach

Migration execution is outside the first coding sprint. This document defines
the control boundary needed to design the application without treating legacy
workbooks as the target database.

## Source roles

- `Approved Test Systems.xlsx` is governed reference data subject to owner
  approval.
- MIST and HIR workbooks are operational migration sources and lineage
  evidence.
- `CA Relational Tables.xlsx` is a non-authoritative design reference.
- Raw operational rows and generated reconciliation outputs never enter public
  Git.

## Controlled sequence

1. Register a MigrationBatch with source identity, custodian, extraction
   context, and SHA-256.
2. Copy authorized source rows into restricted, immutable staging without
   changing the source workbook.
3. Profile sheets, formulas, dates, blanks, aliases, duplicates, and conflicts.
4. Preserve workbook, sheet, row/source identifier, and original value.
5. Propose legacy-to-current crosswalks without overwriting source values.
6. Route ambiguous or contradictory values to MigrationException.
7. Obtain data/laboratory-owner approval for terminology and entity mappings.
8. Load approved reference/configuration data before dependent records.
9. Load approved records idempotently with batch and source lineage.
10. Reconcile counts, representative values, exclusions, and exceptions.
11. Obtain explicit human approval of reconciliation before operational use.
12. Retain or dispose of staging only under approved records requirements.

## Reconciliation evidence

Evidence includes source and staged counts, target counts, accepted mappings,
duplicate handling, rejected rows, unresolved exceptions, representative field
comparisons, and the approving owner. No agent may silently correct formulas,
aliases, dates, missing documents, or contradictory source values.

## Prototype boundary

The first coding sprint uses synthetic fixtures shaped to exercise approved
lineage fields. It does not ingest MIST/HIR rows, estimate migration quality,
or claim readiness for operational migration.
