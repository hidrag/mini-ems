# 13 — Architecture Decision Records

Record context, options, decision, consequences, status and date for significant decisions.

## ADR-001 — Hosting topology
**Status:** Accepted. React frontend on Vercel, FastAPI backend on Render, PostgreSQL on Neon. Consequences: CORS, public API URL, health checks and environment-specific configuration; verify provider limits before deployment.

## ADR-002 — Docker excluded
**Status:** Accepted. No Docker/Compose in current scope. Local setup uses native Windows tools. Reopen only with owner approval.

## ADR-003 — Dedicated Neon database
**Status:** Accepted. Mini EMS gets a separate Neon project/database. Never reuse More Supermarket Mega database.

## ADR-004 — AI implementation and Git ownership
**Status:** Accepted. Hermes implements/tests from approved prompts. Owner performs smoke tests and all commits/pushes/merges/releases.

## ADR-005 — MQTT broker
**Status:** Open. Evaluate managed broker or separately hosted private broker. Assess TLS, authentication, network reachability from Windows and Render, quotas, availability, cost and complexity. Anonymous public broker prohibited.

## ADR-006 — Runtime versions
**Status:** Proposed. Target Python 3.12+ and Node LTS; pin exact compatible versions after local verification.
