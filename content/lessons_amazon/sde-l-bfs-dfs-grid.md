# BFS e DFS su una griglia: una cella è un nodo

Una griglia rettangolare è un grafo implicito: ogni cella libera è un nodo e le mosse consentite definiscono i vicini. Con movimenti su/giù/sinistra/destra, una cella al centro ha al massimo quattro vicini; prima di leggerli bisogna controllare che le coordinate siano dentro la matrice.

Per contare mosse minime quando ogni passo costa uno, la BFS esplora per distanza. Con `S . # / . . E`, la distanza di S è 0. La prima frontiera è `(0,1)` e `(1,0)` a distanza 1; poi si raggiunge `(1,1)` a distanza 2 e infine E a distanza 3. Una matrice `distance` usa `-1` per le celle non ancora scoperte; impostarla quando accodi la cella impedisce che due genitori la inseriscano entrambi.

**Versione Python**

```python
from collections import deque


def shortest_grid_path(grid, start, target):
    rows = len(grid)
    if rows == 0 or len(grid[0]) == 0:
        return -1
    cols = len(grid[0])

    start_row, start_col = start
    target_row, target_col = target
    inside_start = 0 <= start_row < rows and 0 <= start_col < cols
    inside_target = 0 <= target_row < rows and 0 <= target_col < cols
    if not inside_start or not inside_target:
        return -1
    if grid[start_row][start_col] == "#" or grid[target_row][target_col] == "#":
        return -1
    distance = [[-1] * cols for _ in range(rows)]
    distance[start_row][start_col] = 0
    queue = deque([start])
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while queue:
        row, col = queue.popleft()
        if (row, col) == target:
            return distance[row][col]

        for dr, dc in directions:
            next_row = row + dr
            next_col = col + dc
            inside = 0 <= next_row < rows and 0 <= next_col < cols
            if inside and grid[next_row][next_col] != "#" and distance[next_row][next_col] == -1:
                distance[next_row][next_col] = distance[row][col] + 1
                queue.append((next_row, next_col))

    return -1
```

**Versione C++**

```cpp
#include <queue>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int shortest_grid_path(const vector<string>& grid, pair<int, int> start, pair<int, int> target) {
    const int rows = static_cast<int>(grid.size());
    if (rows == 0 || grid[0].empty()) {
        return -1;
    }
    const int cols = static_cast<int>(grid[0].size());
    auto inside = [&](int row, int col) {
        return 0 <= row && row < rows && 0 <= col && col < cols;
    };
    if (!inside(start.first, start.second) || !inside(target.first, target.second)) {
        return -1;
    }
    if (grid[start.first][start.second] == '#' || grid[target.first][target.second] == '#') {
        return -1;
    }

    vector<vector<int>> distance(rows, vector<int>(cols, -1));
    queue<pair<int, int>> pending;
    distance[start.first][start.second] = 0;
    pending.push(start);
    const int dr[4] = {1, -1, 0, 0};
    const int dc[4] = {0, 0, 1, -1};

    while (!pending.empty()) {
        const auto [row, col] = pending.front();
        pending.pop();
        if (pair<int, int>{row, col} == target) {
            return distance[row][col];
        }

        for (int direction = 0; direction < 4; ++direction) {
            const int next_row = row + dr[direction];
            const int next_col = col + dc[direction];
            if (inside(next_row, next_col) && grid[next_row][next_col] != '#' && distance[next_row][next_col] == -1) {
                distance[next_row][next_col] = distance[row][col] + 1;
                pending.push({next_row, next_col});
            }
        }
    }

    return -1;
}
```

Le due versioni visitano ogni cella al massimo una volta: `O(R·C)` tempo e `O(R·C)` per distanze e frontiera. Il codice assume una matrice rettangolare e coordinate di partenza e destinazione valide o da rifiutare; non modifica il contenuto ricevuto. La BFS trova il cammino minimo solo con costi uniformi. Per contare isole si può usare una DFS per componente; il primo percorso esplorato non è necessariamente il più corto.

### Lo stack di una DFS conta componenti

Nella griglia `1 1 0 / 0 1 0 / 1 0 1`, una DFS avviata da `(0,0)` aggiunge `(0,1)` allo stack; da lì scopre `(1,1)`. Quando lo stack si svuota, tutte e tre quelle celle appartengono alla prima isola. Le celle `(2,0)` e `(2,2)` avviano due visite indipendenti, quindi le isole sono tre. Marcale quando le aggiungi allo stack, non quando le estrai, così una cella non viene accodata dai due vicini.

Una cella marcata sul posto risparmia la matrice `visited`, ma cambia l'input. Se il chiamante deve conservarlo, tieni una struttura separata: nel caso peggiore occupa `O(R·C)` spazio, come la coda della BFS.

### Due visite inverse dai bordi

Per sapere quali celle raggiungono ciascun oceano, parti dai bordi e percorri gli archi al contrario: dall'altezza h puoi visitare una vicina di altezza almeno h, perché l'acqua potrà poi scendere verso la cella precedente. Avvia una BFS dal bordo nord/ovest e una dal sud/est; le celle presenti in entrambi gli insiemi raggiungono entrambi gli oceani. Così ogni cella viene visitata al massimo una volta per oceano invece di lanciare una ricerca da ciascuna posizione.

**Da ricordare.** Tratta ogni cella accessibile come nodo, controlla i limiti prima di leggerla e marca la visita prima di accodare. **Per praticare:** Contare componenti di terra; Propagazione a livelli simultanei; Celle che raggiungono entrambi gli oceani.