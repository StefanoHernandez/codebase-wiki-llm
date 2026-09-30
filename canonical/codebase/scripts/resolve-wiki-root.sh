#!/bin/sh
# Print this repository's Codebase Wiki root for the agent session context.
# Claude Code and Codex run it as a plugin SessionStart hook; the resolution
# rule is canonical/codebase/partials/resolve-wiki-root.md.
# Copied into the host packages by scripts/generate-codebase-packages.py.
# --print-root: print only the bare root value (for other scripts), or nothing.
# Always exits 0 and prints nothing when the repository has no wiki.
# The pointer is repository content: an invalid value is never echoed.

STALE_COMMITS=5
mode=context
[ "${1:-}" = "--print-root" ] && mode=print

root=$(git rev-parse --show-toplevel 2>/dev/null) || root=$(pwd)
pointer="$root/.wikidir"
wiki=
msg=

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
    msg="Codebase Wiki LLM: .wikidir does not contain a valid wiki folder name."
  elif [ -d "$root/$value" ]; then
    wiki=$value
  else
    msg="Codebase Wiki LLM: .wikidir points to missing directory $value."
  fi
elif [ -f "$root/wiki/SCHEMA.md" ]; then
  wiki=wiki
fi

if [ "$mode" = print ]; then
  [ -n "$wiki" ] && printf '%s\n' "$wiki"
  exit 0
fi

[ -n "$msg" ] && echo "$msg"
[ -n "$wiki" ] || exit 0
echo "Codebase Wiki LLM: wiki_root: $wiki"

# Core map path for a role, relative to the wiki root; default when absent or unsafe.
core_path() {
  p=$(sed -n "s/^|[[:space:]]*$1[[:space:]]*|[[:space:]]*\`\{0,1\}\([^\`|]*\)\`\{0,1\}[[:space:]]*|.*/\1/p" "$root/$wiki/SCHEMA.md" 2>/dev/null | head -n 1 | sed 's/[[:space:]]*$//')
  case "$p" in ''|/*|*..*) p=$2 ;; esac
  printf '%s\n' "$p"
}

handoff="$wiki/$(core_path handoff agent/handoff.md)"
if [ -f "$root/$handoff" ]; then
  last=$(git -C "$root" log -1 --format=%H -- "$handoff" 2>/dev/null)
  if [ -n "$last" ]; then
    n=$(git -C "$root" rev-list --count "$last..HEAD" 2>/dev/null) || n=0
    if [ "$n" -ge "$STALE_COMMITS" ]; then
      echo "Codebase Wiki LLM: handoff is $n commits old ($handoff); read it and refresh it before relying on it."
    fi
  fi
fi
exit 0
