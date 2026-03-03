# Skills & Workflows Operating Guide

This guide explains how skills and workflows are selected and how they integrate with board/evidence contracts.

## Selection Priority

When tags are present, use this order:
1. `#INTAKE` -> `jira-loop`
2. `#TRIZ` -> `triz-ariz-solver`
3. `#REFACTOR` -> `autonomous-refactor-loop`
4. `#SIMPLIFY` -> `code-simplifier` or `/code-simplify-commit`
5. `#SPIKE` -> `browser-spikes`
6. `#FEEDBACK` -> `autonomous-feedback-loop`
7. `#VERIFY` -> `verify-evidence`

No-tag fallback:
- planning/intake/backlog -> `jira-loop`
- contradictions/high-risk decisions -> `triz-ariz-solver`
- debt/architecture cleanup -> `autonomous-refactor-loop`
- cleanup/simplify/readability by commit -> `code-simplifier`
- browser uncertainty/layout/anti-bot -> `browser-spikes`
- debug/restart/runbook hardening -> `autonomous-feedback-loop`
- acceptance/tests/evidence -> `verify-evidence`

## Skills (Detailed)

- `jira-loop`
  - Intake normalization, board mapping, deterministic `DOING/NEXT` control.
- `triz-ariz-solver`
  - Full contradiction-to-decision pipeline with ARIZ deep pass for high-risk cards.
- `autonomous-refactor-loop`
  - Behavior-safe refactor slices with explicit parity verification.
- `code-simplifier`
  - Post-implementation cleanup with strict behavior parity and scoped diffs.
- `browser-spikes`
  - Bounded browser experiments with artifact-driven decisions.
- `autonomous-feedback-loop`
  - Runtime-by-runtime verified debug/test/restart runbook construction.
- `verify-evidence`
  - Command-level acceptance gate and evidence integrity.

Skill sources:
- `.agent/skills/*/SKILL.md`

## Workflows (Operational Playbooks)

- `/jira-intake`
  - Builds execution-ready cards from user directives.
- `/verify-e2e`
  - Runs baseline + scope checks and writes evidence.
- `/multi-stream-mode`
  - Controls multi-lane execution with metrics and WIP limits.
- `/code-simplify-commit`
  - Runs commit-scoped simplification with deterministic verification.
- `/spike-browser-research`
  - Runs bounded uncertainty experiments with reproducible artifacts.

Workflow sources:
- `.agent/workflows/*.md`

## Mandatory Integration Rules

1. Skills/workflows must not bypass board invariants:
   - `DOING == 1`
   - `NEXT <= 3`
2. Any meaningful transition requires evidence linkage in `EVIDENCE_LOG.md`.
3. Contract changes must be reflected in `PROJECT_MANIFEST.md`.
4. Directive traceability must be maintained in `docs/DIRECTIVE_REGISTER.md`.

## Quality Gate

After skill/workflow-driven changes, run:
- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label skills_workflows --strict-medium`
