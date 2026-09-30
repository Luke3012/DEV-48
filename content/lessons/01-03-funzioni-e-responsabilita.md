# Funzioni e responsabilità

## In parole semplici

Prima di iniziare, ripassa [Valori, tipi e confronti](01-01-valori-tipi-e-confronti.md).

Scrivere funzioni piccole, prevedibili e con input/output espliciti.

Una buona funzione riceve pochi dati, svolge un compito riconoscibile e restituisce un risultato chiaro. Se per descriverla servono molti verbi, probabilmente contiene più responsabilità da separare.

Definire una funzione non la esegue: la chiamata passa argomenti ai parametri e riceve il valore di `return`. Senza `return` il risultato è `undefined`. Una funzione pura può essere chiamata più volte sugli stessi dati senza modificarli né cambiare variabili esterne. Una callback è una funzione passata a un'altra funzione, che decide quando chiamarla.

## Le parole da riconoscere

`parametri`; `return`; `arrow function`; `funzione pura`; `default parameter`; `early return`

## Un esempio concreto

```javascript
function fullName(first, last = '') {
  const clean = first.trim();
  if (clean === '') return 'Unknown';
  return `${clean} ${last.trim()}`.trim();
}
function apply(value, transform) {
  return transform(value);
}
console.log(fullName(' Anna ', ' Bianchi ')); // 'Anna Bianchi'
console.log(apply(' anna ', text => text.trim())); // 'anna'
```

Il parametro `last` usa il default soltanto se l'argomento manca o è `undefined`, non se è `null`. L'arrow `text => text.trim()` restituisce implicitamente l'espressione; con `{ ... }` serve un `return` esplicito. In `apply` passiamo la funzione, senza chiamarla prima: sarà `transform(value)` a eseguirla.

## Prova tu

Scrivi `fullName` partendo dal contratto dell'esercizio. Poi sostituisci la callback di `apply` con una che rende il testo maiuscolo. Spiega la differenza tra `transform` e `transform(value)`.

## Dove ci si confonde spesso

- Funzioni che modificano variabili globali
- Troppi rami e responsabilità

## Domanda di verifica

> Che differenza c'è tra restituire un valore e produrre un side effect?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
