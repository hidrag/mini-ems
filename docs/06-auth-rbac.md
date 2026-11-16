# 06 — Authentication and RBAC

Planned roles: Super Admin, Organisation Admin, Site Manager, Operator, Viewer.

Authentication proves identity; authorisation controls actions and data. Backend checks are authoritative.

Permission principles:
- Super Admin: cross-organisation administration.
- Organisation Admin: manage users/sites/devices within own organisation.
- Site Manager: manage/view assigned sites according to approved permissions.
- Operator: monitoring and alarm actions for assigned sites.
- Viewer: read-only access to permitted data.

Exact permission matrix must be approved before implementation; do not infer permissions from role names.

Requirements:
- Use a maintained password hashing library/algorithm.
- Never log passwords or tokens.
- JWT signing secret comes from environment configuration.
- Document expiry and refresh/revocation.
- Enforce tenant/site scope on every protected query.
- Frontend route guards are UX only.
- Test cross-tenant access denial.
- Demo credentials must not be published as production secrets.

Authentication is outside Phase 1.
