# Modello mentale, componenti e JSX

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md), [Moduli ed organizzazione del codice](01-08-moduli-ed-organizzazione-del-codice.md) e [HTML semantico e struttura](03-01-html-semantico-e-struttura.md).

Descrivere la UI come funzione di props e stato mediante componenti puri.

Un componente è una funzione che descrive la UI a partire da props e state. A parità di input dovrebbe produrre lo stesso JSX, senza modificare dati o avviare operazioni durante il render.

React richiama le funzioni componente per calcolare la UI; poi applica al DOM le modifiche necessarie. JSX è una sintassi trasformata dagli strumenti del progetto, non un file HTML che Node esegue direttamente. Un componente inizia con maiuscola, restituisce un albero e usa le graffe per inserire espressioni JavaScript. Prima di introdurre hook, costruisci una UI usando soltanto props.

## Le parole da riconoscere

`component`; `JSX`; `render`; `purezza`; `composizione`; `albero UI`; `espressione`

## Un esempio concreto

```jsx
export default function Badge({ active }) {
  const label = active ? 'Attivo' : 'Inattivo';
  return <span className={active ? 'active' : 'idle'}>{label}</span>;
}
// Uso in un altro componente: <Badge active={true} />
```

Le graffe non trasformano ogni istruzione in JSX: il ternario è un'espressione, mentre un if può stare prima del return. className corrisponde all'attributo CSS class. Il componente legge active senza cambiarlo. Non avvia richieste, non scrive globali e non modifica il DOM durante il render: React può richiamarlo più volte.

## Prova tu

Scrivi un badge che mostri anche 'Inattivo'. Passagli false e true dal genitore senza creare stato. Nel laboratorio verifica il testo nel DOM; il controllo breve verifica soltanto la struttura del codice.

## Dove ci si confonde spesso

- Modificare dati durante il render
- Componenti monolitici
- Confondere JSX con HTML

## Domanda di verifica

> Perché il render di un componente dovrebbe essere puro?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
