# Revisione JavaScript & React Academy

Audit avviato il 30 settembre 2026. Nessun commit o push richiesto.

## Cosa preservare

La progressione copre già valori, funzioni, collezioni, copie, errori, asincronia,
HTML e React prima delle estensioni backend e database. Il contesto dell'archivio
soggetti collega bene trasformazioni dei dati e interazioni UI. Le unità brevi,
le flashcard e la separazione del progresso tra percorsi rendono il materiale
ripassabile. Non servono nuove lezioni o una migrazione di framework.

Il catalogo iniziale contiene 50 lezioni, 100 esercizi, 12 laboratori,
150 flashcard e quattro sessioni. Gli ID fanno parte della persistenza:
rimangono invariati anche quando cambia l'ordine di lettura.

## Problemi osservati prima degli interventi

- `code_task` assegnava gli esercizi JavaScript usando l'indice globale:
  Valori e tipi riceveva `fullName`, mentre la closure riceveva `activeNames`.
  Le lezioni di orientamento spostavano di due posizioni tutti gli esercizi.
- Closure precedeva la prima spiegazione delle funzioni; import/export era
  facoltativo benché necessario per i componenti dei progetti React.
- Le nove pratiche React ripetevano la stessa lista tipizzata da eliminare,
  richiedendo stato anche dove bastavano props e composizione. HTML e
  TypeScript riutilizzavano anch'essi una consegna comune per temi diversi.
- Gli esempi di effect e form chiamavano funzioni non definite (`load`,
  `handleSubmit`) senza spiegare il contratto. La spiegazione dell'annullamento
  non dimostrava come evitare risposte fuori ordine.
- Il type guard per JSON verificava la presenza dei campi ma prometteva
  tipi che non controllava. La validazione numerica accettava stringhe vuote
  e assenze convertendole a zero.
- La seconda flashcard di ogni lezione dava indicazioni su come rispondere,
  anziché rispondere alla domanda. Richiami e pratica teorica attribuivano
  XP tramite sola presenza di parole, senza verifica del significato.
- Le sezioni «Perché è utile», checklist e conclusione erano ripetute
  quasi identiche per tutte le lezioni. Alcune istruzioni non corrispondevano
  all'esempio: la transazione invitava a leggere FROM e JOIN.
- Tutti i laboratori non React ricevevano il medesimo `solve(input)` per
  filtrare gli attivi; quelli React lo stesso archivio con eliminazione.
  I test non coprivano i rispettivi brief di CRUD, form, fetch, SQL e Git.
- La stima di 12–16 ore non corrispondeva alle durate: circa 36,3 ore
  di lezioni e 72,7 ore includendo esercizi, laboratori e sessioni iniziali.

## Priorità e fonti editoriali

Prima allineare spiegazioni, esempi e pratica; poi dare a ogni laboratorio
un contratto e test pertinenti. Conservare le trasformazioni immutabili
quando ricompaiono in React: il nuovo contesto aggiunge rendering ed eventi.
Rimuovere invece le consegne identiche che non allenano il tema della lezione.

`tools/generate_content.py` resta l'entry point che genera catalogo e Markdown.
I testi specifici sono raccolti in `tools/js_react_notes.py`, le pratiche in
`tools/js_react_practice.py`, i brief in `tools/js_react_lab_briefs.py`.
Gli output sotto `content/` non sono mantenuti manualmente.

Fonti ufficiali consultate per gli interventi:

- [MDN: closure](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)
- [MDN: moduli](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
- [MDN: fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [React: snapshot dello stato](https://react.dev/learn/state-as-a-snapshot)
- [React: calcoli ed eventi senza effect](https://react.dev/learn/you-might-not-need-an-effect)
- [React: dipendenze, cleanup e caricamento](https://react.dev/reference/react/useEffect)
- [React: identità e conservazione dello stato](https://react.dev/learn/preserving-and-resetting-state)
- [React: hook personalizzati](https://react.dev/learn/reusing-logic-with-custom-hooks)

## Modifiche realizzate

Il generatore ora collega la pratica al tema della lezione, anziché alla sua
posizione globale. Le funzioni precedono la closure; import/export è un
prerequisito essenziale. TypeScript, routing e le estensioni WordPress,
Electron e architettura AI sono riconoscibili come approfondimenti. React
usa JSX senza richiedere prima TypeScript. Non sono state aggiunte lezioni:
rimangono 50 lezioni, 100 esercizi, 12 laboratori, 150 flashcard e quattro
sessioni, con gli stessi ID in tutte e cinque le raccolte.

Le spiegazioni JavaScript e React seguono esempi completi e ne illustrano
il comportamento: contatori indipendenti tramite closure, copie annidate,
callback, Promise, errori HTTP, snapshot dello stato, aggiornamenti
funzionali, identità delle key, form controllati e dati derivati.
Gli effetti distinguono sincronizzazione esterna, calcoli nel rendering
e azioni negli eventi. Le richieste concorrenti mostrano abort e risultati
ignorati dopo la cleanup. Hook personalizzati, context e reducer vengono
presentati quando risolvono un bisogno, senza renderli obbligatori.
I prerequisiti specifici rimandano alle lezioni da ripassare.

Sono state eliminate le introduzioni, checklist e conclusioni identiche
per modulo. Sono rimaste le ripetizioni che cambiano contesto: l'immutabilità
prima nelle funzioni JavaScript e poi negli aggiornamenti React; errori e
validazione prima al confine HTTP e poi nel form e nel caricamento UI.
Flashcard e soluzioni di richiamo rispondono davvero alla domanda.
Le risposte concettuali richiedono confronto manuale e non assegnano nuovo
XP per la presenza di parole. L'XP storico non viene ricalcolato.
La stima ora distingue 29,9 ore di lezioni essenziali e 36,3 ore complessive,
con la pratica esclusa dal conteggio.

## Pratica e autonomia

Ogni laboratorio ha starter, soluzione e test propri. Il contesto dell'archivio
soggetti collega CRUD JavaScript, lista React, form, API e mini gestionale.
Gli aiuti passano dal completamento mirato di funzioni e componenti alla
diagnosi di più moduli e alla progettazione autonoma del laboratorio finale.
Il server HTTP locale e le fixture sono forniti per concentrare il lavoro
su UI, errori e integrazione, senza introdurre altre dipendenze.

| Laboratorio | Comportamento verificato |
| --- | --- |
| CRUD JavaScript | Aggiunta, modifica, eliminazione, ricerca, riepilogo e dati originali immutati |
| Bug JavaScript | Sei difetti distinti, incluse copie annidate e validazione numerica |
| Fetch | Loading, empty, error, retry, HTTP, JSON, cancellazione e risposte fuori ordine |
| Dashboard HTML | Struttura semantica; layout e tastiera verificati separatamente nel browser |
| TypeScript | Guardie runtime e stati discriminati con tipi cancellabili da Node |
| Lista React | Ricerca, eliminazione per ID, conteggio e due casi vuoti |
| Form React | Creazione, modifica, annullamento, validazione associata al campo e immutabilità |
| CRUD React/API | Trasporto HTTP, caricamento, errori, retry, concorrenza e blocco dell'invio duplicato |
| SQL | SQLite reale: vincoli, query, soggetti senza misure e rollback dopo un errore |
| Git | Repository temporanea, conflitto reale, merge e due intenzioni conservate |
| Debug applicazione | Riparazione coordinata di repository, servizio e formattazione |
| Mini gestionale | Integrazione autonoma e riepilogo derivato dai risultati correnti |

Il runner JavaScript attende ora anche il risultato delle Promise. I test
di regressione rifiutano soluzioni scorrette per mutazione, contatori globali,
coercizione, errori asincroni ignorati e type guard che promettono tipi
non verificati. I controlli brevi JSX dichiarano esplicitamente di verificare
struttura e testo; gli eventi si provano nei laboratori React.

## Versioni e fonti

La verifica è stata eseguita con Node 24.19.0 e npm 11.15.0. Sono state
conservate le dipendenze già fissate dal progetto: React/React DOM 19.2.8,
Vite 8.2.1, plugin React 6.0.5, Vitest 4.1.10, jsdom 29.1.1,
Testing Library React 16.3.2 e jest-dom 7.0.0. Nessuna libreria di stato,
router aggiuntivo, Next.js o migrazione di framework. Il filtro semplice
non richiede memoizzazione preventiva. Le fonti React/MDN sopra hanno
guidato le correzioni del modello mentale e dei confini asincroni.

La [documentazione Node sul TypeScript](https://nodejs.org/docs/latest-v24.x/api/typescript.html)
conferma che l'esecuzione con rimozione dei tipi non svolge il controllo
statico e non legge tsconfig. Il laboratorio lo dichiara nel proprio README.
L'installazione di prova delle dipendenze è rimasta in una cartella temporanea.

## Verifiche eseguite

- Suite completa: **95 test passati, nessuno saltato**, con
  `DEV48_REACT_NODE_MODULES` impostata alla toolchain del laboratorio temporaneo.
  Include tutte le 100 soluzioni brevi del percorso e le regressioni degli
  altri percorsi. Un test TUI che cercava una domanda `short` è stato adeguato
  alla pratica `reflection`, conservando la verifica dell'editor semplice.
- Tutti i 12 starter falliscono i test pertinenti e le 12 soluzioni di
  riferimento li passano, in cartelle temporanee. Le quattro suite React
  eseguono rispettivamente 4, 4, 9 e 11 test; tutte le quattro build Vite
  sono riuscite. SQL usa SQLite e Git una repository didattica senza remote.
- Diagnostica `tools/doctor.py`: riuscita per tutti i cataloghi e per i
  runner JavaScript, Python, C++20 e C# disponibili.
- Rigenerazione ripetuta: **51 file identici** tra due esecuzioni. Tutti gli
  ID conservati; catalogo Angular/.NET identico alla copia iniziale.
  `git diff --check` riuscito.
- Browser Edge tramite Playwright sulle soluzioni temporanee: ricerca
  normalizzata, eliminazione del solo elemento scelto, invio con Invio,
  nome vuoto e correzione, creazione/modifica, conservazione degli altri campi,
  CRUD con HTTP reale, risultato vuoto, rete offline, errore visibile e
  retry dopo il ripristino della rete. Nel finale: annullamento della
  modifica e riepilogo coerente con il filtro.
- Verifica visiva di lista/form desktop, finale a 320 px, dashboard HTML
  a 320/768/1280 px. Nessuno scorrimento orizzontale a 320 px; focus
  visibile e ordine Tab tra navigazione, ricerca e pulsante nella dashboard.
  Snapshot e screenshot sono conservati fuori dalla repository nella
  cartella visualizzazioni della sessione.
- Console: nessun errore applicativo durante il flusso normale. È presente
  il solo 404 della favicon non fornita; la prova offline genera l'errore
  di rete atteso, recuperato con retry. Nessun overlay Vite residuo.

## Preservazione e limiti

Sono stati ricontrollati i 17 file dei workspace personali presenti
all'inizio: tutti identici. I vecchi progetti vengono lasciati integralmente
intatti, compresi i test; gli starter rivisti si applicano alle cartelle
nuove. La suite verifica anche che la riapertura di un progetto già
modificato non riscriva i file dello studente. Non sono state eseguite
migrazioni, cancellazioni o ricalcoli del database personale. L'app era
attiva durante il lavoro: lock, WAL e backup runtime possono cambiare
per la sessione di studio, quindi non si dichiara identità byte per byte
di quei file.

Le modifiche concorrenti a TUI e contenuti Amazon già presenti nel working
tree sono state conservate. Questa revisione non modifica il generatore
Amazon o i relativi contenuti; nel test TUI condiviso è stata cambiata
soltanto la selezione della domanda JavaScript/React.
Nessun commit o push.

Restano limiti dichiarati: le risposte riflessive non sono corrette
semanticamente in automatico; i controlli brevi HTML/JSX sono strutturali;
Node rimuove i tipi senza sostituire `tsc`; jsdom non certifica layout o
accessibilità completa. La dashboard HTML è statica e non simula un filtro
funzionante. Il server didattico conserva i dati solo fino al riavvio e
non implementa autenticazione o distribuzione. Non sono stati provati
screen reader, zoom browser al 200%, altri browser o tutte le combinazioni
di viewport. Gli esempi delle lezioni sono stati rivisti; l'esecuzione
automatica riguarda soluzioni degli esercizi e laboratori, non ogni snippet
isolato. I test coprono i casi dichiarati, non garantiscono ogni input.
