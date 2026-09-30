# Matrice teoria → pratica → verifica

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
| Fast/slow e rimozione dalla fine | linked-lists | remove-nth-from-end: gap fisso, dummy e casi testa/coda | Extended |
| Ricorsione, Trees, BST | recursion, tree-traversal, bst-paths | depth, diameter, validate-BST, LCA, max-path | timer individuali |
| Alberi elementari e strutturali | tree-traversal, bst-paths | invert-tree, same-tree, subtree, tree-level-order, kth-smallest, build-tree-pre-in, serialize-tree | Extended |
| Visita per livelli | tree-traversal, bfs-dfs-grid | tree-level-order su alberi; oranges-rotting resta esempio distinto di BFS multi-sorgente | timer individuale |
| BFS, DFS, Grid | bfs-dfs-grid, graphs | islands, oranges, word-ladder | timer individuali |
| Raggiungibilità inversa su griglia | bfs-dfs-grid | pacific-atlantic: visite dai bordi e intersezione | Extended |
| Graph e componenti | graphs | connected-components, islands | timer individuali |
| Proprietà di un grafo albero | graphs | valid-tree: connettività più n−1 archi | Extended |
| Cloning del grafo | graphs: rappresentazione e visited | clone-graph, copie per identità, cicli e self-loop | timer individuale; Extra |
| Cycle Detection, Topological Sort | topological-sort | course-schedule | timer individuale |
| Heap, Priority Queue, Top K | heap | kth-largest, top-k-frequent, k-closest | timer individuali |
| Mediana online | heap | median-stream: due heap e invariante di bilanciamento | Extended |
| Graph + Heap | graphs/heap; Dijkstra, rilassamento e voci obsolete | network-delay | Extra |
| Greedy, Sorting + Greedy | greedy | interval-scheduling | timer individuale, Core giorno 5 |
| Inizio e minimo di un segmento | arrays-strings, complexity | max-subarray con tabella di Kadane; max-product mostra max/min correnti | Core + Extended |
| Ricerca del minimo ruotato | binary-variants | find-min-rotated con invariante distinta dalla ricerca del target | Extended |
| Sequenze e palindromi | hashmap-set, two-pointers | longest-consecutive; palindromic-substrings con espansione dal centro | Extended |
| Trie e wildcard | trie (facoltativa), backtracking | trie, trie-wildcard, word-search-ii | Extended, fuori dai sei giorni |
| DP e greedy aggiuntivi | dp-memoization, dp-models, greedy | LIS, House Robber II, Decode Ways, Jump Game | Extended |
| Backtracking | backtracking | subsets, permutations, combination-sum | timer individuali |
| DP: min/max/esistenza | dp-memoization, dp-models | stairs, house-robber, coin-change, word-break | coding 40: coin-change |
| Repository navigation e debugging | repo-orientation, tests-stack-traces, debugging-loop | demo, lab intermedi, Parcel Node/C++ | repository 60 e full mock |
| Async, error handling, contratti | node-repository, async-contract | profile, orders, Parcel; 404/409, retry, stato | Parcel Node 60 |
| OOD e stato interno C++ | cpp-repository, debugging-loop | Repository/Service/API/helper Parcel | Parcel C++ 60 |
| AI Assistant contestuale | ai-assistant | prompt su README/file, ipotesi e verifica | esercizio di comprensione locale; nessun servizio cloud |
| LP, customer impact, ownership, dati, comunicazione | leadership-principles, work-simulation | 36 scenari originali con tradeoff | debrief formativo; nessuna chiave ufficiale Amazon |
| Work Style | work-style | 8 riflessioni | familiarizzazione, nessun punteggio |

Il confronto completo, deduplicato per titolo, con Blind 75, Grind 75 e LeetCode 75
è in [amazon-blind75-coverage.md](amazon-blind75-coverage.md). La matrice distingue
pratica diretta, equivalente, parziale ed esclusioni intenzionali. I benchmark sono
un riferimento generale di pattern e non una misura di frequenza Amazon. Il Core
di sei giorni e i suoi ID restano invariati.
