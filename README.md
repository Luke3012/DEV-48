# DEV//48 — Enterprise Web & Software Academy

DEV//48 è una piattaforma di studio in italiano per lo sviluppo web e software. L'interfaccia è una TUI Python/Textual pensata per PowerShell; codice, test e laboratori restano file normali sul computer.

La piattaforma contiene tre percorsi, selezionabili all'avvio o con `Ctrl+T` da qualsiasi schermata non bloccata dal Full Mock:

1. **Angular & .NET Enterprise Academy:** basi di C#, TypeScript, HTML e CSS, poi ASP.NET Core Minimal API, Entity Framework Core, Angular 22 Standalone, Signals e Control Flow, fino ai laboratori full-stack (`client/` + `server/`).
2. **JavaScript & React Academy:** JavaScript da zero, React 19, Node.js, Express, SQLite e test con Vitest.
3. **Amazon SDE-I OA Bootcamp:** piano essenziale di sei giorni, 44 lezioni distinte e navigabili, 67 esercizi DSA con varianti Python e C++ (22 Easy, 35 Medium, 10 Hard), sei repository lab, 160 flashcard, quattro simulazioni, 36 scenari Work Simulation e otto prompt Work Style.

Ogni percorso mantiene catalogo e progresso separati. Alla prima schermata scegli `1`, `2` o `3`; anche le frecce e Invio funzionano. `Ctrl+T` riapre la selezione. Il piano essenziale Amazon distribuisce tutte le lezioni e attività scelte in circa 34 ore e mezza; il catalogo completo dichiara circa 54,7 ore includendo anche esercizi, laboratori e simulazioni facoltativi. Gli scenari singoli non hanno una durata predefinita.

Il bootcamp include simulazioni da 25, 40 e 60 minuti e un mock sequenziale da 40 minuti di coding più 60 minuti su una repository. I due timer sono indipendenti: il tempo inutilizzato non passa alla sezione successiva. È un formato di pratica richiesto; ruolo, paese e invito ricevuto determinano il processo Amazon effettivo.

## Sistema di Valutazione Intelligente e Creatività

Le verifiche dichiarano che cosa controllano:
- **C#:** il codice dell'esercizio viene compilato con il .NET SDK e verificato sui casi di input/output indicati.
- **TypeScript e Angular:** gli esercizi brevi controllano sintassi eseguibile e casi di logica isolati. Per Angular il runner usa piccoli mock di Signals: non avvia Angular, non compila i template, non esegue `tsc` e non controlla il DOM.
- **HTML/CSS:** i controlli verificano struttura e requisiti testuali; non effettuano rendering nel browser.
- **Richiami teorici:** il controllo automatico verifica soltanto la presenza dei termini mostrati nel prompt. Non interpreta il significato: confronta sempre la risposta con il modello.
- **Laboratori:** vengono eseguiti i test xUnit e Angular presenti nel workspace. I test verdi verificano quei comportamenti; usa anche i criteri del README del laboratorio per valutare sicurezza, accessibilità, documentazione e requisiti non coperti.

Le estensioni creative sono facoltative e non assegnano XP automatici.

## Anteprima

### Dashboard e percorso guidato

![Dashboard di DEV48 con progresso, statistiche e accesso rapido alle attività](docs/screenshots/dashboard.png)

### Esercizi interattivi

![Editor integrato di un esercizio con indizi, soluzione e navigazione guidata](docs/screenshots/exercise-editor.png)

### Flashcard

| Domanda | Risposta |
|---|---|
| ![Flashcard prima di mostrare la risposta](docs/screenshots/flashcard-question.png) | ![Flashcard con la risposta visualizzata](docs/screenshots/flashcard-answer.png) |

### Laboratori e curriculum

| Laboratori pratici | Curriculum ricercabile |
|---|---|
| ![Elenco dei laboratori pratici disponibili](docs/screenshots/labs.png) | ![Curriculum completo con lezioni, moduli e stato](docs/screenshots/curriculum.png) |

## Avvio rapido

1. Fai doppio clic su **`Avvia DEV48.bat`**.
2. Solo al primo avvio attendi la creazione di `.venv` e l'installazione delle dipendenze Python.
3. Scegli `1`, `2` o `3` nella schermata iniziale. Usa **`Ctrl+T`** per tornare al selettore dei tre percorsi.

Requisiti di sistema: Windows 10/11, Python 3.11+, .NET SDK 10 e Node.js. Per Angular 22 usa Node.js `22.22.3` o superiore nella linea 22, `24.15.0` o superiore nella linea 24, oppure la linea 26 supportata. Git e VS Code sono raccomandati per i laboratori. Esegui **`Diagnostica DEV48.bat`** per verificare automaticamente l'ambiente locale. Vedi la [tabella ufficiale di compatibilità Angular](https://angular.dev/reference/versions) e il [ciclo di supporto .NET](https://learn.microsoft.com/dotnet/core/releases-and-support).

Avvio equivalente da PowerShell:

```powershell
cd "C:\percorso\DEV48"
.\.venv\Scripts\python.exe -m dev48
```

## Comandi dell'interfaccia

| Tasto | Azione |
|---|---|
| Frecce | Navigano subito nella schermata: selezione nelle tabelle, scorrimento nei testi, cursore nell'editor e cambio flashcard |
| `Invio` | Apre la voce selezionata / continua |
| `Ctrl+T` | Apre il selettore dei tre percorsi, tranne durante il Full Mock bloccato |
| `Ctrl+S` | Salva la risposta o completa una lezione |
| `F5` | Esegue l'esercizio corrente nel runner dedicato |
| `F1` | Alterna traccia dell'esercizio e teoria della lezione, conservando risposta e posizione di lettura |
| `H` | Mostra l'indizio successivo |
| `Esc` | Torna alla schermata precedente |
| `Ctrl+K` | Apre il curriculum |
| `Ctrl+G` | Apre il glossario |
| `Ctrl+D` | Torna alla dashboard |
| `Ctrl+Q` | Chiude salvando il progresso |
| `Spazio` | Gira una flashcard / avvia o mette in pausa un timer |
| `/` | Porta il focus alla ricerca in curriculum e glossario |

La soluzione completa di un esercizio breve si sblocca dopo due tentativi falliti. Quando consulti la teoria con `F1`, l'editor e la posizione di lettura restano nella schermata dell'esercizio.

## Amazon SDE-I OA Bootcamp

Il piano Core distribuisce la scelta del linguaggio e le due demo repository nel Giorno 1; pattern lineari e primo sprint da 25 minuti nel Giorno 2; stack/ricerca e lab intermedio nel Giorno 3; liste, alberi e grafi nel Giorno 4; heap, greedy, backtracking, DP e coding da 40 minuti nel Giorno 5; debugging, behavioral e Full Mock nel Giorno 6. Dopo il confronto, usa un linguaggio DSA e uno stack repository: il piano cambia con le scelte salvate. I lab demo hanno il pulsante **USA QUESTO STACK**; il mock finale offre Node.js e C++.

Il Core richiede circa 5h56–6h01, 6h10–6h30, 6h05–6h10, 6h50, 6h40 e 5h35 al giorno, includendo 15 minuti di flashcard e 20 di error review quotidiani, senza pause. Gli esercizi fuori dal piano e lo stack non scelto sono Extra. Le 67 famiglie di problemi hanno varianti Python/C++ e sono 21 Easy, 34 Medium e 10 Hard; i sei lab logici includono due implementazioni del mock finale.

I sei repository lab passano da due demo equivalenti C++ e Node.js a Promise/controller, inventario C++, contratto API sugli ordini e mock finale con sei famiglie di difetti fra route, service e repository. Il mock finale non indica i file da correggere. La demo HackerRank può offrire anche Django e Spring Boot; il bootcamp fornisce pratica eseguibile in C++ e Node.js e non presume che l'esame riusi la stessa repository. Node usa `npm test`; C++ richiede GCC o Clang con C++20. La diagnostica rileva il compilatore, che resta facoltativo per gli altri contenuti.

Le simulazioni coding e repository hanno timer indipendenti e non mostrano indizi o soluzioni durante il tentativo. La Full Mock pratica passa dal coding di 40 minuti al repository di 60 minuti e poi mostra il riepilogo. I 36 scenari Work Simulation e le otto domande Work Style offrono feedback formativo, non un punteggio di selezione o una previsione dell'esito di candidatura.

## Laboratori

Dalla scheda di un laboratorio:

1. premi **Apri VS Code** per creare e aprire lo starter project;
2. premi **Installa dipendenze** per ripristinare i pacchetti .NET e Angular/Node necessari;
3. modifica i file nella cartella `workspace/<id-lab>`;
4. premi **Esegui test** nell'app oppure usa il comando indicato nel README del laboratorio, fra cui `dotnet test Tests/Server.Tests.csproj`, `npm test` o la suite C++20.

DEV//48 crea solo i file mancanti. Il vecchio starter simulato viene conservato in cartelle `*-legacy` quando viene sostituito con un progetto Angular CLI o .NET reale. I laboratori Angular usano Angular CLI 22, Vitest e TestBed; quelli .NET usano .NET 10 e xUnit. I repository del bootcamp usano Node.js integrato o compilazione C++20 senza dipendenze scaricate. Le versioni dei pacchetti sono definite nei file `package.json` e `.csproj` del laboratorio.

## Salvataggio, backup e privacy

- Il progresso è salvato subito in `data/progress.sqlite3`.
- L'ultima posizione, risposte, tentativi, XP, indizi e tempo vengono ripristinati alla riapertura.
- `data/backups/progress_latest.json` è un backup leggibile aggiornato dopo i risultati e alla chiusura.
- `data/.dev48.lock` impedisce due istanze contemporanee. Un lock lasciato da una chiusura forzata viene riconosciuto e sostituito automaticamente al prossimo avvio.
- Non esistono account, telemetria, cloud o invii remoti dei contenuti.

Per conservare uno snapshot personale basta copiare `data/progress.sqlite3` e `data/backups/progress_latest.json` mentre l'app è chiusa. Per ricominciare senza perdere i dati, chiudi DEV//48 e **rinomina** `progress.sqlite3`, per esempio in `progress-precedente.sqlite3`; al nuovo avvio verrà creato un database vuoto.

## Come vengono corretti gli esercizi

- **JavaScript e Python:** Node o Python vengono avviati in una cartella temporanea con timeout e output limitato; i problemi Amazon eseguono i casi comportamentali dichiarati per il linguaggio selezionato.
- **C++:** gli esercizi Amazon vengono compilati come C++20 con GCC o Clang, poi eseguiti con timeout e limite di output. Senza compilatore, il runner riporta che C++ non è disponibile.
- **C#:** il codice viene compilato dal .NET SDK 10 in un progetto temporaneo.
- **TypeScript e Angular brevi:** Node rimuove i tipi e controlla il modello di logica. Il controllo non sostituisce il compilatore TypeScript né il runtime Angular.
- **SQL:** le query girano su un database SQLite temporaneo ricreato per ogni prova.
- **HTML/CSS e React breve:** vengono controllati struttura e requisiti mirati.
- **Richiami teorici:** checklist trasparente dei termini richiesti e confronto con risposta modello.
- **Laboratori .NET/Angular:** xUnit e il test runner Angular eseguono le suite presenti nei rispettivi workspace.

Il runner impone timeout e limite di output, ma non è una sandbox del sistema operativo: il codice può accedere ai file e alla rete con i permessi del tuo account. Il codice scritto nell'editor viene eseguito localmente.

## Mappa dei file

| Percorso | A cosa serve | Si può modificare? |
|---|---|---|
| `Avvia DEV48.bat` | Primo setup e avvio normale | Meglio di no |
| `Diagnostica DEV48.bat` | Controlla ambiente, catalogo, scrittura e runner Node | Sì, non necessario |
| `README.md` | Questo manuale | Sì |
| `requirements.txt` | Dipendenze Python minime | Solo per manutenzione |
| `pyproject.toml` | Metadati Python e configurazione pytest | Solo per manutenzione |
| `dev48/__main__.py` | Entry point di `python -m dev48` | Solo per sviluppo |
| `dev48/app.py` | Schermate, navigazione e comandi Textual | Solo per sviluppo |
| `dev48/styles.tcss` | Tema graphite/ciano/viola | Sì, per personalizzare il tema |
| `dev48/models.py` | Modelli e validazione del catalogo | Solo per sviluppo |
| `dev48/database.py` | SQLite, backup e blocco seconda istanza | Solo per sviluppo |
| `dev48/runners.py` | Correttori JavaScript, SQL, HTML, React e lab | Solo per sviluppo |
| `dev48/workspace.py` | Creazione starter project, npm e apertura VS Code | Solo per sviluppo |
| `content/catalog.json` | Manifest del percorso JavaScript & React | Non modificare a mano |
| `content/catalog_dotnet_angular.json`, `content/catalog_amazon_sde.json` | Manifest dei relativi percorsi | Non modificare a mano |
| `content/lessons/*.md`, `content/lessons_dotnet/*.md`, `content/lessons_amazon/*.md` | Testi delle lezioni | Sì, con cautela |
| `tools/generate_content.py`, `tools/generate_dotnet_angular.py`, `tools/generate_amazon_sde.py` | Sorgenti editoriali che rigenerano i cataloghi | Solo per manutenzione |
| `tools/doctor.py` | Diagnostica richiamata dal file `.bat` | Solo per sviluppo |
| `tests/` | Test automatici del catalogo, DB, runner e TUI | Sì, per sviluppo |
| `data/` | Stato personale e backup, creati a runtime | Non mentre l'app è aperta |
| `workspace/` | Codice modificabile dei laboratori e repository di pratica | **Sì: è il tuo lavoro** |
| `.venv/` | Ambiente Python isolato, ricreabile | Non modificare |

Attenzione: i due generatori riscrivono il relativo catalogo e i Markdown generati. Falli soltanto se stai mantenendo il contenuto editoriale.

## Diagnostica e test

In caso di dubbio esegui **`Diagnostica DEV48.bat`**. Verifica Python, Textual, Node/npm, tutti i cataloghi, permessi di scrittura e runner disponibili; Git, VS Code e il compilatore C++ vengono segnalati come opzionali.

Suite completa per chi modifica il programma:

```powershell
cd "C:\percorso\DEV48"
.\.venv\Scripts\python.exe -m pytest -q
```

La suite esegue le 65 soluzioni di riferimento Python del bootcamp contro i rispettivi casi; quelle C++ vengono compilate e verificate quando GCC o Clang è installato. Include anche test per sintassi e runtime errati, risposte sbagliate, timeout, output e compilazione C++ facoltativa.

## Risoluzione dei problemi

**La finestra dice che Python non è trovato.** Installa Python 3.11+ da python.org, seleziona “Add Python to PATH”, chiudi e riapri PowerShell.

**Il primo setup si è interrotto.** Controlla la connessione, chiudi DEV//48 e rilancia `Avvia DEV48.bat`. Se `.venv` esiste ma Textual manca, il launcher completa automaticamente l'installazione.

**Node o npm non sono trovati.** Reinstalla Node.js LTS includendo npm, poi riapri PowerShell e lancia la diagnostica.

**VS Code non si apre.** In VS Code esegui dalla Command Palette “Shell Command: Install 'code' command in PATH”, oppure apri manualmente la cartella indicata nella scheda del lab.

**Un laboratorio React non parte.** Dalla cartella del lab esegui `npm install`, poi `npm test -- --run`. Se l'installazione è stata interrotta, ripetila; `package-lock.json` manterrà le versioni risolte.

**L'app afferma di essere già aperta.** Cerca prima un'altra finestra DEV//48. Se non esiste, rilancia: i lock dei processi terminati vengono ripuliti automaticamente. Non cancellare il lock mentre un'altra istanza è attiva.

**Il servizio di sincronizzazione cloud mostra un conflitto.** Chiudi l'app, attendi la fine della sincronizzazione e riaprila. Non usare la stessa cartella simultaneamente da due computer.

**Il terminale è troppo piccolo o i simboli sono strani.** Allarga PowerShell almeno a circa 110×35 caratteri e usa Windows Terminal o PowerShell con un font Unicode moderno.

## Aggiornamento controllato

Per riallineare le dipendenze Python dichiarate:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Non è necessario aggiornare i pacchetti durante una sessione di studio: l'ambiente già verificato è più prevedibile.
