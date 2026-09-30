# Effect e sincronizzazione

## In parole semplici

Prima di iniziare, ripassa [State ed eventi](05-03-state-ed-eventi.md), [Scope, const, let e closure](01-02-scope-const-let-e-closure.md) e [Progettare e sollevare lo stato](05-06-progettare-e-sollevare-lo-stato.md).

Usare useEffect solo per sincronizzarsi con sistemi esterni e gestire cleanup.

`useEffect` serve a sincronizzare React con qualcosa di esterno, per esempio una richiesta, un timer o una subscription. Se l'operazione può continuare dopo un nuovo render, la cleanup deve annullarla o scollegarla.

Un effect collega il componente a un sistema esterno dopo il commit. Prima di cambiare quel collegamento React esegue la cleanup precedente; la esegue anche allo smontaggio. L'array delle dipendenze descrive i valori reattivi letti, non una frequenza scelta per tentativi. Qui document.title appartiene al browser e title è la sola prop letta.

## Le parole da riconoscere

`useEffect`; `dependency array`; `cleanup`; `subscription`; `fetch`; `race condition`; `Strict Mode`

## Un esempio concreto

```jsx
import { useEffect } from 'react';
export default function PageTitle({ title }) {
  useEffect(() => {
    const previous = document.title;
    document.title = title;
    return () => { document.title = previous; };
  }, [title]);
  return <h1>{title}</h1>;
}
```

Al primo collegamento salva il titolo precedente e scrive quello nuovo. Se title cambia, la cleanup ripristina il vecchio titolo prima del nuovo setup. Con [] il titolo resterebbe quello della prima prop: la closure dell'effect non riceverebbe il nuovo valore. Strict Mode in sviluppo esegue un ciclo aggiuntivo setup/cleanup per far emergere sincronizzazioni non reversibili; non disattivarlo per nascondere il problema.

## Prova tu

Aggiorna title dal genitore e poi smonta PageTitle. Verifica document.title nei due momenti. Confronta tre operazioni: filtrare items nel render, salvare nel submit, collegare il titolo con un effect. Motiva la collocazione prima di usare l'hook.

## Dove ci si confonde spesso

- Usare effect per calcoli derivabili
- Dipendenze mancanti
- Cleanup assente

## Domanda di verifica

> Quali operazioni non richiedono useEffect?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/reference/react/useEffect).
