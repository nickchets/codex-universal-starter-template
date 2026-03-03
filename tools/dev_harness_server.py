#!/usr/bin/env python3
"""Lightweight governance wrapper for Codex starter repositories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_bootstrap import build_payload


REPO_ROOT = Path(__file__).resolve().parents[1]
DIRECTIVE_REGISTER = REPO_ROOT / "docs" / "DIRECTIVE_REGISTER.md"
CORE_DOCS = [
    REPO_ROOT / "PROJECT_MANIFEST.md",
    REPO_ROOT / "ACTION_PLAN.md",
    REPO_ROOT / "EVIDENCE_LOG.md",
    REPO_ROOT / "DEBUG.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CODEX_RULES.md",
    REPO_ROOT / "docs" / "CONTEXT_SYNC_PROTOCOL.en.md",
    REPO_ROOT / "docs" / "NETWORK_SEARCH_PROTOCOL.en.md",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def utc_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def escape_cell(value: str) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|").strip()


def artifact_dir(prefix: str, label: str) -> Path:
    out = REPO_ROOT / "shared" / "spikes" / f"{prefix}_{label}_{now_ts()}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def persist(prefix: str, label: str, payload: dict[str, Any]) -> dict[str, Any]:
    out_dir = artifact_dir(prefix, label)
    summary = out_dir / "summary.json"
    summary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload["artifact_dir"] = str(out_dir)
    payload["artifact_summary"] = str(summary)
    return payload


def compute_next_directive_id(text: str) -> str:
    today = utc_date()
    max_n = 0
    for m in re.finditer(r"\|\s*DIR-(\d{8})-(\d{3})\s*\|", text):
        d = m.group(1)
        n = int(m.group(2))
        if d == today and n > max_n:
            max_n = n
    return f"DIR-{today}-{max_n + 1:03d}"


def ensure_directive_register() -> None:
    if DIRECTIVE_REGISTER.exists():
        return
    DIRECTIVE_REGISTER.parent.mkdir(parents=True, exist_ok=True)
    DIRECTIVE_REGISTER.write_text(
        "\n".join(
            [
                "# Directive Register",
                "",
                "| ID | Captured At (UTC) | Verbatim User Message | Intent | Planned Integration | Verify Hook | Status |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def directive_sync(message: str, intent: str, planned_integration: str, label: str) -> dict[str, Any]:
    ensure_directive_register()
    current = DIRECTIVE_REGISTER.read_text(encoding="utf-8")
    directive_id = compute_next_directive_id(current)
    captured_at = now_iso()
    verify_hook = f"python3 tools/dev_harness_server.py workflow-context-gate --label {label}"
    row = (
        f"| {directive_id} | {captured_at} | \"{escape_cell(message)}\" | "
        f"{escape_cell(intent)} | {escape_cell(planned_integration)} | "
        f"`{escape_cell(verify_hook)}` | IN_PROGRESS |"
    )
    updated = current.rstrip() + "\n" + row + "\n"
    DIRECTIVE_REGISTER.write_text(updated, encoding="utf-8")
    return {
        "created_at": captured_at,
        "status_code": 0,
        "directive_id": directive_id,
        "verify_hook": verify_hook,
        "row": row,
        "register_path": str(DIRECTIVE_REGISTER),
    }


def governance_audit(label: str) -> dict[str, Any]:
    bootstrap = build_payload()
    checks: list[dict[str, Any]] = []
    for path in CORE_DOCS:
        checks.append({"name": f"exists:{path.relative_to(REPO_ROOT)}", "ok": path.exists()})
    checks.append({"name": "bootstrap_status_ok", "ok": int(bootstrap.get("status_code", 1)) == 0})
    checks.append({"name": "board_invariants_ok", "ok": bool(bootstrap.get("board_invariants_ok"))})
    checks.append(
        {
            "name": "doing_has_task_breakdown",
            "ok": bool(bootstrap.get("doing_card_has_task_breakdown")),
        }
    )
    ok = all(bool(x.get("ok")) for x in checks)
    return {
        "created_at": now_iso(),
        "status_code": 0 if ok else 1,
        "label": label,
        "checks": checks,
        "board_counts": bootstrap.get("board_counts", {}),
        "bootstrap_summary": bootstrap,
    }


def governance_quality_audit(label: str, strict_medium: bool) -> dict[str, Any]:
    audit = governance_audit(label)
    text_checks: list[dict[str, Any]] = []
    min_lines = {
        "PROJECT_MANIFEST.md": 25,
        "ACTION_PLAN.md": 30,
        "EVIDENCE_LOG.md": 10,
        "DEBUG.md": 8,
    }
    for rel, min_count in min_lines.items():
        path = REPO_ROOT / rel
        content = path.read_text(encoding="utf-8") if path.exists() else ""
        text_checks.append(
            {
                "name": f"line_count:{rel}",
                "ok": len(content.splitlines()) >= min_count,
                "current": len(content.splitlines()),
                "min_required": min_count,
            }
        )

    dual_lang_docs = [
        "docs/AGENT_BOOTSTRAP_PROTOCOL.en.md",
        "docs/AGENT_BOOTSTRAP_PROTOCOL.ru.md",
        "docs/CONTEXT_SYNC_PROTOCOL.en.md",
        "docs/CONTEXT_SYNC_PROTOCOL.ru.md",
        "docs/AGENT_STARTUP_QUESTIONNAIRE.en.md",
        "docs/AGENT_STARTUP_QUESTIONNAIRE.ru.md",
    ]
    for rel in dual_lang_docs:
        text_checks.append({"name": f"exists:{rel}", "ok": (REPO_ROOT / rel).exists()})

    has_todo_markers = False
    for path in [REPO_ROOT / "AGENTS.md", REPO_ROOT / "CODEX_RULES.md"]:
        if path.exists() and "TODO" in path.read_text(encoding="utf-8"):
            has_todo_markers = True
    text_checks.append({"name": "no_todo_in_governance_docs", "ok": not has_todo_markers})

    all_ok = int(audit.get("status_code", 1)) == 0 and all(bool(x.get("ok")) for x in text_checks)
    status_code = 0 if all_ok else (2 if strict_medium else 1)

    return {
        "created_at": now_iso(),
        "status_code": status_code,
        "label": label,
        "strict_medium": bool(strict_medium),
        "governance_audit_status": audit.get("status_code"),
        "checks": text_checks,
    }


def context_bootstrap(label: str) -> dict[str, Any]:
    payload = build_payload()
    return {
        "created_at": now_iso(),
        "status_code": int(payload.get("status_code", 1)),
        "label": label,
        "summary": payload,
    }


def workflow_context_gate(
    label: str,
    strict_medium: bool = False,
    directive_message: str | None = None,
) -> dict[str, Any]:
    directive_payload = None
    if directive_message:
        directive_payload = directive_sync(
            message=directive_message,
            intent=f"AUTO:{directive_message[:80]}",
            planned_integration="AUTO integration into current board card",
            label=f"{label}_directive",
        )

    audit = governance_audit(f"{label}_audit")
    quality = governance_quality_audit(f"{label}_quality", strict_medium=strict_medium)
    bootstrap = context_bootstrap(f"{label}_bootstrap")

    status_code = 0
    for code in [
        int(audit.get("status_code", 1)),
        int(quality.get("status_code", 1)),
        int(bootstrap.get("status_code", 1)),
    ]:
        if code != 0:
            status_code = code
            break

    return {
        "created_at": now_iso(),
        "status_code": status_code,
        "label": label,
        "strict_medium": bool(strict_medium),
        "directive_sync": directive_payload,
        "governance_audit": audit,
        "governance_quality_audit": quality,
        "context_bootstrap": bootstrap,
    }


def print_and_exit(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return int(payload.get("status_code", 1))


def main() -> int:
    parser = argparse.ArgumentParser(description="Governance wrapper commands for Codex template.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_dir = sub.add_parser("directive-sync")
    p_dir.add_argument("--message", required=True)
    p_dir.add_argument("--intent", required=True)
    p_dir.add_argument("--planned-integration", required=True)
    p_dir.add_argument("--label", required=True)

    p_audit = sub.add_parser("governance-audit")
    p_audit.add_argument("--label", default="manual")

    p_quality = sub.add_parser("governance-quality-audit")
    p_quality.add_argument("--label", default="manual")
    p_quality.add_argument("--strict-medium", action="store_true")

    p_bootstrap = sub.add_parser("context-bootstrap")
    p_bootstrap.add_argument("--label", default="manual")

    p_gate = sub.add_parser("workflow-context-gate")
    p_gate.add_argument("--label", default="manual")
    p_gate.add_argument("--strict-medium", action="store_true")
    p_gate.add_argument("--directive-message")

    p_exec = sub.add_parser("execution-guard")
    p_exec.add_argument("--label", default="manual")
    p_exec.add_argument("--strict-medium", action="store_true")
    p_exec.add_argument("--directive-message")

    args = parser.parse_args()

    if args.cmd == "directive-sync":
        payload = directive_sync(args.message, args.intent, args.planned_integration, args.label)
        payload = persist("directive_sync", args.label, payload)
        return print_and_exit(payload)

    if args.cmd == "governance-audit":
        payload = governance_audit(args.label)
        payload = persist("governance_audit", args.label, payload)
        return print_and_exit(payload)

    if args.cmd == "governance-quality-audit":
        payload = governance_quality_audit(args.label, strict_medium=bool(args.strict_medium))
        payload = persist("governance_quality_audit", args.label, payload)
        return print_and_exit(payload)

    if args.cmd == "context-bootstrap":
        payload = context_bootstrap(args.label)
        payload = persist("context_bootstrap", args.label, payload)
        return print_and_exit(payload)

    if args.cmd in ("workflow-context-gate", "execution-guard"):
        payload = workflow_context_gate(
            label=args.label,
            strict_medium=bool(args.strict_medium),
            directive_message=args.directive_message,
        )
        payload = persist("workflow_context_gate", args.label, payload)
        return print_and_exit(payload)

    return 1


if __name__ == "__main__":
    sys.exit(main())
