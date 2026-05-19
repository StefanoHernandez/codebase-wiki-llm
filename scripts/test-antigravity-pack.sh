#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACK_DIR="$ROOT_DIR/plugins/antigravity-wiki-llm"
TMP_HOME="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_HOME"
}
trap cleanup EXIT

required_files=(
  "$PACK_DIR/README.md"
  "$PACK_DIR/GEMINI.md"
  "$PACK_DIR/AGENTS.md"
  "$PACK_DIR/.agent/rules/codebase-wiki.md"
  "$PACK_DIR/.agent/workflows/wiki-init.md"
  "$PACK_DIR/.agent/workflows/wiki-ingest.md"
  "$PACK_DIR/.agent/workflows/wiki-sync.md"
  "$PACK_DIR/.agent/workflows/wiki-lint.md"
  "$PACK_DIR/.agent/skills/codebase-wiki-maintainer/SKILL.md"
  "$PACK_DIR/.agent/skills/codebase-wiki-maintainer/default-schema.md"
  "$ROOT_DIR/scripts/install-antigravity-wiki-llm.sh"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "missing required file: $file" >&2
    exit 1
  fi
done

HOME="$TMP_HOME" "$ROOT_DIR/scripts/install-antigravity-wiki-llm.sh" --yes

installed_files=(
  "$TMP_HOME/.gemini/antigravity/skills/wiki-maintainer/SKILL.md"
  "$TMP_HOME/.gemini/antigravity/skills/wiki-maintainer/default-schema.md"
  "$TMP_HOME/.gemini/antigravity/global_workflows/wiki-init.md"
  "$TMP_HOME/.gemini/antigravity/global_workflows/wiki-ingest.md"
  "$TMP_HOME/.gemini/antigravity/global_workflows/wiki-sync.md"
  "$TMP_HOME/.gemini/antigravity/global_workflows/wiki-lint.md"
  "$TMP_HOME/.gemini/antigravity/rules/wiki.md"
  "$TMP_HOME/.gemini/antigravity/GEMINI.md"
  "$TMP_HOME/.gemini/antigravity/AGENTS.md"
)

for file in "${installed_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "missing installed file: $file" >&2
    exit 1
  fi
done

if ! grep -q "wiki-maintainer" "$TMP_HOME/.gemini/antigravity/skills/wiki-maintainer/SKILL.md"; then
  echo "installed skill does not contain expected skill name" >&2
  exit 1
fi

echo "antigravity pack validation passed"
