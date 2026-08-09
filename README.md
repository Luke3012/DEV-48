# DEV//48 — Web Development Academy

DEV//48 è una piattaforma di studio offline, in italiano, dedicata allo sviluppo web e software. L'interfaccia è una TUI Python/Textual pensata per PowerShell; codice, test e laboratori restano file normali sul computer.

Il catalogo include **50 lezioni**, **100 esercizi brevi**, **12 laboratori**, **150 flashcard** e **4 sfide a tempo**. Le attività fondamentali formano un percorso guidato; gli approfondimenti restano facoltativi.

## Avvio rapido

1. Fai doppio clic su **`Avvia DEV48.bat`**.
2. Solo al primo avvio attendi la creazione di `.venv` e l'installazione delle dipendenze Python.
3. Al primo avvio scegli **Inizia il percorso**. In seguito il pulsante diventa **Continua dal prossimo passo** e guida automaticamente attraverso lezione, relativi esercizi e lezione successiva. **Torna all'ultima schermata** serve invece a riaprire esattamente ciò che stavi guardando, anche se già completato.

Sono richiesti Windows 10/11, Python 3.11 o successivo e Node.js. Git e il comando `code` di VS Code sono raccomandati per i laboratori. La prima installazione Python e il primo `npm install` richiedono Internet; in seguito lezioni ed esercizi brevi funzionano offline.

Avvio equivalente da PowerShell:

```powershell
cd "C:\percorso\DEV48"
.\.venv\Scripts\python.exe -m dev48
```

## Percorso consigliato

Inizia dal diagnostico e dai fondamenti di JavaScript, poi passa ad async/await, API, HTML/CSS e React.

Prosegui con TypeScript, CRUD React, SQL, backend, Git e debugging. Consolida infine le competenze con i laboratori, la comunicazione tecnica dei progetti e le sfide complete.

Per ogni blocco: leggi la lezione, spiega il riepilogo ad alta voce senza guardare, svolgi gli esercizi, usa gli indizi solo dopo un tentativo reale e chiudi con le flashcard. Nei laboratori descrivi ad alta voce requisiti, ipotesi e casi limite: verbalizzare il ragionamento aiuta a renderlo più preciso.

Il flusso guidato è: **lezione → Completa e vai agli esercizi → primo esercizio → Prossimo passo → secondo esercizio → Prossimo passo → lezione successiva**. Non è possibile saltare avanti da un esercizio finché non viene superato.

## Comandi dell'interfaccia

| Tasto | Azione |
|---|---|
| Frecce | Navigano subito nella schermata: selezione nelle tabelle, scorrimento nei testi, cursore nell'editor e cambio flashcard |
| `Invio` | Apre la voce selezionata / continua |
| `Ctrl+S` | Salva la risposta o completa una lezione |
| `F5` | Esegue l'esercizio corrente |
| `H` | Mostra l'indizio successivo |
| `Esc` | Torna alla schermata precedente |
| `Ctrl+K` | Apre il curriculum |
| `Ctrl+G` | Apre il glossario |
| `Ctrl+D` | Torna alla dashboard |
| `Ctrl+Q` | Chiude salvando il progresso |
| `Spazio` | Gira una flashcard / avvia o mette in pausa un timer |
| `/` | Porta il focus alla ricerca in curriculum e glossario |

La soluzione completa di un esercizio breve si sblocca dopo due tentativi falliti. Le risposte aperte vengono valutate mediante concetti richiesti e vanno poi confrontate con la risposta modello.

## Laboratori

Dalla scheda di un laboratorio:

1. premi **Apri VS Code** per creare e aprire lo starter project;
2. nei progetti React premi una sola volta **Installa dipendenze**;
3. modifica i file nella cartella `workspace/<id-lab>`;
4. premi **Esegui test** nell'app oppure usa `npm test -- --run` nel terminale di VS Code.

DEV//48 crea solo i file mancanti: riaprire un laboratorio non sovrascrive il tuo lavoro. I lab React usano versioni fissate di React, Vite, Vitest, jsdom e Testing Library per evitare aggiornamenti incompatibili improvvisi.

## Salvataggio, backup e privacy

- Il progresso è salvato subito in `data/progress.sqlite3`.
- L'ultima posizione, risposte, tentativi, XP, indizi e tempo vengono ripristinati alla riapertura.
- `data/backups/progress_latest.json` è un backup leggibile aggiornato dopo i risultati e alla chiusura.
- `data/.dev48.lock` impedisce due istanze contemporanee. Un lock lasciato da una chiusura forzata viene riconosciuto e sostituito automaticamente al prossimo avvio.
- Non esistono account, telemetria, cloud o invii remoti dei contenuti.

Per conservare uno snapshot personale basta copiare `data/progress.sqlite3` e `data/backups/progress_latest.json` mentre l'app è chiusa. Per ricominciare senza perdere i dati, chiudi DEV//48 e **rinomina** `progress.sqlite3`, per esempio in `progress-precedente.sqlite3`; al nuovo avvio verrà creato un database vuoto.

## Come vengono corretti gli esercizi

- **JavaScript:** Node viene avviato in una cartella temporanea, con timeout di 5 secondi e output limitato.
- **SQL:** le query girano su un database SQLite temporaneo ricreato per ogni prova.
- **HTML/CSS e React breve:** vengono controllati struttura e requisiti mirati.
- **Risposte aperte:** checklist di concetti e confronto con risposta modello.
- **Lab React:** Vitest e React Testing Library eseguono test nel workspace persistente.

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
| `content/catalog.json` | Manifest di tutti gli elementi didattici | Non modificare a mano |
| `content/lessons/*.md` | Testi completi delle 50 lezioni | Sì, con cautela |
| `tools/generate_content.py` | Sorgente editoriale che rigenera il catalogo | Solo per manutenzione |
| `tools/doctor.py` | Diagnostica richiamata dal file `.bat` | Solo per sviluppo |
| `tests/` | Test automatici del catalogo, DB, runner e TUI | Sì, per sviluppo |
| `data/` | Stato personale e backup, creati a runtime | Non mentre l'app è aperta |
| `workspace/` | Codice modificabile dei 12 laboratori | **Sì: è il tuo lavoro** |
| `.venv/` | Ambiente Python isolato, ricreabile | Non modificare |

Attenzione: eseguire `tools/generate_content.py` riscrive `content/catalog.json` e tutti i Markdown generati. Fallo soltanto se stai mantenendo il generatore editoriale.

## Diagnostica e test

In caso di dubbio esegui **`Diagnostica DEV48.bat`**. Verifica Python, Textual, Node/npm, catalogo, permessi di scrittura e un'esecuzione JavaScript reale; Git e VS Code vengono segnalati come opzionali.

Suite completa per chi modifica il programma:

```powershell
cd "C:\percorso\DEV48"
.\.venv\Scripts\python.exe -m pytest -q
```

Il test delle soluzioni esegue tutte le 100 soluzioni ufficiali contro i rispettivi controlli e verifica anche rifiuto di una soluzione errata e arresto di codice infinito.

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
