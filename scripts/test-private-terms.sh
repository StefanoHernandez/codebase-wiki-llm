#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECK="$ROOT_DIR/canonical/codebase/scripts/check-private-terms.sh"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
failures=0

# expect <case> <dir> <expected exit> <args...>; stderr saved in $TMP_DIR/err
expect() {
  local name="$1" dir="$2" want="$3" got=0
  shift 3
  (cd "$dir" && sh "$CHECK" "$@") 2>"$TMP_DIR/err" || got=$?
  [ "$got" = "$want" ] || { echo "FAIL $name: exit $got, expected $want" >&2; cat "$TMP_DIR/err" >&2; failures=$((failures + 1)); }
}

new_repo() {
  local dir="$TMP_DIR/$1"
  mkdir -p "$dir/wiki"
  git -C "$dir" init -q
  printf '%s\n' "$dir"
}

r="$(new_repo no-terms)"; echo "Acme rocket" > "$r/a.txt"; git -C "$r" add a.txt
expect "no terms file passes" "$r" 0

r="$(new_repo staged-hit)"; printf 'Acme\n' > "$r/wiki/.private-terms"
printf 'line one\nWe work with acme corp\n' > "$r/a.txt"; git -C "$r" add a.txt
expect "staged hit blocks" "$r" 1
grep -q "a.txt:2" "$TMP_DIR/err" || { echo "FAIL staged hit: file:line missing" >&2; failures=$((failures + 1)); }
if grep -qi "acme" "$TMP_DIR/err"; then echo "FAIL staged hit: term echoed" >&2; failures=$((failures + 1)); fi

r="$(new_repo unstaged)"; printf 'Acme\n' > "$r/wiki/.private-terms"
echo clean > "$r/a.txt"; git -C "$r" add a.txt; echo "Acme" > "$r/a.txt"
expect "unstaged change passes --staged" "$r" 0
expect "unstaged change fails --all" "$r" 1 --all

r="$(new_repo crlf)"; printf '# partner names\r\n\r\n  Acme  \r\n' > "$r/wiki/.private-terms"
echo "# partner names are here" > "$r/a.txt"; git -C "$r" add a.txt
expect "comment lines are not terms" "$r" 0
echo "ACME" > "$r/b.txt"; git -C "$r" add b.txt
expect "CRLF terms match case-insensitively" "$r" 1

r="$(new_repo schema)"; printf 'Acme\n' > "$r/wiki/.private-terms"
echo "Partner: Acme" > "$r/wiki/SCHEMA.md"; git -C "$r" add wiki/SCHEMA.md
expect "term in committed SCHEMA.md is flagged" "$r" 1

r="$(new_repo self)"; printf 'Acme\n' > "$r/wiki/.private-terms"; git -C "$r" add -f wiki/.private-terms
expect "the terms file itself is excluded" "$r" 0

r="$(new_repo pointer)"; mkdir -p "$r/.wiki"; printf '.wiki\r\n' > "$r/.wikidir"
printf 'Acme\n' > "$r/.wiki/.private-terms"; echo acme > "$r/a.txt"; git -C "$r" add a.txt
expect ".wikidir root is used" "$r" 1

r="$(new_repo empty)"; : > "$r/wiki/.private-terms"; echo acme > "$r/a.txt"; git -C "$r" add a.txt
expect "empty terms file passes" "$r" 0

r="$(new_repo bom-term)"; printf '\357\273\277Acme\r\n' > "$r/wiki/.private-terms"
echo acme > "$r/a.txt"; git -C "$r" add a.txt
expect "BOM-prefixed term matches" "$r" 1

r="$(new_repo bom-comment)"; printf '\357\273\277# names\nAcme\n' > "$r/wiki/.private-terms"
echo "# names here" > "$r/a.txt"; git -C "$r" add a.txt
expect "BOM-prefixed comment is not a term" "$r" 0

r="$(new_repo path-hit)"; printf 'Acme\n' > "$r/wiki/.private-terms"
mkdir -p "$r/docs"; echo clean > "$r/docs/acme-integration.md"; git -C "$r" add docs
expect "term in a staged file name blocks" "$r" 1
grep -q "docs/acme-integration.md" "$TMP_DIR/err" || { echo "FAIL path hit: path missing" >&2; failures=$((failures + 1)); }
expect "term in a tracked file name fails --all" "$r" 1 --all
git -C "$r" mv docs/acme-integration.md docs/integration.md
expect "clean file names pass" "$r" 0

# =term: whole word, case-insensitive; word chars are [A-Za-z0-9_] as in git grep -w.
# ww <case> <terms> <content> <exit> [args]: content staged as a.txt
ww() {
  local r; r="$(new_repo "ww-$RANDOM$RANDOM")"; printf "$2" > "$r/wiki/.private-terms"
  printf '%s\n' "$3" > "$r/a.txt"; git -C "$r" add a.txt
  expect "$1" "$r" "$4"
  if [ "$4" = 1 ] && grep -qi "acme\|secretco" "$TMP_DIR/err"; then echo "FAIL $1: term echoed" >&2; failures=$((failures + 1)); fi
}
ww "whole word blocks" '=Acme\n' "We work with acme corp" 1
ww "whole word ignores longer words" '=Acme\n' "Acmecorp and pacme" 0
ww "whole word stops at hyphen" '=Acme\n' "acme-client" 1
ww "underscore is a word char" '=Acme\n' "acme_client" 0
ww "mixed lines" '=Acme\nSecretCo\n' "mysecretcox" 1
ww "only whole-word terms" '=Acme\n' "nothing here" 0
ww "whole-word CRLF" '=Acme  \r\n' "the acme team" 1
ww "bare equals ignored" '=\n' "anything" 0

r="$(new_repo ww-path)"; printf '=Acme\n' > "$r/wiki/.private-terms"
echo clean > "$r/acme-notes.txt"; git -C "$r" add acme-notes.txt
expect "whole-word file name" "$r" 1
r="$(new_repo ww-path-long)"; printf '=Acme\n' > "$r/wiki/.private-terms"
echo clean > "$r/acmecorp.txt"; git -C "$r" add acmecorp.txt
expect "whole-word file name longer word" "$r" 0
r="$(new_repo ww-all)"; printf '=Acme\n' > "$r/wiki/.private-terms"
echo clean > "$r/a.txt"; git -C "$r" add a.txt; echo "Acme" > "$r/a.txt"
expect "whole-word --all" "$r" 1 --all

r="$(new_repo usage)"
expect "unknown argument" "$r" 2 --bogus

nogit="$TMP_DIR/nogit"; mkdir -p "$nogit"
expect "outside git passes" "$nogit" 0

[ "$failures" -eq 0 ] || { echo "$failures private-terms test(s) failed" >&2; exit 1; }
echo "private-terms tests passed"
