# Workflow: /jira-intake

Purpose:
- convert incoming user request into deterministic board-ready execution.

## Entry Conditions

- New request affects scope, priorities, or acceptance.
- Board state needs refresh or recovery.

## Steps

1. Capture intake facts
   - objective, DoD, constraints, non-goals.
2. Update contracts
   - reflect behavior/acceptance in `PROJECT_MANIFEST.md` if needed.
3. Update directive register
   - append verbatim directive row in `docs/DIRECTIVE_REGISTER.md`.
4. Build board mapping
   - one card in `DOING`,
   - up to three in `NEXT`,
   - remaining scope in backlog notes.
5. Add task breakdown
   - 3-7 concrete subtasks for current `DOING`.
6. Define verify hooks
   - baseline gate + scope-specific checks + artifact paths.
7. Run governance gate
   - `python3 tools/dev_harness_server.py workflow-context-gate --label jira_intake --strict-medium`

## Exit Criteria

- Board invariants valid (`DOING == 1`, `NEXT <= 3`).
- Current `DOING` card is execution-ready.
- Verify hook and evidence plan are explicit.
