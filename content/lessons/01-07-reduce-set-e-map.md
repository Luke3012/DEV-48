# Reduce, Set e Map

## In parole semplici

Prima di iniziare, ripassa [Array: map, filter, find e some](01-04-array-map-filter-find-e-some.md).

Aggregare valori e scegliere strutture dati adeguate per lookup e unicità.

`reduce` combina molti valori in un solo risultato. `Set` è comodo per eliminare duplicati, mentre `Map` associa chiavi a valori ed è utile quando cerchi spesso un elemento per identificatore.

Questo è un approfondimento: filtro e trasformazione bastano per iniziare React. `reduce` accumula un risultato, `Set` conserva valori unici e `Map` associa chiavi a valori. Usali quando rendono la domanda sui dati più chiara, senza trasformare ogni ciclo in una catena compatta.

## Le parole da riconoscere

`reduce`; `accumulatore`; `Set`; `Map`; `unicità`; `lookup`

## Un esempio concreto

```javascript
const orders = [{ amount: 4 }, { amount: 2 }];
console.log(orders.reduce((sum, order) => sum + order.amount, 0)); // 6
console.log([ ...new Set(['Nord', 'Centro', 'Nord']) ]); // ['Nord', 'Centro']
const byId = new Map([[1, { name: 'Anna' }]]);
console.log(byId.get(1).name, byId.has(9)); // 'Anna', false
```

Lo zero iniziale rende la somma definita anche su `[]`. Set conserva l'ordine di inserimento; Map cerca per chiave, mentre `array.map` è una trasformazione e non una struttura dati. Non costruire una Map a ogni ricerca se usi una sola volta una lista minuscola.

## Prova tu

Calcola la somma dei controlli degli attivi, poi riscrivila con un ciclo. Scegli la versione che riesci a spiegare meglio; entrambe devono restituire zero sull'array vuoto.

## Dove ci si confonde spesso

- Usare reduce per rendere il codice inutilmente compatto
- Confondere Map con map

## Domanda di verifica

> Quando preferiresti un oggetto Map rispetto a un array?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
