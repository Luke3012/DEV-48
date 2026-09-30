# Array: map, filter, find e some

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Trasformare e interrogare collezioni senza cicli confusi.

Questi metodi rispondono a domande diverse: `map` trasforma tutti gli elementi, `filter` ne conserva alcuni, `find` cerca il primo e `some` verifica se ne esiste almeno uno. Scegli il metodo partendo dal risultato che ti serve.

Prima di scegliere un metodo, decidi che forma deve avere la risposta. Vuoi un elemento per ciascun input, soltanto gli elementi che passano una condizione, il primo corrispondente o una risposta sì/no? Questa domanda porta al metodo giusto più facilmente della memorizzazione di quattro nomi.

Usiamo sempre le stesse tre persone. `filter` visita ogni oggetto e conserva quelli per cui la callback restituisce `true`; `map` trasforma ciascun oggetto rimasto in un nome. Leggiamo prima i due passaggi da soli, poi li componiamo.

## Le parole da riconoscere

`map`; `filter`; `find`; `some`; `every`; `callback`; `array originale`

## Un esempio concreto

```javascript
const users = [
  { id: 1, name: "Anna", active: true },
  { id: 2, name: "Luca", active: false },
  { id: 3, name: "Sara", active: true }
];

const activeUsers = users.filter(user => user.active);
console.log(activeUsers.map(user => user.name)); // ["Anna", "Sara"]

const activeNames = users
  .filter(user => user.active)
  .map(user => user.name);
console.log(activeNames); // ["Anna", "Sara"]

console.log(users.find(user => user.id === 2)); // l'oggetto Luca
console.log(users.find(user => user.id === 9)); // undefined
console.log(users.some(user => user.active));   // true
console.log(users.every(user => user.active));  // false
```

Seguiamo prima `filter`. La callback viene chiamata una volta per ogni utente: Anna produce `true`, Luca `false`, Sara `true`. Entra l'array con tre oggetti ed esce un nuovo array con Anna e Sara; non abbiamo cambiato `users`.

Ora `map` riceve quei due oggetti e restituisce la proprietà `name` per ciascuno: esce un array di due stringhe. Il numero di elementi è ancora due, ma la forma dei valori è cambiata. Per questo la pipeline si legge da sinistra a destra: `users` → utenti attivi → nomi degli utenti attivi.

`find` dà un solo oggetto, il primo che soddisfa la condizione, oppure `undefined` se non ne trova uno. `some` e `every` restituiscono invece un booleano: il primo chiede se almeno uno passa, il secondo se li superano tutti. Prima di leggere una proprietà del risultato di `find`, gestisci l'eventuale `undefined`.

`filter` crea un array nuovo, ma gli oggetti selezionati sono gli stessi riferimenti presenti nell'array originale. Mutare `user.name` dentro una callback può quindi modificare anche l'input. “Nuovo array” non significa “copia profonda”.

## Prova tu

Implementa il filtro senza modificare l'input. Aggiungi un caso in cui nessuno è attivo e uno in cui lo sono tutti. Correggi poi `users.map(user => { user.name; })`: spiega perché produce elementi `undefined`.

## Dove ci si confonde spesso

- Usare map quando serve filter
- Dimenticare che find può restituire undefined

## Domanda di verifica

> Quando useresti find invece di filter?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
