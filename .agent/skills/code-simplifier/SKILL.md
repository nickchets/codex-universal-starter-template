---
name: code-simplifier
description: Perform behavior-safe post-implementation cleanup using scoped, evidence-backed simplification.
metadata:
  short-description: Reduce accidental complexity after delivery without behavior drift.
  tags: [simplify, cleanup, refactor, maintainability, readability, verification]
---

# Agent Skill: Code Simplifier (Post-Commit Cleanup)

## Core Mission

Simplify recently changed code while preserving behavior and contracts:

`scope lock -> simplify -> parity verify -> evidence -> board-safe transition`

This skill is for cleanup quality, not feature work.

## Trigger (When To Use)

Use this skill when:
- user asks for cleanup/readability improvements,
- recent AI-generated diff is too noisy or over-complicated,
- large feature commit needs a second pass before merge.

Tag router trigger:
- `#SIMPLIFY`

## Boundaries

- Do not add features.
- Do not perform architecture rewrites in this flow.
- Do not expand scope outside selected files unless user asks.
- Do not close work without verification evidence.

## Principles

1. Behavior parity first.
2. Scope discipline (commit-scoped by default).
3. Readability over cleverness.
4. Small reversible diffs.
5. Verification before closure.

## Required Inputs

- Preferred: commit id (`<sha>`).
- Fallback: staged diff or explicit file list from user.

## Required Outputs

- Simplified, behavior-equivalent code in selected scope.
- Verification command output recorded in `EVIDENCE_LOG.md` when cleanup affects execution-critical paths.
- Board state remains valid (`DOING == 1`, `NEXT <= 3`).

## Simplification Workflow

### Phase 1: Scope Lock

1. Resolve target scope:
   - `git show --name-only --pretty=format: <sha>`
2. Capture invariants that must remain unchanged.
3. Exclude unrelated files from this pass.

### Phase 2: Candidate Cleanup Map

Identify simplification opportunities:
- duplicate or near-duplicate branches,
- unnecessary nesting or temporary variables,
- over-abstracted wrappers with no value,
- repeated error handling paths,
- dead code and stale comments.

### Phase 3: Apply Minimal Cleanup

Prefer:
- flattening deeply nested conditionals,
- extracting repeated fragments into small local helpers,
- normalizing naming for consistent intent,
- keeping interfaces stable unless contract update is intentional.

### Phase 4: Verify Parity

Run:
- `./tools/verify_fail_fast.sh`

If scope is narrow and faster checks are enough, run focused checks too, but baseline gate remains mandatory before close.

### Phase 5: Evidence + Handoff

1. Record verification outcome in `EVIDENCE_LOG.md` for meaningful cleanup cards.
2. Keep cleanup commit focused and traceable to source `<sha>`.
3. Transition board only after verification evidence exists.

## Acceptance Criteria

- Code is simpler to read and maintain.
- Intended behavior is unchanged.
- Verification gate passes and evidence is replayable.
- Diff is scoped and reversible.

## Anti-Patterns

- "Cleanup" that sneaks in feature behavior changes.
- Wide formatting churn unrelated to readability problems.
- Mixing unrelated modules in one simplification pass.
- Declaring done without parity verification.
