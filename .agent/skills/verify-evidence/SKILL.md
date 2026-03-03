---
name: verify-evidence
description: Execute deterministic verification gates and record machine-checkable evidence before any card can be closed.
metadata:
  short-description: Verification discipline and evidence integrity gate.
  tags: [verification, testing, acceptance, evidence, quality, gates]
---

# Agent Skill: Verify-Evidence (Deterministic Acceptance)

## Core Mission

Your job is to prove changes, not describe them.

Every completion claim must map to:
- command(s) that were run,
- observed result,
- artifact path(s),
- board transition eligibility.

## Trigger (When To Use)

Use this skill when:
- closing or advancing cards,
- validating risky changes,
- running acceptance checks,
- preparing release/merge decisions.

## Boundaries

- Do not mark work complete on "looks good".
- Do not skip evidence because tests are expensive.
- Do not bury failures in summary text.

## Principles

1. Verify first, claim second.
2. Prefer deterministic commands over manual checks.
3. Keep artifacts durable and path-addressable.
4. Record both PASS and FAIL honestly.
5. Keep acceptance criteria measurable.

## Required Outputs

- Updated `EVIDENCE_LOG.md` block:
  - scope,
  - commands,
  - results,
  - artifact paths,
  - decision.
- Updated card status in `ACTION_PLAN.md` only after evidence is written.

## Verification Workflow

### Phase 1: Baseline Gate

Run:
- `./tools/verify_fail_fast.sh`

If baseline fails:
- stop state transition,
- classify failure and record artifacts.

### Phase 2: Scope-Specific Checks

1. Identify checks tied to the changed scope.
2. Run explicit command list.
3. Capture outputs to durable artifact paths when needed.

### Phase 3: Evidence Recording

Add evidence block with:
- exact commands run,
- PASS/FAIL per command,
- artifact links,
- outcome decision.

### Phase 4: Transition Gate

Allow `DOING->DONE` only if:
- baseline passed,
- scope checks passed (or approved degraded policy exists),
- evidence block is present.

## Acceptance Criteria

- Evidence is sufficient for a new agent to replay the decision.
- Artifact paths are valid and reproducible.
- No board closure without verify proof.

## Anti-Patterns

- "Tested manually" without reproducible steps.
- Aggregated PASS with hidden failing command.
- Card closure before evidence append.
- Missing artifact pointers for non-trivial checks.
