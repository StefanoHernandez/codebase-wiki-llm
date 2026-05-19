#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACK_DIR="$ROOT_DIR/plugins/antigravity-wiki-llm"
TARGET_DIR="${ANTIGRAVITY_HOME:-$HOME/.gemini/antigravity}"
ASSUME_YES=0

usage() {
  cat <<'USAGE'
Install Codebase Wiki LLM files for Antigravity.

Usage:
  scripts/install-antigravity-wiki-llm.sh [--yes]

Environment:
  ANTIGRAVITY_HOME  Override target directory.
                    Default: $HOME/.gemini/antigravity

Installs into $TARGET_DIR:
  rules/wiki.md
  skills/wiki-maintainer/SKILL.md
  skills/wiki-maintainer/default-schema.md
  global_workflows/wiki-{init,ingest,sync,lint}.md
  GEMINI.md
  AGENTS.md
USAGE
}

while (($#)); do
  case "$1" in
    --yes|-y)
      ASSUME_YES=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

require_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "missing required source file: $file" >&2
    exit 1
  fi
}

copy_file() {
  local src="$1"
  local dest="$2"
  require_file "$src"
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
  echo "installed $dest"
}

if [[ ! -d "$PACK_DIR" ]]; then
  echo "missing Antigravity pack directory: $PACK_DIR" >&2
  exit 1
fi

if [[ "$ASSUME_YES" -ne 1 ]]; then
  cat <<EOF
This will install Codebase Wiki LLM for Antigravity into:

  $TARGET_DIR

Existing files with the same names will be overwritten.
EOF
  read -r -p "Continue? [y/N] " answer
  case "$answer" in
    y|Y|yes|YES) ;;
    *)
      echo "installation cancelled"
      exit 0
      ;;
  esac
fi

copy_file "$PACK_DIR/GEMINI.md" "$TARGET_DIR/GEMINI.md"
copy_file "$PACK_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
copy_file "$PACK_DIR/.agent/rules/codebase-wiki.md" "$TARGET_DIR/rules/wiki.md"

copy_file "$PACK_DIR/.agent/workflows/wiki-init.md" "$TARGET_DIR/global_workflows/wiki-init.md"
copy_file "$PACK_DIR/.agent/workflows/wiki-ingest.md" "$TARGET_DIR/global_workflows/wiki-ingest.md"
copy_file "$PACK_DIR/.agent/workflows/wiki-sync.md" "$TARGET_DIR/global_workflows/wiki-sync.md"
copy_file "$PACK_DIR/.agent/workflows/wiki-lint.md" "$TARGET_DIR/global_workflows/wiki-lint.md"

copy_file "$PACK_DIR/.agent/skills/codebase-wiki-maintainer/SKILL.md" "$TARGET_DIR/skills/wiki-maintainer/SKILL.md"
copy_file "$PACK_DIR/.agent/skills/codebase-wiki-maintainer/default-schema.md" "$TARGET_DIR/skills/wiki-maintainer/default-schema.md"

cat <<EOF

Antigravity Wiki LLM installed.

Restart or refresh Antigravity customizations if the files are not picked up
immediately.
EOF
