# 07 — Current Sprint: Phase 1 Foundation

Status: Planned; nothing is complete until verified.

## Objective
Establish a Windows-native local foundation using FastAPI, React/TypeScript, Neon PostgreSQL, SQLAlchemy and Alembic. No Docker.

## Approved scope
1. Inspect repository and environment.
2. Create project structure.
3. Configure Python venv and backend dependencies.
4. Implement FastAPI application/configuration.
5. Configure SQLAlchemy/Psycopg 3.
6. Connect only to dedicated Mini EMS Neon database.
7. Configure Alembic and one `system_metadata` migration.
8. Implement root, application health and database health endpoints.
9. Create React + TypeScript + Vite frontend.
10. Configure frontend API client and health status UI.
11. Add tests, lint/type/build checks and CI.
12. Write README and architecture documentation.

## Excluded
Docker, auth/RBAC, organisations/sites/devices, MQTT, simulator, telemetry, WebSockets, analytics, alarms, reports and cloud deployment.

## Acceptance
Backend and frontend start locally; Swagger works; Neon `SELECT 1` succeeds; Alembic migration applies; health endpoints report real status; frontend displays backend health; backend tests and frontend type/build checks pass; no secrets are committed; README is reproducible; no unrelated database/project is changed.

## Final report
Initial audit, files changed, commands, actual test results, tests not run, limitations, manual smoke steps, Git status and confirmation no commit/push.

Agent must inspect and present plan before editing. Owner approves plan, reviews implementation and performs smoke test.
