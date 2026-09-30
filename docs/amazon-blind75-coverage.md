# Matrice benchmark Blind 75 / Grind 75 / LeetCode 75

Snapshot delle liste pubbliche consultate il **1 ottobre 2026**. È una matrice di copertura didattica DSA generale; l'appartenenza a una lista non dimostra frequenza o rilevanza specifica Amazon.

- [Blind 75, lista LeetCode dell'autore](https://leetcode.com/problem-list/xi4ci4ig/) — il catalogo pubblico restituisce **76** titoli distinti, anche se il nome della lista dice 75; conservo il dato osservato senza rimuoverne uno.
- [Grind 75](https://www.techinterviewhandbook.org/grind75/) — snapshot di **75** voci dal [file di catalogo del repository dell'autore](https://github.com/yangshun/tech-interview-handbook/blob/main/apps/website/contents/_components/QuestionGroups.json). Il sito permette di personalizzare il bacino e la pianificazione; questa matrice fissa un elenco per rendere riproducibile il confronto.
- [LeetCode 75](https://leetcode.com/studyplan/leetcode-75/) — **75** titoli nei gruppi del piano ufficiale.

Le snapshot hanno 226 occorrenze e **172 titoli distinti** dopo la deduplicazione per titolo normalizzato. Sovrapposizioni a coppie: Blind/Grind 40, Blind/LeetCode 11, Grind/LeetCode 10. Un titolo presente in più liste compare una sola volta.

## Come leggere la copertura

- **Diretta**: il catalogo contiene un esercizio DEV48 originale che allena lo stesso contratto algoritmico.
- **Equivalente**: un esercizio diverso verifica lo stesso pattern/invariante; il collegamento è indicato nella colonna esercizio.
- **Parziale**: la teoria o un esercizio vicino introduce solo una parte del meccanismo; la specifica variante non è verificata.
- **Escluso intenzionalmente**: manca una pratica locale dedicata e la variante resta fuori dal Core, per evitare che tre benchmark generali gonfino il percorso.
- **Core/Extended** si riferisce al piano DEV48 di sei giorni, non alla difficoltà. I nuovi esercizi di questa revisione restano Extended.

Le formulazioni e gli esempi DEV48 sono originali; la matrice riporta solo titoli e pattern. “Coperto” non implica che DEV48 replichi integralmente la consegna esterna.

## Riepilogo di copertura

| Stato | Titoli |
|---|---:|
| Diretta | 72 |
| Equivalente | 36 |
| Parziale | 44 |
| Escluso intenzionalmente | 20 |
| Titoli con pratica diretta/equivalente già prima di questa revisione | 80 |
| Titoli collegati a nuovi esercizi diretti | 22 |
| Titoli equivalenti collegati a nuovi esercizi | 6 |

## Matrice completa

| Problema benchmark | Lista/e | Pattern principale/composizione | Lezione/i DEV48 | Pratica DEV48 | Copertura | Piano / decisione |
|---|---|---|---|---|---|---|
| 01 Matrix | Grind75 | Multi-source BFS distances | sde-l-graphs | sde-e-oranges-rotting | Equivalente | Riusa un modello equivalente; Core. |
| 3Sum | Blind75, Grind75 | Sort + two pointers | sde-l-two-pointers | sde-e-three-sum | Diretta | Già presente; nessuna duplicazione. |
| Accounts Merge | Grind75 | Graphs: connectivity/components | sde-l-graphs | sde-e-connected-components | Equivalente | Riusa un modello equivalente; Core. |
| Add Binary | Grind75 | Reverse scan + carry | sde-l-arrays-strings | — | Parziale | Si spiegano le scansioni di sequenze; non si pratica l'addizione binaria con riporto. |
| Alien Dictionary | Blind75 | Directed graph + topological ordering | sde-l-topological-sort, sde-l-graphs | — | Parziale | Ordinamento topologico e rilevamento dei cicli sono spiegati; manca la costruzione degli archi dalle parole ordinate. |
| Asteroid Collision | LeetCode75 | Stack / Queue | sde-l-stack-queue | — | Parziale | Lo stack è spiegato; manca una simulazione delle collisioni. |
| Balanced Binary Tree | Grind75 | Trees: recursive DFS | sde-l-tree-traversal | sde-e-tree-diameter | Equivalente | Riusa un modello equivalente; Extended. |
| Basic Calculator | Grind75 | Stack / Queue | sde-l-stack-queue, sde-l-monotonic-stack | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Best Time to Buy and Sell Stock | Blind75, Grind75 | Running minimum + maximum profit | sde-l-arrays-strings | sde-e-stock-profit | Diretta | Già presente; nessuna duplicazione. |
| Best Time to Buy and Sell Stock with Transaction Fee | LeetCode75 | Dynamic Programming / greedy | sde-l-dp-models | sde-e-stock-cooldown | Equivalente | Riusa un modello equivalente; Extended. |
| Binary Search | Grind75 | Binary search / boundary | sde-l-binary-search | sde-e-binary-search | Diretta | Già presente; nessuna duplicazione. |
| Binary Tree Level Order Traversal | Blind75, Grind75 | BFS by levels | sde-l-tree-traversal | sde-e-tree-level-order | Diretta | Aggiunto in questa revisione; Extended. |
| Binary Tree Maximum Path Sum | Blind75 | Trees: recursive DFS | sde-l-tree-traversal | sde-e-max-path-sum | Diretta | Già presente; nessuna duplicazione. |
| Binary Tree Right Side View | Grind75, LeetCode75 | Trees: BFS by levels | sde-l-tree-traversal | sde-e-tree-level-order | Equivalente | Riusa un modello equivalente; Extended. |
| Can Place Flowers | LeetCode75 | Intervals / greedy scheduling | sde-l-greedy, sde-l-arrays-strings | — | Parziale | Si spiegano scansioni greedy; non si pratica il vincolo di adiacenza locale. |
| Climbing Stairs | Blind75, Grind75 | Dynamic Programming / greedy | sde-l-dp-memoization | sde-e-climbing-stairs | Diretta | Già presente; nessuna duplicazione. |
| Clone Graph | Blind75, Grind75 | Graphs: clone/traverse + visited identity | sde-l-graphs | sde-e-clone-graph | Diretta | Già presente; nessuna duplicazione. |
| Coin Change | Blind75, Grind75 | Dynamic Programming / greedy | sde-l-dp-models | sde-e-coin-change | Diretta | Già presente; nessuna duplicazione. |
| Combination Sum | Blind75, Grind75 | Backtracking | sde-l-backtracking | sde-e-combination-sum | Diretta | Già presente; nessuna duplicazione. |
| Combination Sum III | LeetCode75 | Backtracking | sde-l-backtracking | sde-e-combination-sum | Equivalente | Riusa un modello equivalente; Extended. |
| Construct Binary Tree from Preorder and Inorder Traversal | Blind75, Grind75 | Recursive reconstruction + index map | sde-l-tree-traversal | sde-e-build-tree-pre-in | Diretta | Aggiunto in questa revisione; Extended. |
| Container With Most Water | Blind75, Grind75, LeetCode75 | Two pointers: drop shorter side | sde-l-two-pointers | sde-e-container-water | Diretta | Già presente; nessuna duplicazione. |
| Contains Duplicate | Blind75, Grind75 | HashMap / Set / frequency | sde-l-hashmap-set | sde-e-contains-duplicate | Diretta | Già presente; nessuna duplicazione. |
| Count Good Nodes in Binary Tree | LeetCode75 | Trees: recursive DFS | sde-l-tree-traversal | — | Parziale | La DFS è spiegata; non si pratica il trasporto del massimo lungo il cammino. |
| Counting Bits | Blind75, LeetCode75 | Bit-count DP | — (non insegnato nel track) | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Course Schedule | Blind75, Grind75 | Directed graph + cycle/topological sort | sde-l-topological-sort | sde-e-course-schedule | Diretta | Già presente; nessuna duplicazione. |
| Daily Temperatures | LeetCode75 | Monotonic stack | sde-l-monotonic-stack | sde-e-daily-temperatures | Diretta | Già presente; nessuna duplicazione. |
| Decode String | LeetCode75 | Stack / Queue | sde-l-stack-queue, sde-l-recursion | — | Parziale | Stack e ricorsione sono prerequisiti; non si pratica il parsing annidato. |
| Decode Ways | Blind75 | DP over one/two digits | sde-l-dp-memoization | sde-e-decode-ways | Diretta | Aggiunto in questa revisione; Extended. |
| Delete Node in a BST | LeetCode75 | Trees: BST ordering/inorder | sde-l-bst-paths | — | Parziale | Si spiega l'ordinamento BST; manca l'eliminazione con ricollegamento dei figli. |
| Delete the Middle Node of a Linked List | LeetCode75 | Linked lists: fast/slow | sde-l-linked-lists | — | Parziale | Puntatori e tecnica fast/slow sono spiegati; questa rimozione non è verificata direttamente. |
| Design Add and Search Words Data Structure | Blind75 | Trie + wildcard DFS | sde-l-trie | sde-e-trie-wildcard | Diretta | Aggiunto in questa revisione; Extended. |
| Determine if Two Strings Are Close | LeetCode75 | HashMap / Set / frequency | sde-l-hashmap-set | — | Parziale | Si spiegano le frequenze; mancano i controlli su alfabeto e multinsieme delle frequenze. |
| Diameter of Binary Tree | Grind75 | Trees: recursive DFS | sde-l-tree-traversal | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Domino and Tromino Tiling | LeetCode75 | Dynamic Programming / greedy | sde-l-dp-memoization | — | Parziale | La DP è spiegata; non si pratica la ricorrenza con più stati per il tassellamento. |
| Dota2 Senate | LeetCode75 | Stack / Queue | sde-l-stack-queue | — | Parziale | La coda è spiegata; manca un esercizio con regole cicliche di eliminazione. |
| Edit Distance | LeetCode75 | Two-prefix DP | sde-l-dp-models | sde-e-edit-distance | Diretta | Già presente; nessuna duplicazione. |
| Encode and Decode Strings | Blind75 | Stack / Queue | sde-l-arrays-strings, sde-l-hashmap-set | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Equal Row and Column Pairs | LeetCode75 | HashMap / Set / frequency | sde-l-hashmap-set | sde-e-group-anagrams | Equivalente | Riusa un modello equivalente; Extended. |
| Evaluate Division | LeetCode75 | Graphs/grids: BFS or DFS | sde-l-graphs | — | Parziale | La DFS sui grafi è spiegata; non si pratica il prodotto dei pesi lungo un percorso. |
| Evaluate Reverse Polish Notation | Grind75 | Stack / Queue | sde-l-stack-queue | — | Parziale | Lo stack è spiegato; manca un esercizio diretto per valutare un'espressione postfissa. |
| Find All Anagrams in a String | Grind75 | Sliding window | sde-l-sliding-window | sde-e-min-window, sde-e-character-replacement | Equivalente | Riusa un modello equivalente; Extended. |
| Find Median from Data Stream | Blind75, Grind75 | Two heaps + balance invariant | sde-l-heap | sde-e-median-stream | Diretta | Aggiunto in questa revisione; Extended. |
| Find Minimum in Rotated Sorted Array | Blind75 | Binary search: half containing minimum | sde-l-binary-variants | sde-e-find-min-rotated | Diretta | Aggiunto in questa revisione; Extended. |
| Find Peak Element | LeetCode75 | Binary search / boundary | sde-l-binary-search, sde-l-binary-boundaries, sde-l-binary-variants, sde-l-binary-answer | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Find Pivot Index | LeetCode75 | Prefix sum and remaining total | sde-l-arrays-strings, sde-l-prefix-sum | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Find the Difference of Two Arrays | LeetCode75 | HashMap / Set / frequency | sde-l-hashmap-set | sde-e-contains-duplicate | Equivalente | Riusa un modello equivalente; Core. |
| Find the Highest Altitude | LeetCode75 | Prefix sum | sde-l-prefix-sum | sde-e-pivot-index | Equivalente | Riusa un modello equivalente; Extended. |
| First Bad Version | Grind75 | Lower bound: first true | sde-l-binary-boundaries | sde-e-first-true | Equivalente | Riusa un modello equivalente; Extended. |
| Flood Fill | Grind75 | Graphs/grids: BFS or DFS | sde-l-bfs-dfs-grid | sde-e-number-islands | Equivalente | Riusa un modello equivalente; Core. |
| Graph Valid Tree | Blind75 | Connectivity + n-1 edges | sde-l-graphs | sde-e-valid-tree | Diretta | Aggiunto in questa revisione; Extended. |
| Greatest Common Divisor of Strings | LeetCode75 | Array/string scan or data structure | sde-l-arrays-strings | — | Parziale | Si spiega la scansione di stringhe; periodicità e MCD restano fuori dal Core. |
| Group Anagrams | Blind75 | HashMap / Set / frequency | sde-l-arrays-strings, sde-l-hashmap-set | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Guess Number Higher or Lower | LeetCode75 | Binary search / boundary | sde-l-binary-boundaries | sde-e-first-true | Equivalente | Riusa un modello equivalente; Extended. |
| House Robber | Blind75, LeetCode75 | Dynamic Programming / greedy | sde-l-dp-models | sde-e-house-robber | Diretta | Già presente; nessuna duplicazione. |
| House Robber II | Blind75 | Circular DP as two linear ranges | sde-l-dp-models | sde-e-house-robber-ii | Diretta | Aggiunto in questa revisione; Extended. |
| Implement Queue using Stacks | Grind75 | Stack / Queue | sde-l-stack-queue | — | Parziale | FIFO e LIFO sono spiegati; manca un esercizio sull'adattatore a due stack. |
| Implement Trie (Prefix Tree) | Blind75, Grind75, LeetCode75 | Trie: prefixes and terminal words | sde-l-trie | sde-e-trie | Diretta | Aggiunto in questa revisione; Extended. |
| Increasing Triplet Subsequence | LeetCode75 | Array/string scan or data structure | sde-l-dp-memoization | sde-e-lis | Equivalente | Riusa un modello equivalente; Extended. |
| Insert Interval | Blind75, Grind75 | Intervals / greedy scheduling | sde-l-sorting-intervals | sde-e-insert-interval | Diretta | Già presente; nessuna duplicazione. |
| Invert Binary Tree | Blind75, Grind75 | Trees: recursive DFS | sde-l-tree-traversal | sde-e-invert-tree | Diretta | Aggiunto in questa revisione; Extended. |
| Is Subsequence | LeetCode75 | Two pointers | sde-l-two-pointers | sde-e-is-subsequence | Diretta | Già presente; nessuna duplicazione. |
| Jump Game | Blind75 | Greedy farthest reach | sde-l-greedy | sde-e-jump-game | Diretta | Aggiunto in questa revisione; Extended. |
| K Closest Points to Origin | Grind75 | Heap / Priority Queue | sde-l-heap | sde-e-k-closest | Diretta | Già presente; nessuna duplicazione. |
| Keys and Rooms | LeetCode75 | Graphs/grids: BFS or DFS | sde-l-graphs, sde-l-bfs-dfs-grid | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Kids With the Greatest Number of Candies | LeetCode75 | Array/string scan or data structure | sde-l-arrays-strings, sde-l-prefix-sum | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Koko Eating Bananas | LeetCode75 | Binary search on answer | sde-l-binary-answer | sde-e-min-eating-speed | Diretta | Già presente; nessuna duplicazione. |
| Kth Largest Element in an Array | LeetCode75 | Heap / Priority Queue | sde-l-heap | sde-e-kth-largest | Diretta | Già presente; nessuna duplicazione. |
| Kth Smallest Element in a BST | Blind75, Grind75 | BST inorder: kth value | sde-l-bst-paths | sde-e-kth-smallest | Diretta | Aggiunto in questa revisione; Extended. |
| Largest Rectangle in Histogram | Grind75 | Monotonic stack | sde-l-monotonic-stack | sde-e-largest-rectangle | Diretta | Già presente; nessuna duplicazione. |
| Leaf-Similar Trees | LeetCode75 | Trees: recursive DFS | sde-l-tree-traversal | — | Parziale | La DFS è spiegata; manca il confronto delle sequenze di foglie. |
| Letter Combinations of a Phone Number | Grind75, LeetCode75 | Backtracking | sde-l-backtracking | sde-e-combination-sum | Equivalente | Riusa un modello equivalente; Extended. |
| Linked List Cycle | Blind75, Grind75 | Linked lists: fast/slow | sde-l-linked-lists | sde-e-linked-list-cycle | Diretta | Già presente; nessuna duplicazione. |
| Longest Common Subsequence | Blind75, LeetCode75 | Two-prefix DP | sde-l-dp-memoization | — | Parziale | La DP su due prefissi è vicina all'Edit Distance; non si pratica la ricorrenza LCS. |
| Longest Consecutive Sequence | Blind75 | HashSet: sequence starts | sde-l-hashmap-set | sde-e-longest-consecutive | Diretta | Aggiunto in questa revisione; Extended. |
| Longest Increasing Subsequence | Blind75 | O(n^2) DP, then tails | sde-l-dp-memoization | sde-e-lis | Diretta | Aggiunto in questa revisione; Extended. |
| Longest Palindrome | Grind75 | HashMap / Set / frequency | sde-l-hashmap-set | sde-e-valid-anagram | Equivalente | Riusa un modello equivalente; Core. |
| Longest Palindromic Substring | Blind75, Grind75 | Expand around center | sde-l-two-pointers | sde-e-palindromic-substrings | Equivalente | Riusa un modello equivalente; Extended. |
| Longest Repeating Character Replacement | Blind75 | Sliding window + frequencies | sde-l-sliding-window | sde-e-character-replacement | Diretta | Già presente; nessuna duplicazione. |
| Longest Subarray of 1's After Deleting One Element | LeetCode75 | Sliding window with one deletion | sde-l-sliding-window | sde-e-character-replacement | Equivalente | Riusa un modello equivalente; Extended. |
| Longest Substring Without Repeating Characters | Blind75, Grind75 | Sliding window + last-seen indices | sde-l-sliding-window | sde-e-longest-substring | Diretta | Già presente; nessuna duplicazione. |
| Longest ZigZag Path in a Binary Tree | LeetCode75 | Trees: recursive DFS | sde-l-tree-traversal, sde-l-dp-memoization | — | Parziale | La DFS è spiegata; non si pratica lo stato direzionale dei sottoalberi. |
| Lowest Common Ancestor of a Binary Search Tree | Blind75, Grind75 | Trees: BST ordering/inorder | sde-l-bst-paths | sde-e-lca-bst | Diretta | Già presente; nessuna duplicazione. |
| Lowest Common Ancestor of a Binary Tree | Blind75, Grind75, LeetCode75 | Trees: recursive DFS | sde-l-tree-traversal | — | Parziale | Si pratica la LCA in un BST; la variante su albero generico non può usare l'ordinamento BST. |
| LRU Cache | Grind75 | Array/string scan or data structure | sde-l-linked-lists | sde-e-lru-cache | Diretta | Già presente; nessuna duplicazione. |
| Majority Element | Grind75 | HashMap / Set / frequency | sde-l-hashmap-set | sde-e-majority-element | Diretta | Già presente; nessuna duplicazione. |
| Max Consecutive Ones III | LeetCode75 | Array/string scan or data structure | sde-l-sliding-window | sde-e-character-replacement | Equivalente | Riusa un modello equivalente; Extended. |
| Max Number of K-Sum Pairs | LeetCode75 | Prefix sum | sde-l-two-pointers | sde-e-two-sum-sorted | Equivalente | Riusa un modello equivalente; Core. |
| Maximum Average Subarray I | LeetCode75 | Sliding window | sde-l-sliding-window | — | Parziale | La finestra mobile è spiegata; manca un esercizio su finestre di lunghezza fissa. |
| Maximum Depth of Binary Tree | Blind75, Grind75, LeetCode75 | Trees: recursive DFS | sde-l-recursion | sde-e-max-depth | Diretta | Già presente; nessuna duplicazione. |
| Maximum Level Sum of a Binary Tree | LeetCode75 | Trees: BFS by levels | sde-l-tree-traversal | sde-e-tree-level-order | Equivalente | Riusa un modello equivalente; Extended. |
| Maximum Number of Vowels in a Substring of Given Length | LeetCode75 | Trees: BST ordering/inorder | sde-l-sliding-window | — | Parziale | La finestra mobile è spiegata; manca un esercizio su finestre di lunghezza fissa. |
| Maximum Product Subarray | Blind75 | Product Kadane: max/min states | sde-l-arrays-strings | sde-e-max-product-subarray | Diretta | Aggiunto in questa revisione; Extended. |
| Maximum Profit in Job Scheduling | Grind75 | Intervals / greedy scheduling | sde-l-sorting-intervals, sde-l-dp-models | — | Parziale | Si pratica la pianificazione non pesata; quella pesata richiede una DP diversa. |
| Maximum Subarray | Blind75, Grind75 | Kadane: best segment ending here | sde-l-arrays-strings | sde-e-max-subarray | Diretta | Già presente; nessuna duplicazione. |
| Maximum Subsequence Score | LeetCode75 | Sort + min-heap | sde-l-heap, sde-l-greedy | — | Parziale | Heap e greedy sono spiegati; non si pratica la combinazione basata sulla soglia del punteggio. |
| Maximum Twin Sum of a Linked List | LeetCode75 | Linked lists: fast/slow | sde-l-linked-lists | — | Parziale | Inversione e due puntatori sono spiegati; manca l'abbinamento tra metà della lista. |
| Meeting Rooms | Blind75 | Graphs/grids: BFS or DFS | sde-l-sorting-intervals | sde-e-meeting-rooms | Equivalente | Riusa un modello equivalente; Extended. |
| Meeting Rooms II | Blind75 | Heap of active end times | sde-l-sorting-intervals | sde-e-meeting-rooms | Diretta | Già presente; nessuna duplicazione. |
| Merge Intervals | Blind75, Grind75 | Intervals / greedy scheduling | sde-l-sorting-intervals | sde-e-merge-intervals | Diretta | Già presente; nessuna duplicazione. |
| Merge k Sorted Lists | Blind75, Grind75 | Array/string scan or data structure | sde-l-linked-lists | sde-e-merge-k-lists | Diretta | Già presente; nessuna duplicazione. |
| Merge Strings Alternately | LeetCode75 | Alternating index scan | sde-l-arrays-strings | sde-e-merge-strings | Diretta | Già presente; nessuna duplicazione. |
| Merge Two Sorted Lists | Blind75, Grind75 | Two-pointer merge of sorted linked lists | sde-l-linked-lists | — | Parziale | Si spiegano il riaggancio dei nodi e il merge k-way; non si pratica direttamente il merge di due liste con puntatori. |
| Middle of the Linked List | Grind75 | Linked lists: fast/slow | sde-l-linked-lists | sde-e-linked-list-cycle | Equivalente | Riusa un modello equivalente; Core. |
| Min Cost Climbing Stairs | LeetCode75 | Dynamic Programming / greedy | sde-l-dp-memoization | sde-e-climbing-stairs | Equivalente | Riusa un modello equivalente; Core. |
| Min Stack | Grind75 | Stack / Queue | sde-l-stack-queue | — | Parziale | Lo stack è spiegato; non si pratica l'estensione che mantiene il minimo in O(1). |
| Minimum Flips to Make a OR b Equal to c | LeetCode75 | Bit manipulation | — (non insegnato nel track) | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Minimum Height Trees | Grind75 | Array/string scan or data structure | sde-l-graphs | — | Parziale | Si spiega la visita dei grafi; non si pratica la rimozione iterativa delle foglie. |
| Minimum Number of Arrows to Burst Balloons | LeetCode75 | Intervals / greedy scheduling | sde-l-greedy | sde-e-interval-scheduling | Equivalente | Riusa un modello equivalente; Core. |
| Minimum Window Substring | Blind75, Grind75 | Sliding window + required counts | sde-l-sliding-window | sde-e-min-window | Diretta | Già presente; nessuna duplicazione. |
| Missing Number | Blind75 | Array/string scan or data structure | sde-l-problem-solving | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Move Zeroes | LeetCode75 | Two pointers | sde-l-arrays-strings | sde-e-move-zeroes | Diretta | Già presente; nessuna duplicazione. |
| N-th Tribonacci Number | LeetCode75 | Dynamic Programming / greedy | sde-l-dp-memoization | sde-e-climbing-stairs | Equivalente | Riusa un modello equivalente; Core. |
| Nearest Exit from Entrance in Maze | LeetCode75 | Graphs/grids: BFS or DFS | sde-l-graphs | sde-e-oranges-rotting | Equivalente | Riusa un modello equivalente; Core. |
| Non-overlapping Intervals | Blind75, LeetCode75 | Greedy by earliest finish | sde-l-greedy | sde-e-interval-scheduling | Equivalente | Riusa un modello equivalente; Core. |
| Number of 1 Bits | Blind75 | Bit manipulation | — (non insegnato nel track) | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Number of Connected Components in an Undirected Graph | Blind75 | Graphs: connectivity/components | sde-l-graphs | sde-e-connected-components | Diretta | Già presente; nessuna duplicazione. |
| Number of Islands | Blind75, Grind75 | DFS/BFS over grid components | sde-l-bfs-dfs-grid | sde-e-number-islands | Diretta | Già presente; nessuna duplicazione. |
| Number of Provinces | LeetCode75 | Graphs: connectivity/components | sde-l-graphs | sde-e-connected-components | Equivalente | Riusa un modello equivalente; Core. |
| Number of Recent Calls | LeetCode75 | Stack / Queue | sde-l-stack-queue | — | Parziale | La coda è usata nella BFS; manca una coda con finestra temporale. |
| Odd Even Linked List | LeetCode75 | Linked lists: pointer rewiring | sde-l-linked-lists | — | Parziale | Si spiega il riaggancio; manca la partizione stabile in base alla posizione. |
| Online Stock Span | LeetCode75 | Monotonic stack with spans | sde-l-monotonic-stack | sde-e-daily-temperatures | Equivalente | Riusa un modello equivalente; Core. |
| Pacific Atlantic Water Flow | Blind75 | Reverse BFS/DFS + intersection | sde-l-bfs-dfs-grid | sde-e-pacific-atlantic | Diretta | Aggiunto in questa revisione; Extended. |
| Palindromic Substrings | Blind75 | Expand around center | sde-l-two-pointers | sde-e-palindromic-substrings | Diretta | Aggiunto in questa revisione; Extended. |
| Partition Equal Subset Sum | Grind75 | Dynamic Programming / greedy | sde-l-dp-memoization, sde-l-dp-models | — | Parziale | La DP è spiegata; non si pratica lo stato dello zaino 0/1. |
| Path Sum III | LeetCode75 | Prefix sum | sde-l-tree-traversal, sde-l-prefix-sum | — | Parziale | Prefissi e DFS sono spiegati separatamente; manca la loro combinazione sui cammini dell'albero. |
| Permutations | Grind75 | Backtracking | sde-l-problem-solving | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Product of Array Except Self | Blind75, Grind75, LeetCode75 | Prefix/suffix products | sde-l-prefix-sum | sde-e-product-except-self | Diretta | Già presente; nessuna duplicazione. |
| Ransom Note | Grind75 | HashMap / Set / frequency | sde-l-hashmap-set | sde-e-valid-anagram | Equivalente | Riusa un modello equivalente; Core. |
| Remove Nth Node From End of List | Blind75 | Fast/slow with fixed gap and dummy | sde-l-linked-lists | sde-e-remove-nth-from-end | Diretta | Aggiunto in questa revisione; Extended. |
| Removing Stars From a String | LeetCode75 | Stack / Queue | sde-l-stack-queue | — | Parziale | Lo stack è spiegato; non si pratica questa regola di cancellazione. |
| Reorder List | Blind75 | Array/string scan or data structure | sde-l-problem-solving | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Reorder Routes to Make All Paths Lead to the City Zero | LeetCode75 | Graphs/grids: BFS or DFS | sde-l-graphs | — | Parziale | La visita del grafo è spiegata; manca il conteggio degli archi da invertire. |
| Reverse Bits | Blind75 | Bit manipulation | — (non insegnato nel track) | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Reverse Linked List | Blind75, Grind75, LeetCode75 | Linked lists: pointer rewiring | sde-l-linked-lists | sde-e-reverse-list | Diretta | Già presente; nessuna duplicazione. |
| Reverse Vowels of a String | LeetCode75 | Sliding window | sde-l-two-pointers | sde-e-valid-palindrome | Equivalente | Riusa un modello equivalente; Core. |
| Reverse Words in a String | LeetCode75 | Array/string scan or data structure | sde-l-arrays-strings | — | Parziale | Si spiegano le scansioni di stringhe; manca un esercizio di tokenizzazione. |
| Rotate Image | Blind75 | Array/string scan or data structure | sde-l-arrays-strings | — | Parziale | Si spiegano indici e scambi; manca la trasformazione bidimensionale. |
| Rotting Oranges | Grind75, LeetCode75 | Multi-source BFS by layers | sde-l-graphs | sde-e-oranges-rotting | Diretta | Già presente; nessuna duplicazione. |
| Same Tree | Blind75 | Trees: recursive DFS | sde-l-tree-traversal | sde-e-same-tree | Diretta | Aggiunto in questa revisione; Extended. |
| Search in a Binary Search Tree | LeetCode75 | Trees: BST ordering/inorder | sde-l-binary-search, sde-l-binary-boundaries, sde-l-binary-variants, sde-l-binary-answer | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Search in Rotated Sorted Array | Blind75, Grind75 | Binary search in sorted half | sde-l-binary-variants | sde-e-search-rotated | Diretta | Già presente; nessuna duplicazione. |
| Search Suggestions System | LeetCode75 | Trie + prefixes | sde-l-trie, sde-l-backtracking | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Serialize and Deserialize Binary Tree | Grind75 | Preorder serialization + null markers | sde-l-tree-traversal | sde-e-serialize-tree | Diretta | Aggiunto in questa revisione; Extended. |
| Serialize and Deserialize BST | Blind75 | BST serialization | sde-l-tree-traversal | sde-e-serialize-tree | Equivalente | Riusa un modello equivalente; Extended. |
| Set Matrix Zeroes | Blind75 | Array/string scan or data structure | sde-l-bfs-dfs-grid | — | Parziale | Si spiega la visita delle matrici; manca la modifica coordinata di righe e colonne. |
| Single Number | LeetCode75 | Bitwise XOR | — (non insegnato nel track) | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Smallest Number in Infinite Set | LeetCode75 | Heap / Priority Queue | sde-l-heap | — | Parziale | L'heap è spiegato; non si praticano appartenenza ordinata e reinserimento. |
| Sort Colors | Grind75 | Array/string scan or data structure | sde-l-two-pointers | — | Parziale | Si pratica la compattazione in-place; non la partizione in tre gruppi. |
| Spiral Matrix | Blind75, Grind75 | Array/string scan or data structure | sde-l-bfs-dfs-grid | — | Parziale | Si spiega la visita delle griglie; non si esercitano i confini a spirale. |
| String Compression | LeetCode75 | Run-length + read/write compaction | sde-l-arrays-strings | sde-e-move-zeroes | Equivalente | Riusa un modello equivalente; Core. |
| String to Integer (atoi) | Grind75 | Array/string scan or data structure | sde-l-arrays-strings | — | Parziale | Si spiegano le scansioni di stringhe; mancano parsing numerico e gestione dell'overflow. |
| Subsets | Grind75 | Backtracking | sde-l-problem-solving | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Subtree of Another Tree | Blind75 | Trees: recursive DFS | sde-l-tree-traversal | sde-e-subtree | Diretta | Aggiunto in questa revisione; Extended. |
| Successful Pairs of Spells and Potions | LeetCode75 | Binary search / boundary | sde-l-binary-boundaries | sde-e-lower-bound | Equivalente | Riusa un modello equivalente; Extended. |
| Sum of Two Integers | Blind75 | Prefix sum | sde-l-arrays-strings, sde-l-prefix-sum | — | Escluso intenzionalmente | Fuori dal Core di sei giorni; non aggiungo un esercizio locale dedicato. |
| Task Scheduler | Grind75 | Intervals / greedy scheduling | sde-l-heap, sde-l-greedy | — | Parziale | Heap e greedy sono spiegati; non si pratica la pianificazione con cooldown. |
| Time Based Key-Value Store | Grind75 | Array/string scan or data structure | sde-l-hashmap-set, sde-l-binary-search | — | Parziale | Mappe e lower bound sono trattati separatamente; non si pratica la cronologia per chiave. |
| Top K Frequent Elements | Blind75 | Heap / Priority Queue | sde-l-heap | sde-e-top-k-frequent | Diretta | Già presente; nessuna duplicazione. |
| Total Cost to Hire K Workers | LeetCode75 | Two min-heaps | sde-l-heap | — | Parziale | L'heap è spiegato; manca la selezione simultanea da due frontiere. |
| Trapping Rain Water | Grind75 | Two pointers: running bounds | sde-l-two-pointers | sde-e-trapping-rainwater | Diretta | Già presente; nessuna duplicazione. |
| Two Sum | Blind75, Grind75 | HashMap: lookup of the complement | sde-l-hashmap-set | sde-e-two-sum | Diretta | Già presente; nessuna duplicazione. |
| Unique Number of Occurrences | LeetCode75 | HashMap / Set / frequency | sde-l-hashmap-set | — | Parziale | Si spiegano le mappe di frequenza; manca il controllo che i conteggi siano tutti diversi. |
| Unique Paths | Blind75, Grind75, LeetCode75 | Dynamic Programming / greedy | sde-l-dp-models | sde-e-unique-paths | Diretta | Già presente; nessuna duplicazione. |
| Valid Anagram | Blind75, Grind75 | HashMap / Set / frequency | sde-l-hashmap-set | sde-e-valid-anagram | Diretta | Già presente; nessuna duplicazione. |
| Valid Palindrome | Blind75, Grind75 | Two pointers | sde-l-two-pointers | sde-e-valid-palindrome | Diretta | Già presente; nessuna duplicazione. |
| Valid Parentheses | Blind75, Grind75 | Stack / Queue | sde-l-stack-queue | sde-e-valid-parentheses | Diretta | Già presente; nessuna duplicazione. |
| Validate Binary Search Tree | Blind75, Grind75 | Trees: BST ordering/inorder | sde-l-bst-paths | sde-e-validate-bst | Diretta | Già presente; nessuna duplicazione. |
| Word Break | Blind75, Grind75 | Segmentation DP | sde-l-dp-models | sde-e-word-break | Diretta | Già presente; nessuna duplicazione. |
| Word Ladder | Grind75 | Graphs/grids: BFS or DFS | sde-l-graphs | sde-e-word-ladder | Diretta | Già presente; nessuna duplicazione. |
| Word Search | Blind75, Grind75 | Backtracking | sde-l-trie | sde-e-word-search-ii | Equivalente | Riusa un modello equivalente; Extended. |
| Word Search II | Blind75 | Trie + grid backtracking | sde-l-trie | sde-e-word-search-ii | Diretta | Aggiunto in questa revisione; Extended. |

## Gap dichiarati

- **Bit manipulation** (Counting Bits, Number of 1 Bits, Reverse Bits, Single Number, Minimum Flips): fuori dal track corrente; non è prerequisito del Core a sei giorni.
- **Parsing e scansioni specialistiche** (atoi, calcolatrici, codifica di stringhe, trasformazioni di matrici): non hanno task dedicati; alcuni riusano fondamenti già spiegati, ma non sono dichiarati coperti.
- **Grafi e DP composti**: valutare in futuro solo se il tempo lo consente; il track pratica i fondamenti senza imporre Union-Find o stati DP più avanzati come prerequisiti.
- La lezione Trie è facoltativa e fuori dal piano; Trie, wildcard e Word Search II hanno pratica Extended collegata, dopo backtracking e griglie.

## Riepilogo dell'integrazione DEV48

- Prima della revisione: 44 lezioni e 67 esercizi logici, ciascuno con varianti Python e C++.
- Dopo: 45 lezioni, di cui 1 facoltativa, e 89 esercizi logici: 25 Easy, 51 Medium, 13 Hard.
- Nuovi esercizi: 22 (3 Easy, 16 Medium, 3 Hard), tutti con varianti, soluzioni e test Python/C++; non cambiano il piano Core.
- Il piano conserva gli stessi sei giorni e gli stessi ID pianificati. Stima dell'intero catalogo: 55,7 → 66,5 ore (+10,8); stima Core: 37,8 ore invariata.
- Il confronto è un benchmark generale di pattern: non misura e non predice la copertura Amazon.
- Due titoli di serializzazione puntano allo stesso esercizio generico; per questo le righe di benchmark collegate ai nuovi esercizi possono superare di uno il numero degli esercizi aggiunti.
