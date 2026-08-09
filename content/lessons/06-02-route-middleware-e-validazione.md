# Route, middleware e validazione

## In parole semplici

L'obiettivo di questa lezione è seguire il percorso request → middleware → handler → servizio → response.

La route associa un URL a un handler; il middleware applica controlli o preparazione comuni. La logica di business resta in un servizio, così l'handler si limita a tradurre richiesta e risposta.

### Perché è utile

Sul backend ogni dato attraversa un confine: arriva da una richiesta, viene controllato, passa nella logica applicativa e produce una risposta. Tenere distinti questi passaggi rende più semplici sia gli errori sia la sicurezza.

## Le parole da riconoscere

- `router`
- `middleware`
- `handler`
- `service`
- `repository`
- `validation`
- `error middleware`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **router, middleware, handler** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
app.post('/subjects', validateSubject, async (req,res,next) => {
 try { res.status(201).json(await service.create(req.body)); } catch(e) { next(e); }
});
```

Segui la richiesta nell'ordine reale: ingresso, controllo, logica, accesso ai dati e risposta. Nota anche dove finirebbe un errore.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Business logic nella route
- Input non validato
- Catch duplicati ovunque

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Qual è la responsabilità di un middleware?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
