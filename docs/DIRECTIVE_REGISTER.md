# Directive Register

Purpose:
- store user directives verbatim,
- keep deterministic traceability:
  `directive -> board card -> verification -> evidence`.

## Rules
1. Append every new directive before major implementation.
2. Keep the message verbatim in source field.
3. Map each directive to a verify hook.
4. Close directive only after evidence is linked.

## Directives

| ID | Captured At (UTC) | Verbatim User Message | Intent | Planned Integration | Verify Hook | Status |
| --- | --- | --- | --- | --- | --- | --- |
| DIR-20260303-001 | 2026-03-03T00:00:00Z | "Initialize repository governance baseline" | EXEC_NOW | BOOT-001 | `python3 tools/dev_harness_server.py workflow-context-gate --label dir_001` | IN_PROGRESS |
