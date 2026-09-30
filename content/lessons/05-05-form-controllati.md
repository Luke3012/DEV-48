# Form controllati

## In parole semplici

Prima di iniziare, ripassa [State ed eventi](05-03-state-ed-eventi.md), [Form e accessibilità](03-02-form-e-accessibilita.md) e [Errori e validazione](01-09-errori-e-validazione.md).

Mantenere input, validazione e submit coerenti con lo state React.

In un input controllato, il valore mostrato viene dallo state e `onChange` aggiorna quello state. Hai così un'unica fonte di verità per validazione, invio e messaggi di errore.

Un input controllato crea un giro completo tra React e il browser:

~~~text
state React
   ↓
value mostrato nell'input
   ↑
utente digita → onChange → setState → nuovo render
~~~

Il valore parte dallo state, quindi React sa che cosa mostrare. Quando l'utente digita, onChange legge il testo corrente dall'evento e aggiorna lo state; il render successivo restituisce quel testo come value. Se il gestore non aggiorna lo state, React continua a fornire il valore precedente e il campo sembra bloccato.

Il submit è un evento distinto. L'handler può impedire il ricaricamento predefinito, validare i dati e inviare solo ciò che rispetta il contratto.

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

Il campo parte da una stringa vuota, non da `undefined`: resta controllato fin dal primo render. `value={name}` mostra lo state; `onChange` legge `event.target.value`, che è una stringa, e `setName` richiede il render che la mostrerà. La `label` fornisce il nome accessibile del campo, mentre `aria-invalid` e `aria-describedby` comunicano errore e messaggio associato.

La validazione avviene dentro `submit` perché è l'utente ad aver chiesto di salvare. `trim()` rimuove gli spazi esterni: una stringa composta solo da spazi produce un errore e non chiama `onSave`. `noValidate` rende esplicito questo ramo dell'esempio senza lasciare che la validazione nativa del browser lo intercetti prima. `preventDefault()` impedisce la normale navigazione/invio del form, così è il gestore React a elaborare il submit.

Questo esempio salva in modo sincrono. Con un server, conserviamo il testo e gli errori se la richiesta fallisce e svuotiamo il campo solo dopo il successo. Anche quando il client valida, il server deve controllare di nuovo il contratto e i permessi.

## Prova tu

Verifica submit con Invio, nome vuoto e nome con spazi esterni. L'errore deve essere leggibile, il campo deve conservare il testo invalido e onSave deve ricevere il nome normalizzato una sola volta. Nel lab estendi alla modifica di un record.

## Dove ci si confonde spesso

- Mescolare input controllati e non controllati
- Validare soltanto dopo la chiamata API

## Domanda di verifica

> Che cosa rende controllato un input React?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
