#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BEFORE="$(mktemp)"
AFTER="$(mktemp)"

cleanup() {
  rm -f "$BEFORE" "$AFTER"
}
trap cleanup EXIT

# Whole roots, so the list cannot drift from the generators; hand-written files
# under them are unaffected by the before/after comparison.
GENERATED_PATHS=(plugins skills .claude-plugin)

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

# The commit is built from the index: regenerated files must be staged too.
if ! git diff --quiet -- "${GENERATED_PATHS[@]}" || [ -n "$(git ls-files --others --exclude-standard -- "${GENERATED_PATHS[@]}")" ]; then
  echo "generated files are not staged; run: git add ${GENERATED_PATHS[*]}" >&2
  git status --short -- "${GENERATED_PATHS[@]}" >&2
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
require "Core map" canonical/codebase/workflows/wiki-sync.md canonical/codebase/workflows/wiki-ingest.md
require "log-archive" canonical/codebase/workflows/wiki-sync.md
require "propose" canonical/codebase/workflows/wiki-sync.md
require "check-private-terms.sh --all" canonical/codebase/workflows/wiki-lint.md
require "### Budget" canonical/codebase/workflows/wiki-lint.md
require "### Evidence" canonical/codebase/workflows/wiki-lint.md
require "### Single status" canonical/codebase/workflows/wiki-lint.md
require "scripts/validate-wiki.py" canonical/codebase/workflows/wiki-lint.md canonical/codebase/maintainer.md
require "Python 3.10+" canonical/codebase/workflows/wiki-lint.md canonical/codebase/maintainer.md
require "Core map" canonical/codebase/rules/wiki-context.md
require "⚠️ NOT VERIFIED" canonical/codebase/rules/wiki-context.md

require "@<short-sha>" canonical/codebase/default-schema.md
require "⚠️ TO RE-VERIFY" canonical/codebase/workflows/wiki-sync.md canonical/codebase/workflows/wiki-lint.md canonical/codebase/references/agent-context-template.md
require "**Workaround:**" canonical/codebase/references/troubleshooting-template.md
require "git diff <source_commit>..HEAD" canonical/codebase/workflows/wiki-lint.md

require "## Proposals" canonical/codebase/references/work-tracker-template.md
require "| ID | Status | Goal | Done when | Owner | Next verification | Evidence |" canonical/codebase/references/work-tracker-template.md
require "## Approval" canonical/codebase/references/decision-template.md
require "## Agent autonomy" canonical/codebase/maintainer.md
require "## Conflicts" canonical/codebase/maintainer.md
require "## Parallel work" canonical/codebase/maintainer.md
require "### Decisions" canonical/codebase/workflows/wiki-lint.md

require "<!-- wiki:baton -->" canonical/codebase/references/agent-handoff-template.md
require "No open work." canonical/codebase/references/agent-handoff-template.md
require "<!-- wiki:verified-facts -->" canonical/codebase/references/agent-context-template.md
require "wiki:<id>" canonical/codebase/default-schema.md

require "merge=union" canonical/codebase/workflows/wiki-init.md
require "Migration plan" canonical/codebase/workflows/wiki-init.md
require "Archive the log" canonical/codebase/workflows/wiki-sync.md
require ".gitattributes" canonical/codebase/maintainer.md

echo "generated files are up to date"
