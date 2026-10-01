#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT_DIR/scripts/test-wiki-validator.py"

# Install each shipped copy in isolation; Python -I and fixture cwd outside this
# checkout demonstrate that development scripts/modules are not runtime inputs.
TEST_DIR="$(mktemp -d)"
trap 'rm -rf "$TEST_DIR"' EXIT
for package in \
  plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer \
  plugins/claude-codebase-wiki-llm/skills/wiki-maintainer \
  plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer \
  skills/codebase-wiki-llm; do
  script="$ROOT_DIR/$package/scripts/validate-wiki.py"
  cmp "$ROOT_DIR/canonical/codebase/scripts/validate-wiki.py" "$script"
  cp "$script" "$TEST_DIR/validate-wiki.py"
  python3 "$ROOT_DIR/scripts/test-wiki-validator.py" "$TEST_DIR/validate-wiki.py" > "$TEST_DIR/result"
  echo "standalone fixtures and byte equality passed: $package"
done
