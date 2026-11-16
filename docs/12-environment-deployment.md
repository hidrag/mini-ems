# 12 — Environment and Deployment

## Environments
Local: Windows 11 native processes. Preview/staging and production: Vercel frontend, Render backend, Neon database.

## Local tools
Python venv under `backend/.venv/`; Node/npm under `frontend/`. Docker is excluded.

## Environment contract
Root `.env.example` is authoritative. Define new variables in settings/code and docs together. Expected categories: app environment/debug, database URL, CORS/frontend origin, JWT settings when auth exists, MQTT host/port/TLS/auth when MQTT exists.

Never expose backend secrets through Vite variables.

## Hosting
- Vercel: React frontend.
- Render Web Service: FastAPI HTTP/WebSocket API.
- Render Background Worker or suitable host: long-running telemetry consumer/simulator if required.
- Neon: PostgreSQL.
- MQTT broker: provider/topology pending ADR.

## Render
Bind web service to `0.0.0.0` and platform `PORT`. Configure health checks. Do not assume local filesystem writes persist. Verify plan limitations, spin-down behaviour, worker availability and cost.

## Vercel
Set public API base URL separately for preview/production. Configure backend CORS for actual domains. Never place database credentials or signing secrets in frontend build variables.

## Neon
Dedicated Mini EMS project. Use SSL. Keep connection string backend-only. Evaluate pooled runtime connections and direct migration connections according to Neon guidance. Verify limits. No destructive migrations without owner approval.

Do not deploy during Phase 1. Deployment requires a separate approved task and verification.
