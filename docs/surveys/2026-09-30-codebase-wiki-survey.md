# Codebase Wiki LLM — survey a scelta multipla

Data: 2026-09-30  
Partecipanti: Stefano e Alessandro  
Stato: da compilare; nessuna risposta preselezionata.

## Obiettivo già espresso

La wiki deve aiutare sviluppatori e ingegneri già nel progetto, persone nuove
che devono iniziare a lavorarci e agenti che operano sul codice e sulla
gestione del lavoro. Deve rendere comprensibili progetto e decisioni,
permettere modifiche verificate e sostenere il coordinamento delle attività.
Il perimetro è Codebase Wiki LLM; SecondBrain rimane distinto.

## Come rispondere

Ogni domanda propone alternative concrete. La modalità indica se scegliere
**una sola opzione** o **più opzioni**, con eventuale limite e ordine.

Scrivete le lettere nel vostro campo **Scelta**:

- Una scelta: `A`.
- Più scelte: `A, C, D`.
- Quando è richiesto un ordine: `C > A > B`.
- `X`: altra proposta; descrivetela nelle note.
- `Y`: non so ancora; potete indicare cosa servirebbe per decidere.
- `Z`: non applicabile al vostro caso; potete spiegare perché.

X, Y e Z sono disponibili in ogni domanda. Y e Z si usano da sole; X può
accompagnare altre scelte rispettando il limite. Le note sono facoltative,
tranne quando scegliete X. Non occorre scrivere un testo lungo: un esempio
concreto è spesso più utile.

**La mia proposta** segnala una raccomandazione con la sua motivazione.
Non è una risposta già scelta per voi. Le domande sul vostro contesto non
hanno raccomandazioni: devono riflettere ciò che usate e osservate davvero.

Compilate prima individualmente e poi confrontatevi. Uno spazio vuoto non
vale come accettazione di una proposta. Le differenze tra le vostre risposte
serviranno a distinguere comportamenti di base, opzioni e decisioni aperte.

Questo è un file Markdown: le scelte si compilano scrivendo le lettere,
senza pulsanti o invio automatico. Esempio:

```text
Stefano
Scelta: A
Note / esempio: vorrei che il nuovo collega trovasse subito setup e test.

Alessandro
Scelta: D
Note / esempio: nel nostro progetto il primo task può essere molto piccolo.
```

## Direzioni già concordate con Stefano

Le risposte precisano queste direzioni e le priorità. Alessandro può
segnalare esigenze aggiuntive o divergenze:

1. Documentazione utile per sviluppo, onboarding, agenti e gestione del lavoro.
2. Obsolescenza valutata rispetto alle fonti e all’impatto delle modifiche.
3. Evidenza riferita allo stato verificato, incluse modifiche locali rilevanti.
4. Fatti accertati aggiornati direttamente; fatti dubbi dichiarati;
   decisioni prese registrate e proposte tenute distinte.
5. Stato delle attività in una sola fonte; handoff orientato a come ripartire;
   completamento subordinato ai criteri e alle prove.
6. Controlli strutturali automatici e review del significato, con supporto
   della lingua scelta.
7. Reminder che aiutano a sincronizzare, senza confondere una modifica
   qualsiasi alla wiki con la copertura del cambiamento.
8. Evidenza proporzionata e risultati di efficacia misurati su progetti reali.

## A. Utilizzatori, valore e perimetro

### Q01 — Chi deve guidare le scelte della prossima versione?

**Modalità:** Una sola scelta.

Scegliete il criterio prevalente quando le esigenze dei diversi destinatari entrano in conflitto.

- **A.** Bilanciare sviluppatori, persone nuove e agenti, con un punto di ingresso comune e approfondimenti per ruolo.
- **B.** Privilegiare il lavoro quotidiano degli ingegneri già nel progetto.
- **C.** Privilegiare chi entra nel progetto e deve arrivare alla prima modifica.
- **D.** Privilegiare la continuità degli agenti tra coding e gestione del lavoro.

**La mia proposta:** A: mantiene il vostro obiettivo condiviso; i percorsi possono poi avere priorità diverse.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q02 — Quali problemi incontrate più spesso oggi?

**Modalità:** Più scelte, massimo 3.

Selezionate problemi realmente osservati, non quelli che potrebbero capitare in teoria.

- **A.** Si perde tempo a trovare file, comandi, test e informazioni di architettura.
- **B.** Persone o agenti ripetono analisi e tentativi già fatti.
- **C.** Le motivazioni delle decisioni tecniche vengono dimenticate.
- **D.** La documentazione è obsoleta e induce modifiche sbagliate.
- **E.** Non è chiaro chi sta facendo cosa, cosa è bloccato e quale sia il prossimo passo.
- **F.** Il costo di scrivere e aggiornare la documentazione è troppo alto.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q03 — Quali risultati volete ottenere per primi?

**Modalità:** Più scelte, massimo 3; indicate anche l’ordine.

Selezionate le priorità per la prima release migliorata: non tutte possono avere lo stesso peso.

- **A.** Una persona nuova trova il contesto e arriva alla prima modifica verificata.
- **B.** Chi modifica il codice trova invarianti, contratti, rischi e verifiche.
- **C.** Un altro agente riprende un’attività senza rifare il lavoro.
- **D.** Il team vede avanzamento, dipendenze e blocchi con fonti verificabili.
- **E.** Le decisioni e le alternative rimangono comprensibili nel tempo.
- **F.** La wiki richiede poco tempo e poche letture per rimanere utile.

**La mia proposta:** A, B e C come prima base; D va incluso nei casi di prova per coprire anche la gestione del lavoro.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q04 — Su quali tipi di progetto volete usarlo davvero?

**Modalità:** Più scelte, massimo 3.

Indicate i primi contesti concreti. Nelle note potete precisare dimensione del team e numero di repository.

- **A.** Applicazioni web, servizi e backend.
- **B.** Embedded, firmware, hardware/software o ricerca e sviluppo.
- **C.** Librerie, SDK, strumenti CLI o plugin.
- **D.** Monorepo con più componenti e team.
- **E.** Progetti distribuiti su più repository.
- **F.** Progetti legacy con documentazione e vincoli già esistenti.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## B. Onboarding e lavoro di sviluppo

### Q05 — Quale risultato deve ottenere una persona nuova nella prima ora?

**Modalità:** Una sola scelta.

Il risultato deve essere osservabile; la lettura delle pagine da sola non dimostra che l’onboarding funziona.

- **A.** Capire obiettivo e confini, trovare setup e test, individuare il primo task e sapere da dove partire.
- **B.** Ottenere una panoramica del prodotto e dei componenti; setup e primo task possono venire dopo.
- **C.** Comprendere in profondità architettura e decisioni prima di eseguire il progetto.
- **D.** Completare una piccola modifica verificata, con un percorso guidato specifico.

**La mia proposta:** A come requisito generale; D è un buon obiettivo aggiuntivo per i repository pilota.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q06 — Quali informazioni devono essere facili da trovare prima di cambiare codice?

**Modalità:** Più scelte, massimo 4.

Questa scelta determina quali contenuti rendere centrali nelle pagine di modulo.

- **A.** File e punti in cui intervenire.
- **B.** Invarianti e comportamenti che non devono cambiare.
- **C.** Contratti API, dati e compatibilità.
- **D.** Test e comandi per verificare la modifica.
- **E.** Dipendenze, chiamanti e impatto sugli altri componenti.
- **F.** Failure mode noti, rischi e motivazioni delle scelte.

**La mia proposta:** A, B, D e F come base; C ed E diventano centrali quando il modulo espone contratti o dipendenze importanti.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q07 — Quanto deve essere grande la struttura iniziale della wiki?

**Modalità:** Una sola scelta.

Più pagine iniziali danno copertura, ma possono creare sezioni vuote e aumentare il lavoro di manutenzione.

- **A.** Un core compatto e argomenti aggiunti in base alle fonti e alle esigenze del progetto.
- **B.** Un profilo iniziale per tipo di progetto, con un insieme di pagine già proposto.
- **C.** Una struttura completa comune a tutti, lasciando esplicite le parti non ancora documentate.
- **D.** Solo una mappa della documentazione esistente; nuove pagine su richiesta.

**La mia proposta:** A, con la possibilità di proporre profili come aiuto all’inizializzazione.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q08 — Quando un problema risolto merita una voce di troubleshooting?

**Modalità:** Una sola scelta.

Scegliete quanto sapere operativo conservare oltre al log delle attività.

- **A.** Quando è non ovvio o ricorrente: sintomo, causa, fix, verifica e limiti; workaround distinto da soluzione.
- **B.** Per ogni bug risolto, usando una scheda breve standard.
- **C.** Solo quando una persona lo richiede o lo approva.
- **D.** Solo per incidenti e problemi operativi rilevanti; gli altri restano nel log.

**La mia proposta:** A: conserva ciò che può evitare lavoro ripetuto senza catalogare ogni correzione.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## C. Agenti e continuità

### Q09 — Come deve acquisire contesto un agente a inizio lavoro?

**Modalità:** Una sola scelta.

Considerate costo delle letture e rischio di agire con informazioni insufficienti.

- **A.** Leggere un ingresso breve e poi pagine pertinenti al task, verificando le fonti coinvolte prima delle modifiche.
- **B.** Leggere l’intero core a ogni sessione, poi approfondire il task.
- **C.** Esplorare prima il codice e usare la wiki per decisioni e storia quando servono.
- **D.** Scegliere un percorso iniziale diverso per coding, onboarding e gestione del lavoro.

**La mia proposta:** A come base, con percorsi mirati per ruolo come in D.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q10 — Quale formato di handoff vi permette di proseguire davvero?

**Modalità:** Una sola scelta.

Immaginate di cambiare persona, agente oppure host a metà di un’attività.

- **A.** ID del task, prossimo passo, file iniziali, verifiche già fatte e limiti; criteri e stato richiamati dal tracker.
- **B.** Un riepilogo narrativo della sessione, con i principali link.
- **C.** Una checklist molto breve con task, file e prossimo comando; dettagli nel log.
- **D.** Una scheda separata per ogni attività aperta, collegata a un indice degli handoff.

**La mia proposta:** A: mantiene la continuità senza creare una seconda fonte dello stato. Se non resta lavoro, dichiararlo senza inventare task.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q11 — Quali errori degli agenti vi costano di più?

**Modalità:** Più scelte, massimo 3.

Se potete, aggiungete nelle note un episodio che permetta di verificare se il plugin previene l’errore.

- **A.** Trattare come veri fatti inventati o non verificati.
- **B.** Ripetere analisi, comandi o tentativi già conclusi.
- **C.** Ignorare invarianti oppure estendere il perimetro del lavoro.
- **D.** Usare risultati di test vecchi su codice cambiato.
- **E.** Trasformare suggerimenti in decisioni o impegni del team.
- **F.** Chiudere task senza criteri soddisfatti o sovrascrivere il lavoro altrui.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q12 — Quanto può fare autonomamente un agente che gestisce il lavoro?

**Modalità:** Una sola scelta.

Questo riguarda priorità, task, blocchi e avanzamento; non implica autorizzazione a scrivere su strumenti esterni.

- **A.** Aggiornare fatti e avanzamento provati, rilevare blocchi e proporre piani; nuove assegnazioni, scadenze e scope restano decisioni umane.
- **B.** Leggere e riassumere; ogni modifica al tracker viene fatta da una persona.
- **C.** Gestire task e priorità entro limiti espliciti stabiliti dal responsabile del progetto.
- **D.** Preparare tutte le modifiche alla gestione del lavoro, ma richiedere una review prima di applicarle.

**La mia proposta:** A come comportamento predefinito; C può essere un’opzione per progetti che delegano esplicitamente quella responsabilità.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## D. Gestione del lavoro e fonti di autorità

### Q13 — Dove deve vivere lo stato autorevole delle attività?

**Modalità:** Una sola scelta.

Il plugin deve evitare due stati mantenuti indipendentemente per lo stesso task.

- **A.** Adattarsi al progetto: tracker wiki se non c’è uno strumento esterno; altrimenti link alla fonte esterna e riepiloghi con data.
- **B.** Sempre nel tracker wiki; gli strumenti esterni sono solo riferimenti.
- **C.** Sempre nello strumento esterno; la wiki contiene solo contesto e collegamenti.
- **D.** Scegliere la fonte di stato per area o team, dichiarandola nella configurazione del progetto.

**La mia proposta:** A come default. Se non si può leggere la fonte esterna, dichiarare il limite senza indovinare lo stato.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q14 — Quanto dettaglio deve avere il tracker?

**Modalità:** Una sola scelta.

Lo stato delle attività vive qui; l’handoff usa gli ID per spiegare come riprendere il lavoro.

- **A.** ID, stato, obiettivo, responsabile quando noto, criteri, evidenza e prossima verifica; priorità e dipendenze solo se utili.
- **B.** Una tabella essenziale con ID, attività e stato; tutto il dettaglio è nelle pagine dei task.
- **C.** Una scheda completa con priorità, stime, scadenze, dipendenze e milestone per ogni attività.
- **D.** Un indice di task esterni con contesto locale, senza mantenere stati o criteri duplicati.

**La mia proposta:** A per un tracker locale; D quando il progetto ha già una fonte esterna autorevole.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q15 — Come distinguere idee, lavoro approvato e lavoro svolto?

**Modalità:** Una sola scelta.

Una proposta dell’agente non deve diventare automaticamente un impegno del team.

- **A.** Idee e proposte separate dai task approvati; risultati e prove registrati quando osservati.
- **B.** Un unico backlog con categorie esplicite per idea, approvato e in corso.
- **C.** Pianificazione nello strumento esterno; la wiki conserva solo contesto e risultati.
- **D.** Solo attività richieste esplicitamente; il plugin non conserva suggerimenti per il futuro.

**La mia proposta:** A, oppure C se il team ha già un processo di pianificazione stabile.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q16 — Come deve risolvere informazioni in conflitto?

**Modalità:** Una sola scelta.

Esempio: il codice si comporta diversamente dal requisito, oppure un agente dichiara un task concluso senza prove.

- **A.** Distinguere comportamento attuale, requisito desiderato, decisione accettata e stato autorevole; segnalare la divergenza.
- **B.** Conservare entrambe le versioni e richiedere una review per ogni conflitto.
- **C.** Dare precedenza alle fonti eseguibili per i fatti tecnici; richiedere una decisione umana sugli altri conflitti.
- **D.** Usare regole di autorità configurate per progetto e applicarle per ogni categoria di informazione.

**La mia proposta:** A come modello generale, configurabile come in D. Il codice può documentare il comportamento attuale e contenere comunque un bug.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## E. Autonomia, decisioni ed evidenza

### Q17 — Cosa deve fare sync quando cambia un fatto?

**Modalità:** Una sola scelta.

Confrontate il caso di un nuovo comando verificato con quello di una fonte cambiata ma non verificabile.

- **A.** Aggiornare direttamente il fatto provato; rendere visibile l’incertezza e sospendere la vecchia etichetta di verificato quando non confermata.
- **B.** Preparare una proposta per ogni modifica ai fatti verificati, lasciando l’applicazione a una review.
- **C.** Aggiornare automaticamente solo fatti semplici come percorsi e comandi; gli altri richiedono review.
- **D.** Applicare una politica diversa per pagina, in base a criticità e responsabile.

**La mia proposta:** A come default; pagine critiche possono avere vincoli di review espliciti.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q18 — Quale prova basta per registrare una decisione accettata?

**Modalità:** Una sola scelta.

Distinguete registrare una scelta già presa da approvare una nuova proposta.

- **A.** Scelta umana esplicita o approvazione documentata nel processo del progetto; motivazioni sconosciute dichiarate come tali.
- **B.** Solo una dichiarazione esplicita di una persona, anche se esiste già una PR approvata.
- **C.** Qualunque implementazione incorporata nel branch principale, descrivendo solo ciò che si osserva e senza inferire motivi.
- **D.** Fonti di accettazione configurate per progetto, con decisioni proposte separate da quelle accettate.

**La mia proposta:** A, configurabile come D. Una proposta dell’agente rimane una proposta; il solo codice non dimostra le motivazioni.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q19 — Quando un’attività può essere marcata completata?

**Modalità:** Una sola scelta.

La regola deve funzionare per codice, documenti e attività di gestione, non soltanto per test automatici.

- **A.** Quando i criteri concordati sono soddisfatti e provati con verifiche appropriate al tipo di attività; i limiti restano espliciti.
- **B.** Quando una persona responsabile approva il risultato, anche se non esistono verifiche automatiche.
- **C.** Dopo verifiche tecniche e review umana obbligatoria per ogni task.
- **D.** Con livelli distinti: implementata, verificata e accettata, con una regola di chiusura per progetto.

**La mia proposta:** A come minimo, con D se il processo distingue verifica e accettazione. Test non eseguibili non diventano test superati.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q20 — Quale formato di evidenza volete usare?

**Modalità:** Una sola scelta.

Considerate un test, una relazione tra moduli, una decisione e un’ipotesi di rischio.

- **A.** Formato proporzionato: comando/risultato/data per verifiche, fonti precise per descrizioni, approvazione per decisioni, ipotesi esplicite per rischi.
- **B.** Una scheda standard per ogni affermazione, con tipo, fonte, data e limite della prova.
- **C.** Fonti a livello di pagina, con evidenza dettagliata solo per risultati e affermazioni critiche.
- **D.** Un registro delle evidenze separato, richiamato dalle pagine tramite identificatori.

**La mia proposta:** A: consente di controllare le affermazioni senza ripetere output e metadati ovunque.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## F. Aggiornamento, Git e collaborazione

### Q21 — Come deve riconoscere che un’informazione potrebbe essere obsoleta?

**Modalità:** Una sola scelta.

Una modifica cosmetica e un cambio di contratto API non devono avere necessariamente lo stesso effetto.

- **A.** Rilevare modifiche alle fonti e alle dipendenze pertinenti; valutare l’impatto sul contenuto e verificare le affermazioni coinvolte.
- **B.** Considerare ogni modifica alle fonti sufficiente per richiedere una nuova verifica completa della pagina.
- **C.** Usare soglie di commit ed età come primo filtro, poi controllare le pagine segnalate.
- **D.** Verificare le informazioni al momento dell’uso, aggiornando le pagine coinvolte nel task.

**La mia proposta:** A. Soglie come in C sono segnali aggiuntivi: un solo commit può invalidare un fatto importante.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q22 — Come descrivere il codice sul quale è stata eseguita una verifica?

**Modalità:** Una sola scelta.

Il commit corrente da solo non rappresenta eventuali modifiche locali usate per produrre un risultato.

- **A.** Commit, ambito delle fonti e presenza di modifiche locali rilevanti; branch/ambiente quando influiscono sulla prova.
- **B.** Impronte dei file verificati, insieme a comando e ambiente; più precisione e più metadati.
- **C.** Solo verifiche su codice committato; risultati su modifiche locali dichiarati provvisori.
- **D.** Riferimento a commit oppure patch/diff salvata, quando serve riprodurre lo stato completo.

**La mia proposta:** A come base leggibile. B o D possono servire per verifiche che richiedono maggiore riproducibilità; senza Git i limiti vanno dichiarati.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q23 — Quando deve sincronizzare e quanto deve insistere il reminder?

**Modalità:** Una sola scelta.

Il controllo deve considerare anche codice committato nella sessione e modifiche alla wiki che non riguardano il cambiamento.

- **A.** A fine attività significativa, confrontando l’ambito cambiato con quello documentato; reminder informativo e spiegazione breve se non serve sync.
- **B.** Come A, ma il reminder trattiene l’agente finché aggiorna la wiki o motiva perché non occorre.
- **C.** Solo su comando esplicito, con eventuali avvisi informativi a fine sessione.
- **D.** Come verifica prima del commit, con un riepilogo delle possibili lacune da revisionare.

**La mia proposta:** A per limitare l’attrito; B solo se il team vuole un vincolo più forte. Una modifica qualsiasi alla wiki non dimostra copertura.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q24 — Come gestire lavoro parallelo di più persone o agenti?

**Modalità:** Una sola scelta.

Considerate ID nuovi, modifiche alla stessa pagina e handoff di attività diverse.

- **A.** Tracker condiviso, aggiornamenti circoscritti e handoff per ambito; rilevare conflitti e preservare il lavoro altrui.
- **B.** Una persona o un agente coordina tutte le scritture alla wiki; gli altri preparano proposte.
- **C.** Note e handoff separati per partecipante, poi consolidamento esplicito.
- **D.** Supportare prima sessioni sequenziali, dichiarando il limite sul lavoro contemporaneo.

**La mia proposta:** A come obiettivo, con una soluzione minima verificabile; D è accettabile solo come limite esplicito della prima release.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## G. Struttura, leggibilità e costo

### Q25 — Come deve adottare documentazione già esistente?

**Modalità:** Una sola scelta.

La wiki può avere una struttura diversa dai percorsi predefiniti del plugin.

- **A.** Mappare i documenti esistenti e aggiungere solo ciò che manca, senza creare copie o riorganizzare automaticamente.
- **B.** Proporre una migrazione alla struttura standard, con spostamenti concordati.
- **C.** Creare un piccolo core nuovo che collega i documenti esistenti, lasciandoli separati.
- **D.** Usare soltanto la documentazione esistente e segnalare lacune senza creare nuovi file.

**La mia proposta:** A; C è utile quando il progetto vuole conservare docs e contesto operativo distinti.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q26 — Dove leggerete e compilerete più spesso la wiki?

**Modalità:** Più scelte, massimo 3.

Indicate gli strumenti che usate già: questa risposta orienta navigazione e formato, non richiede una nuova piattaforma.

- **A.** Editor/IDE, aprendo direttamente i file Markdown.
- **B.** Interfaccia web del repository, con link e review.
- **C.** Obsidian o un altro lettore di note.
- **D.** Chat con l’agente, chiedendo risposte basate sulla wiki.
- **E.** Terminale e ricerca testuale.
- **F.** Una vista leggibile dedicata, per onboarding o gestione del lavoro.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q27 — Come bilanciare completezza e costo di aggiornamento?

**Modalità:** Una sola scelta.

Considerate letture, tempo dell’agente, costo in token e tempo umano di review.

- **A.** Aggiornamenti piccoli e mirati per il lavoro ordinario; approfondimenti più costosi dichiarati separatamente.
- **B.** Priorità alla copertura completa, anche se ogni sync richiede più tempo.
- **C.** Un budget rigido per ogni operazione; fermarsi e riportare le lacune quando è superato.
- **D.** Budget configurabili per progetto e criticità, con un riepilogo del lavoro rinviato.

**La mia proposta:** A con configurazione come D. Nelle note potete indicare un limite concreto per un piccolo cambiamento.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q28 — Come deve archiviare log e informazioni storiche?

**Modalità:** Una sola scelta.

Lo storico deve restare distinguibile dalle istruzioni attuali e conservare le proprie evidenze.

- **A.** Archiviare secondo regole del progetto, con operazioni reversibili, link e date preservati; riepilogo delle modifiche.
- **B.** Proporre ogni archiviazione e applicarla solo dopo conferma.
- **C.** Archiviare solo a chiusura di release/milestone, su iniziativa del responsabile.
- **D.** Mantenere pagine correnti brevi e uno storico append-only separato.

**La mia proposta:** A se le regole sono concordate; B per riorganizzazioni che richiedono giudizio oltre quelle regole.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## H. Controlli, linguaggio e gestione degli errori

### Q29 — Quali controlli automatici hanno priorità?

**Modalità:** Più scelte, massimo 4.

Questi controlli riguardano errori riconoscibili senza giudicare il significato di tutta la documentazione.

- **A.** Campi obbligatori, tipi e date validi.
- **B.** Fonti esistenti e link interni funzionanti.
- **C.** ID univoci e riferimenti a task presenti.
- **D.** Percorsi validi e ruoli coerenti nel Core map.
- **E.** Criteri ed evidenza minimi per handoff e completamento.
- **F.** Dimensioni e budget, fonti cambiate e duplicazione dello stato.

**La mia proposta:** A, B, D ed E come primo gruppo; C e F seguono secondo le priorità d’uso. La correttezza del significato richiede anche review.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q30 — Come gestire la lingua senza rompere i controlli?

**Modalità:** Una sola scelta.

Un progetto può avere pagine italiane, inglesi o documenti adottati con titoli differenti.

- **A.** Titoli e testo nella lingua scelta, con identificatori tecnici stabili per gli strumenti.
- **B.** Intestazioni tecniche fisse in inglese, corpo del testo nella lingua scelta.
- **C.** Tutto in inglese per mantenere uniforme il formato.
- **D.** Convenzioni configurabili e riconoscimento di più varianti linguistiche, anche in wiki miste.

**La mia proposta:** A: separa la leggibilità umana dal contratto degli strumenti, senza basarsi su frasi inglesi esatte.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q31 — Cosa deve fare quando non può verificare una fonte o eseguire un comando?

**Modalità:** Una sola scelta.

Esempi: test assenti, servizio non raggiungibile, accesso negato, file rinominato o Git non disponibile.

- **A.** Fermare solo la conclusione non verificabile, dichiarare il limite e proseguire con ciò che è controllabile.
- **B.** Fermare l’intera operazione e chiedere come ottenere la verifica mancante.
- **C.** Preparare modifiche provvisorie, chiaramente non verificate, e richiedere review prima di applicarle.
- **D.** Applicare regole diverse per contenuti critici e descrizioni a basso impatto.

**La mia proposta:** A come default; D per criticità esplicite. Un errore di verifica non è prova né di successo né di fallimento del comportamento.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q32 — Come gestire correzioni manuali e contraddizioni trovate dall’agente?

**Modalità:** Una sola scelta.

Il codice descrive il comportamento attuale, mentre un documento umano può descrivere il comportamento desiderato.

- **A.** Correggere fatti verificabili senza perdere requisiti e motivazioni umane; segnalare i conflitti che richiedono una decisione.
- **B.** Non modificare pagine scritte manualmente; proporre sempre la correzione.
- **C.** Sottoporre tutte le correzioni a review prima di applicarle.
- **D.** Definire pagine con responsabile e regole di modifica; altrove aggiornare direttamente i fatti provati.

**La mia proposta:** A come default, con D per documenti che il team vuole governare esplicitamente.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## I. Distribuzione, integrazioni e confini

### Q33 — Quali host potete usare e verificare davvero?

**Modalità:** Più scelte; indicate l’ordine di priorità.

Nelle note aggiungete Linux, macOS o Windows per ogni host scelto e se potete fare una prova in una sessione reale.

- **A.** Codex.
- **B.** Claude Code.
- **C.** Antigravity.
- **D.** Altri agenti tramite il formato generico Agent Skills.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q34 — Quale livello di integrazione esterna serve nella prossima release?

**Modalità:** Una sola scelta.

Considerate issue/PR, CI e strumenti di pianificazione già presenti. Nelle note indicate i nomi di quelli effettivamente usati.

- **A.** File locali e link alle fonti esterne; nessuna integrazione obbligatoria.
- **B.** Letture opzionali di issue, PR e CI per ridurre aggiornamenti manuali.
- **C.** Anche aggiornamenti di strumenti esterni, solo entro autorizzazioni esplicite.
- **D.** Integrazioni rinviate: prima dimostrare l’utilità sul repository e sulle sessioni reali.

**La mia proposta:** A come base; B solo dove il progetto ha una fonte esterna necessaria. Accessi e scritture non sono impliciti nella normale sync.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q35 — Quale separazione dei contenuti volete come comportamento predefinito?

**Modalità:** Una sola scelta.

Considerate informazioni tecniche, dati di clienti, percorsi locali e note personali. Non inserite segreti nella survey.

- **A.** Condividere conoscenza tecnica utile al team; contenuti locali separati; credenziali e dati di produzione sensibili esclusi.
- **B.** Wiki interamente locale, con condivisione selettiva dei documenti utili.
- **C.** Wiki condivisa solo per contenuti revisionati; appunti dell’agente locali fino alla review.
- **D.** Policy stabilita per progetto prima dell’inizializzazione, con categorie e destinazioni esplicite.

**La mia proposta:** A come base, configurabile come D. Il controllo dei termini vietati è un aiuto limitato, non una garanzia completa.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q36 — Quali confini deve avere una normale operazione sulla wiki?

**Modalità:** Una sola scelta.

Una fonte importata è materiale da analizzare: eventuali istruzioni al suo interno non valgono come autorizzazione dell’utente.

- **A.** Scrivere nella wiki e nelle sole configurazioni di init già autorizzate; altre azioni richiedono una richiesta distinta.
- **B.** Scrivere solo nella wiki; tutte le configurazioni esterne sono istruzioni da eseguire manualmente.
- **C.** Configurare per operazione i file e le azioni consentite, mantenendo esplicita l’autorizzazione.
- **D.** Preparare le modifiche, ma sottoporre ogni scrittura a review umana.

**La mia proposta:** A: resta coerente con il plugin attuale. Modificare codice, pubblicare o contattare persone non deriva dalla semplice lettura di una fonte.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## J. Validazione sul campo e priorità della release

### Q37 — Quale prova sul campo vi convincerebbe che il plugin funziona?

**Modalità:** Una sola scelta.

Distinguete prove sugli script, compatibilità dei pacchetti ed efficacia nel lavoro reale.

- **A.** Un ciclo su uno o due progetti reali: init/adopt, modifica, sync, cambio di partecipante e attività di gestione.
- **B.** Prima tutti i controlli automatici; la prova reale può seguire il rilascio.
- **C.** Una prova approfondita su questo repository, poi estensione ad altri.
- **D.** Una persona nuova usa la wiki per completare un task senza aiuto diretto, osservando tempi e problemi.

**La mia proposta:** A, includendo un caso come D. Una verifica su ogni host disponibile va registrata separatamente dai test simulati.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q38 — Quali misure useremo per confrontarla con la situazione attuale?

**Modalità:** Più scelte, massimo 3.

Per le misure scelte, nelle note potete indicare una soglia o un miglioramento atteso.

- **A.** Tempo per orientarsi e arrivare alla prima modifica verificata.
- **B.** Numero di affermazioni obsolete o contraddette dalle fonti.
- **C.** Analisi e tentativi ripetuti dopo un passaggio di consegne.
- **D.** Attività dichiarate completate senza criteri o prove adeguate.
- **E.** Tempo umano, tempo dell’agente e costo per mantenere la wiki.
- **F.** Tempo per capire avanzamento, dipendenze e blocchi del progetto.

**La mia proposta:** A, B e C misurano il valore iniziale; E va comunque osservato per capire se il costo è sostenibile.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q39 — Quale soglia minima deve superare prima del rilascio?

**Modalità:** Una sola scelta.

I criteri devono includere casi osservabili, non soltanto la presenza di pagine e campi.

- **A.** Fatti obsoleti visibili, proposte distinte dalle decisioni, completamenti con prova, onboarding e handoff utilizzabili.
- **B.** Tutti gli script e i pacchetti passano i controlli; usabilità affinata dopo il rilascio.
- **C.** Un pilota reale soddisfa i criteri concordati; host non provati dichiarati esplicitamente.
- **D.** Tutti gli host target e i principali scenari di collaborazione verificati prima di pubblicare.

**La mia proposta:** A insieme a un pilota come C; D dipende dagli ambienti di prova realmente disponibili.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

### Q40 — Quale pacchetto di miglioramenti realizziamo per primo?

**Modalità:** Una sola scelta.

Questa scelta fissa l’ordine, non elimina i suggerimenti già concordati. Nelle note indicate anche il compromesso che non accettereste.

- **A.** Affidabilità dei fatti, evidenza proporzionata, tracker/handoff coerenti e aggiornamenti prevedibili.
- **B.** Percorsi per sviluppatori e onboarding, con esempi e navigazione migliori.
- **C.** Coordinamento e management: dipendenze, priorità e collaborazione tra partecipanti.
- **D.** Compatibilità degli host, controlli e integrazioni con gli strumenti già usati.

**La mia proposta:** A, verificato con scenari di B e C; D deve garantire il funzionamento di base senza espandere prematuramente le integrazioni.

**Stefano**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

**Alessandro**

- Scelta:
- Note / esempio (facoltativo; richiesto per X):

## Confronto finale — dopo le risposte individuali

Per le domande in cui concordate, riportate le lettere condivise. Per le
altre, scegliete insieme il seguito:

- **A.** Adottare una scelta comune come comportamento predefinito.
- **B.** Supportare entrambe tramite configurazione del progetto.
- **C.** Fare una prova sul campo prima di decidere.
- **D.** Rinviare la scelta perché non necessaria nella prossima release.

| Domanda | Scelta Stefano | Scelta Alessandro | Seguito A/B/C/D | Scelta comune o prova necessaria |
| --- | --- | --- | --- | --- |
| Da compilare | | | | |

### Priorità condivise

P0 = indispensabile nella prossima release; P1 = utile dopo P0;
P2 = rinviabile; fuori perimetro = non previsto per il plugin.

| Priorità | Domande di origine | Comportamento richiesto | Risultato osservabile per accettarlo |
| --- | --- | --- | --- |
| Da compilare | | | |

### Prova sul campo

La scelta di Q37 va completata con i dati pratici, quando disponibili:

- Repository e scenario:
- Partecipanti e ruoli:
- Host e sistemi disponibili:
- Misure scelte in Q38 e situazione iniziale:
- Criteri di rilascio scelti in Q39:

## Come saranno usate le risposte

Le scelte guideranno requisiti condivisi e criteri di accettazione. Le
raccomandazioni e le risposte individuali non diventano automaticamente
requisiti approvati. Le divergenze verranno risolte distinguendo un default,
un’opzione per progetto o una prova necessaria.

I requisiti saranno tradotti in modifiche coerenti a schema, template,
workflow, controlli e documentazione. I pacchetti dei diversi host
continueranno a essere generati dalle fonti canoniche. I test degli script,
le sessioni reali e le misure di utilità resteranno risultati distinti.
