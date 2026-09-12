# S0-03 Repository and Flask Application Foundation

## Task contract

| Field | Value |
| --- | --- |
| Task ID | S0-03 |
| Tracking issue | GitHub issue #9 |
| Owner Agent | Flask Application Agent, coordinated by Orchestrator; QA owns test files |
| Goal | Create a secure, minimal, runnable, tested Flask foundation that preserves the approved S0-02 boundaries without implementing workflow behavior. |
| Business Reason | Give S0-04A and S0-04B a reproducible application and test foundation without prematurely selecting domain behavior or infrastructure. |
| Required Context | `AGENTS.md`, approved S0-02 contract, and canonical product, architecture, development, authorization, AI-boundary, and testing documents. |
| Dependencies | S0-02 merged into `dev` through PR #8 at `eca4468`. |
| Approved Dependencies | Flask 3.1.3, SQLAlchemy 2.0.52, Alembic 1.20.0, and pytest 9.1.1. These implement the already approved Flask/SQLAlchemy/Alembic/test baseline; no database driver or Azure SDK is selected. |
| Flask writable lease | `app/**`; `wsgi.py`. |
| QA writable lease | `tests/**`; `pyproject.toml`. |
| Orchestrator writable lease | This task contract; `README.md`; `.env.example`; `requirements.in`; `requirements-dev.in`; generated `requirements.lock`; generated `requirements-dev.lock`. |
| Review-only files | All other repository files and controlled/operational sources. |
| Prohibited Actions | Assessment workflow, domain rules, database models/tables, migrations, real Entra integration, notifications, Blob operations, assistant implementation, Azure resources, production data, controlled content, or additional packages/platforms. |
| Expected Outputs | Modular package structure, application factory, safe configuration, minimal home and health routes, mock identity boundary, pinned dependency manifests/locks, smoke/configuration/boundary tests, and documented commands. |
| Security and Privacy | No secrets or sensitive data. Mock identity is synthetic, disabled by default, never enabled in production, and grants no workflow authority. Health output exposes no environment or dependency detail. |
| Validation | Create `.venv`; install `requirements-dev.lock`; run `python -m pytest`; start/import smoke checks; run `python scripts/verify_repository.py`; run `git diff --check`. |
| Stop Conditions | Any unapproved package/platform, real identity or data requirement, workflow behavior, cross-lease edit, secret exposure, or conflict with S0-02. |
| Human Approval Gate | The Project Requester explicitly authorized S0-03 implementation on 2026-09-12. Deployment and all controlled business decisions remain separate gates. |
| Lease expiry | All leases expire when issue #9 is merged or abandoned. |

## Acceptance criteria

1. `create_app()` returns an application under explicit development, testing, or production configuration.
2. Production configuration fails startup when its required secret placeholder is missing; no fallback secret is embedded.
3. `/health` returns only a minimal healthy response and `/` renders a server-side template.
4. The S0-02 module boundaries exist and import without implementing their later responsibilities.
5. The mock identity provider can be enabled only in development/testing, uses server configuration rather than client-supplied roles, and is rejected in production.
6. Runtime and development dependencies are direct-manifested and fully pinned in generated lock files.
7. Pytest covers the factory, configuration safety, health/home routes, mock identity boundary, and module imports.
8. README documents supported setup, start, test, and validation commands and accurately states that workflow/database/assistant behavior is absent.
9. Flask, QA, and independent security/boundary reviews pass; exact files and validation results are recorded.

## Review record

| Review | Status | Evidence |
| --- | --- | --- |
| Project authorization | Approved | User requested S0-03 implementation on 2026-09-12. |
| Flask implementation | Passed | Application factory, configuration, web, identity, and module-boundary files completed within the application lease. |
| QA | Passed | Clean Python 3.12.13 install from `requirements-dev.lock`; 29 foundation tests passed and `pip check` reported no broken requirements on 2026-09-12. |
| Security/configuration | Passed | Independent review verified production fail-closed behavior, mock-identity controls, dependency and scope boundaries, and regression coverage on 2026-09-12. |
| Orchestrator integration | Passed | Python 3.12.13: 29 tests passed; dependency check, Flask route smoke check, repository verifier for 91 tracked files, compilation, and staged diff check passed. |

S0-04 work remains unauthorized by this task.

## Completion evidence

Changed files: `.env.example`, `README.md`, this task contract, `pyproject.toml`,
`requirements.in`, `requirements-dev.in`, `requirements.lock`,
`requirements-dev.lock`, `wsgi.py`, `app/__init__.py`, `app/config.py`,
`app/auth/__init__.py`, `app/auth/identity.py`, `app/web/__init__.py`,
`app/web/routes.py`, `app/templates/base.html`, `app/templates/home.html`,
`app/static/styles.css`, the behavior-free `__init__.py` boundaries under
`app/ai`, `app/audit`, `app/data`, `app/documents`, `app/domain`,
`app/notifications`, `app/reporting`, and `app/services`, plus
`tests/conftest.py`, `tests/test_app_factory.py`, `tests/test_mock_identity.py`,
`tests/test_module_boundaries.py`, and `tests/test_routes.py`.
