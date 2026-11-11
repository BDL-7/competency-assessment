# Data: examples and protected inputs

This directory does **not** contain the laboratory's operational datasets.
Its public contents are handling guidance and [fictional examples](examples/README.md).
The application's SQL persistence code lives separately in [app/data](../app/data/).

## Choose the right synthetic resource

| Resource | Purpose | Loaded by the app? |
| --- | --- | --- |
| [Local pilot fixture](../docs/BUILDATHON.md) | One assessment, two issued versions and seven synthetic identities for the current read-only UI | Yes, only through explicit `init-demo` setup |
| [Fictional examples](examples/README.md) | Generator for a local 70-person roster and five data-quality scenarios | No; illustrative roles grant no access |

These are purpose-built fictional resources, not samples or anonymized copies
of operational trackers. Keep projections distinct from completed activity.

## Obtain real inputs privately

The former `authoritative`, `migration` and `reference` public subfolders held
only guidance. Their distinct requirements are collected below; any ignored
local copies remain untouched and protected at their existing paths.

| Input | Meaning and handling |
| --- | --- |
| Approved test-system catalog | Governed reference data. Keep workbooks outside public Git unless the owner approves release; record authorized versions/hashes in the [source manifest](../docs/SOURCE_MANIFEST.md). Add sanitized machine-readable fixtures separately after review. |
| MIST/HIR operational trackers | Restricted inputs to a future staged, reconciled migration, not the target database design. Never commit raw rows to public Git. Keep them in approved controlled staging; future import tests use synthetic workbooks exercising schema and edge cases. |
| Earlier relational-model workbooks | Non-authoritative design ideas. Current project documents and controlled sources take precedence. Review and sanitize before publishing any derived schema or mapping. |

Follow [data classification](DATA_CLASSIFICATION.md) and the
[migration controls](../docs/DATA_MIGRATION.md). Preserve source workbook,
sheet, row and source-identifier lineage; do not silently resolve ambiguous
values. Do not copy identifiable workforce data into documentation, fixtures,
demonstrations, logs or AI prompts.
