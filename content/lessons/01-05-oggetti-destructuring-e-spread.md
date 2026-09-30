# Oggetti, destructuring e spread

## In parole semplici

Prima di iniziare, ripassa [Array: map, filter, find e some](01-04-array-map-filter-find-e-some.md).

Leggere e creare copie aggiornate di strutture dati applicative.

Destructuring rende espliciti i campi che stai leggendo; spread aiuta a creare una copia con alcuni campi aggiornati. Ricorda però che la copia è superficiale: gli oggetti annidati restano condivisi se non li copi a loro volta.

Gli oggetti contengono proprietà; il valore di una proprietà può essere a sua volta un riferimento a un altro oggetto. Perciò due oggetti distinti possono ancora condividere una parte della loro struttura.

`{ ...user }` copia le proprietà del primo livello. Se `user.address` punta a un altro oggetto, la copia riceve lo stesso riferimento. Per aggiornare la città senza toccare l'originale, devi ricreare sia l'oggetto esterno sia `address`; gli altri campi dell'indirizzo restano copiati.

## Le parole da riconoscere

`proprietà`; `destructuring`; `spread`; `optional chaining`; `nullish coalescing`; `copia superficiale`

## Un esempio concreto

```javascript
const user = {
  name: "Anna",
  address: {
    city: "Napoli",
    postalCode: "80100"
  }
};

const shallow = { ...user };
console.log(shallow !== user); // true: oggetto esterno nuovo
console.log(shallow.address === user.address); // true: indirizzo condiviso

const updated = {
  ...user,
  address: { ...user.address, city: "Milano" }
};

console.log(user.address.city); // "Napoli"
console.log(updated.address.city); // "Milano"
console.log(updated.address.postalCode); // "80100"

const { name, address } = updated;
console.log(name, address.city); // "Anna", "Milano"
console.log(updated.address?.city ?? "N/D"); // città mostrata: Milano
```

Dopo il primo spread, `shallow` e `user` sono due oggetti esterni, ma la proprietà `address` conduce allo stesso oggetto:

~~~text
user   ──────→ { name, address } ──────→ { city: "Napoli", postalCode: "80100" }
                                          ↑
shallow ─────→ { name, address } ─────────┘
~~~

Quindi una scrittura come `shallow.address.city = "Milano"` cambierebbe anche `user.address.city`. Non basta copiare il contenitore che sta sopra: si deve copiare ogni oggetto lungo il percorso modificato. In `updated`, il secondo spread crea un nuovo `address`; `postalCode` viene conservato, mentre `city` riceve il nuovo valore.

Il destructuring estrae proprietà dai dati già ottenuti: `const { name, address } = updated` non fa una copia profonda. L'optional chaining `?.` interrompe la lettura se il valore a sinistra è `null` o `undefined`; `??` applica il default soltanto in quei due casi, quindi conserva valori come `0` e stringa vuota.

La stessa regola servirà in React: lo state può contenere più livelli di oggetti e array, e un aggiornamento deve produrre riferimenti nuovi per i livelli modificati senza alterare i dati precedenti.

## Prova tu

Implementa `moveUser` e controlla sia il risultato sia la città originale. Aggiungi una proprietà a `profile`: deve sopravvivere all'aggiornamento. Confronta i riferimenti esterni e annidati.

## Dove ci si confonde spesso

- Credere che spread faccia una copia profonda
- Modificare oggetti condivisi

## Domanda di verifica

> Perché {...obj} non è sempre una copia completamente indipendente?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
