# Feedback dal campo su 0.10.0 (okf-lite): esclusioni, tipi per cartella, freschezza di `verified`

Data: 2026-10-27 · Stato: bozza per revisione · Base: 0.10.0 (`a04ee96`) · Riferimento:
OKF v0.2, `GoogleCloudPlatform/open-knowledge-format` a `ad30107`

## Intento

Applicare il feedback di una prova reale della 0.10.0 su un wiki adottato (radice `docs/`, 67
pagine, cartelle numerate, Core map con log in `00-project/project-log.md`). Il wiki deve poter
descrivere la propria struttura (quali file non sono pagine, che `type` hanno le sue cartelle)
e il lint deve dire quando una conferma umana non copre più le fonti attuali. Successo =
sullo stesso wiki il validator non segnala più i report generati, sync scrive il `type`
giusto per le cartelle numerate, e il lint mostra le conferme superate.

Solo aggiunte: un wiki 0.10.0 resta valido senza modifiche. Si cambia solo la variante
codebase (secondbrain non usa i campi okf-lite). Rilascio 0.11.0.

## Vincoli da OKF v0.2 (upstream)

- Ogni timestamp è un datetime ISO 8601 con offset esplicito; un valore solo-data non è
  conforme e i consumer lo ignorano (commit upstream `3dc3029`). Quindi `generated.at` e
  `verified.at` restano datetime.
- I livelli di fiducia si ricavano solo da `verified` (§5.3, §11) e `verified` è indipendente
  dai cambi di contenuto (§5.2). Quindi la freschezza di una conferma è un segnale separato,
  non un declassamento del livello.
- `type` è libero e scelto dal produttore (§4.1): una mappa cartella → tipo è compatibile.
- Ogni `.md` non riservato deve avere frontmatter con `type` (§11.1): un'esclusione rilassa
  solo il nostro validator, non rende conforme il bundle.
- Chiavi in più sono ammesse e vanno preservate (§4.1): `verified.commit` è lecito.

## Cambi

### A. `## Excluded paths` (feedback 3)

Sezione opzionale di SCHEMA.md: elenco puntato di glob, relativi alla radice del wiki, tra
backtick.

```markdown
## Excluded paths

- `50-benchmark/results/*-data/**`
```

- Corrispondenza: `fnmatch` sul percorso POSIX relativo alla radice del wiki (Python 3.10,
  niente `PurePath.full_match`). `*` attraversa anche `/`, quindi `adr/*` copre le
  sottocartelle. Le istruzioni dei workflow usano la stessa regola.
- Il validator salta i file corrispondenti (niente controllo di frontmatter né di link al
  loro interno) e stampa una riga `info: <n> paths excluded by SCHEMA` su stdout. Non incide
  sul codice d'uscita.
- I link che puntano a un file escluso restano validi: il file esiste.
- `SCHEMA.md` e i file della Core map non sono escludibili: un glob che li corrisponde è un
  errore su SCHEMA ("Excluded paths must not match SCHEMA or Core map pages").
- Righe non nel formato `` - `<glob>` ``, glob assoluti o con `..`: errore su SCHEMA.
- Sync e lint ignorano gli stessi file; il riferimento oggi a vuoto in `wiki-sync.md`
  ("paths excluded by SCHEMA.md") punta a questa sezione.
- Limite dichiarato nella spec di schema: per un lettore OKF i file esclusi restano concetti
  senza frontmatter. Chi vuole la conformità dà loro il solo `type:` (es. `type: Report`).

### B. Freschezza di `verified` (feedback 1)

- `verified` accetta un `commit` opzionale per voce:
  `{ by: human:<id>, at: <datetime>, commit: <sha> }`. Gli agenti continuano a non scrivere
  né modificare `verified`.
- Lint, per ogni voce: se c'è `commit`, la conferma è *stale* quando una delle `sources` ha
  commit dopo di esso (`git log <commit>..HEAD -- <sources>`); altrimenti quando ne ha dopo
  `at` (`git log --since=<at> -- <sources>`). Commit non risolvibile o `at` non datetime:
  freschezza non determinabile, segnalata come info.
- Esito: warning *Stale verified* con pagina, attore e fonti cambiate. Il livello di fiducia
  non cambia; il riepilogo aggiunge il conteggio:
  `Trust: unverified <n>, machine-confirmed <n>, human-reviewed <n> (stale verified <n>)`.
- Una pagina conta come stale verified quando tutte le voci che le danno il livello sono
  stale (per human-reviewed: tutte le voci `human:`). Una conferma fresca dello stesso
  livello basta a non segnalarla.
- Il validator non cambia: non chiama git e il parsing di `verified` resta quello attuale.

### C. `## Page types` (feedback 2)

Tabella opzionale di SCHEMA.md, colonne `Path | type`, glob con la regola di A.

```markdown
## Page types

| Path | type |
| --- | --- |
| `50-benchmark/*-plan.md` | `Plan` |
| `50-benchmark/results/*` | `Result` |
| `00-project/*` | `Project` |
| `adr/*` | `Decision` |
```

- Vince la prima riga che corrisponde; senza corrispondenza valgono i default esistenti.
  Righe più specifiche vanno quindi prima.
- La usano init (scrive la tabella solo se l'utente sceglie cartelle proprie), ingest e sync
  quando scrivono `type`; il lint segnala come info un `type` diverso da quello atteso.
  Un override esplicito su una singola pagina resta lecito.
- Il validator controlla solo la forma: intestazione `Path | type`, due celle per riga, glob
  relativo senza `..`, tipo non vuoto. Non controlla il `type` delle pagine.

### D. `generated` solo per cambi significativi (feedback 5)

- Formato invariato: datetime UTC con `Z`.
- Sync aggiorna `generated` (by e at) solo quando cambiano le affermazioni della pagina:
  fatti, comandi, percorsi citati come evidenza, stato. Correzioni di link, formattazione,
  riordino o soli metadati (incluso aggiungere `type`/`description` a una pagina legacy) non
  lo toccano. Su una pagina legacy toccata solo nei metadati, sync lascia `updated` com'è
  e non aggiunge `generated` (il validator accetta l'uno o l'altro): non si inventa un
  autore. `updated` viene sostituito da `generated` alla prima modifica significativa.
- Nessuna impostazione di precisione nello SCHEMA: OKF non ammette valori solo-data.

### E. Migrazione `unknown` (nota minore)

Riga in `wiki-sync.md` Step 6: quando sync tocca una riga del tracker o del baton che ha
`unknown` in una colonna obbligatoria, la sostituisce con `Not verified - <motivo>` (o con il
valore ora noto). Nessuna migrazione di massa.

## Fuori scopo (deciso)

- Feedback 4: il validator esegue il tracker sempre e prima della handoff
  (`validate-wiki.py` `run()`), e stampa tutti i findings; non riprodotto. Si riapre con un
  caso minimo.
- Info sul validator per `type`/`description` mancanti: il validator restituisce 1 se trova
  qualcosa; il backlog di migrazione resta compito del lint.
- `stale_after`, `sources[]` come oggetti, frontmatter-free `index.md`, titoli del log solo
  data: differenze note da okf-lite, invariate.

## Dove si cambia

| File | Cambio |
|---|---|
| `canonical/codebase/scripts/validate-wiki.py` | parsing e applicazione di `## Excluded paths`; forma di `## Page types`; riga info |
| `scripts/test-wiki-validator.py` | fixture nuove (sotto) |
| `canonical/codebase/default-schema.md` | sezioni opzionali `## Excluded paths` e `## Page types` (commentate), `verified.commit`, nota OKF sui file esclusi |
| `canonical/codebase/maintainer.md` | regole di A–D |
| `canonical/codebase/workflows/wiki-sync.md` | esclusioni, tipi, criterio di `generated`, migrazione `unknown` |
| `canonical/codebase/workflows/wiki-lint.md` | esclusioni, tipo atteso, *Stale verified*, riepilogo |
| `canonical/codebase/workflows/wiki-ingest.md`, `wiki-init.md` | esclusioni e tipi quando scrivono pagine |
| `canonical/codebase/VERSION`, `.claude-plugin/marketplace.json` | 0.11.0 |
| `docs/release-checklist.md` | voce 0.11.0 |

I pacchetti sotto `plugins/` e `skills/` si rigenerano, non si editano.

## Verifica

Fixture nuove del validator:

1. Un `.md` senza frontmatter sotto un glob escluso → nessun finding, riga info con 1.
2. Lo stesso file senza esclusione → "missing or unterminated frontmatter" (regressione).
3. Glob che corrisponde a una pagina della Core map o a SCHEMA → errore su SCHEMA.
4. Riga di esclusione malformata o con `..` → errore su SCHEMA.
5. Link da una pagina a un file escluso → nessun finding.
6. `## Page types` con intestazione sbagliata, riga a una cella, glob con `..` → errori.
7. `## Page types` valida → nessun finding.

Poi `bash scripts/run-tests.sh` completo (canonico e distribuzioni byte-identiche,
`check-generated.sh` "up to date"). Le regole di lint e sync sono istruzioni per agenti, non
codice: si verificano con uno scenario applicativo su una fixture (wiki con cartelle numerate,
report esclusi, una pagina `verified` con fonte cambiata dopo `at`), dichiarato come tale e
non come prova su host reale.
