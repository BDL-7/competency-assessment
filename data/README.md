# Data Sources

- `authoritative/` contains governed reference data, currently the approved test-system catalog.
- `migration/` contains legacy operational trackers. These are inputs to a future staged and reconciled migration, not the target database design.
- `reference/` contains earlier relational-model ideas. Current project documents and controlled sources take precedence when terminology conflicts.
- `synthetic/buildathon/` contains purpose-built fictional edge-case scenarios,
  not app-ready records; see its README for limits and approval gates.

Do not copy identifiable workforce data into documentation, tests, demonstrations, logs, or AI prompts. Future migration work must preserve workbook, sheet, row, and source-identifier lineage.
