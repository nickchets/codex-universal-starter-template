# Codex Rules (Universal Governance Profile)

## 1. Objective
- Keep execution deterministic and evidence-backed.
- Reduce regression risk through small safe changes.

## 2. Contracts
- Requirements: `PROJECT_MANIFEST.md`
- Execution board: `ACTION_PLAN.md`
- Verification evidence: `EVIDENCE_LOG.md`
- Verified runbook: `DEBUG.md`
- Context sync: `docs/CONTEXT_SYNC_PROTOCOL.en.md`
- Directive traceability: `docs/DIRECTIVE_REGISTER.md`

## 3. First-Run Chain
1. `python3 tools/agent_bootstrap.py`
2. `python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap`
3. Validate:
   - `DOING == 1`
   - `NEXT <= 3`

## 4. Board Rules
- Canonical states: `NEXT`, `DOING`, `BLOCKED`, `DONE`
- Allowed transitions only:
  - `NEXT->DOING`
  - `DOING->BLOCKED`
  - `BLOCKED->DOING`
  - `DOING->DONE`
- `DOING` must contain exactly one card.
- `NEXT` must contain at most three cards.

## 5. Mandatory Transaction
1. Capture directive.
2. Lock board card.
3. Implement.
4. Verify.
5. Record evidence.
6. Transition card.

No `DOING->DONE` without evidence block.

## 6. Quality Gates
- Baseline gate:
  - `./tools/verify_fail_fast.sh`
- Governance gate:
  - `python3 tools/dev_harness_server.py workflow-context-gate --label <name>`

## 7. Network Research Rule
For volatile facts, high-risk changes, and explicit “check latest” requests:
- use primary sources first,
- record URLs and timestamp in evidence.

Protocol:
- `docs/NETWORK_SEARCH_PROTOCOL.en.md`

## 8. Metrics + Reflection
Per cycle:
- `python3 tools/agent_metrics.py log ...`
- `python3 tools/agent_metrics.py summary --out shared/agent_metrics/summary_latest.json`
- `python3 tools/agent_metrics.py dashboard --out-json shared/agent_metrics/dashboard_latest.json --out-md shared/agent_metrics/dashboard_latest.md`

Reflection trigger:
- every 5 completed cycles,
- immediately after `BLOCKED`,
- after repeated regressions.

## 9. Tag Routing
- `#INTAKE` -> `jira-loop`
- `#TRIZ` -> `triz-ariz-solver`
- `#REFACTOR` -> `autonomous-refactor-loop`
- `#SIMPLIFY` -> `code-simplifier` / `/code-simplify-commit`
- `#SPIKE` -> `browser-spikes`
- `#FEEDBACK` -> `autonomous-feedback-loop`
- `#VERIFY` -> `verify-evidence`
