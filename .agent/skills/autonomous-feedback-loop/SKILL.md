---
name: autonomous-feedback-loop
description: Discover, validate, and document verified debug/test/restart feedback loops for every runtime. Only proven methods are accepted.
metadata:
  short-description: Build an evidence-backed, runtime-by-runtime debug runbook.
  tags: [debugging, runbook, observability, testing, feedback-loop, automation, agent]
---

# Agent Skill: Autonomous Feedback Loop (Universal)

## Core Mission

Your job is to build deterministic feedback loops for every runtime in the repository:

`discover runtime -> verify observation/control methods -> document only proven methods`

Primary rule:
- Nothing is documented as working until you run it and verify output.

## Trigger (When To Use)

Use this skill when:
- debugging is slow or inconsistent,
- restart/reload behavior is unclear,
- tests are flaky due to unclear runtime state,
- new runtime/environment is introduced,
- team asks for a verified DEBUG/runbook baseline.

## Boundaries

- Do not document "theoretical" methods.
- Do not keep dev backdoors enabled in production paths.
- Do not skip artifact capture for non-trivial runtime checks.

## Principles

1. Verify before documenting
   - "Should work" is not evidence.
2. Runtime coverage
   - each runtime gets explicit start/stop/observe/verify path.
3. Fastest deterministic loop
   - prefer eval/repl/probe + rebuild/restart confirmation.
4. Safety
   - debug hooks dev-only and removable.
5. Reproducibility
   - commands and outputs must be replayable by another agent.

## Required Outputs

- Updated `DEBUG.md` with verified methods only.
- Evidence block in `EVIDENCE_LOG.md` with:
  - commands run,
  - observed output,
  - artifact paths.
- Optional helper scripts under `tools/` or `debug/` when needed.

## Canonical Workflow

### Phase 1: Runtime Discovery

1. Detect runtimes via manifests/entrypoints.
2. Map runtime types (api, worker, ui, cli, background, etc.).
3. Note how each runtime is started and controlled.

### Phase 2: Control Loop Verification

For each runtime verify:

1. Start/stop/restart
   - run command,
   - confirm process/port/log signal,
   - confirm clean stop and restart.
2. Observation path
   - add/trigger a log probe,
   - confirm where output appears.
3. Eval/probe path
   - use existing repl/eval endpoint or create a bounded dev probe.
4. Rebuild + restart activation
   - change code,
   - rebuild/restart,
   - confirm new behavior is active.
5. Test path
   - run available tests for that runtime.

### Phase 3: Harden Fast Feedback

1. Prefer scripted checks over manual clicking.
2. Create helper commands/scripts for repeated debug steps.
3. Remove temporary test probes not intended for runbook.

### Phase 4: Runbook + Evidence

1. Write verified steps into `DEBUG.md`.
2. Add evidence block with commands/artifacts.
3. Link to updated runbook from governance docs if needed.

## Acceptance Criteria

Skill execution is complete only if:
- each targeted runtime has a verified control/observe path,
- all runbook entries are command-level reproducible,
- evidence exists for claimed methods,
- no unsafe debug mechanism is left open.

## Anti-Patterns

- documenting from source reading without execution,
- hot-reload assumptions without activation proof,
- missing command output details,
- keeping permanent insecure eval endpoints.

## Minimal Verification Commands

- `./tools/verify_fail_fast.sh`
- `python3 tools/dev_harness_server.py workflow-context-gate --label feedback_loop --strict-medium`
