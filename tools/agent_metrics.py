#!/usr/bin/env python3
"""Metrics utility for agent execution cycles."""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STREAMS = ("CORE_STREAM", "PLATFORM_STREAM", "VERIFY_STREAM")
STATUSES = ("PASS", "FAIL", "BLOCKED")
LANE_BRANCH_PREFIX: dict[str, tuple[str, ...]] = {
    "CORE_STREAM": ("core/", "feature/", "app/"),
    "PLATFORM_STREAM": ("platform/", "refactor/", "infra/"),
    "VERIFY_STREAM": ("verify/", "qa/"),
}


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_base_dir(repo_root: Path) -> Path:
    return repo_root / "shared" / "agent_metrics"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def parse_csv(value: str) -> list[str]:
    out: list[str] = []
    for item in str(value or "").split(","):
        v = item.strip()
        if v:
            out.append(v)
    return out


def append_event(path: Path, payload: dict[str, Any]) -> None:
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
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


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(statistics.fmean(values))


def run_git(repo_root: Path, *args: str) -> str:
    cmd = ["git", "-C", str(repo_root), *args]
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""


def short_branch(branch: str) -> str:
    s = str(branch or "").strip()
    if s.startswith("refs/heads/"):
        s = s[len("refs/heads/") :]
    return s


def detect_lane(branch: str) -> str:
    b = short_branch(branch).lower()
    for lane, prefixes in LANE_BRANCH_PREFIX.items():
        for pref in prefixes:
            if b.startswith(pref):
                return lane
    return "UNASSIGNED"


def parse_worktree_porcelain(raw: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    current: dict[str, Any] = {}
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            if current:
                blocks.append(current)
                current = {}
            continue
        if " " in s:
            k, v = s.split(" ", 1)
            current[k] = v
        else:
            current[s] = True
    if current:
        blocks.append(current)

    out: list[dict[str, Any]] = []
    for block in blocks:
        branch = short_branch(str(block.get("branch") or ""))
        out.append(
            {
                "path": str(block.get("worktree") or ""),
                "branch": branch,
                "lane": detect_lane(branch),
                "head": str(block.get("HEAD") or ""),
            }
        )
    return out


def collect_worktrees(repo_root: Path) -> list[dict[str, Any]]:
    raw = run_git(repo_root, "worktree", "list", "--porcelain")
    if not raw:
        return []
    return parse_worktree_porcelain(raw)


def summarize(events: list[dict[str, Any]]) -> dict[str, Any]:
    by_status = Counter(str(e.get("status") or "") for e in events)
    by_stream: dict[str, dict[str, Any]] = {}
    for stream in STREAMS:
        rows = [e for e in events if str(e.get("stream") or "") == stream]
        durations = [float(e.get("duration_s") or 0.0) for e in rows]
        verify = [int(e.get("verify_pass") or 0) for e in rows]
        count = len(rows)
        by_stream[stream] = {
            "events": count,
            "pass": sum(1 for e in rows if str(e.get("status")) == "PASS"),
            "fail": sum(1 for e in rows if str(e.get("status")) == "FAIL"),
            "blocked": sum(1 for e in rows if str(e.get("status")) == "BLOCKED"),
            "cycle_time_s_avg": round(mean(durations), 3),
            "verify_pass_rate": round((sum(verify) / count) if count else 0.0, 4),
        }

    skills = Counter()
    rules = Counter()
    for e in events:
        for s in e.get("skills") or []:
            skills[str(s)] += 1
        for r in e.get("rules") or []:
            rules[str(r)] += 1

    return {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_events": len(events),
        "status_counts": dict(by_status),
        "by_stream": by_stream,
        "top_skills": skills.most_common(10),
        "top_rules": rules.most_common(10),
    }


def cmd_log(args: argparse.Namespace, base: Path) -> int:
    payload = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "epoch_s": int(time.time()),
        "board_card": str(args.board_card),
        "stream": str(args.stream),
        "status": str(args.status),
        "duration_s": float(args.duration_s),
        "skills": parse_csv(args.skills),
        "rules": parse_csv(args.rules),
        "verify_pass": int(args.verify_pass),
        "timeouts": int(args.timeouts),
        "retries": int(args.retries),
        "notes": str(args.notes or "").strip(),
    }
    events_path = base / "events.jsonl"
    append_event(events_path, payload)
    print(str(events_path))
    return 0


def cmd_summary(args: argparse.Namespace, base: Path) -> int:
    out = Path(args.out) if args.out else (base / "summary_latest.json")
    data = summarize(load_events(base / "events.jsonl"))
    ensure_parent(out)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out))
    return 0


def cmd_dashboard(args: argparse.Namespace, base: Path, repo_root: Path) -> int:
    summary_payload = summarize(load_events(base / "events.jsonl"))
    worktrees = collect_worktrees(repo_root)

    lane_counts: dict[str, int] = defaultdict(int)
    for wt in worktrees:
        lane_counts[str(wt.get("lane") or "UNASSIGNED")] += 1

    active_lanes = [lane for lane in STREAMS if lane_counts.get(lane, 0) > 0]
    payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "repo_root": str(repo_root),
        "metrics_summary": summary_payload,
        "worktrees": worktrees,
        "lane_worktree_counts": dict(lane_counts),
        "policy_checks": {
            "global_active_lanes_ok": len(active_lanes) <= 3,
            "per_lane_doing_ok": all(lane_counts.get(lane, 0) <= 1 for lane in STREAMS),
            "has_unassigned_worktrees": lane_counts.get("UNASSIGNED", 0) > 0,
        },
    }

    out_json = Path(args.out_json) if args.out_json else (base / "dashboard_latest.json")
    out_md = Path(args.out_md) if args.out_md else (base / "dashboard_latest.md")
    ensure_parent(out_json)
    ensure_parent(out_md)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Agent Metrics Dashboard",
        "",
        f"- Generated at: {payload['generated_at']}",
        f"- Total events: {summary_payload['total_events']}",
        f"- Status counts: {summary_payload['status_counts']}",
        f"- Lane counts: {payload['lane_worktree_counts']}",
        "",
        "## Policy Checks",
        f"- global_active_lanes_ok: {payload['policy_checks']['global_active_lanes_ok']}",
        f"- per_lane_doing_ok: {payload['policy_checks']['per_lane_doing_ok']}",
        f"- has_unassigned_worktrees: {payload['policy_checks']['has_unassigned_worktrees']}",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(str(out_json))
    print(str(out_md))
    return 0


def cmd_reflect(args: argparse.Namespace, base: Path) -> int:
    events = load_events(base / "events.jsonl")
    window = events[-max(1, int(args.last_n)) :]
    status_counts = Counter(str(e.get("status") or "") for e in window)
    timeout_total = sum(int(e.get("timeouts") or 0) for e in window)
    verify_fails = sum(1 for e in window if int(e.get("verify_pass") or 0) == 0)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{time.strftime('%Y%m%d_%H%M%S')}.md"
    lines = [
        f"# Reflection ({time.strftime('%Y-%m-%d %H:%M:%S')})",
        "",
        f"- Window size: {len(window)}",
        f"- Status counts: {dict(status_counts)}",
        f"- Total timeouts: {timeout_total}",
        f"- Verify failures: {verify_fails}",
        "",
        "## Actions",
        "- Reduce cycle duration for the slowest stream.",
        "- Add explicit unblock runbook for repeated blockers.",
        "- Shift verification earlier in cycle for risky changes.",
        "",
    ]
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(str(out_file))
    return 0


def cmd_worktree_check(args: argparse.Namespace, repo_root: Path) -> int:
    worktrees = collect_worktrees(repo_root)
    lane_counts: dict[str, int] = defaultdict(int)
    for wt in worktrees:
        lane_counts[str(wt.get("lane") or "UNASSIGNED")] += 1
    payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "worktrees": worktrees,
        "lane_counts": dict(lane_counts),
        "global_active_lanes_ok": sum(1 for lane in STREAMS if lane_counts.get(lane, 0) > 0) <= 3,
        "per_lane_doing_ok": all(lane_counts.get(lane, 0) <= 1 for lane in STREAMS),
    }
    out = Path(args.out)
    ensure_parent(out)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Agent metrics utility.")
    p.add_argument("--repo-root", default=str(default_repo_root()))
    p.add_argument("--base-dir", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    s_log = sub.add_parser("log")
    s_log.add_argument("--board-card", required=True)
    s_log.add_argument("--stream", required=True, choices=STREAMS)
    s_log.add_argument("--status", required=True, choices=STATUSES)
    s_log.add_argument("--duration-s", required=True, type=float)
    s_log.add_argument("--skills", default="")
    s_log.add_argument("--rules", default="")
    s_log.add_argument("--verify-pass", type=int, default=1)
    s_log.add_argument("--timeouts", type=int, default=0)
    s_log.add_argument("--retries", type=int, default=0)
    s_log.add_argument("--notes", default="")

    s_sum = sub.add_parser("summary")
    s_sum.add_argument("--out", default="")

    s_dash = sub.add_parser("dashboard")
    s_dash.add_argument("--out-json", default="")
    s_dash.add_argument("--out-md", default="")

    s_ref = sub.add_parser("reflect")
    s_ref.add_argument("--out-dir", required=True)
    s_ref.add_argument("--last-n", type=int, default=10)

    s_wc = sub.add_parser("worktree-check")
    s_wc.add_argument("--out", required=True)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    base = Path(args.base_dir).resolve() if args.base_dir else default_base_dir(repo_root)

    if args.cmd == "log":
        return cmd_log(args, base)
    if args.cmd == "summary":
        return cmd_summary(args, base)
    if args.cmd == "dashboard":
        return cmd_dashboard(args, base, repo_root)
    if args.cmd == "reflect":
        return cmd_reflect(args, base)
    if args.cmd == "worktree-check":
        return cmd_worktree_check(args, repo_root)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
