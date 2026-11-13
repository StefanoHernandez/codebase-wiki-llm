#!/bin/sh
# Wiki sync note for the next turn. It never blocks the agent.
#   remind-wiki-sync.sh --host claude        Claude Code and Codex (UserPromptSubmit; plain text)
#   remind-wiki-sync.sh --host antigravity   Antigravity (PreInvocation; injectSteps JSON;
#                                            cwd is the plugin folder)
# Reads the hook payload on stdin. The first call of a session records the
# base (HEAD at that call) and content fingerprints of files already dirty
# then, and stays quiet. Later calls look at code changed since the base,
# committed or not, and at wiki files edited since the base or the last
# covered state (by modification time, so a wiki git ignores works too). They
# speak when code changed and either no wiki file changed, or a wiki page
# listing a changed file in `sources:` was not updated; once per changed set
# of file states. Baseline and covered files stay quiet while their content
# matches the saved fingerprint; editing them again makes them eligible.
# Antigravity speaks only on the first model call of a turn (initialNumSteps
# changes).

host=claude
[ "${1:-}" = "--host" ] && host=${2:-claude}
LC_ALL=C; export LC_ALL
payload=$(cat | tr -d '\n')

quiet() {
  [ "$host" = antigravity ] && printf '{}\n'
  exit 0
}
# say <text>: hand the note to the agent and stop.
say() {
  if [ "$host" = antigravity ]; then
    esc=$(printf '%s' "$1" | tr -d '\000-\037' | sed 's/\\/\\\\/g; s/"/\\"/g')
    printf '{"injectSteps":[{"ephemeralMessage":"%s"}]}\n' "$esc"
  else
    printf '%s\n' "$1"
  fi
  exit 0
}
# field <key>: value of a top-level key; a string is unescaped (\" \\ \/), an array gives its
# first string, a number its digits. Nested objects, key order and spacing do not matter.
field() {
  printf '%s' "$payload" | awk -v want="$1" '
    function str(   o, c, e) {  # at an opening quote; returns the unescaped string
      o = ""; i++
      while (i <= n) {
        c = substr(j, i, 1)
        if (c == "\\") { e = substr(j, i + 1, 1); i += 2
          if (e == "n") o = o "\n"; else if (e == "t") o = o "\t"; else if (e == "u") { o = o "\\u"; } else o = o e
          continue }
        if (c == "\"") { i++; return o }
        o = o c; i++
      }
      return o
    }
    { j = j $0 }
    END {
      n = length(j); d = 0; key = ""; i = 1
      while (i <= n) {
        c = substr(j, i, 1)
        if (c == "\"") {
          t = str()
          if (d == 1 && key == "") { k = t; while (substr(j, i, 1) ~ /[ \t\r]/) i++
            if (substr(j, i, 1) == ":") { key = k; i++ } }
          else if (key == want) { print t; exit }
          else if (d == 1) key = ""
          continue
        }
        if (d == 1 && key == want && c ~ /[0-9]/) { v = ""; while (substr(j, i, 1) ~ /[0-9]/) { v = v substr(j, i, 1); i++ } print v; exit }
        # An object under the wanted key is not a string: stop looking there.
        if (c == "{" || c == "[") { if (d == 1 && key == want && c == "{") key = ""; d++ }
        else if (c == "}" || c == "]") { d--; if (d == 1) key = "" }
        else if (c == "," && d == 1) key = ""
        i++
      }
    }'
}
str() { field "$1"; }
num() { field "$1" | sed -n 's/^\([0-9][0-9]*\).*/\1/p'; }

if [ "$host" = antigravity ]; then
  dir=$(field workspacePaths)
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
  git -C "$root" diff --name-only --no-renames -z "$base" -- 2>/dev/null
  git -C "$root" ls-files -z --others --exclude-standard 2>/dev/null
} | tr '\000' '\n' | sed '/^$/d' | sort -u)
wiki_re=$(printf '%s' "$wiki" | sed 's/\./\\./g')
code=$(printf '%s\n' "$paths" | grep -v -e "^$wiki_re/" -e '^\.wikidir$' -e '^$')
covered="$state_dir/covered-$key"
# Saved paths may have returned to HEAD or disappeared from the untracked list.
[ ! -f "$covered" ] || code=$({ printf '%s\n' "$code"; awk -F '\t' 'NF == 2 { print $1 }' "$covered"; } | sed '/^$/d' | sort -u)
# One path<TAB>fingerprint record per source state; deletions differ from blobs.
code_states=$(printf '%s\n' "$code" | while IFS= read -r path; do
  [ -n "$path" ] || continue
  if [ -L "$root/$path" ]; then
    # A link's Git content is its target text; never follow the referent.
    fingerprint=unavailable
  elif [ -f "$root/$path" ]; then
    if fingerprint=$(git -C "$root" hash-object --no-filters -- "$root/$path" 2>/dev/null); then
      fingerprint="blob:$fingerprint"
    else
      # Unreadable files must not silence other changed sources.
      fingerprint=unavailable
    fi
  elif [ -e "$root/$path" ]; then
    # Gitlinks and special files (including FIFOs) cannot be blob-hashed.
    fingerprint=unavailable
  else
    fingerprint=deleted
  fi
  printf '%s\t%s\n' "$path" "$fingerprint"
done) || quiet
# Only the same content as the baseline or the latest wiki coverage is excluded.
# Legacy path-only records cannot match a fingerprint and are ignored safely.
if [ "$first" = yes ]; then
  save "covered-$key" "$code_states"
  # Antigravity has no SessionStart hook: its first call carries the stale-handoff line instead.
  if [ "$host" = antigravity ]; then
    old=$(cd "$root" && sh "$script_dir/resolve-wiki-root.sh" | grep '^Codebase Wiki LLM: handoff is ')
    [ -z "$old" ] || say "$old"
  fi
  quiet
fi
if [ -f "$covered" ]; then
  code_states=$(printf '%s\n' "$code_states" | awk -F '\t' '
    FILENAME == ARGV[1] { if (NF == 2) covered[$1] = $2; next }
    NF == 2 && ($2 == "unavailable" || !($1 in covered) || covered[$1] != $2)
  ' "$covered" -)
fi
code=$(printf '%s\n' "$code_states" | cut -f1)
if [ -z "$code" ]; then save "said-$key" ""; quiet; fi
# Wiki files edited since the last covered state, or since the session start.
since="$state_dir/stamp-$key"
[ -f "$since" ] || since="$state_dir/base-$key"
wikichg=$(cd "$root" && find "$wiki" -type f -newer "$since" ! -name .private-terms 2>/dev/null | sort)

state=$(printf '%s\n%s\n' "$code_states" "$wikichg" | cksum)
# Without a content fingerprint, repeated notes are safer than hiding edits.
unfingerprinted=$(printf '%s\n' "$code_states" | awk -F '\t' '$2 == "unavailable" { print "yes"; exit }')
if [ -z "$unfingerprinted" ]; then
  [ "$(cat "$state_dir/said-$key" 2>/dev/null)" = "$state" ] && quiet
fi

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
    gsub(/^["\047`]+|["\047`]+$/, "", s); sub(/^\.\//, "", s); sub(/[:#][^\/]*$/, "", s)
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
if [ -n "$wikichg" ] && [ -z "$stale" ]; then
  # Replace coverage for these paths, retaining the other baseline/covered states.
  coverage=$({ [ ! -f "$covered" ] || cat "$covered"; printf '%s\n' "$code_states"; } |
    awk -F '\t' 'NF == 2 { states[$1] = $0 } END { for (path in states) print states[path] }' | sort)
  save "covered-$key" "$coverage"
  save "stamp-$key" ""
  save "said-$key" ""
  quiet
fi
save "said-$key" "$state"

# list <lines>: the first five, comma separated, then "(+N more)".
list() {
  n=$(printf '%s\n' "$1" | wc -l | tr -d ' ')
  printf '%s\n' "$1" | head -n 5 | awk 'NR > 1 { printf ", " } { printf "%s", $0 }'
  [ "$n" -gt 5 ] && printf ' (+%s more)' "$((n - 5))"
}
msg="Codebase Wiki LLM (note, not a stop): code changed since this session started that the wiki does not cover yet: $(list "$code")."
[ -n "$wikichg" ] || msg="$msg The wiki did not change."
[ -z "$stale" ] || msg="$msg Wiki pages whose sources list these files but were not updated: $(list "$stale")."
msg="$msg Handle the user's message first. When the task that changed the code is done, run the wiki sync workflow (/wiki-sync: log entry, tracker, handoff), or say in one line why no wiki update is needed."

say "$msg"
