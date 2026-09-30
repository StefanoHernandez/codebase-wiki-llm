#!/bin/sh
# Stop hook: when files outside the wiki changed and the wiki did not, ask the
# agent once to run the wiki sync workflow.
#   remind-wiki-sync.sh --host claude        Claude Code and Codex
#   remind-wiki-sync.sh --host antigravity   Antigravity (cwd is the plugin folder)
# Reads the hook payload on stdin. Prints nothing and exits 0 when there is
# nothing to say. Only uncommitted changes are seen; commits made during the
# session are covered by the stale-handoff notice at session start.

host=claude
[ "${1:-}" = "--host" ] && host=${2:-claude}
payload=$(cat | tr -d '\n')

case "$payload" in *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;; esac

if [ "$host" = antigravity ]; then
  dir=$(printf '%s' "$payload" | sed -n 's/.*"workspacePaths"[[:space:]]*:[[:space:]]*\[[[:space:]]*"\([^"]*\)".*/\1/p')
  [ -n "$dir" ] || exit 0
else
  dir=$(printf '%s' "$payload" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  [ -n "$dir" ] || dir=$(pwd)
fi
[ -d "$dir" ] || exit 0

root=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null) || exit 0
script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
wiki=$(cd "$root" && sh "$script_dir/resolve-wiki-root.sh" --print-root)
[ -n "$wiki" ] || exit 0

status=$(git -C "$root" status --porcelain --untracked-files=all 2>/dev/null)
[ -n "$status" ] || exit 0

wiki_re=$(printf '%s' "$wiki" | sed 's/\./\\./g')
paths=$(printf '%s\n' "$status" | cut -c4- | sed 's/.* -> //; s/^"//; s/"$//')
inside=$(printf '%s\n' "$paths" | grep -c -e "^$wiki_re/" -e '^\.wikidir$')
outside=$(printf '%s\n' "$paths" | grep -v -c -e "^$wiki_re/" -e '^\.wikidir$')
[ "$outside" -gt 0 ] && [ "$inside" -eq 0 ] || exit 0

marker="$(git -C "$root" rev-parse --absolute-git-dir)/codebase-wiki-sync-reminded"
state=$(printf '%s\n' "$status" | cksum)
[ -f "$marker" ] && [ "$(cat "$marker")" = "$state" ] && exit 0
{ printf '%s\n' "$state" > "$marker"; } 2>/dev/null || exit 0

reason='Code changed but the wiki did not. Run the wiki sync workflow (/wiki-sync): log entry, tracker, handoff. If the change needs no wiki update, say why in one line.'
if [ "$host" = antigravity ]; then
  printf '{"decision":"continue","reason":"%s"}\n' "$reason"
else
  printf '{"decision":"block","reason":"%s"}\n' "$reason"
fi
exit 0
