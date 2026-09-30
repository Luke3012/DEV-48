# State ed eventi

## In parole semplici

Prima di iniziare, ripassa [Props e composizione](05-02-props-e-composizione.md) e [Scope, const, let e closure](01-02-scope-const-let-e-closure.md).

Aggiornare l'interfaccia in risposta alle interazioni usando useState.

Lo state è la memoria locale del componente. Il setter pianifica un nuovo render; quando il nuovo valore dipende dal precedente, la forma funzionale evita di usare una fotografia ormai vecchia dello state.

Ogni render riceve uno snapshot dello stato. Il setter richiede un aggiornamento, ma non cambia la variabile letta nell'handler che sta già girando. Gli aggiornamenti nello stesso evento sono accodati: tre sostituzioni con count + 1 usano lo stesso count e producono un solo incremento. Tre updater funzionali ricevono invece, in sequenza, il risultato dell'aggiornamento precedente.

## Le parole da riconoscere

`useState`; `setter`; `event handler`; `re-render`; `functional update`; `snapshot`

## Un esempio concreto

```jsx
import { useState } from 'react';
export default function Counter() {
  const [count, setCount] = useState(0);
  function addThree() {
    setCount(current => current + 1);
    setCount(current => current + 1);
    setCount(current => current + 1);
    console.log(count); // snapshot prima del click
  }
  return <button onClick={addThree}>Conteggio: {count}</button>;
}
```

Il primo click mostra 3 nella UI e stampa 0. Sostituendo gli updater con tre setCount(count + 1), la UI mostra 1. Una callback di setTimeout creata nell'handler continua a leggere lo snapshot di quel render anche dopo che il DOM si aggiorna. L'updater risolve gli aggiornamenti basati sul valore precedente, non riscrive tutte le closure già create.

## Prova tu

Prevedi testo e console per due click consecutivi, poi verifica nel progetto React. Aggiungi un decremento che non scenda sotto zero. Chiama gli hook al livello superiore del componente, nello stesso ordine, senza inserirli in if o handler.

## Dove ci si confonde spesso

- Chiamare il setter durante il render
- Leggere state come variabile immediatamente mutabile

## Domanda di verifica

> Quando serve la forma funzionale di setState?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/state-as-a-snapshot).
