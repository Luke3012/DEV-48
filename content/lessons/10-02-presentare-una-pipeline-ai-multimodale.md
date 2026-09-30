# Presentare una pipeline AI multimodale

## In parole semplici

Raccontare un flusso AI distribuito, fallimenti parziali e scelte di deployment.

Racconta la pipeline nell'ordine in cui scorrono i dati: input in un client interattivo, trascrizione con Whisper, recupero del contesto e risposta del modello. Per ogni passaggio chiarisci latenza, possibile errore e dato conservato.

## Le parole da riconoscere

`Unity`; `Whisper`; `RAG`; `ChromaDB`; `Ollama`; `TTS`; `systemd`; `Caddy`; `fallback`; `observability`

## Un esempio concreto

```text
Audio → STT → recupero memoria per avatar → generazione → TTS streaming → UI
```

Se TTS fallisce, la risposta testuale può rimanere disponibile mentre l'audio mostra un errore recuperabile. Conservo l'ID della richiesta per evitare che un retry associ audio a una risposta diversa. Distinguo il fallimento di un servizio dal fallimento dell'intera conversazione.

## Prova tu

La risposta testuale è pronta, ma TTS non risponde. Disegna il recupero che conserva il testo e permette retry audio, evitando di associarlo a una richiesta successiva. Non serve implementare nuovi servizi.

## Dove ci si confonde spesso

- Dire soltanto 'usa IA'
- Non spiegare latenze, errori e separazione dei dati

## Domanda di verifica

> Che cosa accade se il servizio TTS non è disponibile?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
