# Heap e Priority Queue: tenere in vista il prossimo estremo

Un heap conserva una sola garanzia: il minimo (o il massimo) è in cima. Gli altri elementi non sono ordinati fra loro. Per trattenere i `k` valori maggiori, un min-heap di capacità `k` mantiene in cima il più piccolo fra i candidati. Ogni volta che la dimensione supera `k`, espelli quell'elemento: se era troppo piccolo, il nuovo insieme conserva i migliori visti finora.

Con `[7,2,9,4,1]` e `k=2`, l'evoluzione è:

| Valore entrato | Heap dopo la correzione | Minimo espulso |
| ---: | --- | ---: |
| 7 | `[7]` | — |
| 2 | `[2,7]` | — |
| 9 | `[7,9]` | 2 |
| 4 | `[7,9]` | 4 |
| 1 | `[7,9]` | 1 |

Il min-heap non è una lista crescente; la tabella mostra soltanto la sua proprietà rilevante: la cima è il minimo. Qui la cima finale 7 è il secondo valore più grande.

**Versione Python**

```python
import heapq


def retain_largest(values, k):
    if k <= 0:
        raise ValueError("k deve essere positivo")

    heap = []
    for value in values:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

**Versione C++**

```cpp
#include <functional>
#include <queue>
#include <stdexcept>
#include <vector>
using namespace std;

using MinHeap = priority_queue<int, vector<int>, greater<int>>;

MinHeap retain_largest(const vector<int>& values, int k) {
    MinHeap heap;
    if (k <= 0) {
        throw invalid_argument("k deve essere positivo");
    }

    for (int value : values) {
        heap.push(value);
        if (static_cast<int>(heap.size()) > k) {
            heap.pop();
        }
    }
    return heap;
}
```

`n` inserimenti e al più `n` rimozioni costano `O(n log k)`; l'heap conserva `O(k)` valori. Ordinare tutto costa `O(n log n)` e mantiene ogni elemento, ma è più semplice se serve l'ordine completo. C++ usa un max-heap per default, quindi `greater<int>` è necessario per avere il minimo in cima; Python `heapq` è già un min-heap.


### Distanze con pesi positivi: Dijkstra

La BFS minimizza il numero di archi; con pesi diversi quel numero non è il costo.
Dijkstra mantiene distanze provvisorie e un min-heap `(distanza,nodo)`. Dal nodo
estratto prova ogni arco: se `distanza[u]+peso < distanza[v]`, aggiorna v e accoda
la nuova coppia. Una vecchia coppia può restare nel heap: scartala se la distanza
non coincide più con quella registrata. Con A->C di costo 10 e A->B->C di costi
1 e 2, C viene prima proposto a 10, poi migliorato a 3. Non segnare C definitivamente
quando lo inserisci. La correttezza della scelta minima richiede pesi non negativi;
il lab Network Delay usa pesi positivi e applica la stessa logica a un grafo completo.

### Proprietà dell'heap e scelta top-k

In un min-heap l'elemento in cima è minore o uguale ai figli, ma due nodi fratelli non sono completamente ordinati. Per esempio l'array `[2,5,3,9]` è un heap valido: 2 precede 5 e 3, e 5 precede 9. Per inserire 1, aggiungilo in fondo e scambialo col genitore finché l'ordine è ripristinato; per estrarre il minimo, sposta in cima l'ultimo elemento e fallo scendere. Le operazioni costano O(log n), la lettura dell'estremo O(1).

Per i due più grandi valori di `[9,1,7,3,5]`, il min-heap limitato a k evolve: `[9]`, `[1,9]`, inserisci 7 ed elimina 1 (`[7,9]`); 3 non supera la cima 7, 5 non la supera. La cima è 7, il secondo più grande. Tempo O(n log k), spazio O(k); se serve l'ordine completo, sort può essere più semplice.

Per Dijkstra, il min-heap ordina distanze provvisorie, non nodi per numero di archi. Un costo 10 per A→C può essere sostituito da A→B→C di costo 1+2=3. Aggiorna C a 3 e ignora l'entrata obsoleta 10 quando verrà estratta. La prova richiede pesi non negativi. Il grafo pesato di Network Delay usa questa variante; la queue FIFO della BFS non basta.

**Da ricordare.** Un heap conserva in cima un estremo, non ordina tutto; usalo quando devi ripetere estrazioni di priorità o mantenere pochi candidati. **Per praticare:** K-esimo valore più grande; Selezionare i valori più frequenti; Tempo massimo di consegna con pesi positivi.