# C++ moderno e STL senza rumore

Un `vector<int>` è la scelta normale per una sequenza modificabile; `string` è una sequenza di caratteri con indici da zero. Per lookup medio costante scegli `unordered_map` o `unordered_set`; `map` e `set` mantengono l'ordine e costano `O(log n)`. `pair<int,int>` è utile per portare insieme due coordinate senza creare una classe.

`stack`, `queue` e `deque` esprimono LIFO, FIFO e accesso a entrambe le estremità. `priority_queue<int>` è un max-heap; per il min-heap usa `greater<int>`. `sort`, `lower_bound` e `upper_bound` stanno in `<algorithm>`. Una lambda per ordinare intervalli è spesso sufficiente: `[](const auto& a, const auto& b) { return a[0] < b[0]; }`.

Una reference `const vector<int>&` evita una copia e impedisce alla funzione di modificare l'input. Il range-based `for (const auto& x : values)` è più sicuro che incrementare un indice quando non ti serve l'indice. `size()` restituisce un tipo unsigned: confrontarlo con `int` può produrre sorprese, soprattutto sottraendo uno da una sequenza vuota.

Per alberi e liste, un `struct TreeNode` con puntatori `left/right` e `nullptr` basta. Usa ricorsione quando il problema segue naturalmente i figli; conserva uno stato locale chiaro e valuta la profondità massima. Non serve ripassare template avanzati per risolvere un OA.
