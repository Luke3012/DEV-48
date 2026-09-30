# Form controllati

## In parole semplici

Prima di iniziare, ripassa [State ed eventi](05-03-state-ed-eventi.md), [Form e accessibilità](03-02-form-e-accessibilita.md) e [Errori e validazione](01-09-errori-e-validazione.md).

Mantenere input, validazione e submit coerenti con lo state React.

In un input controllato, il valore mostrato viene dallo state e `onChange` aggiorna quello state. Hai così un'unica fonte di verità per validazione, invio e messaggi di errore.

Il browser sa inviare un form e può ricaricare la pagina; preventDefault impedisce quel comportamento quando React gestisce l'invio. L'input controllato legge il valore dallo stato e onChange registra ogni modifica. Inizia con una stringa, anche vuota, evitando il passaggio da undefined a un valore controllato. Validazione e richiesta restano nel submit, perché dipendono dall'azione dell'utente.

## Le parole da riconoscere

`controlled input`; `value`; `onChange`; `onSubmit`; `preventDefault`; `validation`; `error state`

## Un esempio concreto

```jsx
import { useState } from 'react';
export default function SubjectForm({ onSave }) {
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  function submit(event) {
    event.preventDefault();
    if (!name.trim()) { setError('Inserisci un nome'); return; }
    onSave(name.trim());
    setName(''); setError('');
  }
  return <form onSubmit={submit} noValidate>
    <label htmlFor="name">Nome</label>
    <input id="name" value={name} onChange={event => setName(event.target.value)}
      aria-invalid={Boolean(error)} aria-describedby={error ? 'name-error' : undefined} />
    {error && <p id="name-error" role="alert">{error}</p>}
    <button type="submit">Salva</button>
  </form>;
}
```

Il form aggiorna il campo su onChange ma salva soltanto sul submit. noValidate rende osservabile la validazione dell'esempio invece di lasciarla al browser. Una stringa di soli spazi produce l'errore e non chiama onSave; il collegamento aria-describedby associa il messaggio al campo. L'esempio è sincrono: per un salvataggio remoto il reset deve avvenire solo dopo il successo.

## Prova tu

Verifica submit con Invio, nome vuoto e nome con spazi esterni. L'errore deve essere leggibile, il campo deve conservare il testo invalido e onSave deve ricevere il nome normalizzato una sola volta. Nel lab estendi alla modifica di un record.

## Dove ci si confonde spesso

- Mescolare input controllati e non controllati
- Validare soltanto dopo la chiamata API

## Domanda di verifica

> Che cosa rende controllato un input React?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
