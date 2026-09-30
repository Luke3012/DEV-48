# HTTP e API REST

## In parole semplici

Collegare metodi, risorse e status code a operazioni applicative.

Una API REST espone risorse attraverso URL e usa i metodi HTTP per esprimere l'azione. Lo status code fa parte della risposta: permette al client di distinguere una creazione, un errore di input o una risorsa assente.

## Le parole da riconoscere

`GET`; `POST`; `PUT`; `PATCH`; `DELETE`; `status code`; `header`; `body`; `JSON`

## Un esempio concreto

```text
GET /api/subjects/42
PATCH /api/subjects/42
Content-Type: application/json

{"active": false}
```

Dopo una creazione riuscita uso normalmente 201 Created, spesso con Location per la nuova risorsa. Uno status 200 indica successo ma non comunica la creazione; uno status 400 indica input invalido. Il client deve distinguere questi esiti prima di mostrare un risultato.

## Prova tu

L'API ha creato il soggetto 42. Scrivi un esempio di risposta con status e Location e spiega come la distingui da input invalido e risorsa assente.

## Dove ci si confonde spesso

- Usare GET per modificare dati
- Restituire sempre 200
- Confondere PUT e PATCH

## Domanda di verifica

> Quale status useresti dopo la creazione riuscita di una risorsa?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
