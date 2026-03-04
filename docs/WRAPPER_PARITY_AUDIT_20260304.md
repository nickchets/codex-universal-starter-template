# Wrapper Parity Audit (2026-03-04)

## Scope
- Compare template wrapper capabilities with the original reference wrapper.
- Keep the template implementation domain-neutral and reusable.
- Do not change reference repository code.

## Method
- Command-surface diff (`--help` + parser scan).
- Function-level revision of `tools/dev_harness_server.py`.
- Runtime smoke checks for newly added lifecycle commands.

## Compliance Matrix

Legend:
- `FULL`: capability implemented and runnable in template.
- `PARTIAL`: implemented with reduced depth/surface.
- `MISSING`: absent in template.

| Capability Group | Reference Surface | Template Surface | Status | Notes |
| --- | --- | --- | --- | --- |
| Governance audit | `governance-audit` | `governance-audit` | FULL | Runnable and artifact-backed. |
| Governance quality audit | `governance-quality-audit` | `governance-quality-audit` | FULL | Runnable with strict mode. |
| Context bootstrap | `context-bootstrap` | `context-bootstrap` | FULL | Board contract + task-breakdown checks preserved. |
| Directive capture | `directive-sync` | `directive-sync` | FULL | Supports auto-fill and deterministic IDs. |
| Directive lifecycle tracking | `directive-track` | `directive-track` | FULL | Lifecycle events persisted to `shared/harness/directive_lifecycle.jsonl` at runtime. |
| Directive freshness gate | `directive-freshness` | `directive-freshness` | FULL | Age + mapping-to-DOING checks. |
| Directive trace | `directive-trace` | `directive-trace` | FULL | Route/lifecycle inspection available. |
| Plan sync lifecycle | `update-plan-sync` | `update-plan-sync` | FULL | Deterministic IDs + JSONL lifecycle event log. |
| Plan freshness gate | `update-plan-freshness` | `update-plan-freshness` | FULL | Age + DOING-card mapping checks. |
| Plan trace | `update-plan-trace` | `update-plan-trace` | FULL | Filtered lifecycle trace available. |
| Workflow gate chain | `workflow-context-gate` behavior | `workflow-context-gate` | PARTIAL | Core chain present; no server/API orchestration layer. |
| Execution guard chain | `execution-guard` behavior | `execution-guard` | PARTIAL | Core guard chain present; reduced compared with full harness stack semantics. |
| Harness lifecycle control | `serve/up/down/status/metrics` | none | MISSING | Intentionally excluded from lightweight template profile. |
| HTTP API layer | `/harness/*` endpoints | none | MISSING | No FastAPI service in template wrapper. |
| Sinks/observability/ops | event sinks + observability endpoints | none | MISSING | Out of scope for minimal universal starter profile. |

## Verified Facts (Post-Revision)
- Template command surface now includes:
  - `directive-sync`, `directive-track`, `directive-freshness`, `directive-trace`
  - `update-plan-sync`, `update-plan-freshness`, `update-plan-trace`
  - `governance-audit`, `governance-quality-audit`, `context-bootstrap`
  - `workflow-context-gate`, `execution-guard`
- Previously blocked commands (`directive-freshness`, `update-plan-freshness`) are now runnable.
- `workflow-context-gate --strict-medium` and `execution-guard --strict-medium` pass in smoke checks.

## Residual Gaps (Intentional)
1. No harness process orchestration (`serve/up/down/status/metrics`).
2. No HTTP API (`/harness/*`) and request models.
3. No sinks/observability stack wiring.

## Recommendation
- Keep current profile as default universal baseline.
- Add an optional "extended wrapper profile" later if a project needs service/API/observability orchestration.
