# Data classification and repository policy

| Data class | Examples | Git policy |
| --- | --- | --- |
| Synthetic | Invented employees, assessments, teams, and test systems | Source fixtures may be committed outside `data/`; generated workbooks remain ignored |
| Schema and mapping | Field definitions and approved value mappings without operational rows | Commit after review |
| Governed reference | Approved test-system catalog | Commit only with owner and release approval |
| Migration source | MIST and HIR operational trackers | Never commit raw to public Git |
| Generated export | Reports, extracts, reconciliation files | Ignore; store in controlled staging |
| Local training input | Optional buildathon training workbooks | Ignore local XLSX under `docs/buildathon-resources/`; publication requires separate release approval |

Migration tooling must preserve source workbook, sheet, row, and source-record
lineage. It must not silently normalize ambiguous values. Tests and demos must
use synthetic fixtures.

## Source versus local output

The entire `data/` directory is ignored. Never force-add it; Git ignore does not
remove previously committed content from history or keep local files private
outside Git. Use only approved channels for controlled material. Clean clones
regenerate synthetic files from tracked fixtures outside this directory.

Keep application source, tests, synthetic fixtures, canonical guidance, manifests
and public presentation HTML/JavaScript/CSS/assets tracked. The presentation
builder's default output belongs under ignored `artifacts/generated/`; renders
belong under ignored `artifacts/renders/`. PDF/ZIP release outputs saved directly
under `presentations/html-workshop/` are also ignored.

Do not blanket-ignore HTML, images, PDFs or workbooks across the repository.
Tracked reference formats remain tracked until their ownership and source/output
relationship are reviewed. Adding an ignore rule does not untrack a committed
file, remove it from history or authorize deletion. Never use force-add to bypass
these rules without the applicable owner/release approval.
