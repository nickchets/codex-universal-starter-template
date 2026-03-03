---
auto_execution_mode: 1
---
# Workflow: /code-simplify-commit

Purpose:
- run deterministic post-commit cleanup without behavior drift.

## Entry Conditions

- commit id (`<sha>`) is provided,
- simplification scope is limited to files touched by that commit.

## Steps

1. Lock scope
   - `git show --name-only --pretty=format: <sha>`
2. Capture invariants
   - list behavior that must remain unchanged.
3. Apply targeted simplification
   - remove duplication/dead paths,
   - reduce unnecessary nesting,
   - normalize naming and error handling.
4. Run baseline verification
   - `./tools/verify_fail_fast.sh`
5. Run governance context gate (for docs/flow updates if touched)
   - `python3 tools/dev_harness_server.py workflow-context-gate --label code_simplify --strict-medium`
6. Record evidence
   - append commands/results/artifacts to `EVIDENCE_LOG.md` when cleanup card is closed.
7. Commit cleanup
   - focused commit referencing source `<sha>`.

## Exit Criteria

- cleanup diff is scoped, readable, and behavior-safe,
- verification passed,
- evidence links are available for closure.
