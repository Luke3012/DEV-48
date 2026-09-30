# Promise e async/await

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md) e [Errori e validazione](01-09-errori-e-validazione.md).

Ragionare su operazioni che terminano in futuro senza bloccare il programma.

Una Promise rappresenta un risultato futuro: può essere ancora in attesa, completato oppure fallito. `await` sospende quella funzione, non l'intero programma, e rende più leggibile la sequenza delle operazioni asincrone.

Una funzione async restituisce sempre una Promise. `await` aspetta il suo esito all'interno di quella funzione: le altre attività possono proseguire. Un rifiuto diventa un errore intercettabile con try/catch. Usare then insieme ad await è valido, ma alternarli senza motivo rende più difficile seguire lo stesso flusso.

## Le parole da riconoscere

`Promise`; `pending`; `fulfilled`; `rejected`; `async`; `await`; `concorrenza`

## Un esempio concreto

```text
async function getData() { return ['Anna']; }
async function load() {
  try {
    const data = await getData();
    return data.length;
  } catch (error) {
    throw new Error(`Caricamento fallito: ${error.message}`);
  }
}
load().then(count => console.log(count)); // 1
console.log('richiesta avviata'); // appare prima di 1
```

`getData()` produce una Promise anche se restituisce subito un array. Dopo `await`, `data` è l'array. Il chiamante di load riceve ancora una Promise: deve attendere o collegare then/catch. Per operazioni indipendenti puoi usare Promise.all; se una dipende dal risultato dell'altra, mantieni la sequenza.

## Prova tu

Sostituisci getData con una funzione che lancia Error. Prevedi quale catch lo riceve e aggiungi la gestione al chiamante. Non restituire un array vuoto per nascondere l'errore: vuoto e fallimento sono esiti diversi.

## Dove ci si confonde spesso

- Dimenticare await
- Mescolare then e await
- Perdere gli errori asincroni

## Domanda di verifica

> Cosa restituisce sempre una funzione dichiarata async?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
