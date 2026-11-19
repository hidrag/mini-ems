# 04 — Database Schema Governance

Database: PostgreSQL dedicated to Mini EMS. Never use the More Supermarket Mega database or any other project's database. Do not replace PostgreSQL with SQLite for development or testing.

Maintain separate databases for local development, automated testing and production, with separate credentials and restricted roles. Development and test databases run locally during Stage A; production runs on the approved EC2 instance in Stage C. Separate schemas in a development or production database do not satisfy test isolation.

Automated tests must never modify development or production data. Before migrations, fixtures, writes or cleanup, test setup must validate an explicitly configured test target and reject development/production targets. Do not fall back from a missing test connection to the application's development connection. Test credentials must not grant write access to development or production databases.

SQLAlchemy 2.x models define mappings; Alembic migrations define schema evolution. Review migrations before applying. Never rewrite an already-applied production migration; create a new one.

Provisioning a database and roles is separate from creating application tables: all application schema changes use Alembic. Confirm the target before every database operation, take an appropriate backup before production changes, and require owner approval for destructive migrations. Never rely on manually created production tables. Backup, restore and recovery procedures belong in `12-environment-deployment.md`.

Planned logical entities:
- Identity: users, roles, user_roles.
- Tenancy: organizations, sites, user_site_access.
- Devices: devices, device_status.
- Telemetry: device_telemetry.
- Alarms/events: alarm_rules, alarms, events, audit_logs.
- Simulation: simulator_configs, simulation_scenarios.

This inventory is not permission to create every table in Phase 1. Design and approve columns, types, constraints, indexes, retention and relationships in the relevant milestone.

Phase 1 approves only `system_metadata`: id, key, value, created_at, updated_at.

Rules:
- Use TIMESTAMPTZ for instants and store UTC.
- Document units explicitly.
- Use appropriate numeric precision.
- Enforce foreign keys and tenant relationships.
- Avoid cascading deletion of historical telemetry.
- Index according to actual query patterns.
- Use parameterised SQL/ORM expressions.
- Integration and migration tests use the dedicated automated testing database only.
- Verify target database before testing; never truncate/reset development, production or shared data.
- Bound query results and connection pools. Define telemetry indexes and retention from actual query patterns and measured data growth; any deletion policy requires explicit approval before execution.
