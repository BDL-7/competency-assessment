# Contributing

1. Do not add controlled or identifiable source data to this public repository.
2. Use synthetic fixtures for application and migration tests.
3. Keep generated output under `artifacts/generated/` or `artifacts/renders/`.
4. Update `docs/SOURCE_MANIFEST.md` when a governing source changes.
5. Run `python scripts/verify_repository.py` before opening a pull request.
6. Document architecture decisions that change roles, signature authority,
   workflow states, data retention, notifications, or AI boundaries.

Generated Word, PDF, HTML, and image files should be distributed through an
approved release or document-management channel, not added casually to Git.
