# Progettare e sollevare lo stato

## In parole semplici

Prima di iniziare, ripassa [Props e composizione](05-02-props-e-composizione.md), [Immutabilità e operazioni CRUD](01-06-immutabilita-e-operazioni-crud.md) e [Form controllati](05-05-form-controllati.md).

Collocare ogni informazione nel proprietario comune più vicino evitando duplicazioni.

Lo state dovrebbe vivere nel componente comune più vicino a tutti quelli che lo usano. Un valore calcolabile da props e state esistenti non va duplicato: puoi ricalcolarlo durante il render.

Immagina che SearchBox tenga query="ann" in uno state e Results abbia una propria copia query="anna". Le due parti possono divergere: ogni modifica deve essere copiata manualmente da una all'altra, e un aggiornamento dimenticato mostra conteggio e lista incoerenti.

Quando due componenti devono leggere lo stesso valore, spostane la proprietà nel loro genitore comune. Il genitore passa query e una callback al campo; passa i risultati calcolati alla lista. Così c'è una sola fonte di verità:

~~~text
             Archive
          query = "anna"
            /                  ↓         ↓
     SearchBox     Results
       valore       lista filtrata
~~~

La lista filtrata dipende interamente da items e query: non è un terzo stato da mantenere. Calcolala durante il render, come una formula sui valori correnti.

## Le parole da riconoscere

`single source of truth`; `lifting state`; `derived state`; `normalizzazione`; `prop drilling`

## Un esempio concreto

```jsx
import { useState } from "react";

function SearchBox({ query, onChange }) {
  return <label>Cerca
    <input value={query} onChange={event => onChange(event.target.value)} />
  </label>;
}

function Results({ items, query }) {
  return <section>
    <p>Risultati per: {query || "tutti"}</p>
    <ul>{items.map(item => <li key={item.id}>{item.name}</li>)}</ul>
  </section>;
}

export default function Archive({ items }) {
  const [query, setQuery] = useState("");
  const normalizedQuery = query.trim().toLowerCase();
  const visibleItems = items.filter(item =>
    item.name.toLowerCase().includes(normalizedQuery)
  );

  return <>
    <SearchBox query={query} onChange={setQuery} />
    <Results items={visibleItems} query={query} />
  </>;
}
```

SearchBox non possiede una seconda `query`: mostra quella ricevuta e segnala il testo nuovo con `onChange`. Archive conserva lo state condiviso e lo passa ai componenti che ne hanno bisogno. Se la ricerca è vuota, `includes("")` conserva tutti i nomi; altrimenti il filtro crea l'array che Results mostra. Quando `items` cambia, il render rifà lo stesso calcolo e lista e conteggio restano basati sui dati correnti.

Confrontalo con `visibleItems` salvato in `useState` e sincronizzato da un Effect. Quando `items` o `query` cambiano, React può prima renderizzare con il vecchio `visibleItems`; solo dopo il commit l'Effect lo aggiorna e provoca un altro render. Se la sincronizzazione dimentica una dipendenza, i risultati possono restare vecchi. Qui `visibleItems` è una formula, quindi lo stato duplicato non aggiunge informazione e può divergere.

Un filtro così piccolo non richiede `useMemo`. Una cache introduce complessità e serve solo se una misurazione mostra un costo rilevante. “Lifting state up” risolve chi possiede il valore condiviso; non significa spostare tutto lo state in cima all'applicazione.

## Prova tu

Aggiungi un pulsante che azzera query e mostra di nuovo tutti i risultati. Poi sostituisci items dal genitore: conteggio e lista devono aggiornarsi senza setter dedicati a visible. Nel lab integra eliminazione e ricerca insieme.

## Dove ci si confonde spesso

- Duplicare stato derivabile
- Sincronizzare copie della stessa informazione con effect

## Domanda di verifica

> Come riconosci uno state che dovrebbe essere derivato?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/you-might-not-need-an-effect).
