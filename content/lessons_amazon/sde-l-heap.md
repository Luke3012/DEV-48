# Heap e Priority Queue: tenere in vista il prossimo estremo

Un heap non mantiene tutti gli elementi ordinati: garantisce soltanto che l'estremo sia in cima. Se ti servono i `k` valori più grandi, un min-heap di dimensione `k` conserva i migliori finora. Ogni nuovo valore entra; se il heap supera `k`, rimuovi il minimo.

Con `[9, 1, 7, 3, 5]` e `k = 2`, dopo avere inserito `9` e `1` il minimo è `1`. Inserendo `7`, lo elimini e restano `7` e `9`; `3` e `5` vengono poi scartati allo stesso modo. Il valore in cima, `7`, è il secondo più grande: il resto del heap non promette un ordine completo.

Il costo diventa `O(n log k)` e lo spazio `O(k)`, utile quando `k` è piccolo rispetto a `n`. Se ti serve l'ordine completo, ordinare una volta può essere più semplice. Se i dati arrivano in streaming, il heap evita di conservare tutto.

In C++ `priority_queue` è max-heap di default; in Python `heapq` è min-heap. Esplicita i pareggi nel comparatore: il test può aspettarsi una regola deterministica quando due frequenze sono uguali.


### Extra: distanze con pesi positivi

La BFS minimizza il numero di archi; con pesi diversi quel numero non è il costo.
Dijkstra mantiene distanze provvisorie e un min-heap `(distanza,nodo)`. Dal nodo
estratto prova ogni arco: se `distanza[u]+peso < distanza[v]`, aggiorna v e accoda
la nuova coppia. Una vecchia coppia può restare nel heap: scartala se la distanza
non coincide più con quella registrata. Con A->C di costo 10 e A->B->C di costi
1 e 2, C viene prima proposto a 10, poi migliorato a 3. Non segnare C definitivamente
quando lo inserisci. La correttezza della scelta minima richiede pesi non negativi;
il lab Network Delay usa pesi positivi. È un challenge dopo il Core, non una nuova
priorità da inserire nell'ultimo giorno.
