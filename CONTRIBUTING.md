# Contributing Guide

Thanks for contributing.

## 1. Start With Contracts
Before implementation, align these files:
- `PROJECT_MANIFEST.md`
- `ACTION_PLAN.md`
- `docs/DIRECTIVE_REGISTER.md`

Board invariants must remain valid:
- `DOING == 1`
- `NEXT <= 3`

## 2. Change Workflow
1. Pick current `DOING` card.
2. Make the smallest safe diff.
3. Run verification.
4. Record evidence.
5. Transition board state.

## 3. Verification
Minimum baseline:
```bash
./tools/verify_fail_fast.sh
python3 tools/dev_harness_server.py workflow-context-gate --label contrib_check --strict-medium
```

## 4. Commit Quality
- Keep commits focused and reversible.
- Include evidence-impact context in commit message when relevant.
- Do not merge work that fails verification.

## 5. Pull Request Checklist
- [ ] Scope matches `DOING` card.
- [ ] Tests/checks pass.
- [ ] `EVIDENCE_LOG.md` updated.
- [ ] Board transition is valid.
- [ ] No contradictory updates in governance docs.
