# Dal bug distribuito al fix minimo

Un bug tra più file raramente si risolve cercando una riga “sbagliata”. Confronta requisito e comportamento, individua un input piccolo che li separa e annota dove il dato entra, cambia e viene restituito. Se la failure è su un filtro, controlla sia il predicato sia il punto in cui quel filtro viene applicato.

Modifica il componente responsabile più vicino alla causa. Un fallback aggiunto in una route può far passare il test senza correggere il service; la stessa anomalia riapparirà in un'altra chiamata. Dopo il test mirato, riesegui la suite intera e guarda i file modificati.

Per gli edge case pensa a `null`, lista vuota, ultimo indice, ID assente, Promise rifiutata e input riutilizzato dopo la chiamata. Se la funzione deve essere pura, confronta l'input con una copia prima e dopo.

### Un difetto seguito fino alla causa

Il test segnala che `GET /orders` include righe archiviate. Il controller inoltra correttamente la richiesta; il service riceve tutte le righe dal repository; il filtro confronta `row.status !== "deleted"`, quindi lascia passare anche `archived`. L'ipotesi più precisa è che il predicato non corrisponda al requisito “solo attive”. Un test con `active`, `archived` e `deleted` discrimina i casi; correggere il filtro nel service risolve anche gli altri chiamanti.

Un fallback nella route che nasconde l'archived farebbe passare solo quel percorso, lasciando il service errato. Per questo si modifica il livello più vicino alla causa, poi si esegue prima il test mirato e quindi la suite. Confronta il diff: se sono cambiati contratto, formattazione di molti file e filtro insieme, hai perso la possibilità di attribuire il risultato a una causa.

Registra fatto osservato, ipotesi, prova e risultato. Se la prova smentisce l'ipotesi, torna al flusso invece di aggiungere un altro ramo condizionale.

**Da ricordare.** Riproduci, segui il dato, formula una causa falsificabile, correggi un punto e verifica la regressione. **Per praticare:** Ordini · filtro e contratto API; Inventario · indici e riferimenti in C++.