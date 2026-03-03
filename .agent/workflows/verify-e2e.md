# Workflow: /verify-e2e

Purpose:
- execute deterministic verification chain and produce evidence artifacts.

## Steps

1. Baseline gate
   - run `./tools/verify_fail_fast.sh`.
2. Project-specific e2e
   - run configured e2e command for current scope.
3. Capture artifacts
   - store logs/results under `shared/spikes/<label>/...`.
4. Governance confirmation
   - run `python3 tools/dev_harness_server.py workflow-context-gate --label verify_e2e --strict-medium`.
5. Evidence update
   - append command results and artifact paths to `EVIDENCE_LOG.md`.
6. Board transition
   - allow `DOING->DONE` only after PASS evidence.

## Failure Handling

- If a gate fails:
  - classify blocker,
  - record fail artifacts,
  - move card to `BLOCKED` with explicit unblock condition.
