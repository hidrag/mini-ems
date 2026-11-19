# 00 — AI Rules and Source-of-Truth Policy

## Source hierarchy
1. Current implementation and executable tests.
2. Approved contracts: database schema, API, auth/RBAC and environment.
3. Approved architecture and ADRs.
4. Current sprint acceptance criteria.
5. Product specification.
6. Roadmap.
7. README and informal notes.

Report contradictions; do not silently reconcile them.

The owner may approve a change to these sources. Record that decision and align the affected contracts and ADRs explicitly; historical provider decisions do not override the approved local-first strategy in ADR-007.

## Never invent
Do not invent routes, request/response fields, tables, columns, constraints, environment variables, credentials, packages, services, workers, broker capabilities, roles, permissions, device protocols, telemetry units, engineering thresholds, provider limits, pricing or files.

## Inspect and plan
Inspect code, tests, Git status and relevant docs before each task. Produce a file-level plan and wait for approval before editing.

## No silent scope expansion
Do not add features or replace approved technology without an ADR and owner approval.

## Delivery approval boundaries
- Stage A: complete local development and automated/manual integration testing on Windows 11 with local PostgreSQL and Mosquitto. AWS credentials and infrastructure are not prerequisites.
- Stage B: prepare the complete locally accepted application for owner-controlled GitHub upload, including secrets/ignore review, reproducible instructions and a release-ready report.
- Stage C: deploy to one Ubuntu EC2 instance only after the owner accepts the local implementation and GitHub upload and separately approves deployment.
- Documentation approval authorises documentation only, not application code, database operations, infrastructure installation or AWS provisioning.
- Preserve product scope and Docker exclusion. Additional AWS services and new infrastructure dependencies require explicit approval; do not silently resolve WebSocket delivery by adding one.
- Keep local development, automated testing and production PostgreSQL databases separate. Automated tests must never modify development or production data.
- Keep local and production MQTT configurations separate: local development need not reproduce production TLS, while production requires authentication, restricted access and appropriate TLS security.
- Complete the local application and measure CPU, RAM, disk and database usage before preparing the AWS resource recommendation, which is required before Stage C. No instance type selection or cost claims now.

## Truthful verification
Separate executed/passed, executed/failed, not executed and blocked. Never fabricate logs, tests, screenshots or deployment success.

## Security and traceability
Never expose secrets. Update relevant docs and `CHANGELOG-AI.md` for significant changes. Record architecture decisions in `docs/13-decisions-log.md`.

## Git ownership
Only the project owner commits, pushes, merges, tags and releases. Agents must not initialise Git. Deployment remains an owner-controlled, separately approved Stage C operation. Existing publication of governance files does not mean Stage B application acceptance has occurred.
