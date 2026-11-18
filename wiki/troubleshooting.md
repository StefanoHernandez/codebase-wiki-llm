---
type: Engineering
title: Troubleshooting
description: Known failures when developing the plugin and their fixes.
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - scripts/check-generated.sh
  - scripts/install-dev-hooks.sh
source_commit: 94f5dc0
confidence: high
---
# Troubleshooting

## Commit refused: generated files out of date or not staged
- **Symptom:** the pre-commit prints `generated files were out of date` or `generated files are not staged`.
- **Cause:** a canonical change without regenerated packages, or regenerated files not added.
- **Fix:** `python3 scripts/generate-host-packages.py`, then `git add plugins skills .claude-plugin .agents`.

## Commit refused: private terms found
- **Symptom:** the pre-commit prints `private terms found` with `file:line` (never the term).
- **Cause:** a line of `wiki/.private-terms` appears in a staged file or file name.
- **Fix:** replace it with the generic wording recorded in [SCHEMA](SCHEMA.md) `## Confidentiality`.
