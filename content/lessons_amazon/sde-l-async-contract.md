# Promise, null e contratto HTTP: seguire il dato fino alla risposta

Una funzione `async` restituisce sempre una Promise. Se il controller assegna la chiamata senza `await`, il body della risposta può diventare la Promise stessa; un test che attende `response.body` può nascondere il problema, quindi verifica il tipo effettivo ricevuto.

I parametri di route identificano una risorsa, la query restringe una ricerca e il body porta dati da creare o aggiornare. Un middleware può aver già validato l'input, ma il service deve comunque rappresentare esiti mancanti ed errori secondo il contratto del progetto. `null`, `undefined` e una lista vuota non significano la stessa cosa.

Una route che trova un dato dovrebbe restituire un codice coerente; un identificativo inesistente non deve trasformarsi in una risposta apparentemente riuscita. Leggi i test prima di uniformare tutto a `200` o catturare ogni eccezione. L'errore deve arrivare al posto dove il progetto sa trasformarlo in una risposta utile.
