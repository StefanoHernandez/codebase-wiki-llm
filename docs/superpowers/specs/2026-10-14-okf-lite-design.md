# OKF-lite: frontmatter v2 per il codebase wiki

Data: 2026-10-14 · Stato: bozza per revisione · Fonte: `SPEC.md` (Open Knowledge Format v0.2, Google)

## Intento

Rendere le pagine del wiki leggibili come concetti OKF e rispondere a due domande che oggi
non hanno risposta: *chi ha scritto questa pagina* e *chi l'ha confermata*. Solo aggiunte,
nessuna rottura per i wiki esistenti. Successo = un wiki generato dal plugin ha ogni pagina
con `type`, `description`, `status`, `generated`, e `wiki-lint` riporta il livello di fiducia.

Assunzioni (da correggere se sbagliate): il decadimento per commit (`source_commit`,
`confidence`) resta il meccanismo di freschezza; l'obiettivo è compatibilità OKF, non
conformità stretta.

## Cambio di schema

```yaml
---
type: Module                    # NUOVO, obbligatorio. Stringa libera.
title: ...                      # invariato
description: Una riga.          # NUOVO, obbligatorio. Alimenta index.md.
status: stable                  # NUOVO. draft | stable | deprecated. Default stable.
generated: { by: antigravity/gemini-3.5, at: 2026-10-14T00:58:00Z }   # NUOVO, sostituisce `updated`
verified: { by: human:stefano, at: 2026-10-14T09:00:00Z }             # NUOVO, opzionale
sources: [...]                  # invariato (elenco di file)
source_commit: abc123           # invariato
confidence: high                # invariato
---
```

## Regole

1. **`type`**: valore di default per cartella, sovrascrivibile. `modules/` → `Module`,
   `engineering/` → `Engineering`, `project/` → `Project`, `project-docs/` → `ProjectDoc`,
   `agent/` → `AgentNote`, `overview*.md` → `Overview`. Tabella nello schema di default.
2. **Attore** (`generated.by`, `verified.by`): `human:<id>`, oppure `<host>/<modello>` con
   host `claude-code`, `codex`, `antigravity`. Modello ignoto → `<host>/unknown`.
3. **`verified`**: gli agenti NON lo scrivono mai da soli. Solo quando l'utente conferma
   esplicitamente una pagina (attore `human:`), o un processo dichiarato (`process:<id>`).
   `verified` può essere una mappa singola o una lista; chi legge tratta la mappa come lista.
4. **Fiducia derivata** (come OKF §5.3): nessun `verified` → *unverified*; solo attori non
   umani → *machine-confirmed*; almeno un `human:` → *human-reviewed*. Non si salva, si calcola.
5. **`status: deprecated`**: sostituisce la nota di supersessione come marcatore. La pagina
   resta, nessuna cancellazione silenziosa (regola esistente invariata).
6. **`index.md` e `log.md`** non sono concetti: niente `type`. Il frontmatter di `index.md`
   resta com'è. Il wiki è "compatibile OKF", non "conforme" alla lettera di §8.

## Compatibilità e migrazione

- Una pagina senza i campi nuovi resta valida. `wiki-lint` la segnala come *legacy* (livello
  info), mai come errore. `updated` viene letto come ripiego se manca `generated`.
- `wiki-sync` aggiorna solo le pagine che già tocca: lì aggiunge `type`, `description`,
  `generated` e toglie `updated`. Nessuna migrazione di massa.
- `wiki-init` e `wiki-ingest` scrivono sempre lo schema nuovo.

## Dove si cambia

| File | Cambio |
|---|---|
| `canonical/codebase/maintainer.md` | blocco frontmatter, regole 1–5, truth hierarchy invariata |
| `canonical/codebase/default-schema.md` | tabella `type` per cartella, convenzione attore |
| `canonical/codebase/workflows/wiki-init.md`, `wiki-ingest.md` | scrivere schema nuovo; `description` per `index.md` |
| `canonical/codebase/workflows/wiki-sync.md` | aggiornare `generated`, mai `verified` |
| `canonical/codebase/workflows/wiki-lint.md` | controlli sotto, report fiducia |
| `canonical/codebase/references/*-template.md` | frontmatter nuovo |
| `scripts/validate-agent-handoff.py`, `scripts/test-agent-handoff-validator.sh` | `updated` obbligatorio → `updated` oppure `generated` (altrimenti `agent/handoff.md` scritto col formato nuovo fallisce la validazione) |
| `scripts/generate-codebase-packages.py`, `.claude-plugin/marketplace.json` | solo versione plugin (minor, 0.8.0 → 0.9.0) |

I pacchetti sotto `plugins/` e `skills/` si rigenerano, non si editano.

## Controlli aggiunti a `wiki-lint`

- `type` o `description` mancanti → warning (legacy → info).
- `status` fuori da `draft|stable|deprecated` → errore.
- `generated.by` non nel formato attore → warning.
- pagina `deprecated` linkata da pagine `stable` → warning.
- riepilogo fiducia: conteggio unverified / machine-confirmed / human-reviewed.

## Fuori scopo (deciso, non rimandato per caso)

`stale_after`, `sources[]` come oggetti con note a piè di pagina, Attested Computation,
indici per sottocartella, link assoluti da radice bundle, script validatore dedicato (il lint
è un workflow, non codice).

## Verifica

1. `scripts/generate-codebase-packages.py` poi `scripts/check-generated.sh` → "up to date".
2. Dogfooding: `/wiki-lint` sul `wiki/` di questo repo (tutte pagine legacy) → solo info,
   zero errori; poi `/wiki-sync` dopo una modifica e controllo che la pagina toccata abbia
   i campi nuovi.
