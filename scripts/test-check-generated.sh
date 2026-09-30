#!/usr/bin/env bash
# check-generated.sh must fail when regenerated files are left unstaged or untracked.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
failures=0
r="$TMP_DIR/repo"
mkdir -p "$r"

# Copy the current tree (tracked + untracked, not ignored) into a scratch repo.
git -C "$ROOT_DIR" ls-files -z -c -o --exclude-standard | (cd "$ROOT_DIR" && xargs -0 tar -cf - --ignore-failed-read 2>/dev/null) | tar -xf - -C "$r"
python3 "$r/scripts/generate-host-packages.py" >/dev/null
git -C "$r" init -q
git -C "$r" add -A
git -C "$r" -c user.email=t@example.com -c user.name=t commit -qm init

expect() { # <case> <expected exit>
  local got=0
  bash "$r/scripts/check-generated.sh" >"$TMP_DIR/out" 2>&1 || got=$?
  [ "$got" = "$2" ] || { echo "FAIL $1: exit $got, expected $2" >&2; cat "$TMP_DIR/out" >&2; failures=$((failures + 1)); }
}

expect "committed tree passes" 0

echo "Drift test line." >> "$r/canonical/codebase/workflows/wiki-sync.md"
python3 "$r/scripts/generate-host-packages.py" >/dev/null
git -C "$r" add canonical
expect "regenerated but unstaged files fail" 1
grep -q "git add" "$TMP_DIR/out" || { echo "FAIL unstaged: no git add hint" >&2; failures=$((failures + 1)); }
git -C "$r" add -A
expect "staged regenerated files pass" 0

git -C "$r" -c user.email=t@example.com -c user.name=t commit -qm drift
git -C "$r" rm -q --cached skills/codebase-wiki-llm/SKILL.md
expect "untracked generated files fail" 1

[ "$failures" -eq 0 ] || { echo "$failures check-generated test(s) failed" >&2; exit 1; }
echo "check-generated tests passed"
