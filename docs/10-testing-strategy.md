# 10 — Testing Strategy

Test behaviour, use deterministic data, isolate integration tests and report unexecuted checks honestly.

## Stage A — local checks and isolation
Run the complete application and checks locally on Windows 11 with PostgreSQL and Mosquitto, without AWS credentials or infrastructure. Test commands will be pinned alongside the implementation; there are no executable application tests in the documentation scaffold.

- Maintain separate local development, automated testing and production PostgreSQL databases and credentials. A separate schema in development or production is not sufficient.
- Automated tests must never modify development or production data, including through API calls, migration setup, fixtures, telemetry consumers or cleanup.
- The planned `TEST_DATABASE_URL` must explicitly identify the isolated test database. Missing configuration must fail closed; never fall back to `DATABASE_URL`. Validate target identity and restricted credentials before any write, and exercise rejection of non-test targets without connecting to or modifying protected data.
- Use test API/consumer/simulator processes configured only for test data. Isolate MQTT test traffic with a dedicated local broker instance or an approved topic/ACL separation that development consumers cannot ingest. Never publish automated-test telemetry into the development stream.
- Local MQTT integration tests may use locally configured Mosquitto without production TLS. Keep local and production broker configurations separate; do not treat local success as proof of production MQTT security.
- Exercise Alembic migrations against the dedicated test database, with only explicitly approved cleanup. No destructive operations against development, production or another project's database.

Backend:
- Unit tests for calculations/validation/services.
- API tests using HTTPX.
- Database integration and migration tests against the separate automated testing database.
- Auth/RBAC and tenant-isolation tests.
- MQTT publisher/consumer tests.
- Telemetry validation, duplicate and out-of-order tests.
- WebSocket tests.

Frontend:
- TypeScript checks.
- Component and API behaviour tests.
- Loading/error/empty-state tests.
- Role-aware UI tests.
- Production build.
- Playwright end-to-end tests.

Critical E2E:
simulator emits → Mosquitto receives → consumer validates → PostgreSQL persists → WebSocket broadcasts → React displays → threshold creates alarm → authorised operator acknowledges → history/report includes reading.

The owner performs manual smoke tests at each milestone. Stage A acceptance includes complete manual integration coverage; this is separate from permission to upload the completed application or deploy it.

Portability checks must exercise environment-based database/MQTT settings, an independently configured simulator and the frontend build-time API URL. Rebuild the same frontend source for the target URL; do not rewrite business logic for AWS. Verify local operation without AWS credentials. WebSocket tests must cover the eventual approved delivery design; no new infrastructure dependency is implied by this test plan.

After completing the local application, measure actual CPU, RAM, disk and database usage for the simulated workload, including steady ingestion, dashboard activity and report generation. Record simulator intervals, observation duration, data growth and peaks. Prepare a resource recommendation before Stage C; do not select an EC2 instance type or make cost claims now.

## Stage B — release readiness
After complete local acceptance, run the required suites, review `.gitignore` and secret exclusions, update reproducible setup/deployment documentation, and record exact results in the release-ready report. Only the owner commits, pushes, merges and tags the application to GitHub. Remote CI does not replace local acceptance.

## Stage C — deployment smoke tests
Run only during a separately approved deployment after owner acceptance of local implementation and GitHub upload:
- HTTPS frontend loads; React route refresh works; API routes return API errors rather than the SPA page; WebSocket upgrades/reconnects work through Nginx.
- The approved health endpoints report actual application/database status without exposing secrets. Apply reviewed migrations only after confirming the production target.
- MQTT authentication and topic permissions reject unauthorised clients; network rules prevent unintended public access; production TLS verifies the broker certificate. Validate separate production configuration rather than copying local no-TLS settings.
- Confirm service start, stop, restart and reboot recovery, startup dependencies, reconnect behaviour and absence of duplicate telemetry consumers/simulator instances.
- Verify backup restoration into a separate isolated recovery database with no development or production data overwritten. Record restored schema/data checks and the observed recovery time.
- Inspect application/system logs and resource usage under a bounded smoke workload. Any production write exercise must be explicitly approved and use identifiable simulated smoke data; never point the automated test suite at production.

## Verification reporting
For documentation-only work, check changed-file scope, links, architecture/ADR consistency, example environment contracts and ignore rules without running or inventing application tests. Preserve the product inventory and report pending runtime checks.

For every check report exact command, working directory, execution status, result and limitations. Never use destructive cleanup against shared/production data.
