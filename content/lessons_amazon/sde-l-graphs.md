# Grafi: adjacency list, visited e componenti

Una lista di adiacenza conserva, per ogni nodo, i vicini raggiungibili. Se gli archi sono pochi rispetto a `V²`, occupa molto meno di una matrice. In un grafo non diretto, ogni arco appare in entrambe le liste; dimenticare il verso cambia la domanda.

DFS o BFS marcano un nodo come visto quando lo mettono in frontiera, non quando lo estraggono. Così un nodo raggiunto da più vicini non viene accodato molte volte. Per contare componenti, avvia una visita da ogni nodo non ancora visto; i nodi isolati contano comunque.

La stessa mappa che in Two Sum ricordava gli elementi precedenti ora associa un ID alla sua lista di vicini. La struttura si riusa, ma la ragione è diversa: qui non stai cercando un complemento, stai rappresentando connessioni.


### Copiare il grafo: valori e identità

Due nodi possono avere lo stesso valore e restare oggetti diversi. Per clonare una
componente conserva una mappa `originale -> copia`. Crea e registra la copia appena
scopri un nodo, prima di seguire i vicini. In un ciclo A -> B -> A, la seconda visita
ad A riusa la copia già registrata: non ricomincia a clonare per sempre. Per ciascun
arco aggiungi alla copia del nodo il riferimento alla copia del vicino, preservando
anche ordine e archi ripetuti. L'esercizio Clone Graph è Extra dopo il Core BFS/DFS.
