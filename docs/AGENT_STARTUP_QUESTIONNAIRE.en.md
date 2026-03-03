# Agent Startup Questionnaire (EN)

Use this before coding starts.

## Questions the Agent Must Ask
1. What is the exact objective for this cycle (single sentence)?
2. What is the measurable Definition of Done for this cycle?
3. What constraints are strict (time, security, compliance, architecture)?
4. What is explicitly out of scope (non-goals)?
5. Which verification commands are mandatory before marking done?
6. Are there any required external sources to validate (docs/specs/latest rules)?

## Documents to Fill Before Work Begins
1. `PROJECT_MANIFEST.md`
   - objective
   - DoD
   - constraints
   - non-goals
2. `ACTION_PLAN.md`
   - exactly one `DOING` card
   - up to three `NEXT` cards
   - task breakdown for current `DOING`
3. `docs/DIRECTIVE_REGISTER.md`
   - verbatim user directive
   - intent (`EXEC_NOW` or `WORKFLOW_IDEA`)
   - planned integration
   - verify hook
4. `EVIDENCE_LOG.md`
   - initial bootstrap evidence block

## Mandatory Startup Commands
```bash
python3 tools/agent_bootstrap.py
python3 tools/dev_harness_server.py workflow-context-gate --label startup
./tools/verify_fail_fast.sh
```
