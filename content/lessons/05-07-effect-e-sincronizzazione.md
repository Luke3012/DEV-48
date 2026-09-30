# Effect e sincronizzazione

## In parole semplici

Prima di iniziare, ripassa [State ed eventi](05-03-state-ed-eventi.md), [Scope, const, let e closure](01-02-scope-const-let-e-closure.md) e [Progettare e sollevare lo stato](05-06-progettare-e-sollevare-lo-stato.md).

Usare useEffect solo per sincronizzarsi con sistemi esterni e gestire cleanup.

`useEffect` serve a sincronizzare React con qualcosa di esterno, per esempio una richiesta, un timer o una subscription. Se l'operazione può continuare dopo un nuovo render, la cleanup deve annullarla o scollegarla.

In un archivio dei soggetti chiediti prima che tipo di lavoro devi fare. L'elenco filtrato è un calcolo a partire da `items` e `query`: si esegue durante il render. Eliminare una riga avviene perché l'utente ha premuto un pulsante: si gestisce nell'event handler. Sincronizzare `document.title` con il conteggio mostrato tocca invece una API del browser, esterna al flusso di React: qui serve un Effect.

`useEffect` descrive un processo di sincronizzazione dopo che React ha aggiornato il DOM. Non è una callback generica per “quando il componente parte”; `setup` e `cleanup` seguono i valori reattivi che il processo usa.

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

Per il componente dell'esempio, React segue questo ciclo:

~~~text
render → commit → setup: document.title = title

title cambia
render → commit → cleanup con il vecchio title
                 → nuovo setup con il nuovo title

il componente viene rimosso
→ cleanup finale
~~~

La cleanup salva il titolo che c'era prima di questo collegamento e lo ripristina; non annulla lo state React. Questa simmetria descrive anche altri sistemi:

~~~text
subscribe → unsubscribe
setInterval → clearInterval
addEventListener → removeEventListener
start → stop
~~~

Le dipendenze non sono un timer scelto a tentativi. Se il setup legge la prop `title`, `title` deve comparire in `[title]`; quando cambia, React pulisce la sincronizzazione vecchia e ne avvia una nuova. Se lasci l'array vuoto, il setup continua a usare la closure del primo render e il titolo del browser resta obsoleto. Le dipendenze sono quindi i valori reattivi letti dal setup.

In sviluppo, `Strict Mode` può provare un ciclo `setup → cleanup → setup` in più. Se questo produce un effetto visibile scorretto, la cleanup non sta davvero annullando il collegamento; disattivare Strict Mode nasconderebbe il difetto invece di correggerlo.

Per un timer, la cleanup cancella l'ID restituito da `setInterval`. Per un listener, rimuove lo stesso handler dallo stesso target. Per una richiesta remota, la cleanup può abortire o ignorare una risposta diventata obsoleta: lo vedrai nella lezione seguente.

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
