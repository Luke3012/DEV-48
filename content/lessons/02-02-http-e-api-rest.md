# HTTP e API REST

## In parole semplici

L'obiettivo di questa lezione è collegare metodi, risorse e status code a operazioni applicative.

Una API REST espone risorse attraverso URL e usa i metodi HTTP per esprimere l'azione. Lo status code fa parte della risposta: permette al client di distinguere una creazione, un errore di input o una risorsa assente.

### Perché è utile

Quando entra in gioco una richiesta di rete, il risultato non arriva subito e può anche non arrivare affatto. Per questo devi ragionare sia sul dato atteso sia sugli stati di attesa, errore e annullamento.

## Le parole da riconoscere

- `GET`
- `POST`
- `PUT`
- `PATCH`
- `DELETE`
- `status code`
- `header`
- `body`
- `JSON`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **GET, POST, PUT** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
GET /api/subjects/42
PATCH /api/subjects/42
Content-Type: application/json

{"active": false}
```

Individua il momento in cui parte l'operazione, quello in cui arriva la risposta e il punto in cui viene gestito un fallimento.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare GET per modificare dati
- Restituire sempre 200
- Confondere PUT e PATCH

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quale status useresti dopo la creazione riuscita di una risorsa?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
