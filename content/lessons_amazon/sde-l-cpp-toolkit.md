# C++ moderno e STL per gli esercizi DSA

Un `vector<int>` è la scelta normale per una sequenza modificabile; `string` è una sequenza di caratteri con indici da zero. Per lookup medio costante scegli `unordered_map` o `unordered_set`; `map` e `set` mantengono l'ordine e costano `O(log n)`. `pair<int,int>` è utile per portare insieme due coordinate senza creare una classe.

`stack`, `queue` e `deque` esprimono LIFO, FIFO e accesso a entrambe le estremità. `priority_queue<int>` è un max-heap; per il min-heap usa `greater<int>`. `sort`, `lower_bound` e `upper_bound` stanno in `<algorithm>`. Una lambda per ordinare intervalli è spesso sufficiente: `[](const auto& a, const auto& b) { return a[0] < b[0]; }`.

Una reference `const vector<int>&` evita una copia e impedisce alla funzione di modificare l'input. Il range-based `for (const auto& x : values)` è più sicuro che incrementare un indice quando non ti serve l'indice. `size()` restituisce un tipo unsigned: confrontarlo con `int` può produrre sorprese, soprattutto sottraendo uno da una sequenza vuota.

Per alberi e liste, un `struct TreeNode` con puntatori `left/right` e `nullptr` basta. Usa ricorsione quando il problema segue naturalmente i figli; conserva uno stato locale chiaro e valuta la profondità massima. Non serve ripassare template avanzati per risolvere un OA.

### Esempio svolto: leggere una sequenza senza copiarla

Considera tre rilevazioni `[18, 20, 17]`. Vogliamo contare quante superano 18. La funzione riceve il vector per riferimento costante: può leggere i valori, non modificarli e non deve creare una copia dell'intera sequenza.

```cpp
#include <vector>
using namespace std;

int count_above(const vector<int>& values, int limit) {
    int count = 0;
    for (const auto& value : values) {
        if (value > limit) {
            ++count;
        }
    }
    return count;
}
```

Seguiamo il ciclo: `18 > 18` è falso, quindi `count` resta 0; `20 > 18` è vero, quindi diventa 1; `17 > 18` è falso. La funzione restituisce 1 e il vector originale resta `[18, 20, 17]`. Il tempo è `O(n)` e la memoria aggiuntiva `O(1)`.

`const vector<int>&` descrive due scelte distinte: `&` evita la copia e `const` vieta la modifica attraverso quel parametro. `const auto&` applica la stessa cautela a ogni elemento del ciclo. Se servisse davvero cambiare la sequenza, la firma non dovrebbe nascondere quella mutazione.

Quando usi `size()`, ricorda che il tipo è unsigned. Per un vector vuoto, `size()-1` non vale -1: il risultato diventa un numero enorme. Controlla `empty()` prima di accedere all'ultimo indice; quando non ti serve l'indice, il range-based `for` evita proprio quel confine.

**Da ricordare.** In C++ il tipo del contenitore e il suo contratto contano quanto l'algoritmo: evita copie, dereferenziazioni invalide e mutazioni implicite. **Per praticare:** Mini-prova: finestra con somma massima; Cercare un valore ordinato.