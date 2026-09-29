# Ricorsione: caso base, progresso e costo dello stack

Una funzione ricorsiva è una funzione che delega un problema più piccolo a sé stessa. Per fidarti del risultato, trova il caso base e dimostra che ogni chiamata lo raggiunge. In una lista, per esempio, il passo può spostarsi al nodo successivo finché il riferimento diventa nullo.

L'albero delle chiamate rende visibile il costo. Fibonacci ingenuo ricalcola gli stessi numeri molte volte; la memoization conserva il risultato già ottenuto. Così il numero di stati scende da crescita esponenziale a `O(n)`, pagando `O(n)` di memoria.

Il call stack consuma spazio e ha un limite pratico. Per DFS su un grafo profondo, una versione iterativa con stack può essere più robusta. La ricorsione non è automaticamente più elegante: deve rendere più chiara la struttura del problema.
