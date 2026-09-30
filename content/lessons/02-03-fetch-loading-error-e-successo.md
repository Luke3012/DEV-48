# Fetch: loading, error e successo

## In parole semplici

Prima di iniziare, ripassa [Promise e async/await](02-01-promise-e-async-await.md) e [HTTP e API REST](02-02-http-e-api-rest.md).

Implementare una richiesta robusta e rappresentarne tutti gli stati nella UI.

`fetch` risolve la Promise anche quando il server risponde 404 o 500, quindi devi controllare `response.ok`. La UI deve inoltre distinguere attesa, dati disponibili, risultato vuoto ed errore.

Una richiesta attraversa passaggi distinti: contatto con il server, risposta HTTP, lettura del corpo e controllo della forma dei dati. Se mostri tutto come “successo o errore” senza sapere a quale passaggio sei arrivato, è difficile capire il guasto.

Costruiamo quindi la funzione a piccoli passi. `fetch` restituisce una `Promise<Response>`, non il JSON. Prima controlliamo `response.ok` perché un `404` è comunque una risposta HTTP; dopo aver accettato la risposta leggiamo il corpo con `response.json()`. Questa lettura è a sua volta asincrona e può fallire se il corpo non è JSON valido. Infine controlliamo il contratto minimo che l'app si aspetta.

## Le parole da riconoscere

`fetch`; `response.ok`; `response.json`; `loading`; `errore`; `finally`; `AbortController`

## Un esempio concreto

```javascript
async function readSubjects(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("HTTP " + response.status);
  }

  const data = await response.json();
  if (!Array.isArray(data)) {
    throw new Error("La risposta non è una lista");
  }

  return data;
}
```

La prima `await` aspetta la risposta del trasporto. Un errore di rete, un URL irraggiungibile o una richiesta annullata rifiutano la Promise; un `404` invece arriva come `Response` e richiede il controllo esplicito di `ok`. Quando `ok` è `false`, lanciamo l'errore prima di leggere il corpo.

Solo dopo passiamo alla seconda `await`. `response.json()` può rifiutare durante il parsing: ricevere byte dal server non garantisce che siano JSON leggibile. Se il parse riesce, `data` è ancora un valore esterno non fidato. `Array.isArray` controlla il contenitore, ma non dimostra che ogni elemento abbia `id` e `name` validi; per quel contratto serve la stessa validazione runtime introdotta ai confini dei dati esterni.

La funzione trasforma il trasporto in due esiti per il chiamante: una lista valida, anche vuota, oppure un errore che può essere gestito più in alto. La UI può rappresentare una richiesta in caricamento, un errore recuperabile, un successo vuoto o una lista piena. Una lista vuota non dice se la richiesta sia partita né se sia fallita, quindi questi stati vanno tenuti distinti.

Qui non aggiungiamo ancora `AbortController`. Prima rendiamo chiari risposta, status, parsing ed errore; la lezione sul caricamento remoto aggiungerà cleanup e richieste fuori ordine.

## Prova tu

Prova la funzione con risposte controllate: 200 con [], 404, JSON non valido e un oggetto al posto dell'array. Annota quale caso è successo vuoto e quali sono errori. Nel lab la rete sarà sostituita da un trasporto riproducibile.

## Dove ci si confonde spesso

- Credere che fetch rifiuti automaticamente su 404
- Non gestire richieste obsolete

## Domanda di verifica

> Perché bisogna controllare response.ok?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).
