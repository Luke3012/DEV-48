# Form e accessibilità

## In parole semplici

Costruire form utilizzabili da tastiera e tecnologie assistive.

Ogni campo deve avere una label riconoscibile e gli errori devono essere collegati al campo interessato. Prova sempre il form usando soltanto la tastiera: il percorso del focus rivela molti problemi.

## Le parole da riconoscere

`form`; `label`; `name`; `required`; `fieldset`; `aria-describedby`; `focus`; `validazione`

## Un esempio concreto

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" required>
```

La validazione client dà feedback prima dell'invio ma può essere aggirata. Il server deve verificare di nuovo il contratto e i permessi. Per esempio un campo required aiuta l'utente, ma non impedisce a un altro client di inviare una richiesta senza quel campo.

## Prova tu

Crea un form con label Nome associata a input id=name e name=name, required, descrizione id=help collegata con aria-describedby e pulsante submit. Il runner controlla struttura; verifica label, focus e invio nel browser.

## Dove ci si confonde spesso

- Placeholder al posto della label
- Focus invisibile
- Errori non associati al campo

## Domanda di verifica

> Qual è la differenza tra validazione client e server?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
