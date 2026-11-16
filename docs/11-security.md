# 11 — Security Requirements

## Secrets
- Never commit `.env`, credentials, tokens or private keys.
- `.env.example` contains placeholders only.
- Redact secrets from logs/reports.
- Vite `VITE_*` variables are public.
- Store production secrets in Render/Vercel environment settings as appropriate.

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
- Use HTTPS and MQTT TLS in hosted environments.
- No anonymous public MQTT broker.
- Restrict CORS to approved origins.

## Operations
- Health endpoints reveal only necessary status.
- Logs must not contain passwords, JWTs, connection strings or unnecessary personal data.
- Review dependencies and provider permissions.
- Separate development and production credentials.

The system is not safety-rated and must not control real equipment.
