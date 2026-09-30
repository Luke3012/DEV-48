# Progettare e sollevare lo stato

## In parole semplici

Prima di iniziare, ripassa [Props e composizione](05-02-props-e-composizione.md), [Immutabilità e operazioni CRUD](01-06-immutabilita-e-operazioni-crud.md) e [Form controllati](05-05-form-controllati.md).

Collocare ogni informazione nel proprietario comune più vicino evitando duplicazioni.

Lo state dovrebbe vivere nel componente comune più vicino a tutti quelli che lo usano. Un valore calcolabile da props e state esistenti non va duplicato: puoi ricalcolarlo durante il render.

Se filtro e conteggio devono descrivere la stessa lista, il genitore comune conserva items e query; i figli ricevono dati e callback. La lista visibile è un calcolo, non un secondo archivio da sincronizzare. Uno stato duplicato richiederebbe aggiornare contemporaneamente items e visible dopo ogni creazione, eliminazione o cambio di ricerca: basta dimenticare un percorso per mostrare dati incoerenti.

## Le parole da riconoscere

`single source of truth`; `lifting state`; `derived state`; `normalizzazione`; `prop drilling`

## Un esempio concreto

```jsx
import { useState } from 'react';
function Search({ query, onChange }) {
  return <label>Cerca <input value={query} onChange={event => onChange(event.target.value)} /></label>;
}
export default function Archive({ items }) {
  const [query, setQuery] = useState('');
  const visible = items.filter(item => item.name.toLowerCase().includes(query.toLowerCase()));
  return <main>
    <Search query={query} onChange={setQuery} />
    <p>{visible.length} risultati</p>
    <ul>{visible.map(item => <li key={item.id}>{item.name}</li>)}</ul>
  </main>;
}
```

Search non ha una copia di query. Il genitore ricalcola visible a ogni render con i dati correnti. Qui un filtro piccolo non richiede useMemo: introduci una cache soltanto dopo aver misurato un costo rilevante, senza usarla per correggere la logica. Il reset della ricerca avviene in un evento, non in un effect dedicato a sincronizzare due copie.

## Prova tu

Aggiungi un pulsante che azzera query e mostra di nuovo tutti i risultati. Poi sostituisci items dal genitore: conteggio e lista devono aggiornarsi senza setter dedicati a visible. Nel lab integra eliminazione e ricerca insieme.

## Dove ci si confonde spesso

- Duplicare stato derivabile
- Sincronizzare copie della stessa informazione con effect

## Domanda di verifica

> Come riconosci uno state che dovrebbe essere derivato?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/you-might-not-need-an-effect).
