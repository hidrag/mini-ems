# 03 — Architecture

## Confirmed hosting direction
- React/TypeScript frontend: Vercel.
- FastAPI API: Render Web Service.
- Long-running consumer/simulator: evaluate Render Background Worker or suitable worker host.
- Database: Neon PostgreSQL.
- MQTT broker: not selected.
- Local development: Windows 11 native processes; Docker excluded.

## Logical architecture
```text
Browser → React (Vercel) → FastAPI (Render) → Neon PostgreSQL
                              ↑
Telemetry consumer ← MQTT broker ← Python meter simulator
                              |
                         WebSocket → Browser
```

## Principles
- Frontend never connects directly to PostgreSQL.
- API is the application boundary.
- Telemetry processing is separate from browser request handling.
- MQTT is transport; Neon is persistent system of record.
- WebSockets distribute updates, not replace stored history.
- Enforce device, organisation and site authorisation server-side.
- Persist UTC-aware timestamps.
- Handle duplicates, out-of-order messages and reconnects.
- Gracefully stop long-running processes.
- Do not rely on ephemeral files for durable data.

## Render considerations
Render supports Python web services and background workers. Free web services may spin down; background workers require paid compute. Verify current plans/limits before deployment. Web services must bind to `0.0.0.0` and the platform `PORT`.

## MQTT decision open
Evaluate managed broker or private broker hosting: TLS, authentication, network reachability from Windows and Render, quotas, connection limits, availability and cost. Anonymous public MQTT is prohibited. Record decision in ADR before cloud-specific implementation.

## Docker
Docker/Compose are excluded unless the owner explicitly reopens the decision through an ADR.
