# Greedy e scheduling: dimostrare la scelta locale

Per massimizzare il numero di intervalli compatibili, supponiamo intervalli semiaperti `[inizio,fine)`: uno che termina alle 3 può essere seguito da uno che inizia alle 3. La scelta locale è prendere l'intervallo disponibile che finisce prima. Lascia più tempo possibile alle decisioni successive.

Con `[1,10)`, `[2,3)` e `[3,4)`, ordinando per fine si considera prima `[2,3)`, poi `[3,4)`: entrambi entrano e il lungo `[1,10)` viene scartato. La scelta “inizia prima” avrebbe preso il lungo e ottenuto un solo intervallo invece di due.

La ragione di correttezza è un argomento di scambio. In una soluzione ottima, sia `O` il primo intervallo; il greedy sceglie `G`, il cui termine non è successivo a quello di `O`. Sostituire `O` con `G` non rende incompatibili gli intervalli successivi, quindi esiste una soluzione ottima che comincia con la scelta greedy. Ripetere il ragionamento dopo quell'intervallo dimostra l'intera strategia.

**Versione Python**

```python
def max_compatible_intervals(intervals):
    ordered = sorted(intervals, key=lambda interval: interval[1])
    selected = []
    last_end = None

    for start, end in ordered:
        if last_end is None or start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected
```

**Versione C++**

```cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

vector<pair<int, int>> max_compatible_intervals(vector<pair<int, int>> intervals) {
    sort(intervals.begin(), intervals.end(), [](const auto& first, const auto& second) {
        if (first.second != second.second) {
            return first.second < second.second;
        }
        return first.first < second.first;
    });

    vector<pair<int, int>> selected;
    for (const auto& interval : intervals) {
        if (selected.empty() || interval.first >= selected.back().second) {
            selected.push_back(interval);
        }
    }
    return selected;
}
```

L'ordinamento costa `O(n log n)` e la scansione `O(n)`; la copia ordinata e l'output usano `O(n)` spazio. Greedy non funziona soltanto perché una scelta sembra ragionevole: “prendi l'intervallo più corto” fallisce con `[1,4)`, `[4,7)` e `[3,5)`. Il terzo è più corto ma impedisce di scegliere i primi due, che sono compatibili fra loro. Ogni algoritmo greedy richiede una dimostrazione legata al suo obiettivo e ai suoi vincoli.

### Quando lo scheduling richiede DP

Se ogni intervallo ha un profitto, massimizzare il numero di intervalli non equivale a massimizzare il profitto. Due intervalli brevi compatibili possono valere 2 ciascuno mentre un intervallo lungo incompatibile vale 100: la regola del primo termine non risponde più alla domanda. Serve confrontare il profitto con la migliore soluzione prima dell'intervallo compatibile più vicino, una transizione da dynamic programming.

Anche i confini fanno parte dell'input: per `[start,end)` il contatto è compatibile con `start >= last_end`; se gli estremi sono inclusivi, serve una regola diversa. Cambiare una sola convenzione può modificare il numero di intervalli selezionati.

### Intervalli: liberare presto la linea temporale

Per conservare il massimo numero di attività compatibili, ordina per ora di fine e scegli l'attività che termina prima; dopo averla scelta, accetta la prossima che inizia non prima di quella fine. Una fine anticipata lascia almeno lo stesso spazio residuo di una scelta che termina più tardi. Con `[1,3)`, `[2,4)`, `[3,5)`, scegli la prima e la terza: gli intervalli che si toccano sono compatibili secondo il contratto semiaperto.

Per rimuovere il minimo numero di intervalli sovrapposti calcoli il complemento di quelli conservati. Jump Game usa invece un'altra frontiera greedy: `farthest` riassume fino a dove puoi arrivare dalle posizioni già visitate. Se l'indice corrente la supera, il traguardo non è raggiungibile.

**Da ricordare.** Una scelta greedy richiede una dimostrazione che le decisioni locali possano essere estese a una soluzione ottima. **Per praticare:** Selezionare il massimo numero di intervalli compatibili; Verificare se si può raggiungere l'ultima posizione.