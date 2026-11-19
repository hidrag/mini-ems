# 03 — Architecture

## Confirmed hosting direction
- Stage A: complete and test all components locally on Windows 11 using native processes, local PostgreSQL and Mosquitto. No AWS credentials or infrastructure are required.
- Stage B: prepare the complete locally accepted application for GitHub; only the owner commits, pushes, merges and tags.
- Stage C: after acceptance of the local application and GitHub upload, separately approve one Ubuntu AWS EC2 instance for approximately 3–4 months.
- The instance hosts Nginx, the React production build, FastAPI, PostgreSQL, Mosquitto, the Python meter simulator and required supporting application processes. Use systemd for long-running services.
- Docker is excluded. No RDS, ECS, EKS, Lambda or other additional AWS services without owner approval and an ADR.
- ADR-007 in `13-decisions-log.md` records this decision. Product features and the simulated demo inventory are unchanged.

## Local logical architecture — planned
```text
Browser ← React/Vite development server
Browser ← HTTP / WebSocket → FastAPI → local development PostgreSQL
Simulator → local Mosquitto → telemetry consumer → local development PostgreSQL
Telemetry consumer → [delivery design pending] → FastAPI WebSocket clients

Automated test processes → separate local testing PostgreSQL database
```

The diagram shows responsibilities, not implemented services or an approved inter-process delivery mechanism. Local MQTT may use a loopback listener without production TLS configuration. Keep test telemetry isolated from development consumers as well as using a separate test database.

## Production topology — planned Stage C
```text
Browser → HTTPS / WSS → Nginx on one Ubuntu EC2 instance
                         ├─ React production static files / SPA fallback
                         └─ API and WebSocket reverse proxy → FastAPI → PostgreSQL

On the same EC2 instance:
Simulator → authenticated, restricted Mosquitto with TLS → telemetry consumer
Telemetry consumer → PostgreSQL
Telemetry consumer → [delivery design pending] → FastAPI WebSocket clients
systemd → Nginx, PostgreSQL, Mosquitto and approved application processes
```

Nginx is the public application entry point. Serve the built frontend, proxy the planned `/api/v1` API prefix, and support WebSocket upgrades at the eventual approved endpoint. Keep API errors out of the SPA fallback. Bind FastAPI, PostgreSQL and Mosquitto to restricted interfaces; do not expose their service ports publicly by default. Define the production domain, certificate arrangement and exact service units during the approved deployment task.

## Process responsibilities and unresolved delivery
- FastAPI handles HTTP, authorisation and WebSocket client sessions. Telemetry processing stays separate from browser request handling.
- The simulator publishes simulated readings through Paho MQTT to Mosquitto; the consumer validates and persists readings through SQLAlchemy/Psycopg 3.
- Running all processes on one host does not make their memory shared. A consumer cannot directly broadcast through another process's in-memory WebSocket connection registry.
- Consumer-to-API notification, reconnect recovery, process ownership and duplicate-consumer prevention remain open design decisions for the ingestion/realtime milestones. Resolve and approve them before implementation.
- Do not silently add Redis, another message bus, an AWS service or any infrastructure dependency to resolve this design. The number of API workers is also pending the approved delivery design and local measurements.

## Principles
- Frontend never connects directly to PostgreSQL.
- API is the application boundary.
- Telemetry processing is separate from browser request handling.
- MQTT is transport; PostgreSQL is the persistent system of record.
- WebSockets distribute updates, not replace stored history.
- Enforce device, organisation and site authorisation server-side.
- Persist UTC-aware timestamps.
- Handle duplicates, out-of-order messages and reconnects.
- Gracefully stop long-running processes.
- Keep database/broker data outside replaceable application release directories. A persistent EC2 disk is not a backup.

## Environment portability and isolation
- Use environment variables for credentials, database connections, origins, MQTT endpoints/security and simulator settings. Do not hardcode environment-specific hostnames, IPs or production URLs in application code.
- Maintain separate local development, automated testing and production PostgreSQL databases and credentials. Automated tests must never modify development or production data; reject unsafe targets before any write. Do not substitute SQLite or schema-only isolation.
- Use Alembic migrations for every application schema change. Do not manually create production tables.
- Keep the simulator configurable independently from the API, including its broker identity and publishing interval. Do not give it database credentials it does not need.
- Configure the frontend API base URL at build time. The same source may be rebuilt for production; public Vite configuration must contain no secrets.
- Keep local and production broker configurations separate. Production requires MQTT authentication, restricted network access and appropriate TLS security with certificate verification. Local operation need not reproduce production TLS.
- No AWS-specific dependencies belong in business logic. Native Windows commands and Ubuntu systemd operations may differ without changing application behaviour.
- `12-environment-deployment.md` defines the configuration, backup/restore and service operations requirements.

## Resource and reliability constraints
This is one shared failure domain, not a high-availability deployment. Database, API, reporting and simulator workloads compete for the same CPU, RAM and disk.

Bound simulator publishing intervals, retries, connection pools, query sizes, in-memory queues and report generation. Avoid excessive polling and unnecessary processes. Define indexes and retention from actual access patterns and data growth; rotate application/system logs and keep them free of secrets. Retention values and deletion procedures still require approval.

First complete the local application. Then measure actual CPU, RAM, disk and database usage under the simulated workload, including live ingestion, concurrent dashboard activity and report generation. Record workload settings, peaks, sustained usage and Windows-to-Ubuntu uncertainty. Prepare a separate AWS resource recommendation before Stage C using that evidence and explicit headroom/limitations. Do not select an EC2 instance type or make cost claims now. The owner verifies account eligibility, credits and costs before provisioning; do not assume Free Tier is unlimited or permanently free.

## Docker
Docker/Compose are excluded unless the owner explicitly reopens the decision through an ADR.
