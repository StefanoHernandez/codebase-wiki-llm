#!/usr/bin/env bash
# Install this repository's pre-commit hook: block commits with stale generated files.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
hook="$(git -C "$ROOT_DIR" rev-parse --absolute-git-dir)/hooks/pre-commit"
printf '#!/bin/sh\nexec bash "%s/scripts/check-generated.sh"\n' "$ROOT_DIR" > "$hook"
chmod +x "$hook"
echo "installed $hook"
