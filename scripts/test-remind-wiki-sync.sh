#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$ROOT_DIR/canonical/codebase/scripts/remind-wiki-sync.sh"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
failures=0
REASON='Code changed but the wiki did not. Run the wiki sync workflow (/wiki-sync): log entry, tracker, handoff. If the change needs no wiki update, say why in one line.'
BLOCK="{\"decision\":\"block\",\"reason\":\"$REASON\"}"
CONTINUE="{\"decision\":\"continue\",\"reason\":\"$REASON\"}"

# run <case> <expected stdout> <payload> <args...>  (runs from $TMP_DIR, not the repo)
run() {
  local name="$1" expected="$2" payload="$3" actual
  shift 3
  actual="$(cd "$TMP_DIR" && printf '%s' "$payload" | sh "$HOOK" "$@")" || { echo "FAIL $name: exit non-zero" >&2; failures=$((failures + 1)); return; }
  [ "$actual" = "$expected" ] || { echo "FAIL $name: expected [$expected] got [$actual]" >&2; failures=$((failures + 1)); }
}

new_repo() {
  local dir="$TMP_DIR/$1"
  mkdir -p "$dir/wiki"; touch "$dir/wiki/SCHEMA.md"
  git -C "$dir" init -q
  git -C "$dir" add -A
  git -C "$dir" -c user.email=t@example.com -c user.name=t commit -qm init
  printf '%s\n' "$dir"
}
claude() { printf '{"session_id":"s","cwd":"%s","stop_hook_active":%s}' "$1" "${2:-false}"; }

r="$(new_repo clean)"
run "clean tree is silent" "" "$(claude "$r")" --host claude

r="$(new_repo code)"; echo x > "$r/main.c"
run "code change without wiki change blocks" "$BLOCK" "$(claude "$r")" --host claude
run "same state is reminded once" "" "$(claude "$r")" --host claude
echo y > "$r/other.c"
run "new state reminds again" "$BLOCK" "$(claude "$r")" --host claude

r="$(new_repo readonly)"; echo x > "$r/main.c"; chmod a-w "$r/.git"
run "unwritable marker is silent" "" "$(claude "$r")" --host claude
run "unwritable marker stays silent" "" "$(claude "$r")" --host claude
chmod u+w "$r/.git"

r="$(new_repo both)"; echo x > "$r/main.c"; echo note >> "$r/wiki/SCHEMA.md"
run "code and wiki changed is silent" "" "$(claude "$r")" --host claude

r="$(new_repo active)"; echo x > "$r/main.c"
run "stop_hook_active is silent" "" "$(claude "$r" true)" --host claude

r="$(new_repo wikidir)"; printf 'wiki\n' > "$r/.wikidir"
run ".wikidir change alone is silent" "" "$(claude "$r")" --host claude

r="$(new_repo spaces)"; echo x > "$r/wiki/my page.md"
run "wiki path with spaces counts as wiki" "" "$(claude "$r")" --host claude

r="$(new_repo rename)"; echo a > "$r/wiki/a.md"
git -C "$r" add -A; git -C "$r" -c user.email=t@example.com -c user.name=t commit -qm a
git -C "$r" mv wiki/a.md wiki/b.md
run "rename inside wiki is silent" "" "$(claude "$r")" --host claude

nowiki="$TMP_DIR/nowiki"; mkdir -p "$nowiki"; git -C "$nowiki" init -q; echo x > "$nowiki/main.c"
run "repo without wiki is silent" "" "$(claude "$nowiki")" --host claude

nocommit="$TMP_DIR/nocommit"; mkdir -p "$nocommit/wiki"; touch "$nocommit/wiki/SCHEMA.md"; git -C "$nocommit" init -q; echo x > "$nocommit/main.c"
run "repo without commits exits quietly (untracked wiki counts as wiki)" "" "$(claude "$nocommit")" --host claude

r="$(new_repo agy)"; echo x > "$r/main.c"
run "antigravity uses workspacePaths" "$CONTINUE" "{\"conversationId\":\"c\",\"workspacePaths\":[\"$r\"],\"fullyIdle\":true}" --host antigravity
run "antigravity without workspacePaths is silent" "" '{"conversationId":"c"}' --host antigravity

[ "$failures" -eq 0 ] || { echo "$failures remind-wiki-sync test(s) failed" >&2; exit 1; }
echo "remind-wiki-sync tests passed"
