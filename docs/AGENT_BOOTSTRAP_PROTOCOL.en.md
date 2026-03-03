# Agent Bootstrap Protocol (EN)

Use this protocol when:
- the chat is new,
- context is uncertain,
- the agent cannot confidently name the current `DOING` card.

## Mandatory Chain
1. Run:
   - `python3 tools/agent_bootstrap.py`
   - `python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap`
2. Load context in strict order:
   - `PROJECT_MANIFEST.md`
   - `docs/ADR/README.md`
   - `ACTION_PLAN.md`
   - `EVIDENCE_LOG.md`
   - `DEBUG.md`
   - `docs/CONTEXT_SYNC_PROTOCOL.en.md`
3. Confirm board invariants:
   - `DOING == 1`
   - `NEXT <= 3`
4. Start execution only after checks are PASS.

## Stop Condition
If bootstrap checks fail, fix docs/board integrity first; do not proceed to feature work.
