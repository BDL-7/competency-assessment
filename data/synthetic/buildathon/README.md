# Buildathon synthetic scenario catalog

This directory is a safe starting point for the separate buildathon dataset.
It contains only scenario descriptions, not app-ready employee or assessment
records. The existing one-assessment local demo remains the regression
baseline.

HIR and MIST are examples of inconsistent current formats, not canonical
schemas or source data for this dataset. Do not copy, anonymize, transform,
sample, or infer values, names, taxonomies, or distributions from those
workbooks. The scenario catalog is purpose-built and fictional.

The catalog identifies missing/incomplete information and conflicting
candidate values so future UI work can test how gaps are surfaced. A conflict
must remain unresolved until an authorized human decides; the app must not
silently pick or normalize a value. It also describes future planning as
projection-only, not a completed assessment, signature, or event.

This catalog does not define the eventual population size or role distribution,
laboratory taxonomies, required-field rules, or CLIA behavior. Those decisions
require the relevant owner approval before records are generated or loaded.
No application schema, workflow, authorization, migration, cloud, or deployment
behavior is enabled by these descriptions.

Use the local demo instructions in `docs/BUILDATHON.md` for the currently
implemented read-only pilot. The catalog is not currently consumed by the app.
