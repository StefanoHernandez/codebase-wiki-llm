#!/bin/sh
# Print this repository's Codebase Wiki root for the agent session context.
# Claude Code runs it as a plugin SessionStart hook; the resolution rule is
# canonical/codebase/partials/resolve-wiki-root.md.
# Copied into plugins/claude-codebase-wiki-llm/scripts/ by
# scripts/generate-codebase-packages.py.
# Always exits 0 and prints nothing when the repository has no wiki.
# The pointer is repository content: an invalid value is never echoed.

root=$(git rev-parse --show-toplevel 2>/dev/null) || root=$(pwd)
pointer="$root/.wikidir"

if [ -f "$pointer" ]; then
  # Drop NUL bytes, UTF-8/UTF-16 BOM bytes and CR so files written by
  # PowerShell still read as plain ASCII; valid names are ASCII only.
  value=$(tr -d '\000\015\357\273\277\376\377' < "$pointer" | sed -n '/[^[:space:]]/{p;q;}' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
  lower=$(printf '%s\n' "$value" | tr '[:upper:]' '[:lower:]')
  case "$lower" in
    .git|.github|.claude|.codex|.agents|.agent|.gemini|.opencode|.obsidian|.vscode|node_modules|.wikidir)
      valid=no ;;
    *)
      if printf '%s\n' "$value" | grep -Eq '^\.?[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9_-])?$'; then
        valid=yes
      else
        valid=no
      fi ;;
  esac
  if [ "$valid" = no ]; then
    echo "Codebase Wiki LLM: .wikidir does not contain a valid wiki folder name."
  elif [ -d "$root/$value" ]; then
    echo "Codebase Wiki LLM: wiki_root: $value"
  else
    echo "Codebase Wiki LLM: .wikidir points to missing directory $value."
  fi
elif [ -f "$root/wiki/SCHEMA.md" ]; then
  echo "Codebase Wiki LLM: wiki_root: wiki"
fi
exit 0
