# 09 — Coding Standards

## Python
- Type hints on functions/public interfaces.
- Pydantic for external data validation.
- SQLAlchemy 2.x typed mappings/sessions.
- Separate routers, schemas, services and repositories where justified.
- Dependency injection for request-scoped resources.
- Avoid global mutable state and circular imports.
- Use UTC-aware datetimes.
- Use Decimal where exact decimal arithmetic is required.
- Structured logging; never log secrets.
- Catch specific exceptions; no bare `except`.
- Focused modules, meaningful docstrings and comments explaining why.

## TypeScript / React
- TypeScript strict mode.
- Avoid `any`.
- Focused components.
- Separate API clients, hooks and UI.
- TanStack Query for server state.
- No secrets in frontend.
- No direct database access from browser.
- Handle loading, empty, error and success states.

## Dependencies and checks
Add packages only when justified. Python: Ruff. Frontend: approved formatter/linter and TypeScript checks. Keep checks reproducible.

Update README and relevant docs when commands, env vars, architecture or behaviour changes.
