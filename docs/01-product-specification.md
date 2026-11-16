# 01 — Product Specification

## Purpose
Mini EMS is a simulated multi-site industrial energy monitoring platform demonstrating telemetry ingestion, persistence, real-time monitoring, analytics, alarms and reporting.

## Planned users
Super Admin, Organisation Admin, Site Manager, Operator and Viewer. Exact permissions must be approved in `06-auth-rbac.md`.

## Full scope
1. Authentication and RBAC.
2. Organisation/site management.
3. Device/meter management.
4. Python simulator and MQTT.
5. Real-time dashboard.
6. Historical analytics.
7. Alarm/event management.
8. PDF, Excel and CSV reporting.
9. Administration/configuration.
10. Cloud deployment and operational monitoring.

## Demo environment
One fictional organisation, three fictional sites, nine simulated meters and six equipment units.

## Simulation
Support normal operation, configurable load profiles, production changes, equipment shutdown, voltage/current/power variation, heartbeat loss and fault scenarios. Measurements must follow a documented model and be internally consistent. Label all demo data as simulated.

Before implementing calculations, define voltage type, current type, phase/balance assumptions, power definitions, power factor semantics, frequency units, cumulative/interval energy and timestamp handling.

Alarm thresholds are configurable demonstration values, not electrical engineering recommendations.

## Non-goals
No real PLC control, certified electrical measurement, safety-critical alarms, industrial process control, utility billing or predictive-maintenance claims.

## End-to-end success
Simulator emits reading → MQTT transports → backend validates and stores → WebSocket broadcasts → React displays → configured threshold triggers alarm → authorised operator acknowledges → history/report includes reading.

## Disclaimer
Educational/portfolio simulation only; not a certified industrial monitoring or control product.
