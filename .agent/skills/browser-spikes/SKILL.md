---
name: browser-spikes
description: Run bounded browser experiments to resolve UI/anti-bot/layout uncertainty with reproducible artifacts and decision-ready outcomes.
metadata:
  short-description: Time-boxed browser research with evidence outputs.
  tags: [browser, spike, ui, anti-bot, observability, experiments, evidence]
---

# Agent Skill: Browser Spikes (Bounded Uncertainty Resolution)

## Core Mission

Turn unknown browser behavior into known decision facts:

`uncertainty -> hypothesis -> bounded experiment -> artifact evidence -> decision`

## Trigger (When To Use)

Use this skill when:
- selectors/layout are unstable,
- anti-bot behavior is inconsistent,
- browser automation outcome is ambiguous,
- system behavior differs across environments.

## Boundaries

- Do not run unbounded exploratory sessions.
- Do not claim conclusions without artifacts.
- Do not bypass legal/platform restrictions.

## Principles

1. Hypothesis-first experiments.
2. Time-box every spike.
3. Reproduce with exact commands.
4. Save durable artifacts for every conclusion.
5. Convert observations into contract-level decisions.

## Required Outputs

- Spike artifact directory:
  - `shared/spikes/<spike_id>/summary.json`
  - screenshots/html/log extracts as needed.
- Decision note in plan/evidence:
  - what was tested,
  - what was observed,
  - what changed next.

## Spike Workflow

### Phase 1: Spike Definition

1. Write one testable question.
2. Define success and failure signals.
3. Set strict runtime/time budget.

### Phase 2: Experiment Execution

1. Run scripted browser actions.
2. Capture screenshots/DOM/network/logs.
3. Repeat minimal times needed for confidence.

### Phase 3: Evidence Packaging

1. Persist artifacts under one spike directory.
2. Create machine-readable summary (`summary.json`).
3. Tag blocker class if failed (`NETWORK`, `UI`, `ANTIBOT`, `LOCAL`).

### Phase 4: Decision Integration

1. Update `ACTION_PLAN.md` with chosen follow-up.
2. Add evidence block to `EVIDENCE_LOG.md`.
3. Transition board accordingly (`DONE` or `BLOCKED` with unblock condition).

## Acceptance Criteria

- Spike question is answered with artifacts.
- Decision path is clear and reversible.
- No ambiguous "likely" outcomes left unresolved.

## Anti-Patterns

- Random clicking without hypothesis.
- Screenshots without context or command history.
- Long spikes with no decision output.
- Declaring root cause without reproducible run.
