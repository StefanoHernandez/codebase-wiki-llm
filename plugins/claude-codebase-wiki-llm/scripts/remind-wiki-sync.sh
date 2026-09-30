#!/bin/sh
# Wiki sync note for the next turn. It never blocks the agent.
#   remind-wiki-sync.sh --host claude        Claude Code and Codex (UserPromptSubmit; plain text)
#   remind-wiki-sync.sh --host antigravity   Antigravity (PreInvocation; injectSteps JSON;
#                                            cwd is the plugin folder)
# Reads the hook payload on stdin. The first call of a session records the
# base (HEAD and the changed paths) and stays quiet. Later calls look at
# everything changed since the base, committed or not, and speak when code
# changed and either the wiki did not, or a wiki page listing a changed file
# in `sources:` was not updated; once per changed set of paths. Antigravity
# speaks only on the first model call of a turn (initialNumSteps changes).

host=claude
[ "${1:-}" = "--host" ] && host=${2:-claude}
LC_ALL=C; export LC_ALL
payload=$(cat | tr -d '\n')

quiet() {
  [ "$host" = antigravity ] && printf '{}\n'
  exit 0
}
str() { printf '%s' "$payload" | sed -n 's/.*"'"$1"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p'; }
num() { printf '%s' "$payload" | sed -n 's/.*"'"$1"'"[[:space:]]*:[[:space:]]*"\{0,1\}\([0-9][0-9]*\).*/\1/p'; }

if [ "$host" = antigravity ]; then
  dir=$(printf '%s' "$payload" | sed -n 's/.*"workspacePaths"[[:space:]]*:[[:space:]]*\[[[:space:]]*"\([^"]*\)".*/\1/p')
  key=$(str conversationId)
  turn=$(num initialNumSteps)
  [ -n "$dir" ] || quiet
else
  dir=$(str cwd)
  key=$(str session_id)
  turn=
  [ -n "$dir" ] || dir=$(pwd)
fi
[ -d "$dir" ] || quiet
key=$(printf '%s' "$key" | tr -cd 'A-Za-z0-9_-' | cut -c1-64)
[ -n "$key" ] || key=default

root=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null) || quiet
script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
wiki=$(cd "$root" && sh "$script_dir/resolve-wiki-root.sh" --print-root)
[ -n "$wiki" ] || quiet

state_dir="$(git -C "$root" rev-parse --absolute-git-dir 2>/dev/null)/codebase-wiki"
mkdir -p "$state_dir" 2>/dev/null || quiet
find "$state_dir" -type f -mtime +30 -exec rm -f {} + 2>/dev/null
# save <file> <value>; an unwritable git dir means no note.
save() { { printf '%s\n' "$2" > "$state_dir/$1"; } 2>/dev/null || quiet; }

if [ -n "$turn" ]; then
  [ "$(cat "$state_dir/turn-$key" 2>/dev/null)" = "$turn" ] && quiet
  save "turn-$key" "$turn"
fi

first=no
if [ -f "$state_dir/base-$key" ]; then
  base=$(cat "$state_dir/base-$key")
else
  base=$(git -C "$root" rev-parse -q --verify HEAD 2>/dev/null)
  save "base-$key" "$base"
  first=yes
fi
[ -n "$base" ] || base=$(git -C "$root" hash-object -t tree /dev/null)
git -C "$root" cat-file -e "$base" 2>/dev/null || base=HEAD

# Committed since the base plus uncommitted and untracked; -z avoids git's path quoting.
paths=$({
  git -C "$root" diff --name-only -z "$base" -- 2>/dev/null
  git -C "$root" ls-files -z --others --exclude-standard 2>/dev/null
} | tr '\000' '\n' | sed '/^$/d' | sort -u)
wiki_re=$(printf '%s' "$wiki" | sed 's/\./\\./g')
code=$(printf '%s\n' "$paths" | grep -v -e "^$wiki_re/" -e '^\.wikidir$' -e '^$')
[ -n "$code" ] || quiet
wikichg=$(printf '%s\n' "$paths" | grep -e "^$wiki_re/")

state=$(printf '%s\n%s\n' "$code" "$wikichg" | cksum)
if [ "$first" = yes ]; then save "said-$key" "$state"; quiet; fi
[ "$(cat "$state_dir/said-$key" 2>/dev/null)" = "$state" ] && quiet

tmp=$(mktemp -d 2>/dev/null) || quiet
trap 'rm -rf "$tmp"' EXIT
printf '%s\n' "$code" > "$tmp/code"
printf '%s\n' "$wikichg" > "$tmp/wiki"
# One "page<TAB>source" line per entry of each page's frontmatter `sources:` list.
(cd "$root" && find "$wiki" -type f -name '*.md' -exec awk '
  { sub(/\r$/, "") }
  FNR == 1 { fm = ($0 == "---"); src = 0; next }
  !fm { next }
  $0 == "---" { fm = 0; next }
  /^sources:[[:space:]]*$/ { src = 1; next }
  src && /^[[:space:]]+-[[:space:]]/ {
    s = $0; sub(/^[[:space:]]+-[[:space:]]+/, "", s); sub(/[[:space:]]+$/, "", s)
    gsub(/^["\047`]+|["\047`]+$/, "", s)
    print FILENAME "\t" s; next
  }
  { src = 0 }' {} +) > "$tmp/pairs" 2>/dev/null
# Pages not updated whose sources name a changed file, or a directory above one.
# ponytail: pages x changed files scan; fine for wikis of a few hundred pages.
stale=$(awk -F '\t' '
  FILENAME == ARGV[1] { if ($0 != "") code[$0] = 1; next }
  FILENAME == ARGV[2] { if ($0 != "") done[$0] = 1; next }
  ($1 in done) || ($1 in seen) { next }
  { s = $2; sub(/\/+$/, "", s); if (s == "") next
    for (c in code) if (c == s || index(c, s "/") == 1) { seen[$1] = 1; print $1; break } }
' "$tmp/code" "$tmp/wiki" "$tmp/pairs" | sort)
[ -z "$wikichg" ] || [ -n "$stale" ] || quiet
save "said-$key" "$state"

# list <lines>: the first five, comma separated, then "(+N more)".
list() {
  n=$(printf '%s\n' "$1" | wc -l | tr -d ' ')
  printf '%s\n' "$1" | head -n 5 | awk 'NR > 1 { printf ", " } { printf "%s", $0 }'
  [ "$n" -gt 5 ] && printf ' (+%s more)' "$((n - 5))"
}
msg="Codebase Wiki LLM (note, not a stop): code changed in this session: $(list "$code")."
[ -n "$wikichg" ] || msg="$msg The wiki did not change."
[ -z "$stale" ] || msg="$msg Wiki pages whose sources list these files but were not updated: $(list "$stale")."
msg="$msg Handle the user's message first. When the task that changed the code is done, run the wiki sync workflow (/wiki-sync: log entry, tracker, handoff), or say in one line why no wiki update is needed."

if [ "$host" = antigravity ]; then
  esc=$(printf '%s' "$msg" | tr -d '\000-\037' | sed 's/\\/\\\\/g; s/"/\\"/g')
  printf '{"injectSteps":[{"ephemeralMessage":"%s"}]}\n' "$esc"
else
  printf '%s\n' "$msg"
fi
exit 0
