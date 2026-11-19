# 13 — Architecture Decision Records

Record context, options, decision, consequences, status and date for significant decisions.

## ADR-001 — Hosting topology
**Status:** Superseded by ADR-007 on 2026-11-17. Historical decision: React frontend on Vercel, FastAPI backend on Render, PostgreSQL on Neon. Historical consequences: CORS, public API URL, health checks and environment-specific configuration; verify provider limits before deployment. These providers are no longer the approved hosting architecture.

## ADR-002 — Docker excluded
**Status:** Accepted. No Docker/Compose in current scope. Local setup uses native Windows tools. Reopen only with owner approval.

## ADR-003 — Dedicated Neon database
**Status:** Superseded by ADR-007 on 2026-11-17. Historical decision: Mini EMS gets a separate Neon project/database. Dedicated project isolation and the prohibition on reusing the More Supermarket Mega database remain mandatory; the Neon-specific choice is superseded.

## ADR-004 — AI implementation and Git ownership
**Status:** Accepted. Hermes implements/tests from approved prompts. Owner performs smoke tests and all commits/pushes/merges/tags/releases. Agents must not initialise Git. ADR-007 defines local acceptance, application upload and separate deployment gates.

## ADR-005 — MQTT broker
**Status:** Resolved by ADR-007 on 2026-11-17. Historical open question: evaluate managed broker or separately hosted private broker, including TLS, authentication, reachability from Windows and Render, quotas, availability, cost and complexity. Mosquitto is now selected locally and on the EC2 host. Anonymous public MQTT remains prohibited.

## ADR-006 — Runtime versions
**Status:** Proposed. Target Python 3.12+ and Node LTS; pin exact compatible versions after local verification.

## ADR-007 — Local-first development and temporary single-EC2 hosting
**Status:** Accepted by the project owner for documentation alignment; implementation and deployment require separate task approvals.

**Date:** 2026-11-17.

### Context
Mini EMS is a simulated portfolio project intended for approximately 3–4 months of AWS hosting. The owner approved completing and testing the application locally, publishing the accepted application to GitHub, then deploying it to one EC2 instance. Existing multi-provider guidance and the open broker choice conflict with that direction. All product features and the fictional demo inventory remain unchanged.

### Options considered
- Retain the historical multi-provider architecture: superseded by the owner's hosting decision.
- Local-first development followed by one Ubuntu EC2 host: selected.
- Add managed database, container or other AWS services: outside approved scope; requires a future approved ADR.

### Decision
1. **Stage A:** develop and test all components locally on Windows 11 with local PostgreSQL and Mosquitto, without AWS credentials or infrastructure. Complete automated tests and owner manual integration testing.
2. **Stage B:** after complete local acceptance, review secrets/ignore rules, documentation and test evidence and prepare a release-ready report. Only the owner commits, pushes, merges and tags. Existing governance publication does not bypass application acceptance.
3. **Stage C:** only after owner approval of the local implementation and GitHub upload, separately approve provisioning and deployment. Deploy from GitHub to one Ubuntu EC2 instance hosting Nginx, the React production build, FastAPI, PostgreSQL, Mosquitto, Python simulator and necessary application processes. Use systemd for long-running services.
4. Nginx serves static frontend assets and reverse-proxies API/WebSocket traffic. PostgreSQL is the persistent system of record; browsers never access it directly.
5. Maintain separate dedicated PostgreSQL databases and credentials for local development, automated testing and production. Automated tests must never modify development or production data. Fail closed on unsafe test targets before any write; use Alembic rather than manually created application tables.
6. Local development may use a restricted local Mosquitto listener without production TLS configuration. Production requires MQTT authentication, restricted network access and appropriate TLS security with certificate verification. Keep local and production broker configurations separate.
7. Use environment configuration for database connections, origins, MQTT settings and independent simulator settings. Configure frontend API URLs at build time; keep browser variables secret-free. The same application source must work locally and on AWS without business-logic rewrites or AWS-specific dependencies.
8. First complete the local application and measure actual CPU, RAM, disk and database usage under the simulated workload. Prepare a separate resource recommendation before Stage C with assumptions, headroom and limitations. Do not select an EC2 instance type or make cost claims now. The owner verifies AWS account eligibility, credits and costs before provisioning; Free Tier is not assumed unlimited or permanently free.
9. Docker remains excluded. RDS, ECS, EKS, Lambda and other additional AWS services require future owner approval. Do not introduce infrastructure dependencies to resolve consumer-to-WebSocket delivery without an approved design.

### Consequences
- One host simplifies deployment but is a single failure domain with shared resources; no high-availability claim is made.
- The owner is responsible for OS/database/broker operations, patching, restricted service access, backups, restore verification and recovery procedures.
- Bound simulator rates, polling, queries, memory, logs and database growth. Approve retention and backup policies; an on-host backup alone does not cover host loss.
- Local development TLS configuration differs from production security; production validation is a separate gate, not a local development prerequisite.
- Frontend configuration changes may require rebuilding the same source. Production application settings, persistent data and secrets remain outside replaceable release files.

### Superseded decisions and unresolved details
Supersedes ADR-001 and the provider-specific part of ADR-003; resolves ADR-005. ADR-002 Docker exclusion and ADR-004 owner authority remain in force. ADR-006 runtime pinning remains proposed.

Still open: consumer-to-WebSocket delivery and process topology, exact runtime versions/frontend test tooling, publishing rates and retention, backup frequency/destination and recovery objectives, domain/certificate arrangement, and measured AWS resource selection. Resolve these at their milestone/deployment gates; this ADR does not select extra infrastructure or authorise application implementation.
