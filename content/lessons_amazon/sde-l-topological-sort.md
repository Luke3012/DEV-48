# Topological Sort e cicli: dipendenze prima dei dipendenti

Un ordinamento topologico mette ogni prerequisito prima di ciò che dipende da esso. Gli archi sono diretti e descrivono `prerequisito → attività`; se il grafo contiene un ciclo, non esiste un ordine che possa rispettare tutte le dipendenze.

Kahn conta quanti prerequisiti entrano in ogni nodo (`indegree`). I nodi con grado entrante zero possono iniziare; quando ne rimuovi uno, decrementi il grado dei suoi successori. Se la coda si svuota prima di emettere tutti i nodi, quelli rimasti sono bloccati da un ciclo.

**Versione Python**

```python
from collections import deque


def topological_order(node_count, edges):
    graph = [[] for _ in range(node_count)]
    indegree = [0] * node_count
    for prerequisite, dependent in edges:
        graph[prerequisite].append(dependent)
        indegree[dependent] += 1

    ready = deque(node for node in range(node_count) if indegree[node] == 0)
    order = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for dependent in graph[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)

    return order if len(order) == node_count else None
```

**Versione C++**

```cpp
#include <optional>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

optional<vector<int>> topological_order(int node_count, const vector<pair<int, int>>& edges) {
    vector<vector<int>> graph(node_count);
    vector<int> indegree(node_count, 0);
    for (const auto& [prerequisite, dependent] : edges) {
        graph[prerequisite].push_back(dependent);
        ++indegree[dependent];
    }

    queue<int> ready;
    for (int node = 0; node < node_count; ++node) {
        if (indegree[node] == 0) {
            ready.push(node);
        }
    }

    vector<int> order;
    while (!ready.empty()) {
        const int node = ready.front();
        ready.pop();
        order.push_back(node);
        for (int dependent : graph[node]) {
            --indegree[dependent];
            if (indegree[dependent] == 0) {
                ready.push(dependent);
            }
        }
    }

    if (static_cast<int>(order.size()) != node_count) {
        return nullopt;
    }
    return order;
}
```

Ogni nodo entra ed esce dalla coda una volta e ogni arco decrementa un grado una volta: `O(V+E)` tempo e spazio per il grafo, i gradi e la coda. Più code possibili possono produrre ordinamenti validi diversi; confronta le precedenze se la traccia non impone un ordine specifico.

### La coda di Kahn passo per passo

Per `A→C`, `B→C`, `C→D`, i gradi entranti iniziali sono `A:0, B:0, C:2, D:1`; la coda parte con `[A,B]`. Togli A e il grado di C scende a 1. Togli B: C scende a 0 e viene accodato. Togli C: D scende a 0 e viene accodato. Togli D: sono stati emessi tutti e quattro i nodi, quindi il grafo è aciclico. Ogni nodo e arco viene elaborato una volta: O(V+E) tempo e spazio.

Se aggiungi `D→A`, nessuno dei nodi nel ciclo potrà raggiungere grado entrante zero; restano elementi non emessi. Kahn rileva così il ciclo anche se la coda si svuota senza un errore esplicito. L'ordine fra A e B può variare ed entrambe le sequenze sono valide: verifica le precedenze, a meno che il prompt richieda un ordine deterministico.

**Da ricordare.** Un ordinamento topologico esiste solo se tutte le dipendenze possono essere rimosse; i nodi residui segnalano un ciclo. **Per praticare:** Verificare che tutti i corsi siano completabili.