# Presentare l'architettura di un'app Electron

## In parole semplici

L'obiettivo di questa lezione è spiegare Electron main/preload/renderer, IPC, SQLite e trade-off offline-first.

Nel processo main vivono filesystem, database e funzioni privilegiate; il renderer mostra l'interfaccia. Il preload espone un ponte ristretto e l'IPC permette ai due lati di comunicare senza consegnare alla UI accesso completo al sistema.

### Perché è utile

Non devi presentare un progetto come se fosse perfetto. Una risposta credibile spiega il problema, la scelta fatta, il compromesso accettato e ciò che oggi miglioreresti con più tempo o più esperienza.

## Le parole da riconoscere

- `Electron main`
- `preload`
- `renderer`
- `IPC`
- `context isolation`
- `repository`
- `SQLite`
- `offline-first`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **Electron main, preload, renderer** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
Renderer React → API tipizzata del preload → IPC → service → repository SQLite
```

Usalo come traccia, non come frase da recitare. Sostituisci ogni affermazione generica con un fatto del tuo progetto: una scelta che hai fatto, una verifica che hai eseguito o un limite che hai riconosciuto.

Adesso copri l'esempio e racconta lo stesso concetto usando un episodio reale. Una risposta imperfetta ma tua è più credibile di una formula elegante imparata a memoria.

## Dove ci si confonde spesso

- Elencare librerie senza motivare
- Non riconoscere file troppo grandi e debito tecnico

Se la risposta suona generica, fermati e aggiungi un dettaglio verificabile: il nome di un componente, un errore incontrato, un'alternativa scartata oppure ciò che oggi cambieresti.

## Controllo rapido

- Riesco a raccontarlo senza leggere la pagina?
- Distinguo chiaramente ciò che ho fatto io da ciò che ha prodotto uno strumento?
- Cito almeno una decisione tecnica e il relativo compromesso?
- So riconoscere un limite senza sminuire tutto il progetto?

## Domanda di verifica

> Perché il renderer non accede direttamente a filesystem e database?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
