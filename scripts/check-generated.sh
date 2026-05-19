#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BEFORE="$(mktemp)"
AFTER="$(mktemp)"

cleanup() {
  rm -f "$BEFORE" "$AFTER"
}
trap cleanup EXIT

GENERATED_PATHS=(
  "plugins/codebase-wiki-llm/skills"
  "plugins/wiki-maintainer/commands"
  "plugins/wiki-maintainer/skills/wiki-maintainer"
  "plugins/antigravity-wiki-llm/plugin.json"
  "plugins/antigravity-wiki-llm/rules"
  "plugins/antigravity-wiki-llm/skills"
)

cd "$ROOT_DIR"
git diff -- "${GENERATED_PATHS[@]}" > "$BEFORE"
python3 "$ROOT_DIR/scripts/generate-host-packages.py"
git diff -- "${GENERATED_PATHS[@]}" > "$AFTER"

if ! cmp -s "$BEFORE" "$AFTER"; then
  echo "generated files were out of date; regenerated output differs" >&2
  diff -u "$BEFORE" "$AFTER" || true
  exit 1
fi

echo "generated files are up to date"
