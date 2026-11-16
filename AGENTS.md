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
The human project owner is final authority for requirements, architecture and acceptance. The owner performs all commits, pushes, merges, tags and deployments. Never perform them without explicit current-task authorisation.

Never run `git reset --hard`, force-push, rewrite history, delete branches or discard uncommitted work.

## Scope boundaries
- Implement only approved task/milestone scope.
- Do not change unrelated features or implement future milestones opportunistically.
- Do not invent routes, fields, packages, roles, services, env vars, credentials or configuration.
- Do not modify More Supermarket Mega or any other project.
- Docker is excluded unless the owner explicitly changes the decision.
- Frontend must never connect directly to Neon.
- Never expose secrets in code, logs, prompts, screenshots or documentation.

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
- Mini EMS uses its own dedicated Neon project/database.
- Never use the More Supermarket Mega database.
- No DROP, TRUNCATE, reset or destructive migration without explicit approval.
- Use isolated test data/test database for integration tests.

## Required workflow
`inspect → plan → wait for approval → implement → test → report`

Architectural changes require an ADR in `docs/13-decisions-log.md` and owner approval.

## Final report
Report scope, initial state, files changed, decisions, tests actually run, tests not run, risks, smoke-test steps, Git status and confirmation that no commit/push occurred.
