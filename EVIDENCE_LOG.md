# EVIDENCE_LOG

Canonical evidence journal.
Add new blocks in chronological order.

## Evidence (2026-03-03) — Template bootstrap initialized

Scope:
- Universal Codex governance template created in a new repository folder.

Commands (expected PASS):
- `python3 -m py_compile tools/*.py`
- `python3 tools/agent_bootstrap.py`
- `python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap`
- `./tools/verify_fail_fast.sh`

Artifacts:
- `shared/spikes/agent_bootstrap_*/summary.json`
- `shared/spikes/workflow_context_gate_*/summary.json`
- `shared/agent_metrics/summary_latest.json`

## Evidence (2026-03-03) — Smoke verification in template repo

Commands (PASS):
- `python3 -m py_compile tools/*.py`
- `python3 tools/agent_bootstrap.py --label smoke`
- `python3 tools/dev_harness_server.py workflow-context-gate --label smoke --strict-medium`
- `./tools/verify_fail_fast.sh`
- `python3 tools/agent_metrics.py log --board-card BOOT-001 --stream PLATFORM_STREAM --status PASS --duration-s 12.0 --skills "jira-loop,verify-evidence" --rules "board,bootstrap" --verify-pass 1 --notes "template smoke cycle"`
- `python3 tools/agent_metrics.py summary --out shared/agent_metrics/summary_latest.json`
- `python3 tools/agent_metrics.py dashboard --out-json shared/agent_metrics/dashboard_latest.json --out-md shared/agent_metrics/dashboard_latest.md`

Artifacts:
- `shared/spikes/agent_bootstrap_smoke_20260303_140200/summary.json`
- `shared/spikes/workflow_context_gate_smoke_20260303_140200/summary.json`
- `shared/agent_metrics/events.jsonl`
- `shared/agent_metrics/summary_latest.json`
- `shared/agent_metrics/dashboard_latest.json`
- `shared/agent_metrics/dashboard_latest.md`

## Evidence (2026-03-03) — Post-documentation governance re-check

Commands (PASS):
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label post_docs --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_post_docs_20260303_140254/summary.json`

## Evidence (2026-03-03) — License + acknowledgements + project profile

Commands (PASS):
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label legal_ack_profile --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_legal_ack_profile_20260303_141450/summary.json`

## Evidence (2026-03-03) — Community docs baseline

Commands (PASS):
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label community_docs --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_community_docs_20260303_141714/summary.json`

## Evidence (2026-03-03) — GitHub templates for PR/issues

Commands (PASS):
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label github_templates --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_github_templates_20260303_141940/summary.json`

## Evidence (2026-03-03) — Audit fix pack (template portability + CI)

Commands (PASS):
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label audit_fix_pack --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_audit_fix_pack_20260303_142642/summary.json`

## Evidence (2026-03-03) — Skills/workflows full rewrite + TRIZ deep upgrade

Scope:
- Rewrote all `.agent/skills/*/SKILL.md` to production-grade format.
- Reworked all `.agent/workflows/*.md` with deterministic entry/exit criteria.
- Upgraded `triz-ariz-solver` with full contradiction pipeline and ARIZ A1-A7 deep pass.
- Replaced legacy domain-specific stream naming with generic `CORE_STREAM`.

Commands (PASS):
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label skills_workflows_rewrite --strict-medium`
- `python3 tools/agent_bootstrap.py --label skills_workflows_rewrite`

Artifacts:
- `shared/spikes/workflow_context_gate_skills_workflows_rewrite_20260303_144147/summary.json`
- `shared/spikes/agent_bootstrap_skills_workflows_rewrite_20260303_144147/summary.json`

### Network Cross-Check
- Question: How should SKILL files be structured for reliable invocation and maintainability?
- Sources:
  - https://developers.openai.com/codex/cli/skills/
  - https://developers.openai.com/apps-sdk/plan/skills
  - https://www.agentskills.org/
- Checked at (UTC): 2026-03-03T14:00:00Z
- Decision:
  - Use one-sentence scoped description in front matter.
  - Keep clear trigger/boundary/outputs/acceptance sections.
  - Prefer progressive disclosure and deterministic workflow phases.
- Repo impact:
  - `.agent/skills/*/SKILL.md`
  - `.agent/workflows/*.md`
  - `tools/agent_metrics.py` (stream naming normalization)
  - `docs/SKILL_AUTHORING_GUIDELINES.md`

## Evidence (2026-03-03) — Universality audit pass #2 (docs + methods)

Scope:
- Full scan for residual domain-specific terms and non-universal method naming.
- Manual review of governance/docs references for oversimplified or mismatched routing.
- Alignment refresh for skills/workflows documentation and tag routing.

Commands (PASS):
- `rg -n "geo_|GEO|city_first|celery|turnstile|datadome|cloudflare|residential|xvfb|streamlit|fastapi|redis|selenium|worker2" -S .`
- `rg -n "nickchets|codex-universal-starter-template|CORE_STREAM|PLATFORM_STREAM|VERIFY_STREAM|GEO_STREAM|DIR-|DOING == 1|NEXT <= 3|TODO|<fill>|<project-owner>" -S .`
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label universality_audit_pass2 --strict-medium`
- `python3 tools/agent_bootstrap.py --label universality_audit_pass2`

Artifacts:
- `shared/spikes/workflow_context_gate_universality_audit_pass2_20260303_144435/summary.json`
- `shared/spikes/agent_bootstrap_universality_audit_pass2_20260303_144435/summary.json`

Decision:
- No remaining explicit project-specific/domain tails detected in active template docs/skills/workflows/scripts.
- Routing/guide docs strengthened and synchronized with rewritten skill/workflow set.

## Evidence (2026-03-03) — Universality audit final gate

Commands (PASS):
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label universality_audit_finalize --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_universality_audit_finalize_20260303_144511/summary.json`

## Evidence (2026-03-03) — Added autonomous-feedback-loop skill

Scope:
- Added full `autonomous-feedback-loop` skill to template.
- Integrated routing via `#FEEDBACK` tag and no-tag debug/runbook fallback.
- Updated skills operating guide to include the new skill in selection priority.

Commands (PASS):
- `rg -n "autonomous-feedback-loop|#FEEDBACK|debug/runbook/feedback" AGENTS.md CODEX_RULES.md SKILLS_WORKFLOWS.md .agent/skills -S`
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label add_feedback_skill --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_add_feedback_skill_20260303_144948/summary.json`

## Evidence (2026-03-03) — Added missing simplify skill/workflow (universal)

Scope:
- Added missing universal skill `code-simplifier`.
- Added missing universal workflow `/code-simplify-commit`.
- Synced routing docs (`AGENTS.md`, `CODEX_RULES.md`, `SKILLS_WORKFLOWS.md`) with `#SIMPLIFY`.

Updated files:
- `.agent/skills/code-simplifier/SKILL.md`
- `.agent/workflows/code-simplify-commit.md`
- `AGENTS.md`
- `CODEX_RULES.md`
- `SKILLS_WORKFLOWS.md`

Commands (PASS):
- `timeout 10s python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agent/skills/autonomous-feedback-loop`
- `timeout 10s python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agent/skills/autonomous-refactor-loop`
- `timeout 10s python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agent/skills/browser-spikes`
- `timeout 10s python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agent/skills/code-simplifier`
- `timeout 10s python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agent/skills/jira-loop`
- `timeout 10s python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agent/skills/triz-ariz-solver`
- `timeout 10s python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agent/skills/verify-evidence`
- `timeout 10s ./tools/verify_fail_fast.sh`
- `timeout 10s python3 tools/dev_harness_server.py workflow-context-gate --label template_simplify_gap_add_20260303 --strict-medium`

Artifacts:
- `shared/spikes/workflow_context_gate_template_simplify_gap_add_20260303_20260303_153250/summary.json`
- `shared/spikes/workflow_context_gate_template_simplify_gap_post_evidence_20260303_20260303_153345/summary.json`

## Evidence (2026-03-04) — Wrapper plan/evidence contour synced from reference wrapper into template

Scope:
- Reviewed latest reference board/evidence wrapper updates and transferred reusable governance patterns into template sources.
- Upgraded template `ACTION_PLAN` and markdown templates to reflect stricter wrapper-driven close gates and richer evidence structure.

Updated files:
- `ACTION_PLAN.md`
- `docs/templates/TASK_BREAKDOWN_TEMPLATE.md`
- `docs/templates/EVIDENCE_BLOCK_TEMPLATE.md`
- `EVIDENCE_LOG.md`

Verification commands:
- `cd /home/lap/projects/codex-universal-starter-template && python3 -m py_compile tools/*.py`
- `cd /home/lap/projects/codex-universal-starter-template && ./tools/verify_fail_fast.sh`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py workflow-context-gate --label template_wrapper_sync_20260304 --strict-medium`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py governance-audit --label template_wrapper_sync_20260304`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py context-bootstrap --label template_wrapper_sync_20260304`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py governance-quality-audit --label template_wrapper_sync_20260304 --strict-medium`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/agent_bootstrap.py --label template_wrapper_sync_20260304`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py workflow-context-gate --label template_wrapper_sync_post_fix_20260304 --strict-medium`

Observed:
- Wrapper governance checks are `PASS` after template updates (`status_code=0` across workflow/governance/bootstrap/quality).
- Post-fix strict workflow gate is also `PASS` (`template_wrapper_sync_post_fix_20260304`).
- Board invariants remain valid (`DOING=1`, `NEXT=2`).
- Template now includes transferred wrapper practices:
  - hard close gates (`workflow-context-gate`, `context-bootstrap`, `update-plan-freshness`);
  - mandatory `Check-A/Check-B` in task breakdown;
  - expanded evidence block schema (`Updated files`, `Observed`, optional `Metrics update`, optional `Directive/context sync`).

Artifacts:
- `shared/spikes/workflow_context_gate_template_wrapper_sync_20260304_20260304_145917/summary.json`
- `shared/spikes/governance_audit_template_wrapper_sync_20260304_20260304_145917/summary.json`
- `shared/spikes/context_bootstrap_template_wrapper_sync_20260304_20260304_145917/summary.json`
- `shared/spikes/governance_quality_audit_template_wrapper_sync_20260304_20260304_145917/summary.json`
- `shared/spikes/agent_bootstrap_template_wrapper_sync_20260304_20260304_145923/summary.json`
- `shared/spikes/workflow_context_gate_template_wrapper_sync_post_fix_20260304_20260304_150053/summary.json`

Decision:
- Template wrapper governance baseline is upgraded and validated.
- Next expected use: instantiate a new project from this template and run the same strict wrapper close-gates unchanged.

## Evidence (2026-03-04) — Core wrapper parity uplift (lifecycle + freshness + trace)

Scope:
- Closed core wrapper parity gaps in template by implementing directive lifecycle and update-plan lifecycle commands.
- Removed non-runnable close-gate gaps where docs expected commands that were previously missing.
- Produced a persistent parity matrix artifact for future audits.

Updated files:
- `tools/dev_harness_server.py`
- `docs/WRAPPER_PARITY_AUDIT_20260304.md`
- `EVIDENCE_LOG.md`

Verification commands:
- `cd /home/lap/projects/codex-universal-starter-template && python3 -m py_compile tools/*.py`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py --help`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py directive-freshness --max-age-s 999999`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py update-plan-sync --summary "smoke sync" --status IN_PROGRESS --source TEST --label smoke_up_sync`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py update-plan-freshness --max-age-s 3600`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py update-plan-trace --limit 5`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py directive-track --directive-id DIR-20260303-001 --phase integrated --note "smoke" --label smoke_dir_track`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py directive-trace --directive-id DIR-20260303-001`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py workflow-context-gate --label parity_smoke --strict-medium`
- `cd /home/lap/projects/codex-universal-starter-template && python3 tools/dev_harness_server.py execution-guard --label parity_exec_smoke --strict-medium`

Observed:
- Template wrapper command surface now includes:
  - `directive-sync`, `directive-track`, `directive-freshness`, `directive-trace`;
  - `update-plan-sync`, `update-plan-freshness`, `update-plan-trace`;
  - `governance-audit`, `governance-quality-audit`, `context-bootstrap`, `workflow-context-gate`, `execution-guard`.
- Previously missing commands (`directive-freshness`, `update-plan-freshness`) now execute successfully.
- `update-plan-trace` command executes and returns structured trace payload.
- `workflow-context-gate --strict-medium` and `execution-guard --strict-medium` pass with `status_code=0`.

Artifacts:
- `shared/spikes/directive_freshness_manual_20260304_152306/summary.json`
- `shared/spikes/update_plan_sync_smoke_up_sync_20260304_152306/summary.json`
- `shared/spikes/update_plan_freshness_manual_20260304_152306/summary.json`
- `shared/spikes/update_plan_trace_manual_20260304_152542/summary.json`
- `shared/spikes/directive_track_smoke_dir_track_20260304_152312/summary.json`
- `shared/spikes/directive_trace_manual_20260304_152312/summary.json`
- `shared/spikes/workflow_context_gate_parity_smoke_20260304_152318/summary.json`
- `shared/spikes/execution_guard_parity_exec_smoke_20260304_152318/summary.json`

Decision:
- Core lifecycle parity is now present in template wrapper while keeping domain-neutral design.
- Residual gaps are now explicit and intentional: no service/API/observability harness profile in baseline template.
