# Big-O e vincoli: capire quando una risposta è troppo lenta

Se raddoppi `n`, un passaggio lineare fa circa il doppio del lavoro; due cicli annidati spesso ne fanno quattro volte tanto. Quella differenza diventa visibile quando i vincoli passano da 100 a 100.000. L'esempio non deve essere cronometrato al millisecondo: serve a scartare una famiglia di soluzioni incompatibile con la scala.

Contiamo le coppie di posizioni con lo stesso valore in `[1,2,1,2]`. Consideriamo ogni coppia una volta sola:

| `i` | `j` provati | Confronti uguali |
| ---: | --- | --- |
| 0 | 1, 2, 3 | `(0,2)` |
| 1 | 2, 3 | `(1,3)` |
| 2 | 3 | nessuno |

Sono sei confronti, cioè `3+2+1`. In generale il ciclo esterno sceglie `n` posizioni e quello interno ne prova `n-1`, poi `n-2` e così via: il totale è `n(n-1)/2`, che cresce come `O(n²)`.

**Versione Python**

```python
def count_equal_pairs(values):
    count = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                count += 1
    return count
```

**Versione C++**

```cpp
#include <vector>

int count_equal_pairs(const std::vector<int>& values) {
    int count = 0;
    for (std::size_t i = 0; i < values.size(); ++i) {
        for (std::size_t j = i + 1; j < values.size(); ++j) {
            if (values[i] == values[j]) {
                ++count;
            }
        }
    }
    return count;
}
```

Le due implementazioni confrontano `(0,2)` e `(1,3)`, quindi restituiscono 2. Anche se nessun valore coincide, ogni coppia viene comunque controllata: l'input senza match impedisce che un'uscita anticipata nasconda il lavoro peggiore. Lo spazio extra resta `O(1)` perché bastano indici e contatore.

Una ricerca binaria dimezza lo spazio a ogni confronto e richiede `O(log n)`, ma l'array deve essere ordinato o la condizione deve essere monotona. Ordinare prima costa `O(n log n)`. Una mappa può portare lookup medio a `O(1)` pagando spazio `O(n)`; non è «gratis», è uno scambio esplicito.

Quando leggi i constraints, cerca numeri massimi, valori negativi, duplicati e input vuoti. Se `n` arriva a 200.000, `O(n²)` è quasi sempre un segnale d'allarme. Per distinguere una scansione lineare da un doppio ciclo, prova anche un input grande senza risposta che consenta di interrompere subito.

La complessità spaziale conta quanto quella temporale: una soluzione che copia una matrice può passare i test piccoli e superare la memoria. Specifica se lo spazio ausiliario cresce con l'input o se stai modificando la struttura ricevuta.

### Esempio svolto: da un ciclo al suo costo

Un doppio ciclo che confronta ogni coppia distinta non esegue `n × n` confronti, perché non confronta un elemento con sé stesso e non ripete le coppie al contrario. Con quattro elementi, il primo indice ha 3 valori successivi da provare, il secondo ne ha 2, il terzo ne ha 1 e l'ultimo ne ha 0: `3 + 2 + 1 + 0 = 6` confronti.

| Elementi `n` | Confronti | Formula |
| ---: | ---: | --- |
| 4 | 6 | `3 + 2 + 1 + 0` |
| 8 | 28 | `7 + 6 + ... + 1 + 0` |
| 100 | 4.950 | `100 × 99 / 2` |

La formula generale è `n(n-1)/2`. Il termine dominante è `n²`, perciò la classe di crescita è `O(n²)`. Una singola scansione che visita ogni elemento una volta fa invece 4, 8 e 100 visite: è `O(n)`. Non abbiamo cronometrato il computer; abbiamo contato operazioni che crescono con l'input.

Per stimare lo spazio, fai una domanda separata: «che cosa resta allocato mentre elaboro tutti gli elementi?». Due indici e un contatore occupano `O(1)` spazio aggiuntivo; un dizionario con una voce per ogni valore distinto cresce fino a `O(n)`. La lista restituita fa parte dell'output e va distinta dalla memoria ausiliaria. Big-O descrive questa crescita, non i millisecondi esatti.

**Da ricordare.** Descrivi quante volte vengono visitati gli elementi e quale memoria cresce con n; poi confronta la stima coi vincoli. **Per praticare:** Due valori che completano il target; Rilevare un duplicato senza ordinare.