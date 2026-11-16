# 02 — Roadmap and Revised Estimate

## Hermes-assisted delivery model
Hermes performs implementation, automated tests, debugging, linting and documentation from approved prompts. The owner defines requirements, reviews plans/diffs, performs final manual smoke tests and controls Git. ChatGPT supplies architecture, prompts, reviews and acceptance guidance.

## Revised effort estimate
The earlier 133–190 hours assumed largely manual implementation. Revised planning estimate:

| Workstream | Active project hours |
|---|---:|
| M1 Foundation | 5–8 |
| M2 Identity, tenancy, devices | 8–12 |
| M3 Simulator and MQTT | 9–14 |
| M4 Ingestion and persistence | 7–11 |
| M5 React monitoring dashboard | 10–15 |
| M6 Analytics and alarms | 9–13 |
| M7 Reporting and administration | 6–9 |
| M8 QA, deployment, documentation | 11–18 |
| **Total** | **65–100** |

These are active project hours including prompt/review/verification cycles, not guaranteed agent execution time. Excludes provider delays and major rework. Indicative calendar: 6–10 weeks at 2–3 focused hours on most days.

## Milestones
- M1 Foundation: repo, backend, frontend, Neon, migrations, health checks, CI, docs.
- M2 Identity/devices: auth, RBAC, organisations, sites, device registry, tenant isolation.
- M3 Simulator/MQTT: meter models, scenarios, publishing/subscribing, heartbeat/faults.
- M4 Ingestion: validation, idempotency, persistence, retry and telemetry queries.
- M5 Dashboard: React layout, site/device views, KPIs, charts, WebSockets.
- M6 Analytics/alarms: consumption, aggregation, rules, alarm lifecycle, events.
- M7 Reports/admin: PDF/Excel/CSV, settings, audit logs, simulator controls.
- M8 QA/deployment: security, E2E, Vercel/Render/Neon, operations docs and smoke tests.

## Gate
Inspect → plan → wait for approval → implement → test → report → owner smoke test → owner commit/push. Do not start the next milestone before acceptance.
