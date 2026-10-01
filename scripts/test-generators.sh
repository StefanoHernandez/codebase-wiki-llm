#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
failures=0
fail() { echo "FAIL $1" >&2; failures=$((failures + 1)); }

# Stale generated files disappear on regeneration.
stale=(
  "plugins/claude-codebase-wiki-llm/commands/stale-test.md"
  "plugins/antigravity-codebase-wiki-llm/skills/stale-test/SKILL.md"
  "plugins/secondbrain-wiki-llm/skills/stale-test/SKILL.md"
  "skills/codebase-stale-test/SKILL.md"
)
for f in "${stale[@]}"; do mkdir -p "$(dirname "$f")"; echo stale > "$f"; done
python3 scripts/generate-host-packages.py
for f in "${stale[@]}"; do
  [ ! -e "$f" ] || fail "stale file survived: $f"
  rmdir "$(dirname "$f")" 2>/dev/null || true
done

# Non-generated files survive.
for f in plugins/codebase-wiki-llm/assets/icon.svg plugins/codebase-wiki-llm/README.md plugins/secondbrain-wiki-llm/assets/icon.svg; do
  [ -f "$f" ] || fail "non-generated file removed: $f"
done

# Every manifest carries the VERSION file value.
cv="$(tr -d '[:space:]' < canonical/codebase/VERSION)"
sv="$(tr -d '[:space:]' < canonical/secondbrain/VERSION)"
for f in plugins/codebase-wiki-llm/.codex-plugin/plugin.json plugins/claude-codebase-wiki-llm/plugin.json plugins/antigravity-codebase-wiki-llm/plugin.json; do
  grep -q "\"version\": \"$cv\"" "$f" || fail "$f does not carry codebase version $cv"
done
for f in plugins/secondbrain-wiki-llm/.codex-plugin/plugin.json plugins/claude-secondbrain-wiki-llm/plugin.json plugins/antigravity-secondbrain-wiki-llm/plugin.json; do
  grep -q "\"version\": \"$sv\"" "$f" || fail "$f does not carry secondbrain version $sv"
done
python3 - "$cv" "$sv" <<'EOF' || fail "marketplace versions"
import json, sys
m = json.load(open(".claude-plugin/marketplace.json"))
v = {p["name"]: p["version"] for p in m["plugins"]}
assert v == {"codebase-wiki-llm": sys.argv[1], "secondbrain-wiki-llm": sys.argv[2]}, v
EOF
if grep -rq "@VERSION@" plugins .claude-plugin; then fail "unreplaced @VERSION@ token"; fi

for package in \
  plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer \
  plugins/claude-codebase-wiki-llm/skills/wiki-maintainer \
  plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer \
  skills/codebase-wiki-llm; do
  cmp -s canonical/codebase/scripts/validate-wiki.py "$package/scripts/validate-wiki.py" || fail "validator differs or missing: $package"
done

[ "$failures" -eq 0 ] || { echo "$failures generator test(s) failed" >&2; exit 1; }
echo "generator tests passed"
