# Leggere un failing test e uno stack trace

Un test fallito spesso dice già il punto di attrito: chiamata, input, valore atteso e valore reale. Prima di correggere, controlla se il test è deterministico e se il fallimento riproduce il requisito. Se il test si aspetta una lista con un ordine preciso, capire se l'ordine è parte del contratto evita un falso fix.

Uno stack trace mostra la catena degli stack frame. Parti dal primo frame del progetto, non da una riga interna di Node o del framework. Risali a chi ha costruito l'input e scendi a chi ha prodotto l'output. Il test nomina l'esempio; lo stack trace collega i file.

Fai una sola ipotesi per volta: «il controller restituisce una Promise non attesa». La verifica è concreta: il test vede una Promise invece dell'array. Un fix minimo aggiunge `await`, poi controlli le route vicine e i casi di errore.

### Dal valore inatteso al primo frame utile

Considera un test che chiama `findActive([A attivo, B pending], "B")` e si aspetta `None`, ma riceve B. L'assertion localizza il disaccordo; lo stack trace potrebbe mostrare `test_find_active` → `orderService.findActive` → `filter`. Parti dal primo frame del progetto e verifica il predicato: `status != "archived"` invece di `status == "active"` accetta anche `pending`. Il caso pending distingue le due ipotesi: non è archived, ma non è active.

Expected e actual descrivono l'osservazione, non ancora la causa. Una riga nel trace indica il punto in cui l'errore è emerso, che non sempre coincide con quello in cui è nato. Riproduci il test da solo, leggi il contratto e cambia una sola ipotesi per volta. Se la failure è intermittente, annota ordine, tempo e dipendenze prima di modificare la logica: un test flaky può indicare race o stato condiviso.

**Da ricordare.** Il test mostra il contratto violato; lo stack trace collega la failure ai file. Verifica la causa, non correggere la sola riga segnalata. **Per praticare:** Repository di esempio · C++; Repository di esempio · Node.js.