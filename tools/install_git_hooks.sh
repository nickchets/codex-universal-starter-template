#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

chmod +x "$repo_root/.githooks/pre-commit"
chmod +x "$repo_root/run-silent.sh" "$repo_root/tools/verify_fail_fast.sh"

git -C "$repo_root" config core.hooksPath .githooks
echo "[OK] git hooks configured: .githooks/pre-commit"
