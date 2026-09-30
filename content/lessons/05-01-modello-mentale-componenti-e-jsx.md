# Modello mentale, componenti e JSX

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md), [Moduli ed organizzazione del codice](01-08-moduli-ed-organizzazione-del-codice.md) e [HTML semantico e struttura](03-01-html-semantico-e-struttura.md).

Descrivere la UI come funzione di props e stato mediante componenti puri.

Un componente è una funzione che descrive la UI a partire da props e state. A parità di input dovrebbe produrre lo stesso JSX, senza modificare dati o avviare operazioni durante il render.

Una schermata React parte da dati, non da modifiche manuali al DOM. Il componente legge props e state e restituisce JSX: una descrizione della UI che React può calcolare di nuovo quando quegli input cambiano.

Pensala in due casi. Se ricevo il nome Anna, la funzione produce una descrizione con “Ciao Anna”; se il nome cambia in Luca, React richiama la funzione e ottiene un nuovo JSX. JSX non è una stringa HTML: le graffe inseriscono un'espressione JavaScript dentro la descrizione.

## Le parole da riconoscere

`component`; `JSX`; `render`; `purezza`; `composizione`; `albero UI`; `espressione`

## Un esempio concreto

```jsx
function Greeting({ name }) {
  return <p>Ciao {name}</p>;
}

function App() {
  const name = "Anna";
  return <Greeting name={name} />;
}
```

In `<p>Ciao {name}</p>`, `Ciao` è testo letterale e `name` è un'espressione: React inserisce il valore della variabile. In `<p>name</p>`, invece, vedresti proprio le lettere “name”. Le graffe accettano espressioni che producono un valore, come `name` o `active ? "Attivo" : "Inattivo"`; un `if` è un'istruzione e può stare prima del `return`.

Quando `App` restituisce `<Greeting name={name} />`, passa una prop al componente figlio. `App` e `Greeting` sono normali funzioni JavaScript che descrivono parti dell'albero UI; il nome con iniziale maiuscola distingue un componente da un elemento nativo. JSX viene trasformato dagli strumenti del progetto, quindi il browser non lo interpreta da solo come un file HTML.

Il ciclo essenziale è:

~~~text
props + state
     ↓
React richiama il componente
     ↓
il componente restituisce JSX
     ↓
render: React calcola che cosa mostrare
     ↓
commit: React applica al DOM le differenze necessarie
     ↓
il browser dipinge la schermata
~~~

Render e commit sono passaggi distinti. React può richiamare il componente senza modificare il DOM se il JSX risultante non richiede cambiamenti. Per questo il render deve essere una funzione pura: con gli stessi input produce la stessa descrizione, senza modificare oggetti esterni, avviare richieste o registrare handler nel browser. Gli effetti di un click appartengono a un handler; la sincronizzazione con un sistema esterno verrà trattata più avanti.

## Prova tu

Scrivi un badge che mostri anche 'Inattivo'. Passagli false e true dal genitore senza creare stato. Nel laboratorio verifica il testo nel DOM; il controllo breve verifica soltanto la struttura del codice.

## Dove ci si confonde spesso

- Modificare dati durante il render
- Componenti monolitici
- Confondere JSX con HTML

## Domanda di verifica

> Perché il render di un componente dovrebbe essere puro?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/render-and-commit).
