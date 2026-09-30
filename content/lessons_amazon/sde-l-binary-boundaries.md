# Lower Bound e Upper Bound: trovare un confine, non un elemento

Con duplicati, `binary_search` conferma che un valore è presente, ma non individua quale copia. `lower_bound` restituisce il primo elemento non minore del target; `upper_bound` il primo strettamente maggiore. La differenza tra gli iteratori è il numero di occorrenze.

Una formulazione pulita è cercare un punto di taglio in `[0, n)`. Se `nums[mid] < target`, il confine è a destra; altrimenti può essere `mid` o prima. Il ciclo termina quando i due bordi coincidono. Questo schema evita di restituire un indice fuori range quando il target è minore del minimo o maggiore del massimo.

In C++ le due funzioni sono in `<algorithm>`. In Python `bisect_left` e `bisect_right` fanno lo stesso lavoro. Impara il significato del confine: la libreria non elimina la necessità di verificare che l'indice sia valido.
