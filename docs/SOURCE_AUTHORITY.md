# Source Authority

## Governing order

Apply this order without silently reconciling conflicts:

1. `Competency_Assessment_Tracker_Project_Plan.docx` for current product scope,
   roles, workflow decisions, and delivery direction.
2. `App Architecture & Implementation Guide.pdf` for technical implementation.
3. Controlled forms, laboratory guidance, and `Approved Test Systems.xlsx` for
   their governed domain requirements and catalog values.
4. MIST and HIR workbooks as migration sources and lineage evidence.
5. `CA Relational Tables.xlsx` as a non-authoritative design reference.
6. Presentations as stakeholder communication.
7. Generated files, renders, and archives as supporting evidence only.

When a higher-level project decision conflicts with a controlled laboratory
requirement within that document's authority, implementation stops and both
owners resolve the conflict. An agent may not choose a winner.

## Current source status

| Source | Current use | Limitation or gate |
| --- | --- | --- |
| Project Plan | Governing product direction | Prototype assumptions remain revisable before MVP or production |
| Architecture Guide | Governing technical baseline | Networking, retention, ownership, and production authorization remain open |
| Non-CLIA form V04 | Provisional prototype fields, evidence prompts, remedial-action prompt, and signatures | Revalidate currency before production |
| QMML and NCIRD Guidelines | Link index | Full authorized corpus is not acquired; do not invent linked content |
| Approved Test Systems | Governed catalog source | Owner approval required before public release or operational load |
| MIST/HIR | Migration lineage | Raw operational rows never enter public Git or synthetic fixtures |
| CA Relational Tables | Earlier schema ideas | Terminology and structure do not override current decisions |
| Current presentation | Approved stakeholder framing | Does not create policy or technical authority |

## Superseded material

The current Project Plan supersedes the former Project Proposal,
Implementation Plan, and Leadership Concept Brief. Former React, Azure
Functions, CLIA electronic-signature, WORM-storage, and Staff/Lab
Director/Auditor directions are not implementation requirements.

## Traceability and staleness

Canonical implementation rules record the source label, status, and required
human gate, but do not reproduce controlled content. Source owners, versions,
approval/effective dates, and hashes are maintained through
`docs/SOURCE_MANIFEST.md` when authorized. A source version change reopens all
affected rules, tests, and approvals.
