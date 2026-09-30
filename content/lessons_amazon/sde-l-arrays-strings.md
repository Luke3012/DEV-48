# Array e stringhe: scansione, indici e mutazioni

Un array offre accesso diretto alla posizione `i`: leggere `nums[i]` costa `O(1)`, ma inserire nel mezzo sposta in genere gli elementi successivi e costa `O(n)`. Prima di scorrere, dichiara quale intervallo stai visitando. `[left,right)` include `left` ed esclude `right`, quindi ha lunghezza `right-left`; se è vuoto, i due estremi coincidono. Questa convenzione si incastra bene con gli slicing Python e con l'intervallo di iteratori C++.

Per capire la scansione in-place, teniamo solo i valori pari in `[3,4,7,2,5]`, conservandone l'ordine. Una soluzione con un array nuovo è semplice, ma usa spazio proporzionale all'input. Con due indici possiamo invece leggere ogni posizione e scrivere i valori che ci interessano nel prefisso già elaborato.

Su `[3,4,7,2,5]`, la traccia è:

| `read` | Valore letto | Azione | Array dopo l'azione |
| ---: | ---: | --- | --- |
| 0 | 3 | salta; `write` resta 0 | `[3,4,7,2,5]` |
| 1 | 4 | scrivi in posizione 0; `write` diventa 1 | `[4,4,7,2,5]` |
| 2 | 7 | salta | `[4,4,7,2,5]` |
| 3 | 2 | scrivi in posizione 1; `write` diventa 2 | `[4,2,7,2,5]` |
| 4 | 5 | salta | `[4,2,7,2,5]` |

Alla fine il risultato è il prefisso di lunghezza 2, `[4,2]`; ciò che resta oltre quel prefisso non fa parte del risultato.

**Versione Python**

```python
def compact_even_values(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] % 2 == 0:
            nums[write] = nums[read]
            write += 1
    return write
```

**Versione C++**

```cpp
#include <vector>
using namespace std;

int compact_even_values(vector<int>& nums) {
    int write = 0;
    for (int read = 0; read < static_cast<int>(nums.size()); ++read) {
        if (nums[read] % 2 == 0) {
            nums[write] = nums[read];
            ++write;
        }
    }
    return write;
}
```

La variabile `write` non supera mai `read`: non sovrascrivi quindi dati che non hai ancora esaminato. Ogni elemento viene letto una volta e gli elementi conservati vengono riscritti al massimo una volta; il tempo è `O(n)` e lo spazio aggiuntivo `O(1)`. La funzione muta l'input e comunica la lunghezza valida: chi la chiama deve usare solo quel prefisso.

Un accumulatore diverso risolve il massimo segmento contiguo. Per ogni posizione, il miglior segmento che termina lì o riparte dal valore corrente, oppure si estende aggiungendo quel valore alla somma precedente. Inizializza dal primo elemento: un array tutto negativo deve restituire il meno negativo, non zero.

**Versione Python**

```python
def max_subarray(nums):
    if not nums:
        raise ValueError("serve almeno un elemento")

    best_ending_here = nums[0]
    best = nums[0]
    for i in range(1, len(nums)):
        value = nums[i]
        best_ending_here = max(value, best_ending_here + value)
        best = max(best, best_ending_here)
    return best
```

**Versione C++**

```cpp
#include <algorithm>
#include <stdexcept>
#include <vector>
using namespace std;

long long max_subarray(const vector<int>& nums) {
    if (nums.empty()) {
        throw invalid_argument("serve almeno un elemento");
    }

    long long best_ending_here = nums[0];
    long long best = nums[0];
    for (int i = 1; i < static_cast<int>(nums.size()); ++i) {
        best_ending_here = max(static_cast<long long>(nums[i]), best_ending_here + nums[i]);
        best = max(best, best_ending_here);
    }
    return best;
}
```

Per `[-2,3,-1,4,-6]`, la somma migliore che termina in ciascuna posizione diventa `-2, 3, 2, 6, 0`; il massimo osservato è 6. Ogni elemento produce un solo aggiornamento: `O(n)` tempo e `O(1)` spazio. Array e stringhe condividono gli indici, ma le stringhe sono immutabili in Python; quando la risposta è una nuova stringa, anche costruirla richiede spazio proporzionale alla sua lunghezza.

### Esempio svolto: leggere un intervallo senza sbagliare il confine

Molte API rappresentano una porzione con `[left, right)`: l'indice `left` è incluso e `right` è escluso. Con `values = [10, 20, 30, 40]`, scegliendo `left = 1` e `right = 3` leggi gli elementi agli indici 1 e 2, cioè `[20, 30]`. La lunghezza è `right - left = 2`.

| Valori di `left` e `right` | Indici letti | Risultato |
| --- | --- | --- |
| `0, 4` | `0, 1, 2, 3` | `[10, 20, 30, 40]` |
| `1, 3` | `1, 2` | `[20, 30]` |
| `2, 2` | nessuno | intervallo vuoto `[]` |

Il caso `left == right` è valido e vuoto; non devi leggere `values[right]`. Per questo la condizione tipica di un ciclo è `i < right`, non `i <= right`. La stessa convenzione rende più semplice calcolare la lunghezza e concatenare porzioni adiacenti senza contare due volte il confine.

Nel compattamento in-place della lezione, `read` indica il prossimo elemento da esaminare e `write` la prossima posizione del prefisso valido. Se nessun elemento supera il filtro, `write` rimane 0: il risultato è un prefisso vuoto anche se la vecchia memoria dell'array contiene ancora valori oltre il confine. Chi usa il risultato deve rispettare la lunghezza restituita.

**Da ricordare.** Gli indici di lettura e scrittura rendono esplicito il prefisso già valido; inizializza gli accumuli in base ai casi ammessi. **Per praticare:** Compattare i valori non nulli; Massima somma di un segmento contiguo; Miglior guadagno da un acquisto e una vendita.