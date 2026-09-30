# Binary Search classica: dimezzare uno spazio ordinato

Una ricerca lineare può dover controllare tutti gli `n` elementi. Se i valori sono ordinati, ogni confronto al centro dell'intervallo può eliminare circa metà dei candidati. La ricerca binaria usa l'intervallo chiuso `[left,right]`: entrambi gli estremi possono ancora contenere la risposta; quando `left > right`, non è rimasto alcun indice.

In `[1,3,5,8,12]`, cerca 8. Inizialmente `left=0`, `right=4`, quindi `mid=2`: il valore 5 è minore del target e tutti gli indici fino a 2 possono essere scartati. L'intervallo residuo è `[3,4]`. Il suo medio è 3, dove si trova 8.

| Passo | `left` | `mid` | `right` | `nums[mid]` | Nuovo intervallo |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0 | 2 | 4 | 5 | `[3,4]` |
| 2 | 3 | 3 | 4 | 8 | trovato all'indice 3 |

**Versione Python**

```python
def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Versione C++**

```cpp
#include <vector>
using namespace std;

int binary_search_index(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;

    while (left <= right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        }
        if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}
```

Il test `left <= right` include l'intervallo con un solo candidato. Aggiornare a `mid+1` o `mid-1` lo elimina dopo averlo confrontato, quindi il ciclo avanza. Per un target assente, ad esempio 9, i confini diventano prima `[4,4]`, poi `[5,4]` e terminano. Se l'array è vuoto, `right=-1` e non si accede a `nums[0]`.

Ogni iterazione circa dimezza i candidati: dopo `k` passi ne restano al più `n/2^k`; servono quindi `O(log n)` confronti e `O(1)` spazio. In C++ il calcolo `left+(right-left)/2` evita l'overflow che può causare `(left+right)/2`. La condizione decisiva è l'ordine: senza una sequenza ordinata o un predicato monotono non puoi scartare una metà in base al valore centrale.

### Un errore plausibile: conservare il medio

Con l'intervallo chiuso, dopo aver confrontato `mid` quel valore è già stato escluso, quindi gli aggiornamenti usano `mid+1` o `mid-1`. Se al posto di `right = mid-1` scrivi `right = mid`, e il target è minore del valore al centro di un intervallo di due elementi, `mid` può restare uguale: il ciclo non termina. Un invariante scritto prima del codice rende visibile il problema.

Questo schema trova una qualsiasi occorrenza. Con duplicati non promette la prima: Lower Bound e Upper Bound cercano un confine e adottano un intervallo semiaperto, con aggiornamenti leggermente diversi.

**Da ricordare.** La binary search è una prova ripetuta che una metà non può contenere la risposta; l'invariante decide gli aggiornamenti. **Per praticare:** Cercare un valore ordinato.