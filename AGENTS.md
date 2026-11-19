# AI Agent Instructions — Mini EMS

## Mandatory startup sequence
Before every task:
1. Read this file and `docs/00-ai-rules.md`.
2. Read `docs/01-product-specification.md`, `docs/03-architecture.md` and `docs/07-current-sprint.md`.
3. Read relevant API, database, security, testing and deployment documents.
4. Inspect current code, tests and Git status; verify prior agent claims.
5. Summarise current state, conflicts, assumptions and a file-level plan.
6. Wait for explicit owner approval before editing.

## Project owner authority
The human project owner is final authority for requirements, architecture and acceptance. Only the owner performs Git commits, pushes, merges, tags and releases. Agents must not initialise Git. Deployment requires a separate owner-approved Stage C task; documentation approval is not deployment approval.

Never run `git reset --hard`, force-push, rewrite history, delete branches or discard uncommitted work.

## Scope boundaries
- Implement only approved task/milestone scope.
- Do not change unrelated features or implement future milestones opportunistically.
- Do not invent routes, fields, packages, roles, services, env vars, credentials or configuration.
- Do not modify More Supermarket Mega or any other project.
- Docker is excluded unless the owner explicitly changes the decision.
- Frontend must never connect directly to PostgreSQL.
- Never expose secrets in code, logs, prompts, screenshots or documentation.

## Delivery and hosting boundaries
- Stage A: complete and test the application locally on Windows 11 using local PostgreSQL and Mosquitto, without AWS credentials or infrastructure.
- Stage B: after complete local acceptance, prepare the release report and GitHub upload; the owner controls all Git actions. Existing governance publication does not establish application readiness.
- Stage C: only after owner acceptance of the local application and GitHub upload, separately approve deployment to one Ubuntu AWS EC2 instance for approximately 3–4 months.
- The instance hosts Nginx, the React production build, FastAPI, PostgreSQL, Mosquitto, the simulator and required supporting application processes, managed with systemd where appropriate.
- Do not introduce RDS, ECS, EKS, Lambda or other additional AWS services without owner approval and an ADR.
- Local Mosquitto may run without production TLS configuration on a restricted local listener. Production requires MQTT authentication, restricted network access and appropriate TLS security. Keep broker configurations separate.
- Complete the local application and measure actual CPU, RAM, disk and database usage under the simulated workload before recommending AWS resources. Prepare the recommendation before Stage C; do not select an EC2 instance type or make cost claims now.
- Keep environment-specific settings out of application business logic. Do not silently add infrastructure to solve consumer-to-WebSocket delivery.

## Quality
- Python type hints; strict TypeScript.
- Validate external input.
- Use UTC-aware timestamps for persisted instants.
- Use migrations for schema changes.
- Add/update tests for behaviour changes.
- Run relevant lint, type, test and build checks.
- Report exact commands and actual outcomes; never claim unexecuted tests passed.
- Document meaningful functions/classes and non-obvious design decisions.

## Database safety
- Confirm target database before every database operation.
- Mini EMS uses dedicated PostgreSQL databases, separate for local development, automated testing and production, with separate credentials and restricted roles.
- Never use the More Supermarket Mega database.
- No DROP, TRUNCATE, reset or destructive migration without explicit approval.
- Automated tests must never modify development or production data. A separate schema in either database is not sufficient isolation.
- Test setup must reject missing or non-test database targets before any migration, fixture, write or cleanup. Never fall back to the development connection.
- Use Alembic for application schema changes; never rely on manually created production tables.

## Required workflow
`inspect → plan → wait for approval → implement → test → report`

Architectural changes require an ADR in `docs/13-decisions-log.md` and owner approval.

Approval applies only to the named task. A documentation-only update does not authorise Phase 1 implementation, database operations, infrastructure installation or provisioning.

## Final report
Report scope, initial state, files changed, decisions, tests actually run, tests not run, risks, smoke-test steps, Git status and confirmation that no commit/push occurred.
