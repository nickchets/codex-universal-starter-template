---
name: triz-ariz-solver
description: Resolve high-risk or contradictory tasks using full TRIZ/ARIZ decomposition with explicit decision, rollback, and verification gates.
metadata:
  short-description: Contradiction-driven decision engine for hard engineering tasks.
  tags: [triz, ariz, contradictions, architecture, risk, decision, verification]
---

# Agent Skill: TRIZ-ARIZ Solver (Project Pride Edition)

## Core Mission

Your job is to transform ambiguous or contradictory requests into a defensible engineering decision packet:

`contradiction -> models -> candidates -> smallest-safe decision -> verification -> evidence`

This is not a brainstorming skill.  
This is an execution-grade decision skill.

## Trigger (When To Use)

Use this skill when at least one condition is true:
- requirements conflict ("must be faster and safer", "ship now but zero risk"),
- failure causes are unclear,
- architecture choice has non-obvious tradeoffs,
- repeated regressions indicate systemic contradiction.

## Boundaries

- Do not jump into implementation before contradiction model is explicit.
- Do not close analysis with a single favorite option.
- Do not produce "advice-only" output; produce decision-ready artifacts.

## Principles

1. Contradiction-first
   - If no contradiction is written, analysis is incomplete.
2. IFR-driven direction
   - Define ideal state before proposing mechanisms.
3. Resource realism
   - Use available system resources before adding complexity.
4. Option plurality
   - Generate 3-7 candidate paths, not one.
5. Smallest-safe commitment
   - Prefer reversible, measurable slices.
6. Verification before transition
   - No `DOING->DONE` without evidence-backed gate pass.

## Required Artifacts

- `shared/triz/<timestamp>_<slug>/TRIZ_PACKET.md`
- `shared/triz/<timestamp>_<slug>/decision_matrix.json`
- `shared/triz/<timestamp>_<slug>/verify_plan.md`
- `ACTION_PLAN.md` update for selected decision path.

If `shared/triz` does not exist, create it.

## Canonical Workflow

### Phase 1: Problem Framing

1. State objective and measurable DoD.
2. State constraints and non-goals.
3. Write IF-THEN-BUT contradiction.

Template:
- IF we `<action A>`, THEN we gain `<benefit>`, BUT we lose `<harm>`.

### Phase 2: Physical Contradiction

1. Identify parameter that must be in opposite states.
2. Express contradiction explicitly:
   - object/parameter must be `X` and `not-X`.
3. Select separation strategy candidates:
   - in time,
   - in space,
   - by condition,
   - by system/subsystem levels.

### Phase 3: IFR + Resource Inventory

1. Write IFR (ideal final result) in one sentence.
2. Enumerate resources:
   - existing components,
   - data/telemetry,
   - time windows,
   - environment/runtime controls,
   - human/operator affordances.
3. Mark missing critical resources.

### Phase 4: Candidate Generation (3-7)

For each candidate, define:
- mechanism,
- expected gain,
- expected risk,
- complexity cost,
- reversibility,
- verification cost.

Use TRIZ lenses when relevant:
- inventive principles mapping,
- separation principles,
- system transition trends,
- Su-Field transformation ideas (optional but encouraged for deep technical blocks).

### Phase 5: Decision Matrix

Score each candidate (0-5) on:
- risk,
- implementation effort,
- reversibility,
- observability,
- expected impact on DoD.

Select:
- primary path,
- fallback path,
- rollback trigger.

### Phase 6: Verification Contract

Define exact gate before execution:
- baseline verify command,
- scope-specific tests/probes,
- required artifacts,
- explicit PASS/FAIL threshold.

### Phase 7: Board Integration

1. Map selected path to current `DOING` card.
2. Add subtask sequence in `TASK BREAKDOWN`.
3. Add evidence hook references.

## ARIZ Deep Pass (Mandatory For High-Risk Cards)

When scope is architecture-level or regression-critical, run explicit ARIZ pass:

- A1: Situation model and objective boundary
- A2: Contradiction model and harmful interaction
- A3: IFR and ideal mechanism sketch
- A4: Resource deep inventory (space/time/system fields)
- A5: Transformation options and separation strategy
- A6: Candidate stress test (failure modes and reversibility)
- A7: Final decision + rollout + rollback + verify gates

If any stage is skipped, decision must be marked provisional and cannot close the card.

## Acceptance Criteria

TRIZ cycle is considered complete only if:
- contradiction is explicit and testable,
- IFR exists and is relevant,
- at least 3 candidates are evaluated,
- one primary + one fallback + rollback trigger are defined,
- verify gate is command-level explicit,
- artifacts are persisted and linked from plan/evidence.

## Anti-Patterns

- "Best practice says so" without contradiction modeling.
- Single-option decision with no fallback.
- Architecture choice without rollback trigger.
- Long theoretical write-up with no verify command.
- Skipping board/evidence integration after decision.

## Fast Output Skeleton

Use this structure inside `TRIZ_PACKET.md`:

1. Objective / DoD
2. Constraints / Non-goals
3. IF-THEN-BUT
4. Physical contradiction
5. IFR
6. Resource inventory
7. Candidate matrix (3-7)
8. Selected path + fallback + rollback
9. Verify plan
10. Board mapping
