# FINAL READINESS REPORT

Data: 1 ottobre 2026. Working tree locale, successivo all'audit iniziale.

## Stato

READY FOR STUDY

## Evidence

La decisione significa che si può iniziare a studiare senza un'altra riprogettazione materiale; non prevede il superamento Amazon. Sono stati confrontati teoria, pratica, timer, repository e comportamento, corretti i problemi concreti trovati e verificato il software.

Catalogo corrente: 45 lezioni (44 obbligatorie e 1 Trie facoltativa), 10 moduli, 89 problemi logici (89 varianti Python e 89 C++), 6 laboratori logici, 160 flashcard, 36 scenari, 8 riflessioni Work Style, 4 simulazioni. Difficoltà: 25 Easy, 51 Medium, 13 Hard. La doppia variante non raddoppia il numero dei problemi.

## Confronto con fonti

Fonti consultate durante questa validazione il 29 settembre 2026:

| Fonte | Tipo | Confronto |
|---|---|---|
| [Amazon University SDE OA](https://www.amazon.jobs/content/en/how-we-hire/university/sde-oa) | UFFICIALE | Formato variabile; l'invito dell'utente resta il riferimento per 40+60 e risorse vietate, anche quando i tempi pubblici generali differiscono. |
| [Annuncio AUTA 10476343](https://www.amazon.jobs/it/jobs/10476343/software-development-engineer-amazon-university-talent-aquisition-auta) | UFFICIALE | DSA, algoritmi, OOD, debugging, codice mantenibile, collaborazione e SDLC. Focus OA; nessuna certificazione delle competenze lavorative AWS/distributed systems. |
| [Software development topics](https://amazon.jobs/content/en-gb/how-we-hire/interview-prep/software-development-topics) | UFFICIALE | Linguaggio, DSA, coding e OOD applicati concretamente. I temi dell'intero colloquio non diventano tutti Core in sei giorni. |
| [Leadership Principles](https://www.amazon.jobs/content/en/our-workplace/leadership-principles) | UFFICIALE | Tutti i 16 principi verificati. |
| [AI Assistant](https://candidatesupport.hackerrank.com/articles/7634558376-ai-assistant-in-tests) | UFFICIALE | Configurazioni Guarded/Unguarded, contesto file e interazioni registrate; applicare le regole dell'invito, senza presumere le capacità AI di ogni prova. |
| [Project assessments](https://candidatesupport.hackerrank.com/articles/8606305957-taking-front-end-back-end-full-stack-and-mobile-developer-assessments) | UFFICIALE | Navigazione progetto, esecuzione e test. |
| [Execution environment](https://candidatesupport.hackerrank.com/articles/2201684846-execution-environment) | UFFICIALE | Versioni e limiti reali da controllare; GCC/Python locali non definiscono l'ambiente Amazon. |
| [HackerRank Preparation Kit](https://www.hackerrank.com/interview/interview-preparation-kit) | UFFICIALE, benchmark generale | Principali famiglie DSA; percentuali pubblicate non interpretate come probabilità Amazon. |
| [Python structures](https://docs.python.org/3/tutorial/datastructures.html), [Node test runner](https://nodejs.org/api/test.html) | UFFICIALE | Semantica strutture Python e test Node locali senza pacchetti esterni. |
| [C++ priority_queue](https://en.cppreference.com/w/cpp/container/priority_queue.html) | RIFERIMENTO TECNICO | Heap di default e comparatori. |
| [Top Interview 150](https://leetcode.com/studyplan/top-interview-150/), [Minimum Window](https://leetcode.com/problems/minimum-window-substring/), [NeetCode](https://neetcode.io/roadmap) | COMMUNITY / BENCHMARK | Famiglie e difficoltà. Top 150 propone oltre tre mesi; non imposto come carico di sei giorni. Minimum Window riclassificato Hard. |
| [Discussione candidati](https://www.reddit.com/r/leetcode/comments/1ua137z/recently_received_amazon_sde_online_assessment/) | ANECDOTAL | Racconti recenti su repository/AI, contraddittori su alcuni dettagli: solo contesto operativo, senza domande reali o leak. |

## Coverage

| Componente | Pratica |
|---|---|
| Coding 40 | Un problema, starter minimo, lingua scelta, runner reale, pattern nascosto, hint/soluzione assenti nella simulazione. |
| Repository 60 | Node/C++ multi-file, README, test, Repository/Service/API/helper, difetti iniziali reali. |
| Full Mock | 40, stop, nuovi 60 minuti senza trasferimento; scelta stack bloccata dopo start e ritorno bloccato durante mock. |
| Work Simulation | 36 scenari originali con tradeoff e spiegazioni formative; lettere permutate, nessuna chiave Amazon dichiarata. |
| Work Style | 8 riflessioni su lettura/coerenza/autenticità; nessun punteggio o profilo da fingere. |
| LP | 16 principi applicati a cliente, ownership, evidenze, collaborazione, priorità e qualità. |

## DSA coverage

Nessun gap bloccante individuato per il Core OA. Matrice teoria→pratica→timer: [amazon-sde-coverage.md](amazon-sde-coverage.md). Confronto deduplicato di 172 titoli Blind 75 / Grind 75 / LeetCode 75: [amazon-blind75-coverage.md](amazon-blind75-coverage.md). I benchmark descrivono pattern generali e non frequenza Amazon.

| Benchmark richiesti | Task locale, prefisso sde-e- |
|---|---|
| Two Sum; Group Anagrams; Top K Frequent | two-sum; group-anagrams; top-k-frequent |
| Product Except Self; Stock Profit; 3Sum | product-except-self; stock-profit; three-sum |
| Container; Longest Substring; Minimum Window | container-water; longest-substring; min-window |
| Parentheses; Daily Temperatures; Binary Search | valid-parentheses; daily-temperatures; binary-search |
| Rotated Search; Search on Answer; Merge Intervals | search-rotated; min-eating-speed; merge-intervals |
| Reverse List; Linked List Cycle; Tree Level Order | reverse-list; linked-list-cycle; tree-level-order |
| Validate BST; Islands; Clone Graph | validate-bst; number-islands; clone-graph |
| Oranges; Course Schedule; Kth Largest | oranges-rotting; course-schedule; kth-largest |
| K Closest; Subsets; Combination Sum | k-closest; subsets; combination-sum |
| House Robber; Coin Change; Word Break | house-robber; coin-change; word-break |

Tree Level Order ha ora un task diretto Extended; la BFS multi-sorgente su grid resta un esempio distinto. Clone Graph è già presente nel catalogo e Dijkstra/network-delay resta Extra.

## Practice quality

I 25 Easy recuperano sintassi, indici e casi base. I 51 Medium includono finestre con frequenze, prefissi/mappe, confini, ricerca sulla risposta, grafi e DP con stato da scegliere. I 13 Hard sono approfondimenti limitati, non un requisito per completare il Core.

La pratica mista combina window/map, graph/BFS, graph/heap, sorting/greedy, prefix/map e heap/Top K. Pattern visibile nello studio, rimosso nelle prove a tempo. Simulazioni: 25 min longest-substring, 40 min coin-change, repository 60 e full mock 40+60 (three-sum/Parcel). Quest'ultimo è riservato al giorno 6.

Nove soluzioni algoritmiche sbagliate sono rifiutate: quadratica su input grande, duplicati, visited assente, boundary errato, heap invertito, greedy Coin Change, conteggi prefissi sovrascritti, identità confusa con valore e grafo restituito senza copia. I test dimostrano il comportamento sui casi eseguiti, non la complessità universale di ogni submission.

## Repository readiness

Due demo consentono scelta pragmatica Node/C++; poi il piano mantiene lo stack scelto. Lab intermedi: async/contratti Node oppure inventario/stato C++. Parcel richiede riparazioni in più file, senza soluzione inclusa nel workspace: lookup, filtri, 404/409, transizioni, evento singolo, retry idempotenti per parcel, conflitti e snapshot.

Entrambi gli starter falliscono; copie temporanee riparate passano. Il test Node corretto passa anche negando le API di rete. L'AI viene allenata come metodo: contesto README/file, chiarimenti, ipotesi e verifica; nessun servizio AI reale simulato.

## Six-day feasibility

Stime dai metadata, con pratica e 15 min carte + 20 min error review quotidiani; pause escluse. Giorno 6: altri 30 min behavior.

| Giorno | Core | Durata |
|---|---|---|
| 1 | Formato/metodo, confronto lingue, toolkit scelto, Big-O, array/hash, demo stack | 5h56–6h01 |
| 2 | Pointers/window/prefix/intervalli, pratica mista, sprint 25, lab scelto | 6h10–6h30 |
| 3 | Stack/deque/monotonic, search/confini/risposta, lab o riparazione autonoma | 6h05–6h10 |
| 4 | Liste/ciclo, alberi/BST, ricorsione, grid/grafi/componenti/toposort | 6h50 |
| 5 | Heap/greedy/backtracking/DP/Word Break, coding 40 | 6h40 |
| 6 | Test/debugging, AI, LP/behavior/style, full mock | 5h35 |

Core circa 37–38 ore, massimo conservativo 37,8. Con pause: giornate piene di circa 7–8 ore; per studio serale distribuire ogni giorno su più sessioni. Nessuna misura empirica sul candidato.

Core: ID del piano e ramo della lingua/stack scelti. Extra: toolkit non scelto, esercizi/lab fuori piano, altri scenari, LRU/Dijkstra/Word Ladder/Edit Distance/histogram. Carte essenziali: argomenti Core e sintassi propria lingua; utili/Extra: approfondimenti e altra lingua. Non aggiungere l'intera banca al carico Core.

Modifiche: lab anticipati ai giorni 2/3, toolkit separati, task ridondanti rimossi dal Core, BST/ciclo e greedy/Word Break aggiunti, recall quotidiano. Giorno 6 senza nuovi pattern DSA.

## Editorial quality

Riletto campione trasversale di formato/metodo, toolkit, HashMap, Sliding Window, ricerche/confini/risposta, liste, BFS/DFS/grafi, heap, DP, backtracking, stack choice, AI e behavior. Rivisti contratti/spiegazioni della banca, tutte le carte e i 36 scenari.

Lezioni concrete e navigabili, con esempi e collegamenti; il giorno è un piano sopra il curriculum. Ripetizione di mappe/invarianti/stato in contesti diversi. Tre carte duplicative sostituite; tracce aggiunte per DP/ricerca sulla risposta/backtracking; soluzioni impaginate e complessità di copie/sottostringhe corrette. In questa revisione, le prime lezioni aggiungono esempi svolti di scansione, confronto di complessità, compattazione in-place, Kadane e Two Sum; le versioni di codice Python e C++ seguono il selettore di lingua.

Due scenari poco pertinenti riscritti per payload incompleto e denominatori diversi. Alcune alternative deboli restano riconoscibili: formazione sui tradeoff, non replica della psicometria Amazon.

## Technical verification

- Suite finale: **94 passed, 4 skipped, 0 failed**, in 158,62 secondi; comando `.venv\Scripts\python.exe -m pytest -q -rs`. I quattro skip riguardano l'esecuzione UI dei laboratori React, non il track Amazon.
- Doctor: exit 0; tre cataloghi, scrittura e runner JavaScript/Python/C++20/C# verificati.
- Soluzioni: tutti gli 89 task Python e 89 C++ eseguiti; anche soluzioni degli altri percorsi.
- Runner: syntax/runtime error, risposte errate, timeout, limiti output e anomalie compilazione/esecuzione.
- Lab: failure iniziali e riparazioni reali, Parcel in entrambi gli stack.
- UI: tre track/Ctrl+T, persistenza/statistiche separate, editor/layout corto e largo, behavior, stack e timer sequenziali. Timer del mock avanza mentre il runner è occupato; risultato tardivo ignorato dopo cambio sezione.
- Coding simulation: starter fresco e traccia nascosta prestart, niente pausa/reset/cambio lingua dopo start, editor bloccato alla scadenza; test dedicato.
- Determinismo: due rigenerazioni consecutive hanno prodotto gli stessi JSON e 45 file lezione Amazon (46 artefatti totali). `tools/doctor.py` exit 0 sui tre cataloghi e runner Python, C++20, JavaScript e C#.
- Reset: il dashboard Amazon mostra già “Ricomincia il percorso” e richiede conferma. Il test dedicato verifica che vengano rimossi i progressi di entrambe le varianti linguistiche e che restino intatti gli altri percorsi, il linguaggio scelto e i file di laboratorio.
- Offline: materiali/runner/lab locali senza pacchetti applicativi da scaricare. Socket negati nel processo di verifica materiali e API Node negate nel lab. Non è isolamento di rete dell'intero OS o dei figli Python/C++.
- Batch Windows: verificato nella precedente fase da copia isolata con tre dashboard e chiusura exit 0; launcher invariato qui. Nuova UI verificata via Textual, installazione da zero non ripetuta.

## Ultime correzioni effettuate

Pattern/prompt prestart protetti; clock mock asincrono; simulazioni senza pausa/reset e senza risposta vecchia; scelta stack persistente; Parcel ampliato; ciclo lista e clone grafo; Coin Change/Three Sum edge case; overflow Missing Number C++; constraints espliciti; soluzioni impaginate e tokenizer corretto; complessità copie/substrings; tracce DP/backtracking/ricerca; carte/scenari corretti; piano Core/Extra/recall. Questa revisione aggiunge 22 esercizi Extended e una lezione Trie facoltativa, conserva tutti gli ID del piano Core, aggiorna la matrice benchmark e testa il reset del percorso.

## Limitazioni residue

Nessuna garanzia di esito Amazon; problemi/stack possono variare. Il mock fisso perde valore di prova mai vista dopo il primo tentativo. Soluzioni accessibili nei file: disciplina personale necessaria. Nessun proctoring, cloud IDE, IntelliSense o AI HackerRank riprodotto.

## Confronto con la versione precedente

Il percorso è cambiato rispetto alla prima pubblicazione: il commit `5240d9c` ha ampliato e riorganizzato la teoria Amazon in 46 file del track (4.392 inserimenti e 415 rimozioni), mantenendo però 44 lezioni e 67 esercizi. Anche gli snapshot dei commit successivi `fbc3090`, `4369190` e `a212166` conservavano quei conteggi; gli ultimi due non modificano file Amazon. Il catalogo corrente aggiunge contenuti, senza rimuovere il piano di studio: restano invariati i 44 ID di lezione pianificati.

Durate e difficoltà repo sono stime, non misure su candidati. Test ed editoriale non dimostrano assenza assoluta di bug. Clone Graph C++ affida la proprietà dei nodi copiati al chiamante: esempio algoritmico, non modello production di memory ownership.

Nessun commit, push o merge effettuato.

## Come iniziare

Apri Avvia DEV48.bat, scegli **3 — Amazon SDE-I OA Bootcamp**, parti dalla lezione **sde-l-oa-format** e segui il piano dashboard. Ctrl+K per ripassare direttamente una lezione.

Giorno 1: formato/metodo, mini-prova 8 min per lingua, scegli Python/C++, toolkit scelto, Big-O/array/hash, Two Sum/duplicati/anagrammi e due demo repo. Scegli lo stack dove navighi/correggi più autonomamente e mantienilo. 15 min carte e 20 error review.

Primo timed problem 25 min al giorno 2; coding 40 al giorno 5; full mock 40+60 al giorno 6. Conserva Three Sum/Parcel per quel tentativo. Core è il piano con i rami scelti; Extra può aspettare finché autonomia e recall Core sono stabili.
