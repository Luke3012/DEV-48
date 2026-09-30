# Liste, key e rendering condizionale

## In parole semplici

Prima di iniziare, ripassa [State ed eventi](05-03-state-ed-eventi.md) e [Array: map, filter, find e some](01-04-array-map-filter-find-e-some.md).

Renderizzare collezioni mantenendo correttamente identità e stato degli elementi.

React usa la `key` per riconoscere lo stesso elemento tra due render. Un identificatore stabile evita che stato e focus si spostino sulla riga sbagliata quando la lista viene riordinata o filtrata.

Quando una lista cambia, React deve capire quali righe sono rimaste, quali sono nuove e quali sono state rimosse. Il posto nell'array non basta a descrivere l'identità di una persona. Per esempio:

~~~text
prima:  id 10 → Anna     id 20 → Luca     id 30 → Sara
dopo:   id 10 → Anna     id 15 → Marco    id 20 → Luca    id 30 → Sara
~~~

L'ID 15 è nuovo; Luca è sempre la persona con ID 20, anche se ora occupa un'altra posizione. La key comunica questa identità tra un render e il successivo e aiuta React a conservare lo stato del componente figlio corretto.

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
```

Immagina un input in ogni riga. All'inizio ci sono Anna (10), Luca (20) e Sara (30). Scrivi un testo nell'input di Luca, poi inserisci Marco (15) tra Anna e Luca. Con key={index}, la seconda posizione aveva la key 1 per Luca e continua ad avere la key 1 per Marco: React può riusare per Marco il nodo input che conteneva il testo di Luca. La riga ha cambiato persona, ma la key dice il contrario.

Con key={item.id}, Marco ottiene una nuova identità 15; Luca conserva 20 anche quando passa dalla seconda alla terza posizione, e il suo input resta associato a Luca. Lo stesso problema può apparire riordinando, filtrando o rimuovendo righe. Le key devono essere uniche tra fratelli e stabili nel tempo; Math.random() a ogni render crea identità sempre nuove, facendo ricreare i nodi e perdendo stato o focus.

La key è un suggerimento per React, non una prop ricevuta dal componente. Se una riga ha bisogno dell'ID nel proprio codice, passa anche item.id come normale prop. Il caso items vuoto va descritto esplicitamente; per una condizione booleana evita items.length && ..., che può mostrare lo zero numerico.

## Prova tu

Riproduci il caso con due ID e un input modificato, poi passa dalle key posizionali agli ID. Prova anche [] e un riordinamento. Per una quantità numerica usa `items.length > 0 && ...`: con `items.length && ...` potresti renderizzare 0.

## Dove ci si confonde spesso

- Usare l'indice come key in liste modificabili
- Dimenticare lo stato vuoto

## Domanda di verifica

> Perché la key deve essere stabile e unica tra fratelli?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/preserving-and-resetting-state).
