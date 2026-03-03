# Workflow: /spike-browser-research

Purpose:
- run bounded browser research for uncertain UI/automation behavior.

## Steps

1. Define question
   - one uncertainty, one success signal.
2. Define bounds
   - time budget, attempt budget, artifact checklist.
3. Execute experiment
   - run scripted browser scenario.
4. Capture artifacts
   - screenshot(s), html snapshot, logs, optional network trace.
5. Summarize outcome
   - write `summary.json` with question/result/decision.
6. Integrate decision
   - update `ACTION_PLAN.md` and `EVIDENCE_LOG.md`.

## Exit Criteria

- Uncertainty resolved or blocker classified with unblock condition.
- Artifact package is reproducible and linked in evidence.
