#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${ANTIGRAVITY_HOME:-$HOME/.gemini/antigravity}"
ASSUME_YES=0

usage() {
  cat <<'USAGE'
Uninstall Codebase Wiki LLM files from Antigravity.

Removes only files this project's install script created. Other files in
$TARGET_DIR are left untouched.

Usage:
  scripts/uninstall-antigravity-wiki-llm.sh [--yes]

Environment:
  ANTIGRAVITY_HOME  Override target directory.
                    Default: $HOME/.gemini/antigravity

Removes from $TARGET_DIR:
  rules/wiki.md
  skills/wiki-maintainer/SKILL.md
  skills/wiki-maintainer/default-schema.md
  skills/wiki-maintainer/        (if empty after removals)
  global_workflows/wiki-init.md
  global_workflows/wiki-ingest.md
  global_workflows/wiki-sync.md
  global_workflows/wiki-lint.md
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

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "nothing to remove: $TARGET_DIR does not exist"
  exit 0
fi

FILES=(
  "$TARGET_DIR/GEMINI.md"
  "$TARGET_DIR/AGENTS.md"
  "$TARGET_DIR/rules/wiki.md"
  "$TARGET_DIR/global_workflows/wiki-init.md"
  "$TARGET_DIR/global_workflows/wiki-ingest.md"
  "$TARGET_DIR/global_workflows/wiki-sync.md"
  "$TARGET_DIR/global_workflows/wiki-lint.md"
  "$TARGET_DIR/skills/wiki-maintainer/SKILL.md"
  "$TARGET_DIR/skills/wiki-maintainer/default-schema.md"
)

DIRS=(
  "$TARGET_DIR/skills/wiki-maintainer"
)

if [[ "$ASSUME_YES" -ne 1 ]]; then
  cat <<EOF
This will remove Codebase Wiki LLM files from:

  $TARGET_DIR

The following files will be deleted if they exist:
EOF
  for f in "${FILES[@]}"; do
    echo "  $f"
  done
  echo
  read -r -p "Continue? [y/N] " answer
  case "$answer" in
    y|Y|yes|YES) ;;
    *)
      echo "uninstall cancelled"
      exit 0
      ;;
  esac
fi

removed=0
for f in "${FILES[@]}"; do
  if [[ -f "$f" ]]; then
    rm -f "$f"
    echo "removed $f"
    removed=$((removed + 1))
  fi
done

for d in "${DIRS[@]}"; do
  if [[ -d "$d" ]] && [[ -z "$(ls -A "$d")" ]]; then
    rmdir "$d"
    echo "removed empty dir $d"
  fi
done

cat <<EOF

Codebase Wiki LLM uninstalled. $removed file(s) removed.

Run "scripts/install-antigravity-wiki-llm.sh" to reinstall.
EOF
