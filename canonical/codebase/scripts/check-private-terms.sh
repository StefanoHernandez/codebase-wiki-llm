#!/bin/sh
# Block content that contains a term listed in <wiki-root>/.private-terms.
#   (no argument) / --staged  search the git index (git pre-commit hook)
#   --all                     search tracked files in the working tree (/wiki-lint)
# /wiki-init copies this file to .git/hooks/pre-commit, so it is standalone.
# Exit 0: clean, no repo, or no terms. Exit 1: hits (file:line on stderr,
# never the term itself). Exit 2: usage.

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
tmp_hits=$(mktemp) || exit 2
trap 'rm -f "$patterns" "$tmp_hits"' EXIT
bom=$(printf '\357\273\277')
tr -d '\015' < "$terms" | sed "1s/^$bom//" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | grep -v -e '^#' -e '^$' > "$patterns"
[ -s "$patterns" ] || exit 0

# shellcheck disable=SC2086 # $cached is empty or one flag
cd "$root" && git grep $cached -I -i -F -n -f "$patterns" -- . ":(exclude)$wiki/.private-terms" > "$tmp_hits" 2>/dev/null || {
  gg_status=$?
  [ "$gg_status" = 1 ] || { echo "Codebase Wiki LLM: private-terms check failed (git grep error)." >&2; exit 2; }
}
hits=$(cut -d: -f1-2 < "$tmp_hits")
if [ -n "$hits" ]; then
  echo "Codebase Wiki LLM: private terms found (list in $wiki/.private-terms):" >&2
  printf '%s\n' "$hits" >&2
  echo "Replace them with the generic wording recorded in SCHEMA.md." >&2
  exit 1
fi
exit 0
