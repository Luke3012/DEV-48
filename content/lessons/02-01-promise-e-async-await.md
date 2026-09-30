# Promise e async/await

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md) e [Errori e validazione](01-09-errori-e-validazione.md).

Ragionare su operazioni che terminano in futuro senza bloccare il programma.

Una Promise rappresenta un risultato futuro: può essere ancora in attesa, completato oppure fallito. `await` sospende quella funzione, non l'intero programma, e rende più leggibile la sequenza delle operazioni asincrone.

Una `Promise` non è il dato futuro: è un oggetto che rappresenta un'operazione e il suo esito. Durante l'attesa è `pending`; poi diventa `fulfilled` con un valore oppure `rejected` con un errore. Una Promise completata non torna `pending`.

Prima puoi riceverla in una variabile e collegare una callback; il valore non si legge come se fosse già un array. `async` e `await` rendono più lineare il passo successivo: `async` fa restituire una Promise alla funzione, e `await` sospende quel flusso asincrono finché la Promise si assesta. Nel frattempo il resto del programma può continuare.

## Le parole da riconoscere

`Promise`; `pending`; `fulfilled`; `rejected`; `async`; `await`; `concorrenza`

## Un esempio concreto

```javascript
async function getData() {
  return ["Anna"];
}

async function load() {
  const data = await getData();
  return data.length;
}

load().then(count => console.log(count)); // 1
console.log("richiesta avviata"); // appare prima di 1
```

Quando chiami `getData`, ottieni una Promise, non direttamente l'array. La funzione `async` avvolge il valore restituito in una Promise. `load` si ferma alla sua `await`: quando `getData` si completa, `data` riceve l'array e la funzione restituisce 1. Anche `load` è `async`, quindi il suo chiamante riceve un'altra Promise e deve attenderla oppure usare `then`/`catch`.

Per visualizzare che cosa succede intorno alle Promise, seguiamo questo esempio:

~~~javascript
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
~~~

Il codice sincrono stampa A, pianifica il timer e registra il lavoro della Promise, poi stampa D. Solo quando questo codice ha finito, JavaScript esegue la callback Promise accodata e stampa C; in seguito il timer stampa B. L'ordine è `A, D, C, B`. `await` non blocca il thread fino alla risposta: sospende la funzione che lo contiene, e il suo seguito riprende quando il risultato è pronto.

Asincronia significa poter proseguire mentre un'operazione attende; concorrenza significa che più operazioni sono in corso nello stesso intervallo; parallelismo significa eseguire lavoro nello stesso istante su più risorse di calcolo. Avviare due richieste indipendenti prima di aspettarle, per esempio con `Promise.all`, permette concorrenza; `async` non crea automaticamente un thread né rende parallelo un calcolo CPU.

## Prova tu

Sostituisci getData con una funzione che lancia Error. Prevedi quale catch lo riceve e aggiungi la gestione al chiamante. Non restituire un array vuoto per nascondere l'errore: vuoto e fallimento sono esiti diversi.

## Dove ci si confonde spesso

- Dimenticare await
- Mescolare then e await
- Perdere gli errori asincroni

## Domanda di verifica

> Cosa restituisce sempre una funzione dichiarata async?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises).
