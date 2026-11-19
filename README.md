# Mini EMS — Industrial Energy Monitoring & Management System

> A simulated industrial energy monitoring platform planned with React, FastAPI, Mosquitto MQTT and PostgreSQL.

**Status:** Phase 1 foundation implemented and verified locally (Stage A). Later milestones pending.

**Hardware:** None required. All meters, measurements, equipment states and events are simulated.

## 1. Purpose

Mini EMS demonstrates how an industrial energy monitoring platform collects, validates, stores, analyses and visualises electrical measurements from multiple simulated sites.

Goals:
- Develop practical Python backend, React, PostgreSQL, MQTT, real-time and cloud skills.
- Produce a documented portfolio application relevant to full-stack, backend, data engineering and industrial software roles.

This is an educational simulation. It is not certified for industrial control, electrical safety, billing or operational decision-making.

## 2. Confirmed technology

| Area | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| UI | Tailwind CSS, shadcn/ui |
| Routing / API | React Router, Axios |
| Server state / charts | TanStack Query, Recharts |
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL; separate development, automated testing and production databases |
| ORM / driver | SQLAlchemy 2.x, Psycopg 3 |
| Migrations | Alembic |
| Messaging | Mosquitto MQTT broker / Paho MQTT client |
| Realtime | FastAPI WebSockets |
| Analytics | Pandas, NumPy |
| Reports | ReportLab, OpenPyXL |
| Testing | Pytest, HTTPX, frontend tests, Playwright |
| Hosting | Local Windows 11 first; then one Ubuntu AWS EC2 instance with Nginx and systemd |
| Version control | Git / GitHub |

Docker is excluded from the current scope. Local development uses native Windows tools/processes. Reconsider Docker only through an approved architecture decision.

## 3. Development workflow

- Windows 11; PyCharm for backend; VS Code for frontend.
- Project repository: `mini-ems`. Publication of governance files does not establish application readiness.
- **Stage A — local:** complete all application components and automated/manual integration testing with local PostgreSQL and Mosquitto, without AWS credentials or infrastructure.
- **Stage B — GitHub:** after complete local acceptance, review secrets/ignore rules, run required checks, update instructions and prepare a release-ready report for owner-controlled application upload.
- **Stage C — AWS:** only after owner approval of the local implementation and GitHub upload, separately approve provisioning and deployment to one Ubuntu EC2 instance for approximately 3–4 months.
- Hermes implements and runs automated checks from approved prompts.
- Project owner reviews plans/diffs and performs final manual smoke tests.
- Project owner alone performs Git commits, pushes, merges, tags and releases. Agents must not initialise Git or rewrite history.
- Deployment is separately approved and owner-controlled. Documentation approval does not authorise application implementation or infrastructure work.

## 4. Full product scope

1. Authentication and role-based access control.
2. Organisation and site management.
3. Device and energy-meter management.
4. Python meter simulator and MQTT communication.
5. Real-time monitoring dashboard.
6. Historical energy analytics.
7. Alarm and event management.
8. PDF, Excel and CSV reporting.
9. Administration and configuration.
10. Cloud deployment, health checks and operational logging.

Initial fictional demo data: one organisation, three sites, nine simulated meters and six equipment units.

## 5. Planned architecture

```text
Local Windows 11:
Browser ← React/Vite; Browser ← HTTP / WebSocket → FastAPI → local PostgreSQL
Python simulator → local Mosquitto → telemetry consumer → local PostgreSQL
Automated tests → separate local testing PostgreSQL database

Production — all hosted on one Ubuntu EC2 instance:
Browser → HTTPS / WSS → Nginx ─┬─ React production static files
                             └─ FastAPI API / WebSocket proxy → PostgreSQL
Python simulator → Mosquitto → telemetry consumer → PostgreSQL
Telemetry consumer → [delivery design pending] → FastAPI WebSocket clients
systemd manages long-running services
```

Mosquitto is selected. Local development may use a restricted local broker without production TLS configuration. Production must use MQTT authentication, restricted network access and appropriate TLS security with certificate verification. Keep broker configurations and credentials separate.

The consumer-to-WebSocket delivery mechanism and exact process topology remain unresolved; a shared host does not share process memory. Approve this design before the ingestion/realtime implementation without silently adding infrastructure dependencies. See [architecture](docs/03-architecture.md) and [ADR-007](docs/13-decisions-log.md#adr-007--local-first-development-and-temporary-single-ec2-hosting).

Nginx serves the production React build and proxies API/WebSocket traffic. Keep the API, PostgreSQL and broker listeners restricted; the browser never connects to PostgreSQL. Persistent data stays outside replaceable application releases and requires verified backups.

## 6. Repository structure

Phase 1 implements the backend and frontend foundations. `simulator/` and `mqtt/` arrive in their own milestones.

```text
mini-ems/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # root + health routers
│   │   ├── core/            # settings, fail-closed test database guard
│   │   └── db/              # session management, models/system_metadata
│   ├── alembic/             # env + one system_metadata migration
│   ├── tests/               # config, guard, API, DB-unavailable, migration, updated_at
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   ├── src/
│   │   ├── api/             # Axios client + health calls
│   │   ├── hooks/           # TanStack Query health hooks
│   │   ├── components/      # StatusCard
│   │   ├── pages/           # StatusPage
│   │   └── *.test.tsx       # Vitest + React Testing Library
│   ├── package.json
│   └── package-lock.json
├── .github/workflows/ci.yml
├── docs/
├── AGENTS.md
├── CHANGELOG-AI.md
├── .env.example
├── .gitignore
└── README.md
```


## 7. Local setup (verified)

Phase 1 runs entirely on Windows 11 with local PostgreSQL. No AWS credentials or infrastructure are required.

### 7.1 Prerequisites
- Git for Windows.
- Python 3.12.x (verified with 3.12.14). [uv](https://docs.astral.sh/uv/) manages the Python version and locked backend dependencies.
- Node.js 24 LTS (verified with 24.20.0) and npm (verified with 11.19.0); nvm-windows may manage the Node version.
- PostgreSQL 17 (verified with 17.12), reachable at `localhost:5432`. On Windows it was installed with Chocolatey (`choco install postgresql17`); any native PostgreSQL 17 install works. Docker is not used.

### 7.2 PostgreSQL databases and roles
Create separate development and testing databases with dedicated restricted roles (run once as a PostgreSQL superuser via `psql`). Choose strong private passwords; never commit them.

```sql
CREATE ROLE mini_ems_dev LOGIN PASSWORD '<dev-password>' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE ROLE mini_ems_test LOGIN PASSWORD '<test-password>' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE DATABASE mini_ems_dev OWNER mini_ems_dev;
CREATE DATABASE mini_ems_test OWNER mini_ems_test;
REVOKE ALL ON DATABASE mini_ems_dev FROM PUBLIC;
REVOKE ALL ON DATABASE mini_ems_test FROM PUBLIC;
REVOKE ALL ON DATABASE mini_ems_dev FROM mini_ems_test;
REVOKE ALL ON DATABASE mini_ems_test FROM mini_ems_dev;
```

The test role has no CONNECT privilege on the development (or production) database, so automated tests cannot reach development data. Production uses a third separate database created at Stage C.

### 7.3 Backend
```powershell
cd backend
uv sync --frozen --extra dev   # Python 3.12 env + locked dependencies from uv.lock
```
Create `backend/.env` (ignored) using the root `.env.example` contract:
```
APP_ENV=development
DATABASE_URL=postgresql+psycopg://mini_ems_dev:<dev-password>@localhost:5432/mini_ems_dev
FRONTEND_URL=http://localhost:5173
API_HOST=127.0.0.1
API_PORT=8000
```
Apply the schema migration, then start the API:
```powershell
uv run alembic upgrade head
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 7.4 Frontend
```powershell
cd frontend
npm ci
```
Create `frontend/.env` (ignored) from `frontend/.env.example`:
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```
Start the dev server:
```powershell
npm run dev
```

### 7.5 Local URLs
Frontend `http://localhost:5173`, backend `http://localhost:8000`, Swagger `http://localhost:8000/docs`. The frontend reads the public build-time `VITE_API_BASE_URL` and normalizes it so `/api/v1` is never appended twice.


## 8. Environment and secrets

Root `.env.example` is the planned environment-variable contract. Settings loaders are not implemented; commented frontend, test, MQTT and simulator additions are assigned to future milestones. Actual values belong in separate ignored local/test configurations and protected production environment files outside the checkout and web root. Supply each process only its own settings.

Never commit real connection strings, database passwords, JWT signing keys or private credentials. `VITE_*` variables are exposed to browser users and must never contain secrets. `VITE_API_BASE_URL` is a planned public build-time API base including `/api/v1`; changing environments may rebuild the same source without code rewrites. MQTT endpoints/security and simulator identity/publishing interval are independently configurable. Do not reuse the More Supermarket Mega database.

Use Alembic for application schema changes; do not rely on manually created production tables. Keep environment-specific addresses and AWS dependencies out of business logic. See [environment and deployment](docs/12-environment-deployment.md) for variable ownership and local/production security rules.

## 9. Testing and CI (verified)

Automated tests never modify development or production data. The backend test bootstrap runs a fail-closed guard that validates `APP_ENV=testing`, the test URL, the expected host (`TEST_DATABASE_HOST`), port, database name and role before connecting, then verifies `current_database()`/`current_user`. It never falls back to `DATABASE_URL`.

Local test configuration lives in root `.env.testing` (ignored): `APP_ENV=testing`, `TEST_DATABASE_HOST=localhost`, `TEST_DATABASE=mini_ems_test@localhost:5432/mini_ems_test`, and `TEST_DATABASE_PASSWORD=<test-password>` (exported as `PGPASSWORD`).

Backend (from `backend/`, with the test environment loaded):
```powershell
uv run ruff check .    # lint — passed
uv run pytest          # 29 tests passed
```
Frontend (from `frontend/`):
```powershell
npm run lint           # ESLint — passed
npm run typecheck      # tsc -b — passed
npm test               # Vitest + React Testing Library — 17 tests passed
npm run build          # tsc -b && vite build — passed
```
Backend tests cover settings, the database guard (including host validation, dev/prod target rejection, mocked connection failure and live identity mismatch), the three API contracts, database-unavailable 503 behaviour, migration schema and `updated_at` on update. Component tests mock API responses; the local smoke test uses the real backend.

### CI workflow
`.github/workflows/ci.yml` defines two jobs on GitHub-hosted Ubuntu runners:
- **backend:** installs PostgreSQL natively via apt (no Docker), creates a dedicated CI database + restricted role with a generated, masked password, sets up Python 3.12 via uv, runs `uv sync --frozen --extra dev`, then Ruff and pytest under the test guard.
- **frontend:** sets up Node 24, runs `npm ci`, then ESLint, type-check, tests and production build.

The workflow runs only after the owner publishes the repository (Stage B). It was reviewed and its commands validated locally; remote CI has not been executed. No AWS or production credentials are used.


## 10. Deployment

- Follow Stage A local-first → Stage B owner-controlled GitHub upload → Stage C separately approved AWS deployment. Do not deploy during Phase 1.
- One Ubuntu EC2 instance hosts Nginx, React static files, FastAPI, PostgreSQL, Mosquitto, simulator and required supporting processes. Use systemd for long-running services and Nginx for HTTPS/API/WebSocket routing.
- Prepare service start/stop/restart, backup/restore, certificate renewal, logging, migration and recovery procedures before deployment acceptance. Validate restore against an isolated recovery database; an on-host backup alone does not protect against host loss.
- Complete the local application first, then measure actual CPU, RAM, disk and database usage under the simulated workload, including dashboards and reports. Prepare a separate AWS resource recommendation before Stage C; do not select an EC2 instance type or make cost claims now.
- The owner verifies AWS account eligibility, credits and costs before provisioning. Free Tier is not assumed unlimited or permanently free. Intended hosting duration is approximately 3–4 months.
- Docker is excluded. No RDS, ECS, EKS, Lambda or other additional AWS services without owner approval and an ADR.

Bound data generation, polling, memory, queries and logs; define indexes and approve retention from actual workload evidence. This single-host architecture has a shared failure domain and no high-availability guarantee. The deployment runbook contains planned command templates, not evidence of an executed deployment.

## 11. Current status

| Area | Status |
|---|---|
| Product scope and technology | Defined; all features preserved |
| AI governance / hosting documents | Aligned with ADR-007 |
| Phase 1 foundation (backend + frontend + CI) | Implemented and verified locally (Stage A) |
| Authentication / devices | Not started |
| Simulator / MQTT / ingestion | Not started |
| Dashboard / analytics / alarms | Not started |
| Reports | Not started |
| Cloud deployment | Planned; separate approval after local acceptance, GitHub upload and measured resource recommendation |

### Known limitations (Phase 1)
- Foundation only: no auth/RBAC, organisations/sites/devices, MQTT, simulator, telemetry, WebSockets, dashboards, analytics, alarms or reports yet.
- The frontend is a minimal health/status interface. shadcn/ui, Recharts and Playwright end-to-end tests are deferred to the dashboard/analytics/E2E milestones.
- Consumer-to-WebSocket delivery/process topology remains unresolved until its own design approval.
- Single-host architecture has a shared failure domain and no high-availability guarantee; AWS deployment is not provisioned.
- Remote GitHub Actions CI has not been executed (owner publishes in Stage B).


## 12. Revised effort estimate

Hermes-assisted planning estimate: **65–100 active project hours**, including prompt/review/verification cycles. Indicative calendar: **6–10 weeks** at a few focused hours on most days. This excludes provider delays and major unexpected rework. See `docs/02-roadmap.md`.

These inherited effort estimates are provisional and have not been revalidated for local service administration and the single-EC2 deployment. They are not AWS sizing or cost claims.

## 13. AI-assisted development

Agents must read `AGENTS.md`, `docs/00-ai-rules.md`, product spec, architecture, current sprint and relevant contracts before acting. Required workflow: inspect → plan → wait for approval → implement → test → report.

Do not invent requirements, APIs, fields, environment variables, credentials or files. The project owner controls all Git and deployment actions.

## 14. License and disclaimer

Choose a license before publishing as open source. Mini EMS is a simulated educational/portfolio prototype, not a certified industrial monitoring/control product.
