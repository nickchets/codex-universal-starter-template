# Agent Start Prompt (EN)

Use this as a first message to Codex in a new project:

```text
Work in autonomous execution mode.
Before implementation:
1) Run bootstrap and context gate.
2) Sync active plan snapshot with update-plan-sync.
3) Ask me startup questions from docs/AGENT_STARTUP_QUESTIONNAIRE.en.md.
4) Fill/update PROJECT_MANIFEST.md, ACTION_PLAN.md, docs/DIRECTIVE_REGISTER.md.
5) Confirm board invariants (DOING==1, NEXT<=3).
Then implement minimal safe diffs, verify, and record evidence in EVIDENCE_LOG.md.
```
