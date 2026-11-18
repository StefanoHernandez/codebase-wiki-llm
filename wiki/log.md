---
title: Log
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - wiki/SCHEMA.md
  - CHANGELOG.md
source_commit: 94f5dc0
confidence: high
---
# Log

## 2026-11-18 · Plugin wiki created; field-test references removed; 0.16.0 changes · agent
- What: created this wiki with the plugin's own `/wiki-init` (new wiki, Sensitive data yes); replaced field-test project references with generic wording in current files; added `=term` whole-word private terms, `\uXXXX` decoding in the reminder hook, and `references/legacy-adoption.md`.
- Evidence: `bash scripts/run-tests.sh` → exit 0 @94f5dc0; `sh canonical/codebase/scripts/check-private-terms.sh --all` → exit 0 @94f5dc0
- IDs: T1
