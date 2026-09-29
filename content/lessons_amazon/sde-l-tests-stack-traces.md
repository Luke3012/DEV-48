# Leggere un failing test e uno stack trace

Un test fallito spesso dice già il punto di attrito: chiamata, input, valore atteso e valore reale. Prima di correggere, controlla se il test è deterministico e se il fallimento riproduce il requisito. Se il test si aspetta una lista con un ordine preciso, capire se l'ordine è parte del contratto evita un falso fix.

Uno stack trace mostra la catena degli stack frame. Parti dal primo frame del progetto, non da una riga interna di Node o del framework. Risali a chi ha costruito l'input e scendi a chi ha prodotto l'output. Il test nomina l'esempio; lo stack trace collega i file.

Fai una sola ipotesi per volta: «il controller restituisce una Promise non attesa». La verifica è concreta: il test vede una Promise invece dell'array. Un fix minimo aggiunge `await`, poi controlli le route vicine e i casi di errore.
