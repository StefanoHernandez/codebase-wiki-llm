---
type: Project
title: Risks
description: What can break a release or a user's wiki.
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - wiki/project/work-tracker.md
  - scripts/check-generated.sh
  - canonical/codebase/scripts/check-private-terms.sh
source_commit: 94f5dc0
confidence: high
---
# Risks

Severity uses words, not status icons.

## Register
<!-- wiki:risk-register -->

| ID | Risk | Severity | Trigger | Mitigation | Owner | IDs |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | A hand edit under `plugins/` or `skills/` is lost or ships unreviewed | medium | assumed: everyone edits `canonical/`; a diff in generated files without a canonical diff shows it failing | `scripts/check-generated.sh` in the pre-commit hook and in `run-tests.sh` | Stefano | — |
| R2 | A private term reaches a public commit from a clone without `wiki/.private-terms` | medium | assumed: each collaborator creates the local file; a clone where `install-dev-hooks.sh` reports no terms check shows it failing | per-clone terms file and chained pre-commit hook | Stefano | T1 |
| R3 | Smaller models skip secondary clauses in long workflow prompts | medium | assumed: legacy rules out of the common path are enough; wrong `/wiki-sync` results on current-format wikis show it failing | legacy rules read only when needed ([legacy file](../../canonical/codebase/references/legacy-adoption.md)) | Stefano | T1 |

## Details

### R2 — private terms are per clone
The terms file is git-ignored by design, so the protection exists only where it
was created ([decision 0005](decisions/0005-public-wiki-and-private-terms.md)).
