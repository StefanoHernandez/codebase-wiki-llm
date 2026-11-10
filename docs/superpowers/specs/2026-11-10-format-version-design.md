# Versione dichiarata del formato, controlli di aggiornamento, indice dei proprietari, prossimi passi, registro rischi

Data: 2026-11-10 · Stato: bozza per revisione · Base: 0.11.0 (`d0cdfaa`) · Rilascio: 0.12.0

## Intento

Oggi una wiki non dice con quale versione del plugin è stata scritta, e il validator accetta
wiki parzialmente aggiornate senza dirlo. Esempio reale, la wiki Versal (adottata, layout
numerato): il validator dentro `docs/` trova solo le 31 pagine senza frontmatter, ma
- gli ADR hanno lo stato nel testo (`- **Status**: accepted`) e non `status:` nel frontmatter,
  né `## Approval`;
- la tabella Done ha le colonne vecchie senza `Status`, quindi una chiusura ⚫ non si può
  scrivere;
- lo SCHEMA non ha `## Page frontmatter` (arrivata con 0.10.0).

Chi legge la wiki con uno strumento (l'app desktop Codebase Wiki, altri agenti) non può fidarsi
della struttura e non può dire alla persona cosa fare.

Successo =
1. ogni wiki inizializzata o aggiornata dichiara la versione del formato;
2. il validator dice, in righe leggibili da uno strumento, cosa manca per l'ultima versione;
3. `/wiki-init --adopt` su una wiki già v2 porta a zero quelle righe senza cambiare il layout
   scelto dal progetto;
4. tre pratiche nate sulla wiki Versal diventano disponibili a tutte le wiki: tabella
   "un argomento, una pagina" nell'indice, "Prossimi passi" nel tracker, registro dei rischi
   con ID.

Si cambia solo la variante codebase (secondbrain non usa queste pagine). Nessuna rottura: una
wiki 0.11.0 resta strutturalmente valida (stesso codice d'uscita); riceve solo righe
`upgrade:` che dicono cosa aggiornare.

## Decisioni prese prima di questa spec

- Le wiki v1 (senza `## Core map`) non vanno lette dagli strumenti: si aggiornano con
  `/wiki-init --adopt`, che esiste già. Questa spec non aggiunge compatibilità all'indietro.
- La versione è dichiarata nello SCHEMA (Stefano, 2026-11-10).

## Cambi

### P0. Versione del formato nello SCHEMA

Chiave nuova nel frontmatter di `SCHEMA.md`:

```yaml
---
type: Schema
title: Wiki Schema
format_version: 0.12.0
...
---
```

- Valore: la versione del plugin (`canonical/codebase/VERSION`, copiata come costante `FORMAT_VERSION` nel validator, che si installa da solo; un test ne verifica l'uguaglianza) che ha scritto o aggiornato la
  **struttura** della wiki per l'ultima volta. Non cambia a ogni modifica di contenuto.
- La scrive `/wiki-init` (nuova wiki) e `/wiki-init --adopt` (alla fine dell'aggiornamento, solo
  se il validator non stampa più righe `upgrade:`). `/wiki-sync` non la cambia; se la trova più
  vecchia della propria versione lo dice nel report e propone `/wiki-init --adopt`.
- Scalare semplice `X.Y.Z`. Assente = wiki precedente alla 0.12.0.
- Una versione **più nuova** di quella del validator: riga `upgrade:` che chiede di aggiornare
  il plugin (non la wiki).

### P5. Righe `upgrade:` nel validator

Un terzo tipo di riga accanto a findings (stderr, codice 1) e `info:` (stdout, codice 0):

```
upgrade: <path>:<line>: <cosa manca per la versione corrente>
```

su stdout, **senza** cambiare il codice d'uscita. Una wiki è "al formato corrente" quando non
ci sono righe `upgrade:`. Righe prodotte in 0.12.0:

| Controllo | Riga |
| --- | --- |
| `format_version` assente | `SCHEMA.md:1: format_version missing; run /wiki-init --adopt <wiki-root> with plugin 0.12.0` |
| `format_version` < VERSION | `SCHEMA.md:<n>: format_version 0.11.0 is older than 0.12.0; run /wiki-init --adopt <wiki-root>` |
| `format_version` > VERSION | `SCHEMA.md:<n>: format_version 0.13.0 is newer than this plugin (0.12.0); update the plugin` |
| sezioni v2 mancanti nello SCHEMA (`## Project profile`, `## Conventions`, `## Evidence`, `## Confidentiality`, `## Budgets`, `## Log format`, `## Topics`, `## Page frontmatter`; titolo inglese o marker `<!-- wiki:<slug> -->` se tradotto) | una riga per sezione |
| file nella cartella `decisions` (`NNNN-*.md`) senza `status:` nel frontmatter | `<file>:1: decision status must be in frontmatter (status: proposed \| accepted \| rejected \| superseded by NNNN)` |
| file decisione senza `## Approval` (o marker `<!-- wiki:approval -->` nelle wiki tradotte) | `<file>:1: decision has no ## Approval section` |
| `status:` della decisione con un valore fuori formato | `<file>:<n>: decision status must be proposed, accepted, rejected or superseded by NNNN` |
| ruolo `decisions` che punta a un file unico (v1) | `SCHEMA.md:1: decisions must be a folder of NNNN-<slug>.md files` |
| SCHEMA senza `## Core map` (v1) | `SCHEMA.md:1: Core map missing (v1 wiki)` |
| tabella Done del tracker senza colonna `Status` (header legacy a 5 colonne) | `<tracker>:<n>: Done table has no Status column; ⚫ closures cannot be recorded` |

Note:
- Le righe Done legacy restano **valide** come oggi (completamento dimostrato). Il controllo
  riguarda solo l'header: senza `Status` non si può scrivere un ⚫.
- Pagine con `updated` e senza `generated`: resta `info` come oggi (non bloccante, `/wiki-sync`
  le aggiorna quando le tocca).
- Una wiki v1 (senza `## Core map`) produce già l'errore di configurazione attuale; in più la
  riga `format_version missing`.
- Il confronto delle versioni è numerico per componenti (`0.12.0 > 0.9.2`).

### P6. Aggiornamento con `/wiki-init --adopt` su una wiki già v2

`wiki-init.md` Step 4 (adopt mode) guadagna un passo "aggiornamento al formato corrente" che
risolve ogni riga `upgrade:` senza cambiare il layout scelto:

- **SCHEMA**: aggiunge le sezioni mancanti dal default schema, conserva le esistenti (regola già
  presente), poi scrive `format_version`.
- **Decisioni**: porta lo stato nel frontmatter.
  - Lo stato scritto nel testo (`- **Status**: accepted`, `Status: proposed`, …) diventa
    `status:`; la riga nel testo resta.
  - `## Approval`: se il testo registra già chi ha deciso, dove e quando (es.
    `**Decision makers**: … at the project meeting of 2026-10-20`), lo riporta come
    `accepted: <chi>, <dove>, <data>`; altrimenti scrive `Approval not recorded.` (riga già
    prevista dal template per decisioni precedenti al template). Mai inferire un'approvazione.
  - Stato non riconoscibile: lascia la decisione com'è e la elenca nel report per la persona.
- **Tracker**: aggiunge la colonna `Status` alla tabella Done; le righe legacy ricevono 🟢, che
  è il significato che il formato già attribuisce loro ("Legacy Done rows without Status remain
  valid for proven completion"). Nessun ⚫ inferito.
- Rilancia il validator: zero righe `upgrade:` → scrive `format_version`; altrimenti elenca le
  righe rimaste e non scrive la versione.
- Si comporta come oggi per spostamenti di file: nessuno senza conferma; se lo SCHEMA registra
  che gli spostamenti sono stati rifiutati, non li ripropone.
- `/wiki-init` su una cartella che ha già SCHEMA con `## Core map` ma è indietro di versione
  propone direttamente questo aggiornamento (oggi propone "skip / adopt / re-init").

### P1. Indice: "un argomento, una pagina"

Nuovo `references/index-template.md` (oggi l'indice non ha template, solo la regola "aggiorna
l'indice"):

```markdown
# <Project> wiki

<one paragraph: what this repo is>

## Index
<grouped links to every page, one line each, from its `description`>

## Where things stand
Status lives only in the [tracker](<tracker path>); what was done in the [log](<log path>).

## How this wiki is organised
<!-- wiki:owners -->

| Topic | Owner page |
| --- | --- |
| Activity status, next steps | [tracker](<tracker path>) |
| What was done, when | [log](<log path>) |
| Decisions | [decisions](<decisions path>) |
| Next task for an agent | [handoff](<handoff path>) |
```

- Regola nello schema (`## Page granularity`): ogni argomento ha **una** pagina proprietaria
  elencata in questa tabella; le altre pagine la linkano in una riga e non la ripetono.
- `/wiki-init` crea la tabella con le righe del core e una riga per argomento confermato;
  `/wiki-sync` e `/wiki-ingest` aggiungono la riga quando creano la pagina proprietaria di un
  argomento nuovo.
- Validator: se il marker `wiki:owners` c'è, la tabella deve avere le colonne `Topic | Owner
  page` e ogni riga un link che risolve (i link sono già controllati). Il marker è opzionale:
  nessuna riga `upgrade:` se manca.

### P2. Tracker: "Prossimi passi"

Sezione opzionale in cima al tracker, prima di `## Open`:

```markdown
## Next steps
<!-- wiki:next -->

**In one line:** <current state in one sentence, with date>

1. <next step> (T12)
2. <next step> (T14)
```

- Al massimo 5 punti, ognuno cita almeno un ID del tracker o una proposta; nessuno stato qui
  (lo stato resta nelle tabelle).
- Gli agenti la aggiornano con `/wiki-sync` quando cambiano i lavori aperti; l'ordine dei punti è
  una proposta, le priorità restano decisioni umane (regola già presente nel template).
- Validator: se il marker c'è, ogni `T<n>` citato deve esistere nel tracker. Opzionale: nessuna
  riga `upgrade:` se manca.

### P3. Registro dei rischi

Nuovo `references/risks-template.md` per il ruolo `risks` (oggi senza template):

```markdown
# Risks

Severity uses words, not status icons.

## Register
<!-- wiki:risk-register -->

| ID | Risk | Severity | Trigger | Mitigation | Owner | IDs |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | <what can go wrong> | high | <the assumption, and what would show it is failing> | <what reduces it> | <person or unknown> | T12 |

## Details
### R1 — <title>
<optional: context, evidence, history>
```

- `R<n>` stabili e mai riusati, come `T<n>`. Severità: `critical`, `high`, `medium`, `low`.
- Marker `wiki:risk-register`, distinto dal `wiki:risks` già usato nella handoff.
- La severità è un token fisso (come le icone di stato): `critical`, `high`, `medium`, `low`,
  anche nelle wiki in altre lingue.
- Validator: se il marker c'è, ID unici e nel formato `R<n>`, severità tra le quattro, `IDs`
  citati esistenti nel tracker. Opzionale per le wiki esistenti.
- Evidence in `default-schema.md` (riga Risk: "the stated assumption and what would trigger
  it") resta e corrisponde alla colonna `Trigger`.

### P4. `verified` su una riga

`maintainer.md` e `## Page frontmatter` dicono oggi "`{ by, at }` or a list of them" senza dire
la forma; il validator accetta solo valori che iniziano con `{` o `[` sulla riga della chiave e
rifiuta le liste indentate. Allineare la documentazione al validator:

- una voce: `verified: { by: human:<id>, at: <ISO 8601 Z>, commit: <sha> }`;
- più voci: `verified: [{ by: …, at: … }, { by: …, at: … }]` su una riga;
- le liste indentate non sono ammesse.

Nessun cambio di codice nel validator.

## Cosa non cambia

- Layout, Core map, Page types, Excluded paths, regole locali del log (ordine delle voci,
  divieto di hash): invariati. Gli strumenti devono leggere l'ordine del log dalle regole locali
  (`## Log format` dello SCHEMA o `## Rules` della pagina log), non presumerlo.
- Codici d'uscita del validator e findings esistenti.
- Secondbrain.

## Test

Fixture nuove in `scripts/test-wiki-validator.py` (eseguite sullo script canonico e sulle
quattro distribuzioni byte-identiche, come oggi):

1. SCHEMA senza `format_version` → riga `upgrade:`, codice 0.
2. `format_version` più vecchia, uguale, più nuova del VERSION → upgrade / niente / upgrade
   "update the plugin".
3. SCHEMA senza `## Page frontmatter` → una riga upgrade.
4. Decisione con stato nel testo e senza `status:` → upgrade; con `status:` ma senza
   `## Approval` → upgrade; completa → niente.
5. Tracker con Done legacy a 5 colonne → upgrade, righe ancora valide; con `Status` → niente.
6. `wiki:owners` con link rotto → finding; senza marker → niente.
7. `wiki:next` con `T99` inesistente → finding.
8. `wiki:risk-register` con ID duplicato, severità sconosciuta o `T<n>` inesistente → finding;
   il `wiki:risks` della handoff resta controllato come oggi.
9. Scenario di applicazione: copia della forma Versal (layout numerato, ADR con stato nel
   testo, Done legacy, SCHEMA senza Page frontmatter) → prima: righe upgrade attese; dopo i
   passi P6 applicati a mano sulla fixture: zero righe upgrade, codice 0, layout invariato.

Più: `scripts/check-generated.sh` e `test-generators.sh` per le distribuzioni rigenerate.

## Rilascio 0.12.0

- `canonical/codebase/VERSION` → `0.12.0`; template e workflow aggiornati; distribuzioni
  rigenerate con gli script esistenti.
- Release checklist con la stessa forma della 0.11.0, più: prova reale `/wiki-init --adopt` su
  una copia della wiki Versal, con l'output del validator prima e dopo.
- README: sezione "Changes in 0.12.0".

## Fuori scope (proposte successive)

Argomenti opzionali con template proposti da `/wiki-init` in base al progetto: requisiti con ID
e tracciabilità verso i risultati, roadmap a fasi con condizione d'uscita, registro risultati
(una pagina per sessione, dati grezzi esclusi con `sha256`), registro consegne, metodo di
verifica, runbook e artefatti locali. Spec separata dopo la 0.12.0.
