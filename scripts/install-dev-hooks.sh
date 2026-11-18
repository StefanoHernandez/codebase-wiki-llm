#!/usr/bin/env bash
# Install this repository's pre-commit hook: block commits with stale generated files and,
# when wiki/.private-terms exists in this clone, commits with private terms.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
hook="$(git -C "$ROOT_DIR" rev-parse --absolute-git-dir)/hooks/pre-commit"
cat > "$hook" <<EOF
#!/bin/sh
bash "$ROOT_DIR/scripts/check-generated.sh" || exit 1
[ ! -f "$ROOT_DIR/wiki/.private-terms" ] || sh "$ROOT_DIR/canonical/codebase/scripts/check-private-terms.sh" || exit 1
EOF
chmod +x "$hook"
echo "installed $hook"
