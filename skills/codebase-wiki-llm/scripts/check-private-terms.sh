#!/bin/sh
# Block content that contains a term listed in <wiki-root>/.private-terms.
#   (no argument) / --staged  search the git index (git pre-commit hook)
#   --all                     search tracked files in the working tree (/wiki-lint)
# Both modes also check tracked and staged file names. Binary files are skipped.
# /wiki-init copies this file into the git hooks folder, so it is standalone.
# A line `=term` matches term as a whole word ([A-Za-z0-9_] are word characters); any other
# line matches as a substring. Both ignore case.
# Exit 0: clean, no repo, or no terms. Exit 1: hits (file:line or file name on
# stderr, never the term itself). Exit 2: usage.

case "${1:-}" in
  ""|--staged) cached=--cached ;;
  --all) cached= ;;
  *) echo "usage: check-private-terms.sh [--staged|--all]" >&2; exit 2 ;;
esac

root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
wiki=wiki
if [ -f "$root/.wikidir" ]; then
  wiki=$(tr -d '\000\015\357\273\277\376\377' < "$root/.wikidir" | sed -n '/[^[:space:]]/{p;q;}' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
fi
case "$wiki" in ''|.|..|*/*) exit 0 ;; esac

terms="$root/$wiki/.private-terms"
[ -f "$terms" ] || exit 0
patterns=$(mktemp) || exit 2
words=$(mktemp) || exit 2
tmp_hits=$(mktemp) || exit 2
trap 'rm -f "$patterns" "$words" "$tmp_hits"' EXIT
bom=$(printf '\357\273\277')
tr -d '\015' < "$terms" | sed "1s/^$bom//" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | grep -v -e '^#' -e '^$' > "$tmp_hits"
# An empty pattern line would match everything: neither file may hold one.
grep -v '^=' "$tmp_hits" > "$patterns"
sed -n 's/^=[[:space:]]*//p' "$tmp_hits" | grep -v '^$' > "$words"
[ -s "$patterns" ] || [ -s "$words" ] || exit 0
: > "$tmp_hits"
# search <file> <extra grep flag>: content hits of one pattern file, appended to $tmp_hits.
search() {
  [ -s "$1" ] || return 0
  # shellcheck disable=SC2086 # $cached and $2 are empty or one flag
  git grep $cached -I -i -F $2 -n -f "$1" -- . ":(exclude)$wiki/.private-terms" >> "$tmp_hits" 2>/dev/null || {
    gg_status=$?
    [ "$gg_status" = 1 ] || { echo "Codebase Wiki LLM: private-terms check failed (git grep error)." >&2; exit 2; }
  }
}

cd "$root" || exit 2
search "$patterns" ""
search "$words" -w
hits=$(cut -d: -f1-2 < "$tmp_hits" | sort -u)
# File names count too: the index holds the staged and tracked paths.
names=$(git ls-files -- . ":(exclude)$wiki/.private-terms")
path_hits=$( { [ ! -s "$patterns" ] || printf '%s\n' "$names" | grep -i -F -f "$patterns"
               [ ! -s "$words" ] || printf '%s\n' "$names" | grep -i -w -F -f "$words"; } | sort -u)
if [ -n "$hits" ] || [ -n "$path_hits" ]; then
  echo "Codebase Wiki LLM: private terms found (list in $wiki/.private-terms):" >&2
  [ -z "$hits" ] || printf '%s\n' "$hits" >&2
  [ -z "$path_hits" ] || printf '%s\n' "$path_hits" | sed 's/^/file name: /' >&2
  echo "Replace them with the generic wording recorded in SCHEMA.md; rename matching files." >&2
  exit 1
fi
exit 0
