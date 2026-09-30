# Oggetti, destructuring e spread

## In parole semplici

Prima di iniziare, ripassa [Array: map, filter, find e some](01-04-array-map-filter-find-e-some.md).

Leggere e creare copie aggiornate di strutture dati applicative.

Destructuring rende espliciti i campi che stai leggendo; spread aiuta a creare una copia con alcuni campi aggiornati. Ricorda però che la copia è superficiale: gli oggetti annidati restano condivisi se non li copi a loro volta.

Un oggetto associa proprietà a valori. Due variabili possono indicare lo stesso oggetto: una modifica attraverso l'una sarà visibile dall'altra. `const` impedisce di riassegnare la variabile, non di modificarne le proprietà. Spread copia soltanto il primo livello, quindi devi ricostruire ogni livello del percorso che vuoi cambiare.

## Le parole da riconoscere

`proprietà`; `destructuring`; `spread`; `optional chaining`; `nullish coalescing`; `copia superficiale`

## Un esempio concreto

```javascript
const user = { id: 1, profile: { city: 'Roma', age: 30 } };
const shallow = { ...user };
console.log(shallow.profile === user.profile); // true
const updated = { ...user, profile: { ...user.profile, city: 'Milano' } };
console.log(user.profile.city, updated.profile.city); // 'Roma', 'Milano'
const { id } = updated;
console.log(id, updated.profile?.city ?? 'N/D'); // 1, 'Milano'
```

`shallow` è un oggetto nuovo ma contiene il riferimento al vecchio `profile`. Una scrittura su `shallow.profile.city` cambierebbe anche `user`. `updated` ricrea entrambi i livelli e conserva `age`. `?.` interrompe l'accesso su null/undefined; `??` usa il default soltanto per quei due valori, conservando zero e stringa vuota.

## Prova tu

Implementa `moveUser` e controlla sia il risultato sia la città originale. Aggiungi una proprietà a `profile`: deve sopravvivere all'aggiornamento. Confronta i riferimenti esterni e annidati.

## Dove ci si confonde spesso

- Credere che spread faccia una copia profonda
- Modificare oggetti condivisi

## Domanda di verifica

> Perché {...obj} non è sempre una copia completamente indipendente?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
