# 10 — Testing Strategy

Test behaviour, use deterministic data, isolate integration tests and report unexecuted checks honestly.

Backend:
- Unit tests for calculations/validation/services.
- API tests using HTTPX.
- Database integration and migration tests against a dedicated test database/schema.
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
simulator emits → MQTT receives → consumer validates → Neon persists → WebSocket broadcasts → React displays → threshold creates alarm → authorised operator acknowledges → history/report includes reading.

The owner performs manual smoke tests at each milestone before committing.

For every check report exact command, working directory, execution status, result and limitations. Never use destructive cleanup against shared/production data.
