# Liste, key e rendering condizionale

## In parole semplici

Prima di iniziare, ripassa [State ed eventi](05-03-state-ed-eventi.md) e [Array: map, filter, find e some](01-04-array-map-filter-find-e-some.md).

Renderizzare collezioni mantenendo correttamente identità e stato degli elementi.

React usa la `key` per riconoscere lo stesso elemento tra due render. Un identificatore stabile evita che stato e focus si spostino sulla riga sbagliata quando la lista viene riordinata o filtrata.

La key identifica un elemento tra fratelli e deve provenire dai dati, restando stabile tra render. Se la riga contiene un input o stato locale, una key basata sulla posizione può associare lo stato alla persona sbagliata dopo un'eliminazione. La key non viene passata come prop: passa l'ID separatamente se Row deve usarlo.

## Le parole da riconoscere

`map`; `key`; `identità`; `conditional rendering`; `empty state`; `fragment`

## Un esempio concreto

```jsx
function SubjectList({ items }) {
  if (items.length === 0) return <p>Nessun soggetto</p>;
  return <ul>{items.map(item =>
    <li key={item.id}>
      <label>{item.name} <input defaultValue={item.name} /></label>
    </li>
  )}</ul>;
}
// Uso: <SubjectList items={[{id: 1, name: 'Anna'}]} />
```

Con due righe, modifica il nome della seconda nell'input e poi elimina la prima. Con key={index} React può riusare la prima riga per un'altra persona e conservare un valore non pertinente. Con item.id riconosce quale riga è rimasta. Evita Math.random nel render: cambierebbe identità a ogni render e perderebbe stato e focus.

## Prova tu

Riproduci il caso con due ID e un input modificato, poi passa dalle key posizionali agli ID. Prova anche [] e un riordinamento. Per una quantità numerica usa `items.length > 0 && ...`: con `items.length && ...` potresti renderizzare 0.

## Dove ci si confonde spesso

- Usare l'indice come key in liste modificabili
- Dimenticare lo stato vuoto

## Domanda di verifica

> Perché la key deve essere stabile e unica tra fratelli?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/preserving-and-resetting-state).
