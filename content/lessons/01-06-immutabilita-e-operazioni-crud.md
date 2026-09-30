# Immutabilità e operazioni CRUD

## In parole semplici

Prima di iniziare, ripassa [Oggetti, destructuring e spread](01-05-oggetti-destructuring-e-spread.md).

Aggiungere, modificare ed eliminare elementi nel modo atteso da React.

Invece di modificare l'array esistente, ne produci uno nuovo: spread per aggiungere, `map` per aggiornare e `filter` per eliminare. React può così riconoscere il cambiamento e aggiornare la UI in modo prevedibile.

L'immutabilità qui è un modo per tenere distinguibili lo stato precedente e quello successivo. Non significa vietare ogni mutazione locale: significa che una trasformazione dei dati applicativi produce una nuova collezione e non altera quella che ha ricevuto.

Per creare una riga, aggiungila a un nuovo array; per rimuoverla, filtra gli ID che restano; per cambiare una riga, usa `map` e copia l'oggetto corrispondente. Se non cambi un oggetto, puoi conservarne il riferimento. Questo schema prepara direttamente agli aggiornamenti dello state React.

## Le parole da riconoscere

`spread`; `map`; `filter`; `identità`; `aggiornamento immutabile`; `CRUD`

## Un esempio concreto

```javascript
const items = [
  { id: 1, name: "Anna", active: false },
  { id: 2, name: "Mario", active: true }
];

const added = [...items, { id: 3, name: "Sara", active: true }];
const changed = items.map(item =>
  item.id === 1 ? { ...item, active: true } : item
);
const removed = items.filter(item => item.id !== 2);

console.log(added.length, items.length); // 3, 2
console.log(changed[0].active, items[0].active); // true, false
console.log(changed !== items); // true: array nuovo
console.log(changed[1] === items[1]); // true: riga non modificata
```

L'inserimento produce `added`, senza allungare `items`. Per l'aggiornamento, `map` restituisce l'oggetto copiato per Anna e riusa quello di Mario. Il confronto mostra due livelli distinti: il contenitore è nuovo (`changed !== items`), mentre la riga non toccata conserva la sua identità.

Ora confronta questo con il bug React:

~~~jsx
items.push(newItem);
setItems(items);
~~~

push ha già cambiato l'array esistente e poi setItems riceve lo stesso riferimento. React confronta il valore precedente e quello richiesto; se sono lo stesso array, può saltare il render. Anche copiando l'array dopo aver mutato un oggetto, l'oggetto precedente è già stato alterato: la copia del solo contenitore non annulla quella scrittura.

Una trasformazione immutabile mantiene un “prima” leggibile e consegna un riferimento nuovo a React, per esempio `setItems(current => [...current, newItem])`. Per un elemento annidato copia l'array, la riga modificata e il percorso degli oggetti annidati che cambi. `sort()` invece modifica l'array su cui lavora: ordina una copia o usa `toSorted()` se l'ambiente del progetto lo supporta.

## Prova tu

Scrivi un aggiornamento per ID assente: il contenuto deve rimanere equivalente e nessun oggetto deve essere mutato. Riprendi poi la stessa regola nel laboratorio React: il nuovo contesto allena il collegamento tra trasformazione dei dati e rendering.

## Dove ci si confonde spesso

- Push sullo state
- Cambiare direttamente una proprietà
- Perdere campi durante una copia

## Domanda di verifica

> Come aggiorni un elemento di un array senza modificarlo direttamente?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
