# Context Sync Protocol (EN)

Goal:
- ensure each user directive is captured, mapped to plan work, and verified.

## Canonical Load Order
1. `PROJECT_MANIFEST.md`
2. `docs/ADR/README.md`
3. `ACTION_PLAN.md`
4. `EVIDENCE_LOG.md`
5. `DEBUG.md`
6. `docs/CONTEXT_SYNC_PROTOCOL.en.md`
7. `docs/DIRECTIVE_REGISTER.md`

## Mandatory Transaction (Per Directive)
1. Classify intent:
   - `EXEC_NOW`
   - `WORKFLOW_IDEA`
2. Capture directive (verbatim) in register.
3. Map directive to board card in `ACTION_PLAN.md`.
4. Update contracts in `PROJECT_MANIFEST.md` if acceptance/behavior changed.
5. Run governance gate:
   - `python3 tools/dev_harness_server.py workflow-context-gate --label <name>`
6. Append command/artifact evidence to `EVIDENCE_LOG.md`.

## Non-Ambiguity Rules
- No `DOING->DONE` without evidence.
- No directive may disappear without register entry.
- No board with invalid invariants (`DOING != 1` or `NEXT > 3`).
