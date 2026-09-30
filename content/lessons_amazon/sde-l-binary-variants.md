# Ricerca binaria in un array ruotato

Una rotazione sposta un prefisso in fondo: `[1,2,3,4,5,6,7,8]` può diventare `[6,7,8,1,2,3,4,5]`. L'intero array non è ordinato, ma il confronto tra `nums[mid]` e `nums[right]` rivela da quale lato si trova il minimo. Prima impariamo a trovare quel confine; per cercare un target, l'esercizio aggiunge poi il controllo di appartenenza alla metà crescente.

Con `[6,7,8,1,2,3,4,5]`, il medio iniziale vale 1 ed è minore di 5: il minimo è nel tratto `[left,mid]`, quindi `right=mid`. Al passo successivo `nums[mid]=7` supera `nums[right]=1`, perciò il minimo deve stare a destra e spostiamo `left` oltre `mid`.

| Passo | `left` | `mid` | `right` | `nums[mid]` / `nums[right]` | Decisione |
| ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0 | 3 | 7 | 1 / 5 | minimo a sinistra o in `mid` → `right=3` |
| 2 | 0 | 1 | 3 | 7 / 1 | minimo a destra → `left=2` |
| 3 | 2 | 2 | 3 | 8 / 1 | minimo a destra → `left=3` |

**Versione Python**

```python
def minimum_rotated(nums):
    if not nums:
        raise ValueError("serve almeno un elemento")
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]
```

**Versione C++**

```cpp
#include <stdexcept>
#include <vector>
using namespace std;

int minimum_rotated(const vector<int>& nums) {
    if (nums.empty()) {
        throw invalid_argument("serve almeno un elemento");
    }
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;

    while (left < right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] > nums[right]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return nums[left];
}
```

Con valori distinti, il confronto elimina almeno metà dei candidati; il costo è `O(log n)` tempo e `O(1)` spazio. Un array già ordinato restituisce il primo elemento. I duplicati possono rendere uguali gli estremi e nascondere da quale lato è avvenuta la rotazione; il codice non li ammette.

### Quando i duplicati nascondono la rotazione

Se `nums[left]`, `nums[mid]` e `nums[right]` sono uguali, il confronto non rivela quale metà contenga il taglio. Puoi ridurre un estremo di un elemento senza perdere una soluzione, ma in un array di molti valori uguali ciò richiede `O(n)` passi. L'esercizio dichiara valori distinti, quindi il codice può garantire `O(log n)`.

Questa ricerca cerca un elemento in una sequenza ruotata. Binary Search on Answer non confronta i valori dell'array: ordina il dominio di una possibile risposta e cerca dove un predicato passa da falso a vero.

### Cercare il minimo di un array ruotato

Con valori distinti confronta `nums[mid]` con `nums[right]`. Se il medio è maggiore, il minimo deve trovarsi dopo `mid`; altrimenti il minimo è tra `left` e `mid`, incluso il medio. Per `[8,9,12,2,4,6]`, il confronto sposta prima `left` verso 3, poi conserva l'intervallo che contiene 2. L'invariante è che il minimo resta sempre dentro l'intervallo chiuso `[left,right]`; quando gli estremi coincidono hai la risposta.

**Da ricordare.** La rotazione conserva una metà ordinata; restringi l'intervallo in base ai suoi estremi e alle ipotesi sui duplicati. **Per praticare:** Ricerca binaria in un array ruotato; Minimo in un array ruotato.