# Array: map, filter, find e some

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Trasformare e interrogare collezioni senza cicli confusi.

Questi metodi rispondono a domande diverse: `map` trasforma tutti gli elementi, `filter` ne conserva alcuni, `find` cerca il primo e `some` verifica se ne esiste almeno uno. Scegli il metodo partendo dal risultato che ti serve.

Un array è una collezione ordinata. I metodi chiamano la callback per gli elementi visitati: il valore restituito dalla callback decide che cosa succede. `filter` vuole una condizione, `map` il nuovo elemento, `find` restituisce il primo elemento corrispondente e `some` un booleano. Il nome del metodo deve corrispondere alla forma del risultato.

## Le parole da riconoscere

`map`; `filter`; `find`; `some`; `every`; `callback`; `array originale`

## Un esempio concreto

```javascript
const users = [
  { id: 1, name: 'Anna', active: true },
  { id: 2, name: 'Mario', active: false },
];
const names = users.filter(user => user.active).map(user => user.name);
console.log(names); // ['Anna']
console.log(users.find(user => user.id === 9)); // undefined
console.log(users.some(user => user.active)); // true
```

Prima `filter` produce un nuovo array con Anna, poi `map` ne estrae il nome. Gli oggetti selezionati restano gli stessi riferimenti: modificare `user.name` dentro una callback può ancora mutare l'input. In `find` l'assenza è `undefined`; controllala prima di leggere proprietà. Non confondere 'nuovo array' con 'copia profonda'.

## Prova tu

Implementa il filtro senza modificare l'input. Aggiungi un caso in cui nessuno è attivo e uno in cui lo sono tutti. Correggi poi `users.map(user => { user.name; })`: spiega perché produce elementi `undefined`.

## Dove ci si confonde spesso

- Usare map quando serve filter
- Dimenticare che find può restituire undefined

## Domanda di verifica

> Quando useresti find invece di filter?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
