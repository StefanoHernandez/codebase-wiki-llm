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
  ".claude-plugin/marketplace.json"
  "plugins/codebase-wiki-llm/hooks"
  "plugins/codebase-wiki-llm/scripts"
  "plugins/antigravity-codebase-wiki-llm/hooks.json"
  "plugins/antigravity-codebase-wiki-llm/scripts"
  "plugins/codebase-wiki-llm/.codex-plugin/plugin.json"
  "plugins/codebase-wiki-llm/skills"
  "plugins/claude-codebase-wiki-llm/plugin.json"
  "plugins/claude-codebase-wiki-llm/commands"
  "plugins/claude-codebase-wiki-llm/skills"
  "plugins/claude-codebase-wiki-llm/hooks"
  "plugins/claude-codebase-wiki-llm/scripts"
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
  "skills"
)

cd "$ROOT_DIR"

HARDCODED_WIKI="$(grep -rnE '(^|[^A-Za-z<.-])wiki/' canonical/codebase --include='*.md' --exclude-dir=partials || true)"
if [ -n "$HARDCODED_WIKI" ]; then
  echo "hardcoded wiki/ paths in canonical/codebase; use <wiki-root>/ instead:" >&2
  echo "$HARDCODED_WIKI" >&2
  exit 1
fi

snapshot() {
  git status --porcelain --untracked-files=all -- "${GENERATED_PATHS[@]}"
  git diff -- "${GENERATED_PATHS[@]}"
}
snapshot > "$BEFORE"
python3 "$ROOT_DIR/scripts/generate-host-packages.py"
snapshot > "$AFTER"

if ! cmp -s "$BEFORE" "$AFTER"; then
  echo "generated files were out of date; regenerated output differs" >&2
  diff -u "$BEFORE" "$AFTER" || true
  exit 1
fi

STEP0_MARKER="Codebase Wiki LLM: wiki_root:"
STEP0_FILES=(
  "plugins/codebase-wiki-llm/skills/codebase-wiki-init/SKILL.md"
  "plugins/codebase-wiki-llm/skills/codebase-wiki-context/SKILL.md"
  "plugins/claude-codebase-wiki-llm/commands/wiki-sync.md"
  "plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/SKILL.md"
  "plugins/antigravity-codebase-wiki-llm/rules/AGENTS.md"
  "skills/codebase-wiki-lint/SKILL.md"
)
for file in "${STEP0_FILES[@]}"; do
  if ! grep -q "$STEP0_MARKER" "$file"; then
    echo "missing wiki root resolution (Step 0) in $file" >&2
    exit 1
  fi
done

require() { # <marker> <file>...
  local marker="$1"; shift
  for file in "$@"; do
    grep -qF -- "$marker" "$file" || { echo "missing '$marker' in $file" >&2; exit 1; }
  done
}
require "## Core map" canonical/codebase/default-schema.md
require "⚠️ NOT VERIFIED" canonical/codebase/default-schema.md canonical/codebase/references/agent-context-template.md
require ".private-terms" canonical/codebase/default-schema.md canonical/codebase/maintainer.md
require "## Verified Facts" canonical/codebase/references/agent-context-template.md
require "--adopt" canonical/codebase/workflows/wiki-init.md
require "Reply \`ok\`" canonical/codebase/workflows/wiki-init.md
require "check-private-terms.sh" canonical/codebase/workflows/wiki-init.md
require "## Core map" canonical/codebase/workflows/wiki-init.md

echo "generated files are up to date"
