# Presentare l'architettura di un'app Electron

## In parole semplici

Spiegare Electron main/preload/renderer, IPC, SQLite e trade-off offline-first.

Nel processo main vivono filesystem, database e funzioni privilegiate; il renderer mostra l'interfaccia. Il preload espone un ponte ristretto e l'IPC permette ai due lati di comunicare senza consegnare alla UI accesso completo al sistema.

## Le parole da riconoscere

`Electron main`; `preload`; `renderer`; `IPC`; `context isolation`; `repository`; `SQLite`; `offline-first`

## Un esempio concreto

```text
Renderer React → API tipizzata del preload → IPC → service → repository SQLite
```

Il renderer esegue la UI e può ricevere contenuto non affidabile; offrirgli filesystem e database amplia le conseguenze di un bug. Il preload espone operazioni ristrette e l'IPC attraversa il confine verso main, che valida gli argomenti prima di invocare servizi e repository.

## Prova tu

Una vista React deve leggere un soggetto dal database. Disegna renderer → preload → IPC → main e indica quale API ristretta esporresti. Motiva la validazione dell'ID nel processo privilegiato.

## Dove ci si confonde spesso

- Elencare librerie senza motivare
- Non riconoscere file troppo grandi e debito tecnico

## Domanda di verifica

> Perché il renderer non accede direttamente a filesystem e database?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
