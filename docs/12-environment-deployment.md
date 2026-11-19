# 12 — Environment and Deployment

## Status and mandatory sequence
This is a planned runbook, not evidence of installed infrastructure or a working application. The current task changes documentation only. Stage A local-first development → Stage B owner-controlled GitHub upload → Stage C separately approved AWS deployment is mandatory. Existing governance files in Git/GitHub do not establish application readiness.

The approved target is one Ubuntu EC2 instance for approximately 3–4 months. Docker is excluded. RDS, ECS, EKS, Lambda and other additional AWS services require future owner approval and an ADR. See ADR-007 in `13-decisions-log.md`.

## Stage A — local development and acceptance
1. Use native Windows 11 tools: Git for Windows, Python with a venv under `backend/.venv/`, Node/npm under `frontend/`, local PostgreSQL and local Mosquitto. Pin compatible versions and verify actual commands during the relevant implementation milestone.
2. Maintain dedicated, separate local development and automated testing PostgreSQL databases and credentials. Production is a third separate database on EC2 in Stage C. Never use another project's database or substitute SQLite.
3. Configure the API, frontend, consumer and simulator from environment variables. No AWS credentials, SDK dependency in business logic or provisioned AWS resources are required for local execution.
4. Run locally configured Mosquitto on a restricted local listener. Local development may omit production TLS configuration. Keep its configuration/credentials separate from production.
5. Implement and test all approved features through their milestone gates. Use Alembic for application schema changes; database/role provisioning is separate from table creation.
6. Complete automated tests and owner manual integration testing. Tests must never modify development or production data, including indirect writes through API/consumer processes. Reject missing/unsafe test targets before migrations, fixtures or cleanup. Isolate test MQTT traffic from development consumers.
7. Keep local setup reproducible: document each process's working directory, environment source, prerequisites, verified start/stop commands and dependency order when implemented. Do not claim the commands exist before the entry points/manifests do.
8. After the complete local application works, measure CPU, RAM, disk and database usage under the simulated workload as described below. Record the evidence for the resource recommendation required before Stage C.

Phase 1 still excludes MQTT, simulator and the later application modules; these prerequisites are introduced at their respective milestones. Local acceptance does not require production TLS certificates or an AWS account.

## Environment contract and ownership
Root `.env.example` is the authoritative planned variable inventory. There are no settings loaders yet. Existing backend names are retained; commented additions define future configuration for the named milestone. Implementation must add validation, loading and tests together with these docs. JWT variable names remain deferred to authentication design.

| Variables | Consumer / meaning | Milestone and environment rules |
|---|---|---|
| `APP_NAME`, `APP_ENV`, `APP_DEBUG` | Backend application identity/mode | Phase 1. Development examples are not production defaults; production uses `APP_ENV=production` and `APP_DEBUG=false`. |
| `DATABASE_URL` | API and database-using consumer; reviewed migration configuration | Phase 1 onward. Supply only the target environment's PostgreSQL connection. Never send it to the browser or simulator. |
| `TEST_DATABASE_URL` | Automated test bootstrap | Planned Phase 1. Required explicit testing database; no fallback to `DATABASE_URL`. Before starting a test API/consumer, inject only the verified test connection into its database setting. |
| `FRONTEND_URL` | Backend approved frontend origin | Phase 1. Local example is `http://localhost:5173`; production uses the actual approved HTTPS origin. Do not use a wildcard credentialed origin. |
| `VITE_API_BASE_URL` | Public frontend build-time API base | Planned Phase 1. Includes `/api/v1`; client paths must not repeat the prefix. Local example is `http://localhost:8000/api/v1`; production may use same-origin `/api/v1`. Changing it requires rebuilding the same frontend source. |
| `MQTT_HOST`, `MQTT_PORT` | Consumer and simulator broker connection | Planned MQTT milestone. Each process loads its own settings. `localhost`/`1883` are local examples only; use the separately configured production TLS listener. |
| `MQTT_TLS_ENABLED`, `MQTT_TLS_CA_FILE` | Consumer and simulator TLS verification | Planned MQTT milestone. Local TLS may be disabled. Production enables verified TLS and uses an approved CA file or the system trust store; never disable certificate verification. |
| `MQTT_USERNAME`, `MQTT_PASSWORD` | Per-process MQTT credentials | Planned MQTT milestone. Match local broker policy; production authentication is mandatory. Keep publisher/consumer privileges limited to approved topics. |
| `MQTT_CLIENT_ID` | Broker client identity for each process | Planned MQTT milestone. Use distinct configurable IDs to avoid one connection displacing another. Simulator identity is independent from API/consumer configuration. |
| `SIMULATOR_PUBLISH_INTERVAL_SECONDS` | Simulator publishing cadence | Planned simulator milestone. Validate a positive interval; choose it with the measurement model and later resource evidence. No numerical production rate is selected here. |

Rules:
- Keep local development, automated testing and production settings separate. Use ignored environment files locally; do not source the root example wholesale into every process. Exact file-loading conventions are verified when implemented.
- Store production environment files outside the Git checkout and Nginx document root, with restricted service-account permissions. Use systemd environment loading; do not put secret values into unit files committed to Git, shell command arguments or logs.
- Vite `VITE_*` variables are public build output. Never include database/MQTT credentials, JWT keys or other backend secrets in them.
- No hardcoded environment-specific hostnames, IP addresses, production URLs or connection strings in application code. Development examples do not become production defaults.
- PostgreSQL transport security and authentication must match the actual listener/host policy. The local example does not require a hosted-provider SSL setup; document production connection protection explicitly during deployment rather than blindly reusing it.
- Separate local and production Mosquitto listener/authentication/TLS configuration. Simulator configuration must remain independent from the API; it needs broker credentials, not database access.

## Stage B — release-ready GitHub handoff
Only after the complete application passes local automated tests and owner manual integration testing:
1. Run the required checks and record exact commands, working directories, results and unrun checks.
2. Review `.gitignore` and tracked files for secrets, `.env` files, PostgreSQL data/backups, Mosquitto persistence/credentials, logs and temporary/generated files. Ignore rules do not remove already tracked content.
3. Keep database data outside the checkout. Put any temporary local database dumps in ignored `backups/`; plain SQL migrations must remain trackable. Production backups do not belong in Git.
4. Update README, environment contract, verified local instructions and the planned deployment/operations runbook. Record outstanding deployment decisions and resource measurements in the release-ready report.
5. The owner alone performs commits, pushes, merges and tags. Agents must not initialise Git. Verify the uploaded application and any remote CI at this gate; preparing CI earlier does not authorise early application upload.

## AWS resource recommendation — required before Stage C
Do not select an EC2 instance type or make cost claims now. First complete the local application, then measure its actual CPU, RAM, disk and database usage under the approved simulated workload: one organisation, three sites, nine meters and six equipment units.

Record the local machine/runtime baseline, measurement tools, observation duration, simulator publishing intervals, concurrent dashboard users, report workloads and database size at the start/end. Capture steady and peak CPU, per-process and total RAM, disk usage/I/O, database/index growth, query behaviour, connection usage and log/backup growth. Avoid uncontrolled generation; agree on workload and observation bounds before running it.

Prepare a separate recommendation from those observations before Stage C. State capacity headroom, retention assumptions, backup space, shared-host/reporting peaks and Windows-to-Ubuntu limitations; local measurements inform sizing but do not guarantee identical production behaviour. Do not populate this document with invented usage or estimates. The owner reviews the recommendation and verifies AWS account eligibility, credits and actual expected costs before provisioning. Free Tier is not assumed unlimited or permanently free.

## Stage C — separately approved deployment
Entry requires owner acceptance of the complete local application and GitHub upload, a reviewed resource recommendation, and explicit deployment approval. Domain/certificate arrangements, Ubuntu/runtime versions, storage, backup destination/policy and service definitions must be resolved for the deployment task. No provisioning or installation occurs during documentation alignment.

Planned sequence:
1. Provision the approved EC2 instance and configure Ubuntu, least-privilege administrative access, system packages and security group/host firewall rules. Do not add an AWS service without approval.
2. Configure dedicated production PostgreSQL and Mosquitto, data locations outside replaceable releases, restricted listeners and credentials. Production MQTT requires authentication, topic permissions, restricted network access and appropriate verified TLS.
3. Deploy the owner-approved revision from GitHub. Create the Python environment and install pinned dependencies; build React with the approved public API base URL. Keep production secrets outside the checkout and static assets.
4. Confirm the production database target, review migration impact and backup/recovery readiness, then apply Alembic. Never create application tables manually; do not run the automated test suite against production.
5. Configure systemd units for application processes using verified entry points, working directories, environment files and service users. Define readiness/reconnect behaviour, graceful shutdown and bounded restart policies without spawning duplicate consumers or simulators.
6. Configure Nginx to serve React static files with client-side route fallback, reverse-proxy `/api/v1` to FastAPI and support the approved WebSocket route/upgrades. Do not let the SPA fallback mask API errors. Do not run the Vite development server in production.
7. Configure HTTPS/WSS, certificate renewal, restricted administrative sources and private API/database/broker listeners. Verify approved origins, forwarded headers, timeouts and secret-free logs. Local TLS settings are not production settings.
8. Run the approved smoke tests in `10-testing-strategy.md`, validate service restart/reboot and isolated backup restoration, and record the results before owner deployment acceptance.

Consumer-to-WebSocket delivery remains an unresolved design dependency for the ingestion/realtime milestones. Do not deploy an assumed in-memory cross-process broadcast or add another infrastructure service silently.

## Service operations — templates to verify in Stage C
The following roles must each have a recorded unit name, service user, configuration path, dependencies and verified operational commands. Names and application entry points are not yet selected; placeholders below are not runnable instructions as written.

| Service role | Unit placeholder to replace with the verified installed unit | Operational check |
|---|---|---|
| Nginx | `<NGINX_UNIT>` | Validate configuration with `sudo nginx -t` before reload/restart; verify HTTPS, assets, API and WebSocket proxying. |
| PostgreSQL | `<POSTGRESQL_UNIT>` | Identify the unit controlling the actual database cluster, not just a meta-unit; confirm the target and dependent writes before maintenance. |
| Mosquitto | `<MOSQUITTO_UNIT>` | Check the installed version's configuration-validation procedure; verify authenticated TLS reconnects and restricted listeners. |
| FastAPI | `<API_UNIT>` | Verify the approved health endpoints and WebSocket reconnect behaviour. |
| Telemetry consumer, if a separate process | `<CONSUMER_UNIT>` | Confirm one intended consumer, broker subscription, persistence and approved notification delivery. |
| Python simulator | `<SIMULATOR_UNIT>` | Confirm independent settings, publishing cadence and no duplicate publisher. |

For **each** verified unit above, document and exercise these systemd operations during the approved deployment task:
```text
sudo systemctl status <VERIFIED_UNIT>
sudo systemctl start <VERIFIED_UNIT>
sudo systemctl stop <VERIFIED_UNIT>
sudo systemctl restart <VERIFIED_UNIT>
sudo journalctl -u <VERIFIED_UNIT> --since "15 minutes ago" --no-pager
```

Verify startup enablement and dependency/readiness behaviour at reboot. Start PostgreSQL/Mosquitto before dependent application processes, then enable user traffic after health checks. For maintenance, stop or pause simulator generation, drain consumers as supported, prevent new writes and stop dependent application processes before stopping database/broker services. Document the final order from the implemented topology. A successful service restart alone is not an application smoke test.

## PostgreSQL backup and restore — planned procedure
Approve backup frequency, retention, recovery point/time objectives, encryption/access controls and an off-instance destination before production acceptance. The destination is unresolved; this does not authorise adding another AWS service. Do not treat persistent disk or an on-host dump as protection against loss of the EC2 host.

Backup:
1. Confirm the source host/database and authorisation before connecting. Use a suitable PostgreSQL client version and a restricted account; supply credentials securely, never inline in commands or logs.
2. Use `pg_dump` to create a logical custom-format backup in a protected path, recording timestamp, source identity, schema/migration revision and tool versions. Example template, to be verified for the approved environment:
   ```text
   pg_dump --host="<CONFIRMED_HOST>" --port="<CONFIRMED_PORT>" --username="<BACKUP_ROLE>" --dbname="<CONFIRMED_SOURCE_DB>" --format=custom --file="<PROTECTED_BACKUP_PATH>"
   pg_restore --list "<PROTECTED_BACKUP_PATH>"
   ```
3. Check exit results and backup integrity, secure the approved off-instance copy and record its verification. A readable archive listing is not proof of a successful restore.
4. Record required roles/permissions and protect service configuration and credentials separately; a database dump alone does not recreate the host. Backups are sensitive and must not enter Git or public reports.

Restore rehearsal:
1. Confirm a separately provisioned, empty and isolated recovery database and restricted restore role. Never overwrite local development or production data. Creation of a recovery target requires an approved database operation.
2. Inspect archive compatibility and restore into that target using securely supplied credentials. Example template:
   ```text
   pg_restore --host="<CONFIRMED_RECOVERY_HOST>" --port="<CONFIRMED_PORT>" --username="<RESTORE_ROLE>" --dbname="<CONFIRMED_EMPTY_RECOVERY_DB>" --no-owner --no-privileges --exit-on-error "<PROTECTED_BACKUP_PATH>"
   ```
3. Because ownership/privileges are not restored by this template, apply the reviewed target-role permissions separately. Verify schema/Alembic revision, representative row counts, integrity and application reads using isolated recovery configuration. Do not connect recovery consumers to production telemetry.
4. Record actual restore results and recovery time. Production recovery/cutover requires a separate owner-approved incident plan with confirmed target, write control and rollback path; do not automate destructive replacement from these templates.

No backup/restore command in this document was executed during documentation alignment.

## Logs, retention, rollback and end of hosting
- Keep application/system logs useful and secret-free; rotate logs, bound retention and monitor disk growth. Approve data retention before any deletion. Avoid excessive polling, unnecessary processes and unbounded in-memory telemetry/report accumulation.
- Record the deployed revision and configuration references without secrets. Application rollback requires a compatible database schema; do not assume reversing a migration is safe. Any restore or destructive migration requires explicit approval.
- At the end of approximately 3–4 months, the owner decides whether to extend hosting or retire it. Before an approved shutdown, preserve and verify required backups/exports, document restoration and stop generation. Resource deletion and credential retirement require their own approval; this documentation task authorises neither.

## Unresolved decisions
Consumer-to-WebSocket delivery/process count; exact runtime and frontend test-tool versions; workload intervals and retention; backup schedule/destination and recovery objectives; domain/certificate renewal arrangement; and resource selection based on completed-local-application measurements. Resolve these at the appropriate milestone before depending on them. No application command, infrastructure installation or deployment is claimed as verified here.
