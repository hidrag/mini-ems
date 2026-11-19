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

These inherited estimates are provisional and have not been revalidated for local service administration and the single-EC2 deployment. They are not AWS capacity or cost estimates. Re-estimate the affected work after local verification rather than treating this table as a deployment commitment.

## Milestones
- M1 Foundation: backend, frontend, separate local development/test PostgreSQL databases, migrations, health checks, local checks, CI preparation and docs. Preserve the existing repository; agents must not initialise Git.
- M2 Identity/devices: auth, RBAC, organisations, sites, device registry, tenant isolation.
- M3 Simulator/MQTT: meter models, scenarios, local Mosquitto, Paho MQTT publishing/subscribing, heartbeat/faults and independently configurable simulator. Local TLS need not mirror production; document separate broker security profiles.
- M4 Ingestion: validation, idempotency, persistence, retry and telemetry queries.
- M5 Dashboard: React layout, site/device views, KPIs, charts, WebSockets.
- M6 Analytics/alarms: consumption, aggregation, rules, alarm lifecycle, events.
- M7 Reports/admin: PDF/Excel/CSV, settings, audit logs, simulator controls.
- M8 QA/deployment: complete local security/E2E and manual integration testing, measure actual resource usage, prepare release/operations documentation, owner-controlled GitHub upload, then separately approved single-EC2 deployment and smoke tests.

## Mandatory delivery stages
### Stage A — complete local application
Run M1–M7 and M8 local QA on Windows 11 using local PostgreSQL and Mosquitto, without AWS credentials or infrastructure. Preserve every approved product feature. Automated tests use a dedicated testing PostgreSQL database and must never modify development or production data.

After the complete local application works, measure CPU, RAM, disk and database usage under the simulated workload, including ingestion, dashboards and reports. Record publishing rates, retention assumptions and observed growth. No EC2 instance type selection or cost claims at this stage. Prepare the measured AWS resource recommendation before Stage C.

### Stage B — GitHub readiness and owner upload
Require complete local acceptance, required test results, manual integration evidence, `.gitignore`/secret review, updated README/deployment instructions and a release-ready report. Only the owner commits, pushes, merges and tags. Governance files already present in Git/GitHub do not represent a completed application release and do not bypass this gate. CI configuration may be prepared locally; remote execution is verified when the owner uploads the accepted application.

### Stage C — separately approved AWS deployment
After owner approval of the local implementation and GitHub upload, review the resource recommendation, account eligibility, credits and costs before provisioning. Use one Ubuntu EC2 instance for approximately 3–4 months with Nginx, React static files, FastAPI, PostgreSQL, Mosquitto, simulator and required supporting processes. Configure systemd, HTTPS, MQTT authentication/restricted access/TLS, backups, restore, restart/reboot recovery and deployment smoke tests. Docker is excluded; additional AWS services require explicit approval.

## Milestone gate
Inspect → plan → wait for approval → implement → test → report → owner smoke test and acceptance. Do not start the next milestone before acceptance. Owner-controlled local commits do not authorise application upload before Stage B or deployment before Stage C. Agents never commit, push, merge, tag or initialise Git.

The hosting documentation update does not start M1 implementation. Consumer-to-WebSocket delivery remains subject to design approval; do not add infrastructure dependencies implicitly.
