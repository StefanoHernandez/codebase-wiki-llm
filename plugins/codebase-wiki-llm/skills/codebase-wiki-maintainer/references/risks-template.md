<!-- Generated from codebase/references/risks-template.md. Do not edit directly. -->

# Risks Template

Use this template for the `risks` page (Core map). It is the register of what
could go wrong, the assumption behind each risk and what would show it is
failing.

```markdown
---
type: Project
title: Risks
description: <one line>
generated: { by: <host>/<model>, at: <ISO 8601 UTC> }
sources:
  - <wiki-root>/<Core map tracker path>
  - <source-path>
source_commit: <short-sha-or-unknown>
confidence: high | medium | low
---

# Risks

Severity uses words, not status icons.

## Register
<!-- wiki:risk-register -->

| ID | Risk | Severity | Trigger | Mitigation | Owner | IDs |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | <what can go wrong> | high | <the stated assumption, and what would show it is failing> | <what reduces it> | <person or `unknown`> | T1 |

## Details

### R1 — <short title>
<optional: context, evidence, history of the risk>
```

Rules:

- IDs `R1`, `R2`, … are stable and never reused, like tracker IDs. A risk that
  no longer applies stays in the register with its mitigation or a line saying
  why it is closed.
- Severity is a fixed token, also in wikis written in another language:
  `critical`, `high`, `medium`, `low`.
- `Trigger` is the evidence a risk needs (SCHEMA `## Evidence`): the stated
  assumption and what would trigger it.
- `IDs` cites the tracker activities that mitigate or depend on the risk; the
  validator checks that they exist. Status stays in the tracker.
- Owners and severity are human decisions; agents propose them and flag new
  risks, they do not close them.
- `## Details` is optional; one subsection per risk that needs more than a row.
- Keep the `<!-- wiki:risk-register -->` marker on the line under the heading
  when the heading is translated. It is distinct from the handoff's
  `<!-- wiki:risks -->`.
