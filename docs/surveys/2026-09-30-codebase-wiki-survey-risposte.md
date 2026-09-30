# Codebase Wiki LLM — risposte alla survey

Data: 2026-09-30 · Risposte date insieme da Stefano e Alessandro (una sola
scheda, compilata in chat). Survey: [2026-09-30-codebase-wiki-survey.md](2026-09-30-codebase-wiki-survey.md).

Regola usata: una domanda lasciata vuota vale il suggerimento di Claude
mostrato accanto; in questa compilazione tutte le domande hanno una risposta.

| Domanda | Scelta | Suggerimento Claude | Note |
| --- | --- | --- | --- |
| Q01 | A | A | |
| Q02 | B, C, D | B, C, D | |
| Q03 | B, C, E | C > E > B | ordine non indicato |
| Q04 | A, B, E, F | B, C, F | 4 scelte su massimo 3 |
| Q05 | A | A | |
| Q06 | A, B, D, F | A, B, D, F | |
| Q07 | A | A | |
| Q08 | A | A | |
| Q09 | B | A | |
| Q10 | A | A | |
| Q11 | A, E, F | A, B, D | |
| Q12 | A | A | |
| Q13 | B | A | |
| Q14 | A | A | |
| Q15 | A | A | |
| Q16 | A | A | |
| Q17 | A | A | |
| Q18 | A | A | |
| Q19 | A | A | |
| Q20 | A | A | |
| Q21 | A | A | |
| Q22 | A | A | |
| Q23 | A | B | |
| Q24 | A | A | |
| Q25 | B | A | |
| Q26 | A, C, D | A, C, D | |
| Q27 | A | A | |
| Q28 | A | B | |
| Q29 | A, B, D, E | A, B, D, E | |
| Q30 | A + X | A | X: la lingua va chiesta nella survey iniziale, oppure quando esiste già una wiki o documentazione |
| Q31 | A | A | |
| Q32 | A | A | |
| Q33 | A, B, C, D | B > C > A | ordine non indicato |
| Q34 | A | A | |
| Q35 | A | A | |
| Q36 | A | A | |
| Q37 | A | A | |
| Q38 | A, B, C + X | A, B, C | X: i test sul campo li fa Stefano su progetti esistenti; test con subagenti ammessi |
| Q39 | D + X | C | X: prima Codex, Claude e Antigravity; gli altri harness in un secondo momento |
| Q40 | A | A | |

Note generali: «se hai altri dubbi fammi altre domande».

## Chiarimenti successivi (2026-09-30)

- **Q23** — il promemoria arriva all'agente al turno successivo, come nota
  informativa; non ferma mai la sessione.
- **Q25** — init adotta prima i file dove sono, poi propone un piano di
  migrazione verso la struttura standard, confermato spostamento per spostamento.
- **Q09** — l'intero nucleo si rilegge quando il contesto è nuovo (nuova chat,
  ripresa o contesto compattato), non a ogni turno della stessa chat.
- **Q04** — restano tutte e quattro le scelte (A, B, E, F): il plugin deve
  andare bene per tutti questi tipi di progetto.
- **Q03 / Q33** — ordine non indicato: si usa quello suggerito (C > E > B;
  Codex, Claude e Antigravity insieme come primo gruppo, come da Q39).
