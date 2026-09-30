# Caricamento dati e stati remoti

## In parole semplici

Prima di iniziare, ripassa [Fetch: loading, error e successo](02-03-fetch-loading-error-e-successo.md) e [Effect e sincronizzazione](05-07-effect-e-sincronizzazione.md).

Rappresentare esplicitamente idle, loading, success, empty ed error.

I dati remoti hanno più stati di una semplice lista: non ancora richiesti, in caricamento, riusciti, vuoti o falliti. Rappresentarli esplicitamente evita spinner eterni e schermate bianche.

Il risultato di una richiesta non è soltanto una lista. Prima che arrivi c'è il caricamento; la richiesta può fallire; può riuscire senza righe; oppure può riuscire con dati. Una lista vuota non può rappresentare tutti questi casi, perché non dice se il server sia stato contattato o se ci sia stato un errore.

Modelliamo il risultato come una piccola macchina a stati. Lo status dice quale esito è attuale, e ogni esito porta i dati che servono:

~~~text
loading ── successo con righe ─→ success(data)
   │
   ├──── successo senza righe ─→ empty
   └──────────── errore ───────→ error(message)
~~~

Questa è anche la forma di una discriminated union TypeScript: dopo aver controllato `status`, il codice sa se può leggere `data` oppure `message`. In React la UI sceglie un ramo per ciascuno stato.

## Le parole da riconoscere

`remote state`; `loading`; `error`; `retry`; `empty state`; `optimistic update`; `cache`

## Un esempio concreto

```jsx
import { useEffect, useState } from "react";

export default function RemoteList({ url }) {
  const [attempt, setAttempt] = useState(0);
  const [result, setResult] = useState({ url, attempt: 0, status: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    let ignore = false;
    setResult({ url, attempt, status: "loading" });

    async function load() {
      try {
        const response = await fetch(url, { signal: controller.signal });
        if (!response.ok) {
          throw new Error("HTTP " + response.status);
        }

        const data = await response.json();
        if (!Array.isArray(data)) {
          throw new Error("Risposta non valida");
        }

        if (!ignore) {
          setResult(data.length === 0
            ? { url, attempt, status: "empty" }
            : { url, attempt, status: "success", data });
        }
      } catch (error) {
        if (!ignore) {
          const message = error instanceof Error ? error.message : String(error);
          setResult({ url, attempt, status: "error", message });
        }
      }
    }

    load();
    return () => {
      ignore = true;
      controller.abort();
    };
  }, [url, attempt]);

  if (result.url !== url || result.attempt !== attempt || result.status === "loading") {
    return <p role="status">Caricamento…</p>;
  }
  if (result.status === "error") return <div>
    <p role="alert">{result.message}</p>
    <button onClick={() => {
      setAttempt(value => value + 1);
    }}>Riprova</button>
  </div>;
  if (result.status === "empty") return <p>Nessun soggetto</p>;
  return <ul>{result.data.map(item =>
    <li key={item.id}>{item.name}</li>
  )}</ul>;
}
```

Al primo render `result` è `loading` e la UI può annunciarlo con `role="status"`. Se il server restituisce una lista vuota, passiamo a `empty`; se contiene righe, `success` conserva `data`. L'errore è un quarto valore distinto e include il messaggio per `role="alert"`. Non lasciamo `data: []` sia in attesa sia in errore, così `empty` significa davvero “richiesta riuscita, nessun risultato”.

La richiesta viene avviata dall'Effect perché deve seguire la prop `url` anche quando la pagina si apre o cambia URL senza un click specifico. Il codice riusa i passaggi della lezione Fetch: attende `Response`, controlla `ok`, legge il JSON e verifica il contenitore. Per dati esterni il controllo va approfondito fino ai campi usati dalla UI.

La cleanup affronta una gara temporale:

~~~text
richiesta A ─────────────────────────→ risposta A
     richiesta B ───────→ risposta B

ordine di completamento: B, poi A
~~~

Quando parte B, React esegue la cleanup di A. Il flag di A diventa `true` e `abort()` prova a fermare il trasporto. Se A termina comunque più tardi, non può chiamare il setter; B resta il risultato corrente. Abort riduce lavoro quando è possibile, il flag protegge la UI anche se il trasporto ignora l'annullamento.

Ogni risultato conserva anche i valori `url` e `attempt` con cui è stato ottenuto. Se la prop `url` cambia o riprovi, il render rileva che il risultato appartiene alla richiesta precedente e mostra loading subito, prima che parta il nuovo Effect. In questo modo non compare per un frame la lista dell'indirizzo precedente.

Riprova incrementa `attempt` con un updater funzionale; il nuovo valore fa ripartire la sincronizzazione e mostra loading mentre la risposta arriva. `url` e `attempt` sono tutte le dipendenze reattive lette dall'Effect. `idle` serve solo se la richiesta non parte subito, per esempio dopo un'azione esplicita dell'utente.

## Prova tu

Nel laboratorio risolvi prima B e poi A, simulando un trasporto che ignora signal. Devono restare i risultati B. Prova poi errore, retry riuscito e successo con []. Cache e aggiornamenti ottimistici sono estensioni: introducili soltanto dopo aver verificato il flusso base e il recupero dal fallimento.

## Dove ci si confonde spesso

- Mostrare schermata vuota durante il caricamento
- Ignorare retry e richieste concorrenti

## Domanda di verifica

> Quali stati UI devi considerare quando interroghi una API?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/reference/react/useEffect).
