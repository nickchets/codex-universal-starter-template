# Onboarding 30 Minutes (EN)

## 0) Understand the project (3 min)
Read:
- `PROJECT_MANIFEST.md`
- `ACTION_PLAN.md`
- `EVIDENCE_LOG.md`
- `DEBUG.md`

## 1) Fill startup contracts (8 min)
Update:
- `PROJECT_MANIFEST.md` (objective, DoD, constraints),
- `ACTION_PLAN.md` (current `DOING`, `NEXT`, task breakdown),
- `docs/DIRECTIVE_REGISTER.md` (first user directive row).

## 2) Bootstrap checks (5 min)
```bash
python3 tools/agent_bootstrap.py
python3 tools/dev_harness_server.py workflow-context-gate --label onboarding
```

## 3) Baseline verify (5 min)
```bash
./tools/verify_fail_fast.sh
```

## 4) Log evidence (4 min)
Append an evidence block in `EVIDENCE_LOG.md` with:
- commands,
- PASS/FAIL,
- artifact paths.

## 5) Start implementation (5 min)
Pick current `DOING`, execute minimal safe diff, verify, and transition board.
