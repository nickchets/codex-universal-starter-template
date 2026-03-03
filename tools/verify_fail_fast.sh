#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_silent="$repo_root/run-silent.sh"

if [[ ! -x "$run_silent" ]]; then
  chmod +x "$run_silent"
fi

if command -v rg >/dev/null 2>&1; then
  mapfile -t py_files < <(cd "$repo_root" && rg --files -g '*.py')
else
  mapfile -t py_files < <(cd "$repo_root" && find . -type f -name '*.py' | sed 's|^\./||')
fi

if [[ "${#py_files[@]}" -eq 0 ]]; then
  echo "  [OK] No Python files found for py_compile"
  exit 0
fi

files_joined="$(printf " %q" "${py_files[@]}")"
"$run_silent" "py_compile all python files" "cd '$repo_root' && python3 -m py_compile${files_joined}"
