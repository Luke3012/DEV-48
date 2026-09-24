# DEV//48 — Enterprise Web & Software Academy

DEV//48 è una piattaforma di studio in italiano per lo sviluppo web e software. L'interfaccia è una TUI Python/Textual pensata per PowerShell; codice, test e laboratori restano file normali sul computer.

La piattaforma supporta ora **due percorsi completi da zero**, commutabili all'istante con `Ctrl+T`:
1. **Angular & .NET Enterprise Academy:** basi di C#, TypeScript, HTML e CSS, poi ASP.NET Core Minimal API, Entity Framework Core, Angular 22 Standalone, Signals e Control Flow, fino ai laboratori full-stack (`client/` + `server/`).
2. **JavaScript & React Academy:** JavaScript da zero, React 19, Node.js, Express, SQLite e test con Vitest.

Ciascun percorso include **50 lezioni**, **100 esercizi interattivi**, **12 laboratori**, **150 flashcard** e **4 sfide/simulazioni**. Il percorso Angular & .NET include inoltre **3 lezioni di fondamenti**: in totale sono 53 lezioni, 106 esercizi e 159 flashcard.

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
3. Al primo avvio scegli **Inizia il percorso**. Usa **`Ctrl+T`** in qualsiasi momento per cambiare tra il percorso Angular & .NET e il percorso JS & React: la dashboard mostrerà solo i contenuti dello stack attivo senza alcun sovraccarico visivo.

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
| `Ctrl+T` | **Cambia traccia attiva** (Angular & .NET ⇄ JS & React) |
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

## Laboratori

Dalla scheda di un laboratorio:

1. premi **Apri VS Code** per creare e aprire lo starter project;
2. premi **Installa dipendenze** per ripristinare i pacchetti .NET e Angular/Node necessari;
3. modifica i file nella cartella `workspace/<id-lab>`;
4. premi **Esegui test** nell'app oppure esegui `dotnet test Tests/Server.Tests.csproj` da `server/` e `npm test` da `client/`.

DEV//48 crea solo i file mancanti. Il vecchio starter simulato viene conservato in cartelle `*-legacy` quando viene sostituito con un progetto Angular CLI o .NET reale. I laboratori Angular usano Angular CLI 22, Vitest e TestBed; i laboratori .NET usano .NET 10 e xUnit. Le versioni dei pacchetti sono definite nei file `package.json` e `.csproj` del laboratorio.

## Salvataggio, backup e privacy

- Il progresso è salvato subito in `data/progress.sqlite3`.
- L'ultima posizione, risposte, tentativi, XP, indizi e tempo vengono ripristinati alla riapertura.
- `data/backups/progress_latest.json` è un backup leggibile aggiornato dopo i risultati e alla chiusura.
- `data/.dev48.lock` impedisce due istanze contemporanee. Un lock lasciato da una chiusura forzata viene riconosciuto e sostituito automaticamente al prossimo avvio.
- Non esistono account, telemetria, cloud o invii remoti dei contenuti.

Per conservare uno snapshot personale basta copiare `data/progress.sqlite3` e `data/backups/progress_latest.json` mentre l'app è chiusa. Per ricominciare senza perdere i dati, chiudi DEV//48 e **rinomina** `progress.sqlite3`, per esempio in `progress-precedente.sqlite3`; al nuovo avvio verrà creato un database vuoto.

## Come vengono corretti gli esercizi

- **JavaScript:** Node viene avviato in una cartella temporanea, con timeout di 5 secondi e output limitato.
- **C#:** il codice viene compilato dal .NET SDK 10 in un progetto temporaneo.
- **TypeScript e Angular brevi:** Node rimuove i tipi e controlla il modello di logica. Il controllo non sostituisce il compilatore TypeScript né il runtime Angular.
- **SQL:** le query girano su un database SQLite temporaneo ricreato per ogni prova.
- **HTML/CSS e React breve:** vengono controllati struttura e requisiti mirati.
- **Richiami teorici:** checklist trasparente dei termini richiesti e confronto con risposta modello.
- **Laboratori .NET/Angular:** xUnit e il test runner Angular eseguono le suite presenti nei rispettivi workspace.

Il codice scritto nell'editor viene eseguito localmente sul computer. Usa il runner solo per gli esercizi del corso e per codice di cui conosci la provenienza.

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
| `content/catalog_dotnet_angular.json` | Manifest del percorso Angular & .NET | Non modificare a mano |
| `content/lessons/*.md`, `content/lessons_dotnet/*.md` | Testi completi delle lezioni dei due percorsi | Sì, con cautela |
| `tools/generate_content.py`, `tools/generate_dotnet_angular.py` | Sorgenti editoriali che rigenerano i cataloghi | Solo per manutenzione |
| `tools/doctor.py` | Diagnostica richiamata dal file `.bat` | Solo per sviluppo |
| `tests/` | Test automatici del catalogo, DB, runner e TUI | Sì, per sviluppo |
| `data/` | Stato personale e backup, creati a runtime | Non mentre l'app è aperta |
| `workspace/` | Codice modificabile dei 12 laboratori | **Sì: è il tuo lavoro** |
| `.venv/` | Ambiente Python isolato, ricreabile | Non modificare |

Attenzione: i due generatori riscrivono il relativo catalogo e i Markdown generati. Falli soltanto se stai mantenendo il contenuto editoriale.

## Diagnostica e test

In caso di dubbio esegui **`Diagnostica DEV48.bat`**. Verifica Python, Textual, Node/npm, catalogo, permessi di scrittura e un'esecuzione JavaScript reale; Git e VS Code vengono segnalati come opzionali.

Suite completa per chi modifica il programma:

```powershell
cd "C:\percorso\DEV48"
.\.venv\Scripts\python.exe -m pytest -q
```

Il test delle soluzioni esegue tutte le 206 soluzioni ufficiali dei due percorsi contro i rispettivi controlli e verifica anche il rifiuto di una soluzione errata e l'arresto di codice infinito.

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
