# Lower Bound e Upper Bound: trovare un confine, non un elemento

Con duplicati, cercare una qualsiasi occorrenza non basta sempre. In `[1,2,2,2,5]`, il primo `2` è all'indice 1. Lower Bound trova il primo elemento `>= target`; non cerca di “indovinare” una copia, ma restringe il punto in cui cambia una condizione monotona.

L'intervallo di ricerca è semiaperto `[left,right)`: `right` può valere `n` e non è mai letto come indice. Per target 2, l'evoluzione è:

| `left` | `mid` | `right` | `nums[mid]` | Decisione |
| ---: | ---: | ---: | ---: | --- |
| 0 | 2 | 5 | 2 | il primo `>=2` può essere `mid`: `right=2` |
| 0 | 1 | 2 | 2 | può essere `mid`: `right=1` |
| 0 | 0 | 1 | 1 | è troppo piccolo: `left=1` |

Quando `left==right`, hai il confine. Una risposta pari a `n` è valida come punto di inserimento ma non come indice: prima di leggere `nums[left]`, controlla `left < n`.

**Versione Python**

```python
def lower_bound(nums, target):
    left = 0
    right = len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def upper_bound(nums, target):
    left = 0
    right = len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def equal_range(nums, target):
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return (-1, -1)
    after_last = upper_bound(nums, target)
    return (first, after_last - 1)
```

**Versione C++**

```cpp
#include <vector>
using namespace std;

int lower_bound_index(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size());
    while (left < right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return left;
}

int upper_bound_index(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size());
    while (left < right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] <= target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return left;
}
```

Il ciclo cerca un confine, non un valore specifico: a ogni passo mantiene i valori prima di `left` sotto la soglia e quelli da `right` in poi almeno pari alla soglia. Tempo `O(log n)`, spazio `O(1)`. La differenza tra le funzioni sta nel confronto: Lower Bound conserva il medio quando `nums[mid]` è già almeno il target; Upper Bound lo scarta quando è uguale. La libreria C++ offre entrambe in `<algorithm>` e Python in `bisect`; conoscere il significato degli indici resta necessario per controllare i target assenti.

### Intervallo degli indici uguali

Il range di un target usa Lower Bound per il primo indice con valore almeno pari e Upper Bound per il primo indice strettamente maggiore. Se il primo confine è `n` o punta a un valore diverso, l'elemento non c'è; altrimenti l'ultimo indice è `upper-1`. Su `[1,2,2,2,5]`, i confini sono 1 e 4 e il range è `[1,3]`.

Se cerchi una proprietà booleana invece di un numero, lo schema è lo stesso: individua il primo punto in cui il predicato passa da falso a vero. Binary Search on Answer fa questa ricerca sul dominio delle soluzioni e richiede una dimostrazione di monotonia.

**Da ricordare.** La ricerca di confine restituisce un punto fra elementi, che può coincidere con n; definisci il predicato prima del ciclo. **Per praticare:** Primo elemento non minore del target; Primo e ultimo indice del target; Primo indice che supera una soglia.