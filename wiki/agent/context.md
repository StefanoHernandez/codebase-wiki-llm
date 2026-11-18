---
type: AgentNote
title: Agent Context
description: What a new agent must know before changing the plugin.
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - canonical/codebase
  - scripts/run-tests.sh
  - docs/development.md
  - wiki/index.md
  - wiki/SCHEMA.md
source_commit: 94f5dc0
confidence: high
---
# Agent Context

## Goals And Non-Goals
<!-- wiki:goals -->
- Goal: one set of instructions that keeps a repository wiki current on Codex, Claude Code and Antigravity.
- Goal: structure checked by a deterministic validator, not by the model's judgement.
- Non-goal: a hosted service or a search index (the desktop app is a separate repository).
- Non-goal: claims about a project's truth; the wiki records evidence, the code is the authority.

## Non-Negotiable Rules
<!-- wiki:rules -->
1. Edit only `canonical/` and `scripts/`; regenerate with `python3 scripts/generate-host-packages.py` (packages are generated).
2. Never write a term from `wiki/.private-terms` anywhere else; the pre-commit hook blocks it.
3. `verified`, opening tasks, ⚫ closures and accepting decisions are reserved to people.
4. Push, tags and merges to `main` only on Stefano's explicit go-ahead.

## Frequent Commands
<!-- wiki:commands -->
| Purpose | Command | Verified |
| --- | --- | --- |
| All tests | `bash scripts/run-tests.sh` | 2026-11-18 @94f5dc0 |
| Regenerate packages | `python3 scripts/generate-host-packages.py` | 2026-11-18 @94f5dc0 |
| Validate a wiki | `python3 canonical/codebase/scripts/validate-wiki.py <wiki-root>` | 2026-11-18 @94f5dc0 |
| Install dev hook | `bash scripts/install-dev-hooks.sh` | 2026-11-18 @94f5dc0 |

## Verified Facts
<!-- wiki:verified-facts -->
Do not re-derive these. Re-check a fact only when its evidence changed or it is
marked `⚠️ TO RE-VERIFY`.

| Fact | Value | Evidence | Verified |
| --- | --- | --- | --- |
| Plugin release | 0.16.0 | `canonical/codebase/VERSION` | 2026-11-18 @94f5dc0 |
| Wiki format | 0.12.0 | `FORMAT_VERSION` in `canonical/codebase/scripts/validate-wiki.py` | 2026-11-18 @94f5dc0 |
| Python for the validator | 3.10+ | `validate-wiki.py` refuses older versions | 2026-11-18 @94f5dc0 |
| Default budgets | page 30 KB, core read 100 KB, log 30 KB | `canonical/codebase/default-schema.md` `## Budgets` | 2026-11-18 @94f5dc0 |

**Errors already corrected, do not reintroduce:** editing files under `plugins/` or `skills/` → they are regenerated from `canonical/`.

## Read First
<!-- wiki:read-first -->
1. [index](../index.md)
2. [tracker](../project/work-tracker.md)
3. [handoff](handoff.md) (baton row 1 is the first task)
4. [architecture](../architecture.md)
5. [development guide](../../docs/development.md)
