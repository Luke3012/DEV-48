# Prefissi e HashMap: somme di intervalli e prodotti senza divisione

Una somma cumulativa trasforma una domanda su un intervallo in una sottrazione. Definisci `prefix[i]` come la somma dei primi `i` valori: il vettore dei prefissi ha un elemento in più dell'input e comincia da zero. Per `[3,-2,4,1]` ottieni `[0,3,1,5,6]`. L'intervallo `[1,4)` vale `prefix[4]-prefix[1] = 6-3 = 3`, cioè `-2+4+1`.

Per rispondere a molte query di somma, costruisci il vettore dei prefissi una volta (`O(n)` tempo e memoria); ogni query successiva costa `O(1)`. Per contare invece tutti i segmenti con somma `k`, non serve conservare l'intero vettore: basta ricordare quante volte è apparso ciascun prefisso.

Con `[1,2,1]` e `k=3`, la mappa parte da `{0:1}` perché lo zero rappresenta il prefisso prima dell'array. Quando la somma corrente è `s`, un segmento precedente vale `s-k` se il tratto tra quel prefisso e la posizione corrente somma `k`.

| Valore letto | `s` | `s-k` cercato | Conteggi precedenti | Segmenti aggiunti | Totale |
| ---: | ---: | ---: | --- | ---: | ---: |
| 1 | 1 | -2 | `{0:1}` | 0 | 0 |
| 2 | 3 | 0 | `{0:1, 1:1}` | 1 | 1 |
| 1 | 4 | 1 | `{0:1, 1:1, 3:1}` | 1 | 2 |

Dopo aver contato i prefissi che completano `s`, incrementa il conteggio di `s`: così la mappa descrive solo posizioni già passate. La differenza tra prefissi resta valida con numeri negativi; per questo il metodo gestisce casi nei quali restringere una sliding window non è sicuro.

**Versione Python**

```python
def count_subarrays_sum(nums, target):
    frequency = {0: 1}
    prefix = 0
    count = 0

    for value in nums:
        prefix += value
        count += frequency.get(prefix - target, 0)
        frequency[prefix] = frequency.get(prefix, 0) + 1

    return count
```

**Versione C++**

```cpp
#include <unordered_map>
#include <vector>
using namespace std;

long long count_subarrays_sum(const vector<int>& nums, long long target) {
    unordered_map<long long, long long> frequency;
    frequency[0] = 1;
    long long prefix = 0;
    long long count = 0;

    for (int value : nums) {
        prefix += value;
        const auto found = frequency.find(prefix - target);
        if (found != frequency.end()) {
            count += found->second;
        }
        ++frequency[prefix];
    }

    return count;
}
```

Ogni passaggio esegue una lookup e un aggiornamento mediamente `O(1)`, quindi il tempo medio è `O(n)` e la mappa può contenere `O(n)` prefissi. Usa un tipo abbastanza largo per somme e risultato: il numero di segmenti può arrivare a `n(n+1)/2`.

### Dalla somma all'indice

Per `Product Except Self` non si divide: nel primo passaggio il risultato all'indice i riceve il prodotto a sinistra; nel secondo si moltiplica per il prodotto a destra. Con `[2,3,4]`, i prefissi esclusivi sono `[1,2,6]`, poi si combinano coi suffissi `[12,4,1]` ottenendo `[12,8,6]`. Anche gli zeri funzionano senza un ramo dedicato.

Per un pivot in `[1,7,3,6,5,6]`, al valore 6 i prefissi sinistro e destro sommano entrambi 11. Mantenendo `left_sum` e il totale, il lato destro si calcola come `total-left_sum-current`; così si visita ogni elemento una volta senza costruire due array di prefissi. Il vettore risultato non si conta come spazio ausiliario quando il contratto richiede proprio quell'output.

**Da ricordare.** I prefissi trasformano un intervallo in una differenza; la mappa conta i prefissi precedenti che completano il valore richiesto. **Per praticare:** Contare segmenti contigui con somma k; Indice con somme uguali a sinistra e destra; Prodotto di tutti gli elementi tranne quello corrente.