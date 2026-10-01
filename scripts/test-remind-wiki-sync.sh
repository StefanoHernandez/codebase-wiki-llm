#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$ROOT_DIR/canonical/codebase/scripts/remind-wiki-sync.sh"
TMP_DIR="$(mktemp -d)"
trap 'chmod -R u+w "$TMP_DIR" 2>/dev/null; rm -rf "$TMP_DIR"' EXIT
failures=0
TAIL="Handle the user's message first. When the task that changed the code is done, run the wiki sync workflow (/wiki-sync: log entry, tracker, handoff), or say in one line why no wiki update is needed."

# note <changed files> <wiki changed: yes|no> [pages not updated]  (mirrors the hook's wording)
note() {
  local m="Codebase Wiki LLM (note, not a stop): code changed since this session started that the wiki does not cover yet: $1."
  [ "$2" = yes ] || m="$m The wiki did not change."
  [ -z "${3:-}" ] || m="$m Wiki pages whose sources list these files but were not updated: $3."
  printf '%s' "$m $TAIL"
}

# run <case> <expected stdout> <payload> <args...>  (runs from $TMP_DIR, not the repo)
run() {
  local name="$1" expected="$2" payload="$3" actual
  shift 3
  actual="$(cd "$TMP_DIR" && printf '%s' "$payload" | sh "$HOOK" "$@")" || { echo "FAIL $name: exit non-zero" >&2; failures=$((failures + 1)); return; }
  [ "$actual" = "$expected" ] || { echo "FAIL $name: expected [$expected] got [$actual]" >&2; failures=$((failures + 1)); }
}

# Keep special-file regressions bounded and terminate blocked hook descendants.
run_bounded() {
  local name="$1" expected="$2" payload="$3" actual status=0
  actual="$(cd "$TMP_DIR" && printf '%s' "$payload" | timeout --kill-after=1 3 sh "$HOOK" --host claude)" || status=$?
  if [ "$status" -ne 0 ]; then
    echo "FAIL $name: hook did not finish successfully within 3s (exit $status)" >&2
    failures=$((failures + 1)); return
  fi
  [ "$actual" = "$expected" ] || { echo "FAIL $name: expected [$expected] got [$actual]" >&2; failures=$((failures + 1)); }
}

commit() { git -C "$1" add -A; git -C "$1" -c user.email=t@example.com -c user.name=t commit -qm "${2:-c}"; }
new_repo() {
  local dir="$TMP_DIR/$1"
  mkdir -p "$dir/wiki"; touch "$dir/wiki/SCHEMA.md"
  git -C "$dir" init -q
  commit "$dir" init
  printf '%s\n' "$dir"
}
# page <repo> <page file> <source>...  writes a wiki page whose frontmatter lists the sources
page() {
  local repo="$1" p="$2"; shift 2
  { echo '---'; echo 'title: T'; echo 'sources:'; for s in "$@"; do echo "  - $s"; done; echo '---'; echo body; } > "$repo/wiki/$p"
}
claude() { printf '{"session_id":"%s","cwd":"%s","hook_event_name":"UserPromptSubmit","prompt":"hi"}' "${2:-s1}" "$1"; }
agy() { printf '{"conversationId":"%s","workspacePaths":["%s"],"invocationNum":1,"initialNumSteps":%s}' "${3:-c1}" "$1" "$2"; }

r="$(new_repo clean)"
run "first call records the baseline quietly" "" "$(claude "$r")" --host claude
run "clean tree is quiet" "" "$(claude "$r")" --host claude

r="$(new_repo dirty-start)"; echo x > "$r/main.c"
run "changes from before the session are baseline" "" "$(claude "$r")" --host claude
run "baseline state stays quiet" "" "$(claude "$r")" --host claude
echo v2 > "$r/main.c"
run "editing an initially dirty file is a new change" "$(note main.c no)" "$(claude "$r")" --host claude
run "unchanged initially dirty edit stays quiet" "" "$(claude "$r")" --host claude
echo y > "$r/other.c"
run "a new change names only the files changed in the session" "$(note 'main.c, other.c' no)" "$(claude "$r")" --host claude

r="$(new_repo code)"; run "baseline" "" "$(claude "$r")" --host claude
echo x > "$r/main.c"
run "code change without wiki change notes" "$(note main.c no)" "$(claude "$r")" --host claude
run "same state is noted once" "" "$(claude "$r")" --host claude
echo v2 > "$r/main.c"
run "new content at an already-notified path is noted again" "$(note main.c no)" "$(claude "$r")" --host claude
run "same second edit is noted once" "" "$(claude "$r")" --host claude
run "another session has its own baseline" "" "$(claude "$r" s2)" --host claude
for f in a b c d e f; do echo x > "$r/$f.c"; done
run "long lists are cut at five" "$(note 'a.c, b.c, c.c, d.c, e.c (+2 more)' no)" "$(claude "$r")" --host claude

r="$(new_repo covered)"; page "$r" api.md src/api.c; commit "$r" pages
run "baseline" "" "$(claude "$r")" --host claude
mkdir -p "$r/src"; echo x > "$r/src/api.c"; echo entry > "$r/wiki/log.md"
run "wiki changed but a page listing the file did not" "$(note src/api.c yes wiki/api.md)" "$(claude "$r")" --host claude
echo more >> "$r/wiki/api.md"
run "updating the page that lists the file is quiet" "" "$(claude "$r")" --host claude
run "unchanged covered content stays quiet" "" "$(claude "$r")" --host claude
echo v2 > "$r/src/api.c"
run "editing a covered source makes it eligible again" "$(note src/api.c no wiki/api.md)" "$(claude "$r")" --host claude
run "unchanged second edit stays quiet" "" "$(claude "$r")" --host claude

r="$(new_repo deletion)"; echo v1 > "$r/main.c"; page "$r" main.md main.c; commit "$r" source
run "deletion baseline" "" "$(claude "$r")" --host claude
rm "$r/main.c"
run "deleted source is noted" "$(note main.c no wiki/main.md)" "$(claude "$r")" --host claude
run "unchanged deletion stays quiet" "" "$(claude "$r")" --host claude
echo entry >> "$r/wiki/main.md"
run "deletion covered by the wiki stays quiet" "" "$(claude "$r")" --host claude
run "unchanged covered deletion stays quiet" "" "$(claude "$r")" --host claude
echo v2 > "$r/main.c"
run "recreating a covered deleted source is noted" "$(note main.c no wiki/main.md)" "$(claude "$r")" --host claude

r="$(new_repo legacy-state)"
run "legacy state baseline" "" "$(claude "$r")" --host claude
printf 'main.c\n' > "$r/.git/codebase-wiki/covered-s1"
echo v2 > "$r/main.c"
run "legacy path-only coverage cannot hide new content" "$(note main.c no)" "$(claude "$r")" --host claude

r="$(new_repo source-spaces)"; echo v1 > "$r/my source.c"; page "$r" source.md 'my source.c'; commit "$r" source
echo v2 > "$r/my source.c"
run "source with spaces starts dirty quietly" "" "$(claude "$r")" --host claude
echo v3 > "$r/my source.c"
run "new content at an initially dirty spaced path is noted" "$(note 'my source.c' no wiki/source.md)" "$(claude "$r")" --host claude
echo entry >> "$r/wiki/source.md"
run "spaced source is covered quietly" "" "$(claude "$r")" --host claude
echo v4 > "$r/my source.c"
run "new content at a covered spaced path is noted" "$(note 'my source.c' no wiki/source.md)" "$(claude "$r")" --host claude

r="$(new_repo restore-covered)"; echo v1 > "$r/main.c"; page "$r" main.md main.c; commit "$r" source
run "restored source baseline" "" "$(claude "$r")" --host claude
echo v2 > "$r/main.c"
run "restored source first edit is noted" "$(note main.c no wiki/main.md)" "$(claude "$r")" --host claude
echo entry >> "$r/wiki/main.md"
run "restored source edit is covered" "" "$(claude "$r")" --host claude
echo v1 > "$r/main.c"
run "restoring a covered source to HEAD is still a new state" "$(note main.c no wiki/main.md)" "$(claude "$r")" --host claude
echo entry >> "$r/wiki/main.md"
run "restored source is covered again" "" "$(claude "$r")" --host claude
echo v2 > "$r/main.c"
run "returning to earlier content after coverage is noted" "$(note main.c no wiki/main.md)" "$(claude "$r")" --host claude

r="$(new_repo removed-baseline)"; echo v1 > "$r/main.c"
run "untracked baseline before deletion" "" "$(claude "$r")" --host claude
rm "$r/main.c"
run "removing an initially untracked file is a new state" "$(note main.c no)" "$(claude "$r")" --host claude
run "unchanged removed baseline stays quiet" "" "$(claude "$r")" --host claude

sub="$(new_repo submodule-source)"; echo v1 > "$sub/main.c"; commit "$sub" source
r="$(new_repo submodule-parent)"
git -C "$r" -c protocol.file.allow=always submodule add -q "$sub" module
commit "$r" submodule
run "submodule baseline" "" "$(claude "$r")" --host claude
echo v2 > "$r/module/main.c"; echo v1 > "$r/main.c"
run "a changed submodule does not hide ordinary source changes" "$(note 'main.c, module' no)" "$(claude "$r")" --host claude
echo v3 > "$r/module/main.c"
run "another submodule edit cannot be silently deduplicated" "$(note 'main.c, module' no)" "$(claude "$r")" --host claude

r="$(new_repo fifo)"; echo v1 > "$r/main.c"; commit "$r" source
run "FIFO source baseline" "" "$(claude "$r")" --host claude
rm "$r/main.c"; mkfifo "$r/main.c"
run_bounded "a tracked source replaced by a FIFO cannot block" "$(note main.c no)" "$(claude "$r")"

r="$(new_repo dangling-symlink)"; ln -s missing-a "$r/linked.c"; commit "$r" source
run "dangling symlink baseline" "" "$(claude "$r")" --host claude
ln -sf missing-b "$r/linked.c"
run "first dangling symlink target edit is noted" "$(note linked.c no)" "$(claude "$r")" --host claude
ln -sf missing-c "$r/linked.c"
run "another dangling symlink target edit is noted" "$(note linked.c no)" "$(claude "$r")" --host claude
echo entry > "$r/wiki/log.md"
run "dangling symlink edit can be covered" "" "$(claude "$r")" --host claude
ln -sf missing-d "$r/linked.c"
run "a covered dangling symlink target edit is noted" "$(note linked.c no)" "$(claude "$r")" --host claude

r="$(new_repo dirty-symlink)"; ln -s missing-a "$r/linked.c"; commit "$r" source
ln -sf missing-b "$r/linked.c"
run "initially dirty dangling symlink baseline" "" "$(claude "$r")" --host claude
ln -sf missing-c "$r/linked.c"
run "an initially dirty dangling symlink target edit is noted" "$(note linked.c no)" "$(claude "$r")" --host claude

r="$(new_repo equal-symlink-targets)"; echo v1 > "$r/a.c"; echo v1 > "$r/b.c"; echo v1 > "$r/c.c"
ln -s a.c "$r/linked.c"; commit "$r" source
run "equal symlink referents baseline" "" "$(claude "$r")" --host claude
ln -sf b.c "$r/linked.c"
run "first symlink target edit with equal referent bytes is noted" "$(note linked.c no)" "$(claude "$r")" --host claude
ln -sf c.c "$r/linked.c"
run "another symlink target edit with equal referent bytes is noted" "$(note linked.c no)" "$(claude "$r")" --host claude

r="$(new_repo symlink-fifo)"; echo v1 > "$r/linked.c"; commit "$r" source
run "symlink to FIFO baseline" "" "$(claude "$r")" --host claude
mkfifo "$TMP_DIR/source.fifo"; ln -sf "$TMP_DIR/source.fifo" "$r/linked.c"
run_bounded "a source symlink to a FIFO cannot block" "$(note linked.c no)" "$(claude "$r")"

r="$(new_repo unlisted)"; page "$r" api.md src/api.c; commit "$r" pages
run "baseline" "" "$(claude "$r")" --host claude
echo x > "$r/main.c"; echo entry > "$r/wiki/log.md"
run "file listed by no page is covered by any wiki change" "" "$(claude "$r")" --host claude

r="$(new_repo nowiki-stale)"; page "$r" api.md src/api.c; commit "$r" pages
run "baseline" "" "$(claude "$r")" --host claude
mkdir -p "$r/src"; echo x > "$r/src/api.c"
run "no wiki change also names the pages listing the file" "$(note src/api.c no wiki/api.md)" "$(claude "$r")" --host claude

r="$(new_repo dirsrc)"; page "$r" mod.md src/; commit "$r" pages
run "baseline" "" "$(claude "$r")" --host claude
echo x > "$r/srcfoo.c"; echo entry > "$r/wiki/log.md"
run "directory source needs a path boundary" "" "$(claude "$r")" --host claude
mkdir -p "$r/src/deep"; echo x > "$r/src/deep/a.c"
run "directory source covers files below it" "$(note src/deep/a.c no wiki/mod.md)" "$(claude "$r")" --host claude

r="$(new_repo unlisted-next)"; page "$r" api.md src/api.c; commit "$r" pages
run "baseline" "" "$(claude "$r")" --host claude
echo x > "$r/main.c"; echo entry > "$r/wiki/log.md"
run "covered by a wiki change" "" "$(claude "$r")" --host claude
echo x > "$r/b.c"
run "a change after the wiki covered the last one is noted" "$(note b.c no)" "$(claude "$r")" --host claude

r="$TMP_DIR/ignored"; mkdir -p "$r/.wiki" "$r/src"; git -C "$r" init -q
printf '.wiki/\n' > "$r/.gitignore"; printf '.wiki\n' > "$r/.wikidir"; touch "$r/.wiki/SCHEMA.md"
{ echo '---'; echo 'title: T'; echo 'sources:'; echo '  - src/api.c'; echo '---'; echo body; } > "$r/.wiki/api.md"
echo v1 > "$r/src/api.c"; commit "$r" init
run "ignored wiki: baseline" "" "$(claude "$r")" --host claude
echo v2 > "$r/src/api.c"
run "ignored wiki: the page listing the file is named" "$(note src/api.c no .wiki/api.md)" "$(claude "$r")" --host claude
echo more >> "$r/.wiki/api.md"
run "ignored wiki: updating the page is seen" "" "$(claude "$r")" --host claude

r="$(new_repo rename-src)"; mkdir -p "$r/src"; echo x > "$r/src/old.c"; page "$r" api.md src/old.c; commit "$r" pages
run "baseline" "" "$(claude "$r")" --host claude
git -C "$r" mv src/old.c src/new.c; echo entry > "$r/wiki/log.md"
run "a renamed source keeps its old path" "$(note 'src/new.c, src/old.c' yes wiki/api.md)" "$(claude "$r")" --host claude

r="$(new_repo src-suffix)"; page "$r" api.md './src/api.c:12' 'src/b.c#main'; commit "$r" pages
run "baseline" "" "$(claude "$r")" --host claude
mkdir -p "$r/src"; echo x > "$r/src/api.c"; echo x > "$r/src/b.c"; echo entry > "$r/wiki/log.md"
run "sources with ./, :line and #symbol still match" "$(note 'src/api.c, src/b.c' yes wiki/api.md)" "$(claude "$r")" --host claude

r="$(new_repo committed)"; run "baseline" "" "$(claude "$r")" --host claude
echo x > "$r/main.c"; commit "$r" code
run "code committed during the session is seen" "$(note main.c no)" "$(claude "$r")" --host claude
echo entry > "$r/wiki/log.md"; commit "$r" wiki
run "wiki committed during the session covers it" "" "$(claude "$r")" --host claude

r="$(new_repo wikidir)"; run "baseline" "" "$(claude "$r")" --host claude
printf 'wiki\n' > "$r/.wikidir"
run ".wikidir change alone is quiet" "" "$(claude "$r")" --host claude

r="$(new_repo spaces)"; run "baseline" "" "$(claude "$r")" --host claude
echo x > "$r/wiki/my page.md"
run "wiki path with spaces counts as wiki" "" "$(claude "$r")" --host claude

r="$(new_repo rename)"; echo a > "$r/wiki/a.md"; commit "$r" a
run "baseline" "" "$(claude "$r")" --host claude
git -C "$r" mv wiki/a.md wiki/b.md
run "rename inside wiki is quiet" "" "$(claude "$r")" --host claude

nowiki="$TMP_DIR/nowiki"; mkdir -p "$nowiki"; git -C "$nowiki" init -q; echo x > "$nowiki/main.c"
run "repo without wiki is quiet" "" "$(claude "$nowiki")" --host claude
run "repo without wiki stays quiet" "" "$(claude "$nowiki")" --host claude

nocommit="$TMP_DIR/nocommit"; mkdir -p "$nocommit/wiki"; touch "$nocommit/wiki/SCHEMA.md"; git -C "$nocommit" init -q; echo x > "$nocommit/main.c"
run "repo without commits: baseline" "" "$(claude "$nocommit")" --host claude
echo y > "$nocommit/b.c"
run "repo without commits: new code after the baseline is noted" "$(note b.c no)" "$(claude "$nocommit")" --host claude

r="$(new_repo readonly)"; chmod a-w "$r/.git"
echo x > "$r/main.c"
run "unwritable git dir is quiet" "" "$(claude "$r")" --host claude
run "unwritable git dir stays quiet" "" "$(claude "$r")" --host claude
chmod u+w "$r/.git"

r="$(new_repo evil-key)"
run "session id is sanitised" "" "$(claude "$r" '../../evil')" --host claude
[ -f "$r/.git/codebase-wiki/base-evil" ] || { echo "FAIL sanitised state file missing" >&2; failures=$((failures + 1)); }
[ ! -e "$TMP_DIR/evil" ] && [ ! -e "$r/evil" ] || { echo "FAIL state file escaped the state dir" >&2; failures=$((failures + 1)); }

r="$(new_repo fake-cwd)"
fake() { printf '%s' '{"session_id":"s1","cwd":"'"$r"'","prompt":"x \"cwd\":\"/nonexistent\""}'; }
run "prompt text cannot redirect cwd: baseline" "" "$(fake)" --host claude
echo x > "$r/main.c"
run "prompt text cannot redirect cwd" "$(note main.c no)" "$(fake)" --host claude

r="$(new_repo agy)"
run "antigravity baseline prints an empty object" "{}" "$(agy "$r" 10)" --host antigravity
echo x > "$r/main.c"
run "antigravity stays quiet within a turn" "{}" "$(agy "$r" 10)" --host antigravity
run "antigravity new turn injects an ephemeral message" "{\"injectSteps\":[{\"ephemeralMessage\":\"$(note main.c no)\"}]}" "$(agy "$r" 14)" --host antigravity
run "antigravity same state stays quiet" "{}" "$(agy "$r" 20)" --host antigravity
run "antigravity without workspacePaths is quiet" "{}" '{"conversationId":"c"}' --host antigravity

r="$(new_repo agy-quote)"
run "antigravity quote baseline" "{}" "$(agy "$r" 1)" --host antigravity
echo x > "$r/a\"b.c"
out="$(cd "$TMP_DIR" && agy "$r" 2 | sh "$HOOK" --host antigravity)"
printf '%s' "$out" | python3 -c 'import json,sys; m=json.load(sys.stdin)["injectSteps"][0]["ephemeralMessage"]; assert "a\"b.c" in m, m' \
  || { echo "FAIL antigravity message with a quote in a file name is not valid JSON: $out" >&2; failures=$((failures + 1)); }

[ "$failures" -eq 0 ] || { echo "$failures remind-wiki-sync test(s) failed" >&2; exit 1; }
echo "remind-wiki-sync tests passed"
