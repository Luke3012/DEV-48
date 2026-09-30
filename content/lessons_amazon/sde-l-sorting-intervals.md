# Sorting e intervalli: ordinare per scoprire sovrapposizioni

Per sapere se una lista di riunioni contiene una sovrapposizione, il metodo diretto confronta ogni coppia (`O(n²)`). Ordinando per inizio, basta controllare ogni intervallo contro il termine più lontano raggiunto finora. Usiamo intervalli semiaperti: `[inizio,fine)`, così una riunione che comincia esattamente quando un'altra finisce può usare la stessa sala.

Considera l'input non ordinato `[5,8)`, `[1,4)`, `[3,6)`, `[8,9)`. Dopo l'ordinamento:

| Intervallo letto | Termine massimo precedente | Decisione |
| --- | ---: | --- |
| `[1,4)` | — | inizializza a 4 |
| `[3,6)` | 4 | `3 < 4`: c'è una sovrapposizione |

Il termine massimo è importante se gli intervalli sono annidati: guardare soltanto il precedente immediato potrebbe dimenticare un intervallo lungo che contiene gli altri.

**Versione Python**

```python
def has_overlap(intervals):
    ordered = sorted(intervals)
    if not ordered:
        return False
    furthest_end = ordered[0][1]
    for start, end in ordered[1:]:
        if start < furthest_end:
            return True
        furthest_end = max(furthest_end, end)
    return False
```

**Versione C++**

```cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

bool has_overlap(vector<pair<int, int>> intervals) {
    if (intervals.empty()) {
        return false;
    }
    sort(intervals.begin(), intervals.end());
    int furthest_end = intervals.front().second;
    for (int i = 1; i < static_cast<int>(intervals.size()); ++i) {
        if (intervals[i].first < furthest_end) {
            return true;
        }
        furthest_end = max(furthest_end, intervals[i].second);
    }
    return false;
}
```

L'ordinamento domina il tempo con `O(n log n)`; il controllo successivo è `O(n)`. Poiché si ordina una copia per mantenere intatto l'input, lo spazio aggiuntivo è `O(n)`. Rilevare una sovrapposizione è più semplice che fondere gli intervalli: la seconda operazione deve anche costruire i nuovi estremi e gestire intervalli contenuti.

La condizione del confine appartiene al contratto: con intervalli chiusi `[1,3]` e `[3,5]` si toccano e qui vengono fusi; con intervalli semiaperti `[1,3)` e `[3,5)` una riunione finita alle 3 libera la sala per quella che inizia alle 3. Merge Intervals e Meeting Rooms si basano entrambi sull'ordine temporale, ma rispondono a domande diverse.

### Casi da chiarire prima di fondere

Considera un intervallo contenuto in un altro: fondere `[2,8]` con `[3,5]` deve lasciare `[2,8]`, non accorciare la fine. Per questo si usa `max(fine_corrente, fine_nuova)`.

Per `Meeting Rooms`, in `[1,3)` e `[3,5)` la seconda riunione riusa la sala: il primo intervallo termina prima che il successivo cominci. Non confondere il conteggio di sovrapposizioni simultanee con la produzione di intervalli uniti. In entrambi i problemi ordini i confini, ma la variabile che mantieni e la risposta richiesta cambiano.

**Da ricordare.** Ordinare rende locale il confronto, mentre la convenzione sugli estremi resta parte del contratto e va mantenuta nei test. **Per praticare:** Fondere finestre sovrapposte; Numero minimo di sale per riunioni; Inserimento e fusione di un intervallo.