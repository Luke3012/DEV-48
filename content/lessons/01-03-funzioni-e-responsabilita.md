# Funzioni e responsabilità

## In parole semplici

Prima di iniziare, ripassa [Valori, tipi e confronti](01-01-valori-tipi-e-confronti.md).

Scrivere funzioni piccole, prevedibili e con input/output espliciti.

Una buona funzione riceve pochi dati, svolge un compito riconoscibile e restituisce un risultato chiaro. Se per descriverla servono molti verbi, probabilmente contiene più responsabilità da separare.

Una funzione trasforma input in output. Quando la chiami, gli argomenti diventano parametri; il corpo esegue i passaggi e `return` consegna un risultato al chiamante. Tenere visibili questi tre momenti rende più facile capire chi possiede i dati e dove aspettarsi un effetto.

Prendiamo `calculateTotal(12, 2)`: i due numeri sono gli input, la moltiplicazione è l'elaborazione e il valore restituito è `24`. Una funzione diversa può stampare quel risultato. Calcolare un valore e scrivere nella console sono responsabilità diverse.

## Le parole da riconoscere

`parametri`; `return`; `arrow function`; `funzione pura`; `default parameter`; `early return`

## Un esempio concreto

```javascript
function calculateTotal(unitPrice, quantity) {
  return unitPrice * quantity;
}

function printTotal(total) {
  console.log("Totale: " + total + " euro");
}

const total = calculateTotal(12, 2);
console.log(total); // 24: valore restituito
printTotal(total);  // Totale: 24 euro: effetto sulla console
```

Nella chiamata `calculateTotal(12, 2)`, `unitPrice` riceve 12 e `quantity` riceve 2. Il corpo calcola `12 * 2`; `return` passa 24 al punto in cui la funzione è stata chiamata, quindi `total` diventa 24. La funzione non ha modificato i due input né scritto altrove.

`printTotal` usa invece `console.log`, che produce un effetto osservabile fuori dal valore restituito. Non ha un `return`, quindi il suo risultato è `undefined`: stampare “24 euro” non restituisce la stringa al chiamante. Anche una funzione con un side effect può essere utile; basta sapere quando lo esegue. Un handler React può chiamare una funzione di salvataggio in risposta a un click, mentre il calcolo della UI durante il render dovrebbe limitarsi a produrre JSX.

Con un arrow function, `value => value.trim()` restituisce implicitamente l'espressione. Se apri un blocco, `value => { value.trim(); }`, occorre scrivere `return value.trim()`: senza, il chiamante riceve `undefined`. Una callback è semplicemente una funzione passata a un'altra funzione, che decide quando invocarla.

## Prova tu

Scrivi `fullName` partendo dal contratto dell'esercizio. Poi sostituisci la callback di `apply` con una che rende il testo maiuscolo. Spiega la differenza tra `transform` e `transform(value)`.

## Dove ci si confonde spesso

- Funzioni che modificano variabili globali
- Troppi rami e responsabilità

## Domanda di verifica

> Che differenza c'è tra restituire un valore e produrre un side effect?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
