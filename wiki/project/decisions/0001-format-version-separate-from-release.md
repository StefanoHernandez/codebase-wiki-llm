---
type: Decision
title: 0001 - Wiki format has its own version
description: The wiki format is versioned apart from the plugin release.
status: accepted
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - CHANGELOG.md
  - docs/superpowers/specs/2026-11-10-format-version-design.md
source_commit: 94f5dc0
confidence: high
---
# 0001 - Wiki format has its own version

## Context
A wiki did not say which structure it followed, and the validator accepted partly upgraded wikis silently; tools such as the desktop app could not trust the structure ([spec](../../../docs/superpowers/specs/2026-11-10-format-version-design.md)).

## Decision
SCHEMA declares `format_version`; the validator carries `VERSION` (release) and `FORMAT_VERSION` (format) and prints `upgrade:` lines when a wiki is older. A release raises the format only when it adds an `upgrade:` check or changes a structure tools read.

## Alternatives rejected
- Reasons not recorded.

## Consequences
Several releases share format 0.12.0; `/wiki-init --adopt` raises `format_version` only when no other `upgrade:` line remains.

## Approval
<!-- wiki:approval -->
accepted: Stefano, release v0.12.0 and CHANGELOG 0.12.0/0.13.0, 2026-11-10
