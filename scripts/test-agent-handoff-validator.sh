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

## Goals And Non-Goals
- Goal: example service. Non-goal: a UI.

## Non-Negotiable Rules
- Do not invent unsupported facts.

## Frequent Commands
- Test: `npm test` (verified 2026-07-01)

## Verified Facts
| Fact | Value | Evidence | Verified |
| --- | --- | --- | --- |
| Node | 20 | `node --version` | 2026-07-01 |

## Read First
- `README.md`
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

# Core map relocates context and handoff (adopted wiki).
mkdir -p "$TMP_DIR/adopted/docs/00-project"
cp "$TMP_DIR/repo/.wiki/agent/context.md" "$TMP_DIR/adopted/docs/00-project/context.md"
cp "$TMP_DIR/repo/.wiki/agent/handoff.md" "$TMP_DIR/adopted/docs/00-project/handoff.md"
printf '## Core map\n\n| Role | Path |\n| --- | --- |\n| context | `00-project/context.md` |\n| handoff | 00-project/handoff.md |\n' > "$TMP_DIR/adopted/docs/SCHEMA.md"
"$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/adopted/docs"

# v1 context headings are rejected.
sed -i 's/## Verified Facts/## Old Facts/' "$TMP_DIR/adopted/docs/00-project/context.md"
if "$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/adopted/docs" >"$FAIL_OUT" 2>"$FAIL_ERR"; then
  echo "expected validator failure for missing Verified Facts" >&2
  exit 1
fi

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

# Pages in another language: sections found by stable markers.
mkdir -p "$TMP_DIR/it/agent"
cat > "$TMP_DIR/it/agent/context.md" <<'EOF'
---
title: Contesto agente
updated: 2026-09-30
sources:
  - README.md
confidence: high
---

# Contesto agente

## Obiettivi e non-obiettivi
<!-- wiki:goals -->
- Obiettivo: servizio di esempio.

## Regole non negoziabili
<!-- wiki:rules -->
- Non inventare.

## Comandi frequenti
<!-- wiki:commands -->
- Test: `npm test`

## Fatti verificati
<!-- wiki:verified-facts -->
| Fatto | Valore | Evidenza | Verificato |
| --- | --- | --- | --- |
| Node | 20 | `node --version` | 2026-09-30 @abc1234 |

## Da leggere prima
<!-- wiki:read-first -->
- `README.md`
EOF
write_it_handoff() { # <body after the baton heading>
  {
    printf '%s\n' '---' 'title: Passaggio di consegne' 'updated: 2026-09-30' 'sources:' '  - README.md' \
      'confidence: high' '---' '' '# Passaggio di consegne' '' '## Testimone per il prossimo agente'
    printf '%s\n' "$1"
  } > "$TMP_DIR/it/agent/handoff.md"
}
write_it_handoff '<!-- wiki:baton -->

| Ordine | Attività | File iniziali | Fatto quando | Comando di verifica | Note / blocchi |
| --- | --- | --- | --- | --- | --- |
| 1 | T3 - validare il contratto | `README.md` | vedi T3 | `scripts/validate-agent-handoff.py wiki` | Nessuna |'
"$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/it"

write_it_handoff '<!-- wiki:baton -->

No open work.'
"$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/it"

write_it_handoff '<!-- wiki:baton -->

| Ordine | Attività | File iniziali | Fatto quando | Comando di verifica |
| --- | --- | --- | --- | --- |
| 1 | T3 | `README.md` | vedi T3 | `true` |'
if "$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/it" >"$FAIL_OUT" 2>"$FAIL_ERR"; then
  echo "expected validator failure for a five-column baton found by marker" >&2
  exit 1
fi

write_it_handoff '
No open work.'
if "$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/it" >"$FAIL_OUT" 2>"$FAIL_ERR"; then
  echo "expected validator failure for a translated baton heading without its marker" >&2
  exit 1
fi

write_it_handoff '<!-- wiki:baton -->

No open work.'
sed -i '/<!-- wiki:read-first -->/d' "$TMP_DIR/it/agent/context.md"
if "$ROOT_DIR/scripts/validate-agent-handoff.py" "$TMP_DIR/it" >"$FAIL_OUT" 2>"$FAIL_ERR"; then
  echo "expected validator failure for a translated context section without its marker" >&2
  exit 1
fi

echo "agent handoff validator tests passed"
