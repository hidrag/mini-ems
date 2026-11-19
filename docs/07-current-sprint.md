# 07 — Current Sprint: Phase 1 Foundation

Status: Phase 1 foundation is implemented and verified locally (Stage A) under owner approval. Backend, frontend, CI workflow and documentation are complete. Git publication (Stage B) and AWS deployment (Stage C) remain owner-controlled and separately approved.

## Phase 1 implementation — completed and verified (Stage A)
- Backend: FastAPI + Pydantic Settings + SQLAlchemy 2.x + Psycopg 3 + Alembic on Python 3.12.14 (uv, `uv.lock`). Three approved endpoints (`GET /`, `GET /api/v1/health`, `GET /api/v1/health/database`); one `system_metadata` migration; fail-closed test database guard including hostname validation.
- Frontend: React 18 + TypeScript + Vite + React Router + Axios + TanStack Query + Tailwind on Node 24.20.0. Minimal health/status interface with loading/success/error/unavailable states and retry; Vitest + React Testing Library.
- Databases: separate `mini_ems_dev` and `mini_ems_test` with dedicated restricted roles; the test role cannot connect to the development database.
- Verified: 29 backend tests + Ruff; 17 frontend tests + ESLint + type-check + production build; real local integration (frontend→backend→PostgreSQL, liveness during a database outage, 503 readiness, retry recovery).
- CI: `.github/workflows/ci.yml` (native PostgreSQL, no Docker) reviewed and validated locally; not run remotely.
- Known limitations and owner smoke-test steps are in `README.md`.

## Completed documentation alignment
The approved documentation now follows ADR-007: Stage A local-first development → Stage B owner-controlled GitHub upload → Stage C separately approved single-EC2 deployment. All product features are preserved, Docker remains excluded, and consumer-to-WebSocket delivery remains unresolved until its own design approval.

Local Mosquitto need not reproduce production TLS configuration. Production requires MQTT authentication, restricted network access and appropriate TLS security, using separate broker configuration. Maintain separate development, automated testing and production PostgreSQL databases; tests must never modify development or production data. Measure the completed local application's CPU, RAM, disk and database usage before preparing an AWS resource recommendation, required before Stage C; no EC2 type or cost claims now.

## Objective
Establish a Windows-native local foundation using FastAPI, React/TypeScript, local PostgreSQL, SQLAlchemy and Alembic. It must run without AWS credentials or infrastructure. No Docker.

## Phase 1 scope — implemented under owner approval
1. Inspect repository and environment.
2. Create project structure.
3. Configure Python venv and backend dependencies.
4. Implement FastAPI application/configuration.
5. Configure SQLAlchemy/Psycopg 3.
6. Configure dedicated local development and automated testing PostgreSQL databases with separate credentials; reject unsafe test targets before any write.
7. Configure Alembic and one `system_metadata` migration.
8. Implement root, application health and database health endpoints.
9. Create React + TypeScript + Vite frontend.
10. Configure frontend API client and health status UI.
11. Add tests and reproducible local lint/type/build checks; prepare CI configuration for Stage B without requiring GitHub to run the application or local checks.
12. Write README and architecture documentation.

## Excluded
Docker, auth/RBAC, organisations/sites/devices, MQTT, simulator, telemetry, WebSockets, analytics, alarms, reports and cloud deployment.

## Acceptance
Backend and frontend start locally; Swagger works; local PostgreSQL `SELECT 1` succeeds; Alembic migration applies; health endpoints report real status; frontend displays backend health; backend tests and frontend type/build checks pass; no secrets are committed; README is reproducible; no unrelated database/project is changed.

Automated tests use only the separate testing database and must never modify development or production data. Test target checks fail closed before migrations, fixtures or cleanup. Local acceptance requires no AWS credentials, provisioned infrastructure or production secrets. Document the frontend build-time API URL and separate backend/test configuration. MQTT and simulator settings remain planned for later milestones.

## Final report
Initial audit, files changed, commands, actual test results, tests not run, limitations, manual smoke steps, Git status and confirmation no commit/push.

Agent must inspect and present plan before editing. Owner approves the relevant implementation plan, reviews implementation and performs smoke tests. Complete all local milestones before Stage B application upload; Stage C requires separate approval after local acceptance and GitHub upload. Stop after the approved documentation update and report.
