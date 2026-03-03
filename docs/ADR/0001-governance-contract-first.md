# ADR-0001: Governance Contract First

- Status: accepted
- Date: 2026-03-03

## Context
Without explicit governance contracts, agent sessions drift and board/evidence state becomes inconsistent.

## Decision
Make these files mandatory as source of truth:
- `PROJECT_MANIFEST.md`
- `ACTION_PLAN.md`
- `EVIDENCE_LOG.md`
- `DEBUG.md`
- `docs/DIRECTIVE_REGISTER.md`

Enforce board invariants:
- `DOING == 1`
- `NEXT <= 3`

## Consequences
- Better continuity between sessions.
- More up-front process overhead, but lower rework/regression risk.

## Verification Impact
- `python3 tools/agent_bootstrap.py`
- `python3 tools/dev_harness_server.py workflow-context-gate --label adr_0001`
