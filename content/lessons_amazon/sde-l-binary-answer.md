# Binary Search on Answer: trovare la soglia fattibile

Qui non cerchi un elemento già presente: ordini i valori possibili di una risposta e verifichi quale rispetta il vincolo. Una nave deve trasportare in ordine i pesi `[3,2,2,4,1,4]` entro 3 giorni; non si può dividere un pacco fra giorni diversi. Una capacità maggiore non può richiedere più giorni, quindi le capacità fattibili hanno la forma `no, no, ..., sì, sì`. Questa monotonia permette di cercare la capacità minima.

La capacità non può essere minore del pacco più pesante e quella totale è sicuramente sufficiente: `low=4`, `high=16`. Se `mid` è fattibile, potrebbe essere la risposta o essercene una minore, quindi conserviamo `high=mid`; se non lo è, `mid` e tutte le capacità inferiori sono escluse.

| `low` | `mid` | `high` | Giorni necessari | Decisione |
| ---: | ---: | ---: | ---: | --- |
| 4 | 10 | 16 | 2 | sì → `high=10` |
| 4 | 7 | 10 | 3 | sì → `high=7` |
| 4 | 5 | 7 | 4 | no → `low=6` |
| 6 | 6 | 7 | 3 | sì → `high=6` |

Quando `low==high`, la capacità minima è 6.

**Versione Python**

```python
def min_capacity(weights, days):
    if not weights or days <= 0:
        raise ValueError("servono pesi e almeno un giorno")

    def days_needed(capacity):
        required = 1
        load = 0
        for weight in weights:
            if load + weight > capacity:
                required += 1
                load = 0
            load += weight
        return required

    low = max(weights)
    high = sum(weights)
    while low < high:
        mid = low + (high - low) // 2
        if days_needed(mid) <= days:
            high = mid
        else:
            low = mid + 1
    return low
```

**Versione C++**

```cpp
#include <algorithm>
#include <numeric>
#include <stdexcept>
#include <vector>
using namespace std;

long long min_capacity(const vector<int>& weights, int days) {
    if (weights.empty() || days <= 0) {
        throw invalid_argument("servono pesi e almeno un giorno");
    }

    auto days_needed = [&](long long capacity) {
        int required = 1;
        long long load = 0;
        for (int weight : weights) {
            if (load + weight > capacity) {
                ++required;
                load = 0;
            }
            load += weight;
        }
        return required;
    };

    long long low = *max_element(weights.begin(), weights.end());
    long long high = accumulate(weights.begin(), weights.end(), 0LL);
    while (low < high) {
        const long long mid = low + (high - low) / 2;
        if (days_needed(mid) <= days) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}
```

Ogni verifica assegna un pacco a un giorno e visita al massimo `n` pesi; la ricerca dimezza le capacità tra il pacco più pesante e la somma totale, quindi il tempo è `O(n log S)`, con `S` pari alla somma dei pesi, e lo spazio ausiliario `O(1)`. La verifica riempie il giorno corrente finché il prossimo pacco entra; se non entra, apre il successivo. Si assume che ogni peso sia positivo e che almeno un giorno sia disponibile.

### Prima dimostra gli estremi

Non basta che il predicato sia monotono: almeno una risposta valida deve stare in `[low,high]`. Per il problema delle pile, `low=1` è la velocità minima positiva; `high=max(piles)` svuota ogni pila in un'ora, quindi è una soluzione se `hours >= len(piles)`. Se quest'ultima condizione manca, non c'è risposta nel dominio.

Il codice usa un intervallo chiuso che contiene un valore fattibile. È diverso dalla convenzione che conserva esplicitamente un punto falso e uno vero escluso: entrambe funzionano, ma non vanno mischiate nello stesso aggiornamento.

**Da ricordare.** Binary Search on Answer richiede una risposta ordinabile, un predicato monotono e limiti che racchiudono una risposta valida. **Per praticare:** Velocità minima per finire entro h ore.