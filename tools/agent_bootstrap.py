#!/usr/bin/env python3
"""Generate first-run governance summary and enforce board invariants."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "PROJECT_MANIFEST.md"
ACTION_PLAN = REPO_ROOT / "ACTION_PLAN.md"
EVIDENCE = REPO_ROOT / "EVIDENCE_LOG.md"
DEBUG = REPO_ROOT / "DEBUG.md"
ADR_INDEX = REPO_ROOT / "docs" / "ADR" / "README.md"
CONTEXT_SYNC_EN = REPO_ROOT / "docs" / "CONTEXT_SYNC_PROTOCOL.en.md"
DIRECTIVE_REGISTER = REPO_ROOT / "docs" / "DIRECTIVE_REGISTER.md"

DOING_HEADER = "### DOING (exactly 1 card)"
NEXT_HEADER = "### NEXT (maximum 3 cards)"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def count_lines(text: str) -> int:
    return len(text.splitlines())


def extract_section(lines: list[str], header: str) -> list[str]:
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i + 1
            break
    if start is None:
        return []
    out: list[str] = []
    for line in lines[start:]:
        if line.strip().startswith("### "):
            break
        out.append(line)
    return out


def extract_card_lines(section_lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in section_lines:
        s = line.strip()
        if re.match(r"^- \[[ xX]\] \*\*.+\*\*$", s):
            out.append(s)
    return out


def extract_card_id(card_line: str) -> str:
    m = re.search(r"\*\*(.+)\*\*", card_line)
    if not m:
        return ""
    title = m.group(1).strip()
    m2 = re.search(r"([A-Z]+-[0-9]+)", title)
    return m2.group(1) if m2 else title


def doing_has_breakdown(action_plan_text: str, doing_card_line: str) -> bool:
    card_id = extract_card_id(doing_card_line)
    if not card_id:
        return False
    pattern = re.compile(rf"^###\s+{re.escape(card_id)}\s*$", flags=re.MULTILINE)
    return bool(pattern.search(action_plan_text))


def build_payload() -> dict[str, Any]:
    manifest = read_text(MANIFEST)
    action_plan = read_text(ACTION_PLAN)
    evidence = read_text(EVIDENCE)
    debug = read_text(DEBUG)
    adr = read_text(ADR_INDEX)
    context_sync = read_text(CONTEXT_SYNC_EN)
    directives = read_text(DIRECTIVE_REGISTER)

    files_ok = all(
        p.exists()
        for p in [MANIFEST, ACTION_PLAN, EVIDENCE, DEBUG, ADR_INDEX, CONTEXT_SYNC_EN, DIRECTIVE_REGISTER]
    )

    lines = action_plan.splitlines()
    doing_cards = extract_card_lines(extract_section(lines, DOING_HEADER))
    next_cards = extract_card_lines(extract_section(lines, NEXT_HEADER))
    doing_count = len(doing_cards)
    next_count = len(next_cards)

    doing_card_line = doing_cards[0] if doing_cards else ""
    board_invariants_ok = doing_count == 1 and next_count <= 3
    has_breakdown = doing_has_breakdown(action_plan, doing_card_line)

    required_sections = [
        ("ACTION_PLAN has board header", "## PROJECT BOARD" in action_plan),
        ("ACTION_PLAN has task breakdown", "## TASK BREAKDOWN" in action_plan),
        ("MANIFEST has objective", "## 2. Objective + DoD" in manifest),
        ("EVIDENCE has at least one block", "## Evidence (" in evidence),
        ("DEBUG has commands", "```bash" in debug),
        ("ADR index exists", bool(adr.strip())),
        ("Context sync protocol exists", bool(context_sync.strip())),
        ("Directive register has table", "| ID | Captured At (UTC) |" in directives),
    ]

    checks = [{"name": name, "ok": bool(ok)} for name, ok in required_sections]
    checks_ok = all(x["ok"] for x in checks)
    status_code = 0 if files_ok and board_invariants_ok and has_breakdown and checks_ok else 1

    return {
        "created_at": now_iso(),
        "repo_root": str(REPO_ROOT),
        "status_code": status_code,
        "board_counts": {"DOING": doing_count, "NEXT": next_count},
        "board_invariants_ok": board_invariants_ok,
        "doing_card_has_task_breakdown": has_breakdown,
        "files_exist_ok": files_ok,
        "checks": checks,
        "line_counts": {
            "PROJECT_MANIFEST.md": count_lines(manifest),
            "ACTION_PLAN.md": count_lines(action_plan),
            "EVIDENCE_LOG.md": count_lines(evidence),
            "DEBUG.md": count_lines(debug),
            "docs/DIRECTIVE_REGISTER.md": count_lines(directives),
        },
        "quick_links": [
            "PROJECT_MANIFEST.md",
            "docs/ADR/README.md",
            "ACTION_PLAN.md",
            "EVIDENCE_LOG.md",
            "DEBUG.md",
            "docs/CONTEXT_SYNC_PROTOCOL.en.md",
            "docs/DIRECTIVE_REGISTER.md",
        ],
        "recommended_commands": [
            "python3 tools/agent_bootstrap.py",
            "python3 tools/dev_harness_server.py workflow-context-gate --label bootstrap",
            "./tools/verify_fail_fast.sh",
        ],
    }


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines: list[str] = []
    lines.append(f"# Agent Bootstrap Summary ({payload.get('created_at')})")
    lines.append("")
    lines.append(f"- status_code: {payload.get('status_code')}")
    lines.append(f"- board_invariants_ok: {payload.get('board_invariants_ok')}")
    lines.append(f"- doing_card_has_task_breakdown: {payload.get('doing_card_has_task_breakdown')}")
    lines.append(f"- files_exist_ok: {payload.get('files_exist_ok')}")
    lines.append(f"- board_counts: {json.dumps(payload.get('board_counts', {}), ensure_ascii=False)}")
    lines.append("")
    lines.append("## Checks")
    for row in payload.get("checks", []):
        lines.append(f"- {row.get('name')}: {'PASS' if row.get('ok') else 'FAIL'}")
    lines.append("")
    lines.append("## Commands")
    for cmd in payload.get("recommended_commands", []):
        lines.append(f"- `{cmd}`")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def persist_payload(payload: dict[str, Any], label: str) -> Path:
    ts = now_utc()
    out_dir = REPO_ROOT / "shared" / "spikes" / f"agent_bootstrap_{label}_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_json = out_dir / "summary.json"
    summary_md = out_dir / "summary.md"
    summary_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(summary_md, payload)
    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate bootstrap context summary.")
    parser.add_argument("--label", default="manual", help="Artifact label suffix.")
    parser.add_argument("--no-persist", action="store_true", help="Do not write artifacts.")
    args = parser.parse_args()

    payload = build_payload()
    artifact_dir = None
    if not args.no_persist:
        artifact_dir = persist_payload(payload, args.label)
        payload["artifact_dir"] = str(artifact_dir)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return int(payload.get("status_code", 1))


if __name__ == "__main__":
    sys.exit(main())
