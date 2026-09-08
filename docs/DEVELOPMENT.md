# Development Workflow

## Current status

Phase 0 creates planning and governance artifacts only. No application package,
runtime dependency manifest, database migration, test suite, or Azure resource
is authorized by this document.

## Approved future layout

```text
app/
migrations/
tests/
  unit/
  integration/
  authorization/
  migration/
  end_to_end/
  ai_evals/
agent-tasks/
docs/architecture-decisions/
```

The future dependency manifest and lockfile must include only dependencies
needed by the approved Flask/Azure baseline. Adding a tool or platform requires
an approved task and, when it changes architecture, an ADR.

## Git and task workflow

1. Create or identify the issue.
2. Branch from current `dev` as `<issue>-<short-slug>`.
3. Create a task contract and acquire exclusive path leases.
4. Agree on shared interfaces before parallel work.
5. Make small coherent commits without generated, controlled, or sensitive
   files.
6. Run task validation and `python scripts/verify_repository.py`.
7. Open a pull request targeting `dev` with the issue-closing reference.
8. Complete independent review and human gates before merge.

`main` and `dev` are protected. Feature branches remain temporary. Agents do
not modify the same file concurrently; cross-owned edits are serialized.

## Data and secret handling

- Use synthetic fixtures for development, demonstrations, and tests.
- Never commit `.env`, credentials, tokens, connection strings, private keys,
  production configuration, operational exports, or raw MIST/HIR workbooks.
- `.env.example` contains names and safe placeholders only.
- Generated and runtime files remain in ignored locations defined by
  `.gitignore` and repository policy.
