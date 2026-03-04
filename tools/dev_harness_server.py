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
ACTION_PLAN = REPO_ROOT / "ACTION_PLAN.md"
DIRECTIVE_REGISTER = REPO_ROOT / "docs" / "DIRECTIVE_REGISTER.md"
HARNESS_DIR = REPO_ROOT / "shared" / "harness"
DIRECTIVE_LIFECYCLE = HARNESS_DIR / "directive_lifecycle.jsonl"
UPDATE_PLAN_LIFECYCLE = HARNESS_DIR / "update_plan_lifecycle.jsonl"

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

DEFAULT_CONTEXT_FRESHNESS_MAX_AGE_S = 43_200
DEFAULT_PLAN_FRESHNESS_MAX_AGE_S = 21_600
DIRECTIVE_PHASES = ("thought", "integrated", "executed")
UPDATE_PLAN_STATUSES = ("IN_PROGRESS", "DONE", "BLOCKED")
UPDATE_PLAN_STEP_STATUSES = ("pending", "in_progress", "completed", "blocked")

DIRECTIVE_ROW_RE = re.compile(
    r'^\|\s*(DIR-\d{8}-\d{3})\s*\|\s*(.*?)\s*\|\s*"(.*?)"\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*`?(.*?)`?\s*\|\s*(.*?)\s*\|$'
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def utc_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def parse_iso_utc(raw: str) -> datetime | None:
    value = str(raw or "").strip()
    if not value:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(value)
    except Exception:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def status_code(raw: Any, default: int = 1) -> int:
    try:
        return int(raw)
    except Exception:
        return int(default)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def ensure_harness_dir() -> None:
    HARNESS_DIR.mkdir(parents=True, exist_ok=True)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            row = json.loads(s)
        except Exception:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    ensure_harness_dir()
    with path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(row, ensure_ascii=False) + "\n")


def escape_cell(value: str) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|").strip()


def escape_quoted(value: str) -> str:
    return escape_cell(value).replace('"', "'")


def unescape_cell(value: str) -> str:
    return str(value).replace("\\|", "|").strip()


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


def normalize_text(raw: str) -> str:
    return re.sub(r"\s+", " ", str(raw or "").strip()).lower()


def extract_card_id(raw_card: str) -> str:
    match = re.search(r"([A-Z0-9]+(?:-[A-Z0-9]+)+)", str(raw_card or ""))
    return str(match.group(1) if match else "").strip()


def current_doing_card() -> str:
    text = read_text(ACTION_PLAN)
    doing_match = re.search(r"^### DOING.*?(?=^### |\Z)", text, flags=re.M | re.S)
    section = str(doing_match.group(0) if doing_match else "")
    card_match = re.search(r"- \[[ xX]\] \*\*(.+?)\*\*", section, flags=re.M)
    return str(card_match.group(1) if card_match else "").strip()


def current_doing_card_id() -> str:
    return extract_card_id(current_doing_card())


def compute_next_directive_id(text: str) -> str:
    today = utc_date()
    max_n = 0
    for match in re.finditer(r"\|\s*DIR-(\d{8})-(\d{3})\s*\|", text):
        day = str(match.group(1))
        ordinal = int(match.group(2))
        if day == today and ordinal > max_n:
            max_n = ordinal
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


def parse_directive_line(line: str) -> dict[str, Any] | None:
    match = DIRECTIVE_ROW_RE.match(str(line or "").strip())
    if not match:
        return None
    return {
        "directive_id": str(match.group(1)).strip(),
        "captured_at": str(match.group(2)).strip(),
        "message": unescape_cell(str(match.group(3))),
        "intent": unescape_cell(str(match.group(4))),
        "planned_integration": unescape_cell(str(match.group(5))),
        "verify_hook": unescape_cell(str(match.group(6)).strip("`")),
        "status": str(match.group(7)).strip(),
        "_raw": str(line).rstrip("\n"),
    }


def directive_rows(register_text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in str(register_text or "").splitlines():
        row = parse_directive_line(line)
        if isinstance(row, dict):
            rows.append(row)
    return rows


def directive_row_by_id(register_text: str, directive_id: str) -> dict[str, Any] | None:
    did = str(directive_id or "").strip().upper()
    if not did:
        return None
    for row in reversed(directive_rows(register_text)):
        if str(row.get("directive_id") or "").strip().upper() == did:
            return row
    return None


def directive_latest_row_by_message(register_text: str, message: str) -> dict[str, Any] | None:
    probe = normalize_text(message)
    if not probe:
        return None
    for row in reversed(directive_rows(register_text)):
        if normalize_text(str(row.get("message") or "")) == probe:
            return row
    return None


def directive_exists(directive_id: str) -> bool:
    ensure_directive_register()
    text = read_text(DIRECTIVE_REGISTER)
    return directive_row_by_id(text, directive_id) is not None


def update_directive_status(directive_id: str, status: str) -> bool:
    did = str(directive_id or "").strip().upper()
    target_status = str(status or "").strip()
    if not did or not target_status:
        return False
    ensure_directive_register()
    lines = read_text(DIRECTIVE_REGISTER).splitlines()
    changed = False
    out_lines: list[str] = []
    for line in lines:
        row = parse_directive_line(line)
        if not isinstance(row, dict):
            out_lines.append(line)
            continue
        if str(row.get("directive_id") or "").strip().upper() != did:
            out_lines.append(line)
            continue
        new_line = (
            f'| {row.get("directive_id")} | {row.get("captured_at")} | '
            f'"{escape_quoted(str(row.get("message") or ""))}" | '
            f'{escape_cell(str(row.get("intent") or ""))} | '
            f'{escape_cell(str(row.get("planned_integration") or ""))} | '
            f'`{escape_cell(str(row.get("verify_hook") or ""))}` | '
            f"{escape_cell(target_status)} |"
        )
        out_lines.append(new_line)
        changed = True
    if changed:
        DIRECTIVE_REGISTER.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")
    return changed


def append_directive_lifecycle_event(
    *,
    directive_id: str,
    phase: str,
    note: str,
    label: str,
    doing_card: str,
) -> dict[str, Any]:
    phase_norm = str(phase or "").strip().lower()
    if phase_norm not in DIRECTIVE_PHASES and phase_norm != "captured":
        raise ValueError(f"Invalid directive phase: {phase_norm}")
    row = {
        "created_at": now_iso(),
        "directive_id": str(directive_id or "").strip().upper(),
        "phase": phase_norm,
        "note": str(note or "").strip(),
        "label": str(label or "").strip(),
        "doing_card": str(doing_card or "").strip(),
        "doing_card_id": extract_card_id(doing_card),
    }
    append_jsonl(DIRECTIVE_LIFECYCLE, row)
    return row


def directive_lifecycle_events(directive_id: str = "") -> list[dict[str, Any]]:
    did = str(directive_id or "").strip().upper()
    events = read_jsonl(DIRECTIVE_LIFECYCLE)
    if not did:
        return events
    return [row for row in events if str(row.get("directive_id") or "").strip().upper() == did]


def directive_sync(
    *,
    message: str,
    intent: str,
    planned_integration: str,
    label: str,
    verify_hook: str = "",
    status: str = "IN_PROGRESS",
    intent_classification: str = "AUTO",
    captured_at_utc: str = "",
    auto_fill: bool = True,
) -> dict[str, Any]:
    ensure_directive_register()
    current = read_text(DIRECTIVE_REGISTER)
    directive_id = compute_next_directive_id(current)
    doing_card = current_doing_card()
    doing_card_id = extract_card_id(doing_card)

    msg = str(message or "").strip()
    if not msg:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "error": "directive message is empty",
            "register_path": str(DIRECTIVE_REGISTER),
        }

    intent_text = str(intent or "").strip()
    if auto_fill and not intent_text:
        intent_text = f"{str(intent_classification or 'AUTO').strip().upper()}: {msg[:80]}"

    integration_text = str(planned_integration or "").strip()
    if auto_fill and not integration_text:
        integration_text = "AUTO integration into current board card"
    if doing_card_id and f"[card: {doing_card_id}]" not in integration_text:
        integration_text = f"{integration_text}; [card: {doing_card_id}]".strip("; ")

    verify = str(verify_hook or "").strip()
    if auto_fill and not verify:
        verify = f"python3 tools/dev_harness_server.py workflow-context-gate --label {label}"

    captured_at = str(captured_at_utc or "").strip() or now_iso()
    status_text = str(status or "IN_PROGRESS").strip().upper()
    row = (
        f'| {directive_id} | {captured_at} | "{escape_quoted(msg)}" | '
        f"{escape_cell(intent_text)} | {escape_cell(integration_text)} | "
        f"`{escape_cell(verify)}` | {escape_cell(status_text)} |"
    )

    updated = current.rstrip() + "\n" + row + "\n"
    DIRECTIVE_REGISTER.write_text(updated, encoding="utf-8")
    lifecycle_row = append_directive_lifecycle_event(
        directive_id=directive_id,
        phase="captured",
        note="register append",
        label=str(label),
        doing_card=doing_card,
    )

    return {
        "created_at": now_iso(),
        "status_code": 0,
        "directive_id": directive_id,
        "captured_at": captured_at,
        "status": status_text,
        "verify_hook": verify,
        "row": row,
        "register_path": str(DIRECTIVE_REGISTER),
        "doing_card": doing_card,
        "doing_card_id": doing_card_id,
        "lifecycle_event": lifecycle_row,
    }


def directive_track(*, directive_id: str, phase: str, note: str, label: str) -> dict[str, Any]:
    did = str(directive_id or "").strip().upper()
    phase_norm = str(phase or "").strip().lower()
    if not did:
        return {"created_at": now_iso(), "status_code": 1, "error": "directive_id is empty"}
    if phase_norm not in DIRECTIVE_PHASES:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "error": f"invalid phase={phase_norm}; allowed={','.join(DIRECTIVE_PHASES)}",
            "directive_id": did,
        }
    if not directive_exists(did):
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "error": f"directive_id not found: {did}",
            "directive_id": did,
        }

    event = append_directive_lifecycle_event(
        directive_id=did,
        phase=phase_norm,
        note=str(note or ""),
        label=str(label or ""),
        doing_card=current_doing_card(),
    )

    register_status = "DONE" if phase_norm == "executed" else "IN_PROGRESS"
    updated = update_directive_status(did, register_status)
    return {
        "created_at": now_iso(),
        "status_code": 0,
        "directive_id": did,
        "phase": phase_norm,
        "register_status": register_status,
        "register_status_updated": bool(updated),
        "lifecycle_event": event,
        "lifecycle_path": str(DIRECTIVE_LIFECYCLE),
    }


def directive_freshness(*, max_age_s: int, directive_message: str = "") -> dict[str, Any]:
    ensure_directive_register()
    text = read_text(DIRECTIVE_REGISTER)
    rows = directive_rows(text)
    if not rows:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "reason": "DIRECTIVE_REGISTER_EMPTY",
            "register_path": str(DIRECTIVE_REGISTER),
        }

    row = None
    probe = str(directive_message or "").strip()
    if probe:
        row = directive_latest_row_by_message(text, probe)
        if row is None:
            return {
                "created_at": now_iso(),
                "status_code": 1,
                "status": "FAIL",
                "reason": "DIRECTIVE_MESSAGE_NOT_FOUND",
                "directive_message": probe,
                "register_path": str(DIRECTIVE_REGISTER),
            }
    else:
        row = rows[-1]

    captured_at = str(row.get("captured_at") or "")
    captured_dt = parse_iso_utc(captured_at)
    age_s = None
    if captured_dt is not None:
        age_s = (datetime.now(timezone.utc) - captured_dt).total_seconds()

    doing_card = current_doing_card()
    doing_card_id = extract_card_id(doing_card)
    mapped_to_doing = bool(doing_card_id and doing_card_id in str(row.get("planned_integration") or ""))
    age_ok = age_s is not None and float(age_s) <= float(max(1, int(max_age_s)))
    ok = bool(age_ok and mapped_to_doing)

    return {
        "created_at": now_iso(),
        "status_code": 0 if ok else 1,
        "status": "PASS" if ok else "FAIL",
        "max_age_s": int(max(1, int(max_age_s))),
        "directive_id": row.get("directive_id"),
        "captured_at": captured_at,
        "age_s": (round(float(age_s), 3) if age_s is not None else None),
        "age_ok": bool(age_ok),
        "mapped_to_doing_card": bool(mapped_to_doing),
        "doing_card": doing_card,
        "doing_card_id": doing_card_id,
        "planned_integration": row.get("planned_integration"),
        "verify_hook": row.get("verify_hook"),
        "register_path": str(DIRECTIVE_REGISTER),
    }


def directive_trace(*, directive_id: str) -> dict[str, Any]:
    did = str(directive_id or "").strip().upper()
    ensure_directive_register()
    register_text = read_text(DIRECTIVE_REGISTER)
    row = directive_row_by_id(register_text, did)
    if row is None:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "error": f"directive_id not found: {did}",
            "directive_id": did,
            "register_path": str(DIRECTIVE_REGISTER),
        }

    events = directive_lifecycle_events(did)
    phases = [str(item.get("phase") or "") for item in events]
    route = {
        "captured_in_register": True,
        "events_total": len(events),
        "phases": phases,
        "has_integrated": "integrated" in phases,
        "has_executed": "executed" in phases,
        "register_status": str(row.get("status") or ""),
    }
    return {
        "created_at": now_iso(),
        "status_code": 0,
        "status": "PASS",
        "directive_id": did,
        "register_row": row,
        "lifecycle_events": events,
        "route_resolution": route,
        "lifecycle_path": str(DIRECTIVE_LIFECYCLE),
        "register_path": str(DIRECTIVE_REGISTER),
    }


def update_plan_events(
    *,
    update_plan_id: str = "",
    doing_card: str = "",
    directive_id: str = "",
) -> list[dict[str, Any]]:
    pid = str(update_plan_id or "").strip().upper()
    card = str(doing_card or "").strip().upper()
    did = str(directive_id or "").strip().upper()
    rows = read_jsonl(UPDATE_PLAN_LIFECYCLE)
    out: list[dict[str, Any]] = []
    for row in rows:
        row_pid = str(row.get("update_plan_id") or "").strip().upper()
        row_card = str(row.get("doing_card") or "").strip().upper()
        row_did = str(row.get("directive_id") or "").strip().upper()
        if pid and row_pid != pid:
            continue
        if card and row_card != card:
            continue
        if did and row_did != did:
            continue
        out.append(row)
    return out


def update_plan_next_id() -> str:
    today = utc_date()
    max_n = 0
    for row in update_plan_events():
        pid = str(row.get("update_plan_id") or "").strip().upper()
        match = re.match(r"^UPL-(\d{8})-(\d{3})$", pid)
        if not match:
            continue
        day = str(match.group(1))
        ordinal = int(match.group(2))
        if day == today and ordinal > max_n:
            max_n = ordinal
    return f"UPL-{today}-{max_n + 1:03d}"


def normalize_update_plan_steps(raw_steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, row in enumerate(raw_steps):
        if not isinstance(row, dict):
            raise ValueError(f"Invalid update_plan step at index {idx}: not an object")
        step = str(row.get("step") or "").strip()
        if not step:
            raise ValueError(f"Invalid update_plan step at index {idx}: empty step")
        raw_status = str(row.get("status") or "pending").strip().lower()
        if raw_status not in UPDATE_PLAN_STEP_STATUSES:
            allowed = ",".join(UPDATE_PLAN_STEP_STATUSES)
            raise ValueError(f"Invalid update_plan step status at index {idx}: {raw_status} (allowed: {allowed})")
        out.append({"step": step, "status": raw_status})
    return out


def parse_steps_json(steps_json: str) -> list[dict[str, Any]]:
    payload = str(steps_json or "").strip()
    if not payload:
        return []
    parsed = json.loads(payload)
    if not isinstance(parsed, list):
        raise ValueError("steps-json must be a JSON list")
    return normalize_update_plan_steps(parsed)


def update_plan_sync(
    *,
    summary: str,
    status: str,
    steps_json: str,
    directive_id: str,
    note: str,
    source: str,
    doing_card: str,
    label: str,
) -> dict[str, Any]:
    current_card = current_doing_card()
    current_card_id = extract_card_id(current_card)
    target_card = str(doing_card or "").strip() or current_card_id
    target_card_id = extract_card_id(target_card) or target_card
    if not target_card_id:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "error": "cannot sync update_plan: current DOING card is empty",
        }

    if current_card_id and target_card_id and target_card_id != current_card_id:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "error": f"update_plan sync card mismatch: requested={target_card_id} current={current_card_id}",
            "doing_card": current_card_id,
        }

    status_text = str(status or "IN_PROGRESS").strip().upper()
    if status_text not in UPDATE_PLAN_STATUSES:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "error": f"update_plan status must be one of: {', '.join(UPDATE_PLAN_STATUSES)}",
        }

    did = str(directive_id or "").strip().upper()
    if did and not directive_exists(did):
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "error": f"invalid directive_id for update_plan sync: {did}",
            "directive_id": did,
        }

    try:
        steps = parse_steps_json(steps_json)
    except Exception as exc:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "error": str(exc),
        }

    update_plan_id = update_plan_next_id()
    event = {
        "created_at": now_iso(),
        "update_plan_id": update_plan_id,
        "summary": str(summary or "").strip(),
        "status": status_text,
        "steps": steps,
        "directive_id": did,
        "note": str(note or "").strip(),
        "source": str(source or "MANUAL").strip().upper(),
        "doing_card": target_card_id,
        "label": str(label or "").strip(),
    }
    append_jsonl(UPDATE_PLAN_LIFECYCLE, event)

    return {
        "created_at": now_iso(),
        "status_code": 0,
        "status": "PASS",
        "update_plan_id": update_plan_id,
        "doing_card": target_card_id,
        "directive_id": did,
        "steps_count": len(steps),
        "summary": event.get("summary"),
        "update_plan_lifecycle_path": str(UPDATE_PLAN_LIFECYCLE),
        "event": event,
    }


def latest_update_plan_event(*, doing_card: str = "", directive_id: str = "") -> dict[str, Any]:
    rows = update_plan_events(doing_card=doing_card, directive_id=directive_id)
    if not rows:
        return {}
    return rows[-1]


def update_plan_freshness(*, max_age_s: int, directive_id: str = "") -> dict[str, Any]:
    current_card = current_doing_card()
    current_card_id = extract_card_id(current_card)
    row = latest_update_plan_event(doing_card=current_card_id, directive_id=directive_id)
    if not row:
        return {
            "created_at": now_iso(),
            "status_code": 1,
            "status": "FAIL",
            "reason": "UPDATE_PLAN_EVENT_NOT_FOUND",
            "doing_card": current_card_id,
            "directive_id": str(directive_id or "").strip().upper(),
            "update_plan_lifecycle_path": str(UPDATE_PLAN_LIFECYCLE),
        }

    created_at = str(row.get("created_at") or "")
    created_dt = parse_iso_utc(created_at)
    age_s = None
    if created_dt is not None:
        age_s = (datetime.now(timezone.utc) - created_dt).total_seconds()

    mapped = bool(current_card_id and str(row.get("doing_card") or "").strip().upper() == current_card_id.upper())
    age_ok = age_s is not None and float(age_s) <= float(max(1, int(max_age_s)))
    ok = bool(mapped and age_ok)
    return {
        "created_at": now_iso(),
        "status_code": 0 if ok else 1,
        "status": "PASS" if ok else "FAIL",
        "max_age_s": int(max(1, int(max_age_s))),
        "update_plan_id": row.get("update_plan_id"),
        "event_created_at": created_at,
        "age_s": (round(float(age_s), 3) if age_s is not None else None),
        "age_ok": bool(age_ok),
        "mapped_to_doing_card": bool(mapped),
        "doing_card": current_card_id,
        "directive_id": row.get("directive_id"),
        "update_plan_lifecycle_path": str(UPDATE_PLAN_LIFECYCLE),
    }


def update_plan_trace(*, update_plan_id: str = "", doing_card: str = "", limit: int = 100) -> dict[str, Any]:
    card_id = extract_card_id(str(doing_card or "").strip()) or str(doing_card or "").strip()
    events = update_plan_events(update_plan_id=update_plan_id, doing_card=card_id)
    safe_limit = max(1, int(limit))
    sliced = events[-safe_limit:]
    return {
        "created_at": now_iso(),
        "status_code": 0,
        "status": "PASS",
        "count": len(sliced),
        "limit": safe_limit,
        "update_plan_id": str(update_plan_id or "").strip().upper(),
        "doing_card": card_id,
        "events": sliced,
        "update_plan_lifecycle_path": str(UPDATE_PLAN_LIFECYCLE),
    }


def governance_audit(label: str) -> dict[str, Any]:
    bootstrap = build_payload()
    checks: list[dict[str, Any]] = []
    for path in CORE_DOCS:
        checks.append({"name": f"exists:{path.relative_to(REPO_ROOT)}", "ok": path.exists()})
    checks.append({"name": "bootstrap_status_ok", "ok": status_code(bootstrap.get("status_code"), 1) == 0})
    checks.append({"name": "board_invariants_ok", "ok": bool(bootstrap.get("board_invariants_ok"))})
    checks.append({"name": "doing_has_task_breakdown", "ok": bool(bootstrap.get("doing_card_has_task_breakdown"))})
    ok = all(bool(x.get("ok")) for x in checks)
    return {
        "created_at": now_iso(),
        "status_code": 0 if ok else 1,
        "label": str(label),
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
        content = read_text(path)
        current = len(content.splitlines())
        text_checks.append(
            {
                "name": f"line_count:{rel}",
                "ok": current >= min_count,
                "current": current,
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

    all_ok = status_code(audit.get("status_code"), 1) == 0 and all(bool(x.get("ok")) for x in text_checks)
    code = 0 if all_ok else (2 if bool(strict_medium) else 1)
    return {
        "created_at": now_iso(),
        "status_code": code,
        "label": str(label),
        "strict_medium": bool(strict_medium),
        "governance_audit_status": audit.get("status_code"),
        "checks": text_checks,
    }


def context_bootstrap(label: str) -> dict[str, Any]:
    payload = build_payload()
    return {
        "created_at": now_iso(),
        "status_code": status_code(payload.get("status_code"), 1),
        "label": str(label),
        "summary": payload,
    }


def skip_payload(reason: str) -> dict[str, Any]:
    return {
        "created_at": now_iso(),
        "status_code": 0,
        "status": "SKIP",
        "reason": str(reason),
    }


def workflow_context_gate(
    *,
    label: str,
    strict_medium: bool = False,
    directive_message: str = "",
    auto_directive_sync: bool = True,
    auto_update_plan_sync: bool = True,
    max_freshness_age_s: int = DEFAULT_CONTEXT_FRESHNESS_MAX_AGE_S,
    max_plan_freshness_age_s: int = DEFAULT_PLAN_FRESHNESS_MAX_AGE_S,
) -> dict[str, Any]:
    directive_payload: dict[str, Any] = skip_payload("AUTO_DIRECTIVE_SYNC_DISABLED")
    directive_id = ""
    if auto_directive_sync:
        if str(directive_message or "").strip():
            directive_payload = directive_sync(
                message=str(directive_message),
                intent="",
                planned_integration="",
                label=f"{label}_directive",
                auto_fill=True,
            )
            directive_id = str(directive_payload.get("directive_id") or "").strip().upper()
        else:
            directive_payload = skip_payload("NO_DIRECTIVE_MESSAGE")

    update_plan_payload: dict[str, Any] = skip_payload("AUTO_UPDATE_PLAN_SYNC_DISABLED")
    if auto_update_plan_sync:
        update_plan_payload = update_plan_sync(
            summary="AUTO sync from workflow-context-gate",
            status="IN_PROGRESS",
            steps_json="",
            directive_id=directive_id,
            note="",
            source="AUTO",
            doing_card="",
            label=f"{label}_plan",
        )

    directive_freshness_payload: dict[str, Any]
    if directive_id or str(directive_message or "").strip():
        directive_freshness_payload = directive_freshness(
            max_age_s=max(1, int(max_freshness_age_s)),
            directive_message=str(directive_message or ""),
        )
    else:
        directive_freshness_payload = skip_payload("NO_DIRECTIVE_TARGET")

    plan_freshness_payload: dict[str, Any]
    if auto_update_plan_sync:
        plan_freshness_payload = update_plan_freshness(
            max_age_s=max(1, int(max_plan_freshness_age_s)),
            directive_id=directive_id,
        )
    else:
        plan_freshness_payload = skip_payload("NO_UPDATE_PLAN_TARGET")

    audit = governance_audit(f"{label}_audit")
    quality = governance_quality_audit(f"{label}_quality", strict_medium=bool(strict_medium))
    bootstrap = context_bootstrap(f"{label}_bootstrap")

    parts = [
        directive_payload,
        update_plan_payload,
        directive_freshness_payload,
        plan_freshness_payload,
        audit,
        quality,
        bootstrap,
    ]
    gate_code = 0
    for part in parts:
        code = status_code(part.get("status_code"), 1)
        if code != 0:
            gate_code = code
            break

    return {
        "created_at": now_iso(),
        "status_code": gate_code,
        "label": str(label),
        "strict_medium": bool(strict_medium),
        "auto_directive_sync": bool(auto_directive_sync),
        "auto_update_plan_sync": bool(auto_update_plan_sync),
        "max_freshness_age_s": int(max(1, int(max_freshness_age_s))),
        "max_plan_freshness_age_s": int(max(1, int(max_plan_freshness_age_s))),
        "directive_sync": directive_payload,
        "update_plan_sync": update_plan_payload,
        "directive_freshness": directive_freshness_payload,
        "update_plan_freshness": plan_freshness_payload,
        "governance_audit": audit,
        "governance_quality_audit": quality,
        "context_bootstrap": bootstrap,
    }


def execution_guard(
    *,
    label: str,
    strict_medium: bool = False,
    directive_message: str = "",
    auto_directive_sync: bool = True,
    auto_update_plan_sync: bool = True,
    max_freshness_age_s: int = DEFAULT_CONTEXT_FRESHNESS_MAX_AGE_S,
    max_plan_freshness_age_s: int = DEFAULT_PLAN_FRESHNESS_MAX_AGE_S,
) -> dict[str, Any]:
    return workflow_context_gate(
        label=label,
        strict_medium=bool(strict_medium),
        directive_message=str(directive_message or ""),
        auto_directive_sync=bool(auto_directive_sync),
        auto_update_plan_sync=bool(auto_update_plan_sync),
        max_freshness_age_s=int(max_freshness_age_s),
        max_plan_freshness_age_s=int(max_plan_freshness_age_s),
    )


def print_and_exit(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return status_code(payload.get("status_code"), 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Governance wrapper commands for Codex template.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_dir = sub.add_parser("directive-sync")
    p_dir.add_argument("--message", required=True)
    p_dir.add_argument("--intent", default="")
    p_dir.add_argument("--planned-integration", default="")
    p_dir.add_argument("--verify-hook", default="")
    p_dir.add_argument("--status", default="IN_PROGRESS")
    p_dir.add_argument("--intent-classification", default="AUTO")
    p_dir.add_argument("--captured-at-utc", default="")
    p_dir.add_argument("--no-auto-fill", action="store_true")
    p_dir.add_argument("--label", default="manual")

    p_track = sub.add_parser("directive-track")
    p_track.add_argument("--directive-id", required=True)
    p_track.add_argument("--phase", required=True)
    p_track.add_argument("--note", default="")
    p_track.add_argument("--label", default="manual")

    p_fresh = sub.add_parser("directive-freshness")
    p_fresh.add_argument("--max-age-s", type=int, default=DEFAULT_CONTEXT_FRESHNESS_MAX_AGE_S)
    p_fresh.add_argument("--directive-message", default="")

    p_trace = sub.add_parser("directive-trace")
    p_trace.add_argument("--directive-id", required=True)

    p_up_sync = sub.add_parser("update-plan-sync")
    p_up_sync.add_argument("--summary", default="")
    p_up_sync.add_argument("--status", default="IN_PROGRESS")
    p_up_sync.add_argument("--steps-json", default="")
    p_up_sync.add_argument("--directive-id", default="")
    p_up_sync.add_argument("--note", default="")
    p_up_sync.add_argument("--source", default="MANUAL")
    p_up_sync.add_argument("--doing-card", default="")
    p_up_sync.add_argument("--label", default="manual")

    p_up_fresh = sub.add_parser("update-plan-freshness")
    p_up_fresh.add_argument("--max-age-s", type=int, default=DEFAULT_PLAN_FRESHNESS_MAX_AGE_S)
    p_up_fresh.add_argument("--directive-id", default="")

    p_up_trace = sub.add_parser("update-plan-trace")
    p_up_trace.add_argument("--update-plan-id", default="")
    p_up_trace.add_argument("--doing-card", default="")
    p_up_trace.add_argument("--limit", type=int, default=100)

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
    p_gate.add_argument("--directive-message", default="")
    p_gate.add_argument("--no-auto-directive-sync", action="store_true")
    p_gate.add_argument("--no-auto-update-plan-sync", action="store_true")
    p_gate.add_argument("--max-freshness-age-s", type=int, default=DEFAULT_CONTEXT_FRESHNESS_MAX_AGE_S)
    p_gate.add_argument("--max-plan-freshness-age-s", type=int, default=DEFAULT_PLAN_FRESHNESS_MAX_AGE_S)

    p_exec = sub.add_parser("execution-guard")
    p_exec.add_argument("--label", default="manual")
    p_exec.add_argument("--strict-medium", action="store_true")
    p_exec.add_argument("--directive-message", default="")
    p_exec.add_argument("--no-auto-directive-sync", action="store_true")
    p_exec.add_argument("--no-auto-update-plan-sync", action="store_true")
    p_exec.add_argument("--max-freshness-age-s", type=int, default=DEFAULT_CONTEXT_FRESHNESS_MAX_AGE_S)
    p_exec.add_argument("--max-plan-freshness-age-s", type=int, default=DEFAULT_PLAN_FRESHNESS_MAX_AGE_S)

    args = parser.parse_args()

    if args.cmd == "directive-sync":
        payload = directive_sync(
            message=str(args.message),
            intent=str(args.intent),
            planned_integration=str(args.planned_integration),
            label=str(args.label),
            verify_hook=str(args.verify_hook),
            status=str(args.status),
            intent_classification=str(args.intent_classification),
            captured_at_utc=str(args.captured_at_utc),
            auto_fill=(not bool(args.no_auto_fill)),
        )
        payload = persist("directive_sync", str(args.label), payload)
        return print_and_exit(payload)

    if args.cmd == "directive-track":
        payload = directive_track(
            directive_id=str(args.directive_id),
            phase=str(args.phase),
            note=str(args.note),
            label=str(args.label),
        )
        payload = persist("directive_track", str(args.label), payload)
        return print_and_exit(payload)

    if args.cmd == "directive-freshness":
        payload = directive_freshness(
            max_age_s=int(args.max_age_s),
            directive_message=str(args.directive_message),
        )
        payload = persist("directive_freshness", "manual", payload)
        return print_and_exit(payload)

    if args.cmd == "directive-trace":
        payload = directive_trace(directive_id=str(args.directive_id))
        payload = persist("directive_trace", "manual", payload)
        return print_and_exit(payload)

    if args.cmd == "update-plan-sync":
        payload = update_plan_sync(
            summary=str(args.summary),
            status=str(args.status),
            steps_json=str(args.steps_json),
            directive_id=str(args.directive_id),
            note=str(args.note),
            source=str(args.source),
            doing_card=str(args.doing_card),
            label=str(args.label),
        )
        payload = persist("update_plan_sync", str(args.label), payload)
        return print_and_exit(payload)

    if args.cmd == "update-plan-freshness":
        payload = update_plan_freshness(
            max_age_s=int(args.max_age_s),
            directive_id=str(args.directive_id),
        )
        payload = persist("update_plan_freshness", "manual", payload)
        return print_and_exit(payload)

    if args.cmd == "update-plan-trace":
        payload = update_plan_trace(
            update_plan_id=str(args.update_plan_id),
            doing_card=str(args.doing_card),
            limit=int(args.limit),
        )
        payload = persist("update_plan_trace", "manual", payload)
        return print_and_exit(payload)

    if args.cmd == "governance-audit":
        payload = governance_audit(str(args.label))
        payload = persist("governance_audit", str(args.label), payload)
        return print_and_exit(payload)

    if args.cmd == "governance-quality-audit":
        payload = governance_quality_audit(str(args.label), strict_medium=bool(args.strict_medium))
        payload = persist("governance_quality_audit", str(args.label), payload)
        return print_and_exit(payload)

    if args.cmd == "context-bootstrap":
        payload = context_bootstrap(str(args.label))
        payload = persist("context_bootstrap", str(args.label), payload)
        return print_and_exit(payload)

    if args.cmd == "workflow-context-gate":
        payload = workflow_context_gate(
            label=str(args.label),
            strict_medium=bool(args.strict_medium),
            directive_message=str(args.directive_message),
            auto_directive_sync=(not bool(args.no_auto_directive_sync)),
            auto_update_plan_sync=(not bool(args.no_auto_update_plan_sync)),
            max_freshness_age_s=int(args.max_freshness_age_s),
            max_plan_freshness_age_s=int(args.max_plan_freshness_age_s),
        )
        payload = persist("workflow_context_gate", str(args.label), payload)
        return print_and_exit(payload)

    if args.cmd == "execution-guard":
        payload = execution_guard(
            label=str(args.label),
            strict_medium=bool(args.strict_medium),
            directive_message=str(args.directive_message),
            auto_directive_sync=(not bool(args.no_auto_directive_sync)),
            auto_update_plan_sync=(not bool(args.no_auto_update_plan_sync)),
            max_freshness_age_s=int(args.max_freshness_age_s),
            max_plan_freshness_age_s=int(args.max_plan_freshness_age_s),
        )
        payload = persist("execution_guard", str(args.label), payload)
        return print_and_exit(payload)

    return 1


if __name__ == "__main__":
    sys.exit(main())
