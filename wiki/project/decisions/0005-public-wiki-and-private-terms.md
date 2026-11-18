---
type: Decision
title: 0005 - Public plugin wiki and whole-word private terms
description: This repository keeps a public wiki; private terms are blocked per clone, a `=term` line matching a whole word.
status: accepted
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - canonical/codebase/scripts/check-private-terms.sh
  - .gitignore
  - scripts/install-dev-hooks.sh
source_commit: 94f5dc0
confidence: high
---
# 0005 - Public plugin wiki and whole-word private terms

## Context
A review proposed a wiki inside the plugin repository as a showcase and a continuous field test. The public repositories mentioned the project used for field tests and a local path; one of those names is also part of ordinary words used in code.

## Decision
The wiki is public. Field-test references are replaced with generic wording in current files only, without rewriting history. `wiki/.private-terms` is git-ignored and the pre-commit hook blocks its terms; a line `=term` matches a whole word, other lines a substring.

## Alternatives rejected
- Rewriting history on both repositories: irreversible, breaks clones and moves tags.
- Whole-word matching for every term: weaker for existing users (a term would no longer match inside longer names).
- Only longer, specific terms: the short name would not be blocked.

## Consequences
Old commits and tags keep the references. Protection exists only in clones that create the terms file.

## Approval
<!-- wiki:approval -->
accepted: Stefano, conversation, 2026-11-18
