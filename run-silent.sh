#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: ./run-silent.sh \"<description>\" \"<command>\""
}

if [[ $# -ne 2 ]]; then
  usage
  exit 2
fi

description="$1"
command="$2"
tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

if bash -lc "$command" >"$tmp_file" 2>&1; then
  printf "  [OK] %s\n" "$description"
else
  code=$?
  printf "  [FAIL] %s\n" "$description"
  cat "$tmp_file"
  exit "$code"
fi
