# Presentare una pipeline AI multimodale

## In parole semplici

L'obiettivo di questa lezione è raccontare un flusso AI distribuito, fallimenti parziali e scelte di deployment.

Racconta la pipeline nell'ordine in cui scorrono i dati: input in un client interattivo, trascrizione con Whisper, recupero del contesto e risposta del modello. Per ogni passaggio chiarisci latenza, possibile errore e dato conservato.

### Perché è utile

Non devi presentare un progetto come se fosse perfetto. Una risposta credibile spiega il problema, la scelta fatta, il compromesso accettato e ciò che oggi miglioreresti con più tempo o più esperienza.

## Le parole da riconoscere

- `Unity`
- `Whisper`
- `RAG`
- `ChromaDB`
- `Ollama`
- `TTS`
- `systemd`
- `Caddy`
- `fallback`
- `observability`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **Unity, Whisper, RAG** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
Audio → STT → recupero memoria per avatar → generazione → TTS streaming → UI
```

Usalo come traccia, non come frase da recitare. Sostituisci ogni affermazione generica con un fatto del tuo progetto: una scelta che hai fatto, una verifica che hai eseguito o un limite che hai riconosciuto.

Adesso copri l'esempio e racconta lo stesso concetto usando un episodio reale. Una risposta imperfetta ma tua è più credibile di una formula elegante imparata a memoria.

## Dove ci si confonde spesso

- Dire soltanto 'usa IA'
- Non spiegare latenze, errori e separazione dei dati

Se la risposta suona generica, fermati e aggiungi un dettaglio verificabile: il nome di un componente, un errore incontrato, un'alternativa scartata oppure ciò che oggi cambieresti.

## Controllo rapido

- Riesco a raccontarlo senza leggere la pagina?
- Distinguo chiaramente ciò che ho fatto io da ciò che ha prodotto uno strumento?
- Cito almeno una decisione tecnica e il relativo compromesso?
- So riconoscere un limite senza sminuire tutto il progetto?

## Domanda di verifica

> Che cosa accade se il servizio TTS non è disponibile?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
