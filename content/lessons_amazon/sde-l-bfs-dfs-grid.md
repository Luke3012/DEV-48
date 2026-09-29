# BFS e DFS su una griglia: una cella è un nodo

Una griglia è un grafo implicito: i vicini di `(r,c)` sono coordinate a distanza uno. Una matrice `visited` evita di aggiungere la stessa cella alla frontiera più volte. Controlla i limiti prima di indicizzare, soprattutto ai quattro bordi.

DFS esplora una diramazione in profondità; BFS espande in ordine di distanza. Per il numero di isole, entrambe funzionano. Per il numero minimo di mosse in una griglia senza pesi, la BFS è naturale: la prima visita alla destinazione ha il cammino più corto.

In una griglia `S . # / . . E`, partendo da `S` la prima frontiera contiene la cella sotto e quella a destra. Entrambe portano alla cella centrale, ma segnandola `visited` appena la accodi eviti di inserirla due volte. Da lì `E` è a una mossa: la distanza totale è tre.

Se il runner o il servizio riusa la matrice, non mutarla per segnare le celle visitate senza che il contratto lo consenta. Una struttura `visited` separata costa spazio, ma rende visibile la scelta.
