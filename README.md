# Mini EMS — Industrial Energy Monitoring & Management System

> A simulated industrial energy monitoring platform built with React, FastAPI, MQTT and Neon PostgreSQL.

**Status:** Planning / Phase 1 not yet implemented.  
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
| Database | Neon PostgreSQL |
| ORM / driver | SQLAlchemy 2.x, Psycopg 3 |
| Migrations | Alembic |
| Messaging | MQTT / Paho MQTT (broker selection pending) |
| Realtime | FastAPI WebSockets |
| Analytics | Pandas, NumPy |
| Reports | ReportLab, OpenPyXL |
| Testing | Pytest, HTTPX, frontend tests, Playwright |
| Hosting | Vercel frontend, Render backend, Neon database |
| Version control | Git / GitHub |

Docker is excluded from the current scope. Local development uses native Windows tools/processes. Reconsider Docker only through an approved architecture decision.

## 3. Development workflow

- Windows 11; PyCharm for backend; VS Code for frontend.
- New GitHub repository: `mini-ems`.
- Dedicated Neon project/database for Mini EMS.
- Develop locally first; deploy after local acceptance.
- Hermes implements and runs automated checks from approved prompts.
- Project owner reviews plans/diffs and performs final manual smoke tests.
- Project owner alone performs Git commits, pushes, merges and releases.
- Agents must not commit, push, merge, reset history or deploy without explicit approval.

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
React + TypeScript (Vercel)
          |
          | HTTPS / WebSocket
          v
FastAPI backend (Render)
          |
          +----------> Neon PostgreSQL
          |
          +----------> MQTT consumer / telemetry processing
                              ^
                              |
Python meter simulator ------+
                              |
                         MQTT broker
```

The MQTT broker and worker topology are not finalised. Do not assume the broker runs inside the FastAPI web service. Record and approve the broker decision before implementing deployment-specific networking.

Render supports Python/FastAPI web services and separate background workers. Free web services have limitations, including inactivity spin-down; background workers require paid compute. Verify current service limits and costs before deployment.

## 6. Repository structure

The repository grows incrementally. The Phase 1 structure is defined in `docs/07-current-sprint.md`.

```text
mini-ems/
├── backend/
├── frontend/
├── simulator/       # introduced in simulator milestone
├── mqtt/            # after broker selection
├── docs/
├── .github/
├── AGENTS.md
├── CHANGELOG-AI.md
├── .env.example
├── .gitignore
└── README.md
```

## 7. Local setup

Prerequisites: Git for Windows, Python 3.12+ (exact version pinned in Phase 1), Node.js LTS, PyCharm, VS Code, and a dedicated Neon database.

Backend setup (intended):

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Frontend setup (intended):

```powershell
cd frontend
npm install
npm run dev
```

Expected local URLs: frontend `http://localhost:5173`, backend `http://localhost:8000`, Swagger `http://localhost:8000/docs`.

Exact commands will be confirmed after Phase 1 implementation.

## 8. Environment and secrets

Root `.env.example` is the documented environment-variable contract. Actual values belong in ignored `.env` locally and provider environment settings in the cloud.

Never commit `DATABASE_URL`, database passwords, JWT signing keys or private credentials. `VITE_*` variables are exposed to browser users and must never contain secrets. Do not reuse the More Supermarket Mega database.

## 9. Testing

Planned checks include backend unit/API/database tests, migration tests, MQTT and telemetry integration tests, WebSocket tests, frontend type/build/component tests and end-to-end workflows. The project owner performs manual smoke tests before commits.

Never run destructive tests against shared or production data. Use a dedicated test database or isolated test schema.

## 10. Deployment

- Frontend: Vercel.
- FastAPI API: Render Web Service.
- Long-running telemetry consumer/simulator: evaluate Render Background Worker or another suitable worker host.
- Database: Neon PostgreSQL.
- MQTT broker: choose managed or private hosting after evaluating TLS, authentication, networking, availability and cost.

Do not rely on local filesystem persistence for important records.

## 11. Current status

| Area | Status |
|---|---|
| Product scope and technology | Defined |
| AI governance documents | Prepared |
| Phase 1 foundation | Not implemented |
| Authentication / devices | Not started |
| Simulator / MQTT / ingestion | Not started |
| Dashboard / analytics / alarms | Not started |
| Reports | Not started |
| Cloud deployment | Planned |

## 12. Revised effort estimate

Hermes-assisted planning estimate: **65–100 active project hours**, including prompt/review/verification cycles. Indicative calendar: **6–10 weeks** at a few focused hours on most days. This excludes provider delays and major unexpected rework. See `docs/02-roadmap.md`.

## 13. AI-assisted development

Agents must read `AGENTS.md`, `docs/00-ai-rules.md`, product spec, architecture, current sprint and relevant contracts before acting. Required workflow: inspect → plan → wait for approval → implement → test → report.

Do not invent requirements, APIs, fields, environment variables, credentials or files. The project owner controls all Git and deployment actions.

## 14. License and disclaimer

Choose a license before publishing as open source. Mini EMS is a simulated educational/portfolio prototype, not a certified industrial monitoring/control product.
