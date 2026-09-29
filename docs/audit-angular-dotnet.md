# Revisione del percorso Angular & .NET

Revisione del 30 settembre 2026. Le modifiche sono nel worktree e non sono state committate o pubblicate.

## Analisi iniziale

La fonte editoriale è `tools/generate_dotnet_angular.py`: il catalogo e i Markdown sono generati da lì. Gli starter reali sono definiti in `dev48/lab_scaffolds.py`; `dev48/workspace.py` crea soltanto file mancanti. Sono stati esaminati README, catalogo, inventario di tutte le lezioni ed esercizi, criteri dei 12 laboratori, sessioni di pratica e relativi scaffold.

La lettura integrale del campione ha incluso primo metodo C#, setup, async/await, Minimal API, bootstrap Angular, Control Flow, Signals/RxJS, tracking EF Core, migrazioni, Reactive Forms, guard, JWT, interceptor, xUnit, TestBed, Clean Architecture e monorepo. Il controllo del percorso completo ha considerato la sequenza dei concetti e il rapporto tra consegne, esempi, soluzioni e controlli.

Da preservare: spiegazioni della sintassi, esempi piccoli, walkthrough specifici, casi limite, ID persistenti e laboratori con framework reali. La distinzione nel README tra compilazione C#, mock Angular, controllo strutturale e richiamo per termini è utile e onesta.

Problemi osservati prima degli interventi:

- Ogni lezione ripeteva consigli generici nelle sezioni iniziali, finali e di esercizio. Il test imponeva 500 parole anche per concetti piccoli.
- Gli esercizi di bootstrap e Control Flow usavano Signals e computed prima delle lezioni che li introducono.
- Il richiamo concettuale chiedeva sempre di spiegare il titolo; le flashcard riproponevano come esempio la prima riga del codice, spesso un import.
- Alcune pratiche avanzate allenavano abilità distanti dal titolo: estrarre un nome da un'email per JWT, confrontare due interi per xUnit, conservare una stringa per l'interceptor.
- La guida alla pratica anticipava spesso la soluzione; mancava una riduzione degli aiuti nella seconda parte del percorso.
- I controlli strutturali DTO non verificavano tutti i campi richiesti e alcuni controlli dipendevano dagli spazi intorno ai due punti.
- Gli starter offrivano parti già implementate, ma non indicavano con precisione cosa completare e cosa verificare manualmente. EF Core prometteva migrazioni senza fornire il pacchetto Design e il manifest del tool.
- L'ultima sessione era un colloquio. Alcune descrizioni dei lab promettevano bonus o l'uso obbligatorio di effect per dati derivati.
- Erano presenti indicazioni obsolete su allowSignalWrites, un'inizializzazione fragile di FormBuilder e affermazioni troppo assolute su tipi, asincronia e conservazione dei dati nelle migrazioni.

La priorità è stata eliminare il riempitivo, risolvere il salto sui Signals, collegare pratica e laboratori, e correggere i passaggi tecnici identificati. Non è stata necessaria una riscrittura completa.

## Modifiche realizzate

Tutte le 53 lezioni sono state rigenerate dal generatore. Sono state eliminate le istruzioni ripetitive su lettura, glossario, primo errore, controllo rapido e conclusione. Le spiegazioni specifiche, la sintassi, gli esempi e i walkthrough sono stati conservati. Nessuna lezione è stata eliminata o accorpata; sono state consolidate le indicazioni generiche.

Le introduzioni a signal e computed precedono ora il bootstrap e i relativi esercizi. Sono stati aggiunti richiami nominativi ai prerequisiti e collegamenti ai Markdown, istruzioni per eseguire il primo metodo e la prima API, motivi per scegliere DI e Clean Architecture, basi di Observable e HttpClient e passaggi verso il contesto dei soggetti nel gestionale. Le due lezioni facoltative e la panoramica Signal Forms sono indicate come approfondimenti.

I 53 richiami concettuali usano la domanda specifica della lezione. Le 53 risposte modello rispondono alla domanda specifica, con un esempio, un limite o un errore pertinente; le relative flashcard usano queste risposte anziché la prima riga del codice. Sono state eliminate anche formulazioni assolute come ‘infinitamente più sicuro’. Il controllo rimane dichiaratamente un controllo di termini: non assegna correttezza semantica a una risposta.

Nella seconda parte del corso non viene più mostrata sistematicamente la soluzione del piccolo esercizio nella lezione. Restano i riferimenti iniziali e gli esempi di progettazione utili di SOLID e Clean Architecture. La pratica combina completamento, implementazione, previsione del comportamento, debugging ed estensione nei laboratori.

Tre pratiche sono state modificate mantenendo gli ID:

- JWT: decisione 401/403/200 secondo identità e ruolo, con casi che distinguono autenticazione e autorizzazione.
- Interceptor: conservazione del token e selezione dell'header secondo l'origine; controlli su host esterno, porta diversa e token assente.
- xUnit: correzione di un difetto sul caso zero e traduzione dei casi in una Theory nel laboratorio. Il runner breve controlla il metodo, non esegue xUnit.

Sono stati rafforzati i controlli strutturali dei DTO e della busta generica, con tolleranza agli spazi. Le consegne chiariscono che non sostituiscono il compilatore TypeScript.

I 12 nuovi workspace ricevono istruzioni specifiche su file, sequenza di lavoro, parti già fornite, TODO e limiti delle suite. Per EF Core sono disponibili Design e un tool locale della stessa versione: creazione e applicazione di migrazioni sono separate dal test che usa EnsureCreated. Per il laboratorio di test i comandi non presumono un server API eseguibile.

Lo starter JWT conserva un TODO di emissione del token: è lavoro dello studente, ora indicato esplicitamente anche nei requisiti e nella guida. La lezione presenta il flusso completo da usare come riferimento. Il TODO dell'interceptor resta da completare; i test aggiungono URL relativo e token assente.

Le sessioni finali diventano pratica autonoma e revisione del progetto. L'ID storico contenente `interview` resta per compatibilità con i progressi; il titolo e l'attività non sono più un colloquio. Le durate sono riferimenti per organizzare lo studio.

## Correzioni tecniche e fonti

Le versioni restano Angular 22.2.0 e .NET/EF Core 10. Non è stata effettuata una migrazione di versione. La disponibilità dei pacchetti è stata controllata nei registri npm e NuGet; il requisito Node/TypeScript è stato confrontato con la [compatibilità Angular](https://angular.dev/reference/versions).

- `allowSignalWrites` non è più necessario: aggiornata la spiegazione secondo [CreateEffectOptions](https://angular.dev/api/core/CreateEffectOptions).
- Reactive Forms usa `inject(FormBuilder)` prima dell'inizializzazione e controlli non nullable; l'esempio non registra la password nei log. Conservato il confronto con [Signal Forms](https://angular.dev/guide/forms/signals/comparison).
- L'esempio RxJS include import, componente, richiesta tipizzata, parametri URL e gestione dell'errore dentro switchMap, che lascia attive le ricerche successive. Chiariti sottoscrizione e contesto di iniezione secondo la [guida all'interoperabilità](https://angular.dev/ecosystem/rxjs-interop).
- L'interceptor risolve URL relativi rispetto al documento, evitando di attribuire automaticamente all'API ogni URL relativo. La guard ha un servizio coerente e il confine di autorizzazione rimane sul server.
- Chiarito che i tipi TypeScript e il parametro generico di HttpClient non validano il JSON a runtime, come indicato nella [guida HttpClient](https://angular.dev/guide/http/making-requests).
- Distinti blocco del thread pool e deadlock dipendente dal contesto nell'uso di Result/Wait; riferimento: [buone pratiche ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0).
- Chiarito che una migrazione può eliminare dati. Aggiunti gli strumenti richiesti dalla [CLI EF Core](https://learn.microsoft.com/en-us/ef/core/cli/dotnet) e mantenuta la distinzione tra sviluppo locale e distribuzione descritta nella [guida alle migrazioni](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/).
- Aggiunti l'esempio mancante di switch nel template, una spiegazione delle lambda LINQ e le classi usate dagli esempi xUnit. Corretti anche dettagli HTML e un commento Include riferito alla risorsa sbagliata.

## Verifiche

- Rigenerazione deterministica su 54 artefatti e `git diff --check` senza errori.
- Rigenerazione riuscita: 53 lezioni, 106 esercizi, 159 flashcard, 12 laboratori e 4 sessioni.
- Confronto con HEAD: tutti gli ID delle cinque collezioni preservati. Cataloghi e lezioni degli altri percorsi non modificati.
- Test di catalogo: riferimenti, file referenziati, ordine Signals, struttura e walkthrough; tutti passati.
- Test degli starter: generazione dei 12 workspace e conservazione di codice e README personalizzati quando la creazione viene ripetuta; passati.
- Suite catalogo/database/runner: 46 test passati. Il test delle 106 soluzioni Angular/.NET è stato rieseguito dopo la modifica dei controlli strutturali ed è passato.
- Suite catalogo/TUI: 29 test passati; comprende nuovamente i 9 test di catalogo, quindi i conteggi non vanno sommati direttamente.
- Controllo DTO mirato: soluzione e formattazione alternativa accettate, campo price mancante rifiutato.
- In una copia temporanea del laboratorio Angular JWT: starter con un test fallito per il TODO; dopo completamento, 5 test passati e build Angular riuscita. Nella stessa build sono stati inclusi gli esempi aggiornati Reactive Forms, Signal Forms, RxJS e guard.
- In una copia temporanea del backend JWT: tre test falliti per il 501 intenzionale; dopo completamento dell'emissione, 5 test xUnit passati, compresi 401/403/200.
- In una copia temporanea EF Core: tool restore, restore, creazione InitialSubjects e database update riusciti con SQLite.

Non sono stati installati pacchetti nei workspace personali, modificati i progressi o eseguiti commit/push.

## Limiti residui

I richiami teorici controllano termini, i DTO brevi hanno controlli strutturali e i mock Angular non verificano DOM o runtime Angular: rimangono attività preparatorie. Alcuni esercizi brevi, per esempio nomi delle migrazioni e formattazione OpenAPI, allenano una parte limitata del tema; la competenza completa richiede il laboratorio.

Le suite iniziali dei laboratori non coprono ogni requisito: migrazioni, CRUD completo dalla UI, accessibilità e integrazione tra due processi richiedono verifiche aggiuntive. Le nuove guide indicano queste differenze. Non sono stati completati tutti i 12 progetti finali né eseguito un collaudo manuale end-to-end nel browser; i risultati riportati sono compilazioni, test automatici e verifiche delle migrazioni.

Le guide aggiornate sono create nei nuovi workspace. I README già presenti vengono conservati per proteggere gli appunti dello studente; le lezioni rigenerate e il catalogo aggiornato sono disponibili nel percorso dell'app.
