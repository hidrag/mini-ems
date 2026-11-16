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

## Never invent
Do not invent routes, request/response fields, tables, columns, constraints, environment variables, credentials, packages, services, workers, broker capabilities, roles, permissions, device protocols, telemetry units, engineering thresholds, provider limits, pricing or files.

## Inspect and plan
Inspect code, tests, Git status and relevant docs before each task. Produce a file-level plan and wait for approval before editing.

## No silent scope expansion
Do not add features or replace approved technology without an ADR and owner approval.

## Truthful verification
Separate executed/passed, executed/failed, not executed and blocked. Never fabricate logs, tests, screenshots or deployment success.

## Security and traceability
Never expose secrets. Update relevant docs and `CHANGELOG-AI.md` for significant changes. Record architecture decisions in `docs/13-decisions-log.md`.

## Git ownership
Only the project owner commits, pushes, merges, tags and deploys.
