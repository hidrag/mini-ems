# 05 — API Contract Governance

Planned API prefix: `/api/v1`. The endpoint inventory is provisional until each module contract is approved.

Domains: authentication; organisations/sites; users/roles; devices; telemetry; dashboard; analytics; alarms/events; reports; simulator.

For every endpoint document method/path, authentication, permissions, parameters, request/response schema, errors, pagination/filtering, tenant scope and idempotency.

Rules:
- Pydantic request/response schemas.
- Do not expose ORM objects directly.
- Consistent errors and bounded pagination.
- UTC ISO 8601 timestamps.
- Never trust client-supplied tenant/site IDs without authorisation.
- Keep OpenAPI accurate and update frontend types/tests with contract changes.

Phase 1 endpoints:
- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/health/database`

Database health must execute `SELECT 1`; it must not report healthy when the query fails.
