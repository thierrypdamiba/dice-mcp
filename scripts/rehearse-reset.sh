#!/usr/bin/env bash
# Reset dice-mcp to a known filming state.
set -euo pipefail
cd "$(dirname "$0")/.."

TARGET="${1:-scaffold}"

case "$TARGET" in
  scaffold)
    git checkout baseline/scaffold
    echo "→ baseline/scaffold (untouched arcade new dice, F/D grade)"
    ;;
  improved)
    git checkout improved/b
    echo "→ improved/b (reference B state, ~74-75)"
    ;;
  main)
    git checkout main
    echo "→ main (latest)"
    ;;
  *)
    echo "Usage: $0 {scaffold|improved|main}"
    exit 1
    ;;
esac

head -3 src/dice/server.py
python3 -m py_compile src/dice/server.py && echo "✓ py_compile ok"
