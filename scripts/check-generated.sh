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
  "plugins/codebase-wiki-llm/.codex-plugin/plugin.json"
  "plugins/codebase-wiki-llm/skills"
  "plugins/claude-codebase-wiki-llm/plugin.json"
  "plugins/claude-codebase-wiki-llm/commands"
  "plugins/claude-codebase-wiki-llm/skills"
  "plugins/antigravity-codebase-wiki-llm/plugin.json"
  "plugins/antigravity-codebase-wiki-llm/rules"
  "plugins/antigravity-codebase-wiki-llm/skills"
  "plugins/secondbrain-wiki-llm/.codex-plugin/plugin.json"
  "plugins/secondbrain-wiki-llm/skills"
  "plugins/claude-secondbrain-wiki-llm/plugin.json"
  "plugins/claude-secondbrain-wiki-llm/commands"
  "plugins/claude-secondbrain-wiki-llm/skills"
  "plugins/antigravity-secondbrain-wiki-llm/plugin.json"
  "plugins/antigravity-secondbrain-wiki-llm/rules"
  "plugins/antigravity-secondbrain-wiki-llm/skills"
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
