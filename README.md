# Codex Universal Starter Template

Production-oriented repository template for starting new projects with Codex using a deterministic governance loop:
`intake -> plan -> implement -> verify -> evidence`.

This template is extracted from a hardened real-world setup and anonymized for general use.

## What You Get

- Governance contracts:
  - `PROJECT_MANIFEST.md` (requirements + acceptance contracts)
  - `ACTION_PLAN.md` (board + execution plan)
  - `EVIDENCE_LOG.md` (verification facts + artifact links)
  - `DEBUG.md` (verified runbook only)
- Board state machine with invariants:
  - states: `NEXT`, `DOING`, `BLOCKED`, `DONE`
  - allowed transitions only:
    - `NEXT->DOING`
    - `DOING->BLOCKED`
    - `BLOCKED->DOING`
    - `DOING->DONE`
  - invariants:
    - `DOING == 1`
    - `NEXT <= 3`
- Context persistence protocol:
  - bootstrap order
  - directive capture register
  - update-plan lifecycle (`sync/freshness/trace`)
  - workflow context gate
- Lightweight tooling:
  - `tools/agent_bootstrap.py`
  - `tools/dev_harness_server.py` (governance CLI gate)
  - `tools/agent_metrics.py`
  - `tools/verify_fail_fast.sh`

## Quick Start (5-10 min)

1. Clone this template and enter repo.
2. Edit these files first:
   - `PROJECT_MANIFEST.md`
   - `ACTION_PLAN.md`
   - `docs/DIRECTIVE_REGISTER.md`
3. Run bootstrap and context gates:

```bash
python3 tools/agent_bootstrap.py
python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap
python3 tools/dev_harness_server.py update-plan-sync --summary "bootstrap snapshot" --status IN_PROGRESS --label bootstrap
```

4. Run baseline verification:

```bash
./tools/verify_fail_fast.sh
```

## First Conversation Checklist (Agent)

See:
- `docs/AGENT_STARTUP_QUESTIONNAIRE.en.md`
- `docs/AGENT_STARTUP_QUESTIONNAIRE.ru.md`
- `docs/AGENT_START_PROMPT.en.md`
- `docs/AGENT_START_PROMPT.ru.md`

These files define:
- what the agent must ask the user before coding,
- what documents must be filled before starting work.

## Documentation Map

- English onboarding:
  - `docs/AGENT_BOOTSTRAP_PROTOCOL.en.md`
  - `docs/CONTEXT_SYNC_PROTOCOL.en.md`
  - `docs/NETWORK_SEARCH_PROTOCOL.en.md`
  - `docs/ONBOARDING_30_MIN.en.md`
- Russian onboarding:
  - `docs/AGENT_BOOTSTRAP_PROTOCOL.ru.md`
  - `docs/CONTEXT_SYNC_PROTOCOL.ru.md`
  - `docs/NETWORK_SEARCH_PROTOCOL.ru.md`
  - `docs/ONBOARDING_30_MIN.ru.md`
- Project setup profile:
  - `docs/PROJECT_PROFILE.md`
- Acknowledgements:
  - `docs/ACKNOWLEDGEMENTS.md`

## License

This repository uses the MIT License.
See `LICENSE`.

## Community

- Contribution guide: `CONTRIBUTING.md`
- RU contribution guide: `CONTRIBUTING.ru.md`
- Code of conduct: `CODE_OF_CONDUCT.md`
- GitHub templates:
  - `.github/PULL_REQUEST_TEMPLATE.md`
  - `.github/ISSUE_TEMPLATE/*`
- CI workflow:
  - `.github/workflows/ci.yml`

## GitHub Private Repo Push

```bash
git init
git add .
git commit -m "chore: initialize codex universal starter template"

# Requires authenticated GitHub CLI (gh auth status)
gh repo create <your-private-repo-name> --private --source . --remote origin --push
```

## Notes

- This is a governance/template repository, not a business-domain implementation.
- Keep process docs short, explicit, and evidence-backed.
