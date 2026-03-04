# ACTION_PLAN

Use this file for intake, decomposition, board transitions, and wrapper-gated execution control.

## Intake Snapshot

### Objective (current focus)
- `<fill>`

### Definition of Done
- `<fill functional outcome>`
- Latest user directive is captured verbatim in `docs/DIRECTIVE_REGISTER.md` and linked to the active card.
- `workflow-context-gate --strict-medium` is `PASS` before `DOING -> DONE`.
- `context-bootstrap.status_code == 0` before `DOING -> DONE`.
- `update-plan-freshness` is `PASS` before `DOING -> DONE`.
- `EVIDENCE_LOG.md` contains a structured evidence block with commands + artifacts.

### Constraints
- Keep board contract strict: `DOING == 1`, `NEXT <= 3`.
- Allowed transitions only: `NEXT->DOING`, `DOING->BLOCKED`, `BLOCKED->DOING`, `DOING->DONE`.
- No silent close: every `DONE` card must have a matching evidence block.
- No `DOING -> DONE` when wrapper gates are stale or failed.

## Process Wrapper (Task-First Board)

- Cards are task-level only (Epic/Story progress is tracked separately if needed).
- Before `NEXT -> DOING`, fill `TASK BREAKDOWN` for the card.
- For high-risk cards, add a short TRIZ pre-take (`IFR`, contradictions, resources, verify gates).
- For behavior-sensitive cards, use Hard Double-Check Protocol before close.

### TASK BREAKDOWN template (mandatory)

For each task in `DOING`, use atomized steps (`8-20` recommended) in this format:
- `Step`: one concrete action.
- `Done when`: observable completion criterion.
- `Verify/Evidence`: command or artifact path.
- `Check-A (contract)`: policy/contract/invariant check.
- `Check-B (behavior)`: runtime/live behavior check.

### Hard Double-Check Protocol (mandatory for wrapper/runtime changes)

- `A=PASS`, `B=FAIL` -> do not close; treat as behavior regression.
- `A=FAIL`, `B=PASS` -> do not close; treat as contract drift.
- `A=PASS`, `B=PASS` -> close is allowed.
- Any `INCONCLUSIVE` in `Check-B` requires explicit recheck step and artifact.

## PROJECT BOARD

### DOING (exactly 1 card)
- [ ] **BOOT-001 Prepare project contracts and baseline verify**

### NEXT (maximum 3 cards)
- [ ] **PLAN-001 Define milestone roadmap**
- [ ] **ARCH-001 Confirm architecture baseline**

### BLOCKED
- [ ] _empty_

### DONE
- [x] **INIT-001 Repository template initialized**

## TASK BREAKDOWN

### BOOT-001
- [ ] Step: Fill `PROJECT_MANIFEST.md` with objective, constraints, DoD.
- [ ] Done when: manifesto reflects current project contract and close gates.
- [ ] Verify/Evidence: `PROJECT_MANIFEST.md` diff + evidence block reference.
- [ ] Check-A (contract): board and close-gate invariants remain valid.
- [ ] Check-B (behavior): `python3 tools/agent_bootstrap.py --label boot_001_manifest` returns PASS snapshot.

- [ ] Step: Capture latest directive row in `docs/DIRECTIVE_REGISTER.md` and bind it to `BOOT-001`.
- [ ] Done when: directive row has verify hook + status and no placeholder text.
- [ ] Verify/Evidence: updated row in `docs/DIRECTIVE_REGISTER.md`.
- [ ] Check-A (contract): directive schema validation passes.
- [ ] Check-B (behavior): `python3 tools/dev_harness_server.py directive-freshness --max-age-s 43200` returns PASS.

- [ ] Step: Sync plan snapshot via wrapper command.
- [ ] Done when: `update-plan-sync` writes a fresh snapshot linked to active `DOING`.
- [ ] Verify/Evidence: `python3 tools/dev_harness_server.py update-plan-sync --summary "BOOT-001 plan snapshot" --status IN_PROGRESS --label boot_001_plan_sync`.
- [ ] Check-A (contract): `python3 tools/dev_harness_server.py update-plan-freshness --max-age-s 21600` returns PASS.
- [ ] Check-B (behavior): `python3 tools/dev_harness_server.py update-plan-trace --doing-card BOOT-001 --limit 1` shows the latest row bound to `BOOT-001`.

- [ ] Step: Run strict wrapper gate chain.
- [ ] Done when: `workflow-context-gate`, `governance-audit`, `context-bootstrap`, `update-plan-freshness` are PASS.
- [ ] Verify/Evidence: gate command outputs + artifact paths in `shared/spikes/...`.
- [ ] Check-A (contract): `DOING==1`, `NEXT<=3`.
- [ ] Check-B (behavior): spike artifacts contain `status_code=0` and active card mapping.

- [ ] Step: Log final evidence block and perform board transition.
- [ ] Done when: `EVIDENCE_LOG.md` updated and `BOOT-001` can move to `DONE` by contract.
- [ ] Verify/Evidence: new `## Evidence (...)` block with scope/commands/observed/artifacts.
- [ ] Check-A (contract): `DOING -> DONE` transition has matching evidence entry.
- [ ] Check-B (behavior): post-transition `workflow-context-gate --strict-medium` remains PASS.

## ACTIVE TRACKER

- Current cycle owner: `<fill>`
- Started at (UTC): `<fill>`
- Verify hook: `<fill>`

## Queue Refresh Log

- 2026-03-03: Initial board seeded from template.
- 2026-03-04: Wrapper governance contour upgraded (double-check protocol + update-plan close-gate + structured evidence format).
