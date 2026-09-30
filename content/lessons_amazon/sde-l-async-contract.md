# Promise, null e contratto HTTP: seguire il dato fino alla risposta

Una funzione `async` restituisce sempre una Promise. Se il controller assegna la chiamata senza `await`, il body della risposta può diventare la Promise stessa; un test che attende `response.body` può nascondere il problema, quindi verifica il tipo effettivo ricevuto.

I parametri di route identificano una risorsa, la query restringe una ricerca e il body porta dati da creare o aggiornare. Un middleware può aver già validato l'input, ma il service deve comunque rappresentare esiti mancanti ed errori secondo il contratto del progetto. `null`, `undefined` e una lista vuota non significano la stessa cosa.

Una route che trova un dato dovrebbe restituire un codice coerente; un identificativo inesistente non deve trasformarsi in una risposta apparentemente riuscita. Leggi i test prima di uniformare tutto a `200` o catturare ogni eccezione. L'errore deve arrivare al posto dove il progetto sa trasformarlo in una risposta utile.

### Dalla richiesta HTTP alla risposta

Supponi che `GET /orders/42` passi `"42"` dal parametro di route al servizio. Il servizio restituisce una Promise: con `await`, il controller riceve l'ordine oppure `null`; senza attenderla, può provare a serializzare la Promise invece del dato. Il flusso completo è `parametro → ricerca asincrona → risultato → status e body`.

Per un ordine trovato il contratto potrebbe essere `200` con l'oggetto; per un ID assente, `404` con un corpo coerente. Un errore di connessione è un terzo caso: non equivale né a `null` né a una lista vuota. `undefined` spesso segnala un valore non fornito, `null` può indicare assenza esplicita, `[]` è una collezione presente senza elementi. Usa ciò che il progetto e i test definiscono, non uniformare tutto a 200.

Con `try/catch`, cattura l'errore nel livello che può tradurlo secondo il contratto; non nascondere ogni rifiuto restituendo un oggetto vuoto. Il test deve aspettare la route o il service e controllare valore, status e propagazione dell'errore.

**Da ricordare.** Segui il valore e gli errori fino alla risposta: Promise, assenza e collezione vuota hanno significati differenti. **Per praticare:** Repository asincrona · Promise e controller; Ordini · filtro e contratto API.