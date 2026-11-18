---
title: Log
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:18:50Z }
sources:
  - wiki/SCHEMA.md
  - CHANGELOG.md
source_commit: 22e3c85
confidence: high
---
# Log

## 2026-11-18 · Plugin wiki created; field-test references removed; 0.16.0 changes · agent
- What: created this wiki with the plugin's own `/wiki-init` (new wiki, Sensitive data yes); replaced field-test project references with generic wording in current files; added `=term` whole-word private terms, `\uXXXX` decoding in the reminder hook, and `references/legacy-adoption.md`.
- Evidence: `bash scripts/run-tests.sh` → exit 0 @94f5dc0; `sh canonical/codebase/scripts/check-private-terms.sh --all` → exit 0 @94f5dc0
- IDs: T1

## 2026-11-18 · 0.16.0 whole-branch review fixes · agent
- What: independent review found no critical issue; recovery rules for content older than an adoption moved back to `/wiki-lint` (they apply to adopted wikis already at the current format, where the legacy trigger does not fire); decision 0002 lost an unsupported line count; CHANGELOG corrected. Stefano asked to bring 0.16.0 to `main` if CI passes.
- Evidence: `bash scripts/run-tests.sh` → exit 0 @22e3c85; `python3 canonical/codebase/scripts/validate-wiki.py wiki` → passed @22e3c85
- IDs: T1
