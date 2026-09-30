# Sliding Window: aggiornare una finestra senza rifarla

Una finestra è un intervallo contiguo che si sposta sull'input. Considera tutte le somme di tre elementi consecutivi in `[2, 1, 5, 1, 3, 2]`. Ricalcolarle da zero produce `8, 7, 9, 6`: il lavoro è corretto, ma tra due somme vicine si ripetono due addendi. Quando la finestra avanza, un elemento esce e uno entra; puoi aggiornare la somma precedente invece di ricominciare.

| Indici inclusi | Operazione dalla finestra precedente | Somma |
| --- | --- | ---: |
| `[0,2]` | somma iniziale `2+1+5` | 8 |
| `[1,3]` | togli `2`, aggiungi `1` | 7 |
| `[2,4]` | togli `1`, aggiungi `3` | 9 |
| `[3,5]` | togli `5`, aggiungi `2` | 6 |

Per una finestra fissa di ampiezza `k`, l'invariante è semplice: `current` è la somma esatta degli ultimi `k` valori entrati. L'inizializzazione richiede `k` addizioni; ogni spostamento ne richiede due, una sottrazione e una addizione. La versione ingenua costa `O((n-k+1)·k)`; dopo l'inizializzazione la scansione costa `O(n)` complessivo.

**Versione Python**

```python
def max_sum_k(nums, k):
    if k <= 0 or k > len(nums):
        raise ValueError("k deve descrivere una finestra non vuota valida")

    current = 0
    for i in range(k):
        current += nums[i]
    best = current

    for right in range(k, len(nums)):
        outgoing = nums[right - k]
        incoming = nums[right]
        current = current - outgoing + incoming
        best = max(best, current)

    return best
```

**Versione C++**

```cpp
#include <algorithm>
#include <stdexcept>
#include <vector>
using namespace std;

long long max_sum_k(const vector<int>& nums, int k) {
    if (k <= 0 || k > static_cast<int>(nums.size())) {
        throw invalid_argument("k deve descrivere una finestra non vuota valida");
    }

    long long current = 0;
    for (int i = 0; i < k; ++i) {
        current += nums[i];
    }
    long long best = current;

    for (int right = k; right < static_cast<int>(nums.size()); ++right) {
        const int outgoing = nums[right - k];
        const int incoming = nums[right];
        current = current - outgoing + incoming;
        best = max(best, current);
    }

    return best;
}
```

I due programmi mantengono lo stesso stato. Con `k=3`, il primo ciclo porta `current` a 8; quando `right=3`, `nums[right-k]` è il 2 che lascia la finestra e `nums[right]` è il nuovo 1. `best` parte dalla prima finestra: inizializzarlo a zero sarebbe sbagliato se tutti gli elementi fossero negativi. Ogni valore viene letto un numero costante di volte; il tempo è `O(n)` e lo spazio ausiliario è `O(1)`.

Una finestra variabile risponde a una domanda diversa: non conosci l'ampiezza in anticipo. Il tentativo diretto sceglie ogni inizio e prova tutti i segmenti che seguono, accumulando la somma: può esaminare `O(n²)` intervalli. Se i valori sono positivi, una somma insufficiente può essere aumentata estendendo a destra; quando è sufficiente, restringere da sinistra può trovare un segmento più corto.

Per target 7 in `[2,3,1,2,4,3]`, la traccia registra ogni restringimento:

| `right` | Valore entrato | Finestra valida candidata | Somma | Migliore |
| ---: | ---: | --- | ---: | ---: |
| 0 | 2 | — | 2 | — |
| 1 | 3 | — | 5 | — |
| 2 | 1 | — | 6 | — |
| 3 | 2 | `[2,3,1,2]` | 8 | 4 |
| 4 | 4 | `[3,1,2,4]`, poi `[1,2,4]` | 10, poi 7 | 3 |
| 5 | 3 | `[2,4,3]`, poi `[4,3]` | 9, poi 7 | 2 |

Quando sottrarre il valore a sinistra fa scendere la somma sotto 7, il `while` termina e il ciclo esterno può aggiungere il prossimo elemento. Per vedere la stessa espansione e contrazione con uno stato diverso, cerchiamo la sottostringa più lunga con al massimo due caratteri distinti in `eceba`:

| Indice | Carattere entrato | Finestra dopo la correzione | Distinti | Migliore |
| ---: | --- | --- | ---: | ---: |
| 0 | `e` | `e` | 1 | 1 |
| 1 | `c` | `ec` | 2 | 2 |
| 2 | `e` | `ece` | 2 | 3 |
| 3 | `b` | `eceb → eb` | 2 | 3 |
| 4 | `a` | `eba → ba` | 2 | 3 |

La condizione da ripristinare è `len(counts) <= k`. Una volta violata, togli caratteri da sinistra finché una frequenza arriva a zero e il numero di chiavi diminuisce. La finestra valida più lunga ha lunghezza 3 (`ece`).

**Versione Python**

```python
def longest_at_most_k_distinct(text, k):
    if k < 0:
        raise ValueError("k deve essere non negativo")
    counts = {}
    left = 0
    best = 0

    for right, char in enumerate(text):
        counts[char] = counts.get(char, 0) + 1
        while len(counts) > k:
            outgoing = text[left]
            counts[outgoing] -= 1
            if counts[outgoing] == 0:
                del counts[outgoing]
            left += 1
        best = max(best, right - left + 1)

    return best
```

**Versione C++**

```cpp
#include <algorithm>
#include <stdexcept>
#include <string>
#include <unordered_map>
using namespace std;

int longest_at_most_k_distinct(const string& text, int k) {
    if (k < 0) {
        throw invalid_argument("k deve essere non negativo");
    }
    unordered_map<char, int> counts;
    int left = 0;
    int best = 0;

    for (int right = 0; right < static_cast<int>(text.size()); ++right) {
        ++counts[text[right]];
        while (static_cast<int>(counts.size()) > k) {
            char outgoing = text[left];
            if (--counts[outgoing] == 0) {
                counts.erase(outgoing);
            }
            ++left;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
```

Gli indici non tornano mai indietro: ciascun carattere entra una volta ed esce al massimo una volta, quindi il tempo atteso è `O(n)` e la mappa usa `O(min(n, alfabeto))` spazio. Il codice illustra il meccanismo delle frequenze; il problema di somma positiva richiede una diversa condizione, anche se i bordi si muovono con lo stesso schema.

La positività non è una nota marginale. Su `[1,-1,5]` con target 5, l'algoritmo può arrivare a somma 5 con tutti e tre gli elementi, registrare lunghezza 3 e fermarsi quando toglie il primo `1`; così non considera il segmento `[5]`, che è la risposta di lunghezza 1. Se i valori possono essere negativi, la monotonia è assente: per contare somme arbitrarie è più adatta la tecnica dei prefissi e della hash map.

Le stringhe usano lo stesso movimento dei bordi, ma lo stato da aggiornare è una mappa di frequenze. Per `abba`, una finestra senza ripetizioni cresce fino a `ab`; al secondo `b`, `left` oltrepassa la prima `b`; poi `ba` torna ad avere lunghezza 2. Per una finestra minima che deve contenere `AA`, una sola `A` non basta: il conteggio delle occorrenze, non la sola presenza, determina la validità. Per `AABABBA` con una sostituzione, la condizione è `lunghezza - massima_frequenza <= 1`. Le finestre fisse, quelle con somma monotona e quelle con requisiti di frequenza condividono i bordi, ma non lo stesso invariante.

### Aggiornare frequenze e molteplicità

Per la sottostringa senza ripetizioni in `abba`, una mappa ricorda l'ultimo indice di ogni carattere. Dopo aver letto `a` e `b`, la finestra valida è `ab` e la lunghezza migliore è 2. Al secondo `b`, la sua ultima posizione era 1: porta `left` a 2. La `a` finale era stata vista prima dell'intervallo corrente, quindi `left` resta 2 e `ba` mantiene il massimo 2.

| Indice | Carattere | Ultima posizione nota | `left` dopo l'aggiornamento | Finestra valida | Migliore |
| ---: | --- | ---: | ---: | --- | ---: |
| 0 | `a` | nessuna | 0 | `a` | 1 |
| 1 | `b` | nessuna | 0 | `ab` | 2 |
| 2 | `b` | 1 | 2 | `b` | 2 |
| 3 | `a` | 0 | 2 | `ba` | 2 |

Per `s="ABAAC"` e `t="AA"`, la finestra deve contenere due occorrenze di `A`, non semplicemente la lettera `A`. Un contatore `missing` parte da 2: entrando nella finestra una `A` lo porta a 1, la seconda a 0; solo allora la finestra è valida e si può provare ad accorciarla. Quando una `A` richiesta esce, `missing` torna a 1. Le frequenze rendono verificabile la molteplicità.

Partendo da `left=0`, quando la finestra `ABA` ha già due A, è valida e lunga 3. Togliere la prima A la rende incompleta. Più avanti la finestra `BAA` torna valida; si può togliere la B senza perdere una A, ottenendo `AA` di lunghezza 2. Togliere una delle due A la rende di nuovo invalida, perciò la scansione ha trovato il minimo.

Per `AABABBA` con `k=1`, `AABA` è una finestra valida: lunghezza 4, tre A, una sostituzione. `AABAB` ha lunghezza 5 ma solo tre A, quindi servirebbero due sostituzioni. La condizione è `lunghezza - frequenza_massima <= k`. Il calcolo della frequenza massima e il momento in cui si restringe fanno parte dell'invariante: non riusare alla cieca il criterio della somma positiva.

**Da ricordare.** La finestra risparmia lavoro perché ogni elemento entra ed esce un numero limitato di volte; la monotonia della condizione va dimostrata. **Per praticare:** Segmento minimo con somma almeno target; Sottostringa più lunga senza ripetizioni; Finestra minima con tutte le frequenze richieste.