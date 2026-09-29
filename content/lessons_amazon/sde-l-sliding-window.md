# Sliding Window: aggiornare una finestra senza rifarla

Provare ogni substring da capo ripete gli stessi conteggi. Una finestra conserva i dati del tratto `[left, right]`: quando `right` avanza aggiungi un elemento, e quando la condizione non regge sposta `left`, rimuovendo ciò che esce. Il costo scende a `O(n)` perché ciascun bordo attraversa l'array al massimo una volta.

Per una finestra di dimensione fissa, prima accumuli i primi `k` valori, poi aggiungi il nuovo e sottrai quello che lascia. Per una finestra variabile, serve che la proprietà migliori o peggiori in modo prevedibile quando restringi. L'esempio classico usa numeri non negativi: con valori negativi, avanzare `left` non garantisce di diminuire la somma e la logica si rompe.

Con frequenze di caratteri, non basta muovere i due indici: aggiorna la mappa alla stessa operazione in cui cambia il bordo. `Longest Substring Without Repeating Characters` restringe finché la frequenza di un carattere supera uno. `Minimum Window` aggiunge invece un contatore dei requisiti ancora mancanti.
