# Un problema Medium in 40 minuti

Prima leggi prompt e constraints fino in fondo. Scrivi un caso normale, un limite e un caso che mette in difficoltà la soluzione lenta. Ripeti il contratto in una frase: input, output, assunzioni. Se serve ordinare o usare spazio extra, dillo prima di farlo.

Quando l'algoritmo è chiaro, implementa la parte centrale senza perfezionare nomi o formattazione. Compila presto. Poi verifica l'input più piccolo, duplicati, indice ai confini e il test grande. Ogni fix dovrebbe corrispondere a una causa che puoi descrivere.

Se dopo dieci minuti manca ancora una strategia, conviene conservare una soluzione parziale corretta e scrivere la brute force. Un risultato funzionante può valere più di un'ottimizzazione incompleta. Gli ultimi minuti servono a rileggere il codice dall'inizio e a verificare il contratto, senza aggiungere funzionalità non richieste.

### Provare il flusso prima del timer

Immagina di ricevere un array crescente di 100.000 elementi e una richiesta di primo indice con valore almeno `x`. La scansione lineare è facile da verificare a mano ma può leggere tutti i 100.000 elementi; il confine binario mantiene `[lo,hi)` e dimezza i candidati. Durante una prova, annotare questo invariante prima di digitare fa risparmiare tempo quando i bordi si avvicinano.

Il timer è un vincolo di lavoro, non un algoritmo. Una pianificazione possibile è: chiarire contratto e casi, scegliere l'approccio e stimarne il costo, implementare la parte centrale, poi spendere gli ultimi minuti su compilazione e casi che possono smentire la soluzione. Se l'ottimizzazione non è pronta, una brute force corretta con costo dichiarato conserva un risultato utile. Non promettere un test passato che non hai eseguito: separa ciò che hai ragionato da ciò che hai verificato.

**Da ricordare.** Allena un ciclo completo: contratto, soluzione, costo e verifica; lascia traccia di ciò che è stato eseguito davvero. **Per praticare:** Problema di coding · 40 min; Problema di coding · 25 min.