## Summary

Describe what changed and why.

## Linked Board Card

- Card ID: `<e.g. BOOT-001>`
- Board transition: `<NEXT->DOING / DOING->DONE / ...>`

## Scope

- In scope:
  - `<item>`
- Out of scope:
  - `<item>`

## Verification

- [ ] `./tools/verify_fail_fast.sh`
- [ ] `python3 tools/dev_harness_server.py workflow-context-gate --label pr_check --strict-medium`
- [ ] Additional project-specific checks completed

Commands run:
```bash
<paste exact commands>
```

Artifacts:
- `<path/to/artifact_1>`
- `<path/to/artifact_2>`

## Evidence + Docs

- [ ] `EVIDENCE_LOG.md` updated
- [ ] `ACTION_PLAN.md` updated (if board state changed)
- [ ] `PROJECT_MANIFEST.md` updated (if contract changed)
- [ ] `docs/DIRECTIVE_REGISTER.md` updated (if new directive was integrated)

## Risk Assessment

- Regression risk: `low / medium / high`
- Rollback plan: `<one line>`
