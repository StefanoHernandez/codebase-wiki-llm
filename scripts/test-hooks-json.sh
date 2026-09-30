#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
python3 - <<'EOF'
import json, pathlib, sys
errors = []
def load(p):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception as e:
        errors.append(f"{p}: {e}")
        return {}
claude = load("plugins/claude-codebase-wiki-llm/hooks/hooks.json")
codex = load("plugins/codebase-wiki-llm/hooks/hooks.json")
if claude != codex:
    errors.append("Claude and Codex hook files differ")
cmds = [h["command"] for ev in claude.get("hooks", {}).values() for g in ev for h in g["hooks"]]
for want in ("resolve-wiki-root.sh", "remind-wiki-sync.sh\" --host claude"):
    if not any(want in c for c in cmds):
        errors.append(f"shared hooks missing {want}")
for ev in ("SessionStart", "UserPromptSubmit"):
    hs = [h for g in claude.get("hooks", {}).get(ev, []) for h in g["hooks"]]
    if not hs or any(h.get("timeout") != 10 for h in hs):
        errors.append(f"shared {ev} hook needs timeout 10")
if load("plugins/codebase-wiki-llm/.codex-plugin/plugin.json").get("hooks") != "./hooks/hooks.json":
    errors.append("Codex manifest does not point at hooks/hooks.json")
agy = load("plugins/antigravity-codebase-wiki-llm/hooks.json")
if "Stop" in claude.get("hooks", {}):
    errors.append("shared hooks must not block at Stop")
named = agy.get("codebase-wiki-sync-reminder", {})
pre = named.get("PreInvocation", [])
if not pre or "--host antigravity" not in pre[0].get("command", "") or pre[0].get("timeout") != 10:
    errors.append("Antigravity PreInvocation hook missing")
if "Stop" in named:
    errors.append("Antigravity hook must not block at Stop")
for p in [
    "plugins/claude-codebase-wiki-llm/scripts/remind-wiki-sync.sh",
    "plugins/codebase-wiki-llm/scripts/resolve-wiki-root.sh",
    "plugins/codebase-wiki-llm/scripts/remind-wiki-sync.sh",
    "plugins/antigravity-codebase-wiki-llm/scripts/resolve-wiki-root.sh",
    "plugins/antigravity-codebase-wiki-llm/scripts/remind-wiki-sync.sh",
    "plugins/codebase-wiki-llm/skills/codebase-wiki-maintainer/scripts/check-private-terms.sh",
    "plugins/claude-codebase-wiki-llm/skills/wiki-maintainer/scripts/check-private-terms.sh",
    "plugins/antigravity-codebase-wiki-llm/skills/wiki-maintainer/scripts/check-private-terms.sh",
    "skills/codebase-wiki-llm/scripts/check-private-terms.sh",
]:
    if not pathlib.Path(p).is_file():
        errors.append(f"missing {p}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("hook wiring tests passed")
EOF
