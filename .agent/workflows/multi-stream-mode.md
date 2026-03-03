# Workflow: /multi-stream-mode

Purpose:
- coordinate concurrent lanes without losing global board determinism.

## Canonical Lanes

- `CORE_STREAM`
- `PLATFORM_STREAM`
- `VERIFY_STREAM`

## Hard Limits

- `global_active_lanes <= 3`
- `per_lane_doing <= 1`
- global board must still satisfy `DOING == 1`

## Steps

1. Lane assignment
   - map work item to one lane and branch prefix.
2. Board synchronization
   - keep one global `DOING` card in `ACTION_PLAN.md`.
3. Execution cycle logging
   - append events to `shared/agent_metrics/events.jsonl`.
4. Metrics refresh
   - run:
     - `python3 tools/agent_metrics.py summary --out shared/agent_metrics/summary_latest.json`
     - `python3 tools/agent_metrics.py dashboard --out-json shared/agent_metrics/dashboard_latest.json --out-md shared/agent_metrics/dashboard_latest.md`
5. Policy check
   - run `python3 tools/agent_metrics.py worktree-check --out shared/agent_metrics/worktree_check_latest.json`

## Exit Criteria

- Lane limits respected.
- Metrics artifacts refreshed.
- Board state remains deterministic.
