# Caricamento dati e stati remoti

## In parole semplici

Prima di iniziare, ripassa [Fetch: loading, error e successo](02-03-fetch-loading-error-e-successo.md) e [Effect e sincronizzazione](05-07-effect-e-sincronizzazione.md).

Rappresentare esplicitamente idle, loading, success, empty ed error.

I dati remoti hanno più stati di una semplice lista: non ancora richiesti, in caricamento, riusciti, vuoti o falliti. Rappresentarli esplicitamente evita spinner eterni e schermate bianche.

Una nuova ricerca può partire prima che la precedente finisca. Se A parte prima di B ma termina dopo, A non deve sovrascrivere B. La cleanup usa sia abort per ridurre il lavoro sia un flag locale per ignorare risultati ormai obsoleti, anche quando il trasporto non rispetta l'annullamento. La UI distingue loading, error, empty e success; retry avvia una nuova richiesta.

## Le parole da riconoscere

`remote state`; `loading`; `error`; `retry`; `empty state`; `optimistic update`; `cache`

## Un esempio concreto

```jsx
import { useEffect, useState } from 'react';
export default function RemoteList({ url }) {
  const [result, setResult] = useState({ status: 'loading', data: [], error: '' });
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    let ignore = false;
    setResult({ status: 'loading', data: [], error: '' });
    async function load() {
      try {
        const response = await fetch(url, { signal: controller.signal });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (!Array.isArray(data)) throw new Error('Risposta non valida');
        if (!ignore) setResult({ status: data.length ? 'success' : 'empty', data, error: '' });
      } catch (error) {
        if (!ignore) setResult({ status: 'error', data: [], error: error.message });
      }
    }
    load();
    return () => { ignore = true; controller.abort(); };
  }, [url, attempt]);
  if (result.status === 'loading') return <p role="status">Caricamento…</p>;
  if (result.status === 'error') return <div><p role="alert">{result.error}</p>
    <button onClick={() => setAttempt(value => value + 1)}>Riprova</button></div>;
  if (result.status === 'empty') return <p>Nessun soggetto</p>;
  return <ul>{result.data.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

Ogni esecuzione dell'effect ha il proprio ignore. La cleanup di A lo imposta a true; B crea una nuova variabile ancora false. Se A termina tardi, non chiama il setter. Il catch distingue un fallimento corrente dall'annullamento obsoleto perché la vecchia esecuzione è già ignorata. L'esempio controlla soltanto l'array: riusa la validazione dei singoli soggetti vista in Fetch prima di applicarlo a dati non affidabili. Per una vista caricata subito, idle non è necessario; serve quando il caricamento attende un'azione.

## Prova tu

Nel laboratorio risolvi prima B e poi A, simulando un trasporto che ignora signal. Devono restare i risultati B. Prova poi errore, retry riuscito e successo con []. Cache e aggiornamenti ottimistici sono estensioni: introducili soltanto dopo aver verificato il flusso base e il recupero dal fallimento.

## Dove ci si confonde spesso

- Mostrare schermata vuota durante il caricamento
- Ignorare retry e richieste concorrenti

## Domanda di verifica

> Quali stati UI devi considerare quando interroghi una API?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/reference/react/useEffect).
