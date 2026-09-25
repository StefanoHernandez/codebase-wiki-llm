#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
FAIL_OUT="$TMP_DIR/failure.out"
FAIL_ERR="$TMP_DIR/failure.err"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$TMP_DIR/wiki/agent"

cat > "$TMP_DIR/wiki/agent/context.md" <<'EOF'
---
title: Agent Context
updated: 2026-07-01
sources:
  - README.md
confidence: high
---

# Agent Context

## Project Snapshot
Example project.

## Architecture
Example service.

## Core Commands
- Setup: `npm install`
- Test: `npm test`
- Lint: `npm run lint`
- Build: `npm run build`

## Read First
- `README.md`

## Risks
- Do not invent unsupported facts.
EOF

cat > "$TMP_DIR/wiki/agent/handoff.md" <<'EOF'
---
title: Agent Handoff
updated: 2026-07-01
sources:
  - README.md
confidence: high
---

# Agent Handoff

## Baton For Next Coding Agent

| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
| 1 | Validate handoff contract | `README.md` | Validator accepts required baton fields | `scripts/validate-agent-handoff.py wiki` | None |
EOF

"$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/wiki"

# Without an argument the validator uses ./wiki, or the folder named in ./.wikidir.
(cd "$TMP_DIR" && "$ROOT_DIR/scripts/validate-agent-handoff.py")

mkdir -p "$TMP_DIR/repo"
cp -R "$TMP_DIR/wiki" "$TMP_DIR/repo/.wiki"
printf '.wiki\n' > "$TMP_DIR/repo/.wikidir"
(cd "$TMP_DIR/repo" && "$ROOT_DIR/scripts/validate-agent-handoff.py")

# Pointers written by PowerShell: UTF-8 with BOM, and UTF-16LE.
printf '\357\273\277.wiki\r\n' > "$TMP_DIR/repo/.wikidir"
(cd "$TMP_DIR/repo" && "$ROOT_DIR/scripts/validate-agent-handoff.py")
printf '\377\376.\000w\000i\000k\000i\000\r\000\n\000' > "$TMP_DIR/repo/.wikidir"
(cd "$TMP_DIR/repo" && "$ROOT_DIR/scripts/validate-agent-handoff.py")

cat > "$TMP_DIR/wiki/agent/handoff.md" <<'EOF'
---
title: Agent Handoff
updated: 2026-07-01
sources:
  - README.md
confidence: high
---

# Agent Handoff

## Baton For Next Coding Agent

| Order | Task | Start files | Done when | Verification command | Notes / blockers |
| --- | --- | --- | --- | --- | --- |
| 1 | Validate handoff contract | `README.md` | Validator accepts required baton fields |  | None |
EOF

if "$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/wiki" >"$FAIL_OUT" 2>"$FAIL_ERR"; then
  echo "expected validator failure for missing verification command" >&2
  exit 1
fi

echo "agent handoff validator tests passed"
