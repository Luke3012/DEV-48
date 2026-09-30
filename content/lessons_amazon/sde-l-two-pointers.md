# Two Pointers: far incontrare due scansioni

Per capire perché l'ordine permette di eliminare candidati, cerchiamo due valori in un array crescente la cui differenza sia 5. Il metodo diretto prova ogni coppia, per `O(n²)` confronti. Con due indici che avanzano, possiamo scartare una famiglia di coppie a ogni passo.

Su `[1,2,4,7,9]`, partiamo con `left=0` e `right=1`. Se la differenza è minore di 5, il valore a destra è ancora troppo vicino: tenere lo stesso `left` e provare valori maggiori è l'unica possibilità. Se è maggiore di 5, il valore a sinistra è troppo piccolo: qualunque elemento ancora più a sinistra produrrebbe una differenza almeno altrettanto grande, quindi avanziamo `left`.

| `left` | `right` | Differenza | Decisione giustificata |
| ---: | ---: | ---: | --- |
| 0 (`1`) | 1 (`2`) | 1 | troppo piccola → `right += 1` |
| 0 (`1`) | 2 (`4`) | 3 | troppo piccola → `right += 1` |
| 0 (`1`) | 3 (`7`) | 6 | troppo grande → `left += 1` |
| 1 (`2`) | 3 (`7`) | 5 | coppia trovata agli indici `(1,3)` |

**Versione Python**

```python
def pair_with_difference(nums, target):
    if target < 0:
        raise ValueError("target deve essere non negativo")
    left = 0
    right = 1

    while right < len(nums):
        if left == right:
            right += 1
            continue
        difference = nums[right] - nums[left]
        if difference == target:
            return (left, right)
        if difference < target:
            right += 1
        else:
            left += 1

    return None
```

**Versione C++**

```cpp
#include <optional>
#include <stdexcept>
#include <utility>
#include <vector>
using namespace std;

optional<pair<int, int>> pair_with_difference(const vector<int>& nums, long long target) {
    if (target < 0) {
        throw invalid_argument("target deve essere non negativo");
    }
    int left = 0;
    int right = 1;

    while (right < static_cast<int>(nums.size())) {
        if (left == right) {
            ++right;
            continue;
        }
        const long long difference = static_cast<long long>(nums[right]) - nums[left];
        if (difference == target) {
            return pair<int, int>{left, right};
        }
        if (difference < target) {
            ++right;
        } else {
            ++left;
        }
    }

    return nullopt;
}
```

I due indici avanzano al massimo `n` volte ciascuno, quindi il tempo è `O(n)` e lo spazio ausiliario `O(1)`. Il prerequisito è l'ordine crescente: senza di esso, una differenza troppo grande o troppo piccola non giustifica l'eliminazione dei candidati. Se `target=0`, il ciclo può trovare valori uguali in posizioni distinte.

“Due puntatori” descrive anche meccanismi diversi: fast/slow su una lista usa velocità differenti per rilevare un ciclo o raggiungere il centro; read/write mantiene un prefisso già sistemato mentre legge il resto. Non sono varianti automaticamente intercambiabili: prima di spostare un indice, spiega quale invariante rende sicura la mossa.

### Gli altri modi in cui si incontrano due indici

Per verificare se `sub` è sottosequenza di `text`, scorri `text` sempre in avanti e fai avanzare l'indice di `sub` soltanto dopo una corrispondenza. Non servono due puntatori agli estremi: la relazione importante è l'ordine delle corrispondenze. Se i caratteri di `sub` non finiscono, non è una sottosequenza.

Per un palindromo, invece, confronti gli estremi. Se il contratto ignora spazi e punteggiatura, salta quei caratteri prima del confronto e normalizza le lettere. La stringa vuota è palindroma per definizione perché non esiste una coppia che la contraddica.

In `Container With Most Water`, l'area dipende dalla parete più bassa. Spostare la parete più alta restringe il contenitore senza poter superare l'altezza già limitante; ha senso provare a muovere quella più bassa. In `Trapping Rain Water`, i massimi osservati da sinistra e destra determinano un limite affidabile dal lato con il massimo minore. Con le altezze `[2,0,2]`, sopra la barra centrale restano 2 unità.

Per `Three Sum`, ordina una copia, fissa un valore e usa la ricerca agli estremi per il complemento. Dopo aver trovato una tripletta, salta i valori uguali per non produrre lo stesso risultato più volte: l'ordinamento aiuta sia la decisione sia il controllo dei duplicati. Il tempo è `O(n²)` dopo l'ordinamento; se ordini una copia, essa richiede `O(n)` spazio.

**Da ricordare.** Due puntatori funzionano quando una proprietà consente di motivare quale parte dei candidati eliminare a ogni passo. **Per praticare:** Coppia con somma in una lista ordinata; Triplette distinte con somma zero; Acqua trattenuta fra le pareti.