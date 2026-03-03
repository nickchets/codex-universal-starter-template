---
name: autonomous-refactor-loop
description: Reduce technical debt through evidence-backed, behavior-safe refactor slices with explicit risk, rollback, and verification.
metadata:
  short-description: Autonomous debt reduction with strict safety gates.
  tags: [refactor, tech-debt, architecture, maintainability, risk, verification]
---

# Agent Skill: Autonomous Refactor Loop

## Core Mission

Refactor for clarity and reliability without accidental behavior drift.

Target loop:
`debt map -> options -> smallest-safe slice -> verify parity -> evidence -> board transition`

## Trigger (When To Use)

Use this skill for:
- high-complexity modules,
- duplicated control logic,
- brittle interfaces,
- maintenance hotspots with repeated regressions.

## Boundaries

- Do not mix refactor with unrelated feature expansion.
- Do not change external behavior unless contract update is intentional and documented.
- Do not ship "large cleanup" without slice boundaries.

## Principles

1. Behavior parity by default.
2. Smallest safe diff over big-bang rewrite.
3. Explicit interfaces over hidden coupling.
4. Measurable risk and rollback before implementation.
5. Evidence-backed closeout.

## Required Outputs

- Refactor plan section in `ACTION_PLAN.md` for current card.
- Contract updates if behavior intentionally changes (`PROJECT_MANIFEST.md`).
- Verification evidence in `EVIDENCE_LOG.md`.

## Refactor Workflow

### Phase 1: Debt Mapping

1. Identify hotspot and why it hurts.
2. List coupling points and likely regression vectors.
3. Define "no-change" behavioral invariants.

### Phase 2: Option Set

1. Generate 2-3 refactor options.
2. Compare complexity, risk, reversibility.
3. Choose smallest safe slice.

### Phase 3: Implementation Slice

1. Refactor one bounded segment.
2. Keep interface contracts explicit.
3. Avoid simultaneous wide-scope edits.

### Phase 4: Parity Verification

1. Run baseline verification gate.
2. Run targeted checks for touched flows.
3. Confirm no unintended behavior drift.

### Phase 5: Evidence + Transition

1. Log commands/results/artifacts.
2. Transition board only after evidence.

## Acceptance Criteria

- Refactor objective is achieved with unchanged intended behavior.
- Verification proves parity on affected paths.
- Diff remains understandable and reversible.

## Anti-Patterns

- "Refactor everything" in one cycle.
- Cleanup mixed with unrelated feature logic.
- Removing abstractions without replacement boundaries.
- Closing card without parity evidence.
