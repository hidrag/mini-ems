# AI-Assisted Change Log

## 2026-11-19 — Phase 1 foundation implemented and verified locally (Stage A)
- Owner approved Phase 1 implementation, then a backend security correction (test-guard hostname validation), then frontend/CI/documentation continuation. The previously verified backend was preserved as the foundation.
- Backend (Python 3.12.14 via uv, `uv.lock`): FastAPI + Pydantic Settings + SQLAlchemy 2.x + Psycopg 3 + Alembic. Implemented `GET /`, `GET /api/v1/health`, `GET /api/v1/health/database`; one `system_metadata` migration (id integer PK, key varchar UNIQUE, value text, created_at/updated_at timestamptz NOT NULL DEFAULT now(), SQLAlchemy-managed `updated_at`).
- Security: fail-closed test database guard validates `APP_ENV=testing`, `TEST_DATABASE_URL`, expected host (`TEST_DATABASE_HOST`), port, database name and role before connecting, then verifies `current_database()`/`current_user`; never falls back to `DATABASE_URL`. Added host validation and negative tests (missing/incorrect host, dev/prod targets, mocked connection failure, live identity mismatch), each asserting no connection/mutation occurs on rejection.
- Databases: created separate `mini_ems_dev` and `mini_ems_test` with restricted roles; verified the test role is denied CONNECT to the development database. PostgreSQL 17.12 installed natively (Chocolatey `postgresql17`); no Docker.
- Frontend (Node 24.20.0, npm 11.19.0): React 18 + TypeScript + Vite + React Router + Axios + TanStack Query + Tailwind; minimal health/status interface with loading/success/error/unavailable states and retry; Vitest + React Testing Library. `VITE_API_BASE_URL` normalized so `/api/v1` is never doubled; HTTP 503 handled as an unavailable reading.
- CI: added `.github/workflows/ci.yml` — backend job (native PostgreSQL via apt, dedicated CI database + restricted role with generated/masked password, Python 3.12 via uv, `uv sync --frozen --extra dev`, Ruff + pytest) and frontend job (Node 24, `npm ci`, ESLint + type-check + tests + build). No Docker/AWS/production credentials. Reviewed and validated locally; remote CI not executed (owner publishes in Stage B).
- Integration fix: reduced the backend engine `connect_timeout` 5→2 so the database-unavailable 503 returns within the frontend Axios timeout (previously ~10s across two libpq addresses exceeded it). Also corrected Alembic log formatting and added `path_separator=os`. Both changes re-tested.
- Verified results: backend `uv run pytest` 29 passed and `uv run ruff check .` clean; frontend `npm test` 17 passed, `npm run lint`/`npm run typecheck`/`npm run build` clean; `npm ci` reproduced the lockfile and built without the esbuild postinstall. Real browser smoke test confirmed frontend→backend→PostgreSQL success, liveness during a database outage, 503 readiness, and retry recovery.
- Documentation: updated README (verified setup, databases/roles, environment, testing/CI, status, known limitations), `docs/07-current-sprint.md`, root `.env.example` (`TEST_DATABASE_HOST`) and this changelog.
- Git state: `main` at `f6058f0daaec3617791868e6442accad547b8be3`; the 15 original unstaged documentation changes preserved; new backend/frontend/CI files untracked; nothing staged. No commit/push/merge/tag/reset/branch/history operation; no AWS provisioning; `.hermes/plans/` untouched.


## 2026-11-17 — Local-first and single-EC2 hosting alignment
- Owner approved the 15-file documentation-only update and clarified local/production MQTT security, separate development/test/production PostgreSQL databases and measurement-led AWS resource planning.
- Replaced active provider-specific hosting guidance with Stage A complete local application/testing → Stage B owner-controlled GitHub upload → Stage C separately approved Ubuntu EC2 deployment for approximately 3–4 months.
- Recorded ADR-007, superseding ADR-001 and the provider-specific part of ADR-003 and resolving ADR-005 in favour of Mosquitto. Preserved all product features, Docker exclusion and owner-only Git authority.
- Documented environment ownership, independently configured simulator/MQTT settings, Nginx/systemd operations, backup/restore templates, resource measurement requirements and deployment smoke-test gates. No EC2 instance type or cost claims were introduced.
- Updated `.env.example` with placeholders and commented planned settings; updated `.gitignore` for PostgreSQL backups/runtime data and Mosquitto runtime/credentials without excluding plain SQL migrations.
- Initial state for this approved update: clean `main` at `f6058f0daaec3617791868e6442accad547b8be3` (`Initial commit`), containing the documentation scaffold. Git had been initialised between the earlier audit and this task; this agent did not initialise it.
- Verification from `F:/work/Python/mini-ems`: `git diff --check` passed (exit 0; Windows LF-to-CRLF notices only). `python C:/Users/Abhishek/AppData/Local/hermes/cache/scratch/mini-ems-doc-consistency-20261117.py` passed (exit 0): 23 documentation checks, including 29 `git check-ignore --no-index -q -- <path>` cases for exclusions and trackable examples/migrations. The temporary validator is outside the repository, not application code or a planning artifact.
- Verified exactly the 15 approved modified files, preserved product/demo/schema scope, unchanged API/RBAC/UI/coding documents, valid Markdown links/anchors/fences, matching planned environment identifiers, explicit stage/resource gates, consistent ADR supersession and legacy providers only in superseded history. `git diff --cached --name-only` and `git ls-files --others --exclude-standard` returned no paths; `git rev-parse HEAD` remained at the initial commit. The empty planning directory's timestamps and contents are unchanged.
- Two inline validator attempts did not execute because shell quoting failed (exit 2); the separate temporary script execution above resolved the invocation issue. No application lint/type/test/build command is configured yet, and application tests, service commands, migrations, backup/restore and AWS deployment were not run; they remain future implementation/deployment checks.
- Unresolved: consumer-to-WebSocket delivery/process topology, runtime/frontend test-tool versions, publishing/retention values, backup destination/frequency and recovery objectives, domain/certificates and measured AWS resource selection before Stage C.
- No application code, database data, Git history or AWS infrastructure changed. No commit, push, merge, tag or Git initialisation performed. The existing empty `.hermes/plans/` directory is left untouched; no planning artifacts were created.

## 2026-11-17 — Initial Mini EMS governance pack
- Defined initial product and technology scope.
- Added source-of-truth and AI agent rules.
- Added roadmap and revised Hermes-assisted estimate.
- Added architecture, database, API, auth/RBAC, sprint, UI, coding, testing, security, environment/deployment and ADR documents.
- Added README, .gitignore and environment example.
- No application code implemented.
- No Git commit or push performed.
