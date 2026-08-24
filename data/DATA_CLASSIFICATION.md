# Data classification and repository policy

| Data class | Examples | Git policy |
| --- | --- | --- |
| Synthetic | Invented employees, assessments, teams, and test systems | Commit |
| Schema and mapping | Field definitions and approved value mappings without operational rows | Commit after review |
| Governed reference | Approved test-system catalog | Commit only with owner and release approval |
| Migration source | MIST and HIR operational trackers | Never commit raw to public Git |
| Generated export | Reports, extracts, reconciliation files | Ignore; store in controlled staging |

Migration tooling must preserve source workbook, sheet, row, and source-record
lineage. It must not silently normalize ambiguous values. Tests and demos must
use synthetic fixtures.
