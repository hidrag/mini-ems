# 14 — Release Baseline: Phase 1 Foundation

Status: Phase 1 foundation is implemented, tested, published to GitHub, and branch-protected. This document records the verified release baseline. It does **not** claim the full Mini EMS application is complete; later phases remain planned.

## Implemented functionality (Phase 1 — in this baseline)
- FastAPI backend foundation on Python 3.12 (uv, locked `uv.lock`).
- PostgreSQL integration via SQLAlchemy 2.x + Psycopg 3.
- Alembic migration creating the single approved `system_metadata` table.
- Endpoints: `GET /` (API info), `GET /api/v1/health` (liveness), `GET /api/v1/health/database` (readiness via `SELECT 1`, HTTP 503 when unavailable).
- React + TypeScript + Vite health/status interface (Tailwind CSS), TanStack Query + Axios.
- Isolated backend testing: dedicated test database with a fail-closed guard (environment, target and hostname validation).
- Frontend testing: Vitest + Testing Library (bounded fork workers).
- GitHub Actions CI: separate backend and frontend jobs.

## Verified test results (at baseline)
- Backend: **29 tests passed** (local and GitHub Actions).
- Frontend: **17 tests passed** (local and GitHub Actions).
- Ruff lint: passed. Ruff formatting: passed.
- TypeScript typecheck: passed. ESLint: passed.
- Frontend production build: passed.
- GitHub Actions: backend and frontend jobs passed (run `44482873466`, commit `2b4ad10`).

## Git baseline
- Phase 1 implementation commit: `762bf383780ce08056880c10a1633f7bf87e9838` (`762bf383`).
- CI syntax correction commit: `2b4ad10e55a3a3a80c23640d5713de36c8521823` (`2b4ad10`).
- Branch: `main`. Remote: `origin/main` (`https://github.com/hidrag/mini-ems.git`).
- Working tree clean at release baseline; local and remote in sync.

## Branch protection baseline (Stage B.1)
- `main` requires pull requests before merging.
- Required status checks (must pass and be up to date before merging): `Backend (Python 3.12 + native PostgreSQL)` and `Frontend (Node 24 LTS)`.
- `enforce_admins` enabled — protections apply to admins; no bypass by default.
- Force pushes disabled; branch deletion disabled.
- Stale review dismissal enabled.
- Mandatory approving reviews: **0**. This is a solo-owner repository and GitHub blocks self-approval, so requiring ≥1 approval would make merging impossible. Raise to 1 if a second maintainer is added.

## Outstanding limitations / not implemented (planned, not in this baseline)
- Starlette/httpx TestClient deprecation warning remains informational (non-blocking).
- AWS deployment (Stage C) has not started; no production infrastructure provisioned.
- Docker explicitly excluded from scope.
- No authentication/RBAC, organisations/sites/devices, MQTT/telemetry ingestion, meter simulator, dashboards/analytics, alarms, or PDF/Excel reports implemented yet (later phases).
- Single-EC2 hosting is the approved production target but is not provisioned; instance sizing will be determined from measured local load before Stage C.

## Implemented vs planned
Implemented: the Phase 1 foundation listed above. Planned (not in this baseline): all later-phase application modules and AWS deployment. This is a foundation release baseline, not the complete Mini EMS product.
