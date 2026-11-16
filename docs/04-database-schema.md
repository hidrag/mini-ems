# 04 — Database Schema Governance

Database: dedicated Mini EMS Neon PostgreSQL project. Never use More Supermarket Mega database.

SQLAlchemy 2.x models define mappings; Alembic migrations define schema evolution. Review migrations before applying. Never rewrite an already-applied production migration; create a new one.

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
- Integration tests use a dedicated test database/schema.
- Verify target database before testing; never truncate/reset shared data.
