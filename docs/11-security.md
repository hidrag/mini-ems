# 11 — Security Requirements

## Secrets
- Never commit `.env`, credentials, tokens or private keys.
- `.env.example` contains placeholders only.
- Redact secrets from logs/reports.
- Vite `VITE_*` variables are public.
- Store production secrets in protected environment files outside the Git checkout and Nginx document root. Restrict ownership/read access to the necessary service accounts; systemd supplies only each service's required settings.
- Separate development, automated testing and production credentials. Never copy local no-TLS/debug settings into production or expose backend secrets to the frontend build.

## Identity and access
- Backend is authoritative.
- Enforce role and tenant/site access on every protected operation.
- Test cross-tenant denial.
- Hash passwords with a maintained algorithm/library.
- Document token expiry/revocation.
- Never trust client-supplied role or tenant IDs.

## Input and network
- Validate API and MQTT input.
- Bound payload sizes.
- Use parameterised queries/ORM.
- Protect against duplicate/replayed telemetry.
- Handle malformed messages without crashing consumers.
- Production HTTP/WebSocket traffic uses HTTPS/WSS through Nginx. Configure trusted proxy handling, WebSocket upgrades and security headers during Stage C.
- No anonymous public MQTT broker.
- Restrict CORS to approved origins.

## MQTT environment separation
- Local development may use a locally configured Mosquitto broker without production TLS configuration. Restrict it to loopback by default; do not expose anonymous development access publicly or copy production credentials locally.
- Production must require MQTT authentication, restricted network access and appropriate TLS security with certificate verification. Use topic permissions and distinct publisher/consumer identities with only the required access.
- Keep local and production Mosquitto configuration, credential files, listeners and certificates separate. The simulator and consumer receive their own settings independently.
- Local no-TLS success does not satisfy production security acceptance. Test authentication rejection, certificate validation and network restrictions at the deployment gate.

## Database and test isolation
- Maintain separate dedicated PostgreSQL databases and restricted credentials for local development, automated testing and production; never use another project's database.
- Automated tests must never modify development or production data. Reject missing/unsafe test targets before migrations, fixtures, API writes, telemetry ingestion or cleanup; no development connection fallback.
- A separate schema in a protected database is insufficient. Test credentials must not provide write access to development or production databases; isolate test MQTT traffic from development consumers.
- Use Alembic for application schema changes. Confirm every target, review migrations and require explicit approval for destructive operations.
- Protect backups as sensitive data and validate restores against an isolated recovery target. Define an approved off-instance copy; on-host backups alone do not protect against host loss.

## Operations
- Health endpoints reveal only necessary status.
- Logs must not contain passwords, JWTs, connection strings or unnecessary personal data.
- Review dependencies and provider permissions.
- Restrict administrative SSH access to approved sources; keep database, broker and FastAPI listeners private to required processes. Expose only approved web/certificate-validation traffic through security group and host firewall rules.
- Run application processes with least-privilege service users under systemd. Keep data outside replaceable release directories; configure bounded restart behaviour, log rotation and disk monitoring.
- Production debug mode must be off. Review OS/package updates, certificate renewal and recovery procedures before acceptance.
- Document backup/restore, service restart and reboot checks in `12-environment-deployment.md`.
- Local-first development → owner-controlled GitHub upload → separately approved AWS deployment is mandatory. No AWS credentials are needed for local operation; Docker is excluded and additional AWS services require approval.

The system is not safety-rated and must not control real equipment.
