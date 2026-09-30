# Props e composizione

## In parole semplici

Prima di iniziare, ripassa [Modello mentale, componenti e JSX](05-01-modello-mentale-componenti-e-jsx.md) e [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Passare dati e comportamento dal genitore senza accoppiare i componenti.

Le props portano dati dal genitore al figlio. Per comunicare nella direzione opposta, il genitore passa una callback: il figlio segnala l'evento senza dover conoscere come verrà gestito.

Pensa a una prop come all'argomento con cui il genitore configura una funzione componente. Partiamo da `Greeting(name)`, poi la chiamiamo da `App`. Il dato viaggia in una direzione precisa:

~~~text
App
 │
 └─ name="Anna"
        ↓
    Greeting
~~~

La risposta a un'interazione segue il percorso opposto attraverso una funzione. Il genitore passa una callback; il figlio la invoca quando accade l'evento. Il figlio non decide come il genitore aggiornerà i propri dati.

## Le parole da riconoscere

`props`; `children`; `callback`; `one-way data flow`; `composizione`; `default value`

## Un esempio concreto

```jsx
function Greeting({ name }) {
  return <p>Ciao {name}</p>;
}

function SaveButton({ onSave }) {
  return <button type="button" onClick={onSave}>Salva</button>;
}

function Panel({ children }) {
  return <section>{children}</section>;
}

export default function App() {
  function handleSave() {
    console.log("Richiesta di salvataggio");
  }

  return <>
    <Greeting name="Anna" />
    <Panel><p>Dettagli del soggetto</p></Panel>
    <SaveButton onSave={handleSave} />
  </>;
}
```

`App` passa `name` a `Greeting`; il figlio lo riceve come dato di sola lettura. `Panel` mostra un'altra forma di composizione: ciò che metti tra i suoi tag diventa la prop `children`, quindi il contenitore non deve conoscere in anticipo il contenuto che ospiterà.

`App` passa anche `handleSave` a `SaveButton`. L'handler lo conserva in `onClick` e lo chiama solo al click: l'evento risale al genitore attraverso la callback. Scrivere `onClick={handleSave()}` la eseguirebbe subito durante il render e passerebbe a React il risultato della chiamata, spesso `undefined`. Se il figlio deve segnalare quale riga è stata scelta, può chiamare `onSelect(item.id)`; il genitore resta proprietario della decisione e dello state.

## Prova tu

Sostituisci il contenuto con una lista mantenendo Card invariata. Poi passa una callback che registra un contatore di chiamate: la costruzione della UI non deve chiamarla; un click deve chiamarla una volta.

## Dove ci si confonde spesso

- Modificare le props
- Passare interi store quando bastano due valori

## Domanda di verifica

> Come comunica un componente figlio un evento al genitore?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/passing-props-to-a-component).
