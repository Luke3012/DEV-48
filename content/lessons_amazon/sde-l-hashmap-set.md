# HashMap e Set: memoria utile, non magia

Prima di scegliere una mappa o un set, chiediti quale informazione vuoi conservare mentre leggi i dati. Considera tre movimenti di magazzino: `("nord", 3)`, `("sud", 2)`, `("nord", 4)`. Vogliamo sommare gli importi per zona. La chiave è il nome della zona e il valore associato è il totale accumulato.

### Esempio svolto: aggiornare una mappa

Partiamo da una mappa vuota e aggiorniamola una riga alla volta:

| Movimento | Chiave letta | Totale prima | Totale dopo |
| --- | --- | ---: | ---: |
| `("nord", 3)` | `nord` | 0 | 3 |
| `("sud", 2)` | `sud` | 0 | 2 |
| `("nord", 4)` | `nord` | 3 | 7 |

Alla fine la mappa contiene `{"nord": 7, "sud": 2}`. Il terzo movimento non crea una nuova zona: aggiorna il totale già presente. Questo è il passaggio chiave: una mappa collega ogni chiave a un valore utile sul passato.

**Versione Python**

```python
def totals_by_region(movements):
    totals = {}
    for region, amount in movements:
        totals[region] = totals.get(region, 0) + amount
    return totals

movements = [("nord", 3), ("sud", 2), ("nord", 4)]
print(totals_by_region(movements))  # {'nord': 7, 'sud': 2}
```

`get(region, 0)` legge il totale precedente; se la chiave non esiste ancora, parte da zero. Poi il codice aggiunge l'importo corrente e salva il nuovo totale.

**Versione C++**

```cpp
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

unordered_map<string, int> totals_by_region(
    const vector<pair<string, int>>& movements
) {
    unordered_map<string, int> totals;
    for (const auto& movement : movements) {
        totals[movement.first] += movement.second;
    }
    return totals;
}
```

In C++, `totals[region]` crea la chiave con valore iniziale zero quando non esiste; l'operatore `+=` aggiunge l'importo. L'ordine con cui una `unordered_map` mostra le chiavi non è garantito: il contenuto è lo stesso, ma la stampa può cambiare ordine.

Usa un `set` quando ti basta sapere se una chiave è già presente; usa una mappa quando a ogni chiave vuoi associare un conteggio, una posizione o un totale. Con una hash table le operazioni costano in media `O(1)`, quindi questa scansione richiede tempo medio `O(n)`. Lo spazio cresce con il numero di zone distinte, non con il numero totale degli importi. La struttura accelera l'accesso conservando informazioni: quel risparmio di tempo richiede memoria.

### Come decidere che cosa conservare

Rileggi la domanda che la struttura deve rendere veloce: «questa chiave esiste?», «quante volte è comparsa?», «qual era l'indice?». Un `set` conserva le chiavi e basta; una mappa conserva una coppia chiave-valore. Nell'esempio dei movimenti, la chiave era una zona e il valore era il totale. Per frequenze il valore diventa un conteggio; per un indice, diventa la posizione.

Un controllo manuale utile è seguire la stessa chiave due volte. Alla prima occorrenza deve partire dal valore iniziale del problema (spesso zero); alla seconda deve leggere lo stato precedente e aggiornarlo. Se l'aggiornamento dimentica il passato o lo salva con una chiave diversa, la tabella dei passaggi lo rende visibile prima di eseguire il programma.

Gli esercizi successivi useranno mappe per domande differenti. Prima di scegliere il pattern, scrivi in una frase che cosa rappresenta il valore associato a ciascuna chiave: così eviti di trattare tutte le mappe come se fossero semplici contenitori di numeri.

**Da ricordare.** Prima di creare una mappa, formula la domanda che ogni chiave deve rendere veloce e annota cosa viene memorizzato. **Per praticare:** Due valori che completano il target; Confrontare due frequenze di caratteri; Raggruppare le permutazioni di parole.