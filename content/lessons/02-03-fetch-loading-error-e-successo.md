# Fetch: loading, error e successo

## In parole semplici

Prima di iniziare, ripassa [Promise e async/await](02-01-promise-e-async-await.md) e [HTTP e API REST](02-02-http-e-api-rest.md).

Implementare una richiesta robusta e rappresentarne tutti gli stati nella UI.

`fetch` risolve la Promise anche quando il server risponde 404 o 500, quindi devi controllare `response.ok`. La UI deve inoltre distinguere attesa, dati disponibili, risultato vuoto ed errore.

Separiamo il trasporto dalla UI. Questa funzione restituisce i soggetti oppure rifiuta con un errore; il componente che la usa decide quando mostrare caricamento, lista vuota o retry. Il controllo HTTP avviene prima di leggere il JSON. JSON valido sintatticamente non significa che abbia la forma prevista dall'applicazione.

## Le parole da riconoscere

`fetch`; `response.ok`; `response.json`; `loading`; `errore`; `finally`; `AbortController`

## Un esempio concreto

```text
async function fetchSubjects(url, signal) {
  const response = await fetch(url, { signal });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  if (!Array.isArray(data) || !data.every(item =>
    item !== null && typeof item === 'object' &&
    Number.isInteger(item.id) && typeof item.name === 'string'
  )) throw new Error('Risposta non valida');
  return data;
}
// Chiamante: await fetchSubjects('/api/subjects', controller.signal)
```

Fetch non rifiuta per uno status 404: response.ok è falso e dobbiamo lanciare l'errore. Può invece rifiutare per rete o annullamento. Passare signal permette ad AbortController di interrompere la richiesta; non annulla automaticamente il lavoro già eseguito dal server. La gestione degli esiti fuori ordine sarà nella lezione sui dati remoti.

## Prova tu

Prova la funzione con risposte controllate: 200 con [], 404, JSON non valido e un oggetto al posto dell'array. Annota quale caso è successo vuoto e quali sono errori. Nel lab la rete sarà sostituita da un trasporto riproducibile.

## Dove ci si confonde spesso

- Credere che fetch rifiuti automaticamente su 404
- Non gestire richieste obsolete

## Domanda di verifica

> Perché bisogna controllare response.ok?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).
