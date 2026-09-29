# Matrice di copertura per la validazione finale

Questa matrice descrive il catalogo corrente. Rilevanza significa competenza utile,
non frequenza stimata delle domande Amazon. Gli esercizi DSA hanno timer individuali;
le simulazioni dedicate verificano soltanto il problema effettivamente selezionato.

| Competenza | Teoria | Codice praticato | Verifica a tempo |
|---|---|---|---|
| Contratto, Big-O, spazio, constraints | problem-solving, complexity | banca DSA, brute force e ottimizzazione | tutti i task; Three Sum nel full mock |
| Array, stringhe, Set, HashMap | arrays-strings, hashmap-set | Two Sum, duplicate, anagrammi, gruppi | timer individuali |
| Two Pointers | two-pointers | coppia ordinata, palindrome, Container, Three Sum | Three Sum, full mock 40 |
| Sliding Window + Map | sliding-window | longest-substring, character-replacement, min-window | sprint 25: longest-substring |
| Prefix Sum + Map | prefix-sum | subarray-sum, pivot-index, product-except-self | timer individuali |
| Sorting, Intervals | sorting-intervals | merge, insert, meeting-rooms | timer individuali |
| Stack, Queue, Deque | stack-queue | parentesi, BFS, heap/frontiere | timer individuali |
| Monotonic Stack | monotonic-stack | daily-temperatures, largest-rectangle | timer individuali |
| Binary Search e boundary | binary-search, binary-boundaries, binary-variants | search, range, lower-bound, rotated | timer individuali |
| Binary Search on Answer | binary-answer | min-eating-speed | timer individuale |
| Linked List e puntatori | linked-lists | reverse-list, merge-k-lists, LRU | timer individuali |
| Fast/slow e ciclo in lista | two-pointers, linked-lists | linked-list-cycle, identità dei nodi | timer individuale; Core giorno 4 |
| Ricorsione, Trees, BST | recursion, tree-traversal, bst-paths | depth, diameter, validate-BST, LCA, max-path | timer individuali |
| Visita per livelli | tree-traversal, bfs-dfs-grid | rotting-oranges applica il modello a livelli; manca un task Tree Level Order diretto | timer individuale del task equivalente |
| BFS, DFS, Grid | bfs-dfs-grid, graphs | islands, oranges, word-ladder | timer individuali |
| Graph e componenti | graphs | connected-components, islands | timer individuali |
| Cloning del grafo | graphs: rappresentazione e visited | clone-graph, copie per identità, cicli e self-loop | timer individuale; Extra |
| Cycle Detection, Topological Sort | topological-sort | course-schedule | timer individuale |
| Heap, Priority Queue, Top K | heap | kth-largest, top-k-frequent, k-closest | timer individuali |
| Graph + Heap | graphs/heap; Dijkstra, rilassamento e voci obsolete | network-delay | Extra |
| Greedy, Sorting + Greedy | greedy | interval-scheduling | timer individuale, Core giorno 5 |
| Backtracking | backtracking | subsets, permutations, combination-sum | timer individuali |
| DP: min/max/esistenza | dp-memoization, dp-models | stairs, house-robber, coin-change, word-break | coding 40: coin-change |
| Repository navigation e debugging | repo-orientation, tests-stack-traces, debugging-loop | demo, lab intermedi, Parcel Node/C++ | repository 60 e full mock |
| Async, error handling, contratti | node-repository, async-contract | profile, orders, Parcel; 404/409, retry, stato | Parcel Node 60 |
| OOD e stato interno C++ | cpp-repository, debugging-loop | Repository/Service/API/helper Parcel | Parcel C++ 60 |
| AI Assistant contestuale | ai-assistant | prompt su README/file, ipotesi e verifica | esercizio di comprensione locale; nessun servizio cloud |
| LP, customer impact, ownership, dati, comunicazione | leadership-principles, work-simulation | 36 scenari originali con tradeoff | debrief formativo; nessuna chiave ufficiale Amazon |
| Work Style | work-style | 8 riflessioni | familiarizzazione, nessun punteggio |

I benchmark pubblici richiesti sono coperti direttamente o per modello equivalente,
con l'equivalenza esplicita sopra: Tree Level Order condivide il meccanismo della
frontiera a livelli già implementato; non viene dichiarato presente come task diretto.
