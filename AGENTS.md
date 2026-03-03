# Codex AGENTS (Universal)

## Scope
These instructions apply to the whole repository.

## Mission
- Deliver minimal safe diffs.
- Keep one deterministic board state.
- Never close work without verification evidence.

## Single Source Of Truth
- `PROJECT_MANIFEST.md` for requirements and contracts.
- `ACTION_PLAN.md` for active plan and board state.
- `EVIDENCE_LOG.md` for command-level evidence and artifacts.
- `DEBUG.md` for verified runbook commands only.
- `docs/CONTEXT_SYNC_PROTOCOL.en.md` for directive integration.
- `docs/DIRECTIVE_REGISTER.md` for verbatim user directives.

## First-Run Bootstrap (Mandatory)
1. `python3 tools/agent_bootstrap.py`
2. `python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap`
3. Load docs in order:
   - `PROJECT_MANIFEST.md`
   - `docs/ADR/README.md`
   - `ACTION_PLAN.md`
   - `EVIDENCE_LOG.md`
   - `DEBUG.md`
   - `docs/CONTEXT_SYNC_PROTOCOL.en.md`
4. Confirm board invariants:
   - `DOING == 1`
   - `NEXT <= 3`

## Board Contract (Mandatory)
- States: `NEXT`, `DOING`, `BLOCKED`, `DONE`.
- Allowed transitions only:
  - `NEXT->DOING`
  - `DOING->BLOCKED`
  - `BLOCKED->DOING`
  - `DOING->DONE`
- Invariants:
  - `DOING == 1`
  - `NEXT <= 3`

## Canonical Loop
1. Pick top `NEXT` card.
2. Lock one `DOING`.
3. Implement minimal safe diff.
4. Verify.
5. Record evidence.
6. Commit board transition.

## Context Sync Rule
- Every new user directive must be:
  - captured verbatim in `docs/DIRECTIVE_REGISTER.md`,
  - mapped to board work in `ACTION_PLAN.md`,
  - linked to verify hooks in `EVIDENCE_LOG.md`.

Preferred command:
`python3 tools/dev_harness_server.py directive-sync --message "<verbatim>" --intent "<EXEC_NOW|WORKFLOW_IDEA>" --planned-integration "<card/scope>" --label <name>`

## Verification Baseline
- `./tools/verify_fail_fast.sh`
- Add targeted tests relevant to changed scope.

## Anti-Hang Rules
- No interactive commands.
- Use explicit timeouts for risky commands.
- Run long-lived services in background with logs and readiness checks.

## Routing (Tags First)
- `#INTAKE` -> `jira-loop`
- `#TRIZ` -> `triz-ariz-solver`
- `#REFACTOR` -> `autonomous-refactor-loop`
- `#SIMPLIFY` -> `code-simplifier` (`/code-simplify-commit`)
- `#SPIKE` -> `browser-spikes`
- `#FEEDBACK` -> `autonomous-feedback-loop`
- `#VERIFY` -> `verify-evidence`

No-tag fallback:
- planning -> `jira-loop`
- contradiction/risk -> `triz-ariz-solver`
- refactor/tech debt -> `autonomous-refactor-loop`
- cleanup/simplify/readability by commit -> `code-simplifier`
- UI uncertainty/anti-bot/layout drift -> `browser-spikes`
- debug/runbook/feedback-loop hardening -> `autonomous-feedback-loop`
- tests/evidence -> `verify-evidence`

## RU Quick Note
Русская версия стартовых процедур:
- `README.ru.md`
- `docs/AGENT_BOOTSTRAP_PROTOCOL.ru.md`
- `docs/CONTEXT_SYNC_PROTOCOL.ru.md`
- `docs/AGENT_STARTUP_QUESTIONNAIRE.ru.md`
