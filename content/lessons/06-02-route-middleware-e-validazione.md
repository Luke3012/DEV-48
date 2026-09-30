# Route, middleware e validazione

## In parole semplici

Seguire il percorso request → middleware → handler → servizio → response.

La route associa un URL a un handler; il middleware applica controlli o preparazione comuni. La logica di business resta in un servizio, così l'handler si limita a tradurre richiesta e risposta.

## Le parole da riconoscere

`router`; `middleware`; `handler`; `service`; `repository`; `validation`; `error middleware`

## Un esempio concreto

```javascript
app.post('/subjects', validateSubject, async (req,res,next) => {
 try { res.status(201).json(await service.create(req.body)); } catch(e) { next(e); }
});
```

Il middleware prepara o controlla una richiesta e poi passa al passo successivo, oppure termina la risposta. Per esempio verifica l'input prima dell'handler. Il servizio applica la regola di business; il middleware degli errori traduce i fallimenti in risposte coerenti.

## Prova tu

Per POST /subjects disegna il percorso da JSON non valido a risposta 400, poi quello da input valido a risposta 201. Indica quale parte valida, quale salva e quale traduce un errore del servizio.

## Dove ci si confonde spesso

- Business logic nella route
- Input non validato
- Catch duplicati ovunque

## Domanda di verifica

> Qual è la responsabilità di un middleware?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
