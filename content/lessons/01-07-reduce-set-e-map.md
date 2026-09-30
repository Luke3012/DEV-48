# Reduce, Set e Map

## In parole semplici

Prima di iniziare, ripassa [Array: map, filter, find e some](01-04-array-map-filter-find-e-some.md).

Aggregare valori e scegliere strutture dati adeguate per lookup e unicità.

`reduce` combina molti valori in un solo risultato. `Set` è comodo per eliminare duplicati, mentre `Map` associa chiavi a valori ed è utile quando cerchi spesso un elemento per identificatore.

Questo è un approfondimento: per iniziare React bastano le trasformazioni con `map` e `filter`. `reduce` è utile quando molti elementi devono diventare un risultato solo, ma è più facile leggerlo dopo aver visto il ciclo equivalente.

Il ciclo mantiene due informazioni: il totale accumulato finora e il valore corrente. Con `[10, 20, 5]`, partiamo da `total = 0`; leggendo 10 otteniamo 10, poi 30, poi 35. In `reduce`, il primo parametro della callback è quell'accumulatore e il secondo è l'elemento letto.

## Le parole da riconoscere

`reduce`; `accumulatore`; `Set`; `Map`; `unicità`; `lookup`

## Un esempio concreto

```javascript
const values = [10, 20, 5];
const total = values.reduce((accumulator, currentValue) => {
  return accumulator + currentValue;
}, 0);
console.log(total); // 35

const regions = [...new Set(["Nord", "Centro", "Nord"])];
console.log(regions); // ["Nord", "Centro"]

const byId = new Map([[1, { name: "Anna" }]]);
console.log(byId.get(1).name, byId.has(9)); // "Anna", false
```

Il ciclo esplicito fa lo stesso lavoro prima che lo comprimiamo in reduce:

~~~javascript
let total = 0;
for (const value of [10, 20, 5]) {
  total += value;
}
~~~

Seguiamo le iterazioni:

~~~text
inizio: total = 0
leggo 10: total = 0 + 10 = 10
leggo 20: total = 10 + 20 = 30
leggo 5:  total = 30 + 5 = 35
~~~

In `reduce`, `accumulator` è il `total` conservato dal ciclo e `currentValue` è il valore letto in quel giro. Il valore iniziale `0` definisce anche il risultato per un array vuoto, la cui somma è zero. Usa un ciclo quando rende i passaggi più chiari: `reduce` non è automaticamente una forma migliore.

`Set` risponde a una domanda diversa: quali valori distinti sono presenti? Conserva l'ordine della prima occorrenza. `Map` associa chiavi a valori; `array.map` invece costruisce un array trasformato. Una `Map` è utile se la ricerca per chiave ricorre, ma non serve costruirla per consultare una sola volta una lista minuscola.

## Prova tu

Calcola la somma dei controlli degli attivi, poi riscrivila con un ciclo. Scegli la versione che riesci a spiegare meglio; entrambe devono restituire zero sull'array vuoto.

## Dove ci si confonde spesso

- Usare reduce per rendere il codice inutilmente compatto
- Confondere Map con map

## Domanda di verifica

> Quando preferiresti un oggetto Map rispetto a un array?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
