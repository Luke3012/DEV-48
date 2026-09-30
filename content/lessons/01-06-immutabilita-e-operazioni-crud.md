# Immutabilità e operazioni CRUD

## In parole semplici

Prima di iniziare, ripassa [Oggetti, destructuring e spread](01-05-oggetti-destructuring-e-spread.md).

Aggiungere, modificare ed eliminare elementi nel modo atteso da React.

Invece di modificare l'array esistente, ne produci uno nuovo: spread per aggiungere, `map` per aggiornare e `filter` per eliminare. React può così riconoscere il cambiamento e aggiornare la UI in modo prevedibile.

CRUD significa creare, leggere, aggiornare ed eliminare. Qui ogni modifica restituisce una nuova collezione e mantiene l'originale disponibile. Questo permette di confrontare prima e dopo e, in React, di consegnare un riferimento nuovo al setter. Anche `sort` muta l'array: usa una copia oppure `toSorted` se disponibile nell'ambiente.

## Le parole da riconoscere

`spread`; `map`; `filter`; `identità`; `aggiornamento immutabile`; `CRUD`

## Un esempio concreto

```javascript
const items = [{ id: 1, name: 'Anna', active: false }, { id: 2, name: 'Mario', active: true }];
const changed = items.map(item =>
  item.id === 1 ? { ...item, active: true } : item
);
const removed = changed.filter(item => item.id !== 2);
console.log(items[0].active, removed[0].active); // false, true
console.log(changed === items, changed[1] === items[1]); // false, true
```

`map` crea l'array; spread crea l'oggetto cambiato. Gli elementi non toccati possono conservare il riferimento, perché nessuno li modifica. Mutare una proprietà e passare lo stesso array a un setter React può lasciare la UI senza aggiornamento: il riferimento è ancora quello precedente. Copiare solo l'array dopo aver mutato l'oggetto non ripristina il vecchio dato.

## Prova tu

Scrivi un aggiornamento per ID assente: il contenuto deve rimanere equivalente e nessun oggetto deve essere mutato. Riprendi poi la stessa regola nel laboratorio React: il nuovo contesto allena il collegamento tra trasformazione dei dati e rendering.

## Dove ci si confonde spesso

- Push sullo state
- Cambiare direttamente una proprietà
- Perdere campi durante una copia

## Domanda di verifica

> Come aggiorni un elemento di un array senza modificarlo direttamente?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
