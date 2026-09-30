# Grafi: adjacency list, visited e componenti

Un grafo esplicita relazioni fra nodi. Una lista di adiacenza associa a ogni nodo i vicini; in un grafo non diretto `(0,1)` compare sia tra i vicini di 0 sia tra quelli di 1. Con pochi archi questa rappresentazione usa `O(V+E)` spazio invece della matrice `O(V²)`.

Costruiamo il grafo con archi `(0,1)`, `(1,2)` e `(0,2)`, più il nodo isolato 3. Per trovare il cammino minimo non pesato da 0 a 2, la BFS parte da `queue=[0]`, visita 0 e accoda 1 e 2 a distanza 1. Il nodo 2 è già stato scoperto quando poi si visita 1, quindi non si accoda una seconda volta.

**Versione Python**

```python
from collections import deque


def shortest_distance(node_count, edges, start, target):
    graph = [[] for _ in range(node_count)]
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)

    distance = [-1] * node_count
    distance[start] = 0
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node == target:
            return distance[node]
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)

    return -1
```

**Versione C++**

```cpp
#include <queue>
#include <utility>
#include <vector>
using namespace std;

int shortest_distance(int node_count, const vector<pair<int, int>>& edges, int start, int target) {
    vector<vector<int>> graph(node_count);
    for (const auto& [first, second] : edges) {
        graph[first].push_back(second);
        graph[second].push_back(first);
    }

    vector<int> distance(node_count, -1);
    queue<int> pending;
    distance[start] = 0;
    pending.push(start);

    while (!pending.empty()) {
        const int node = pending.front();
        pending.pop();
        if (node == target) {
            return distance[node];
        }
        for (int neighbor : graph[node]) {
            if (distance[neighbor] == -1) {
                distance[neighbor] = distance[node] + 1;
                pending.push(neighbor);
            }
        }
    }

    return -1;
}
```

`distance != -1` svolge anche il ruolo di `visited`. Si assegna quando il nodo entra in coda: se due genitori lo scoprono, il secondo lo riconosce già visitato. Una BFS visita ogni nodo e ogni arco al massimo un numero costante di volte, quindi `O(V+E)` tempo; la lista del grafo usa `O(V+E)` e distanze e coda `O(V)`.


### Copiare il grafo: valori e identità

Due nodi possono avere lo stesso valore e restare oggetti diversi. Per clonare una
componente conserva una mappa `originale -> copia`. Crea e registra la copia appena
scopri un nodo, prima di seguire i vicini. In un ciclo A -> B -> A, la seconda visita
ad A riusa la copia già registrata: non ricomincia a clonare per sempre. Per ciascun
arco aggiungi alla copia del nodo il riferimento alla copia del vicino, preservando
anche ordine e archi ripetuti. Clone Graph combina la mappa per identità con la visita in profondità o in ampiezza.

### Componenti, livelli e altri tipi di grafo

Con nodi `{0,1,2,3}` e archi non diretti `(0,1)` e `(1,2)`, una DFS da 0 visita `0,1,2`; il nodo 3 non è raggiunto e avvia una seconda visita. Ci sono quindi due componenti, incluso il nodo isolato. Per contarle, scorri ogni nodo e avvia DFS soltanto se non è ancora stato marcato.

In Word Ladder i nodi non vengono elencati come archi: sono parole e due parole sono collegate se differiscono per una lettera. Da `hit`, i livelli BFS possono essere `hot`, poi `dot` e `lot`, poi `dog` e `log`, infine `cog`. La visita per livelli trova il cammino minimo nel numero di trasformazioni; segnare parole usate evita cicli e ripetizioni.

Qui gli archi hanno costo unitario. Se hanno pesi positivi, BFS non confronta i costi: usa Dijkstra con priorità, spiegato nella lezione Heap. Per copiare un grafo conserva una mappa per identità del nodo, non per valore: due nodi con `val=5` possono essere distinti e avere vicini diversi.

**Da ricordare.** Prima definisci nodi, direzione e peso degli archi; questi tre dettagli determinano rappresentazione e visita corretta. **Per praticare:** Contare componenti di un grafo non diretto; Trasformazione minima tra parole; Copiare una rete conservando le connessioni.