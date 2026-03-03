---
name: jira-loop
description: Turn raw user requests into execution-ready board cards and synchronize contracts/evidence before coding starts.
metadata:
  short-description: Deterministic intake and board transaction control.
  tags: [planning, intake, board, governance, evidence, execution]
---

# Agent Skill: Jira Loop (Deterministic Intake)

## Core Mission

Your job is to convert ambiguous user intent into deterministic execution state:

`request -> objective -> board card -> verify hook -> evidence plan`

Before implementation starts, make sure contracts and board state are valid.

## Trigger (When To Use)

Use this skill when the request is about:
- planning or intake,
- backlog refresh,
- task decomposition,
- board state recovery after drift.

## Boundaries (What This Skill Does Not Do)

- Do not implement major feature code here unless user explicitly asks.
- Do not move cards directly to `DONE` without verification and evidence.
- Do not keep multiple active `DOING` cards.

## Principles

1. Contract-first
   - `PROJECT_MANIFEST.md` defines objective and acceptance.
2. One active task
   - `DOING == 1`, `NEXT <= 3`.
3. Traceability
   - Every directive must map to card + verify hook.
4. Smallest executable unit
   - Break scope to task-level cards with explicit outcomes.
5. Evidence-ready planning
   - Define verification before coding starts.

## Required Outputs

- Updated `ACTION_PLAN.md` with:
  - one `DOING` card,
  - up to three `NEXT` cards,
  - concrete `TASK BREAKDOWN`.
- Updated `docs/DIRECTIVE_REGISTER.md` with verbatim directive row.
- Verify commands planned for `EVIDENCE_LOG.md`.

## Workflow

### Phase 1: Intake Normalization

1. Capture user objective, DoD, constraints, non-goals.
2. Classify intent:
   - `EXEC_NOW`, or
   - `WORKFLOW_IDEA`.
3. Record directive in register.

### Phase 2: Board Mapping

1. Generate or refresh card IDs.
2. Enforce board invariants (`DOING == 1`, `NEXT <= 3`).
3. Add 3-7 concrete subtasks for current `DOING`.

### Phase 3: Verification Plan

1. Define baseline gate command.
2. Define scope-specific verify command(s).
3. Define expected artifacts and evidence block location.

### Phase 4: Handoff To Execution

1. Confirm board transition path is valid.
2. Confirm no hidden dependencies remain.
3. Hand off to implementation loop.

## Acceptance Criteria

- Current card is task-level and actionable.
- `TASK BREAKDOWN` exists for current `DOING`.
- Directive traceability row exists and is coherent.
- Verify hook is explicit and runnable.

## Anti-Patterns

- Planning without verify hooks.
- Overloaded epics in `DOING`.
- Hidden scope changes not reflected in contracts.
- Transitioning board state without evidence intent.
