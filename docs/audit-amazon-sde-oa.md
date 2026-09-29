# Audit Amazon SDE-I OA Bootcamp

Data: 29 settembre 2026. Working tree locale, senza commit o push.
Il report distingue le verifiche automatiche dalle valutazioni didattiche e dai limiti dell'ambiente.

## Problemi trovati

Non sono stati identificati problemi classificati CRITICO. Questo non equivale a una garanzia di assenza di difetti.

| Gravità | File | Problema ed effetto | Correzione |
|---|---|---|---|
| ALTO | `dev48/runners.py` | Alcuni runner dei lab raccoglievano output senza i limiti applicati agli esercizi: un processo bloccato o rumoroso poteva trattenere l'operazione. | Esecuzione con timeout e limite di output per Node, .NET, Angular e C++; risultati interrotti rifiutati. |
| MEDIO | `dev48/runners.py` | Un `package.json` alla radice veniva trattato come progetto Angular, rendendo irraggiungibile il percorso Node generico. | Angular rilevato nel client; progetti Node alla radice instradati a `npm test`. Test su un progetto Node realmente eseguito. |
| MEDIO | `dev48/app.py` | Il prompt repository del Full Mock ripeteva descrizione e requisiti del lab, fornendo indicazioni eccessive sui difetti. | Prompt neutro: README, test, flussi e ipotesi; niente requisiti specifici copiati nel mock. |
| MEDIO | `tools/generate_amazon_sde.py` | Alcune Work Simulation riusavano azioni su cache, flag o duplicati estranee alla situazione descritta. | Famiglie mirate per hotfix, rollback, retention, review, accessibilità, race, incident e altri contesti; feedback specifico. |
| MEDIO | `tools/generate_amazon_sde.py` | In tutte le 36 Work Simulation la D era la scelta meno efficace. Alcune alternative proponevano comportamenti caricaturali. | Permutazione stabile per scenario, senza ciclo di posizioni; alternative riscritte come compromessi plausibili. La scelta meno efficace è A in 7 casi, B in 12, C in 9, D in 8. |
| MEDIO | `dev48/app.py` | Cambiare le lettere delle alternative poteva reinterpretare una classifica salvata. | Impronta del contenuto associata al nuovo tentativo; in caso di variazione il vecchio progresso resta conservato, ma non viene riproposto come risposta alle nuove opzioni. |
| BASSO | `tools/generate_amazon_sde.py` | La spiegazione di Combination Sum descriveva il costo come `O(2^n)` anche con riuso dei candidati. | Costo legato all'albero di ricerca, target, candidato minimo e dimensione dell'output. |
| BASSO | `tools/generate_amazon_sde.py` | Un caso di Climbing Stairs dichiarava necessità di 64 bit, ma il limite `n <= 45` resta nel signed 32 bit. | Titolo del test coerente con il limite dichiarato. |
| BASSO | `tools/generate_amazon_sde.py` | Alcune lezioni sui pattern avevano esempi troppo compressi per una persona arrugginita. | Tracce concrete aggiunte per Binary Search, grid BFS/DFS, Topological Sort e Heap. |

## Cose controllate e risultate corrette

- Tre cataloghi indipendenti caricati attraverso `TRACK_DEFINITIONS`; Ctrl+T apre il selettore anziché alternare due percorsi.
- Lezioni Amazon autonome: 44 Markdown referenziati, nessun Markdown orfano o mancante.
- 65 problemi logici, con scelta di variante Python/C++; le varianti non duplicano le righe del curriculum.
- Gli scaffold creano solo file mancanti e preservano le modifiche nel workspace.
- Gli starter dei sei lab sono volutamente difettosi; i fallimenti non sono presentati come suite verdi.
- I test del progresso usano database e workspace temporanei, verificando separazione fra track e ripristino.
- Work Style offre riflessioni senza punteggio di selezione né istruzioni per falsificare un profilo.

## Audit didattico

Le lezioni sono testi brevi e specifici, recuperabili per argomento. Il piano organizza le attività senza sostituire le lezioni con sei macro-documenti. I collegamenti fra pattern e gli esempi concreti sono preferibili a formule introduttive ripetute. La qualità editoriale è una valutazione manuale: un test di lunghezza o presenza di parole non dimostra che una spiegazione sia sufficiente per ogni studente.

La progressione passa da confronto fra linguaggi, complessità, array/mappe a pattern lineari, ricerca, strutture collegate, grafi, heap e DP. La banca include problemi aggiuntivi rispetto al piano essenziale; non si richiede di terminare l'intero catalogo in sei giorni.

| Giorno | Minuti di lezioni, esercizi, lab e simulazioni selezionati | Ore |
|---|---:|---:|
| 1 | 343 | 5h43 |
| 2 | 275 | 4h35 |
| 3 | 335 | 5h35 |
| 4 | 360 | 6h00 |
| 5 | 380 | 6h20 |
| 6 | 375 | 6h15 |

Totale essenziale: 2.068 minuti, circa 34,5 ore. Catalogo completo: circa 54,7 ore. Sono stime del catalogo, senza pause né una misura empirica su studenti: il piano è intensivo e può richiedere più tempo a chi riparte da zero.

Gli esercizi coprono i pattern richiesti e includono casi limite. Le prove grandi di Two Sum e Contains Duplicate rendono visibile il costo della soluzione quadratica; non costituiscono una verifica generale di Big-O per ogni problema. Le soluzioni ufficiali superano i casi dichiarati, che restano un insieme finito di esempi e non una dimostrazione di correttezza universale.

Le 160 flashcard hanno zero domande duplicate esatte, zero risposte duplicate esatte e zero coppie di domande con similarità SequenceMatcher almeno 0,88 dopo normalizzazione. La risposta più lunga ha 15 parole. Questo controllo non dimostra assenza di equivalenza semantica; il testo va valutato anche manualmente.

Le 36 situazioni Work Simulation hanno brief distinti, quattro azioni e ragioni di confronto. La revisione ha eliminato le incongruenze più evidenti e il segnale della lettera D. Il ranking è feedback formativo relativo al contesto, non una risposta ufficiale Amazon o una previsione del risultato dell'assessment.

## Audit tecnico

| Area | Evidenza | Limite |
|---|---|---|
| Track e UI | Test del selettore, tasti, layout a più dimensioni, Ctrl+T e persistenza della track | Le prove Textual non equivalgono a ogni configurazione di terminale Windows |
| Python | Tutte le 65 soluzioni ufficiali; prove negative di sintassi, runtime, valore errato, ciclo infinito e stdout | Runner locale con i permessi dell'utente, non sandbox OS |
| C++ | GCC MSYS2 16.2.0, C++20; tutte le 65 soluzioni realmente compilate ed eseguite | Non è stata eseguita una seconda campagna con Clang |
| C++ negativo | Compilazione errata, risposta errata, eccezione, exit nonzero, infinito e output enorme realmente rifiutati | Sei casi mirati, non un fuzzing del compilatore/harness |
| Lab Node | Quattro starter realmente eseguiti via runner, con fallimenti attesi; progetto Node corretto passa | La suite del lab verifica solo i requisiti espressi dai suoi test |
| Lab C++ | Entrambi gli starter compilano e falliscono; copie con fix minimi passano | Gli starter restano difettosi per l'attività didattica |
| Progresso | Test di backup, riapertura, separazione track e varianti linguistiche | Nessuna migrazione o modifica diretta del database personale |
| Full Mock | Test di sequenza, stop e blocco della navigazione; timer indipendenti 40 e 60 | La durata reale di 100 minuti non è stata attesa: il test pilota le scadenze |
| NO AI | Hint e soluzione nascosti nel tentativo a tempo; restrizioni nell'interfaccia | Disciplina locale, non controllo degli strumenti esterni |
| Generator | Due generazioni consecutive confrontate mediante digest del catalogo e Markdown | Le regole di contenuto restano da mantenere nel generatore |
| Offline | Cataloghi, lezioni, esercizi e scaffold locali; lab Amazon senza pacchetti da scaricare | Primo setup Python e lab storici possono richiedere download |
| Avvio Windows | Batch aggiornato avviato in PTY dalla copia isolata; tasti 1/2/3 aprono le tre dashboard, Ctrl+T torna al selettore, Ctrl+Q termina con codice 0 | Prova con virtualenv già configurato; non reinstalla l'ambiente da zero |
| Regressioni storiche | Soluzioni ufficiali React e .NET/Angular e test TUI nella suite completa | Non sostituisce una verifica browser di ogni lab storico |

## Numeri reali finali

| Voce | Numero |
|---|---:|
| Moduli | 10 |
| Lezioni | 44 |
| Problemi logici distinti | 65 |
| Implementazioni Python | 65 |
| Implementazioni C++ | 65 |
| Easy / Medium / Hard | 21 / 35 / 9 |
| Lab Node / C++ | 4 / 2 |
| Flashcard | 160 |
| Work Simulation | 36 |
| Work Style | 8 |
| Simulazioni | 4: 25, 40, 60, 40+60 minuti |

## Fonti verificate

La pagina [Amazon SDE OA](https://www.amazon.jobs/content/en/how-we-hire/university/sde-oa) indica che la struttura dipende dal paese e invita a controllare l'email dell'assessment. Il 40+60 del bootcamp è il formato di pratica richiesto, non un formato universale certificato dalla pagina pubblica.

La lezione elenca i 16 [Leadership Principles ufficiali](https://www.amazon.jobs/content/en/our-workplace/leadership-principles) e discute tensioni fra impatto, reversibilità, evidenza e comunicazione. Non propone una tabella meccanica di risposte.

La documentazione [HackerRank AI Assistant](https://candidatesupport.hackerrank.com/articles/7634558376-ai-assistant-in-tests) e quella sulle [repository assessments](https://candidatesupport.hackerrank.com/articles/8606305957-taking-front-end-back-end-full-stack-and-mobile-developer-assessments) sono riferimenti per le funzioni della piattaforma; le istruzioni del singolo invito restano decisive. Il corso allena comprensione e validazione autonoma.

## Test

Suite finale dopo tutte le modifiche: **50 passed, 0 failed, 0 skipped**, in 121,48 secondi (`.venv/Scripts/python.exe -m pytest -q -rs`). Nessun controllo C++ è saltato: GCC era disponibile. `doctor.py` termina con codice 0 e supera anche il controllo C++20. `git diff --check` non rileva errori di whitespace; Git segnala solo la normalizzazione LF/CRLF prevista su Windows.

## Limitazioni residue e pulizia

La policy automatica aveva respinto i tentativi di cancellazione con il solo motivo `blocked by policy`. Dopo aver fornito il comando PowerShell per la pulizia manuale, la verifica del filesystem conferma che tutte le sette cartelle identificate sono assenti: `.pytest_cache`, `tmp/launcher-smoke-oa`, le `__pycache__` in `dev48`, `tests` e `tools`, `workspace/lab-react-list/dist` e la copia `dev48-launch-check-_93nbo5e` sotto AppData/Local/Temp. L'interprete originale `.venv/Scripts/python.exe` è ancora presente. La directory contenitore `tmp` è vuota. Il blocco operativo sulla pulizia è quindi risolto.

Le regole `.gitignore` coprono cache, `tmp/`, `temp/`, backup e residui di patch; dati personali, virtualenv e workspace erano già esclusi. Le nuove lezioni, il catalogo, il generatore e gli scaffold sono sorgenti del corso e non artefatti temporanei da eliminare.

Non sono stati fatti commit o push. Il working tree resta disponibile per revisione.
