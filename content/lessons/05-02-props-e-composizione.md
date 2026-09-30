# Props e composizione

## In parole semplici

Prima di iniziare, ripassa [Modello mentale, componenti e JSX](05-01-modello-mentale-componenti-e-jsx.md) e [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Passare dati e comportamento dal genitore senza accoppiare i componenti.

Le props portano dati dal genitore al figlio. Per comunicare nella direzione opposta, il genitore passa una callback: il figlio segnala l'evento senza dover conoscere come verrà gestito.

Le props sono argomenti del componente. `children` contiene il contenuto racchiuso tra i suoi tag e permette di riusare un contenitore senza sapere quale contenuto ospiterà. Per gli eventi, il genitore passa una funzione; il figlio la chiama quando l'utente agisce. La funzione deve essere passata a onClick, non eseguita durante render.

## Le parole da riconoscere

`props`; `children`; `callback`; `one-way data flow`; `composizione`; `default value`

## Un esempio concreto

```jsx
function Card({ title, children, onClose }) {
  return <section aria-label={title}>
    <h2>{title}</h2>
    <button type="button" onClick={onClose} aria-label={`Chiudi ${title}`}>×</button>
    {children}
  </section>;
}
export default function Example() {
  return <Card title="Dettagli" onClose={() => console.log('chiusura richiesta')}>
    <p>Anna Bianchi</p>
  </Card>;
}
```

Il figlio non modifica onClose né decide quale dato aggiornare. Segnala l'evento al genitore. `onClick={onClose()}` eseguirebbe la callback subito e passerebbe il suo risultato, spesso undefined. La label rende comprensibile il pulsante anche senza interpretare il simbolo ×.

## Prova tu

Sostituisci il contenuto con una lista mantenendo Card invariata. Poi passa una callback che registra un contatore di chiamate: la costruzione della UI non deve chiamarla; un click deve chiamarla una volta.

## Dove ci si confonde spesso

- Modificare le props
- Passare interi store quando bastano due valori

## Domanda di verifica

> Come comunica un componente figlio un evento al genitore?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
