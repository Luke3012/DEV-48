# DP essenziale: House Robber, Coin Change e Word Break

House Robber decide se prendere la casa `i`: se la prende, la precedente non può essere scelta; altrimenti conserva il massimo già raggiunto. Due variabili possono bastare perché la transizione legge soltanto gli ultimi stati.

Prima rendiamo visibile tutta la tabella. Per `best[i]` intendiamo il bottino massimo nelle prime `i` case: `best[0]=0`; per la casa corrente confrontiamo saltarla (`best[i-1]`) con prenderla (`valore[i-1]+best[i-2]`). Con `[2,7,9,3,1]` la tabella diventa `[0,2,7,11,11,12]`. Per esempio, davanti al 9 scegliamo fra 7 e 2+9=11; davanti al 3 scegliamo fra 11 e 7+3=10, quindi lo saltiamo.

**Versione Python**

```python
def max_non_adjacent(values):
    best = [0] * (len(values) + 1)
    for i, value in enumerate(values, start=1):
        take = value + (best[i - 2] if i >= 2 else 0)
        skip = best[i - 1]
        best[i] = max(take, skip)
    return best[-1]
```

**Versione C++**

```cpp
#include <algorithm>
#include <vector>
using namespace std;

long long max_non_adjacent(const vector<int>& values) {
    vector<long long> best(values.size() + 1, 0);
    for (size_t i = 1; i <= values.size(); ++i) {
        long long take = values[i - 1] + (i >= 2 ? best[i - 2] : 0);
        long long skip = best[i - 1];
        best[i] = max(take, skip);
    }
    return best.back();
}
```

La tabella rende semplice verificare la transizione, ma usa `O(n)` memoria. Poiché ogni riga legge solo le due precedenti, dopo aver capito lo schema si possono conservare due variabili e ridurre lo spazio a `O(1)`.

Coin Change chiede il minimo numero di monete. Per ogni importo `x`, provi una moneta `c` e riusi la risposta per `x-c`. Lo stato zero vale zero; con `[1,3,4]`, la tabella fino a 6 è `[0,1,2,1,1,2,2]`. Per arrivare a 6, usare una moneta da 3 lascia l'importo 3, già componibile con una moneta: `1+dp[3]=2`. Le altre scelte richiedono tre monete. Se un importo non è raggiungibile, il suo valore deve restare distinto da `dp[0]=0`.

Word Break considera se il prefisso fino a `i` può essere segmentato. Una posizione è raggiungibile se esiste un taglio precedente raggiungibile e la parte fra i due tagli è nel dizionario. Il set velocizza il lookup, ma il numero dei tagli provati determina il costo.

Scegli il problema DP in base al verbo del prompt: minimo, massimo, numero di modi o esistenza. Stati simili possono avere output diversi e casi base diversi.

### Tracciare i prefissi

In Word Break, `reachable[i]` dice se i primi `i` caratteri sono segmentabili; `reachable[0]=True` rappresenta la stringa vuota. Per `catsand` con parole `cat`, `cats` e `and`:

| `i` | Prefisso | Raggiungibile? | Motivo |
| ---: | --- | --- | --- |
| 0 | `''` | sì | caso base |
| 3 | `cat` | sì | `reachable[0]` e `cat` nel dizionario |
| 4 | `cats` | sì | `reachable[0]` e `cats` nel dizionario |
| 7 | `catsand` | sì | `reachable[4]` e `and` nel dizionario |

Il taglio dopo `cat` non basta: da lì a 7 si ottiene `sand`, che non è una parola ammessa. Si conservano tutti i prefissi raggiungibili finché non si trova una segmentazione completa; fermarsi al primo prefisso valido perderebbe la soluzione che inizia con `cats`.

### Tabelle piccole, stati espliciti

In Unique Paths su una griglia 2×3 senza ostacoli, ogni cella interna riceve i modi da sopra e da sinistra:

| riga / colonna | 0 | 1 | 2 |
| --- | ---: | ---: | ---: |
| 0 | 1 | 1 | 1 |
| 1 | 1 | 2 | 3 |

Quindi ci sono 3 percorsi. Si può conservare una sola riga: il valore corrente della riga precedente e quello appena scritto a sinistra sono i due prerequisiti.

Edit Distance usa prefissi: `dp[i][j]` è il minimo costo per trasformare i primi i caratteri di una stringa nei primi j dell'altra. Con `cat` → `cut`, il costo finale è una sostituzione (`a` → `u`):

| prefisso | vuoto | c | cu | cut |
| --- | ---: | ---: | ---: | ---: |
| vuoto | 0 | 1 | 2 | 3 |
| c | 1 | 0 | 1 | 2 |
| ca | 2 | 1 | 1 | 2 |
| cat | 3 | 2 | 2 | 1 |

Se l'ultimo carattere coincide, copia `dp[i-1][j-1]`; altrimenti prendi 1 più il minimo fra eliminazione, inserimento e sostituzione. La riga iniziale e la colonna iniziale sono i costi per trasformare una stringa vuota. Il tempo è O(mn); conservando solo due righe lo spazio scende a O(min(m,n)).

Nel trading con cooldown tieni tre stati distinti: `hold` (azione in possesso), `sold` (vendita oggi), `rest` (oggi libero senza vendere). Sui prezzi `[1,2,3,0,2]`, i massimi dopo ogni giorno sono:

| Giorno | Prezzo | `hold` | `sold` | `rest` |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | -1 | impossibile | 0 |
| 1 | 2 | -1 | 1 | 0 |
| 2 | 3 | -1 | 2 | 1 |
| 3 | 0 | 1 | -1 | 2 |
| 4 | 2 | 1 | 3 | 2 |

Il profitto migliore finale è 3. Il giorno successivo `hold` può partire solo dal `rest` del giorno precedente, che forza un giorno d'attesa dopo una vendita. Calcola il nuovo terzetto usando solo i valori del giorno prima: aggiornare `rest` prima di `hold` può far riusare accidentalmente una vendita appena avvenuta. Per tutte queste DP, il tempo deriva da numero di stati × lavoro di transizione; la memoria dipende da quanti stati precedenti servono davvero.

**Da ricordare.** Uno stato descrive una sottodomanda precisa: cambiare il significato cambia base, transizione, risposta e casi impossibili. **Per praticare:** Massimo bottino senza case adiacenti; Numero minimo di monete; Percorsi in una griglia senza ostacoli; Segmentare una stringa usando un dizionario; Distanza minima tra due stringhe; Trading con un giorno di cooldown.