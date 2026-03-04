# DEBUG (Verified Runbook)

Only keep commands here that were actually verified in this repository.

## 1) Syntax Sanity Gate

```bash
python3 -m py_compile tools/*.py
```

## 2) Bootstrap Summary

```bash
python3 tools/agent_bootstrap.py
```

## 3) Governance Gate

```bash
python3 tools/dev_harness_server.py workflow-context-gate --label local
```

## 4) Baseline Verify

```bash
./tools/verify_fail_fast.sh
```

## 5) Plan Sync Snapshot

```bash
python3 tools/dev_harness_server.py update-plan-sync --summary "local debug snapshot" --status IN_PROGRESS --label local
python3 tools/dev_harness_server.py update-plan-freshness --max-age-s 21600
```
