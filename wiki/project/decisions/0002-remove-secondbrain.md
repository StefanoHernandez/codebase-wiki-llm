---
type: Decision
title: 0002 - Remove SecondBrain from this repository
description: SecondBrain Wiki LLM is no longer shipped from this repository.
status: accepted
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-18T12:07:28Z }
sources:
  - CHANGELOG.md
source_commit: 94f5dc0
confidence: high
---
# 0002 - Remove SecondBrain from this repository

## Context
The repository shipped two plugins, Codebase Wiki LLM and SecondBrain Wiki LLM.

## Decision
SecondBrain packages, skills and marketplace entries are removed in 0.15.0; its last version stays in tag `v0.14.1` (SecondBrain 0.2.1).

## Alternatives rejected
- Reasons not recorded.

## Consequences
About 1,800 source lines less to maintain; users of SecondBrain uninstall it (CHANGELOG 0.15.0).

## Approval
<!-- wiki:approval -->
accepted: Stefano, release v0.15.0 and CHANGELOG 0.15.0, 2026-11-13
