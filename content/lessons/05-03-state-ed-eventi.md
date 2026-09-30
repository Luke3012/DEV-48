# State ed eventi

## In parole semplici

Prima di iniziare, ripassa [Props e composizione](05-02-props-e-composizione.md) e [Scope, const, let e closure](01-02-scope-const-let-e-closure.md).

Aggiornare l'interfaccia in risposta alle interazioni usando useState.

Lo state è la memoria locale del componente. Il setter pianifica un nuovo render; quando il nuovo valore dipende dal precedente, la forma funzionale evita di usare una fotografia ormai vecchia dello state.

Una variabile locale normale verrebbe ricreata ogni volta che React richiama il componente. `useState` conserva invece il valore tra render e lo consegna come snapshot alla chiamata corrente.

Al primo render, `count` vale 0. Un click avvia l'handler creato da quel render; se l'handler chiama `setCount(1)`, chiede a React un aggiornamento. La variabile `count` dentro l'handler in corso resta 0. React poi richiama il componente e il secondo render riceve `count = 1`.

## Le parole da riconoscere

`useState`; `setter`; `event handler`; `re-render`; `functional update`; `snapshot`

## Un esempio concreto

```jsx
import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  function addThree() {
    setCount(current => current + 1);
    setCount(current => current + 1);
    setCount(current => current + 1);
    console.log(count);
  }

  return <button onClick={addThree}>Conteggio: {count}</button>;
}
```

Il primo click usa un handler nato nel render #1:

~~~text
render #1: count = 0
    │
    └─ click → handler del render #1
                 legge count = 0
                 chiama setCount(1)
                 legge ancora count = 0
                           ↓
                    React pianifica un render
                           ↓
render #2: count = 1
~~~

Il setter non è un'assegnazione immediata alla variabile locale. La UI passa al valore nuovo nel render successivo; `console.log` nello stesso handler stampa ancora 0. Un timeout creato da quel handler è una closure JavaScript e conserva lo snapshot del render #1 anche se nel frattempo la UI è già al render #2.

Ora chiediamo tre incrementi. Tre chiamate `setCount(count + 1)` leggono tutte lo stesso `count` dello snapshot; ognuna chiede quindi il valore 1 e il contatore aumenta una volta. Con `setCount(current => current + 1)`, React accoda invece trasformazioni: la prima riceve 0 e produce 1, la seconda riceve 1 e produce 2, la terza riceve 2 e produce 3. Usa la forma funzionale quando il calcolo dipende dal valore precedente. Non aggiorna retroattivamente le closure già create: per quello ogni nuovo render crea nuovi handler.

## Prova tu

Prevedi testo e console per due click consecutivi, poi verifica nel progetto React. Aggiungi un decremento che non scenda sotto zero. Chiama gli hook al livello superiore del componente, nello stesso ordine, senza inserirli in if o handler.

## Dove ci si confonde spesso

- Chiamare il setter durante il render
- Leggere state come variabile immediatamente mutabile

## Domanda di verifica

> Quando serve la forma funzionale di setState?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/state-as-a-snapshot).
