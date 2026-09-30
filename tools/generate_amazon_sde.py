from __future__ import annotations

from pathlib import Path
import json
import hashlib
import re
from format_amazon_solutions import cpp_solution, python_solution


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
LESSONS_DIR = CONTENT / "lessons_amazon"
CATALOG_FILE = CONTENT / "catalog_amazon_sde.json"


MODULES = [
    {"id": "orientamento", "order": "00", "title": "Formato e metodo di lavoro", "description": "Leggi i requisiti della prova e organizza un metodo per risolvere problemi e verificare il codice."},
    {"id": "linguaggi", "order": "01", "title": "C++ e Python", "description": "Prova entrambi i linguaggi e scegli in base a familiarità, velocità e capacità di debugging."},
    {"id": "fondamenti", "order": "02", "title": "Fondamenti di algoritmi e strutture dati", "description": "Lavora con complessità, array, stringhe, mappe e insiemi."},
    {"id": "pattern", "order": "03", "title": "Tecniche fondamentali", "description": "Applica due puntatori, finestre mobili, prefissi, ordinamento e intervalli."},
    {"id": "ricerca", "order": "04", "title": "Ricerca e strutture lineari", "description": "Usa stack, queue, deque e varianti della ricerca binaria."},
    {"id": "strutture", "order": "05", "title": "Liste, alberi e grafi", "description": "Esplora strutture collegate, ricorsione, BFS, DFS e ordinamento topologico."},
    {"id": "avanzato", "order": "06", "title": "Tecniche avanzate", "description": "Affronta heap, greedy, backtracking e i modelli essenziali di programmazione dinamica."},
    {"id": "repository", "order": "07", "title": "Debugging di repository esistenti", "description": "Segui test, tracce d'errore e flusso del codice; correggi problemi in progetti C++ o Node.js."},
    {"id": "comportamento", "order": "08", "title": "Scenari e riflessione sul lavoro", "description": "Ragiona su Leadership Principles, Work Simulation e Work Style senza imitare risposte modello."},
    {"id": "simulazioni", "order": "09", "title": "Simulazioni a tempo", "description": "Prova esercizi di programmazione e debugging; la simulazione completa divide il tempo tra due attività."},
]


def lesson(lesson_id, module, title, day, minutes, difficulty, objectives, summary, body):
    return {
        "id": f"sde-l-{lesson_id}", "module": module, "title": title,
        "minutes": minutes, "difficulty": difficulty, "mandatory": True,
        "objectives": objectives, "summary": summary,
        "body_file": f"lessons_amazon/sde-l-{lesson_id}.md",
        "recommended_day": day, "body": f"# {title}\n\n{body.strip()}\n",
    }


LESSONS = [
    lesson("oa-format", "orientamento", "Struttura e obiettivi dell'assessment", 1, 15, "base",
           ["sezioni indipendenti", "coding question", "code repository", "variazioni per ruolo e paese"],
           "Distinguere le capacità osservate dalle attività usate per esercitarle, senza scambiare una simulazione con il formato universale dell'assessment.", r'''
Un assessment online è una valutazione composta da una o più attività. La forma concreta dipende dal ruolo, dal paese e dalle istruzioni ricevute: la pagina ufficiale Amazon SDE per studenti e neolaureati invita a controllare l'email dell'assessment, che determina la struttura applicabile. Non dedurre durata, strumenti consentiti o ordine delle prove dal nome del ruolo o da un esempio trovato online.

Le attività possono misurare capacità diverse. In una domanda di coding il candidato riceve un contratto circoscritto: dato un input, deve produrre un output rispettando vincoli e casi limite. In un esercizio su repository il codice esiste già; occorre ricostruire il comportamento fra file, test e componenti prima di correggerlo. Work Style e Work Simulation presentano ancora un altro tipo di ragionamento: familiarità con affermazioni sul proprio modo di lavorare e decisioni in scenari, rispettivamente. Sapere che una di queste prove esiste non significa che sia inclusa in ogni assessment.

#### Un esempio per distinguere le attività

| Consegna ricevuta | Prima domanda da porsi | Evidenza di una risposta solida |
| --- | --- | --- |
| «Restituisci gli indici di due valori che sommano a `target`» | Che cosa significa “due” e che cosa restituire se non esistono? | La funzione rispetta il contratto anche con duplicati e input senza soluzione. |
| «Il test di `findOrder` fallisce in un progetto» | Quale test descrive il comportamento atteso e quale file produce il valore? | Una modifica circoscritta fa passare il caso senza rompere gli altri test. |
| «Scegli un'azione durante un disservizio» | Quale danno continua, quali prove mancano e chi può intervenire? | La motivazione distingue fatti, rischi e assunzioni. |

Le prime due consegne possono entrambe richiedere programmazione, ma il lavoro non è intercambiabile: la prima parte da un problema e una funzione da costruire; la seconda da un sistema e da un comportamento da rintracciare. Il terzo caso non ha una singola funzione corretta da implementare; si confrontano le conseguenze delle azioni nel contesto dato.

Le prove di pratica possono imporre timer o limitare assistenti per allenare una condizione specifica. Quel vincolo appartiene alla simulazione. Per un assessment reale si seguono le istruzioni mostrate nella piattaforma e nell'invito, comprese le regole sull'AI Assistant e sulle risorse esterne.

Per dettagli aggiornati, consulta la [pagina ufficiale Amazon sull'OA SDE](https://www.amazon.jobs/content/en/career-programs/university/sde) e poi verifica il tuo invito: le informazioni pubbliche descrivono il processo generale, non sostituiscono le istruzioni della prova assegnata.
'''),
    lesson("problem-solving", "orientamento", "Dai primi due minuti a una soluzione verificabile", 1, 20, "base",
           ["contratto input/output", "esempio manuale", "invariante", "complessità"],
           "Arrivare a una soluzione corretta passando da un requisito a casi che la possono smentire.", r'''
Quando il cronometro parte, la tentazione è digitare subito. Fai invece un esempio piccolo con le mani. Per una lista `[4, 1, 7]` e una ricerca del valore `1`, scrivi quale risultato deve uscire e cosa succede se la lista è vuota. Una domanda fatta ora costa pochi secondi; una supposizione errata può costarti l'intero tentativo.

Poi scegli la versione più semplice che rispetta il contratto e misurane il costo. Se la prima idea confronta ogni coppia, con `n` elementi esegue circa `n²` confronti. Non è un difetto se `n` è piccolo; diventa un problema quando il vincolo arriva a decine di migliaia. Solo a quel punto cerca l'informazione che manca: una mappa, un ordinamento, una finestra mantenuta tra un passo e il successivo.

Mentre implementi, tieni un'invariante in una frase. Durante una scansione può essere: «tutti gli elementi prima dell'indice corrente sono già stati controllati». In un altro pattern potresti dire: «la mappa contiene i dati già attraversati e il valore associato ha questo significato preciso». Dopo ogni cambiamento, verifica un caso che avrebbe fatto fallire la versione precedente. Se il codice non va, riduci l'input e formula una causa precisa; cambiare tre righe insieme cancella le prove.

Un ritmo realistico per 40 minuti è: chiarimento e casi, 4–6 minuti; scelta e implementazione, circa 25; test manuali e rifinitura, il tempo restante. Se una strada è bloccata, conserva la soluzione parziale e prova un'alternativa con costo chiaro.
'''),
    lesson("language-choice", "linguaggi", "Scegliere il linguaggio per i 40 minuti", 1, 20, "base",
           ["mini-prova equivalente", "velocità di scrittura", "debugging", "strutture standard"],
           "Confrontare Python 3 e C++ su una prova breve prima di impegnare tutta la preparazione.", r'''
La scelta tra Python e C++ dipende dalla familiarità operativa, dalla velocità di scrittura e dalla capacità di individuare gli errori. Una prova breve sugli stessi casi offre un confronto più utile della sola impressione o della conoscenza teorica del linguaggio.

L'esercizio propone una lista di interi e una dimensione `k`; la funzione deve restituire la somma massima di `k` elementi consecutivi. Dopo la somma della prima finestra, il totale si aggiorna sottraendo l'elemento in uscita e aggiungendo quello in entrata, senza ricalcolare ogni somma. La prova dura 8 minuti per linguaggio, con gli stessi input e casi e un editor vuoto.

Per ciascun linguaggio si possono confrontare il tempo di scrittura, le consultazioni di sintassi, gli errori introdotti e la rapidità nel verificare lista vuota, un solo elemento e finestre che avanzano. È preferibile la soluzione che lascia più tempo al ragionamento, non quella che appare più elegante sulla carta.

La scelta può restare provvisoria: aggiornala dopo aver confrontato altri esercizi e il tempo necessario a correggere gli errori. Python e C++ consentono entrambi di implementare gli stessi pattern; la familiarità quotidiana con il compilatore e le librerie conta più della brevità teorica della sintassi.
'''),
    lesson("python-toolkit", "linguaggi", "Python 3 essenziale per gli esercizi DSA", 1, 25, "base",
           ["list, tuple, dict e set", "enumerate e range", "Counter e defaultdict", "deque e heapq"],
           "Recuperare soltanto la sintassi Python che fa risparmiare tempo nei problemi DSA.", r'''
Per un problema su array, `list[int]` basta quasi sempre. `enumerate(nums)` ti dà indice e valore senza una variabile contatore da aggiornare; `range(left, right)` esclude `right`, dettaglio che vale la pena controllare quando gli indici sono già stanchi. Lo slicing `s[::-1]` crea una copia invertita: comodo per una verifica, costoso se la stringa è enorme e la copia non serve.

`dict` e `set` risolvono membership e conteggi: `counts[x] = counts.get(x, 0) + 1`. Quando il default è una collezione, `defaultdict(list)` evita il ramo «chiave vista per la prima volta». `Counter` è ottimo per frequenze, ma anche sotto timer occorre saper spiegare cosa costa ogni passaggio.

Una lista va bene come stack con `append` e `pop`. Per BFS usa `collections.deque` e `popleft()`: togliere il primo elemento da una lista sposta il resto. `heapq` espone un min-heap; per ottenere un max-heap con numeri interi, spesso basta inserire `-value`.

`sorted(values)` crea una nuova lista; `values.sort()` modifica quella esistente. Preferisci la prima quando l'input fa parte del contratto e non deve cambiare. Comprehension e lambda sono strumenti, non una gara a scrivere la riga più corta.
'''),
    lesson("cpp-toolkit", "linguaggi", "C++ moderno e STL per gli esercizi DSA", 1, 30, "base",
           ["vector e string", "hash e contenitori ordinati", "iteratori e confini", "reference e const"],
           "Riprendere la parte di C++ che compare negli esercizi DSA.", r'''
Un `vector<int>` è la scelta normale per una sequenza modificabile; `string` è una sequenza di caratteri con indici da zero. Per lookup medio costante scegli `unordered_map` o `unordered_set`; `map` e `set` mantengono l'ordine e costano `O(log n)`. `pair<int,int>` è utile per portare insieme due coordinate senza creare una classe.

`stack`, `queue` e `deque` esprimono LIFO, FIFO e accesso a entrambe le estremità. `priority_queue<int>` è un max-heap; per il min-heap usa `greater<int>`. `sort`, `lower_bound` e `upper_bound` stanno in `<algorithm>`. Una lambda per ordinare intervalli è spesso sufficiente: `[](const auto& a, const auto& b) { return a[0] < b[0]; }`.

Una reference `const vector<int>&` evita una copia e impedisce alla funzione di modificare l'input. Il range-based `for (const auto& x : values)` è più sicuro che incrementare un indice quando non ti serve l'indice. `size()` restituisce un tipo unsigned: confrontarlo con `int` può produrre sorprese, soprattutto sottraendo uno da una sequenza vuota.

Per alberi e liste, un `struct TreeNode` con puntatori `left/right` e `nullptr` basta. Usa ricorsione quando il problema segue naturalmente i figli; conserva uno stato locale chiaro e valuta la profondità massima. Non serve ripassare template avanzati per risolvere un OA.
'''),
    lesson("complexity", "fondamenti", "Big-O e vincoli: capire quando una risposta è troppo lenta", 1, 25, "base",
           ["O(1), O(log n), O(n)", "O(n log n) e O(n²)", "spazio ausiliario", "dimensione dei vincoli"],
           "Stimare il lavoro prima di affidarsi a una soluzione che supera i casi di esempio.", r'''
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
'''),
    lesson("arrays-strings", "fondamenti", "Array e stringhe: scansione, indici e mutazioni", 1, 20, "base",
           ["traversal", "indici inclusivi ed esclusivi", "in-place", "copie e memoria extra"],
           "Ridurre off-by-one e mutazioni accidentali durante una scansione lineare.", r'''
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
'''),
    lesson("hashmap-set", "fondamenti", "HashMap e Set: memoria utile, non magia", 1, 30, "base",
           ["lookup e complementi", "frequenze", "duplicati e raggruppamento", "chiavi e spazio"],
           "Usare una struttura per ricordare ciò che serve senza ripassare tutto l'input.", r'''
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
'''),
    lesson("two-pointers", "pattern", "Two Pointers: far incontrare due scansioni", 2, 25, "base",
           ["estremi opposti", "fast/slow", "array ordinati", "invariante del movimento"],
           "Eliminare candidati in coppia quando l'ordine consente di motivare ogni spostamento.", r'''
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
'''),
    lesson("sliding-window", "pattern", "Sliding Window: aggiornare una finestra senza rifarla", 2, 30, "intermedio",
           ["finestra fissa", "finestra variabile", "frequenze", "condizione monotona"],
           "Riutilizzare il lavoro tra finestre contigue e riconoscere quando il pattern non vale.", r'''
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
'''),
    lesson("prefix-sum", "pattern", "Prefissi e HashMap: somme di intervalli e prodotti senza divisione", 2, 25, "intermedio",
           ["somme cumulative", "intervalli", "subarray sum", "prefix map"],
           "Rispondere a domande su segmenti usando la differenza tra due prefissi.", r'''
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
'''),
    lesson("sorting-intervals", "pattern", "Sorting e intervalli: ordinare per scoprire sovrapposizioni", 2, 25, "intermedio",
           ["comparatore", "merge intervals", "confini aperti e chiusi", "scheduling"],
           "Usare l'ordinamento per rendere locale un problema che altrimenti richiede confronti incrociati.", r'''
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
'''),
    lesson("mixed-patterns", "pattern", "Problemi misti: scegliere il pattern partendo dal vincolo", 2, 25, "intermedio",
           ["brute force", "segnali dei constraints", "test discriminanti", "scelta motivata"],
           "Confrontare più famiglie di soluzione senza associare parole chiave a ricette automatiche.", r'''
Tre problemi possono dire «trova una coppia» e richiedere approcci diversi. Se l'array è ordinato, due puntatori possono bastare; se devi restituire indici in input non ordinato, una mappa può aiutare; se vuoi tutte le triple uniche, l'ordinamento e la gestione dei duplicati sono parte della soluzione.

Per ogni nuovo enunciato scrivi una versione semplice, poi cerca il collo di bottiglia. Se l'input è 80 elementi, un doppio ciclo può essere una scelta ragionevole. Se sale a 80.000, devi spiegare come scendi a un passaggio lineare o `n log n`.

Un test utile distingue due approcci concorrenti. Per una soluzione hash, usa un complemento che non esiste nell'input lungo: un algoritmo quadratico non si ferma al primo elemento. Per una finestra, usa un caso che obbliga il bordo sinistro a muoversi più di una volta.
'''),
    lesson("stack-queue", "ricerca", "Stack, Queue e Deque: scegliere l'ordine delle visite", 3, 25, "base",
           ["LIFO e FIFO", "parentesi", "BFS", "deque"],
           "Rappresentare il prossimo elemento da elaborare con la struttura corretta.", r'''
Un editor incontra `(`, poi `[`, poi `]`, poi `)`. Per decidere se ogni chiusura corrisponde, basta ricordare le aperture non ancora chiuse. La più recente va controllata per prima: è la regola LIFO di uno stack. Un semplice conteggio non basta, perché `([)]` ha lo stesso numero di parentesi aperte e chiuse ma un ordine impossibile.

Scegliamo di salvare nello stack il carattere di chiusura atteso: leggendo `(` inseriamo `)`, leggendo `[` inseriamo `]`. Quando compare una chiusura, deve coincidere con la cima; dopo il controllo la rimuoviamo.

| Carattere letto | Stack dopo il passo (fondo → cima) | Conseguenza |
| --- | --- | --- |
| `(` | `)` | la prossima chiusura deve essere `)` |
| `[` | `)`, `]` (cima) | la prossima deve essere `]` |
| `]` | `)` | corrisponde alla cima; rimuovi `]` |
| `)` | `[]` | corrisponde alla cima; la stringa è valida |

**Versione Python**

```python
def valid_parentheses(text):
    closing_for = {"(": ")", "[": "]", "{": "}"}
    expected = []

    for char in text:
        if char in closing_for:
            expected.append(closing_for[char])
        elif not expected or expected.pop() != char:
            return False

    return not expected
```

**Versione C++**

```cpp
#include <stack>
#include <string>
using namespace std;

bool valid_parentheses(const string& text) {
    stack<char> expected;

    for (char ch : text) {
        if (ch == '(') {
            expected.push(')');
        } else if (ch == '[') {
            expected.push(']');
        } else if (ch == '{') {
            expected.push('}');
        } else {
            if (expected.empty() || expected.top() != ch) {
                return false;
            }
            expected.pop();
        }
    }

    return expected.empty();
}
```

Entrambe le funzioni assumono che l'input contenga soltanto parentesi; l'else tratta quindi ogni carattere rimanente come una chiusura. Ogni carattere entra o viene rimosso dallo stack al massimo una volta: `O(n)` tempo e fino a `O(n)` spazio, per un input composto solo da aperture annidate. Una queue conserva invece l'ordine FIFO: è adatta alla BFS, che completa la distanza `d` prima di espandere i nodi a distanza `d+1`.
'''),
    lesson("monotonic-stack", "ricerca", "Monotonic Stack: conservare candidati ancora utili", 3, 25, "intermedio",
           ["stack monotono", "prossimo maggiore", "temperatura successiva", "ammortizzato"],
           "Risolvere domande sul prossimo valore maggiore o minore senza riesaminare ogni coppia.", r'''
Per ogni valore vogliamo il primo valore strettamente più grande che compare alla sua destra. Provare tutti i successori per ciascuna posizione confronta fino a `O(n²)` coppie. Invece conserviamo nello stack gli indici a cui non abbiamo ancora assegnato una risposta. I valori corrispondenti restano decrescenti: quando arriva un valore maggiore, risolve gli indici più piccoli che attendono in cima.

Con `[2,1,3]`, i primi due indici restano in attesa; quando arriva 3, esso è il successore maggiore di entrambi. L'ultimo indice non troverà una risposta:

| Indice letto | Valore | Indici in attesa dopo il passo | Risposte determinate |
| ---: | ---: | --- | --- |
| 0 | 2 | `[0:2]` | nessuna |
| 1 | 1 | `[0:2,1:1]` | nessuna |
| 2 | 3 | `[2:3]` | `answer[1]=3`, `answer[0]=3` |
| fine | — | `[2:3]` | `[3,3,-1]` nell'ordine degli indici |

**Versione Python**

```python
def next_greater_values(values):
    answer = [-1] * len(values)
    waiting = []

    for index, value in enumerate(values):
        while waiting and value > values[waiting[-1]]:
            previous = waiting.pop()
            answer[previous] = value
        waiting.append(index)

    return answer
```

**Versione C++**

```cpp
#include <vector>
using namespace std;

vector<int> next_greater_values(const vector<int>& values) {
    vector<int> answer(values.size(), -1);
    vector<int> waiting;

    for (int index = 0; index < static_cast<int>(values.size()); ++index) {
        while (!waiting.empty() && values[index] > values[waiting.back()]) {
            const int previous = waiting.back();
            waiting.pop_back();
            answer[previous] = values[index];
        }
        waiting.push_back(index);
    }

    return answer;
}
```

Il valore `-1` iniziale significa che non esiste un successore maggiore. Ogni indice entra nello stack una volta e ne esce al massimo una; il ciclo interno può fare più operazioni in un passo, ma il totale dei push e pop resta `O(n)`. Lo spazio ausiliario è `O(n)`. Se la consegna chiedesse “maggiore o uguale”, il confronto stretto `>` andrebbe cambiato; con valori uguali, la scelta cambia il risultato.
'''),
    lesson("binary-search", "ricerca", "Binary Search classica: dimezzare uno spazio ordinato", 3, 20, "base",
           ["array ordinato", "mid sicuro", "intervallo residuo", "O(log n)"],
           "Mantenere la garanzia che la risposta, se esiste, resti nell'intervallo di ricerca.", r'''
Una ricerca lineare può dover controllare tutti gli `n` elementi. Se i valori sono ordinati, ogni confronto al centro dell'intervallo può eliminare circa metà dei candidati. La ricerca binaria usa l'intervallo chiuso `[left,right]`: entrambi gli estremi possono ancora contenere la risposta; quando `left > right`, non è rimasto alcun indice.

In `[1,3,5,8,12]`, cerca 8. Inizialmente `left=0`, `right=4`, quindi `mid=2`: il valore 5 è minore del target e tutti gli indici fino a 2 possono essere scartati. L'intervallo residuo è `[3,4]`. Il suo medio è 3, dove si trova 8.

| Passo | `left` | `mid` | `right` | `nums[mid]` | Nuovo intervallo |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0 | 2 | 4 | 5 | `[3,4]` |
| 2 | 3 | 3 | 4 | 8 | trovato all'indice 3 |

**Versione Python**

```python
def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Versione C++**

```cpp
#include <vector>
using namespace std;

int binary_search_index(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;

    while (left <= right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        }
        if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}
```

Il test `left <= right` include l'intervallo con un solo candidato. Aggiornare a `mid+1` o `mid-1` lo elimina dopo averlo confrontato, quindi il ciclo avanza. Per un target assente, ad esempio 9, i confini diventano prima `[4,4]`, poi `[5,4]` e terminano. Se l'array è vuoto, `right=-1` e non si accede a `nums[0]`.

Ogni iterazione circa dimezza i candidati: dopo `k` passi ne restano al più `n/2^k`; servono quindi `O(log n)` confronti e `O(1)` spazio. In C++ il calcolo `left+(right-left)/2` evita l'overflow che può causare `(left+right)/2`. La condizione decisiva è l'ordine: senza una sequenza ordinata o un predicato monotono non puoi scartare una metà in base al valore centrale.
'''),
    lesson("binary-boundaries", "ricerca", "Lower Bound e Upper Bound: trovare un confine, non un elemento", 3, 25, "intermedio",
           ["primo valore non minore", "ultimo valore ammesso", "duplicati", "intervallo semiaperto"],
           "Trasformare la ricerca binaria in una ricerca del primo punto che soddisfa una condizione.", r'''
Con duplicati, cercare una qualsiasi occorrenza non basta sempre. In `[1,2,2,2,5]`, il primo `2` è all'indice 1. Lower Bound trova il primo elemento `>= target`; non cerca di “indovinare” una copia, ma restringe il punto in cui cambia una condizione monotona.

L'intervallo di ricerca è semiaperto `[left,right)`: `right` può valere `n` e non è mai letto come indice. Per target 2, l'evoluzione è:

| `left` | `mid` | `right` | `nums[mid]` | Decisione |
| ---: | ---: | ---: | ---: | --- |
| 0 | 2 | 5 | 2 | il primo `>=2` può essere `mid`: `right=2` |
| 0 | 1 | 2 | 2 | può essere `mid`: `right=1` |
| 0 | 0 | 1 | 1 | è troppo piccolo: `left=1` |

Quando `left==right`, hai il confine. Una risposta pari a `n` è valida come punto di inserimento ma non come indice: prima di leggere `nums[left]`, controlla `left < n`.

**Versione Python**

```python
def lower_bound(nums, target):
    left = 0
    right = len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def upper_bound(nums, target):
    left = 0
    right = len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left


def equal_range(nums, target):
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return (-1, -1)
    after_last = upper_bound(nums, target)
    return (first, after_last - 1)
```

**Versione C++**

```cpp
#include <vector>
using namespace std;

int lower_bound_index(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size());
    while (left < right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return left;
}

int upper_bound_index(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size());
    while (left < right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] <= target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return left;
}
```

Il ciclo cerca un confine, non un valore specifico: a ogni passo mantiene i valori prima di `left` sotto la soglia e quelli da `right` in poi almeno pari alla soglia. Tempo `O(log n)`, spazio `O(1)`. La differenza tra le funzioni sta nel confronto: Lower Bound conserva il medio quando `nums[mid]` è già almeno il target; Upper Bound lo scarta quando è uguale. La libreria C++ offre entrambe in `<algorithm>` e Python in `bisect`; conoscere il significato degli indici resta necessario per controllare i target assenti.
'''),
    lesson("binary-variants", "ricerca", "Ricerca binaria in un array ruotato", 3, 20, "intermedio",
           ["metà ordinata", "intervallo candidato", "array vuoto", "duplicati nel contratto"],
           "Adattare la ricerca quando una sola porzione dell'array è ordinata.", r'''
Una rotazione sposta un prefisso in fondo: `[1,2,3,4,5,6,7,8]` può diventare `[6,7,8,1,2,3,4,5]`. L'intero array non è ordinato, ma il confronto tra `nums[mid]` e `nums[right]` rivela da quale lato si trova il minimo. Prima impariamo a trovare quel confine; per cercare un target, l'esercizio aggiunge poi il controllo di appartenenza alla metà crescente.

Con `[6,7,8,1,2,3,4,5]`, il medio iniziale vale 1 ed è minore di 5: il minimo è nel tratto `[left,mid]`, quindi `right=mid`. Al passo successivo `nums[mid]=7` supera `nums[right]=1`, perciò il minimo deve stare a destra e spostiamo `left` oltre `mid`.

| Passo | `left` | `mid` | `right` | `nums[mid]` / `nums[right]` | Decisione |
| ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0 | 3 | 7 | 1 / 5 | minimo a sinistra o in `mid` → `right=3` |
| 2 | 0 | 1 | 3 | 7 / 1 | minimo a destra → `left=2` |
| 3 | 2 | 2 | 3 | 8 / 1 | minimo a destra → `left=3` |

**Versione Python**

```python
def minimum_rotated(nums):
    if not nums:
        raise ValueError("serve almeno un elemento")
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]
```

**Versione C++**

```cpp
#include <stdexcept>
#include <vector>
using namespace std;

int minimum_rotated(const vector<int>& nums) {
    if (nums.empty()) {
        throw invalid_argument("serve almeno un elemento");
    }
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;

    while (left < right) {
        const int mid = left + (right - left) / 2;
        if (nums[mid] > nums[right]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return nums[left];
}
```

Con valori distinti, il confronto elimina almeno metà dei candidati; il costo è `O(log n)` tempo e `O(1)` spazio. Un array già ordinato restituisce il primo elemento. I duplicati possono rendere uguali gli estremi e nascondere da quale lato è avvenuta la rotazione; il codice non li ammette.
'''),
    lesson("binary-answer", "ricerca", "Binary Search on Answer: trovare la soglia fattibile", 3, 25, "intermedio",
           ["dominio delle risposte", "predicato monotono", "estremi fattibili", "costo della verifica"],
           "Cercare il minimo o massimo valore che rende fattibile una soluzione.", r'''
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
'''),
    lesson("linked-lists", "strutture", "Linked List: cambiare collegamenti senza perdere la lista", 4, 25, "intermedio",
           ["ListNode", "reverse", "merge", "fast/slow", "cycle"],
           "Ragionare su riferimenti e puntatori aggiornando un nodo alla volta.", r'''
Una lista collegata è una catena di nodi; ciascun nodo conserva un valore e un riferimento al successivo. Il nodo iniziale è `head`, la fine è indicata da `None` o `nullptr`. A differenza di un array non puoi saltare direttamente al nodo 20: devi seguire i collegamenti, perciò l'accesso all'indice `k` costa `O(k)`. Se hai già il riferimento al nodo giusto, invece, cambiare un link costa `O(1)`.

Supponi di avere `A → C` e un nodo nuovo `B` da inserire dopo A. Prima fai puntare B al successore di A, poi aggiorni il link di A:

| Passo | `A.next` | `B.next` | Catena raggiungibile da A |
| ---: | --- | --- | --- |
| iniziale | C | `None` | `A → C` |
| collega B al successore | C | C | `A → C` e `B → C` |
| collega A a B | B | C | `A → B → C` |

L'ordine evita di perdere C. Se prima sovrascrivessi `A.next` con B, non sapresti più quale nodo assegnare a `B.next`.

**Versione Python**

```python
class ListNode:
    def __init__(self, value=0, next_node=None):
        self.value = value
        self.next = next_node


def insert_after(previous, node):
    node.next = previous.next
    previous.next = node
```

**Versione C++**

```cpp
struct ListNode {
    int value;
    ListNode* next;
};

void insert_after(ListNode* previous, ListNode* node) {
    node->next = previous->next;
    previous->next = node;
}
```

La funzione presuppone che `previous` e `node` siano validi e che `node` non faccia già parte della catena. Una volta raggiunto `previous`, l'inserimento costa `O(1)` tempo e spazio: la lista non viene ricopiata.

L'inversione generalizza la stessa cautela: per ogni nodo salvi il collegamento originale al successore prima di riscriverlo verso il predecessore. Nella fusione di due liste ordinate colleghi la testa minore e avanzi solo la lista da cui proviene. Per cercare un ciclo, `slow` avanza di uno e `fast` di due; se la catena termina, `fast` o `fast.next` diventa nullo, altrimenti i due possono incontrarsi.
'''),
    lesson("recursion", "strutture", "Ricorsione: caso base, progresso e costo dello stack", 4, 20, "intermedio",
           ["caso base", "sottoproblema più piccolo", "stack di chiamate", "memoization"],
           "Scrivere una chiamata ricorsiva che si avvicina davvero alla terminazione.", r'''
Una funzione ricorsiva delega una parte più piccola del problema a una nuova chiamata. Per iniziare, sommiamo gli interi da 1 a `n`: quando `n=0` la somma restante è zero; quando `n>0`, la risposta è `n` più la somma da 1 a `n-1`. Il numero diminuisce a ogni chiamata, quindi prima o poi raggiunge il caso base.

Con `sum_to(3)`, le chiamate scendono `3 → 2 → 1 → 0`. La chiamata con 0 restituisce 0; poi i frame sospesi rispondono `1+0=1`, `2+1=3`, `3+3=6`. Ogni frame conserva il proprio `n` mentre aspetta il risultato più piccolo.

**Versione Python**

```python
def sum_to(n):
    if n < 0:
        raise ValueError("n deve essere non negativo")
    if n == 0:
        return 0
    return n + sum_to(n - 1)
```

**Versione C++**

```cpp
#include <stdexcept>

long long sum_to(int n) {
    if (n < 0) {
        throw std::invalid_argument("n deve essere non negativo");
    }
    if (n == 0) {
        return 0;
    }
    return n + sum_to(n - 1);
}
```

Il caso `n=0` risponde senza altre chiamate; `n<0` non progredirebbe verso la base, quindi il contratto lo rifiuta. Per un valore non negativo vengono create `n+1` chiamate: tempo e stack sono `O(n)`. La ricorsione non rende il calcolo automaticamente più veloce: per questa somma esiste una formula diretta, ma l'esempio isola la struttura dei casi base e del ritorno.
'''),
    lesson("tree-traversal", "strutture", "Alberi binari: preorder, inorder, postorder e livelli", 4, 25, "intermedio",
           ["TreeNode", "visite DFS", "BFS per livelli", "visita vuota"],
           "Scegliere l'ordine di visita in base a quando serve il nodo rispetto ai figli.", r'''
Preorder elabora il nodo prima dei figli, inorder fra il figlio sinistro e il destro, postorder dopo entrambi. Su un BST, inorder restituisce i valori crescenti perché ogni nodo è maggiore di tutto il sottoalbero sinistro e minore di quello destro.

Per l'albero `1` con figli `2` e `3`, e figli `4` e `5` sotto `2`, le visite differiscono:

| Ordine | Sequenza |
| --- | --- |
| Preorder: nodo, sinistra, destra | `1,2,4,5,3` |
| Inorder: sinistra, nodo, destra | `4,2,5,1,3` |
| Postorder: sinistra, destra, nodo | `4,5,2,3,1` |
| Per livelli, con una queue | `1,2,3,4,5` |

Con una visita postorder puoi anche calcolare una proprietà composta dai figli. Come primo esempio, somma il valore del nodo ai totali dei due sottoalberi. Questa funzione visita entrambi i rami, riceve i loro risultati e combina le risposte soltanto al ritorno.

**Versione Python**

```python
class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def sum_tree(node):
    if node is None:
        return 0
    left_total = sum_tree(node.left)
    right_total = sum_tree(node.right)
    return node.value + left_total + right_total
```

**Versione C++**

```cpp
#include <algorithm>

struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

int sum_tree(const TreeNode* node) {
    if (node == nullptr) {
        return 0;
    }

    const int left_total = sum_tree(node->left);
    const int right_total = sum_tree(node->right);
    return node->value + left_total + right_total;
}
```

Il valore nullo è l'identità della somma: aggiungerlo non cambia il risultato. La funzione visita ogni nodo una volta (`O(n)` tempo) e conserva `O(h)` chiamate; un albero vuoto restituisce zero. Nelle esercitazioni di diametro e massimo cammino, il risultato restituito dai figli non basta da solo: occorre anche aggiornare un massimo globale con una combinazione che il genitore non può usare direttamente.
'''),
    lesson("bst-paths", "strutture", "BST, profondità e antenati: usare la struttura dichiarata", 4, 25, "intermedio",
           ["proprietà BST", "min/max ricorsivi", "LCA", "percorso radice-foglia"],
           "Sfruttare l'ordinamento dell'albero senza dare per vera una proprietà non garantita.", r'''
In un BST, ogni valore nel sottoalbero sinistro è minore della radice e ogni valore a destra è maggiore, se il contratto non ammette duplicati. La proprietà globale permette di cercare un elemento seguendo un solo cammino: ogni confronto elimina un sottoalbero intero.

Nell'albero con radice 10, figlio destro 15 e figlio sinistro di 15 pari a 12, cercare 12 porta prima a destra di 10, poi a sinistra di 15. Se cerchi 6, vai a sinistra verso 5 e poi a destra; arrivare a un figlio nullo dimostra che il valore non è presente.

**Versione Python**

```python
class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def contains_bst(root, target):
    current = root
    while current is not None:
        if current.value == target:
            return True
        if target < current.value:
            current = current.left
        else:
            current = current.right
    return False
```

**Versione C++**

```cpp
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

bool contains_bst(const TreeNode* root, int target) {
    const TreeNode* current = root;
    while (current != nullptr) {
        if (current->value == target) {
            return true;
        }
        if (target < current->value) {
            current = current->left;
        } else {
            current = current->right;
        }
    }
    return false;
}
```

La ricerca costa `O(h)` tempo e `O(1)` spazio, con `h` pari alla lunghezza del cammino percorso. Un BST bilanciato ha altezza logaritmica; un albero inclinato può richiedere `O(n)`. L'ordinamento dei valori non garantisce da solo che l'albero sia bilanciato.
'''),
    lesson("bfs-dfs-grid", "strutture", "BFS e DFS su una griglia: una cella è un nodo", 4, 30, "intermedio",
           ["visited", "quattro direzioni", "componenti", "distanza non pesata"],
           "Trasformare una griglia in un grafo e visitare ogni cella senza ripassarla.", r'''
Una griglia rettangolare è un grafo implicito: ogni cella libera è un nodo e le mosse consentite definiscono i vicini. Con movimenti su/giù/sinistra/destra, una cella al centro ha al massimo quattro vicini; prima di leggerli bisogna controllare che le coordinate siano dentro la matrice.

Per contare mosse minime quando ogni passo costa uno, la BFS esplora per distanza. Con `S . # / . . E`, la distanza di S è 0. La prima frontiera è `(0,1)` e `(1,0)` a distanza 1; poi si raggiunge `(1,1)` a distanza 2 e infine E a distanza 3. Una matrice `distance` usa `-1` per le celle non ancora scoperte; impostarla quando accodi la cella impedisce che due genitori la inseriscano entrambi.

**Versione Python**

```python
from collections import deque


def shortest_grid_path(grid, start, target):
    rows = len(grid)
    if rows == 0 or len(grid[0]) == 0:
        return -1
    cols = len(grid[0])

    start_row, start_col = start
    target_row, target_col = target
    inside_start = 0 <= start_row < rows and 0 <= start_col < cols
    inside_target = 0 <= target_row < rows and 0 <= target_col < cols
    if not inside_start or not inside_target:
        return -1
    if grid[start_row][start_col] == "#" or grid[target_row][target_col] == "#":
        return -1
    distance = [[-1] * cols for _ in range(rows)]
    distance[start_row][start_col] = 0
    queue = deque([start])
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while queue:
        row, col = queue.popleft()
        if (row, col) == target:
            return distance[row][col]

        for dr, dc in directions:
            next_row = row + dr
            next_col = col + dc
            inside = 0 <= next_row < rows and 0 <= next_col < cols
            if inside and grid[next_row][next_col] != "#" and distance[next_row][next_col] == -1:
                distance[next_row][next_col] = distance[row][col] + 1
                queue.append((next_row, next_col))

    return -1
```

**Versione C++**

```cpp
#include <queue>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int shortest_grid_path(const vector<string>& grid, pair<int, int> start, pair<int, int> target) {
    const int rows = static_cast<int>(grid.size());
    if (rows == 0 || grid[0].empty()) {
        return -1;
    }
    const int cols = static_cast<int>(grid[0].size());
    auto inside = [&](int row, int col) {
        return 0 <= row && row < rows && 0 <= col && col < cols;
    };
    if (!inside(start.first, start.second) || !inside(target.first, target.second)) {
        return -1;
    }
    if (grid[start.first][start.second] == '#' || grid[target.first][target.second] == '#') {
        return -1;
    }

    vector<vector<int>> distance(rows, vector<int>(cols, -1));
    queue<pair<int, int>> pending;
    distance[start.first][start.second] = 0;
    pending.push(start);
    const int dr[4] = {1, -1, 0, 0};
    const int dc[4] = {0, 0, 1, -1};

    while (!pending.empty()) {
        const auto [row, col] = pending.front();
        pending.pop();
        if (pair<int, int>{row, col} == target) {
            return distance[row][col];
        }

        for (int direction = 0; direction < 4; ++direction) {
            const int next_row = row + dr[direction];
            const int next_col = col + dc[direction];
            if (inside(next_row, next_col) && grid[next_row][next_col] != '#' && distance[next_row][next_col] == -1) {
                distance[next_row][next_col] = distance[row][col] + 1;
                pending.push({next_row, next_col});
            }
        }
    }

    return -1;
}
```

Le due versioni visitano ogni cella al massimo una volta: `O(R·C)` tempo e `O(R·C)` per distanze e frontiera. Il codice assume una matrice rettangolare e coordinate di partenza e destinazione valide o da rifiutare; non modifica il contenuto ricevuto. La BFS trova il cammino minimo solo con costi uniformi. Per contare isole si può usare una DFS per componente; il primo percorso esplorato non è necessariamente il più corto.
'''),
    lesson("graphs", "strutture", "Grafi: adjacency list, visited e componenti", 4, 25, "intermedio",
           ["lista di adiacenza", "grafo diretto e non diretto", "componenti connesse", "nodi isolati"],
           "Leggere il modello dei collegamenti prima di scegliere la visita.", r'''
Un grafo esplicita relazioni fra nodi. Una lista di adiacenza associa a ogni nodo i vicini; in un grafo non diretto `(0,1)` compare sia tra i vicini di 0 sia tra quelli di 1. Con pochi archi questa rappresentazione usa `O(V+E)` spazio invece della matrice `O(V²)`.

Costruiamo il grafo con archi `(0,1)`, `(1,2)` e `(0,2)`, più il nodo isolato 3. Per trovare il cammino minimo non pesato da 0 a 2, la BFS parte da `queue=[0]`, visita 0 e accoda 1 e 2 a distanza 1. Il nodo 2 è già stato scoperto quando poi si visita 1, quindi non si accoda una seconda volta.

**Versione Python**

```python
from collections import deque


def shortest_distance(node_count, edges, start, target):
    graph = [[] for _ in range(node_count)]
    for first, second in edges:
        graph[first].append(second)
        graph[second].append(first)

    distance = [-1] * node_count
    distance[start] = 0
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node == target:
            return distance[node]
        for neighbor in graph[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)

    return -1
```

**Versione C++**

```cpp
#include <queue>
#include <utility>
#include <vector>
using namespace std;

int shortest_distance(int node_count, const vector<pair<int, int>>& edges, int start, int target) {
    vector<vector<int>> graph(node_count);
    for (const auto& [first, second] : edges) {
        graph[first].push_back(second);
        graph[second].push_back(first);
    }

    vector<int> distance(node_count, -1);
    queue<int> pending;
    distance[start] = 0;
    pending.push(start);

    while (!pending.empty()) {
        const int node = pending.front();
        pending.pop();
        if (node == target) {
            return distance[node];
        }
        for (int neighbor : graph[node]) {
            if (distance[neighbor] == -1) {
                distance[neighbor] = distance[node] + 1;
                pending.push(neighbor);
            }
        }
    }

    return -1;
}
```

`distance != -1` svolge anche il ruolo di `visited`. Si assegna quando il nodo entra in coda: se due genitori lo scoprono, il secondo lo riconosce già visitato. Una BFS visita ogni nodo e ogni arco al massimo un numero costante di volte, quindi `O(V+E)` tempo; la lista del grafo usa `O(V+E)` e distanze e coda `O(V)`.
'''),
    lesson("topological-sort", "strutture", "Topological Sort e cicli: dipendenze prima dei dipendenti", 4, 25, "intermedio",
           ["DAG", "indegree", "Kahn", "ciclo"],
           "Verificare se un insieme di prerequisiti ammette un ordine completo.", r'''
Un ordinamento topologico mette ogni prerequisito prima di ciò che dipende da esso. Gli archi sono diretti e descrivono `prerequisito → attività`; se il grafo contiene un ciclo, non esiste un ordine che possa rispettare tutte le dipendenze.

Kahn conta quanti prerequisiti entrano in ogni nodo (`indegree`). I nodi con grado entrante zero possono iniziare; quando ne rimuovi uno, decrementi il grado dei suoi successori. Se la coda si svuota prima di emettere tutti i nodi, quelli rimasti sono bloccati da un ciclo.

**Versione Python**

```python
from collections import deque


def topological_order(node_count, edges):
    graph = [[] for _ in range(node_count)]
    indegree = [0] * node_count
    for prerequisite, dependent in edges:
        graph[prerequisite].append(dependent)
        indegree[dependent] += 1

    ready = deque(node for node in range(node_count) if indegree[node] == 0)
    order = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for dependent in graph[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)

    return order if len(order) == node_count else None
```

**Versione C++**

```cpp
#include <optional>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

optional<vector<int>> topological_order(int node_count, const vector<pair<int, int>>& edges) {
    vector<vector<int>> graph(node_count);
    vector<int> indegree(node_count, 0);
    for (const auto& [prerequisite, dependent] : edges) {
        graph[prerequisite].push_back(dependent);
        ++indegree[dependent];
    }

    queue<int> ready;
    for (int node = 0; node < node_count; ++node) {
        if (indegree[node] == 0) {
            ready.push(node);
        }
    }

    vector<int> order;
    while (!ready.empty()) {
        const int node = ready.front();
        ready.pop();
        order.push_back(node);
        for (int dependent : graph[node]) {
            --indegree[dependent];
            if (indegree[dependent] == 0) {
                ready.push(dependent);
            }
        }
    }

    if (static_cast<int>(order.size()) != node_count) {
        return nullopt;
    }
    return order;
}
```

Ogni nodo entra ed esce dalla coda una volta e ogni arco decrementa un grado una volta: `O(V+E)` tempo e spazio per il grafo, i gradi e la coda. Più code possibili possono produrre ordinamenti validi diversi; confronta le precedenze se la traccia non impone un ordine specifico.
'''),
    lesson("heap", "avanzato", "Heap e Priority Queue: tenere in vista il prossimo estremo", 5, 25, "intermedio",
           ["min e max heap", "top K", "k-esimo", "streaming"],
           "Mantenere pochi candidati quando non serve ordinare l'intera collezione.", r'''
Un heap conserva una sola garanzia: il minimo (o il massimo) è in cima. Gli altri elementi non sono ordinati fra loro. Per trattenere i `k` valori maggiori, un min-heap di capacità `k` mantiene in cima il più piccolo fra i candidati. Ogni volta che la dimensione supera `k`, espelli quell'elemento: se era troppo piccolo, il nuovo insieme conserva i migliori visti finora.

Con `[7,2,9,4,1]` e `k=2`, l'evoluzione è:

| Valore entrato | Heap dopo la correzione | Minimo espulso |
| ---: | --- | ---: |
| 7 | `[7]` | — |
| 2 | `[2,7]` | — |
| 9 | `[7,9]` | 2 |
| 4 | `[7,9]` | 4 |
| 1 | `[7,9]` | 1 |

Il min-heap non è una lista crescente; la tabella mostra soltanto la sua proprietà rilevante: la cima è il minimo. Qui la cima finale 7 è il secondo valore più grande.

**Versione Python**

```python
import heapq


def retain_largest(values, k):
    if k <= 0:
        raise ValueError("k deve essere positivo")

    heap = []
    for value in values:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

**Versione C++**

```cpp
#include <functional>
#include <queue>
#include <stdexcept>
#include <vector>
using namespace std;

using MinHeap = priority_queue<int, vector<int>, greater<int>>;

MinHeap retain_largest(const vector<int>& values, int k) {
    MinHeap heap;
    if (k <= 0) {
        throw invalid_argument("k deve essere positivo");
    }

    for (int value : values) {
        heap.push(value);
        if (static_cast<int>(heap.size()) > k) {
            heap.pop();
        }
    }
    return heap;
}
```

`n` inserimenti e al più `n` rimozioni costano `O(n log k)`; l'heap conserva `O(k)` valori. Ordinare tutto costa `O(n log n)` e mantiene ogni elemento, ma è più semplice se serve l'ordine completo. C++ usa un max-heap per default, quindi `greater<int>` è necessario per avere il minimo in cima; Python `heapq` è già un min-heap.
'''),
    lesson("greedy", "avanzato", "Greedy e scheduling: dimostrare la scelta locale", 5, 25, "intermedio",
           ["scelta locale", "intervalli", "controesempio", "ordinamento per fine"],
           "Riconoscere un greedy corretto e cercare un caso che lo smentisca.", r'''
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
'''),
    lesson("backtracking", "avanzato", "Backtracking: esplorare scelte e annullarle bene", 5, 25, "intermedio",
           ["decision tree", "subsets e permutazioni", "pruning", "stato ripristinato"],
           "Costruire tutte le risposte valide controllando lo stato che ogni ramo lascia dietro di sé.", r'''
Il backtracking visita un albero di decisioni e mantiene il percorso corrente. Ogni scelta aggiunta vale soltanto per il ramo che la sta esplorando: al ritorno dalla ricorsione la rimuovi, così il ramo seguente parte dallo stato giusto.

Per generare stringhe binarie di lunghezza 2, a ogni posizione scegli `0` oppure `1`. Il percorso produce, in ordine, `00`, `01`, `10`, `11`. Dopo aver salvato `00`, la scelta finale `0` viene tolta prima di provare `1`; dopo aver completato entrambi i rami, si torna alla prima posizione.

**Versione Python**

```python
def binary_strings(length):
    if length < 0:
        raise ValueError("length deve essere non negativa")
    results = []
    current = []

    def build(position):
        if position == length:
            results.append("".join(current))
            return

        for bit in ("0", "1"):
            current.append(bit)
            build(position + 1)
            current.pop()

    build(0)
    return results
```

**Versione C++**

```cpp
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;

void build_binary_strings(int length, int position, string& current, vector<string>& results) {
    if (position == length) {
        results.push_back(current);
        return;
    }

    const char choices[2] = {'0', '1'};
    for (char bit : choices) {
        current.push_back(bit);
        build_binary_strings(length, position + 1, current, results);
        current.pop_back();
    }
}

vector<string> binary_strings(int length) {
    vector<string> results;
    string current;
    if (length < 0) {
        throw invalid_argument("length deve essere non negativa");
    }
    build_binary_strings(length, 0, current, results);
    return results;
}
```

Il percorso `current` viene passato per riferimento in C++ e mutato sul posto; `results.push_back(current)` ne salva una copia alla foglia. Se `length=0`, il caso base salva una stringa vuota. Ci sono `2^n` foglie e ogni risposta contiene `n` caratteri, quindi materializzare l'output richiede `O(n·2^n)` tempo e memoria; lo stato temporaneo e lo stack usano `O(n)`.

Lo stesso albero include/esclude descrive i sottoinsiemi. Per le permutazioni occorre anche impedire di scegliere di nuovo un indice già usato; per Combination Sum il riuso può invece essere consentito. Il costo può essere esponenziale, quindi cerca una regola sicura per potare un ramo prima di esplorare i suoi discendenti.
'''),
    lesson("dp-memoization", "avanzato", "Dynamic Programming: recursion, memoization, tabulation", 5, 30, "intermedio",
           ["stato", "sottoproblemi sovrapposti", "memoization", "ordine tabulato"],
           "Trasformare ricorsione ripetuta in un calcolo che risolve ogni stato una volta.", r'''
Dynamic programming nasce quando una ricorsione risolve più volte lo stesso sottoproblema. La prima domanda non è “quale tabella uso?”, ma “quale stato identifica una domanda la cui risposta può essere riutilizzata?”. Per Fibonacci, lo stato è `n`: la risposta dipende solo da `n-1` e `n-2`, non dal percorso di chiamate che ha portato fin lì.

La ricorsione diretta di `fib(5)` calcola `fib(3)` sia nel ramo di `fib(4)` sia come secondo figlio della radice. Una mappa conserva il risultato alla prima visita:

| Stato richiesto | Dipendenze | Risultato memorizzato |
| ---: | --- | ---: |
| `fib(2)` | `fib(1)+fib(0)` | 1 |
| `fib(3)` | `fib(2)+fib(1)` | 2 |
| `fib(4)` | `fib(3)+fib(2)` | 3 |
| `fib(5)` | `fib(4)+fib(3)` | 5 |

Alla seconda richiesta di `fib(3)`, si legge il valore 2 dalla cache invece di espandere altre chiamate.

Per mantenere equivalenti i risultati numerici degli esempi, consideriamo `0 <= n <= 92`: la risposta entra in un intero a 64 bit.

**Versione Python**

```python
def fibonacci(n):
    if n < 0:
        raise ValueError("n deve essere non negativo")
    memo = {0: 0, 1: 1}

    def solve(state):
        if state not in memo:
            memo[state] = solve(state - 1) + solve(state - 2)
        return memo[state]

    return solve(n)
```

**Versione C++**

```cpp
#include <stdexcept>
#include <vector>
using namespace std;

long long fibonacci(int n) {
    if (n < 0) {
        throw invalid_argument("n deve essere non negativo");
    }
    vector<long long> memo(n + 1, -1);
    memo[0] = 0;
    if (n >= 1) {
        memo[1] = 1;
    }

    auto solve = [&](auto&& self, int state) -> long long {
        if (memo[state] == -1) {
            memo[state] = self(self, state - 1) + self(self, state - 2);
        }
        return memo[state];
    };

    return solve(solve, n);
}
```

Gli stati da 0 a `n` vengono calcolati una sola volta; ciascuno fa lavoro costante, quindi il tempo è `O(n)`, la cache `O(n)` e lo stack ricorsivo può raggiungere `O(n)`. La tabulation usa lo stesso stato ma lo calcola dal basso: dopo aver trovato due valori, può conservarne soltanto gli ultimi due. Quale forma è più chiara dipende da quali stati servono davvero.
'''),
    lesson("dp-models", "avanzato", "DP essenziale: House Robber, Coin Change e Word Break", 5, 30, "intermedio",
           ["massimo con vincolo", "minimo numero di scelte", "segmentazione", "casi impossibili"],
           "Confrontare tre stati DP per vedere come cambia la transizione al cambiare della domanda.", r'''
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
'''),
    lesson("timed-dsa", "simulazioni", "Un problema Medium in 40 minuti", 5, 35, "intermedio",
           ["strategia sotto timer", "test essenziali", "gestire un blocco", "consegna chiara"],
           "Eseguire un ciclo completo di lettura, implementazione e verifica dentro un tempo indipendente.", r'''
Prima leggi prompt e constraints fino in fondo. Scrivi un caso normale, un limite e un caso che mette in difficoltà la soluzione lenta. Ripeti il contratto in una frase: input, output, assunzioni. Se serve ordinare o usare spazio extra, dillo prima di farlo.

Quando l'algoritmo è chiaro, implementa la parte centrale senza perfezionare nomi o formattazione. Compila presto. Poi verifica l'input più piccolo, duplicati, indice ai confini e il test grande. Ogni fix dovrebbe corrispondere a una causa che puoi descrivere.

Se dopo dieci minuti manca ancora una strategia, conviene conservare una soluzione parziale corretta e scrivere la brute force. Un risultato funzionante può valere più di un'ottimizzazione incompleta. Gli ultimi minuti servono a rileggere il codice dall'inizio e a verificare il contratto, senza aggiungere funzionalità non richieste.
'''),
    lesson("repo-orientation", "repository", "Orientarsi in una repository sconosciuta", 1, 20, "base",
           ["struttura", "README", "entry point", "percorso dati"],
           "Trovare il punto di partenza e il flusso coinvolto senza leggere ogni file.", r'''
L'apertura dei file in ordine alfabetico non è una strategia efficace. La struttura iniziale si ricostruisce da manifest, script, README, cartelle principali e test. Dal simbolo o dalla route citata nel requisito si può seguire una chiamata alla volta e disegnare il percorso dei dati, per esempio `route → controller → service → repository`.

Il README descrive come si avvia il progetto, ma il comportamento reale può essere nei test. Prima di cambiare codice, esegui il comando dichiarato e conserva il primo errore completo. Un log lungo contiene spesso una causa utile nelle prime righe o un test con expected e actual molto specifici.

La Code Repository Question verifica la manutenzione di un progetto locale: il file difettoso non è noto in anticipo e lo spazio di ricerca va ridotto con indizi verificabili. Un orientamento iniziale accurato può evitare modifiche premature al file sbagliato.
'''),
    lesson("tests-stack-traces", "repository", "Leggere un failing test e uno stack trace", 6, 25, "intermedio",
           ["expected vs actual", "stack trace", "failure riproducibile", "test minimo"],
           "Usare il test come descrizione eseguibile del contratto e lo stack trace come mappa.", r'''
Un test fallito spesso dice già il punto di attrito: chiamata, input, valore atteso e valore reale. Prima di correggere, controlla se il test è deterministico e se il fallimento riproduce il requisito. Se il test si aspetta una lista con un ordine preciso, capire se l'ordine è parte del contratto evita un falso fix.

Uno stack trace mostra la catena degli stack frame. Parti dal primo frame del progetto, non da una riga interna di Node o del framework. Risali a chi ha costruito l'input e scendi a chi ha prodotto l'output. Il test nomina l'esempio; lo stack trace collega i file.

Fai una sola ipotesi per volta: «il controller restituisce una Promise non attesa». La verifica è concreta: il test vede una Promise invece dell'array. Un fix minimo aggiunge `await`, poi controlli le route vicine e i casi di errore.
'''),
    lesson("cpp-repository", "repository", "Repository C++: header, source, classi e test", 6, 25, "intermedio",
           ["header/source", "CMake", "API di classe", "assertion"],
           "Seguire una funzione C++ tra dichiarazione, implementazione e test.", r'''
Un header dichiara quali nomi e tipi sono disponibili; un file `.cpp` contiene spesso l'implementazione. Se il compilatore dice “undefined reference”, la dichiarazione può esistere ma la definizione non entra nel link. Se segnala un tipo sconosciuto, controlla gli include prima di riscrivere la funzione.

Con CMake si individua il target compilato e i file che lo compongono. La diagnosi parte dall'errore più vicino al codice applicativo e dal numero di riga del progetto. Una modifica a una firma in header deve restare coerente con source e chiamanti.

Un'asserzione `EXPECT_EQ(expected, actual)` confronta valori; per una classe, chiediti se il contratto è osservabile tramite metodo pubblico. Un test che passa non giustifica una modifica ampia all'API. Mantieni lo stato privato e correggi la regola che produce il valore errato.
'''),
    lesson("node-repository", "repository", "Repository Node.js: package, moduli e test", 6, 25, "intermedio",
           ["package.json", "npm test", "import/export", "test unitari"],
           "Capire gli script del progetto e seguire una chiamata JavaScript tra moduli.", r'''
`package.json` dice quale comando avvia la suite e se il progetto usa moduli ES (`type: module`) o CommonJS. Non cambiare formato di import per risolvere un errore di business: prima verifica la convenzione già usata dai file vicini.

Nei laboratori Node forniti con il materiale, `npm test` usa il runner integrato in Node, senza dipendenze di rete. In un repository reale il comando può essere diverso: il README o gli script del progetto ne indicano uno specifico. In caso di test bloccato, le cause frequenti includono Promise non attese, server lasciati aperti e timer.

Un servizio dovrebbe poter essere testato senza avviare tutta l'applicazione. Se la route restituisce status e body, un test mirato può verificare il contratto senza browser. Leggi anche il test del caso mancante: spesso rivela se si deve restituire `null`, un 404 o un errore propagato.
'''),
    lesson("async-contract", "repository", "Promise, null e contratto HTTP: seguire il dato fino alla risposta", 6, 25, "intermedio",
           ["await", "try/catch", "req.params/query/body", "status code"],
           "Evitare mismatch tra route, servizio e dati asincroni.", r'''
Una funzione `async` restituisce sempre una Promise. Se il controller assegna la chiamata senza `await`, il body della risposta può diventare la Promise stessa; un test che attende `response.body` può nascondere il problema, quindi verifica il tipo effettivo ricevuto.

I parametri di route identificano una risorsa, la query restringe una ricerca e il body porta dati da creare o aggiornare. Un middleware può aver già validato l'input, ma il service deve comunque rappresentare esiti mancanti ed errori secondo il contratto del progetto. `null`, `undefined` e una lista vuota non significano la stessa cosa.

Una route che trova un dato dovrebbe restituire un codice coerente; un identificativo inesistente non deve trasformarsi in una risposta apparentemente riuscita. Leggi i test prima di uniformare tutto a `200` o catturare ogni eccezione. L'errore deve arrivare al posto dove il progetto sa trasformarlo in una risposta utile.
'''),
    lesson("debugging-loop", "repository", "Dal bug distribuito al fix minimo", 6, 25, "intermedio",
           ["riprodurre", "seguire il flusso", "fix locale", "regressione"],
           "Separare osservazioni e ipotesi e verificare che la correzione non sposti il difetto.", r'''
Un bug tra più file raramente si risolve cercando una riga “sbagliata”. Confronta requisito e comportamento, individua un input piccolo che li separa e annota dove il dato entra, cambia e viene restituito. Se la failure è su un filtro, controlla sia il predicato sia il punto in cui quel filtro viene applicato.

Modifica il componente responsabile più vicino alla causa. Un fallback aggiunto in una route può far passare il test senza correggere il service; la stessa anomalia riapparirà in un'altra chiamata. Dopo il test mirato, riesegui la suite intera e guarda i file modificati.

Per gli edge case pensa a `null`, lista vuota, ultimo indice, ID assente, Promise rifiutata e input riutilizzato dopo la chiamata. Se la funzione deve essere pura, confronta l'input con una copia prima e dopo.
'''),
    lesson("ai-assistant", "repository", "Usare l'AI Assistant come supporto al debugging", 6, 20, "intermedio",
           ["domande circoscritte", "contesto con @README", "piano senza codice", "verifica indipendente"],
           "Usare l'assistente come strumento di navigazione senza delegargli il giudizio sul fix.", r'''
Le funzioni dell'assistente HackerRank dipendono dal tipo di domanda e dalla configurazione dell'assessment. La documentazione Candidate Support descrive modalità Guarded e Unguarded; alcune viste consentono domande sui file, altre anche agenti che modificano il progetto. Prima di usarlo, leggi l'interfaccia e le istruzioni dell'invito.

Una domanda buona restringe il problema senza chiedere la soluzione intera: «Spiegami il flusso da questa route al service senza modificare il codice». Puoi aggiungere `@README.md` per dare contesto: «Quale requisito qui descrive il comportamento atteso?». Se il test mostra expected X e actual Y, chiedi quali componenti collegano input e output.

Il giudizio sul fix resta indipendente dall'assistente: il processo comprende lettura del requisito, esame dei file, esecuzione dei test, formulazione di un'ipotesi, richiesta di chiarimenti circoscritti, valutazione della risposta e verifica del cambiamento minimo. Una spiegazione convincente non costituisce una prova; lo sono i test e il contratto del repository.
'''),
    lesson("stack-choice", "repository", "Scegliere lo stack repository: C++ o Node.js", 1, 20, "base",
           ["rapidità di lettura", "toolchain", "contratto multi-file", "mini lab equivalenti"],
           "Confrontare due repository demo che riparano lo stesso comportamento prima di scegliere lo stack.", r'''
Le repository C++ e Node.js mettono in evidenza difficoltà diverse: la prima richiede di seguire header, source e target di compilazione; la seconda di orientarsi tra package, route, service e test. Una prova sulle due opzioni consente di confrontarne la leggibilità e il debugging.

I primi due laboratori sono equivalenti: entrambi espongono `visibleActive` e `findSubject`, entrambi hanno due difetti e gli stessi casi osservabili. Nel C++ si esaminano header, source e test; nel Node `package.json`, service e test. Il tempo di orientamento e il numero di passaggi necessari a ricostruire il flusso forniscono misure confrontabili.

La scelta finale considera leggibilità e correzione, oltre alla sintassi. Un repository reale può differire dagli esempi; restano centrali la capacità di riconoscere package e test, seguire un contratto e interpretare gli errori nel linguaggio selezionato.
'''),
    lesson("leadership-principles", "comportamento", "Leadership Principles attraverso decisioni concrete", 6, 30, "intermedio",
           ["customer impact", "ownership", "evidenza", "principi collegati"],
           "Ragionare sui principi Amazon come criteri che entrano in tensione nei casi reali.", r'''
Un Leadership Principle non è uno slogan da citare: aiuta a spiegare quale risultato cerchi e quale compromesso accetti. Una decisione può coinvolgere più principi; il caso concreto e le prove disponibili determinano come pesarli.

Nel lavoro quotidiano entrano in tensione in modi diversi: Frugality chiede di usare bene le risorse, ma non giustifica tagliare una verifica che protegge i clienti; Hire and Develop the Best si vede quando condividi contesto e feedback utili; Strive to be Earth's Best Employer e Success and Scale Bring Broad Responsibility allargano lo sguardo a persone e impatti oltre il team immediato. Non serve forzare ogni principio in ogni decisione.

Negli scenari, valuta ogni azione per impatto sul cliente, qualità delle prove, reversibilità, responsabilità e comunicazione. Poi leggi il ragionamento: non c'è una formula da recitare, e opzioni diverse possono diventare migliori quando cambia il contesto.
'''),
    lesson("work-simulation", "comportamento", "Work Simulation: scegliere un'azione e spiegare il compromesso", 6, 20, "base",
           ["opzioni plausibili", "valutazione di efficacia", "tradeoff", "debrief"],
           "Allenarsi su decisioni di lavoro SDE senza ridurre gli scenari a risposte ovvie.", r'''
Ogni scenario propone azioni che potrebbero sembrare ragionevoli a prima vista. Prima di ordinarle, chiediti quale informazione manca, quale danno potrebbe continuare mentre indaghi e chi deve sapere cosa. A volte la risposta forte unisce una misura immediata reversibile e una verifica più profonda.

Ordina le opzioni dalla più alla meno efficace; una classifica formativa confronta i rischi descritti, non pretende di conoscere una chiave ufficiale Amazon. Il debrief spiega quale rischio ogni scelta riduce e quale lascia aperto. Se la tua classifica differisce, cerca l'assunzione diversa: gravità, tempo, autorità, impatto o qualità dei dati.

Gli scenari sono originali e ispirati a decisioni quotidiane SDE: release, incidenti, review, requisiti incompleti, colleghi, test instabili, rollback e debito tecnico. Non sono domande reali né materiali riservati.
'''),
    lesson("work-style", "comportamento", "Work Style: familiarizzarsi senza recitare un personaggio", 6, 15, "base",
           ["leggere ogni frase", "coerenza", "riflessione personale", "nessuna manipolazione"],
           "Prendersi il tempo di leggere e rispondere con coerenza, senza ottimizzare un profilo inventato.", r'''
Gli item Work Style possono presentare affermazioni o scelte ripetute. Leggi ogni frase per intero, inclusi avverbi come “sempre” e “raramente”; una parola cambia il significato. Se una risposta richiede un episodio, pensa a un fatto concreto invece di scegliere il tratto che sembra più apprezzato.

La familiarizzazione serve a ridurre errori di fretta e risposte che si contraddicono per distrazione. Non costruire un sistema per manipolare il personality assessment e non memorizzare un profilo ideale.

Se un item sembra ambiguo, rileggilo e rispondi secondo il tuo modo abituale di lavorare. Il contesto culturale dei Leadership Principles aiuta a capire il linguaggio della prova; non rende autentica una risposta inventata.
'''),
    lesson("full-mock", "simulazioni", "Full Mock: 40 minuti, stop, poi 60 minuti", 6, 35, "intermedio",
           ["timer indipendenti", "consegna della prima sezione", "repository in ambiente distinto", "no backtracking"],
           "Completare un mock sequenziale che non trasferisce il tempo tra coding e repository.", r'''
Avvia la Coding Question soltanto quando sei pronto. Il timer parte da 40:00; puoi eseguire i test locali, ma non vedrai hint o soluzione. Se consegni prima, il tempo residuo si perde: la sezione successiva parte comunque da 60:00.

Il passaggio alla repository è un cambio di contesto, non una pausa da aggiungere al primo timer. Apri la cartella del mock in VS Code, leggi README e test e annota il comportamento atteso. Durante la sezione non è possibile tornare alla schermata coding tramite i controlli normali.

Allo scadere dei 60 minuti il mock termina. La revisione distingue le attività completate dalle ipotesi effettivamente verificate. Work Simulation e Work Style sono attività successive e separate. Il mock adotta il formato di pratica 40 + 60; struttura e regole di un assessment reale dipendono dalle istruzioni ricevute.
'''),
]


next(item for item in LESSONS if item["id"] == "sde-l-graphs")["body"] += """

### Copiare il grafo: valori e identità

Due nodi possono avere lo stesso valore e restare oggetti diversi. Per clonare una
componente conserva una mappa `originale -> copia`. Crea e registra la copia appena
scopri un nodo, prima di seguire i vicini. In un ciclo A -> B -> A, la seconda visita
ad A riusa la copia già registrata: non ricomincia a clonare per sempre. Per ciascun
arco aggiungi alla copia del nodo il riferimento alla copia del vicino, preservando
anche ordine e archi ripetuti. Clone Graph combina la mappa per identità con la visita in profondità o in ampiezza.
"""
next(item for item in LESSONS if item["id"] == "sde-l-heap")["body"] += """

### Distanze con pesi positivi: Dijkstra

La BFS minimizza il numero di archi; con pesi diversi quel numero non è il costo.
Dijkstra mantiene distanze provvisorie e un min-heap `(distanza,nodo)`. Dal nodo
estratto prova ogni arco: se `distanza[u]+peso < distanza[v]`, aggiorna v e accoda
la nuova coppia. Una vecchia coppia può restare nel heap: scartala se la distanza
non coincide più con quella registrata. Con A->C di costo 10 e A->B->C di costi
1 e 2, C viene prima proposto a 10, poi migliorato a 3. Non segnare C definitivamente
quando lo inserisci. La correttezza della scelta minima richiede pesi non negativi;
il lab Network Delay usa pesi positivi e applica la stessa logica a un grafo completo.
"""


STUDY_PLAN = [
    {"day": 1, "title": "Riprendere il controllo del codice", "lesson_ids": [
        "sde-l-oa-format", "sde-l-problem-solving", "sde-l-language-choice", "sde-l-python-toolkit",
        "sde-l-cpp-toolkit", "sde-l-complexity", "sde-l-arrays-strings", "sde-l-hashmap-set",
        "sde-l-repo-orientation", "sde-l-stack-choice",
    ], "exercise_ids": ["sde-e-language-trial", "sde-e-two-sum", "sde-e-contains-duplicate", "sde-e-valid-anagram"],
       "lab_ids": ["lab-amazon-cpp-demo", "lab-amazon-node-demo"]},
    {"day": 2, "title": "Pattern fondamentali", "lesson_ids": [
        "sde-l-two-pointers", "sde-l-sliding-window", "sde-l-prefix-sum", "sde-l-sorting-intervals",
        "sde-l-mixed-patterns",
    ], "exercise_ids": ["sde-e-valid-palindrome", "sde-e-two-sum-sorted", "sde-e-move-zeroes", "sde-e-subarray-sum", "sde-e-merge-intervals"], "simulation_ids": ["sde-sim-coding-25"]},
    {"day": 3, "title": "Ricerca e strutture lineari", "lesson_ids": [
        "sde-l-stack-queue", "sde-l-monotonic-stack", "sde-l-binary-search", "sde-l-binary-boundaries",
        "sde-l-binary-variants", "sde-l-binary-answer",
    ], "exercise_ids": ["sde-e-valid-parentheses", "sde-e-binary-search", "sde-e-first-true", "sde-e-lower-bound", "sde-e-search-rotated", "sde-e-min-eating-speed", "sde-e-daily-temperatures", "sde-e-search-range"]},
    {"day": 4, "title": "Strutture collegate e grafi", "lesson_ids": [
        "sde-l-linked-lists", "sde-l-recursion", "sde-l-tree-traversal", "sde-l-bst-paths",
        "sde-l-bfs-dfs-grid", "sde-l-graphs", "sde-l-topological-sort",
    ], "exercise_ids": ["sde-e-reverse-list", "sde-e-max-depth", "sde-e-tree-diameter", "sde-e-number-islands", "sde-e-connected-components", "sde-e-oranges-rotting", "sde-e-course-schedule"]},
    {"day": 5, "title": "Problemi più complessi e pratica a tempo", "lesson_ids": [
        "sde-l-heap", "sde-l-greedy", "sde-l-backtracking", "sde-l-dp-memoization",
        "sde-l-dp-models", "sde-l-timed-dsa",
    ], "exercise_ids": ["sde-e-kth-largest", "sde-e-subsets", "sde-e-climbing-stairs", "sde-e-house-robber", "sde-e-word-break", "sde-e-interval-scheduling"],
       "simulation_ids": ["sde-sim-coding-40"]},
    {"day": 6, "title": "Repository, decisioni e simulazione finale", "lesson_ids": [
        "sde-l-tests-stack-traces", "sde-l-cpp-repository", "sde-l-node-repository",
        "sde-l-async-contract", "sde-l-debugging-loop", "sde-l-ai-assistant",
        "sde-l-leadership-principles", "sde-l-work-simulation", "sde-l-work-style", "sde-l-full-mock",
    ], "simulation_ids": ["sde-full-mock"], "scenario_ids": ["sde-ws-01", "sde-ws-09"],
       "work_style_ids": ["sde-style-01"], "practice_minutes": 30},
]

# Core branches protect continuity after the initial comparison.
STUDY_PLAN[0]["lesson_ids"].remove("sde-l-python-toolkit")
STUDY_PLAN[0]["lesson_ids"].remove("sde-l-cpp-toolkit")
STUDY_PLAN[0]["choices"] = [{"setting": "coding_language", "options": {
    "python": {"lesson_ids": ["sde-l-python-toolkit"]},
    "cpp": {"lesson_ids": ["sde-l-cpp-toolkit"]},
}}]
STUDY_PLAN[0]["comparison_minutes"] = 8  # Second run of the same language trial.
STUDY_PLAN[1]["choices"] = [{"setting": "repository_language", "options": {
    "node": {"lesson_ids": ["sde-l-node-repository", "sde-l-async-contract"], "lab_ids": ["lab-amazon-node-async"]},
    "cpp": {"lesson_ids": ["sde-l-cpp-repository"], "lab_ids": ["lab-amazon-cpp-inventory"]},
}}]
STUDY_PLAN[3]["exercise_ids"].extend(["sde-e-validate-bst", "sde-e-linked-list-cycle"])
STUDY_PLAN[2]["choices"] = [{"setting": "repository_language", "options": {
    "node": {"lab_ids": ["lab-amazon-node-contract"]},
    "cpp": {"practice_minutes": 40},  # Reimplement the inventory repair and regression without guidance.
}}]
STUDY_PLAN[5]["lesson_ids"].remove("sde-l-cpp-repository")
STUDY_PLAN[5]["lesson_ids"].remove("sde-l-node-repository")
STUDY_PLAN[5]["lesson_ids"].remove("sde-l-async-contract")
STUDY_PLAN[2]["exercise_ids"].remove("sde-e-first-true")
STUDY_PLAN[2]["exercise_ids"].remove("sde-e-lower-bound")
STUDY_PLAN[3]["exercise_ids"].remove("sde-e-tree-diameter")
for day in STUDY_PLAN:
    day["flashcard_minutes"] = 15
    day["review_minutes"] = 20
    day["practice_minutes"] = int(day.get("practice_minutes", 0)) + 35 + int(day.get("comparison_minutes", 0))



LESSON_DIDACTIC = {
    "sde-l-oa-format": {
        "notes": r'''### Esempio svolto: riconoscere che tipo di lavoro ti viene chiesto

Immagina di ricevere una di queste due richieste.

**Richiesta A — costruire una funzione.** «Dato un elenco di temperature, restituisci l'indice della prima temperatura almeno pari a 30.» Con `[18, 30, 27]`, controlli l'indice 0: `18` non basta; controlli l'indice 1: `30` soddisfa la condizione, quindi il risultato è 1. Qui il comportamento atteso viene dalla frase della consegna. Prima di scrivere codice, chiediti anche cosa restituire se nessuna temperatura raggiunge 30.

**Richiesta B — correggere un progetto.** Un test dice che `getTemperature("Milano")` dovrebbe restituire 30, ma riceve `null`. Il test dà il risultato atteso; il codice esistente mostra invece quello osservato. Il passo successivo è riprodurre il test e seguire il dato dalla route alla funzione che legge le temperature. Riscrivere una nuova ricerca prima di trovare dove il dato si perde rischia di correggere il posto sbagliato.

| Passo | Funzione nuova | Progetto esistente |
| --- | --- | --- |
| Prima fonte | Contratto scritto nella richiesta | Test, README e chiamanti |
| Prova piccola | `[18, 30, 27]` deve dare l'indice 1 | Il test nominato deve riprodurre `null` |
| Obiettivo | Implementare tutti i casi del contratto | Localizzare la causa e cambiare il punto responsabile |

Entrambi i lavori possono richiedere di programmare, ma il primo parte da una specifica e il secondo da un comportamento già presente. Durante una Work Simulation, invece, non c'è una funzione da implementare: devi motivare una decisione usando impatto, prove disponibili e persone da coinvolgere. Le istruzioni del tuo invito stabiliscono quali attività siano davvero previste.''',
        "recap": "Prima identifica quale capacità e quale comportamento osservabile vengono richiesti; poi applica le regole della prova specifica.",
        "practice": [("simulation", "sde-full-mock"), ("scenario", "sde-ws-01")],
    },
    "sde-l-problem-solving": {
        "notes": r'''### Esempio svolto: trasformare una frase in una scansione

Richiesta: «Restituisci l'indice del primo valore strettamente maggiore di `limite`; se non esiste, restituisci `-1`.» Usiamo `values = [2, 7, 1, 9]` e `limite = 5`.

| Indice | Valore | Domanda | Decisione |
| ---: | ---: | --- | --- |
| 0 | 2 | `2 > 5`? | No, passa al successivo |
| 1 | 7 | `7 > 5`? | Sì, restituisci 1 e fermati |

Il risultato è 1: non serve esaminare il 9, perché la parola «primo» impone di fermarsi alla prima corrispondenza. Una scansione possibile è:

```text
per ogni indice i da sinistra a destra:
    se values[i] > limite:
        restituisci i
restituisci -1
```

Proviamo ora due casi che possono smentire una soluzione frettolosa: con `[5, 4]` la risposta è `-1` perché la condizione è strettamente maggiore, non maggiore o uguale; con `[]` la scansione non entra nel ciclo e restituisce comunque `-1`. Il ragionamento resta lo stesso anche quando cambi algoritmo: traduci le parole importanti in confronti precisi, poi segui un input fino al risultato.''',
        "recap": "Un'invariante descrive che cosa è già stato dimostrato dopo ogni passo; i test cercano di falsificarla.",
        "practice": [("exercise", "sde-e-two-sum"), ("exercise", "sde-e-contains-duplicate")],
    },
    "sde-l-language-choice": {
        "notes": r'''### Esempio svolto a mano: aggiornare una finestra

Prima di confrontare Python e C++, seguiamo un input piccolo che non è quello della mini-prova: `[1, 3, 2, 5]`, con finestre di `k=2` elementi consecutivi. La prima finestra è `[1, 3]`, la somma è 4. Per spostarla a destra non rifacciamo tutta l'addizione: togliamo il valore che esce e aggiungiamo quello che entra.

| Finestra | Calcolo rispetto alla precedente | Somma |
| --- | --- | ---: |
| `[1, 3]` | `1 + 3` | 4 |
| `[3, 2]` | `4 - 1 + 2` | 5 |
| `[2, 5]` | `5 - 3 + 5` | 7 |

Il massimo dell'esempio è 7. Nota il controllo manuale: le finestre sono tre, quindi devono comparire esattamente tre somme. Se il tuo programma ne producesse due o quattro, sospetteresti subito un errore nel confine del ciclo.

Ripeti poi la stessa mini-prova in entrambi i linguaggi. Annota non solo il tempo di scrittura, ma anche se hai aggiornato correttamente la finestra e quanto hai impiegato a trovare un eventuale errore. Così confronti la familiarità reale con l'editor, gli indici e gli strumenti, non la quantità di caratteri digitati.''',
        "recap": "Scegli sulla base della soluzione corretta e del tempo rimasto per verificarla, non della brevità del codice.",
        "practice": [("exercise", "sde-e-language-trial")],
    },
    "sde-l-python-toolkit": {
        "notes": r'''### Esempio svolto: costruire un dizionario passo dopo passo

Vogliamo sommare punti per squadra. Partiamo da `events = [("blu", 2), ("oro", 1), ("blu", 3)]` e da un dizionario vuoto. `get(squadra, 0)` restituisce il totale precedente, oppure zero quando la squadra compare per la prima volta.

```python
def totals_by_team(events):
    totals = {}
    for team, points in events:
        totals[team] = totals.get(team, 0) + points
    return totals

print(totals_by_team([("blu", 2), ("oro", 1), ("blu", 3)]))
# {'blu': 5, 'oro': 1}
```

| Passo | Coppia letta | Dizionario dopo l'aggiornamento |
| ---: | --- | --- |
| 1 | `("blu", 2)` | `{"blu": 2}` |
| 2 | `("oro", 1)` | `{"blu": 2, "oro": 1}` |
| 3 | `("blu", 3)` | `{"blu": 5, "oro": 1}` |

La lista resta nell'ordine iniziale; il dizionario conserva un totale per chiave. Per esplorare una coda, invece, usa `deque`: da `[A, B]`, `popleft()` restituisce A e lascia `[B]`. Un heap non è una lista completamente ordinata: con `heapq`, `heappop` restituisce il minimo corrente, ma gli altri elementi possono apparire in un ordine diverso.

Infine confronta `sorted(values)`, che crea una nuova lista, con `values.sort()`, che modifica quella esistente. Prima di usare un'API, chiediti sempre quale dato cambia e quale rimane. Questo piccolo controllo evita bug difficili da vedere quando il caso di prova contiene un solo elemento.''',
        "recap": "Scegli il contenitore in base all'operazione richiesta e ricorda quando un'API modifica o copia i dati.",
        "practice": [("exercise", "sde-e-language-trial"), ("exercise", "sde-e-two-sum")],
    },
    "sde-l-cpp-toolkit": {
        "notes": r'''### Esempio svolto: leggere una sequenza senza copiarla

Considera tre rilevazioni `[18, 20, 17]`. Vogliamo contare quante superano 18. La funzione riceve il vector per riferimento costante: può leggere i valori, non modificarli e non deve creare una copia dell'intera sequenza.

```cpp
#include <vector>
using namespace std;

int count_above(const vector<int>& values, int limit) {
    int count = 0;
    for (const auto& value : values) {
        if (value > limit) {
            ++count;
        }
    }
    return count;
}
```

Seguiamo il ciclo: `18 > 18` è falso, quindi `count` resta 0; `20 > 18` è vero, quindi diventa 1; `17 > 18` è falso. La funzione restituisce 1 e il vector originale resta `[18, 20, 17]`. Il tempo è `O(n)` e la memoria aggiuntiva `O(1)`.

`const vector<int>&` descrive due scelte distinte: `&` evita la copia e `const` vieta la modifica attraverso quel parametro. `const auto&` applica la stessa cautela a ogni elemento del ciclo. Se servisse davvero cambiare la sequenza, la firma non dovrebbe nascondere quella mutazione.

Quando usi `size()`, ricorda che il tipo è unsigned. Per un vector vuoto, `size()-1` non vale -1: il risultato diventa un numero enorme. Controlla `empty()` prima di accedere all'ultimo indice; quando non ti serve l'indice, il range-based `for` evita proprio quel confine.''',
        "recap": "In C++ il tipo del contenitore e il suo contratto contano quanto l'algoritmo: evita copie, dereferenziazioni invalide e mutazioni implicite.",
        "practice": [("exercise", "sde-e-language-trial"), ("exercise", "sde-e-binary-search")],
    },
    "sde-l-complexity": {
        "notes": r'''### Esempio svolto: da un ciclo al suo costo

Un doppio ciclo che confronta ogni coppia distinta non esegue `n × n` confronti, perché non confronta un elemento con sé stesso e non ripete le coppie al contrario. Con quattro elementi, il primo indice ha 3 valori successivi da provare, il secondo ne ha 2, il terzo ne ha 1 e l'ultimo ne ha 0: `3 + 2 + 1 + 0 = 6` confronti.

| Elementi `n` | Confronti | Formula |
| ---: | ---: | --- |
| 4 | 6 | `3 + 2 + 1 + 0` |
| 8 | 28 | `7 + 6 + ... + 1 + 0` |
| 100 | 4.950 | `100 × 99 / 2` |

La formula generale è `n(n-1)/2`. Il termine dominante è `n²`, perciò la classe di crescita è `O(n²)`. Una singola scansione che visita ogni elemento una volta fa invece 4, 8 e 100 visite: è `O(n)`. Non abbiamo cronometrato il computer; abbiamo contato operazioni che crescono con l'input.

Per stimare lo spazio, fai una domanda separata: «che cosa resta allocato mentre elaboro tutti gli elementi?». Due indici e un contatore occupano `O(1)` spazio aggiuntivo; un dizionario con una voce per ogni valore distinto cresce fino a `O(n)`. La lista restituita fa parte dell'output e va distinta dalla memoria ausiliaria. Big-O descrive questa crescita, non i millisecondi esatti.''',
        "recap": "Descrivi quante volte vengono visitati gli elementi e quale memoria cresce con n; poi confronta la stima coi vincoli.",
        "practice": [("exercise", "sde-e-two-sum"), ("exercise", "sde-e-contains-duplicate")],
    },
    "sde-l-arrays-strings": {
        "notes": r'''### Esempio svolto: leggere un intervallo senza sbagliare il confine

Molte API rappresentano una porzione con `[left, right)`: l'indice `left` è incluso e `right` è escluso. Con `values = [10, 20, 30, 40]`, scegliendo `left = 1` e `right = 3` leggi gli elementi agli indici 1 e 2, cioè `[20, 30]`. La lunghezza è `right - left = 2`.

| Valori di `left` e `right` | Indici letti | Risultato |
| --- | --- | --- |
| `0, 4` | `0, 1, 2, 3` | `[10, 20, 30, 40]` |
| `1, 3` | `1, 2` | `[20, 30]` |
| `2, 2` | nessuno | intervallo vuoto `[]` |

Il caso `left == right` è valido e vuoto; non devi leggere `values[right]`. Per questo la condizione tipica di un ciclo è `i < right`, non `i <= right`. La stessa convenzione rende più semplice calcolare la lunghezza e concatenare porzioni adiacenti senza contare due volte il confine.

Nel compattamento in-place della lezione, `read` indica il prossimo elemento da esaminare e `write` la prossima posizione del prefisso valido. Se nessun elemento supera il filtro, `write` rimane 0: il risultato è un prefisso vuoto anche se la vecchia memoria dell'array contiene ancora valori oltre il confine. Chi usa il risultato deve rispettare la lunghezza restituita.''',
        "recap": "Gli indici di lettura e scrittura rendono esplicito il prefisso già valido; inizializza gli accumuli in base ai casi ammessi.",
        "practice": [("exercise", "sde-e-move-zeroes"), ("exercise", "sde-e-max-subarray"), ("exercise", "sde-e-stock-profit")],
    },
    "sde-l-hashmap-set": {
        "notes": r'''### Come decidere che cosa conservare

Rileggi la domanda che la struttura deve rendere veloce: «questa chiave esiste?», «quante volte è comparsa?», «qual era l'indice?». Un `set` conserva le chiavi e basta; una mappa conserva una coppia chiave-valore. Nell'esempio dei movimenti, la chiave era una zona e il valore era il totale. Per frequenze il valore diventa un conteggio; per un indice, diventa la posizione.

Un controllo manuale utile è seguire la stessa chiave due volte. Alla prima occorrenza deve partire dal valore iniziale del problema (spesso zero); alla seconda deve leggere lo stato precedente e aggiornarlo. Se l'aggiornamento dimentica il passato o lo salva con una chiave diversa, la tabella dei passaggi lo rende visibile prima di eseguire il programma.

Gli esercizi successivi useranno mappe per domande differenti. Prima di scegliere il pattern, scrivi in una frase che cosa rappresenta il valore associato a ciascuna chiave: così eviti di trattare tutte le mappe come se fossero semplici contenitori di numeri.''',
        "recap": "Prima di creare una mappa, formula la domanda che ogni chiave deve rendere veloce e annota cosa viene memorizzato.",
        "practice": [("exercise", "sde-e-two-sum"), ("exercise", "sde-e-valid-anagram"), ("exercise", "sde-e-group-anagrams")],
    },
    "sde-l-two-pointers": {
        "notes": r'''### Gli altri modi in cui si incontrano due indici

Per verificare se `sub` è sottosequenza di `text`, scorri `text` sempre in avanti e fai avanzare l'indice di `sub` soltanto dopo una corrispondenza. Non servono due puntatori agli estremi: la relazione importante è l'ordine delle corrispondenze. Se i caratteri di `sub` non finiscono, non è una sottosequenza.

Per un palindromo, invece, confronti gli estremi. Se il contratto ignora spazi e punteggiatura, salta quei caratteri prima del confronto e normalizza le lettere. La stringa vuota è palindroma per definizione perché non esiste una coppia che la contraddica.

In `Container With Most Water`, l'area dipende dalla parete più bassa. Spostare la parete più alta restringe il contenitore senza poter superare l'altezza già limitante; ha senso provare a muovere quella più bassa. In `Trapping Rain Water`, i massimi osservati da sinistra e destra determinano un limite affidabile dal lato con il massimo minore. Con le altezze `[2,0,2]`, sopra la barra centrale restano 2 unità.

Per `Three Sum`, ordina una copia, fissa un valore e usa la ricerca agli estremi per il complemento. Dopo aver trovato una tripletta, salta i valori uguali per non produrre lo stesso risultato più volte: l'ordinamento aiuta sia la decisione sia il controllo dei duplicati. Il tempo è `O(n²)` dopo l'ordinamento; se ordini una copia, essa richiede `O(n)` spazio.''',
        "recap": "Due puntatori funzionano quando una proprietà consente di motivare quale parte dei candidati eliminare a ogni passo.",
        "practice": [("exercise", "sde-e-two-sum-sorted"), ("exercise", "sde-e-three-sum"), ("exercise", "sde-e-trapping-rainwater")],
    },
    "sde-l-sliding-window": {
        "notes": r'''### Aggiornare frequenze e molteplicità

Per la sottostringa senza ripetizioni in `abba`, una mappa ricorda l'ultimo indice di ogni carattere. Dopo aver letto `a` e `b`, la finestra valida è `ab` e la lunghezza migliore è 2. Al secondo `b`, la sua ultima posizione era 1: porta `left` a 2. La `a` finale era stata vista prima dell'intervallo corrente, quindi `left` resta 2 e `ba` mantiene il massimo 2.

| Indice | Carattere | Ultima posizione nota | `left` dopo l'aggiornamento | Finestra valida | Migliore |
| ---: | --- | ---: | ---: | --- | ---: |
| 0 | `a` | nessuna | 0 | `a` | 1 |
| 1 | `b` | nessuna | 0 | `ab` | 2 |
| 2 | `b` | 1 | 2 | `b` | 2 |
| 3 | `a` | 0 | 2 | `ba` | 2 |

Per `s="ABAAC"` e `t="AA"`, la finestra deve contenere due occorrenze di `A`, non semplicemente la lettera `A`. Un contatore `missing` parte da 2: entrando nella finestra una `A` lo porta a 1, la seconda a 0; solo allora la finestra è valida e si può provare ad accorciarla. Quando una `A` richiesta esce, `missing` torna a 1. Le frequenze rendono verificabile la molteplicità.

Partendo da `left=0`, quando la finestra `ABA` ha già due A, è valida e lunga 3. Togliere la prima A la rende incompleta. Più avanti la finestra `BAA` torna valida; si può togliere la B senza perdere una A, ottenendo `AA` di lunghezza 2. Togliere una delle due A la rende di nuovo invalida, perciò la scansione ha trovato il minimo.

Per `AABABBA` con `k=1`, `AABA` è una finestra valida: lunghezza 4, tre A, una sostituzione. `AABAB` ha lunghezza 5 ma solo tre A, quindi servirebbero due sostituzioni. La condizione è `lunghezza - frequenza_massima <= k`. Il calcolo della frequenza massima e il momento in cui si restringe fanno parte dell'invariante: non riusare alla cieca il criterio della somma positiva.''',
        "recap": "La finestra risparmia lavoro perché ogni elemento entra ed esce un numero limitato di volte; la monotonia della condizione va dimostrata.",
        "practice": [("exercise", "sde-e-min-subarray-len"), ("exercise", "sde-e-longest-substring"), ("exercise", "sde-e-min-window")],
    },
    "sde-l-prefix-sum": {
        "notes": r'''### Dalla somma all'indice

Per `Product Except Self` non si divide: nel primo passaggio il risultato all'indice i riceve il prodotto a sinistra; nel secondo si moltiplica per il prodotto a destra. Con `[2,3,4]`, i prefissi esclusivi sono `[1,2,6]`, poi si combinano coi suffissi `[12,4,1]` ottenendo `[12,8,6]`. Anche gli zeri funzionano senza un ramo dedicato.

Per un pivot in `[1,7,3,6,5,6]`, al valore 6 i prefissi sinistro e destro sommano entrambi 11. Mantenendo `left_sum` e il totale, il lato destro si calcola come `total-left_sum-current`; così si visita ogni elemento una volta senza costruire due array di prefissi. Il vettore risultato non si conta come spazio ausiliario quando il contratto richiede proprio quell'output.''',
        "recap": "I prefissi trasformano un intervallo in una differenza; la mappa conta i prefissi precedenti che completano il valore richiesto.",
        "practice": [("exercise", "sde-e-subarray-sum"), ("exercise", "sde-e-pivot-index"), ("exercise", "sde-e-product-except-self")],
    },
    "sde-l-sorting-intervals": {
        "notes": r'''### Casi da chiarire prima di fondere

Considera un intervallo contenuto in un altro: fondere `[2,8]` con `[3,5]` deve lasciare `[2,8]`, non accorciare la fine. Per questo si usa `max(fine_corrente, fine_nuova)`.

Per `Meeting Rooms`, in `[1,3)` e `[3,5)` la seconda riunione riusa la sala: il primo intervallo termina prima che il successivo cominci. Non confondere il conteggio di sovrapposizioni simultanee con la produzione di intervalli uniti. In entrambi i problemi ordini i confini, ma la variabile che mantieni e la risposta richiesta cambiano.''',
        "recap": "Ordinare rende locale il confronto, mentre la convenzione sugli estremi resta parte del contratto e va mantenuta nei test.",
        "practice": [("exercise", "sde-e-merge-intervals"), ("exercise", "sde-e-meeting-rooms"), ("exercise", "sde-e-insert-interval")],
    },
    "sde-l-mixed-patterns": {
        "notes": r'''### Stesso lessico, invarianti diverse

Considera tre richieste di coppia: «trova una coppia in un array crescente» suggerisce due puntatori perché l'ordine elimina candidati; «restituisci due indici nell'array originale non ordinato» può usare una mappa senza perdere l'identità degli indici; «trova tutte le triple uniche» richiede gestire duplicati oltre a trovare somme. La parola “coppia” da sola non seleziona il pattern.

Un modo rapido per decidere è annotare input, output, vincolo di ordine e dimensione: se l'input è piccolo, il doppio ciclo può essere chiaro e sufficiente; se n=100.000 e il prompt richiede tempo lineare atteso, memorizzare gli elementi visti cambia la scala. Prova poi a rompere la tua ipotesi: un duplicato, nessuna soluzione, valori negativi oppure molti dati senza risposta.

Le esercitazioni più utili per il confronto sono due con requisiti vicini ma invarianti diverse: **Two Sum** e **Two Sum Sorted**, poi **Subarray Sum** e **Merge Intervals**. Prima spiega perché il movimento o la memoria è valido; solo dopo scrivi il ciclo.''',
        "recap": "Il pattern deriva da un invariante e dal contratto, non da una parola chiave isolata.",
        "practice": [("exercise", "sde-e-two-sum"), ("exercise", "sde-e-two-sum-sorted"), ("exercise", "sde-e-subarray-sum")],
    },
    "sde-l-stack-queue": {
        "notes": r'''### Dalla FIFO alle visite per livelli

Immagina gli archi `A→B`, `A→C`, `B→D`. Una BFS parte dalla coda `[A]`, visita A e accoda B e C: `[B,C]`. Estrae B e accoda D: `[C,D]`. Prima di D visita C, così tutte le distanze 1 sono trattate prima della distanza 2. In Python usa `collections.deque` e `popleft()`; in C++ `queue.front()` legge la testa e `queue.pop()` la rimuove.

Questa proprietà dà un cammino minimo solo se ogni arco costa lo stesso. Con pesi diversi, una coda FIFO non ordina per costo: occorre un algoritmo come Dijkstra.''',
        "recap": "Stack = ultimo entrato, primo uscito; queue = primo entrato, primo uscito. La scelta codifica l'ordine corretto.",
        "practice": [("exercise", "sde-e-valid-parentheses")],
    },
    "sde-l-monotonic-stack": {
        "notes": r'''### Un rettangolo che aspetta il proprio confine

Nell'istogramma `[2,1,2]`, l'indice 0 di altezza 2 non può estendersi oltre l'indice 1: lì compare una barra più bassa. Quando l'indice 1 viene rimosso, la barra di altezza 1 ha trovato il proprio confine destro; il nuovo indice in cima allo stack determina il confine sinistro. La larghezza è `right-left`, quindi la barra bassa forma un rettangolo di area `1·3=3`.

Una sentinella finale di altezza 0 forza a chiudere le barre rimaste. Le altezze uguali richiedono una condizione coerente: usando `<` o `<=` cambia quale copia resta come candidato, perciò prova anche istogrammi piatti e una singola barra.''',
        "recap": "Lo stack monotono elimina un candidato solo quando il nuovo elemento ne determina la risposta o lo rende inutile.",
        "practice": [("exercise", "sde-e-daily-temperatures"), ("exercise", "sde-e-largest-rectangle")],
    },
    "sde-l-binary-search": {
        "notes": r'''### Un errore plausibile: conservare il medio

Con l'intervallo chiuso, dopo aver confrontato `mid` quel valore è già stato escluso, quindi gli aggiornamenti usano `mid+1` o `mid-1`. Se al posto di `right = mid-1` scrivi `right = mid`, e il target è minore del valore al centro di un intervallo di due elementi, `mid` può restare uguale: il ciclo non termina. Un invariante scritto prima del codice rende visibile il problema.

Questo schema trova una qualsiasi occorrenza. Con duplicati non promette la prima: Lower Bound e Upper Bound cercano un confine e adottano un intervallo semiaperto, con aggiornamenti leggermente diversi.''',
        "recap": "La binary search è una prova ripetuta che una metà non può contenere la risposta; l'invariante decide gli aggiornamenti.",
        "practice": [("exercise", "sde-e-binary-search")],
    },
    "sde-l-binary-boundaries": {
        "notes": r'''### Intervallo degli indici uguali

Il range di un target usa Lower Bound per il primo indice con valore almeno pari e Upper Bound per il primo indice strettamente maggiore. Se il primo confine è `n` o punta a un valore diverso, l'elemento non c'è; altrimenti l'ultimo indice è `upper-1`. Su `[1,2,2,2,5]`, i confini sono 1 e 4 e il range è `[1,3]`.

Se cerchi una proprietà booleana invece di un numero, lo schema è lo stesso: individua il primo punto in cui il predicato passa da falso a vero. Binary Search on Answer fa questa ricerca sul dominio delle soluzioni e richiede una dimostrazione di monotonia.''',
        "recap": "La ricerca di confine restituisce un punto fra elementi, che può coincidere con n; definisci il predicato prima del ciclo.",
        "practice": [("exercise", "sde-e-lower-bound"), ("exercise", "sde-e-search-range"), ("exercise", "sde-e-first-true")],
    },
    "sde-l-binary-variants": {
        "notes": r'''### Quando i duplicati nascondono la rotazione

Se `nums[left]`, `nums[mid]` e `nums[right]` sono uguali, il confronto non rivela quale metà contenga il taglio. Puoi ridurre un estremo di un elemento senza perdere una soluzione, ma in un array di molti valori uguali ciò richiede `O(n)` passi. L'esercizio dichiara valori distinti, quindi il codice può garantire `O(log n)`.

Questa ricerca cerca un elemento in una sequenza ruotata. Binary Search on Answer non confronta i valori dell'array: ordina il dominio di una possibile risposta e cerca dove un predicato passa da falso a vero.''',
        "recap": "La rotazione conserva una metà ordinata; restringi l'intervallo in base ai suoi estremi e alle ipotesi sui duplicati.",
        "practice": [("exercise", "sde-e-search-rotated")],
    },
    "sde-l-binary-answer": {
        "notes": r'''### Prima dimostra gli estremi

Non basta che il predicato sia monotono: almeno una risposta valida deve stare in `[low,high]`. Per il problema delle pile, `low=1` è la velocità minima positiva; `high=max(piles)` svuota ogni pila in un'ora, quindi è una soluzione se `hours >= len(piles)`. Se quest'ultima condizione manca, non c'è risposta nel dominio.

Il codice usa un intervallo chiuso che contiene un valore fattibile. È diverso dalla convenzione che conserva esplicitamente un punto falso e uno vero escluso: entrambe funzionano, ma non vanno mischiate nello stesso aggiornamento.''',
        "recap": "Binary Search on Answer richiede una risposta ordinabile, un predicato monotono e limiti che racchiudono una risposta valida.",
        "practice": [("exercise", "sde-e-min-eating-speed")],
    },
    "sde-l-linked-lists": {
        "notes": r'''### Come ragionare su un ciclo e su una fusione

In `1→2→3→4→2`, il nodo 4 torna al 2. Partendo entrambi da 1, dopo un passo `slow=2, fast=3`; dopo il successivo `slow=3, fast=2`; al terzo `slow=4, fast=4`. La visita incontra un nodo già attraversato senza memorizzare l'intera catena. Se la lista finisse, il controllo di `fast` e `fast.next` impedirebbe di oltrepassare `None`/`nullptr`.

Per fondere `k` liste ordinate, un min-heap conserva una sola testa per lista: estrai la più piccola, collegala al risultato e inserisci il suo successore. Con `N` nodi, il tempo è `O(N log k)` e lo heap usa `O(k)` spazio. Una LRU aggiunge invece una mappa chiave→nodo e due link per spostare un nodo noto in testa in `O(1)`; le sentinelle semplificano le operazioni ai bordi.''',
        "recap": "I collegamenti sono riferimenti modificabili: conserva il prossimo nodo prima di riscriverli e usa una mappa solo quando serve accesso diretto.",
        "practice": [("exercise", "sde-e-reverse-list"), ("exercise", "sde-e-linked-list-cycle"), ("exercise", "sde-e-lru-cache")],
    },
    "sde-l-recursion": {
        "notes": r'''### Profondità delle chiamate e lavoro ripetuto

La profondità dello stack misura quante chiamate restano sospese contemporaneamente; il numero totale di chiamate può essere molto più grande. Fibonacci ingenuo crea un albero di chiamate: `F(5)` chiede `F(4)` e `F(3)`, mentre `F(4)` chiede ancora `F(3)`. Il valore dello stesso stato viene ricalcolato. Una memoization può salvare i risultati soltanto quando le chiamate condividono sottoproblemi; la lezione seguente separa stato, transizione e cache.

Per un albero, il caso base `None → 0` si combina con i risultati dei figli: la profondità è uno più la maggiore profondità dei sottoalberi. Questa forma postorder generalizza la somma ricorsiva del capitolo. La visita fa `O(n)` chiamate, ma la memoria resta `O(h)`; una catena di `n` nodi può raggiungere profondità `n` anche se il lavoro totale è lineare.''',
        "recap": "Definisci prima che cosa restituisce ogni chiamata, qual è la base e come il problema diventa più piccolo.",
        "practice": [("exercise", "sde-e-max-depth")],
    },
    "sde-l-tree-traversal": {
        "notes": r'''### Separare i livelli durante la BFS

Per visita per livelli, la coda iniziale contiene la radice 1. Dopo averla estratta, accoda 2 e 3. Salva `level_size=2`, poi processa esattamente questi due nodi e accoda 4 e 5. Senza quel limite, i nodi appena accodati finirebbero nel risultato dello stesso livello.

Maximum Path Sum usa un'altra combinazione postorder. Con radice `-10`, figlio sinistro `9` e ramo destro `20` con figli `15` e `7`, il nodo 20 riceve guadagni 15 e 7: il cammino che lo attraversa vale 42, mentre verso il genitore può restituire un solo ramo, `20+15=35`. Alla radice il cammino che passa da lì vale `-10+9+35=34`, quindi il massimo globale resta 42.

I guadagni negativi si sostituiscono con zero quando li si aggiunge a un cammino più grande. Il massimo globale va però inizializzato dal primo nodo, non da zero: con soli valori negativi la risposta è il nodo meno negativo, non il cammino vuoto.''',
        "recap": "Preorder, inorder, postorder e BFS differiscono per il momento in cui elaborano un nodo; il dato richiesto decide l'ordine.",
        "practice": [("exercise", "sde-e-tree-diameter"), ("exercise", "sde-e-max-path-sum")],
    },
    "sde-l-bst-paths": {
        "notes": r'''### I limiti arrivano dagli antenati

La radice 10 ha figlio destro 15 e il nodo 6 come figlio sinistro di 15. Ogni coppia padre-figlio sembra ordinata localmente, ma 6 viola il limite ereditato dalla radice: tutto il sottoalbero destro di 10 deve contenere valori maggiori di 10. Una visita porta quindi due limiti: per 15 il limite inferiore diventa 10; 6 non è strettamente maggiore di quel limite.

Con duplicati, il contratto deve stabilire dove possano stare; la validazione corrente richiede valori strettamente compresi e non ammette duplicati. Per LCA dei valori 4 e 7 in un BST con radice 5, uno va a sinistra e l'altro a destra: 5 è il primo punto in cui i percorsi si separano. Se entrambi fossero 4 e 7 a sinistra, si proseguirebbe a sinistra.

Entrambi gli algoritmi seguono al massimo un cammino di altezza h: O(h) tempo. La validazione visita ogni nodo, O(n), con O(h) stack. Un albero sbilanciato può avere h=n; non assumere automaticamente h=log n.''',
        "recap": "Usa la proprietà globale del BST passando limiti e non soltanto confrontando un nodo coi figli immediati.",
        "practice": [("exercise", "sde-e-validate-bst"), ("exercise", "sde-e-lca-bst")],
    },
    "sde-l-bfs-dfs-grid": {
        "notes": r'''### Lo stack di una DFS conta componenti

Nella griglia `1 1 0 / 0 1 0 / 1 0 1`, una DFS avviata da `(0,0)` aggiunge `(0,1)` allo stack; da lì scopre `(1,1)`. Quando lo stack si svuota, tutte e tre quelle celle appartengono alla prima isola. Le celle `(2,0)` e `(2,2)` avviano due visite indipendenti, quindi le isole sono tre. Marcale quando le aggiungi allo stack, non quando le estrai, così una cella non viene accodata dai due vicini.

Una cella marcata sul posto risparmia la matrice `visited`, ma cambia l'input. Se il chiamante deve conservarlo, tieni una struttura separata: nel caso peggiore occupa `O(R·C)` spazio, come la coda della BFS.''',
        "recap": "Tratta ogni cella accessibile come nodo, controlla i limiti prima di leggerla e marca la visita prima di accodare.",
        "practice": [("exercise", "sde-e-number-islands"), ("exercise", "sde-e-oranges-rotting")],
    },
    "sde-l-graphs": {
        "notes": r'''### Componenti, livelli e altri tipi di grafo

Con nodi `{0,1,2,3}` e archi non diretti `(0,1)` e `(1,2)`, una DFS da 0 visita `0,1,2`; il nodo 3 non è raggiunto e avvia una seconda visita. Ci sono quindi due componenti, incluso il nodo isolato. Per contarle, scorri ogni nodo e avvia DFS soltanto se non è ancora stato marcato.

In Word Ladder i nodi non vengono elencati come archi: sono parole e due parole sono collegate se differiscono per una lettera. Da `hit`, i livelli BFS possono essere `hot`, poi `dot` e `lot`, poi `dog` e `log`, infine `cog`. La visita per livelli trova il cammino minimo nel numero di trasformazioni; segnare parole usate evita cicli e ripetizioni.

Qui gli archi hanno costo unitario. Se hanno pesi positivi, BFS non confronta i costi: usa Dijkstra con priorità, spiegato nella lezione Heap. Per copiare un grafo conserva una mappa per identità del nodo, non per valore: due nodi con `val=5` possono essere distinti e avere vicini diversi.''',
        "recap": "Prima definisci nodi, direzione e peso degli archi; questi tre dettagli determinano rappresentazione e visita corretta.",
        "practice": [("exercise", "sde-e-connected-components"), ("exercise", "sde-e-word-ladder"), ("exercise", "sde-e-clone-graph")],
    },
    "sde-l-topological-sort": {
        "notes": r'''### La coda di Kahn passo per passo

Per `A→C`, `B→C`, `C→D`, i gradi entranti iniziali sono `A:0, B:0, C:2, D:1`; la coda parte con `[A,B]`. Togli A e il grado di C scende a 1. Togli B: C scende a 0 e viene accodato. Togli C: D scende a 0 e viene accodato. Togli D: sono stati emessi tutti e quattro i nodi, quindi il grafo è aciclico. Ogni nodo e arco viene elaborato una volta: O(V+E) tempo e spazio.

Se aggiungi `D→A`, nessuno dei nodi nel ciclo potrà raggiungere grado entrante zero; restano elementi non emessi. Kahn rileva così il ciclo anche se la coda si svuota senza un errore esplicito. L'ordine fra A e B può variare ed entrambe le sequenze sono valide: verifica le precedenze, a meno che il prompt richieda un ordine deterministico.''',
        "recap": "Un ordinamento topologico esiste solo se tutte le dipendenze possono essere rimosse; i nodi residui segnalano un ciclo.",
        "practice": [("exercise", "sde-e-course-schedule")],
    },
    "sde-l-heap": {
        "notes": r'''### Proprietà dell'heap e scelta top-k

In un min-heap l'elemento in cima è minore o uguale ai figli, ma due nodi fratelli non sono completamente ordinati. Per esempio l'array `[2,5,3,9]` è un heap valido: 2 precede 5 e 3, e 5 precede 9. Per inserire 1, aggiungilo in fondo e scambialo col genitore finché l'ordine è ripristinato; per estrarre il minimo, sposta in cima l'ultimo elemento e fallo scendere. Le operazioni costano O(log n), la lettura dell'estremo O(1).

Per i due più grandi valori di `[9,1,7,3,5]`, il min-heap limitato a k evolve: `[9]`, `[1,9]`, inserisci 7 ed elimina 1 (`[7,9]`); 3 non supera la cima 7, 5 non la supera. La cima è 7, il secondo più grande. Tempo O(n log k), spazio O(k); se serve l'ordine completo, sort può essere più semplice.

Per Dijkstra, il min-heap ordina distanze provvisorie, non nodi per numero di archi. Un costo 10 per A→C può essere sostituito da A→B→C di costo 1+2=3. Aggiorna C a 3 e ignora l'entrata obsoleta 10 quando verrà estratta. La prova richiede pesi non negativi. Il grafo pesato di Network Delay usa questa variante; la queue FIFO della BFS non basta.''',
        "recap": "Un heap conserva in cima un estremo, non ordina tutto; usalo quando devi ripetere estrazioni di priorità o mantenere pochi candidati.",
        "practice": [("exercise", "sde-e-kth-largest"), ("exercise", "sde-e-top-k-frequent"), ("exercise", "sde-e-network-delay")],
    },
    "sde-l-greedy": {
        "notes": r'''### Quando lo scheduling richiede DP

Se ogni intervallo ha un profitto, massimizzare il numero di intervalli non equivale a massimizzare il profitto. Due intervalli brevi compatibili possono valere 2 ciascuno mentre un intervallo lungo incompatibile vale 100: la regola del primo termine non risponde più alla domanda. Serve confrontare il profitto con la migliore soluzione prima dell'intervallo compatibile più vicino, una transizione da dynamic programming.

Anche i confini fanno parte dell'input: per `[start,end)` il contatto è compatibile con `start >= last_end`; se gli estremi sono inclusivi, serve una regola diversa. Cambiare una sola convenzione può modificare il numero di intervalli selezionati.''',
        "recap": "Una scelta greedy richiede una dimostrazione che le decisioni locali possano essere estese a una soluzione ottima.",
        "practice": [("exercise", "sde-e-interval-scheduling")],
    },
    "sde-l-backtracking": {
        "notes": r'''### Un albero di scelte con stato ripristinato

Per i valori `[1,2]`, ogni livello decide se includere il prossimo valore. Dal percorso vuoto `[]`, includi 1 e salva `[1]`; includi 2 e salva `[1,2]`; togli 2 tornando a `[1]`, poi togli 1 tornando a `[]`. Il ramo che salta 1 e include 2 salva `[2]`; quello che salta entrambi salva `[]`. Se aggiungi una scelta, dopo la chiamata ricorsiva esegui il passo inverso. Quando registri una risposta, copia `path`: salvare sempre lo stesso riferimento fa apparire tutte le risposte uguali all'ultimo stato.

Per n valori distinti ci sono `2^n` sottoinsiemi; materializzarli richiede già O(n·2^n) tempo e memoria di output. Le permutazioni sono n!, e una singola copia costa O(n). La potatura riduce i rami esplorati soltanto se il vincolo lo giustifica: con candidati positivi, un totale oltre il target non può tornare valido; con valori negativi quell'arresto può essere scorretto.

Per Combination Sum il valore scelto può riapparire, quindi la ricorsione riparte dallo stesso indice; per subsets si passa al successivo. Questa differenza evita rispettivamente di vietare un riuso permesso o di generare permutazioni duplicate.''',
        "recap": "Ogni ramo rappresenta una scelta, il caso base salva una risposta e il ripristino garantisce che i rami restino indipendenti.",
        "practice": [("exercise", "sde-e-subsets"), ("exercise", "sde-e-permutations"), ("exercise", "sde-e-combination-sum")],
    },
    "sde-l-dp-memoization": {
        "notes": r'''### Stesso schema, basi diverse

Climbing Stairs usa la stessa dipendenza dagli ultimi due stati, ma `ways(0)=1`: esiste un solo modo di restare al punto di partenza senza fare passi. Quindi `ways(1)=1`, `ways(2)=2`, `ways(3)=3`, `ways(4)=5`. Le basi fanno parte del significato del problema e non si copiano automaticamente da Fibonacci.

Coin Change cambia la transizione: per un importo `x` provi ciascuna moneta `c<=x` e confronti `1+dp[x-c]`. Il sentinel per uno stato irraggiungibile deve restare distinto da zero. Prima conta quanti stati esistono, poi quante transizioni prova ciascuno; così ricavi il tempo invece di ricordare una formula.''',
        "recap": "La DP evita di risolvere più volte lo stesso stato; definizione dello stato, base e transizione vengono prima dell'ottimizzazione dello spazio.",
        "practice": [("exercise", "sde-e-climbing-stairs"), ("exercise", "sde-e-house-robber")],
    },
}


LESSON_DIDACTIC.update({
    "sde-l-dp-models": {
        "notes": r'''### Tabelle piccole, stati espliciti

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

Il profitto migliore finale è 3. Il giorno successivo `hold` può partire solo dal `rest` del giorno precedente, che forza un giorno d'attesa dopo una vendita. Calcola il nuovo terzetto usando solo i valori del giorno prima: aggiornare `rest` prima di `hold` può far riusare accidentalmente una vendita appena avvenuta. Per tutte queste DP, il tempo deriva da numero di stati × lavoro di transizione; la memoria dipende da quanti stati precedenti servono davvero.''',
        "recap": "Uno stato descrive una sottodomanda precisa: cambiare il significato cambia base, transizione, risposta e casi impossibili.",
        "practice": [("exercise", "sde-e-house-robber"), ("exercise", "sde-e-coin-change"), ("exercise", "sde-e-unique-paths"), ("exercise", "sde-e-word-break"), ("exercise", "sde-e-edit-distance"), ("exercise", "sde-e-stock-cooldown")],
    },
    "sde-l-timed-dsa": {
        "notes": r'''### Provare il flusso prima del timer

Immagina di ricevere un array crescente di 100.000 elementi e una richiesta di primo indice con valore almeno `x`. La scansione lineare è facile da verificare a mano ma può leggere tutti i 100.000 elementi; il confine binario mantiene `[lo,hi)` e dimezza i candidati. Durante una prova, annotare questo invariante prima di digitare fa risparmiare tempo quando i bordi si avvicinano.

Il timer è un vincolo di lavoro, non un algoritmo. Una pianificazione possibile è: chiarire contratto e casi, scegliere l'approccio e stimarne il costo, implementare la parte centrale, poi spendere gli ultimi minuti su compilazione e casi che possono smentire la soluzione. Se l'ottimizzazione non è pronta, una brute force corretta con costo dichiarato conserva un risultato utile. Non promettere un test passato che non hai eseguito: separa ciò che hai ragionato da ciò che hai verificato.''',
        "recap": "Allena un ciclo completo: contratto, soluzione, costo e verifica; lascia traccia di ciò che è stato eseguito davvero.",
        "practice": [("simulation", "sde-sim-coding-40"), ("simulation", "sde-sim-coding-25")],
    },
    "sde-l-repo-orientation": {
        "notes": r'''### Seguire un requisito tra file

Supponi che `GET /orders/42` restituisca un ordine archiviato. Parti dal test che dichiara se gli ordini archiviati vadano nascosti; poi segui il simbolo della route al controller, al service e al repository. Un disegno possibile è `routes → controller → orderService → repository`; annota il tipo e il valore a ogni freccia. Se il test riceve l'ordine, controlla se il filtro manca nel service o se la route richiama un servizio diverso. Non leggere tutto il repository per intero: README, manifest, test e ricerca del simbolo riducono lo spazio.

Esegui prima il comando di test indicato dal progetto e conserva l'errore completo. Un README può essere incompleto o non aggiornato; confrontalo con `package.json`, CMake e comandi effettivi. Le cartelle `test`, `src`, `include` o `app` suggeriscono ruoli, ma i riferimenti fra file danno la prova del flusso.''',
        "recap": "La repository è una rete di contratti e chiamate: parti dal test e segui un simbolo fino alla produzione del valore.",
        "practice": [("lab", "lab-amazon-cpp-demo"), ("lab", "lab-amazon-node-demo")],
    },
    "sde-l-tests-stack-traces": {
        "notes": r'''### Dal valore inatteso al primo frame utile

Considera un test che chiama `findActive([A attivo, B pending], "B")` e si aspetta `None`, ma riceve B. L'assertion localizza il disaccordo; lo stack trace potrebbe mostrare `test_find_active` → `orderService.findActive` → `filter`. Parti dal primo frame del progetto e verifica il predicato: `status != "archived"` invece di `status == "active"` accetta anche `pending`. Il caso pending distingue le due ipotesi: non è archived, ma non è active.

Expected e actual descrivono l'osservazione, non ancora la causa. Una riga nel trace indica il punto in cui l'errore è emerso, che non sempre coincide con quello in cui è nato. Riproduci il test da solo, leggi il contratto e cambia una sola ipotesi per volta. Se la failure è intermittente, annota ordine, tempo e dipendenze prima di modificare la logica: un test flaky può indicare race o stato condiviso.''',
        "recap": "Il test mostra il contratto violato; lo stack trace collega la failure ai file. Verifica la causa, non correggere la sola riga segnalata.",
        "practice": [("lab", "lab-amazon-cpp-demo"), ("lab", "lab-amazon-node-demo")],
    },
    "sde-l-cpp-repository": {
        "notes": r'''### Dichiarazione, definizione e target

In una repository piccola, `Inventory.h` può dichiarare `bool visibleActive(const Item&)`; `Inventory.cpp` definisce la regola e `InventoryTest.cpp` verifica il risultato. Se il test compila ma il linker segnala `undefined reference to visibleActive`, la dichiarazione esiste ma la definizione può mancare dal target CMake o avere una firma diversa. Riscrivere l'header senza controllare `add_executable` e `target_sources` rischia di spostare il problema.

Un percorso diagnostico è: leggi il nome del target nel `CMakeLists.txt`; segui l'include usato dal test; confronta firma, namespace e const qualificatori fra header e source; poi esegui il test mirato. Una modifica alla firma pubblica tocca anche ogni chiamante e amplia il rischio. Per correggere una regola di filtro, mantieni API e dati invariati e cambia solo l'implementazione responsabile.

Le assertion provano osservazioni pubbliche. Non rendere pubblico un campo privato per poterlo testare se esiste già un metodo che espone il contratto.''',
        "recap": "Header, source, target e test devono concordare; localizza prima il livello del problema (compilazione, link o comportamento).",
        "practice": [("lab", "lab-amazon-cpp-demo"), ("lab", "lab-amazon-cpp-inventory")],
    },
    "sde-l-node-repository": {
        "notes": r'''### Dal comando al test

Se `package.json` contiene `"type": "module"` e `"test": "node --test"`, il progetto usa moduli ES e il comando della suite è `npm test`. Una route importa il controller, che chiama un service; un test unitario può importare direttamente il service e passargli dati finti. Se `findActive` restituisce un archivio, confronta prima la regola e poi il test che la mostra: non cambiare `import` in `require` per correggere un filtro.

Un `Promise` deve essere atteso dal test: `await findActive(...)` confronta il valore finale, mentre omettere `await` confronta l'oggetto Promise. Quando un test rimane appeso, guarda timer, server e handle aperti; non aggiungere timeout crescenti prima di sapere che cosa resta attivo.

Il runner locale dei laboratori usa Node integrato e non richiede dipendenze di rete. Nei progetti reali controlla però script e versioni effettivi; la stessa cartella può avere comandi diversi.''',
        "recap": "Segui gli script dichiarati e le convenzioni esistenti; un test diretto sul service isola la logica dal server HTTP.",
        "practice": [("lab", "lab-amazon-node-demo"), ("lab", "lab-amazon-node-async")],
    },
})


LESSON_DIDACTIC.update({
    "sde-l-async-contract": {
        "notes": r'''### Dalla richiesta HTTP alla risposta

Supponi che `GET /orders/42` passi `"42"` dal parametro di route al servizio. Il servizio restituisce una Promise: con `await`, il controller riceve l'ordine oppure `null`; senza attenderla, può provare a serializzare la Promise invece del dato. Il flusso completo è `parametro → ricerca asincrona → risultato → status e body`.

Per un ordine trovato il contratto potrebbe essere `200` con l'oggetto; per un ID assente, `404` con un corpo coerente. Un errore di connessione è un terzo caso: non equivale né a `null` né a una lista vuota. `undefined` spesso segnala un valore non fornito, `null` può indicare assenza esplicita, `[]` è una collezione presente senza elementi. Usa ciò che il progetto e i test definiscono, non uniformare tutto a 200.

Con `try/catch`, cattura l'errore nel livello che può tradurlo secondo il contratto; non nascondere ogni rifiuto restituendo un oggetto vuoto. Il test deve aspettare la route o il service e controllare valore, status e propagazione dell'errore.''',
        "recap": "Segui il valore e gli errori fino alla risposta: Promise, assenza e collezione vuota hanno significati differenti.",
        "practice": [("lab", "lab-amazon-node-async"), ("lab", "lab-amazon-node-contract")],
    },
    "sde-l-debugging-loop": {
        "notes": r'''### Un difetto seguito fino alla causa

Il test segnala che `GET /orders` include righe archiviate. Il controller inoltra correttamente la richiesta; il service riceve tutte le righe dal repository; il filtro confronta `row.status !== "deleted"`, quindi lascia passare anche `archived`. L'ipotesi più precisa è che il predicato non corrisponda al requisito “solo attive”. Un test con `active`, `archived` e `deleted` discrimina i casi; correggere il filtro nel service risolve anche gli altri chiamanti.

Un fallback nella route che nasconde l'archived farebbe passare solo quel percorso, lasciando il service errato. Per questo si modifica il livello più vicino alla causa, poi si esegue prima il test mirato e quindi la suite. Confronta il diff: se sono cambiati contratto, formattazione di molti file e filtro insieme, hai perso la possibilità di attribuire il risultato a una causa.

Registra fatto osservato, ipotesi, prova e risultato. Se la prova smentisce l'ipotesi, torna al flusso invece di aggiungere un altro ramo condizionale.''',
        "recap": "Riproduci, segui il dato, formula una causa falsificabile, correggi un punto e verifica la regressione.",
        "practice": [("lab", "lab-amazon-node-contract"), ("lab", "lab-amazon-cpp-inventory")],
    },
    "sde-l-ai-assistant": {
        "notes": r'''### Chiedere un aiuto che si possa controllare

Prima di usare un assistente, verifica se è abilitato e quali modalità mostra l'interfaccia: HackerRank descrive modalità Guarded e Unguarded, ma il test setter configura le funzioni disponibili. Per esempio, con un test che riceve una Promise invece di un array, una domanda circoscritta è: «Indica il percorso fra questa route e il service e spiega quale valore viene restituito in ciascun punto; non modificare file». La risposta propone una pista, non dimostra che la causa sia quella.

Controlla la pista leggendo i file e rilanciando il test. Se l'assistente suggerisce `await`, verifica se il chiamante e il service condividono davvero il contratto asincrono; applicare una modifica senza capirla può spostare l'errore. Le indicazioni HackerRank attuali dicono che le interazioni sono visibili al valutatore e che l'assistente non è presente in ogni prova; seguono comunque le istruzioni specifiche del test. Consulta la [guida ufficiale sull'AI Assistant in tests](https://candidatesupport.hackerrank.com/articles/7634558376-ai-assistant-in-tests) perché interfaccia e capacità possono cambiare.''',
        "recap": "Chiedi contesto o un piano verificabile, poi giudica la risposta con codice, contratto e test indipendenti.",
        "practice": [("lab", "lab-amazon-node-async"), ("lab", "lab-amazon-mock-repository")],
    },
    "sde-l-stack-choice": {
        "notes": r'''### Una scelta basata su evidenza comparabile

I due repository demo espongono gli stessi comportamenti, ma distribuiscono il codice in modo diverso. Nel C++ segui header, source, target CMake e test; nel Node leggi `package.json`, service, moduli e test. Per confrontarli in modo equo, usa lo stesso difetto e lo stesso set di test, poi annota minuti per localizzare il punto, numero di file letti, passaggi necessari a eseguire la suite e facilità di capire il fallimento.

Se in Node il flusso è più chiaro ma i rifiuti Promise sono difficili da seguire, aggiungi quello al confronto invece di decidere dalla sintassi. Se C++ richiede di correggere una firma condivisa, osserva l'effetto sui chiamanti. Una sola demo non rende uno stack universalmente migliore; indica che cosa ti è sembrato più leggibile e quali prove vuoi fare ancora.

La mini-prova confronta il lavoro sulle repository: la preferenza per un linguaggio negli esercizi algoritmici è una domanda diversa e va valutata con prove diverse.''',
        "recap": "Confronta repository equivalenti usando lo stesso comportamento e osservazioni concrete, non preferenze astratte.",
        "practice": [("lab", "lab-amazon-cpp-demo"), ("lab", "lab-amazon-node-demo")],
    },
    "sde-l-leadership-principles": {
        "notes": r'''### Un incidente, criteri che entrano in tensione

Una nuova versione fa aumentare gli errori per una parte delle richieste. `Customer Obsession` chiede di misurare chi è impattato; `Dive Deep` distingue correlazione e causa; `Bias for Action` può sostenere una mitigazione rapida e reversibile; `Earn Trust` richiede comunicare ciò che si sa e ciò che resta ipotesi. Un feature flag può ridurre l'impatto mentre si confrontano richieste riuscite e fallite; un rollback può essere migliore se la flag non è sicura o non esiste. Il contesto decide il compromesso.

Ownership non significa assumersi un'autorità che non si ha: significa seguire il problema, coinvolgere chi controlla il servizio e condividere responsabilità e prove. Insist on the Highest Standards chiede di verificare che la regressione non torni, non soltanto che una metrica migliori per pochi minuti.

La pagina Amazon attualmente elenca 16 principi: Customer Obsession, Ownership, Invent and Simplify, Are Right, A Lot, Learn and Be Curious, Hire and Develop the Best, Insist on the Highest Standards, Think Big, Bias for Action, Frugality, Earn Trust, Dive Deep, Have Backbone; Disagree and Commit, Deliver Results, Strive to be Earth's Best Employer e Success and Scale Bring Broad Responsibility. I nomi e le descrizioni vanno ricontrollati nella [fonte ufficiale](https://www.amazon.jobs/content/en/our-workplace/leadership-principles). I principi aiutano a esaminare una decisione: non forniscono una formula o una risposta ufficiale per ogni scenario.''',
        "recap": "Usa i principi come lenti per motivare effetti, prove, responsabilità e compromessi; evita di citarli come slogan.",
        "practice": [("scenario", "sde-ws-01"), ("scenario", "sde-ws-09")],
    },
    "sde-l-work-simulation": {
        "notes": r'''### Confrontare azioni plausibili

Scenario di esempio: dopo un rilascio, un webhook consegna alcuni eventi duplicati. Un rollback immediato può fermare i duplicati ma annullare anche una correzione indipendente; esaminare due payload identici può isolare la causa ma lascia aperto l'impatto; disattivare temporaneamente soltanto il consumer coinvolto può contenere il danno, ma richiede sapere come recuperare gli eventi sospesi. La scelta dipende da volume, reversibilità, dati persi e responsabilità disponibili.

Per ogni opzione chiediti: quale effetto immediato produce, quale informazione raccoglie, che rischio crea e chi deve essere coinvolto? Un'azione può essere utile dopo una mitigazione anche se non è la prima mossa. Esplicita le assunzioni che potrebbero cambiare l'ordine.

Le classifiche e i debrief di questo materiale sono giudizi formativi sulle conseguenze descritte, non chiavi ufficiali Amazon. Se una scelta diversa presuppone gravità o vincoli differenti, nomina quel dato invece di cercare una lettera da memorizzare.''',
        "recap": "Valuta prima l'impatto che continua, poi reversibilità, qualità delle prove e coordinamento; il contesto può cambiare l'ordine delle azioni.",
        "practice": [("scenario", "sde-ws-01"), ("scenario", "sde-ws-09")],
    },
    "sde-l-work-style": {
        "notes": r'''### Leggere le sfumature senza costruire un personaggio

Confronta le frasi «concludo sempre dopo aver raccolto ogni dato» e «a volte agisco con informazioni incomplete». L'avverbio “sempre” rende la prima assoluta; la seconda ammette contesti diversi. Prima di rispondere, pensa a un episodio reale: quali dati avevi, quanto costava aspettare e quale rischio hai accettato? L'obiettivo della familiarizzazione è leggere con attenzione e rispondere in modo autentico, non trovare la combinazione che sembra più desiderabile.

Se due affermazioni sembrano in tensione, non presumere che descrivano lo stesso momento o rischio: rileggi il testo e considera il comportamento abituale. Una risposta personale può essere coerente e riconoscere eccezioni; non serve inventare una biografia o un profilo ideale.

Gli esercizi di riflessione aiutano a notare le sfumature. Il formato e le istruzioni di una prova reale possono differire; questa attività non deduce come venga valutato un questionario né insegna a manipolarlo.''',
        "recap": "La familiarizzazione riduce fretta e letture superficiali; le risposte descrivono esperienze e comportamenti reali, non un profilo da imitare.",
        "practice": [("work_style", "sde-style-01"), ("work_style", "sde-style-08")],
    },
    "sde-l-full-mock": {
        "notes": r'''### Separare l'esecuzione dalla revisione

Durante la prova annota le evidenze, non soltanto le attività: «ho eseguito test A e B» è diverso da «ho creduto che tutti i casi fossero coperti». Nel debrief puoi usare una tabella semplice: osservazione, ipotesi, verifica, esito, prossimo passo. Esempio: “il test del not-found fallisce; ipotesi: il service confonde null con lista vuota; prova: aggiungo un record assente e uno con lista vuota; esito: solo il primo deve generare 404”. Questo separa una diagnosi verificata da un'impressione.

Il formato 40+60 appartiene a questa simulazione. Il processo effettivo dipende dall'invito e dal ruolo; i risultati del mock misurano pratica svolta, non predicono l'esito di un assessment reale.''',
        "recap": "Esegui ogni fase con il proprio tempo e poi valuta le prove raccolte, distinguendo completamento, ipotesi e verifiche.",
        "practice": [("simulation", "sde-full-mock"), ("simulation", "sde-sim-repository-60")],
    },
})


def code_exercise(
    exercise_id, lesson_id, title, difficulty, minutes, pattern, prompt,
    py_starter, py_solution, py_tests,
    cpp_starter, cpp_solution, cpp_tests,
    hints, explanation, *, no_ai=True, timed=True,
):
    return {
        "id": f"sde-e-{exercise_id}", "lesson_id": f"sde-l-{lesson_id}",
        "title": title, "kind": "python", "difficulty": difficulty,
        "minutes": minutes, "xp": {"easy": 20, "medium": 35, "hard": 50}[difficulty],
        "prompt": f"**Pattern:** {pattern}.\n\n{prompt}",
        "starter": py_starter, "solution": py_solution, "tests": py_tests,
        "hints": hints, "explanation": explanation,
        "no_ai": no_ai, "no_internet": no_ai, "timed": timed,
        "solution_after_attempts": 2,
        "variants": {
            "python": {"kind": "python", "starter": py_starter, "solution": py_solution, "tests": py_tests},
            "cpp": {"kind": "cpp", "starter": cpp_starter, "solution": cpp_solution, "tests": cpp_tests},
        },
    }


EXERCISES = [
    code_exercise(
        "language-trial", "language-choice", "Mini-prova: finestra con somma massima", "easy", 8, "linguaggio e sliding window",
        "Ricevi interi non negativi e una dimensione `k`. Restituisci la somma massima di una finestra contigua lunga `k`. Se `k` non è valido, restituisci `None`. In Python e C++ usa gli stessi casi; cronometra 8 minuti per linguaggio.",
        "def max_window_sum(nums: list[int], k: int) -> int | None:\n    pass\n",
        "def max_window_sum(nums: list[int], k: int) -> int | None:\n    if k <= 0 or k > len(nums):\n        return None\n    current = sum(nums[:k])\n    best = current\n    for right in range(k, len(nums)):\n        current += nums[right] - nums[right - k]\n        best = max(best, current)\n    return best\n",
        [{"name":"finestra centrale","expression":"max_window_sum([2, 1, 5, 1, 3, 2], 3)","expected":9}, {"name":"lista più corta di k","expression":"max_window_sum([4], 2)","expected":None}],
        "#include <algorithm>\n#include <optional>\n#include <vector>\nusing namespace std;\noptional<int> max_window_sum(const vector<int>& nums, int k) { return nullopt; }\n",
        "#include <algorithm>\n#include <optional>\n#include <vector>\nusing namespace std;\noptional<int> max_window_sum(const vector<int>& nums, int k) {\n    if (k <= 0 || k > static_cast<int>(nums.size())) return nullopt;\n    int current = 0;\n    for (int i = 0; i < k; ++i) current += nums[i];\n    int best = current;\n    for (int right = k; right < static_cast<int>(nums.size()); ++right) {\n        current += nums[right] - nums[right-k];\n        best = max(best, current);\n    }\n    return best;\n}\n",
        [{"name":"finestra centrale","assertion":"max_window_sum({2,1,5,1,3,2},3) == 9"}, {"name":"lista più corta di k","assertion":"!max_window_sum({4},2).has_value()"}],
        ["La prima finestra richiede un solo accumulo; le successive riusano il totale precedente.", "Quando il bordo destro avanza, quale elemento esce dalla finestra?", "Perché un input con `k > n` non ha una finestra valida?"],
        "La somma della finestra si aggiorna in O(1): aggiungi il nuovo estremo e sottrai quello appena lasciato. Tempo O(n), spazio O(1). La mini-prova confronta sintassi e debugging, non valuta una preferenza astratta.", no_ai=False, timed=False,
    ),
    code_exercise(
        "two-sum", "hashmap-set", "Due valori che completano il target", "easy", 20, "HashMap e complemento",
        "Restituisci gli indici di due elementi distinti la cui somma è `target`, oppure `None` se non esistono. Puoi assumere al massimo una risposta. Non riusare lo stesso indice. Vincoli: al massimo 100.000 valori, ciascuno compreso tra -1.000.000 e 1.000.000.",
        "def two_sum(nums: list[int], target: int) -> list[int] | None:\n    pass\n",
        "def two_sum(nums: list[int], target: int) -> list[int] | None:\n    seen = {}\n    for index, value in enumerate(nums):\n        needed = target - value\n        if needed in seen:\n            return [seen[needed], index]\n        seen[value] = index\n    return None\n",
        [{"name":"complemento precedente","expression":"two_sum([4, 1, 8, 3], 7)","expected":[0,3]}, {"name":"nessuna coppia","expression":"two_sum([1, 2, 4], 20)","expected":None}, {"name":"duplicato valido","expression":"two_sum([5, 5], 10)","expected":[0,1]}, {"name":"scansione grande","expression":"two_sum(list(range(80000)), -1)","expected":None}],
        "#include <numeric>\n#include <unordered_map>\n#include <vector>\nusing namespace std;\nvector<int> two_sum(const vector<int>& nums, int target) { return {}; }\n",
        "#include <numeric>\n#include <unordered_map>\n#include <vector>\nusing namespace std;\nvector<int> two_sum(const vector<int>& nums, int target) {\n    unordered_map<int,int> seen;\n    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {\n        int needed = target - nums[i];\n        auto found = seen.find(needed);\n        if (found != seen.end()) return {found->second, i};\n        seen[nums[i]] = i;\n    }\n    return {};\n}\n",
        [{"name":"complemento precedente","assertion":"two_sum({4,1,8,3},7) == vector<int>({0,3})"}, {"name":"nessuna coppia","assertion":"two_sum({1,2,4},20).empty()"}, {"name":"duplicato valido","assertion":"two_sum({5,5},10) == vector<int>({0,1})"}, {"name":"scansione grande","assertion":"[](){ vector<int> v(80000); iota(v.begin(),v.end(),0); return two_sum(v,-1).empty(); }()"}],
        ["Per il valore corrente, quale numero renderebbe vera la somma?", "Cerca prima tra gli elementi già letti; salva il corrente soltanto dopo il lookup.", "Se memorizzi il valore come chiave, che cosa devi conservare per restituire gli indici?"],
        "La mappa trasforma i confronti ripetuti in lookup medi O(1), portando il tempo da O(n²) a O(n) con O(n) spazio. Il test grande senza risposta smaschera il doppio ciclo; controlla l'ordine tra ricerca e inserimento per non usare due volte lo stesso elemento.",
    ),
    code_exercise(
        "contains-duplicate", "hashmap-set", "Rilevare un duplicato senza ordinare", "easy", 20, "Set e membership",
        "Restituisci `True` se almeno un valore compare due volte. L'ordine non conta e la lista può essere vuota.",
        "def contains_duplicate(nums: list[int]) -> bool:\n    pass\n",
        "def contains_duplicate(nums: list[int]) -> bool:\n    seen = set()\n    for value in nums:\n        if value in seen:\n            return True\n        seen.add(value)\n    return False\n",
        [{"name":"duplicato separato","expression":"contains_duplicate([7, 2, 9, 7])","expected":True}, {"name":"valori distinti","expression":"contains_duplicate([1, 2, 3])","expected":False}, {"name":"lista vuota","expression":"contains_duplicate([])","expected":False}, {"name":"dataset grande","expression":"contains_duplicate(list(range(60000)) + [0])","expected":True}],
        "#include <numeric>\n#include <unordered_set>\n#include <vector>\nusing namespace std;\nbool contains_duplicate(const vector<int>& nums) { return false; }\n",
        "#include <numeric>\n#include <unordered_set>\n#include <vector>\nusing namespace std;\nbool contains_duplicate(const vector<int>& nums) {\n    unordered_set<int> seen;\n    for (int value : nums) if (!seen.insert(value).second) return true;\n    return false;\n}\n",
        [{"name":"duplicato separato","assertion":"contains_duplicate({7,2,9,7})"}, {"name":"valori distinti","assertion":"!contains_duplicate({1,2,3})"}, {"name":"lista vuota","assertion":"!contains_duplicate({})"}, {"name":"dataset grande","assertion":"[](){ vector<int> v(60000); iota(v.begin(),v.end(),0); v.push_back(0); return contains_duplicate(v); }()"}],
        ["Ti serve sapere quante volte compare il valore, oppure soltanto se è già apparso?", "Aggiungi il valore al set solo dopo avere controllato la membership.", "Il caso vuoto ha un duplicato?"],
        "Il set mantiene soltanto ciò che serve e termina appena trova una ripetizione. Tempo medio O(n), spazio O(n). Ordinare e confrontare i vicini sarebbe O(n log n), corretto ma più lavoro quando non serve l'ordine.",
    ),
    code_exercise(
        "valid-anagram", "hashmap-set", "Confrontare due frequenze di caratteri", "easy", 20, "mappa delle frequenze",
        "Restituisci `True` se `second` contiene gli stessi caratteri con le stesse frequenze di `first`. I caratteri sono lettere ASCII minuscole.",
        "def is_anagram(first: str, second: str) -> bool:\n    pass\n",
        "def is_anagram(first: str, second: str) -> bool:\n    if len(first) != len(second):\n        return False\n    counts = [0] * 26\n    for left, right in zip(first, second):\n        counts[ord(left) - ord('a')] += 1\n        counts[ord(right) - ord('a')] -= 1\n    return all(count == 0 for count in counts)\n",
        [{"name":"stesse lettere riordinate","expression":"is_anagram('listen', 'silent')","expected":True}, {"name":"frequenze diverse","expression":"is_anagram('aab', 'abb')","expected":False}, {"name":"stringhe vuote","expression":"is_anagram('', '')","expected":True}],
        "#include <string>\nusing namespace std;\nbool is_anagram(const string& first, const string& second) { return false; }\n",
        "#include <array>\n#include <string>\nusing namespace std;\nbool is_anagram(const string& first, const string& second) {\n    if (first.size() != second.size()) return false;\n    array<int,26> counts{};\n    for (size_t i=0; i<first.size(); ++i) { ++counts[first[i]-'a']; --counts[second[i]-'a']; }\n    for (int count : counts) if (count != 0) return false;\n    return true;\n}\n",
        [{"name":"stesse lettere riordinate","assertion":"is_anagram(\"listen\",\"silent\")"}, {"name":"frequenze diverse","assertion":"!is_anagram(\"aab\",\"abb\")"}, {"name":"stringhe vuote","assertion":"is_anagram(\"\",\"\")"}],
        ["La lunghezza è già una condizione necessaria: controllala prima di contare.", "Un conteggio cresce per la prima parola e cala per la seconda.", "Perché `aab` e `abb` non sono equivalenti anche se condividono gli stessi caratteri distinti?"],
        "Il vettore fisso contiene 26 contatori, quindi il tempo è O(n) e lo spazio O(1). Il controllo della lunghezza evita lavoro inutile; i conteggi distinguono correttamente le ripetizioni.",
    ),
    code_exercise(
        "stock-profit", "arrays-strings", "Miglior guadagno da un acquisto e una vendita", "easy", 20, "scansione con minimo prefisso",
        "I prezzi sono osservati in ordine. Scegli un giorno di acquisto e uno successivo di vendita; restituisci il guadagno massimo oppure zero se nessuna vendita conviene.",
        "def max_profit(prices: list[int]) -> int:\n    pass\n",
        "def max_profit(prices: list[int]) -> int:\n    lowest = float('inf')\n    best = 0\n    for price in prices:\n        lowest = min(lowest, price)\n        best = max(best, price - lowest)\n    return best\n",
        [{"name":"guadagno dopo un minimo","expression":"max_profit([8, 2, 6, 1, 7])","expected":6}, {"name":"solo discesa","expression":"max_profit([9, 7, 4, 2])","expected":0}, {"name":"un solo prezzo","expression":"max_profit([5])","expected":0}],
        "#include <algorithm>\n#include <vector>\nusing namespace std;\nint max_profit(const vector<int>& prices) { return 0; }\n",
        "#include <algorithm>\n#include <climits>\n#include <vector>\nusing namespace std;\nint max_profit(const vector<int>& prices) {\n    int lowest = INT_MAX, best = 0;\n    for (int price : prices) { lowest = min(lowest, price); best = max(best, price-lowest); }\n    return best;\n}\n",
        [{"name":"guadagno dopo un minimo","assertion":"max_profit({8,2,6,1,7}) == 6"}, {"name":"solo discesa","assertion":"max_profit({9,7,4,2}) == 0"}, {"name":"un solo prezzo","assertion":"max_profit({5}) == 0"}],
        ["La vendita deve avvenire dopo l'acquisto: tieni il minimo già incontrato.", "Aggiorna il guadagno massimo confrontando il prezzo corrente con quel minimo.", "Una discesa non richiede un guadagno negativo se il prompt ammette di non operare."],
        "Ogni prezzo viene letto una volta. Il minimo del prefisso riassume tutte le possibili date di acquisto precedenti, quindi il tempo è O(n) e lo spazio O(1).",
    ),
    code_exercise(
        "valid-palindrome", "two-pointers", "Palindromo ignorando spazi e punteggiatura", "easy", 20, "two pointers",
        "Confronta da estremi opposti ignorando caratteri non alfanumerici e senza distinguere maiuscole e minuscole. L'input contiene ASCII.",
        "def is_palindrome(text: str) -> bool:\n    pass\n",
        "def is_palindrome(text: str) -> bool:\n    left, right = 0, len(text) - 1\n    while left < right:\n        while left < right and not text[left].isalnum():\n            left += 1\n        while left < right and not text[right].isalnum():\n            right -= 1\n        if text[left].lower() != text[right].lower():\n            return False\n        left += 1\n        right -= 1\n    return True\n",
        [{"name":"punteggiatura ignorata","expression":"is_palindrome('A man, a plan, a canal: Panama!')","expected":True}, {"name":"lettere diverse","expression":"is_palindrome('race a car')","expected":False}, {"name":"nessun carattere utile","expression":"is_palindrome('., !')","expected":True}],
        "#include <string>\nusing namespace std;\nbool is_palindrome(const string& text) { return false; }\n",
        "#include <cctype>\n#include <string>\nusing namespace std;\nbool is_palindrome(const string& text) {\n    int left=0, right=static_cast<int>(text.size())-1;\n    while (left < right) {\n        while (left < right && !isalnum(static_cast<unsigned char>(text[left]))) ++left;\n        while (left < right && !isalnum(static_cast<unsigned char>(text[right]))) --right;\n        if (tolower(static_cast<unsigned char>(text[left])) != tolower(static_cast<unsigned char>(text[right]))) return false;\n        ++left; --right;\n    }\n    return true;\n}\n",
        [{"name":"punteggiatura ignorata","assertion":"is_palindrome(\"A man, a plan, a canal: Panama!\")"}, {"name":"lettere diverse","assertion":"!is_palindrome(\"race a car\")"}, {"name":"nessun carattere utile","assertion":"is_palindrome(\"., !\")"}],
        ["Entrambi i puntatori saltano i caratteri che non fanno parte del confronto.", "Normalizza le lettere solo al momento del confronto.", "Controlla il caso in cui, saltando punteggiatura, i bordi si incontrino."],
        "I due bordi avanzano verso il centro, quindi il tempo è O(n) e lo spazio ausiliario O(1). Una stringa senza caratteri confrontabili è palindroma per la definizione adottata.",
    ),

]


def _py_starter(solution):
    signature = next((line for line in solution.splitlines() if line.startswith("def ")), "")
    return signature + "\n    pass\n" if signature else "# Implement the function described in the prompt.\n"


def _cpp_starter(solution):
    prefix = []
    for line in solution.splitlines():
        if line.startswith(("#include", "using namespace", "struct ", "class ")) or not line.strip():
            prefix.append(line)
        elif "(" in line and "{" in line:
            prefix.append(line[:line.index("{")].rstrip() + " {\n    // TODO\n}")
            break
        else:
            prefix.append(line)
    return "\n".join(prefix) + "\n"


def add_task(slug, lesson_id, title, difficulty, minutes, pattern, prompt, py, cpp, py_tests, cpp_tests, hints, explanation):
    py_starter = _py_starter(py)
    cpp_starter = _cpp_starter(cpp)
    if slug == "reverse-list":
        py_starter = "class ListNode:\n def __init__(self,val=0,next=None):self.val,self.next=val,next\ndef reverse_list(head):\n    pass\n"
        cpp_starter = "#include <vector>\nusing namespace std;\nstruct ListNode{int val;ListNode*next;};\nListNode* reverse_list(ListNode* head) {\n    // TODO\n    return nullptr;\n}\n"
    elif slug == "max-depth":
        py_starter = "class TreeNode:\n def __init__(self,val=0,left=None,right=None):self.val,self.left,self.right=val,left,right\ndef max_depth(root):\n    pass\n"
        cpp_starter = "#include <algorithm>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nint max_depth(TreeNode* root) {\n    // TODO\n    return 0;\n}\n"
    elif slug == "lru-cache":
        py_starter = "class LRUCache:\n def __init__(self,capacity):\n  pass\n def get(self,key):\n  return -1\n def put(self,key,value):\n  pass\ndef lru_cache(capacity,operations):\n cache=LRUCache(capacity)\n result=[]\n for op in operations:\n  if op[0]==0:cache.put(op[1],op[2])\n  else:result.append(cache.get(op[1]))\n return result\n"
        cpp_starter = "#include <vector>\nusing namespace std;\nclass LRUCache {\npublic:\n    explicit LRUCache(int capacity) {}\n    int get(int key) { return -1; }\n    void put(int key, int value) {}\n};\nvector<int> lru_cache(int capacity, const vector<vector<int>>& operations) { return {}; }\n"
    elif slug == "tree-diameter":
        cpp_starter = "#include <algorithm>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nint diameter(TreeNode* root) {\n    // TODO\n    return 0;\n}\n"
    elif slug == "max-path-sum":
        cpp_starter = "#include <algorithm>\n#include <climits>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nint max_path_sum(TreeNode* root) {\n    // TODO\n    return 0;\n}\n"
    exercise = code_exercise(
        slug, lesson_id, title, difficulty, minutes, pattern, prompt,
        py_starter, py, py_tests, cpp_starter, cpp, cpp_tests, hints, explanation,
    )
    if any(item["id"] == exercise["id"] for item in EXERCISES):
        raise ValueError(f"Definizione esercizio duplicata nel generator: {exercise['id']}")
    EXERCISES.append(exercise)


add_task("two-sum-sorted", "two-pointers", "Coppia con somma in una lista ordinata", "easy", 20, "two pointers",
         "La lista è crescente. Restituisci gli indici 1-based di una coppia distinta che somma `target`, oppure una lista vuota.",
         "def two_sum_sorted(a,t):\n l,r=0,len(a)-1\n while l<r:\n  s=a[l]+a[r]\n  if s==t:return [l+1,r+1]\n  if s<t:l+=1\n  else:r-=1\n return []\n",
         "#include <vector>\nusing namespace std;\nvector<int> two_sum_sorted(const vector<int>& a,int t){int l=0,r=(int)a.size()-1;while(l<r){int s=a[l]+a[r];if(s==t)return {l+1,r+1};if(s<t)++l;else --r;}return {};}\n",
         [{"name":"coppia","expression":"two_sum_sorted([1,2,4,8,11],12)","expected":[1,5]},{"name":"assente","expression":"two_sum_sorted([2,3,7],20)","expected":[]}],
         [{"name":"coppia","assertion":"two_sum_sorted({1,2,4,8,11},12)==vector<int>({1,5})"},{"name":"assente","assertion":"two_sum_sorted({2,3,7},20).empty()"}],
         ["La lista ordinata permette di scartare un lato a ogni confronto.","Converti a 1-based solo quando costruisci il risultato."],
         "I due indici si muovono in una sola direzione: O(n) tempo e O(1) spazio.")

add_task("move-zeroes", "arrays-strings", "Compattare i valori non nulli", "easy", 20, "scrittura in-place",
         "Modifica la lista mettendo gli zeri alla fine senza cambiare l'ordine relativo dei valori non nulli; restituisci la lista.",
         "def move_zeroes(a):\n w=0\n for x in a:\n  if x!=0:a[w]=x;w+=1\n a[w:]=[0]*(len(a)-w)\n return a\n",
         "#include <vector>\nusing namespace std;\nvector<int> move_zeroes(vector<int> a){int w=0;for(int x:a)if(x!=0)a[w++]=x;while(w<(int)a.size())a[w++]=0;return a;}\n",
         [{"name":"ordine stabile","expression":"move_zeroes([0,3,0,1,8])","expected":[3,1,8,0,0]},{"name":"zeri","expression":"move_zeroes([0,0])","expected":[0,0]}],
         [{"name":"ordine stabile","assertion":"move_zeroes({0,3,0,1,8})==vector<int>({3,1,8,0,0})"},{"name":"zeri","assertion":"move_zeroes({0,0})==vector<int>({0,0})"}],
         ["L'indice di scrittura delimita il prefisso già compatto.","Quanti elementi restano dopo l'ultimo valore non nullo?"],
         "Una scansione più una coda di zeri: O(n) tempo e O(1) spazio aggiuntivo.")

add_task("max-subarray", "arrays-strings", "Massima somma di un segmento contiguo", "easy", 25, "Kadane",
        "Restituisci la somma massima di un segmento contiguo non vuoto. La lista può contenere solo valori negativi. Vincoli: 1 ≤ len(a) ≤ 100.000 e -10.000 ≤ a[i] ≤ 10.000.",
         "def max_subarray(a):\n cur=best=a[0]\n for x in a[1:]:\n  cur=max(x,cur+x);best=max(best,cur)\n return best\n",
         "#include <algorithm>\n#include <vector>\nusing namespace std;\nint max_subarray(const vector<int>& a){int c=a[0],b=a[0];for(int i=1;i<(int)a.size();++i){c=max(a[i],c+a[i]);b=max(b,c);}return b;}\n",
         [{"name":"segmento massimo","expression":"max_subarray([-2,1,-3,4,-1,2,1,-5,4])","expected":6},{"name":"tutti negativi","expression":"max_subarray([-7,-2,-5])","expected":-2}],
         [{"name":"segmento massimo","assertion":"max_subarray({-2,1,-3,4,-1,2,1,-5,4})==6"},{"name":"tutti negativi","assertion":"max_subarray({-7,-2,-5})==-2"}],
         ["A ogni elemento valuta se iniziare un segmento nuovo o estendere il precedente.","Il segmento deve essere non vuoto: parti dal primo valore."],
         "La somma migliore che termina in i riassume tutti i segmenti precedenti. O(n) tempo, O(1) spazio.")

add_task("valid-parentheses", "stack-queue", "Parentheses con tipi e ordine corretti", "easy", 20, "stack",
         "Restituisci True se `()[]{}` sono chiuse con tipo e ordine corretti. La stringa contiene solo parentesi.",
         "def valid_parentheses(s):\n pairs={')':'(',']':'[','}':'{'}; st=[]\n for c in s:\n  if c in pairs.values():st.append(c)\n  elif not st or st.pop()!=pairs[c]:return False\n return not st\n",
         "#include <stack>\n#include <string>\nusing namespace std;\nbool valid_parentheses(const string& s){stack<char> q;for(char c:s){if(c=='('||c=='['||c=='{')q.push(c);else{if(q.empty())return false;char o=q.top();q.pop();if((c==')'&&o!='(')||(c==']'&&o!='[')||(c=='}'&&o!='{'))return false;}}return q.empty();}\n",
         [{"name":"annidate","expression":"valid_parentheses('({[]})')","expected":True},{"name":"incrociate","expression":"valid_parentheses('([)]')","expected":False},{"name":"apertura rimasta","expression":"valid_parentheses('((')","expected":False}],
         [{"name":"annidate","assertion":"valid_parentheses(\"({[]})\")"},{"name":"incrociate","assertion":"!valid_parentheses(\"([)]\")"},{"name":"apertura rimasta","assertion":"!valid_parentheses(\"((\")"}],
         ["L'ultima parentesi aperta è la prima che deve chiudersi.","Rifiuta una chiusura quando lo stack è vuoto o il tipo non coincide."],
         "Lo stack memorizza le aperture in attesa. O(n) tempo e O(n) spazio nel caso annidato.")

add_task("binary-search", "binary-search", "Cercare un valore ordinato", "easy", 20, "binary search",
         "Restituisci l'indice 0-based di `target` in una lista crescente di valori distinti, oppure -1.",
         "def binary_search(a,t):\n l,r=0,len(a)-1\n while l<=r:\n  m=l+(r-l)//2\n  if a[m]==t:return m\n  if a[m]<t:l=m+1\n  else:r=m-1\n return -1\n",
         "#include <vector>\nusing namespace std;\nint binary_search(const vector<int>& a,int t){int l=0,r=(int)a.size()-1;while(l<=r){int m=l+(r-l)/2;if(a[m]==t)return m;if(a[m]<t)l=m+1;else r=m-1;}return -1;}\n",
         [{"name":"valore","expression":"binary_search([-4,0,3,9,12],3)","expected":2},{"name":"assente","expression":"binary_search([1,4,7],5)","expected":-1},{"name":"vuota","expression":"binary_search([],1)","expected":-1}],
         [{"name":"valore","assertion":"binary_search({-4,0,3,9,12},3)==2"},{"name":"assente","assertion":"binary_search({1,4,7},5)==-1"},{"name":"vuota","assertion":"binary_search({},1)==-1"}],
         ["Scegli se i due limiti sono inclusivi o semiaperti e non cambiare convenzione a metà.","Calcola il centro come l+(r-l)//2."],
         "Ogni confronto dimezza il tratto rimasto: O(log n) tempo e O(1) spazio.")

add_task("first-true", "binary-boundaries", "Primo indice che supera una soglia", "easy", 25, "ricerca di confine",
         "La lista contiene False seguiti da True. Restituisci il primo indice True, oppure n quando non esiste.",
         "def first_true(a):\n l,r=0,len(a)\n while l<r:\n  m=(l+r)//2\n  if a[m]:r=m\n  else:l=m+1\n return l\n",
         "#include <vector>\nusing namespace std;\nint first_true(const vector<bool>& a){int l=0,r=a.size();while(l<r){int m=l+(r-l)/2;if(a[m])r=m;else l=m+1;}return l;}\n",
         [{"name":"transizione","expression":"first_true([False,False,True,True])","expected":2},{"name":"mai vero","expression":"first_true([False,False])","expected":2},{"name":"subito vero","expression":"first_true([True])","expected":0}],
         [{"name":"transizione","assertion":"first_true({false,false,true,true})==2"},{"name":"mai vero","assertion":"first_true({false,false})==2"},{"name":"subito vero","assertion":"first_true({true})==0"}],
         ["Rappresenta il candidato in un intervallo semiaperto che può terminare a n.","Se il predicato è vero, mid può ancora essere il primo: conserva mid."],
         "Trova una transizione monotona in O(log n); n rappresenta correttamente l'assenza di True.")

add_task("is-subsequence", "two-pointers", "Verificare una sottosequenza", "easy", 20, "scansione monotona",
         "Restituisci True se tutti i caratteri di `small` appaiono in `large` nello stesso ordine, non necessariamente adiacenti.",
         "def is_subsequence(s,t):\n i=0\n for c in t:\n  if i<len(s) and s[i]==c:i+=1\n return i==len(s)\n",
         "#include <string>\nusing namespace std;\nbool is_subsequence(const string& s,const string& t){int i=0;for(char c:t)if(i<(int)s.size()&&s[i]==c)++i;return i==(int)s.size();}\n",
         [{"name":"ordine conservato","expression":"is_subsequence('ace','abcde')","expected":True},{"name":"ordine non presente","expression":"is_subsequence('aec','abcde')","expected":False},{"name":"stringa vuota","expression":"is_subsequence('','abc')","expected":True}],
         [{"name":"ordine conservato","assertion":"is_subsequence(\"ace\",\"abcde\")"},{"name":"ordine non presente","assertion":"!is_subsequence(\"aec\",\"abcde\")"},{"name":"stringa vuota","assertion":"is_subsequence(\"\",\"abc\")"}],
         ["Avanza l'indice del pattern soltanto quando il carattere corrisponde.","Una sottosequenza vuota è contenuta in ogni stringa."],
         "Un solo passaggio sulla stringa più lunga: O(n) tempo e O(1) spazio.")

add_task("remove-duplicates", "two-pointers", "Rimuovere duplicati da una lista ordinata", "easy", 20, "fast/slow pointers",
         "Modifica la lista crescente lasciando una sola copia di ogni valore e restituisci il prefisso senza duplicati.",
         "def remove_duplicates(a):\n if not a:return []\n w=1\n for r in range(1,len(a)):\n  if a[r]!=a[w-1]:a[w]=a[r];w+=1\n return a[:w]\n",
         "#include <vector>\nusing namespace std;\nvector<int> remove_duplicates(vector<int> a){if(a.empty())return {};int w=1;for(int r=1;r<(int)a.size();++r)if(a[r]!=a[w-1])a[w++]=a[r];a.resize(w);return a;}\n",
         [{"name":"duplicati raggruppati","expression":"remove_duplicates([1,1,2,2,2,5])","expected":[1,2,5]},{"name":"vuota","expression":"remove_duplicates([])","expected":[]}],
         [{"name":"duplicati raggruppati","assertion":"remove_duplicates({1,1,2,2,2,5})==vector<int>({1,2,5})"},{"name":"vuota","assertion":"remove_duplicates({}).empty()"}],
         ["La zona prima di write contiene già valori unici.","Confronta il nuovo valore con l'ultimo già scritto."],
         "Due indici attraversano l'array una volta, O(n) tempo e O(1) spazio extra. Il risultato mostrato è il prefisso compatto.")

add_task("pivot-index", "prefix-sum", "Indice con somme uguali a sinistra e destra", "easy", 20, "prefisso e totale",
         "Restituisci il primo indice il cui lato sinistro e destro hanno la stessa somma; restituisci -1 se manca.",
         "def pivot_index(a):\n total=sum(a);left=0\n for i,x in enumerate(a):\n  if left==total-left-x:return i\n  left+=x\n return -1\n",
         "#include <numeric>\n#include <vector>\nusing namespace std;\nint pivot_index(const vector<int>& a){int total=accumulate(a.begin(),a.end(),0),left=0;for(int i=0;i<(int)a.size();++i){if(left==total-left-a[i])return i;left+=a[i];}return -1;}\n",
         [{"name":"primo pivot","expression":"pivot_index([1,7,3,6,5,6])","expected":3},{"name":"nessun pivot","expression":"pivot_index([1,2,3])","expected":-1}],
         [{"name":"primo pivot","assertion":"pivot_index({1,7,3,6,5,6})==3"},{"name":"nessun pivot","assertion":"pivot_index({1,2,3})==-1"}],
         ["Calcola il totale una volta; la somma destra è totale meno sinistra e valore corrente.","Controlla l'equilibrio prima di includere il valore corrente nella somma sinistra."],
         "Due somme cumulative bastano per O(n) tempo e O(1) spazio.")

add_task("missing-number", "arrays-strings", "Trovare il numero mancante", "easy", 20, "somma attesa",
         "Ricevi n numeri distinti scelti da 0 a n con un valore mancante. Restituisci quello assente. Vincoli: 0 <= n <= 100000; anche la somma intermedia deve usare 64 bit in C++.",
         "def missing_number(a):\n n=len(a)\n return n*(n+1)//2-sum(a)\n",
         "#include <numeric>\n#include <vector>\nusing namespace std;\nint missing_number(const vector<int>& a){int n=a.size();return 1LL*n*(n+1)/2-accumulate(a.begin(),a.end(),0LL);}\n",
         [{"name":"mancante centrale","expression":"missing_number([3,0,1])","expected":2},{"name":"manca zero","expression":"missing_number([1])","expected":0},{"name":"somma oltre int32","expression":"missing_number(list(range(80000)))","expected":80000}],
         [{"name":"mancante centrale","assertion":"missing_number({3,0,1})==2"},{"name":"manca zero","assertion":"missing_number({1})==0"},{"name":"somma oltre int32","assertion":"[](){vector<int> a(80000);iota(a.begin(),a.end(),0);return missing_number(a)==80000;}()"}],
         ["Confronta la somma da 0 a n con quella osservata.","La dimensione della lista è n, ma il massimo dominio termina a n."],
         "Un accumulo lineare e nessuna struttura ausiliaria: O(n) tempo e O(1) spazio.")

add_task("majority-element", "hashmap-set", "Valore presente in più della metà dei casi", "easy", 25, "voto di Boyer-Moore",
         "La lista non è vuota e un valore compare più di n/2 volte. Restituisci quel valore.",
         "def majority_element(a):\n candidate=None;balance=0\n for x in a:\n  if balance==0:candidate=x\n  balance += 1 if x==candidate else -1\n return candidate\n",
         "#include <vector>\nusing namespace std;\nint majority_element(const vector<int>& a){int c=0,b=0;for(int x:a){if(b==0)c=x;b+=(x==c?1:-1);}return c;}\n",
         [{"name":"maggioranza non contigua","expression":"majority_element([2,1,2,3,2,2,4])","expected":2},{"name":"un elemento","expression":"majority_element([9])","expected":9}],
         [{"name":"maggioranza non contigua","assertion":"majority_element({2,1,2,3,2,2,4})==2"},{"name":"un elemento","assertion":"majority_element({9})==9"}],
         ["Un valore diverso cancella un voto del candidato corrente.","La garanzia di maggioranza è parte del contratto: non serve una seconda verifica."],
         "Il conteggio bilanciato usa O(n) tempo e O(1) spazio. Senza la garanzia di maggioranza occorrerebbe verificare il candidato.")

add_task("merge-strings", "arrays-strings", "Alternare caratteri di due stringhe", "easy", 20, "indici sincronizzati",
         "Costruisci una stringa alternando un carattere da `a` e uno da `b`; quando una termina, aggiungi il resto dell'altra.",
         "def merge_strings(a,b):\n out=[]\n for i in range(max(len(a),len(b))):\n  if i<len(a):out.append(a[i])\n  if i<len(b):out.append(b[i])\n return ''.join(out)\n",
         "#include <algorithm>\n#include <string>\nusing namespace std;\nstring merge_strings(const string& a,const string& b){string o;for(size_t i=0;i<max(a.size(),b.size());++i){if(i<a.size())o+=a[i];if(i<b.size())o+=b[i];}return o;}\n",
         [{"name":"lunghezze uguali","expression":"merge_strings('abc','XYZ')","expected":"aXbYcZ"},{"name":"seconda più lunga","expression":"merge_strings('ab','wxyz')","expected":"awbxyz"}],
         [{"name":"lunghezze uguali","assertion":"merge_strings(\"abc\",\"XYZ\")==\"aXbYcZ\""},{"name":"seconda più lunga","assertion":"merge_strings(\"ab\",\"wxyz\")==\"awbxyz\""}],
         ["Itera fino alla lunghezza maggiore.","A ogni posizione aggiungi prima il carattere di a, poi quello di b, se esistono."],
         "Ogni carattere viene copiato una volta: O(n+m) tempo e O(n+m) spazio per il risultato.")












add_task("search-rotated", "binary-variants", "Ricerca binaria in un array ruotato", "medium", 30, "metà ordinata",
 "Array crescente distinto ruotato a un indice ignoto: restituisci l'indice di target o -1.",
 "def search_rotated(a,t):\n l,r=0,len(a)-1\n while l<=r:\n  m=(l+r)//2\n  if a[m]==t:return m\n  if a[l]<=a[m]:\n   if a[l]<=t<a[m]:r=m-1\n   else:l=m+1\n  elif a[m]<t<=a[r]:l=m+1\n  else:r=m-1\n return -1\n",
 "#include <vector>\nusing namespace std;\nint search_rotated(const vector<int>& a,int t){int l=0,r=a.size()-1;while(l<=r){int m=l+(r-l)/2;if(a[m]==t)return m;if(a[l]<=a[m]){if(a[l]<=t&&t<a[m])r=m-1;else l=m+1;}else if(a[m]<t&&t<=a[r])l=m+1;else r=m-1;}return -1;}\n",
 [{"name":"ruotato","expression":"search_rotated([4,5,6,7,0,1,2],0)","expected":4},{"name":"assente","expression":"search_rotated([6,7,1,2,3,4,5],8)","expected":-1}],
 [{"name":"ruotato","assertion":"search_rotated({4,5,6,7,0,1,2},0)==4"},{"name":"assente","assertion":"search_rotated({6,7,1,2,3,4,5},8)==-1"}],
 ["Almeno una metà attorno a mid è ordinata.","Confronta il target con i limiti di quella metà prima di scartarla."], "O(log n) confronti: la proprietà di ordinamento resta disponibile su una delle due metà.")

add_task("lower-bound", "binary-boundaries", "Primo elemento non minore del target", "medium", 20, "lower bound",
 "Restituisci il primo indice con valore >= target, oppure n se il target supera tutto l'array.",
 "def lower_bound(a,t):\n l,r=0,len(a)\n while l<r:\n  m=(l+r)//2\n  if a[m]<t:l=m+1\n  else:r=m\n return l\n",
 "#include <vector>\nusing namespace std;\nint lower_bound_index(const vector<int>& a,int t){int l=0,r=a.size();while(l<r){int m=l+(r-l)/2;if(a[m]<t)l=m+1;else r=m;}return l;}\n",
 [{"name":"duplicati","expression":"lower_bound([1,2,2,5],2)","expected":1},{"name":"oltre","expression":"lower_bound([1,3],9)","expected":2}],
 [{"name":"duplicati","assertion":"lower_bound_index({1,2,2,5},2)==1"},{"name":"oltre","assertion":"lower_bound_index({1,3},9)==2"}],
 ["L'intervallo candidato è semiaperto [left,right).","Se a[mid] è sufficiente, mid potrebbe essere il primo: conserva quel bordo."], "Il confine si trova con O(log n) tempo e O(1) spazio; l'indice n rappresenta l'assenza.")

add_task("min-eating-speed", "binary-answer", "Velocità minima per finire entro h ore", "medium", 30, "binary search on answer",
 "Ogni pila p richiede ceil(p/k) ore alla velocità intera k. Restituisci la velocità minima che finisce entro h ore. Vincoli: 1 ≤ len(p) ≤ 100.000, 1 ≤ p[i] ≤ 1.000.000.000 e h ≥ len(p).",
 "def min_speed(p,h):\n l,r=1,max(p)\n while l<r:\n  m=(l+r)//2\n  if sum((x+m-1)//m for x in p)<=h:r=m\n  else:l=m+1\n return l\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint min_speed(const vector<int>& p,int h){int l=1,r=*max_element(p.begin(),p.end());while(l<r){int m=l+(r-l)/2;long long hours=0;for(int x:p)hours+=(x+m-1)/m;if(hours<=h)r=m;else l=m+1;}return l;}\n",
 [{"name":"soglia","expression":"min_speed([3,6,7,11],8)","expected":4},{"name":"un'ora per pila","expression":"min_speed([30,11,23,4,20],5)","expected":30}],
 [{"name":"soglia","assertion":"min_speed({3,6,7,11},8)==4"},{"name":"un'ora per pila","assertion":"min_speed({30,11,23,4,20},5)==30"}],
 ["Definisci una verifica che dica se una velocità è fattibile.","La fattibilità è monotona: una velocità maggiore non richiede più ore."], "O(n log M): ricerca binaria sull'intervallo delle risposte con una verifica lineare.")

add_task("daily-temperatures", "monotonic-stack", "Attesa fino a una giornata più calda", "medium", 25, "stack monotono",
 "Per ogni giorno restituisci i giorni da attendere per trovare una temperatura più alta, oppure zero.",
 "def daily_temps(a):\n out=[0]*len(a);st=[]\n for i,x in enumerate(a):\n  while st and a[st[-1]]<x:\n   j=st.pop();out[j]=i-j\n  st.append(i)\n return out\n",
 "#include <vector>\nusing namespace std;\nvector<int> daily_temps(const vector<int>& a){vector<int> o(a.size()),st;for(int i=0;i<(int)a.size();++i){while(!st.empty()&&a[st.back()]<a[i]){int j=st.back();st.pop_back();o[j]=i-j;}st.push_back(i);}return o;}\n",
 [{"name":"salite","expression":"daily_temps([73,74,75,71,69,72,76,73])","expected":[1,1,4,2,1,1,0,0]},{"name":"discesa","expression":"daily_temps([5,4,3])","expected":[0,0,0]}],
 [{"name":"salite","assertion":"daily_temps({73,74,75,71,69,72,76,73})==vector<int>({1,1,4,2,1,1,0,0})"},{"name":"discesa","assertion":"daily_temps({5,4,3})==vector<int>({0,0,0})"}],
 ["Lo stack conserva indici ancora senza risposta.","La giornata corrente risolve quelli più freddi in cima allo stack."], "Ogni indice entra ed esce una volta: O(n) tempo e O(n) spazio.")

add_task("number-islands", "bfs-dfs-grid", "Contare componenti di terra", "medium", 30, "DFS su griglia",
 "Conta le componenti 4-connesse di '1' senza modificare la griglia. La griglia è rettangolare e può essere vuota; al massimo 200 righe e 200 colonne, solo caratteri 0/1.",
 "def num_islands(g):\n if not g:return 0\n R,C=len(g),len(g[0]);seen=set();n=0\n for r in range(R):\n  for c in range(C):\n   if g[r][c]=='1' and (r,c) not in seen:\n    n+=1;seen.add((r,c));st=[(r,c)]\n    while st:\n     x,y=st.pop()\n     for a,b in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=a<R and 0<=b<C and g[a][b]=='1' and (a,b) not in seen:seen.add((a,b));st.append((a,b))\n return n\n",
 "#include <string>\n#include <utility>\n#include <vector>\nusing namespace std;\nint num_islands(const vector<string>& g){if(g.empty())return 0;int R=g.size(),C=g[0].size(),ans=0;vector<vector<bool>> v(R,vector<bool>(C));int dr[]={-1,1,0,0},dc[]={0,0,-1,1};for(int i=0;i<R;i++)for(int j=0;j<C;j++)if(g[i][j]=='1'&&!v[i][j]){++ans;vector<pair<int,int>> st{{i,j}};v[i][j]=1;while(!st.empty()){auto [r,c]=st.back();st.pop_back();for(int k=0;k<4;k++){int x=r+dr[k],y=c+dc[k];if(x>=0&&x<R&&y>=0&&y<C&&g[x][y]=='1'&&!v[x][y])v[x][y]=1,st.push_back({x,y});}}}return ans;}\n",
 [{"name":"più regioni","expression":"num_islands(['11000','11010','00100','00011'])","expected":4},{"name":"acqua","expression":"num_islands(['000','000'])","expected":0}],
 [{"name":"più regioni","assertion":"num_islands({\"11000\",\"11010\",\"00100\",\"00011\"})==4"},{"name":"acqua","assertion":"num_islands({\"000\",\"000\"})==0"}],
 ["Avvia una DFS soltanto da terra non ancora visitata.","Marca i vicini quando li inserisci nello stack."], "Ogni cella viene esaminata un numero costante di volte: O(RC) tempo e spazio.")

add_task("kth-largest", "heap", "K-esimo valore più grande", "medium", 25, "heap di dimensione k",
 "Restituisci il k-esimo valore più grande, contando anche i duplicati. Vincoli: 1 <= k <= n <= 100000; valori fra -1000000 e 1000000.",
 "import heapq\ndef kth_largest(a,k):\n h=[]\n for x in a:\n  heapq.heappush(h,x)\n  if len(h)>k:heapq.heappop(h)\n return h[0]\n",
 "#include <functional>\n#include <queue>\n#include <vector>\nusing namespace std;\nint kth_largest(const vector<int>& a,int k){priority_queue<int,vector<int>,greater<int>> h;for(int x:a){h.push(x);if((int)h.size()>k)h.pop();}return h.top();}\n",
 [{"name":"duplicati inclusi","expression":"kth_largest([3,2,3,1,2,4,5,5,6],4)","expected":4},{"name":"massimo","expression":"kth_largest([7],1)","expected":7}],
 [{"name":"duplicati inclusi","assertion":"kth_largest({3,2,3,1,2,4,5,5,6},4)==4"},{"name":"massimo","assertion":"kth_largest({7},1)==7"}],
 ["Mantieni nel min-heap soltanto i k valori più grandi incontrati.","Quando la dimensione supera k, il minimo non può più essere tra le risposte candidate."], "O(n log k) tempo e O(k) spazio con un min-heap limitato.")

add_task("k-closest", "heap", "K punti più vicini all'origine", "medium", 30, "heap / ordinamento per distanza",
 "Restituisci i k punti con distanza quadrata minore dall'origine; a parità, ordina per x e poi y.",
 "def k_closest(points,k):\n return sorted(points,key=lambda p:(p[0]*p[0]+p[1]*p[1],p[0],p[1]))[:k]\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nvector<vector<int>> k_closest(vector<vector<int>> p,int k){sort(p.begin(),p.end(),[](auto&a,auto&b){long long x=1LL*a[0]*a[0]+1LL*a[1]*a[1],y=1LL*b[0]*b[0]+1LL*b[1]*b[1];return x!=y?x<y:(a[0]!=b[0]?a[0]<b[0]:a[1]<b[1]);});p.resize(k);return p;}\n",
 [{"name":"distanza e tie-break","expression":"k_closest([[3,3],[1,1],[-1,1]],2)","expected":[[-1,1],[1,1]]},{"name":"k uno","expression":"k_closest([[4,2],[1,0]],1)","expected":[[1,0]]}],
 [{"name":"distanza e tie-break","assertion":"k_closest({{3,3},{1,1},{-1,1}},2)==vector<vector<int>>({{-1,1},{1,1}})"},{"name":"k uno","assertion":"k_closest({{4,2},{1,0}},1)==vector<vector<int>>({{1,0}})"}],
 ["Confronta le distanze al quadrato: la radice non cambia l'ordine.","Usa un tipo abbastanza largo per moltiplicare coordinate grandi."], "Questa versione leggibile ordina n punti in O(n log n); per k piccolo un heap limita il costo a O(n log k).")

add_task("min-subarray-len", "sliding-window", "Segmento minimo con somma almeno target", "medium", 30, "finestra variabile",
 "I valori sono positivi. Restituisci la lunghezza minima di un segmento con somma >= target, oppure zero.",
 "def min_subarray_len(target,a):\n left=total=0;best=len(a)+1\n for right,x in enumerate(a):\n  total+=x\n  while total>=target:\n   best=min(best,right-left+1);total-=a[left];left+=1\n return 0 if best>len(a) else best\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint min_subarray_len(int t,const vector<int>& a){int l=0,sum=0,b=a.size()+1;for(int r=0;r<(int)a.size();++r){sum+=a[r];while(sum>=t){b=min(b,r-l+1);sum-=a[l++];}}return b>(int)a.size()?0:b;}\n",
 [{"name":"finestra corta","expression":"min_subarray_len(7,[2,3,1,2,4,3])","expected":2},{"name":"nessuna","expression":"min_subarray_len(20,[1,2,3])","expected":0}],
 [{"name":"finestra corta","assertion":"min_subarray_len(7,{2,3,1,2,4,3})==2"},{"name":"nessuna","assertion":"min_subarray_len(20,{1,2,3})==0"}],
 ["La positività rende monotona la somma quando il bordo sinistro avanza.","Mentre la finestra è valida, restringila e conserva la minima lunghezza."], "Ogni bordo avanza al massimo n volte: O(n) tempo e O(1) spazio. Con valori negativi la finestra non sarebbe valida.")
add_task("course-schedule", "topological-sort", "Verificare che tutti i corsi siano completabili", "medium", 30, "topological sort",
 "Ogni coppia [corso, prerequisito] è un arco prerequisito → corso. Restituisci True se non ci sono cicli.",
 "from collections import deque\ndef can_finish(n,edges):\n g=[[] for _ in range(n)];deg=[0]*n\n for course,pre in edges:g[pre].append(course);deg[course]+=1\n q=deque(i for i,d in enumerate(deg) if d==0);done=0\n while q:\n  x=q.popleft();done+=1\n  for y in g[x]:\n   deg[y]-=1\n   if deg[y]==0:q.append(y)\n return done==n\n",
 "#include <queue>\n#include <vector>\nusing namespace std;\nbool can_finish(int n,const vector<vector<int>>& e){vector<vector<int>> g(n);vector<int>d(n);for(auto x:e)g[x[1]].push_back(x[0]),++d[x[0]];queue<int>q;for(int i=0;i<n;i++)if(!d[i])q.push(i);int done=0;while(!q.empty()){int x=q.front();q.pop();++done;for(int y:g[x])if(--d[y]==0)q.push(y);}return done==n;}\n",
 [{"name":"catena aciclica","expression":"can_finish(3,[[1,0],[2,1]])","expected":True},{"name":"ciclo","expression":"can_finish(2,[[1,0],[0,1]])","expected":False}],
 [{"name":"catena aciclica","assertion":"can_finish(3,{{1,0},{2,1}})"},{"name":"ciclo","assertion":"!can_finish(2,{{1,0},{0,1}})"}],
 ["I corsi con indegree zero possono partire subito.","Se al termine sono stati rimossi meno di n nodi, nel grafo resta un ciclo."], "Kahn visita nodi e archi una volta: O(V+E) tempo e spazio.")

add_task("subsets", "backtracking", "Generare tutti i sottoinsiemi", "medium", 30, "backtracking include/skip",
 "Restituisci tutti i sottoinsiemi di valori distinti, in ordine lessicografico per test riproducibili. Vincoli: 0 <= n <= 12.",
 "def subsets(a):\n out=[[]]\n for x in a:out += [s+[x] for s in out]\n return sorted(out)\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nvector<vector<int>> subsets(const vector<int>& a){vector<vector<int>> o(1);for(int x:a){int n=o.size();for(int i=0;i<n;i++){auto v=o[i];v.push_back(x);o.push_back(v);}}sort(o.begin(),o.end());return o;}\n",
 [{"name":"tre valori","expression":"subsets([1,2])","expected":[[],[1],[1,2],[2]]},{"name":"vuoto","expression":"subsets([])","expected":[[]]}],
 [{"name":"tre valori","assertion":"subsets({1,2})==vector<vector<int>>({{},{1},{1,2},{2}})"},{"name":"vuoto","assertion":"subsets({})==vector<vector<int>>({{}})"}],
 ["Per ogni valore, duplica i risultati esistenti aggiungendolo.","n scelte binarie producono 2^n output: la crescita è intrinseca."], "Materializzare tutti i sottoinsiemi costa O(n·2^n) tempo e spazio di output. L'ordinamento lessicografico richiesto aggiunge confronti: limite peggiore O(n²·2^n) tempo; stack e copie sono ausiliari rispetto all'output.")

add_task("permutations", "backtracking", "Ordinare tutti gli ordini possibili", "medium", 30, "backtracking con scelta e ripristino",
 "I valori sono distinti. Restituisci tutte le permutazioni ordinate lessicograficamente. Vincoli: 0 <= n <= 8; per la lista vuota restituisci [[]].",
 "def permutations(a):\n a=sorted(a)\n out=[];path=[];used=[False]*len(a)\n def visit():\n  if len(path)==len(a):out.append(path.copy());return\n  for i,x in enumerate(a):\n   if not used[i]:used[i]=True;path.append(x);visit();path.pop();used[i]=False\n visit();return out\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nvector<vector<int>> permutations(vector<int> a){sort(a.begin(),a.end());vector<vector<int>>o;do{o.push_back(a);}while(next_permutation(a.begin(),a.end()));return o;}\n",
 [{"name":"tre elementi","expression":"permutations([1,2])","expected":[[1,2],[2,1]]},{"name":"input vuoto","expression":"permutations([])","expected":[[]]}],
 [{"name":"tre elementi","assertion":"permutations({1,2})==vector<vector<int>>({{1,2},{2,1}})"},{"name":"input vuoto","assertion":"permutations({})==vector<vector<int>>({{}})"}],
 ["Il path descrive una scelta parziale; used impedisce di riutilizzare un elemento.","Ripristina entrambi dopo la chiamata ricorsiva."], "Il numero di risultati è n!, quindi il tempo è O(n·n!) contando le copie.")

add_task("combination-sum", "backtracking", "Combinazioni che raggiungono il target", "medium", 35, "backtracking con indice iniziale",
 "I candidati sono distinti e positivi; uno stesso valore può essere usato più volte. Restituisci combinazioni uniche ordinate.",
 "def combination_sum(a,target):\n a=sorted(a);out=[];path=[]\n def go(start,left):\n  if left==0:out.append(path.copy());return\n  for i in range(start,len(a)):\n   if a[i]>left:break\n   path.append(a[i]);go(i,left-a[i]);path.pop()\n go(0,target);return out\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nvoid comb(const vector<int>&a,int s,int rem,vector<int>&p,vector<vector<int>>&o){if(!rem){o.push_back(p);return;}for(int i=s;i<(int)a.size()&&a[i]<=rem;i++){p.push_back(a[i]);comb(a,i,rem-a[i],p,o);p.pop_back();}}\nvector<vector<int>> combination_sum(vector<int>a,int t){sort(a.begin(),a.end());vector<vector<int>>o;vector<int>p;comb(a,0,t,p,o);return o;}\n",
 [{"name":"riuso candidato","expression":"combination_sum([2,3,6,7],7)","expected":[[2,2,3],[7]]},{"name":"nessuna","expression":"combination_sum([4,6],3)","expected":[]}],
 [{"name":"riuso candidato","assertion":"combination_sum({2,3,6,7},7)==vector<vector<int>>({{2,2,3},{7}})"},{"name":"nessuna","assertion":"combination_sum({4,6},3).empty()"}],
 ["Passa l'indice del candidato alla ricorsione: così puoi riutilizzarlo senza riordinare la combinazione.","Con candidati ordinati, interrompi quando il valore supera il residuo."], "Il costo dipende dai nodi visitati nell'albero di ricerca e dal numero di combinazioni prodotte; con candidati riutilizzabili può crescere esponenzialmente rispetto al target. Lo spazio ausiliario è O(target/minCandidate), oltre all'output.")

add_task("climbing-stairs", "dp-memoization", "Contare i modi per salire le scale", "easy", 20, "DP a stati sovrapposti",
 "Partendo da zero, puoi salire uno o due gradini per volta. Restituisci il numero di sequenze diverse che raggiungono il gradino n. Vincoli: 0 ≤ n ≤ 45.",
 "def climbing_stairs(n):\n if n<2:return 1\n two=one=1\n for _ in range(2,n+1):two,one=one,two+one\n return one\n",
 "#include <algorithm>\nusing namespace std;\nlong long climbing_stairs(int n){if(n<2)return 1;long long two=1,one=1;for(int i=2;i<=n;i++){long long next=two+one;two=one;one=next;}return one;}\n",
 [{"name":"cinque gradini","expression":"climbing_stairs(5)","expected":8},{"name":"partenza","expression":"climbing_stairs(0)","expected":1},{"name":"limite massimo dichiarato","expression":"climbing_stairs(45)","expected":1836311903}],
 [{"name":"cinque gradini","assertion":"climbing_stairs(5)==8"},{"name":"partenza","assertion":"climbing_stairs(0)==1"},{"name":"limite alto","assertion":"climbing_stairs(45)==1836311903LL"}],
 ["Definisci ways[i] in termini dei gradini da cui puoi arrivare a i.","I due sottoproblemi precedenti si ripetono; calcolali una sola volta e conserva solo gli ultimi due valori."],
 "La ricorrenza è ways[n] = ways[n-1] + ways[n-2], con ways[0] = ways[1] = 1. Il ciclo costa O(n) tempo e O(1) spazio; la versione ricorsiva ingenua ripete gli stessi stati esponenzialmente.")

add_task("house-robber", "dp-models", "Massimo bottino senza case adiacenti", "medium", 25, "DP a due stati compressa",
 "Ogni casa ha un valore non negativo. Massimizza il totale senza scegliere due case consecutive.",
 "def rob(a):\n two=one=0\n for x in a:two,one=one,max(one,two+x)\n return one\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint rob(const vector<int>&a){int two=0,one=0;for(int x:a){int next=max(one,two+x);two=one;one=next;}return one;}\n",
 [{"name":"scelta alternata","expression":"rob([2,7,9,3,1])","expected":12},{"name":"vuoto","expression":"rob([])","expected":0}],
 [{"name":"scelta alternata","assertion":"rob({2,7,9,3,1})==12"},{"name":"vuoto","assertion":"rob({})==0"}],
 ["Per ogni casa scegli tra saltarla e aggiungerla alla soluzione due posizioni prima.","Tieni soltanto i due stati precedenti."], "La ricorrenza è O(n) tempo e O(1) spazio; la base zero gestisce la lista vuota.")

add_task("coin-change", "dp-models", "Numero minimo di monete", "medium", 30, "DP tabulation",
 "Con monete positive riutilizzabili, restituisci il numero minimo per formare amount oppure -1. Vincoli: 0 <= amount <= 10000, da 1 a 50 monete positive di valore <= 10000. Per amount zero il risultato è zero.",
 "def coin_change(coins,amount):\n dp=[amount+1]*(amount+1);dp[0]=0\n for x in range(1,amount+1):\n  for c in coins:\n   if c<=x:dp[x]=min(dp[x],dp[x-c]+1)\n return -1 if dp[amount]>amount else dp[amount]\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint coin_change(const vector<int>&c,int a){vector<int>d(a+1,a+1);d[0]=0;for(int x=1;x<=a;x++)for(int v:c)if(v<=x)d[x]=min(d[x],d[x-v]+1);return d[a]>a?-1:d[a];}\n",
 [{"name":"combinazione minima","expression":"coin_change([1,2,5],11)","expected":3},{"name":"importo irraggiungibile","expression":"coin_change([2],3)","expected":-1},{"name":"greedy non ottimo","expression":"coin_change([1,3,4],6)","expected":2},{"name":"zero monete per zero","expression":"coin_change([2],0)","expected":0}],
 [{"name":"combinazione minima","assertion":"coin_change({1,2,5},11)==3"},{"name":"importo irraggiungibile","assertion":"coin_change({2},3)==-1"},{"name":"greedy non ottimo","assertion":"coin_change({1,3,4},6)==2"},{"name":"zero monete per zero","assertion":"coin_change({2},0)==0"}],
 ["dp[x] è il minimo numero di monete per l'importo x.","Per ogni moneta valida, prova la soluzione già nota per x-c più una moneta."], "La tabulazione costa O(amount·numeroMonete) tempo e O(amount) spazio.")

add_task("unique-paths", "dp-models", "Percorsi in una griglia senza ostacoli", "medium", 25, "DP su griglia compressa",
 "Partendo dall'angolo alto-sinistro, puoi muoverti solo a destra o in basso. Conta i percorsi fino all'angolo basso-destro. Vincoli: da 1 a 20 righe e da 1 a 20 colonne; usa un risultato intero a 64 bit.",
 "def unique_paths(rows,cols):\n dp=[1]*cols\n for _ in range(1,rows):\n  for c in range(1,cols):dp[c]+=dp[c-1]\n return dp[-1]\n",
 "#include <vector>\nusing namespace std;\nlong long unique_paths(int m,int n){vector<long long>d(n,1);for(int r=1;r<m;r++)for(int c=1;c<n;c++)d[c]+=d[c-1];return d.back();}\n",
 [{"name":"griglia rettangolare","expression":"unique_paths(3,7)","expected":28},{"name":"riga singola","expression":"unique_paths(1,5)","expected":1}],
 [{"name":"griglia rettangolare","assertion":"unique_paths(3,7)==28"},{"name":"riga singola","assertion":"unique_paths(1,5)==1"}],
 ["Ogni cella riceve i percorsi dall'alto e da sinistra.","Una singola riga di DP conserva il valore sopra prima di sovrascriverlo."], "O(rows·cols) tempo e O(cols) spazio.")

add_task("word-break", "dp-models", "Segmentare una stringa usando un dizionario", "medium", 30, "DP sui prefissi",
 "Restituisci True se la stringa può essere divisa in zero o più parole presenti nel dizionario. La stringa vuota è segmentabile. Vincoli: stringa ASCII di lunghezza <= 200, al massimo 100 parole ASCII non vuote lunghe <= 200.",
 "def word_break(s,words):\n words=set(words);dp=[False]*(len(s)+1);dp[0]=True\n for end in range(1,len(s)+1):\n  dp[end]=any(dp[start] and s[start:end] in words for start in range(end))\n return dp[-1]\n",
 "#include <string>\n#include <unordered_set>\n#include <vector>\nusing namespace std;\nbool word_break(const string&s,const vector<string>&w){unordered_set<string>d(w.begin(),w.end());vector<bool>dp(s.size()+1);dp[0]=true;for(int e=1;e<=(int)s.size();e++)for(int b=0;b<e;b++)if(dp[b]&&d.count(s.substr(b,e-b))){dp[e]=true;break;}return dp.back();}\n",
 [{"name":"più parole","expression":"word_break('applepenapple',['apple','pen'])","expected":True},{"name":"prefisso non segmentabile","expression":"word_break('catsandog',['cats','dog','sand','and','cat'])","expected":False}],
 [{"name":"più parole","assertion":"word_break(\"applepenapple\",{\"apple\",\"pen\"})"},{"name":"prefisso non segmentabile","assertion":"!word_break(\"catsandog\",{\"cats\",\"dog\",\"sand\",\"and\",\"cat\"})"}],
 ["dp[end] significa che il prefisso fino a end è segmentabile.","Prova ogni taglio precedente raggiungibile e cerca la parola residua."], "La versione base prova O(n²) tagli. Creare e fare hashing di sottostringhe di lunghezza fino a n porta a O(n³) tempo nel caso peggiore; O(n) stato DP più il dizionario. Input brevi rendono questa versione leggibile adeguata.")

add_task("meeting-rooms", "sorting-intervals", "Numero minimo di sale per riunioni", "medium", 25, "eventi ordinati",
 "Ogni intervallo è [inizio,fine) e gli estremi possono toccarsi senza sovrapposizione. Restituisci il numero minimo di sale.",
 "def min_rooms(intervals):\n starts=sorted(x[0] for x in intervals);ends=sorted(x[1] for x in intervals);s=e=rooms=best=0\n while s<len(starts):\n  if starts[s]<ends[e]:rooms+=1;s+=1;best=max(best,rooms)\n  else:rooms-=1;e+=1\n return best\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint min_rooms(vector<vector<int>> a){vector<int>s,e;for(auto x:a)s.push_back(x[0]),e.push_back(x[1]);sort(s.begin(),s.end());sort(e.begin(),e.end());int i=0,j=0,r=0,b=0;while(i<(int)s.size()){if(s[i]<e[j])b=max(b,++r),++i;else --r,++j;}return b;}\n",
 [{"name":"massimo simultaneo","expression":"min_rooms([[0,30],[5,10],[15,20]])","expected":2},{"name":"estremi adiacenti","expression":"min_rooms([[1,4],[4,8]])","expected":1}],
 [{"name":"massimo simultaneo","assertion":"min_rooms({{0,30},{5,10},{15,20}})==2"},{"name":"estremi adiacenti","assertion":"min_rooms({{1,4},{4,8}})==1"}],
 ["Ordina inizi e fini separatamente.","Se una riunione finisce all'ora d'inizio della successiva, la sala si libera prima di assegnarla."], "Due ordinamenti e una scansione: O(n log n) tempo, O(n) spazio.")
add_task("subarray-sum", "prefix-sum", "Contare segmenti contigui con somma k", "medium", 30, "prefissi e HashMap",
 "Conta i subarray con somma esattamente k; i numeri possono essere negativi.",
 "def subarray_sum(a,k):\n m={0:1};s=ans=0\n for x in a:s+=x;ans+=m.get(s-k,0);m[s]=m.get(s,0)+1\n return ans\n",
 "#include <unordered_map>\n#include <vector>\nusing namespace std;\nint subarray_sum(const vector<int>& a,int k){unordered_map<int,int>m{{0,1}};int s=0,n=0;for(int x:a){s+=x;n+=m[s-k];++m[s];}return n;}\n",
 [{"name":"prefissi","expression":"subarray_sum([1,1,1],2)","expected":2},{"name":"negativi","expression":"subarray_sum([1,-1,0],0)","expected":3}],
 [{"name":"prefissi","assertion":"subarray_sum({1,1,1},2)==2"},{"name":"negativi","assertion":"subarray_sum({1,-1,0},0)==3"}],
 ["Un segmento vale k se la differenza tra due prefissi è k.","Inizializza il prefisso vuoto a zero: include i segmenti da indice zero."], "Lookup medi O(1): O(n) tempo e O(n) spazio. La finestra non è affidabile con numeri negativi.")

add_task("merge-intervals", "sorting-intervals", "Fondere finestre sovrapposte", "medium", 25, "ordinamento e scansione",
 "Unisci intervalli sovrapposti o adiacenti al bordo. Restituisci output ordinato e disgiunto.",
 "def merge_intervals(a):\n out=[]\n for s,e in sorted(a):\n  if not out or s>out[-1][1]:out.append([s,e])\n  else:out[-1][1]=max(out[-1][1],e)\n return out\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nvector<vector<int>> merge_intervals(vector<vector<int>>a){sort(a.begin(),a.end());vector<vector<int>>o;for(auto x:a)if(o.empty()||x[0]>o.back()[1])o.push_back(x);else o.back()[1]=max(o.back()[1],x[1]);return o;}\n",
 [{"name":"unione","expression":"merge_intervals([[1,3],[2,6],[8,10],[10,12]])","expected":[[1,6],[8,12]]},{"name":"nessuno","expression":"merge_intervals([])","expected":[]}],
 [{"name":"unione","assertion":"merge_intervals({{1,3},{2,6},{8,10},{10,12}})==vector<vector<int>>({{1,6},{8,12}})"},{"name":"nessuno","assertion":"merge_intervals({}).empty()"}],
 ["Dopo il sort confronta con l'intervallo aperto più recente.","Se gli estremi uguali si uniscono, separa solo quando start > end corrente."], "Sort O(n log n), poi O(n) scansione.")

add_task("longest-substring", "sliding-window", "Sottostringa più lunga senza ripetizioni", "medium", 30, "finestra e ultimo indice",
 "Restituisci la lunghezza massima di una sottostringa contigua con caratteri distinti.",
 "def longest_unique(s):\n last={};l=best=0\n for r,c in enumerate(s):\n  if c in last:l=max(l,last[c]+1)\n  last[c]=r;best=max(best,r-l+1)\n return best\n",
 "#include <algorithm>\n#include <string>\n#include <unordered_map>\nusing namespace std;\nint longest_unique(const string&s){unordered_map<char,int>m;int l=0,b=0;for(int r=0;r<(int)s.size();++r){if(m.count(s[r]))l=max(l,m[s[r]]+1);m[s[r]]=r;b=max(b,r-l+1);}return b;}\n",
 [{"name":"ripetizione","expression":"longest_unique('pwwkew')","expected":3},{"name":"tutti distinti","expression":"longest_unique('abc')","expected":3}],
 [{"name":"ripetizione","assertion":"longest_unique(\"pwwkew\")==3"},{"name":"tutti distinti","assertion":"longest_unique(\"abc\")==3"}],
 ["Salta left oltre l'ultimo indice visto, senza arretrare.","Il valore massimo si aggiorna solo dopo avere ristabilito la finestra."], "Ogni carattere viene visitato una volta: O(n) tempo, O(k) spazio.")

add_task("character-replacement", "sliding-window", "Finestra con al massimo k sostituzioni", "medium", 30, "frequenze nella finestra",
 "Massimizza la lunghezza di una sottostringa che può diventare uniforme cambiando al massimo k caratteri.",
 "def character_replacement(s,k):\n c={};l=b=m=0\n for r,x in enumerate(s):\n  c[x]=c.get(x,0)+1;m=max(m,c[x])\n  if r-l+1-m>k:c[s[l]]-=1;l+=1\n  b=max(b,r-l+1)\n return b\n",
 "#include <algorithm>\n#include <string>\n#include <unordered_map>\nusing namespace std;\nint character_replacement(const string&s,int k){unordered_map<char,int>c;int l=0,b=0,m=0;for(int r=0;r<(int)s.size();++r){m=max(m,++c[s[r]]);if(r-l+1-m>k)--c[s[l++]];b=max(b,r-l+1);}return b;}\n",
 [{"name":"una sostituzione","expression":"character_replacement('AABABBA',1)","expected":4},{"name":"zero sostituzioni","expression":"character_replacement('ABAB',0)","expected":1}],
 [{"name":"una sostituzione","assertion":"character_replacement(\"AABABBA\",1)==4"},{"name":"zero sostituzioni","assertion":"character_replacement(\"ABAB\",0)==1"}],
 ["Le sostituzioni necessarie sono lunghezza meno frequenza dominante.","Quando il costo supera k, restringi la finestra dal bordo sinistro."], "Una scansione O(n); la mappa contiene le frequenze dei caratteri incontrati.")

add_task("product-except-self", "prefix-sum", "Prodotto di tutti gli elementi tranne quello corrente", "medium", 25, "prefissi e suffissi",
 "Restituisci il prodotto degli altri valori per ogni indice, senza divisioni. Vincoli: 2 <= n <= 10000; tutti i prodotti di prefissi, suffissi e risultati sono garantiti entro il signed 32 bit.",
 "def product_except_self(a):\n o=[1]*len(a);p=1\n for i,x in enumerate(a):o[i]=p;p*=x\n s=1\n for i in range(len(a)-1,-1,-1):o[i]*=s;s*=a[i]\n return o\n",
 "#include <vector>\nusing namespace std;\nvector<int> product_except_self(const vector<int>&a){vector<int>o(a.size(),1);int p=1;for(int i=0;i<(int)a.size();++i)o[i]=p,p*=a[i];int s=1;for(int i=(int)a.size()-1;i>=0;--i)o[i]*=s,s*=a[i];return o;}\n",
 [{"name":"zero","expression":"product_except_self([1,2,0,4])","expected":[0,0,8,0]},{"name":"senza zero","expression":"product_except_self([2,3,4])","expected":[12,8,6]}],
 [{"name":"zero","assertion":"product_except_self({1,2,0,4})==vector<int>({0,0,8,0})"},{"name":"senza zero","assertion":"product_except_self({2,3,4})==vector<int>({12,8,6})"}],
 ["Salva il prodotto a sinistra prima di aggiornare il prefisso.","Un passaggio inverso moltiplica per il suffisso senza salvarlo separatamente."], "O(n) tempo e O(1) spazio extra escluso il risultato; gli zeri funzionano senza rami dedicati.")

add_task("group-anagrams", "hashmap-set", "Raggruppare le permutazioni di parole", "medium", 25, "chiave canonica in HashMap",
 "Raggruppa le parole anagramma. Ordina gruppi e parole dentro ogni gruppo per output deterministico.",
 "def group_anagrams(a):\n m={}\n for w in a:m.setdefault(''.join(sorted(w)),[]).append(w)\n return sorted(sorted(v) for v in m.values())\n",
 "#include <algorithm>\n#include <string>\n#include <unordered_map>\n#include <vector>\nusing namespace std;\nvector<vector<string>> group_anagrams(const vector<string>&a){unordered_map<string,vector<string>>m;for(auto w:a){string k=w;sort(k.begin(),k.end());m[k].push_back(w);}vector<vector<string>>o;for(auto&[k,v]:m)sort(v.begin(),v.end()),o.push_back(v);sort(o.begin(),o.end());return o;}\n",
 [{"name":"due gruppi","expression":"group_anagrams(['eat','tea','tan','ate','nat','bat'])","expected":[["ate","eat","tea"],["bat"],["nat","tan"]]},{"name":"vuoto","expression":"group_anagrams([])","expected":[]}],
 [{"name":"due gruppi","assertion":"group_anagrams({\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"})==vector<vector<string>>({{\"ate\",\"eat\",\"tea\"},{\"bat\"},{\"nat\",\"tan\"}})"},{"name":"vuoto","assertion":"group_anagrams({}).empty()"}],
 ["La parola ordinata identifica tutte le sue permutazioni.","HashMap non ordina i gruppi: normalizza l'output soltanto per test e presentazione."], "Le firme costano O(sum k log k). Questa versione ordina anche parole e gruppi per il contratto di output: un limite complessivo è O(sum k log k + N log N · L), con N parole e L lunghezza massima. Memoria proporzionale ai dati raggruppati.")

add_task("top-k-frequent", "heap", "Selezionare i valori più frequenti", "medium", 30, "frequenze e ordine deterministico",
 "Restituisci k valori con frequenza più alta; a parità ordina il valore minore prima.",
 "from collections import Counter\ndef top_k(a,k):\n return [x for x,n in sorted(Counter(a).items(),key=lambda p:(-p[1],p[0]))[:k]]\n",
 "#include <algorithm>\n#include <unordered_map>\n#include <utility>\n#include <vector>\nusing namespace std;\nvector<int> top_k(const vector<int>&a,int k){unordered_map<int,int>m;for(int x:a)++m[x];vector<pair<int,int>>v(m.begin(),m.end());sort(v.begin(),v.end(),[](auto x,auto y){return x.second!=y.second?x.second>y.second:x.first<y.first;});vector<int>o;for(int i=0;i<k&&i<(int)v.size();i++)o.push_back(v[i].first);return o;}\n",
 [{"name":"pareggio","expression":"top_k([4,4,2,2,2,3],2)","expected":[2,4]},{"name":"k uno","expression":"top_k([1,1,5],1)","expected":[1]}],
 [{"name":"pareggio","assertion":"top_k({4,4,2,2,2,3},2)==vector<int>({2,4})"},{"name":"k uno","assertion":"top_k({1,1,5},1)==vector<int>({1})"}],
 ["Conta prima le occorrenze e rendi esplicito il tie-break nel comparatore.","Un min-heap limitato a k evita di ordinare tutti i distinti quando k è piccolo."], "La versione ordinata costa O(n + u log u); heap limitato O(n log k), con u valori distinti.")

add_task("three-sum", "two-pointers", "Triplette distinte con somma zero", "medium", 35, "sort e two pointers",
 "Restituisci tutte le triplette uniche con somma zero. Ordina i valori di ogni tripletta e ordina lessicograficamente le triplette risultanti. Indici distinti possono avere lo stesso valore; non ripetere una tripletta. Vincoli: 0 <= n <= 3000, valori interi fra -100000 e 100000. Con meno di tre elementi restituisci una lista vuota. Puoi ordinare una copia dell'input.",
 "def three_sum(a):\n a=sorted(a);o=[]\n for i in range(len(a)-2):\n  if i and a[i]==a[i-1]:continue\n  l,r=i+1,len(a)-1\n  while l<r:\n   s=a[i]+a[l]+a[r]\n   if s==0:\n    o.append([a[i],a[l],a[r]]);l+=1;r-=1\n    while l<r and a[l]==a[l-1]:l+=1\n    while l<r and a[r]==a[r+1]:r-=1\n   elif s<0:l+=1\n   else:r-=1\n return o\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nvector<vector<int>> three_sum(vector<int>a){sort(a.begin(),a.end());vector<vector<int>>o;for(int i=0;i+2<(int)a.size();i++){if(i&&a[i]==a[i-1])continue;int l=i+1,r=a.size()-1;while(l<r){int s=a[i]+a[l]+a[r];if(!s){o.push_back({a[i],a[l],a[r]});++l;--r;while(l<r&&a[l]==a[l-1])++l;while(l<r&&a[r]==a[r+1])--r;}else if(s<0)++l;else --r;}}return o;}\n",
 [{"name":"risultati distinti","expression":"three_sum([-1,0,1,2,-1,-4])","expected":[[-1,-1,2],[-1,0,1]]},{"name":"tutti zero","expression":"three_sum([0,0,0,0])","expected":[[0,0,0]]},{"name":"input minimo","expression":"three_sum([1,2])","expected":[]},{"name":"nessuna soluzione","expression":"three_sum([1,2,3,4])","expected":[]},{"name":"ripetizioni e ordine","expression":"three_sum([-2,0,0,2,2])","expected":[[-2,0,2]]}],
 [{"name":"risultati distinti","assertion":"three_sum({-1,0,1,2,-1,-4})==vector<vector<int>>({{-1,-1,2},{-1,0,1}})"},{"name":"tutti zero","assertion":"three_sum({0,0,0,0})==vector<vector<int>>({{0,0,0}})"},{"name":"input minimo","assertion":"three_sum({1,2}).empty()"},{"name":"nessuna soluzione","assertion":"three_sum({1,2,3,4}).empty()"},{"name":"ripetizioni e ordine","assertion":"three_sum({-2,0,0,2,2})==vector<vector<int>>({{-2,0,2}})"}],
 ["Fissa un valore e usa i puntatori per cercare il complemento.","Salta duplicati a tutti e tre i livelli per evitare triplette ripetute."], "Ordinamento O(n log n), ricerca O(n²). Le versioni fornite ordinano una copia: O(n) memoria aggiuntiva oltre al risultato; il sort può usare anche stack O(log n).")
add_task("search-range", "binary-boundaries", "Primo e ultimo indice del target", "medium", 25, "due ricerche di confine",
 "Restituisci [primo, ultimo] per target in un array ordinato o [-1,-1] se manca.",
 "def search_range(a,t):\n def b(upper):\n  l,r=0,len(a)\n  while l<r:\n   m=(l+r)//2\n   if a[m]<t or (upper and a[m]==t):l=m+1\n   else:r=m\n  return l\n x=b(False)\n return [-1,-1] if x==len(a) or a[x]!=t else [x,b(True)-1]\n",
 "#include <vector>\nusing namespace std;\nvector<int> search_range(const vector<int>&a,int t){auto b=[&](bool u){int l=0,r=a.size();while(l<r){int m=l+(r-l)/2;if(a[m]<t||(u&&a[m]==t))l=m+1;else r=m;}return l;};int x=b(0);if(x==(int)a.size()||a[x]!=t)return {-1,-1};return {x,b(1)-1};}\n",
 [{"name":"duplicati","expression":"search_range([1,2,2,2,5],2)","expected":[1,3]},{"name":"assente","expression":"search_range([1,3,5],4)","expected":[-1,-1]}],
 [{"name":"duplicati","assertion":"search_range({1,2,2,2,5},2)==vector<int>({1,3})"},{"name":"assente","assertion":"search_range({1,3,5},4)==vector<int>({-1,-1})"}],
 ["Trova il primo >= target e il primo > target.","Il valore precedente al secondo confine è l'ultimo target."], "Due ricerche binarie costano O(log n), anche con grandi blocchi di duplicati.")

add_task("insert-interval", "sorting-intervals", "Inserimento e fusione di un intervallo", "medium", 25, "merge lineare",
 "Gli intervalli sono ordinati e disgiunti. Inserisci il nuovo intervallo e fondi tutte le sovrapposizioni.",
 "def insert_interval(a,new):\n o=[];i=0\n while i<len(a) and a[i][1]<new[0]:o.append(a[i]);i+=1\n while i<len(a) and a[i][0]<=new[1]:new=[min(new[0],a[i][0]),max(new[1],a[i][1])];i+=1\n return o+[new]+a[i:]\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nvector<vector<int>> insert_interval(const vector<vector<int>>&a,vector<int>n){vector<vector<int>>o;int i=0;while(i<(int)a.size()&&a[i][1]<n[0])o.push_back(a[i++]);while(i<(int)a.size()&&a[i][0]<=n[1]){n[0]=min(n[0],a[i][0]);n[1]=max(n[1],a[i][1]);++i;}o.push_back(n);while(i<(int)a.size())o.push_back(a[i++]);return o;}\n",
 [{"name":"fusione interna","expression":"insert_interval([[1,2],[5,7],[9,12]],[6,10])","expected":[[1,2],[5,12]]},{"name":"intervallo isolato","expression":"insert_interval([[1,2],[5,7]],[3,4])","expected":[[1,2],[3,4],[5,7]]}],
 [{"name":"fusione interna","assertion":"insert_interval({{1,2},{5,7},{9,12}},{6,10})==vector<vector<int>>({{1,2},{5,12}})"},{"name":"intervallo isolato","assertion":"insert_interval({{1,2},{5,7}},{3,4})==vector<vector<int>>({{1,2},{3,4},{5,7}})"}],
 ["Copia gli intervalli a sinistra che non si sovrappongono.","Allarga new finché gli inizi successivi non superano la sua fine."], "Ogni intervallo viene letto una volta: O(n) tempo e O(n) spazio per l'output.")

add_task("container-water", "two-pointers", "Massima area tra due pareti", "medium", 25, "two pointers",
 "Ogni elemento è l'altezza di una parete. Trova l'area massima tra due indici distinti.",
 "def max_area(h):\n l,r=0,len(h)-1;b=0\n while l<r:\n  b=max(b,(r-l)*min(h[l],h[r]))\n  if h[l]<h[r]:l+=1\n  else:r-=1\n return b\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint max_area(const vector<int>&h){int l=0,r=h.size()-1,b=0;while(l<r){b=max(b,(r-l)*min(h[l],h[r]));if(h[l]<h[r])++l;else --r;}return b;}\n",
 [{"name":"massimo interno","expression":"max_area([1,8,6,2,5,4,8,3,7])","expected":49},{"name":"due pareti","expression":"max_area([2,3])","expected":2}],
 [{"name":"massimo interno","assertion":"max_area({1,8,6,2,5,4,8,3,7})==49"},{"name":"due pareti","assertion":"max_area({2,3})==2"}],
 ["L'area usa l'altezza minore e la distanza tra gli estremi.","Spostare la parete più alta non può migliorare il limite imposto da quella bassa."], "Un solo passaggio agli estremi: O(n) tempo e O(1) spazio.")

add_task("min-window", "sliding-window", "Finestra minima con tutte le frequenze richieste", "hard", 40, "finestra e contatori",
 "Trova la substring più corta di s contenente ogni carattere di t con la relativa molteplicità. Se t è vuota o non esiste una finestra valida, restituisci ''. I caratteri sono ASCII.",
        "from collections import Counter\ndef min_window(s,t):\n if not t:return ''\n need=Counter(t);missing=len(t);l=0;best=(0,len(s)+1)\n for r,c in enumerate(s):\n  if need[c]>0:missing-=1\n  need[c]-=1\n  while missing==0:\n   if r-l+1<best[1]-best[0]:best=(l,r+1)\n   need[s[l]]+=1\n   if need[s[l]]>0:missing+=1\n   l+=1\n return s[best[0]:best[1]] if best[1]<=len(s) else ''\n",
        "#include <climits>\n#include <string>\n#include <unordered_map>\nusing namespace std;\nstring min_window(const string&s,const string&t){if(t.empty())return \"\";unordered_map<char,int>n;for(char c:t)++n[c];int miss=t.size(),l=0,b=0,e=INT_MAX;for(int r=0;r<(int)s.size();r++){if(n[s[r]]-->0)--miss;while(!miss){if(r-l+1<e-b)b=l,e=r+1;if(++n[s[l++]]>0)++miss;}}return e==INT_MAX?\"\":s.substr(b,e-b);}\n",
        [{"name":"finestra più corta","expression":"min_window('ADOBECODEBANC','ABC')","expected":"BANC"},{"name":"frequenza impossibile","expression":"min_window('a','aa')","expected":""},{"name":"target vuoto","expression":"min_window('abc','')","expected":""},{"name":"sorgente vuota","expression":"min_window('','a')","expected":""}],
        [{"name":"finestra più corta","assertion":"min_window(\"ADOBECODEBANC\",\"ABC\")==\"BANC\""},{"name":"frequenza impossibile","assertion":"min_window(\"a\",\"aa\").empty()"},{"name":"target vuoto","assertion":"min_window(\"abc\",\"\").empty()"},{"name":"sorgente vuota","assertion":"min_window(\"\",\"a\").empty()"}],
 ["missing conta le occorrenze, non solo i tipi di carattere.","Quando la finestra è valida, stringila prima di estenderla ancora."], "I bordi avanzano linearmente: O(n+m) tempo e spazio legato all'alfabeto.")

add_task("oranges-rotting", "graphs", "Propagazione a livelli simultanei", "medium", 30, "BFS multi-source",
 "In una griglia, ogni 2 diffonde ai vicini 1 ortogonali ogni minuto. Restituisci il tempo per marciare tutto o -1.",
 "from collections import deque\ndef oranges_rotting(g):\n q=deque();fresh=0\n for r,row in enumerate(g):\n  for c,x in enumerate(row):\n   if x==2:q.append((r,c,0))\n   elif x==1:fresh+=1\n mins=0\n while q:\n  r,c,d=q.popleft();mins=max(mins,d)\n  for a,b in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):\n   if 0<=a<len(g) and 0<=b<len(g[0]) and g[a][b]==1:g[a][b]=2;fresh-=1;q.append((a,b,d+1))\n return mins if not fresh else -1\n",
 "#include <algorithm>\n#include <queue>\n#include <tuple>\n#include <vector>\nusing namespace std;\nint oranges_rotting(vector<vector<int>>g){int R=g.size(),C=R?g[0].size():0,f=0,m=0;queue<tuple<int,int,int>>q;for(int r=0;r<R;r++)for(int c=0;c<C;c++)if(g[r][c]==2)q.push({r,c,0});else if(g[r][c]==1)++f;int dr[]={-1,1,0,0},dc[]={0,0,-1,1};while(!q.empty()){auto [r,c,d]=q.front();q.pop();m=max(m,d);for(int k=0;k<4;k++){int x=r+dr[k],y=c+dc[k];if(x>=0&&x<R&&y>=0&&y<C&&g[x][y]==1)g[x][y]=2,--f,q.push({x,y,d+1});}}return f?-1:m;}\n",
 [{"name":"tutto raggiunto","expression":"oranges_rotting([[2,1,1],[1,1,0],[0,1,1]])","expected":4},{"name":"isolata","expression":"oranges_rotting([[2,0,1]])","expected":-1}],
 [{"name":"tutto raggiunto","assertion":"oranges_rotting({{2,1,1},{1,1,0},{0,1,1}})==4"},{"name":"isolata","assertion":"oranges_rotting({{2,0,1}})==-1"}],
 ["Accoda tutte le sorgenti prima di iniziare i livelli.","BFS visita ogni cella al minuto minimo e fresh conta ciò che resta irraggiungibile."], "O(RC) tempo e spazio, con ogni cella inserita in coda al massimo una volta.")

add_task("connected-components", "graphs", "Contare componenti di un grafo non diretto", "medium", 25, "DFS e visited",
 "Il grafo ha n nodi 0..n-1 e archi non diretti. Restituisci il numero di componenti connesse.",
 "def components(n,edges):\n g=[[] for _ in range(n)]\n for a,b in edges:g[a].append(b);g[b].append(a)\n seen=set();count=0\n for s in range(n):\n  if s not in seen:\n   count+=1;seen.add(s);st=[s]\n   while st:\n    x=st.pop()\n    for y in g[x]:\n     if y not in seen:seen.add(y);st.append(y)\n return count\n",
 "#include <vector>\nusing namespace std;\nint components(int n,const vector<vector<int>>&e){vector<vector<int>>g(n);for(auto x:e)g[x[0]].push_back(x[1]),g[x[1]].push_back(x[0]);vector<bool>v(n);int ans=0;for(int s=0;s<n;s++)if(!v[s]){++ans;vector<int>st{s};v[s]=1;while(!st.empty()){int x=st.back();st.pop_back();for(int y:g[x])if(!v[y])v[y]=1,st.push_back(y);}}return ans;}\n",
 [{"name":"due gruppi e isolato","expression":"components(5,[[0,1],[1,2],[3,4]])","expected":2},{"name":"nodi isolati","expression":"components(3,[])","expected":3}],
 [{"name":"due gruppi","assertion":"components(5,{{0,1},{1,2},{3,4}})==2"},{"name":"nodi isolati","assertion":"components(3,{})==3"}],
 ["Avvia la visita da ogni nodo ancora non visitato.","Un nodo isolato forma comunque una componente."], "Costruzione e DFS visitano O(V+E) elementi, con O(V+E) memoria per adjacency list e visited.")

add_task("interval-scheduling", "greedy", "Selezionare il massimo numero di intervalli compatibili", "medium", 25, "greedy per fine anticipata",
 "Restituisci quanti intervalli non sovrapposti puoi selezionare. Intervalli con end == next start sono compatibili.",
 "def max_nonoverlap(a):\n end=float('-inf');count=0\n for s,e in sorted(a,key=lambda x:(x[1],x[0])):\n  if s>=end:count+=1;end=e\n return count\n",
 "#include <algorithm>\n#include <climits>\n#include <vector>\nusing namespace std;\nint max_nonoverlap(vector<vector<int>>a){sort(a.begin(),a.end(),[](auto&x,auto&y){return x[1]!=y[1]?x[1]<y[1]:x[0]<y[0];});int end=INT_MIN,n=0;for(auto x:a)if(x[0]>=end)++n,end=x[1];return n;}\n",
 [{"name":"scelta greedy","expression":"max_nonoverlap([[1,3],[2,4],[3,5],[6,7]])","expected":3},{"name":"vuoto","expression":"max_nonoverlap([])","expected":0}],
 [{"name":"scelta greedy","assertion":"max_nonoverlap({{1,3},{2,4},{3,5},{6,7}})==3"},{"name":"vuoto","assertion":"max_nonoverlap({})==0"}],
 ["Scegliere l'intervallo che finisce prima lascia più spazio per i successivi.","Scarta soltanto chi inizia prima della fine già selezionata."], "Ordinamento O(n log n), scansione lineare. Il criterio greedy si giustifica con lo scambio del primo intervallo scelto: quello che finisce prima non toglie spazio ai successivi.")

add_task("max-depth", "recursion", "Profondità massima di un albero", "easy", 20, "ricorsione sui sottoalberi",
   "Restituisci il numero di nodi sul cammino più lungo dalla radice a una foglia. Un albero vuoto ha profondità zero. Vincoli: al massimo 10.000 nodi e altezza massima 500.",
 "class TreeNode:\n def __init__(self,val=0,left=None,right=None):self.val,self.left,self.right=val,left,right\ndef max_depth(root):\n return 0 if root is None else 1+max(max_depth(root.left),max_depth(root.right))\n",
 "#include <algorithm>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nint max_depth(TreeNode*n){return n?1+max(max_depth(n->left),max_depth(n->right)):0;}\n",
 [{"name":"rami di altezze diverse","expression":"max_depth(TreeNode(1,TreeNode(2,TreeNode(4)),TreeNode(3)))","expected":3},{"name":"albero vuoto","expression":"max_depth(None)","expected":0},{"name":"foglia","expression":"max_depth(TreeNode(7))","expected":1}],
 [{"name":"rami di altezze diverse","assertion":"[](){TreeNode a{4,nullptr,nullptr},l{2,&a,nullptr},r{3,nullptr,nullptr},root{1,&l,&r};return max_depth(&root)==3;}()"},{"name":"albero vuoto","assertion":"max_depth(nullptr)==0"},{"name":"foglia","assertion":"[](){TreeNode root{7,nullptr,nullptr};return max_depth(&root)==1;}()"}],
 ["Che valore deve restituire la chiamata per un sottoalbero vuoto?","Ogni chiamata aggiunge un livello e sceglie il ramo più profondo: quale progresso garantisce la terminazione?"],
 "La ricorsione termina ai figli nulli e combina le altezze in postorder. Ogni nodo viene visitato una volta: O(n) tempo e O(h) stack, dove h è l'altezza dell'albero.")

add_task("tree-diameter", "tree-traversal", "Diametro di un albero binario", "medium", 30, "postorder DFS",
 "Restituisci il numero di archi del cammino più lungo fra due nodi. Il cammino può passare dalla radice o no.",
 "class TreeNode:\n def __init__(self,val=0,left=None,right=None):self.val,self.left,self.right=val,left,right\ndef diameter(root):\n best=0\n def depth(n):\n  nonlocal best\n  if not n:return 0\n  l=depth(n.left);r=depth(n.right);best=max(best,l+r);return 1+max(l,r)\n depth(root);return best\n",
 "#include <algorithm>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nint depth(TreeNode*n,int&best){if(!n)return 0;int l=depth(n->left,best),r=depth(n->right,best);best=max(best,l+r);return 1+max(l,r);}\nint diameter(TreeNode*n){int b=0;depth(n,b);return b;}\n",
 [{"name":"cammino interno","expression":"diameter(TreeNode(1,TreeNode(2,TreeNode(4),TreeNode(5)),TreeNode(3)))","expected":3},{"name":"nodo singolo","expression":"diameter(TreeNode(1))","expected":0}],
 [{"name":"cammino interno","assertion":"[](){TreeNode a{4,nullptr,nullptr},b{5,nullptr,nullptr},l{2,&a,&b},r{3,nullptr,nullptr},root{1,&l,&r};return diameter(&root)==3;}()"},{"name":"nodo singolo","assertion":"[](){TreeNode r{1,nullptr,nullptr};return diameter(&r)==0;}()"}],
 ["Ogni chiamata restituisce l'altezza, ma aggiorna anche il miglior passaggio left+right.","Il diametro conta archi: un nodo singolo vale zero."], "Postorder visita ogni nodo una volta: O(n) tempo e O(h) stack.")

add_task("validate-bst", "bst-paths", "Convalidare l'ordine globale di un BST", "medium", 25, "DFS con limiti ereditati",
 "Restituisci True se ogni valore è strettamente compreso nei limiti imposti da tutti gli antenati.",
 "class TreeNode:\n def __init__(self,val,left=None,right=None):self.val,self.left,self.right=val,left,right\ndef valid_bst(root):\n def ok(n,lo,hi):\n  return True if n is None else lo<n.val<hi and ok(n.left,lo,n.val) and ok(n.right,n.val,hi)\n return ok(root,float('-inf'),float('inf'))\n",
 "#include <climits>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nbool valid_bst(TreeNode*n,long long lo=LLONG_MIN,long long hi=LLONG_MAX){return !n||(lo<n->val&&n->val<hi&&valid_bst(n->left,lo,n->val)&&valid_bst(n->right,n->val,hi));}\n",
 [{"name":"BST valido","expression":"valid_bst(TreeNode(5,TreeNode(3),TreeNode(8)))","expected":True},{"name":"vincolo dell'antenato","expression":"valid_bst(TreeNode(5,TreeNode(2,None,TreeNode(6)),TreeNode(8)))","expected":False}],
 [{"name":"BST valido","assertion":"[](){TreeNode a{3,nullptr,nullptr},b{8,nullptr,nullptr},r{5,&a,&b};return valid_bst(&r);}()"},{"name":"vincolo dell'antenato","assertion":"[](){TreeNode x{6,nullptr,nullptr},a{2,nullptr,&x},b{8,nullptr,nullptr},r{5,&a,&b};return !valid_bst(&r);}()"}],
 ["Il figlio sinistro rispetta il massimo di ogni antenato, non solo del genitore.","Passa intervalli aperti aggiornati a ogni passo ricorsivo."], "O(n) visita ogni nodo e O(h) spazio per la ricorsione; i limiti long long coprono gli estremi int.")

add_task("lca-bst", "bst-paths", "Lowest common ancestor in un BST", "medium", 25, "ricerca sullo split",
 "I due valori sono presenti in un BST. Restituisci il valore del loro antenato comune più basso.",
 "class TreeNode:\n def __init__(self,val,left=None,right=None):self.val,self.left,self.right=val,left,right\ndef lca_bst(root,p,q):\n lo,hi=sorted((p,q))\n while root:\n  if hi<root.val:root=root.left\n  elif lo>root.val:root=root.right\n  else:return root.val\n return None\n",
 "#include <algorithm>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nint lca_bst(TreeNode*n,int p,int q){int lo=min(p,q),hi=max(p,q);while(n){if(hi<n->val)n=n->left;else if(lo>n->val)n=n->right;else return n->val;}return -1;}\n",
 [{"name":"antenato su ramo","expression":"lca_bst(TreeNode(6,TreeNode(2,None,TreeNode(4)),TreeNode(8)),2,4)","expected":2},{"name":"nodi opposti","expression":"lca_bst(TreeNode(6,TreeNode(2),TreeNode(8)),2,8)","expected":6}],
 [{"name":"antenato su ramo","assertion":"[](){TreeNode b{4,nullptr,nullptr},a{2,nullptr,&b},r{6,&a,nullptr};return lca_bst(&r,2,4)==2;}()"},{"name":"nodi opposti","assertion":"[](){TreeNode a{2,nullptr,nullptr},b{8,nullptr,nullptr},r{6,&a,&b};return lca_bst(&r,2,8)==6;}()"}],
 ["Se entrambi i valori sono più piccoli, segui il figlio sinistro.","Il primo nodo che separa i target o coincide con uno dei due è l'antenato comune."], "Segue un unico ramo: O(h) tempo e O(1) spazio.")
add_task("trapping-rainwater", "two-pointers", "Acqua trattenuta fra le pareti", "hard", 35, "due puntatori e massimi prefissi",
 "Restituisci il volume d'acqua trattenuto fra barre non negative di larghezza uno. Vincoli: al massimo 20.000 barre, ciascuna alta al massimo 10.000.",
 "def trap(h):\n l,r=0,len(h)-1;lm=rm=ans=0\n while l<r:\n  if h[l]<h[r]:lm=max(lm,h[l]);ans+=lm-h[l];l+=1\n  else:rm=max(rm,h[r]);ans+=rm-h[r];r-=1\n return ans\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint trap(const vector<int>&h){int l=0,r=h.size()-1,lm=0,rm=0,a=0;while(l<r){if(h[l]<h[r]){lm=max(lm,h[l]);a+=lm-h[l++];}else{rm=max(rm,h[r]);a+=rm-h[r--];}}return a;}\n",
 [{"name":"bacino multiplo","expression":"trap([0,1,0,2,1,0,1,3,2,1,2,1])","expected":6},{"name":"barre discendenti","expression":"trap([4,2,0,3,2,5])","expected":9}],
 [{"name":"bacino multiplo","assertion":"trap({0,1,0,2,1,0,1,3,2,1,2,1})==6"},{"name":"barre discendenti","assertion":"trap({4,2,0,3,2,5})==9"}],
 ["L'acqua a un bordo dipende dal massimo visto da quel lato.","Elabora il bordo più basso: l'altro lato garantisce un limite almeno altrettanto alto."], "O(n) tempo e O(1) spazio, mantenendo i due massimi mentre i puntatori convergono.")

add_task("reverse-list", "linked-lists", "Invertire una lista collegata", "easy", 20, "riferimenti previous/current/next",
 "Inverti i collegamenti di una lista singolarmente collegata e restituisci la nuova testa. I nodi vanno riutilizzati. Vincoli: al massimo 100.000 nodi.",
 "class ListNode:\n def __init__(self,val=0,next=None):self.val,self.next=val,next\ndef reverse_list(head):\n prev=None\n cur=head\n while cur:\n  nxt=cur.next\n  cur.next=prev\n  prev=cur\n  cur=nxt\n return prev\n",
 "struct ListNode{int val;ListNode*next;};\nListNode* reverse_list(ListNode*head){ListNode*prev=nullptr;while(head){ListNode*next=head->next;head->next=prev;prev=head;head=next;}return prev;}\n",
 [{"name":"tre nodi","expression":"(lambda n:n.val==3 and n.next.val==2 and n.next.next.val==1 and n.next.next.next is None)(reverse_list(ListNode(1,ListNode(2,ListNode(3)))) )","expected":True},{"name":"lista vuota","expression":"reverse_list(None)","expected":None},{"name":"nodo singolo","expression":"reverse_list(ListNode(8)).val","expected":8}],
 [{"name":"tre nodi","assertion":"[](){ListNode a{1,nullptr},b{2,nullptr},c{3,nullptr};a.next=&b;b.next=&c;auto*r=reverse_list(&a);return r==&c&&r->next==&b&&r->next->next==&a&&a.next==nullptr;}()"},{"name":"lista vuota","assertion":"reverse_list(nullptr)==nullptr"},{"name":"nodo singolo","assertion":"[](){ListNode a{8,nullptr};return reverse_list(&a)==&a&&a.next==nullptr;}()"}],
 ["Prima di cambiare un link, dove salvi il nodo successivo?","Disegna il passaggio sul primo nodo e indica che cosa contiene ciascun puntatore dopo l'iterazione."],
 "Ogni nodo viene visitato una volta: O(n) tempo e O(1) spazio aggiuntivo. Salvare next prima della riassegnazione evita di perdere il resto della lista.")

add_task("lru-cache", "linked-lists", "Cache LRU con capacità limitata", "hard", 40, "HashMap e lista doppiamente collegata",
 "Implementa una cache Least Recently Used con `get` e `put` in tempo medio O(1). Le operazioni sono `[0, key, value]` per put e `[1, key]` per get; registra soltanto i valori restituiti da get, usando -1 per una chiave assente. Un get riuscito e un put rendono la chiave più recente. Quando superi la capacità, rimuovi quella meno recente. Vincoli: capacità da 1 a 1.000, chiavi intere.",
 "class _Node:\n def __init__(self,key=0,value=0):self.key,self.value,self.prev,self.next=key,value,None,None\nclass LRUCache:\n def __init__(self,capacity):\n  self.capacity=capacity;self.nodes={};self.head=_Node();self.tail=_Node();self.head.next=self.tail;self.tail.prev=self.head\n def _remove(self,node):\n  node.prev.next=node.next;node.next.prev=node.prev\n def _front(self,node):\n  node.prev=self.head;node.next=self.head.next;self.head.next.prev=node;self.head.next=node\n def get(self,key):\n  node=self.nodes.get(key)\n  if node is None:return -1\n  self._remove(node);self._front(node);return node.value\n def put(self,key,value):\n  node=self.nodes.get(key)\n  if node is not None:self._remove(node);node.value=value\n  else:node=_Node(key,value);self.nodes[key]=node\n  self._front(node)\n  if len(self.nodes)>self.capacity:\n   old=self.tail.prev;self._remove(old);del self.nodes[old.key]\ndef lru_cache(capacity,operations):\n cache=LRUCache(capacity);result=[]\n for op in operations:\n  if op[0]==0:cache.put(op[1],op[2])\n  else:result.append(cache.get(op[1]))\n return result\n",
 "#include <list>\n#include <unordered_map>\n#include <vector>\nusing namespace std;\nclass LRUCache{int capacity;list<pair<int,int>>order;unordered_map<int,list<pair<int,int>>::iterator>where;public:explicit LRUCache(int c):capacity(c){}int get(int k){auto it=where.find(k);if(it==where.end())return -1;order.splice(order.begin(),order,it->second);return it->second->second;}void put(int k,int v){auto it=where.find(k);if(it!=where.end()){it->second->second=v;order.splice(order.begin(),order,it->second);return;}order.push_front({k,v});where[k]=order.begin();if((int)where.size()>capacity){int old=order.back().first;where.erase(old);order.pop_back();}}};\nvector<int> lru_cache(int capacity,const vector<vector<int>>&ops){LRUCache c(capacity);vector<int>out;for(const auto&op:ops)if(op[0]==0)c.put(op[1],op[2]);else out.push_back(c.get(op[1]));return out;}\n",
 [{"name":"accesso e rimozione meno recente","expression":"lru_cache(2,[[0,1,1],[0,2,2],[1,1],[0,3,3],[1,2]])","expected":[1,-1]},{"name":"aggiornamento rende recente","expression":"lru_cache(2,[[0,1,10],[0,2,2],[0,1,11],[1,1],[1,2]])","expected":[11,2]},{"name":"capacità uno","expression":"lru_cache(1,[[0,4,40],[0,5,50],[1,4],[1,5]])","expected":[-1,50]}],
 [{"name":"accesso e rimozione meno recente","assertion":"lru_cache(2,{{0,1,1},{0,2,2},{1,1},{0,3,3},{1,2}})==vector<int>({1,-1})"},{"name":"aggiornamento rende recente","assertion":"lru_cache(2,{{0,1,10},{0,2,2},{0,1,11},{1,1},{1,2}})==vector<int>({11,2})"},{"name":"capacità uno","assertion":"lru_cache(1,{{0,4,40},{0,5,50},{1,4},{1,5}})==vector<int>({-1,50})"}],
 ["La mappa trova il nodo senza scorrere la lista; la lista conserva l'ordine di uso.","Dopo get o put sposta la chiave in testa. Quale nodo della coda va eliminato quando superi la capacità?"],
 "HashMap e lista doppiamente collegata condividono i nodi: get e put richiedono O(1) medio e la memoria è O(capacità). In C++ `list::splice` riordina un iteratore senza copiarne gli elementi.")

add_task("merge-k-lists", "linked-lists", "Fondere k liste ordinate", "hard", 35, "min-heap di teste",
 "Unisci k liste collegate crescenti in un'unica lista crescente. I nodi sono riutilizzabili.",
 "import heapq\nclass ListNode:\n def __init__(self,val=0,next=None):self.val,self.next=val,next\ndef merge_k_lists(lists):\n h=[];serial=0\n for node in lists:\n  if node:heapq.heappush(h,(node.val,serial,node));serial+=1\n dummy=tail=ListNode()\n while h:\n  _,_,node=heapq.heappop(h);tail.next=node;tail=node\n  if node.next:heapq.heappush(h,(node.next.val,serial,node.next));serial+=1\n tail.next=None;return dummy.next\n",
 "#include <queue>\n#include <vector>\nusing namespace std;\nstruct ListNode{int val;ListNode*next;};\nListNode* merge_k_lists(vector<ListNode*> a){auto cmp=[](ListNode*x,ListNode*y){return x->val>y->val;};priority_queue<ListNode*,vector<ListNode*>,decltype(cmp)>q(cmp);for(auto n:a)if(n)q.push(n);ListNode d{0,nullptr},*t=&d;while(!q.empty()){auto n=q.top();q.pop();t->next=n;t=n;if(n->next)q.push(n->next);}if(t)t->next=nullptr;return d.next;}\nvector<int> vals(ListNode*n){vector<int>v;for(;n;n=n->next)v.push_back(n->val);return v;}\nListNode* make_nodes(vector<int>a){ListNode d{0,nullptr},*t=&d;for(int x:a){t->next=new ListNode{x,nullptr};t=t->next;}return d.next;}\n",
 [{"name":"liste disgiunte","expression":"(lambda n:[n.val,n.next.val,n.next.next.val,n.next.next.next.val,n.next.next.next.next.val])(merge_k_lists([ListNode(1,ListNode(4)),ListNode(1,ListNode(3)),ListNode(2,ListNode(6))]))","expected":[1,1,2,3,4]},{"name":"liste vuote","expression":"merge_k_lists([])","expected":None}],
 [{"name":"liste disgiunte","assertion":"vals(merge_k_lists({make_nodes({1,4}),make_nodes({1,3}),make_nodes({2,6})}))==vector<int>({1,1,2,3,4,6})"},{"name":"liste vuote","assertion":"merge_k_lists({})==nullptr"}],
 ["Il heap conserva soltanto il prossimo nodo disponibile per ogni lista.","Dopo l'estrazione, inserisci il successivo della stessa lista."], "Ogni nodo entra nel heap una volta: O(N log k) tempo e O(k) spazio ausiliario.")

add_task("word-ladder", "graphs", "Trasformazione minima tra parole", "hard", 40, "BFS per livelli",
 "Ogni passo cambia una sola lettera fra a-z e produce una parola di lunghezza uguale nel dizionario. Restituisci il numero di parole del cammino minimo, includendo begin; se non esiste, zero. begin ed end hanno la stessa lunghezza.",
 "from collections import deque\ndef word_ladder(begin,end,words):\n if begin==end:return 1\n allowed={word for word in words if len(word)==len(begin)}\n if end not in allowed:return 0\n q=deque([(begin,1)]);seen={begin}\n while q:\n  word,d=q.popleft()\n  for i in range(len(word)):\n   for c in 'abcdefghijklmnopqrstuvwxyz':\n    nxt=word[:i]+c+word[i+1:]\n    if nxt==end:return d+1\n    if nxt in allowed and nxt not in seen:seen.add(nxt);q.append((nxt,d+1))\n return 0\n",
 "#include <queue>\n#include <string>\n#include <utility>\n#include <unordered_set>\n#include <vector>\nusing namespace std;\nint word_ladder(string b,string e,const vector<string>&w){if(b==e)return 1;unordered_set<string>d;for(const auto&x:w)if(x.size()==b.size())d.insert(x);if(!d.count(e))return 0;queue<pair<string,int>>q;q.push({b,1});unordered_set<string>s{b};while(!q.empty()){auto [x,n]=q.front();q.pop();for(int i=0;i<(int)x.size();i++){char old=x[i];for(char c='a';c<='z';c++){x[i]=c;if(x==e)return n+1;if(d.count(x)&&s.insert(x).second)q.push({x,n+1});}x[i]=old;}}return 0;}\n",
 [{"name":"cammino breve","expression":"word_ladder('hit','cog',['hot','dot','dog','lot','log','cog'])","expected":5},{"name":"destinazione assente","expression":"word_ladder('hit','cog',['hot','dot','dog'])","expected":0},{"name":"parole di altra lunghezza ignorate","expression":"word_ladder('a','c',['xy','b','c'])","expected":2},{"name":"inizio uguale alla fine","expression":"word_ladder('same','same',[]) ","expected":1}],
 [{"name":"cammino breve","assertion":"word_ladder(\"hit\",\"cog\",{\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"})==5"},{"name":"destinazione assente","assertion":"word_ladder(\"hit\",\"cog\",{\"hot\",\"dot\",\"dog\"})==0"},{"name":"parole di altra lunghezza ignorate","assertion":"word_ladder(\"a\",\"c\",{\"xy\",\"b\",\"c\"})==2"},{"name":"inizio uguale alla fine","assertion":"word_ladder(\"same\",\"same\",{})==1"}],
 ["La BFS visita prima tutti i cammini di lunghezza d.","Genera vicini cambiando una posizione e usa visited per evitare cicli."], "Con alfabeto fisso e parole di lunghezza L: O(N·L·26·L) nella versione che costruisce stringhe.")

add_task("network-delay", "graphs", "Tempo massimo di consegna con pesi positivi", "hard", 40, "Dijkstra e priority_queue",
 "Da nodo iniziale k, gli archi diretti hanno peso positivo. Restituisci il massimo tempo minimo per raggiungere tutti i nodi 1..n, o -1.",
 "import heapq\ndef network_delay(edges,n,k):\n g=[[] for _ in range(n+1)]\n for u,v,w in edges:g[u].append((v,w))\n dist=[float('inf')]*(n+1);dist[k]=0;h=[(0,k)]\n while h:\n  d,u=heapq.heappop(h)\n  if d!=dist[u]:continue\n  for v,w in g[u]:\n   nd=d+w\n   if nd<dist[v]:dist[v]=nd;heapq.heappush(h,(nd,v))\n ans=max(dist[1:]);return -1 if ans==float('inf') else ans\n",
 "#include <algorithm>\n#include <climits>\n#include <functional>\n#include <queue>\n#include <tuple>\n#include <utility>\n#include <vector>\nusing namespace std;\nint network_delay(const vector<vector<int>>&e,int n,int k){vector<vector<pair<int,int>>>g(n+1);for(auto x:e)g[x[0]].push_back({x[1],x[2]});vector<int>d(n+1,INT_MAX);d[k]=0;priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>>q;q.push({0,k});while(!q.empty()){auto [cost,u]=q.top();q.pop();if(cost!=d[u])continue;for(auto [v,w]:g[u])if(cost+w<d[v])d[v]=cost+w,q.push({d[v],v});}int a=0;for(int i=1;i<=n;i++){if(d[i]==INT_MAX)return -1;a=max(a,d[i]);}return a;}\n",
 [{"name":"cammino indiretto","expression":"network_delay([[2,1,1],[2,3,1],[3,4,1]],4,2)","expected":2},{"name":"nodo irraggiungibile","expression":"network_delay([[1,2,1]],3,1)","expected":-1}],
 [{"name":"cammino indiretto","assertion":"network_delay({{2,1,1},{2,3,1},{3,4,1}},4,2)==2"},{"name":"nodo irraggiungibile","assertion":"network_delay({{1,2,1}},3,1)==-1"}],
 ["Dijkstra finalizza prima il costo minore disponibile nel heap.","Scarta le entry obsolete quando il costo estratto non coincide più con dist[u]."], "Con heap binario O((V+E) log V) tempo e O(V+E) spazio. I pesi devono essere non negativi.")

add_task("max-path-sum", "tree-traversal", "Massima somma di un cammino in un albero", "hard", 40, "postorder e contributo positivo",
   "L'albero non è vuoto. Un cammino può iniziare e finire in qualsiasi nodo, ma non ripassa su un nodo. Restituisci la somma massima; i valori possono essere negativi. Vincoli: al massimo 10.000 nodi, altezza massima 500, -10.000 ≤ valore ≤ 10.000.",
 "class TreeNode:\n def __init__(self,val,left=None,right=None):self.val,self.left,self.right=val,left,right\ndef max_path_sum(root):\n best=float('-inf')\n def gain(n):\n  nonlocal best\n  if not n:return 0\n  l=max(0,gain(n.left));r=max(0,gain(n.right));best=max(best,n.val+l+r)\n  return n.val+max(l,r)\n gain(root);return best\n",
 "#include <algorithm>\n#include <climits>\nusing namespace std;\nstruct TreeNode{int val;TreeNode*left;TreeNode*right;};\nint gain(TreeNode*n,int&best){if(!n)return 0;int l=max(0,gain(n->left,best)),r=max(0,gain(n->right,best));best=max(best,n->val+l+r);return n->val+max(l,r);}\nint max_path_sum(TreeNode*n){int b=INT_MIN;gain(n,b);return b;}\n",
 [{"name":"cammino non alla radice","expression":"max_path_sum(TreeNode(-10,TreeNode(9),TreeNode(20,TreeNode(15),TreeNode(7))))","expected":42},{"name":"tutti negativi","expression":"max_path_sum(TreeNode(-3,TreeNode(-8),TreeNode(-2)))","expected":-2}],
 [{"name":"cammino non alla radice","assertion":"[](){TreeNode a{9,nullptr,nullptr},b{15,nullptr,nullptr},c{7,nullptr,nullptr},d{20,&b,&c},r{-10,&a,&d};return max_path_sum(&r)==42;}()"},{"name":"tutti negativi","assertion":"[](){TreeNode a{-8,nullptr,nullptr},b{-2,nullptr,nullptr},r{-3,&a,&b};return max_path_sum(&r)==-2;}()"}],
 ["Ogni ricorsione restituisce un solo ramo utilizzabile dal genitore.","Aggiorna il cammino globale usando entrambi i contributi positivi al nodo corrente."], "Postorder O(n) tempo e O(h) stack; inizializzare best a -infinito gestisce alberi tutti negativi.")

add_task("edit-distance", "dp-models", "Distanza minima tra due stringhe", "hard", 40, "DP su prefissi",
 "Restituisci il minimo di inserimenti, eliminazioni e sostituzioni per trasformare una stringa nell'altra.",
 "def edit_distance(a,b):\n prev=list(range(len(b)+1))\n for i,x in enumerate(a,1):\n  cur=[i]+[0]*len(b)\n  for j,y in enumerate(b,1):cur[j]=min(cur[j-1]+1,prev[j]+1,prev[j-1]+(x!=y))\n  prev=cur\n return prev[-1]\n",
 "#include <algorithm>\n#include <string>\n#include <vector>\nusing namespace std;\nint edit_distance(const string&a,const string&b){vector<int>p(b.size()+1);for(int j=0;j<=(int)b.size();j++)p[j]=j;for(int i=1;i<=(int)a.size();i++){vector<int>c(b.size()+1);c[0]=i;for(int j=1;j<=(int)b.size();j++)c[j]=min({c[j-1]+1,p[j]+1,p[j-1]+(a[i-1]!=b[j-1])});p.swap(c);}return p.back();}\n",
 [{"name":"trasformazioni multiple","expression":"edit_distance('horse','ros')","expected":3},{"name":"identiche","expression":"edit_distance('same','same')","expected":0}],
 [{"name":"trasformazioni multiple","assertion":"edit_distance(\"horse\",\"ros\")==3"},{"name":"identiche","assertion":"edit_distance(\"same\",\"same\")==0"}],
 ["Definisci dp[i][j] come il costo di trasformare i primi i e j caratteri.","I tre predecessori corrispondono a inserire, eliminare o sostituire."], "O(mn) tempo; la versione a due righe usa O(min(m,n)) spazio se si scambia l'ordine delle stringhe.")

add_task("largest-rectangle", "monotonic-stack", "Rettangolo massimo in un istogramma", "hard", 35, "stack monotono crescente",
 "Restituisci l'area massima del rettangolo contenuto nell'istogramma; larghezza di ogni barra uno.",
 "def largest_rectangle(h):\n st=[];best=0\n for i,x in enumerate(h+[0]):\n  while st and h[st[-1]]>x:\n   height=h[st.pop()];left=st[-1] if st else -1;best=max(best,height*(i-left-1))\n  st.append(i)\n return best\n",
 "#include <algorithm>\n#include <vector>\nusing namespace std;\nint largest_rectangle(const vector<int>&h){vector<int>st;int b=0;for(int i=0;i<=(int)h.size();i++){int x=i==(int)h.size()?0:h[i];while(!st.empty()&&h[st.back()]>x){int z=h[st.back()];st.pop_back();int l=st.empty()?-1:st.back();b=max(b,z*(i-l-1));}st.push_back(i);}return b;}\n",
 [{"name":"barre differenti","expression":"largest_rectangle([2,1,5,6,2,3])","expected":10},{"name":"altezza uniforme","expression":"largest_rectangle([3,3,3])","expected":9}],
 [{"name":"barre differenti","assertion":"largest_rectangle({2,1,5,6,2,3})==10"},{"name":"altezza uniforme","assertion":"largest_rectangle({3,3,3})==9"}],
 ["Lo stack mantiene indici con altezze crescenti.","Quando una barra più bassa arriva, la barra in cima ha trovato il suo bordo destro."], "Ogni barra entra ed esce una volta: O(n) tempo e O(n) spazio.")

add_task("stock-cooldown", "dp-models", "Trading con un giorno di cooldown", "hard", 35, "DP hold/sold/rest",
 "Puoi comprare e vendere più volte, ma dopo una vendita devi aspettare un giorno prima di comprare. Massimizza il profitto.",
 "def max_profit_cooldown(p):\n hold=float('-inf');sold=0;rest=0\n for x in p:\n  old_hold,old_sold,old_rest=hold,sold,rest\n  hold=max(old_hold,old_rest-x)\n  sold=old_hold+x\n  rest=max(old_rest,old_sold)\n return max(sold,rest)\n",
 "#include <algorithm>\n#include <climits>\n#include <vector>\nusing namespace std;\nint max_profit_cooldown(const vector<int>&p){int hold=INT_MIN/2,sold=0,rest=0;for(int x:p){int h=hold,s=sold,r=rest;hold=max(h,r-x);sold=h+x;rest=max(r,s);}return max(sold,rest);}\n",
 [{"name":"cooldown rispettato","expression":"max_profit_cooldown([1,2,3,0,2])","expected":3},{"name":"nessun profitto","expression":"max_profit_cooldown([5,4,3])","expected":0}],
 [{"name":"cooldown rispettato","assertion":"max_profit_cooldown({1,2,3,0,2})==3"},{"name":"nessun profitto","assertion":"max_profit_cooldown({5,4,3})==0"}],
 ["Tieni separati holding, vendita appena fatta e possibilità di riposo.","Usa lo stato del giorno precedente: aggiornare in sequenza può riciclare un valore del giorno corrente."], "Tre stati per giorno, O(n) tempo e O(1) spazio. Il cooldown è codificato dal passaggio sold → rest → hold.")



EXERCISES.extend([
    code_exercise(
        "linked-list-cycle", "linked-lists", "Rilevare un ciclo nei collegamenti", "easy", 20,
        "fast/slow pointers",
        "Ricevi la testa di una lista di al massimo 10000 nodi. Restituisci True se seguendo next si entra in un ciclo, False altrimenti. Non modificare i link. Valori duplicati sono ammessi: confronta l'identità dei nodi, non i valori. La testa può essere nulla.",
        "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head):\n    pass\n",
        "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef has_cycle(head):\n    slow = fast = head\n    while fast is not None and fast.next is not None:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            return True\n    return False\n",
        [{"name":"vuota","expression":"has_cycle(None)","expected":False},
         {"name":"valori uguali senza ciclo","expression":"has_cycle(ListNode(1,ListNode(1)))","expected":False},
         {"name":"ciclo a due nodi","expression":"(lambda a,b:(setattr(a,'next',b),setattr(b,'next',a),has_cycle(a))[-1])(ListNode(1),ListNode(2))","expected":True},
         {"name":"self loop","expression":"(lambda a:(setattr(a,'next',a),has_cycle(a))[-1])(ListNode(7))","expected":True}],
        "struct ListNode { int val; ListNode* next; };\nbool has_cycle(ListNode* head) { return false; }\n",
        "struct ListNode { int val; ListNode* next; };\nbool has_cycle(ListNode* head) {\n    auto* slow = head;\n    auto* fast = head;\n    while (fast && fast->next) {\n        slow = slow->next;\n        fast = fast->next->next;\n        if (slow == fast) return true;\n    }\n    return false;\n}\n",
        [{"name":"vuota","assertion":"!has_cycle(nullptr)"},
         {"name":"valori uguali senza ciclo","assertion":"[](){ListNode b{1,nullptr},a{1,&b};return !has_cycle(&a);}()"},
         {"name":"ciclo a due nodi","assertion":"[](){ListNode a{1,nullptr},b{2,&a};a.next=&b;return has_cycle(&a);}()"},
         {"name":"self loop","assertion":"[](){ListNode a{7,nullptr};a.next=&a;return has_cycle(&a);}()"}],
        ["Il confronto riguarda indirizzi o identità, non i valori.","Controlla fast e fast.next prima di fare due passi."],
        "Il veloce guadagna un passo sul lento a ogni iterazione. In un ciclo la distanza modulo la lunghezza diminuisce fino all'incontro; senza ciclo il veloce raggiunge la fine. O(n) tempo, O(1) spazio.",
    ),
    code_exercise(
        "clone-graph", "graphs", "Copiare una rete conservando le connessioni", "medium", 35,
        "BFS e mappa da identità originale a copia",
        "Copia profondamente la componente raggiungibile da node, fino a 100 nodi. Ogni Node ha val e neighbors. Valori duplicati, self-loop e vicini ripetuti sono ammessi: preserva identità, ordine e molteplicità degli archi. Nessun nodo della copia deve essere un originale. Per input nullo restituisci nullo; non modificare il grafo sorgente.",
        "class Node:\n    def __init__(self, val=0, neighbors=None):\n        self.val = val\n        self.neighbors = [] if neighbors is None else neighbors\n\ndef clone_graph(node):\n    pass\n",
        "from collections import deque\n\nclass Node:\n    def __init__(self, val=0, neighbors=None):\n        self.val = val\n        self.neighbors = [] if neighbors is None else neighbors\n\ndef clone_graph(node):\n    if node is None:\n        return None\n    copies = {node: Node(node.val)}\n    frontier = deque([node])\n    while frontier:\n        original = frontier.popleft()\n        for neighbor in original.neighbors:\n            if neighbor not in copies:\n                copies[neighbor] = Node(neighbor.val)\n                frontier.append(neighbor)\n            copies[original].neighbors.append(copies[neighbor])\n    return copies[node]\n",
        [{"name":"nullo","expression":"clone_graph(None)","expected":None},
         {"name":"ciclo e valori duplicati","expression":"(lambda a,b:(setattr(a,'neighbors',[b]),setattr(b,'neighbors',[a]),(lambda c:c is not a and c.val == 1 and c.neighbors[0].val == 1 and a.neighbors == [b] and b.neighbors == [a] and c.neighbors[0] is not b and c.neighbors[0] is not c and c.neighbors[0].neighbors[0] is c)(clone_graph(a)))[-1])(Node(1),Node(1))","expected":True},
         {"name":"self loop e archi ripetuti","expression":"(lambda a:(setattr(a,'neighbors',[a,a]),(lambda c:c is not a and c.val == 7 and a.val == 7 and a.neighbors == [a,a] and len(c.neighbors)==2 and all(n is c for n in c.neighbors))(clone_graph(a)))[-1])(Node(7))","expected":True}],
        "#include <vector>\nstruct Node { int val; std::vector<Node*> neighbors; };\nNode* clone_graph(Node* node) { return nullptr; }\n",
        "#include <queue>\n#include <unordered_map>\n#include <vector>\nstruct Node { int val; std::vector<Node*> neighbors; };\nNode* clone_graph(Node* node) {\n    if (!node) return nullptr;\n    std::unordered_map<Node*, Node*> copies;\n    copies[node] = new Node{node->val, {}};\n    std::queue<Node*> frontier;\n    frontier.push(node);\n    while (!frontier.empty()) {\n        auto* original = frontier.front();\n        frontier.pop();\n        for (auto* neighbor : original->neighbors) {\n            if (!copies.count(neighbor)) {\n                copies[neighbor] = new Node{neighbor->val, {}};\n                frontier.push(neighbor);\n            }\n            copies[original]->neighbors.push_back(copies[neighbor]);\n        }\n    }\n    return copies[node];\n}\n",
        [{"name":"nullo","assertion":"clone_graph(nullptr)==nullptr"},
         {"name":"ciclo e valori duplicati","assertion":"[](){Node a{1,{}},b{1,{&a}};a.neighbors={&b};auto*c=clone_graph(&a);bool ok=c&&c->val==1&&a.neighbors[0]==&b&&b.neighbors[0]==&a&&c!=&a&&c->neighbors.size()==1&&c->neighbors[0]!=&b&&c->neighbors[0]!=c&&c->neighbors[0]->neighbors[0]==c;return ok;}()"},
         {"name":"self loop e archi ripetuti","assertion":"[](){Node a{7,{}};a.neighbors={&a,&a};auto*c=clone_graph(&a);return c&&c->val==7&&a.val==7&&a.neighbors.size()==2&&a.neighbors[0]==&a&&c!=&a&&c->neighbors.size()==2&&c->neighbors[0]==c&&c->neighbors[1]==c;}()"}],
        ["Crea la copia prima di espandere i vicini: anche un ciclo troverà già il nodo.","La chiave della mappa è il nodo originale, non val."],
        "Ogni nodo viene creato e accodato una volta; ogni arco viene copiato una volta. O(V+E) tempo e O(V) spazio ausiliario oltre al grafo copiato. In C++ la copia appartiene al chiamante: in un'applicazione completa occorre una strategia di ownership e rilascio per tutta la componente, anche in presenza di cicli.",
    ),
])

FLASHCARD_TOPICS = [
("fondamenti", [
("Che cosa descrive O(1)?","Un numero di operazioni che non cresce con n nel modello considerato."),("Che cosa descrive O(log n)?","Un processo che riduce ripetutamente la dimensione del problema, come la ricerca binaria."),("Come cresce spesso un doppio ciclo completo?","O(n²); verifica quante volte gira ciascun ciclo rispetto ai vincoli."),("Quanto costa un sort comparativo standard?","O(n log n) nel caso usuale."),("Che cosa significa spazio ausiliario?","Memoria aggiuntiva oltre all'input e oltre all'output richiesto."),("Quando può essere adeguato O(n²)?","Con vincoli piccoli o quando il numero di confronti resta contenuto."),("Che tradeoff offre una HashMap?","Lookup medio O(1) pagando memoria proporzionale ai dati e perdendo l'ordine."),("Perché leggere i constraints prima di scrivere?","Per scegliere un costo compatibile e chiarire limiti, duplicati e valori ammessi."),("Quali edge case controllare spesso?","Vuoto/minimo, un elemento, duplicati, valori limite e nessuna soluzione."),("Cosa cambia raddoppiando n in O(n log n)?","Il lavoro cresce un po' più del doppio, non quattro volte come in O(n²)."),
]),
("fondamenti", [
("Ultimo indice di una lista lunga n?","n-1 quando n>0; per la lista vuota non esiste indice valido."),("Che cosa significa [left,right)?","Include left ed esclude right; la lunghezza è right-left."),("Quando modificare l'input in-place?","Quando il contratto lo consente e riduce spazio o semplifica l'algoritmo."),("Che rischio ha copiare una matrice grande?","Picco di memoria O(RC) aggiuntivo."),("Come calcolare la somma di un intervallo da prefix sum?","prefix[right] - prefix[left] per l'intervallo semiaperto [left,right)."),("Perché evitare sorting per una semplice membership?","Sort costa O(n log n); un set dà lookup medio O(1)."),("Che cos'è un ordinamento stabile?","Chiavi uguali mantengono il loro ordine relativo di partenza."),("Byte e carattere Unicode coincidono sempre?","No: encoding, code point e carattere percepito possono differire."),("Che cosa va dichiarato per una funzione che muta?","Quali oggetti cambia e se restituisce anche un nuovo valore."),("Quando range-for C++ è preferibile a un indice?","Quando serve ogni valore e non la sua posizione."),
]),
("fondamenti", [
("Che cosa conserva Two Sum?","Valori già visti e i loro indici per trovare un complemento con lookup."),("Perché cercare il complemento prima di inserire il valore corrente?","Per non usare lo stesso indice due volte."),("Set o mappa frequenze?","Set per appartenenza; mappa quando servono conteggi o dati associati."),("Chiave canonica per anagrammi?","Caratteri ordinati oppure tuple delle frequenze per lettera."),("Complessità media di lookup hash?","O(1), con O(n) nel caso peggiore teorico."),("map vs unordered_map in C++?","map ordina e costa O(log n); unordered_map usa hashing con costo medio O(1)."),("Quale chiave usare nella mappa di Clone Graph?","Identità del nodo originale: valori uguali possono appartenere a nodi diversi."),("Quando usare Counter?","Per contare frequenze, mantenendo comunque consapevolezza dei passaggi e del costo."),("Che effetto ha unordered_map::operator[] su chiave assente?","Inserisce il valore default; find non muta il contenitore."),("Perché inizializzare prefix map con {0:1}?","Per contare i segmenti che partono dall'indice zero."),
]),
("pattern", [
("Quando due puntatori agli estremi eliminano candidati?","Quando l'ordinamento giustifica quale lato non può contenere la risposta."),("Quando sliding window sulle somme è monotona?","Quando i valori sono non negativi e togliere un valore non aumenta la somma."),("Perché la stessa finestra fallisce con valori negativi?","Restringere il bordo può aumentare la somma, quindi la proprietà non è monotona."),("Che cosa indica slow nella deduplicazione?","Fine del prefisso già ripulito e senza ripetizioni."),("Come aggiornare una finestra fissa?","Aggiungi il nuovo elemento e sottrai quello che è uscito."),("Quale stato aiuta longest substring unique?","L'ultimo indice osservato di ciascun carattere."),("Quale equazione trova subarray sum k?","prefix_corrente - prefix_precedente = k."),("Come trovare una finestra minima valida?","Mentre è valida, restringi a sinistra e aggiorna la migliore."),("Quando aggiornare la frequency map?","Nella stessa operazione in cui un elemento entra o esce dalla finestra."),("Quanto spazio richiedono due puntatori semplici?","O(1) se conservano solo indici e contatori."),
]),
("pattern", [
("Qual è il primo passo per unire intervalli?","Ordinare per start e confrontare ogni intervallo con l'ultimo fuso."),("Quando due intervalli semiaperti adiacenti si sovrappongono?","[a,b) e [b,c) non si sovrappongono; decide il contratto specifico."),("Come risolvere Insert Interval in O(n)?","Copiare prefisso, fondere gli overlap e aggiungere il suffisso ordinato."),("Che cosa riassume un prefix sum?","La somma cumulativa di un prefisso."),("Quanti array extra usa product-except-self con spazio costante?","Nessuno oltre l'output: prefisso e suffisso si accumulano separatamente."),("Che cosa assume Boyer-Moore majority?","Un valore compare più di n/2 volte."),("Qual è l'invariante di Kadane?","current è il miglior segmento che termina nella posizione corrente."),("Perché ordinare per distanza al quadrato?","La radice quadrata non cambia l'ordine delle distanze."),("Quando motivare un greedy?","Quando si afferma che la scelta locale preserva un ottimo globale."),("Quale argomento giustifica scegliere l'intervallo che finisce prima?","Sostituirlo al primo intervallo di un ottimo lascia almeno altrettanto spazio ai successivi."),
]),
("ricerca", [
("Perché binary search richiede ordinamento o monotonia?","Il confronto deve permettere di scartare metà dei candidati senza perdere la risposta."),("Ricerca valore vs lower_bound?","La prima cerca un valore; lower_bound trova il primo indice con valore >= target."),("Come calcolare mid evitando overflow?","left + (right-left)/2."),("Quale intervallo usa spesso first_true?","Semiaperto [left,right), con right=n ammesso come sentinella."),("Che cosa significa binary search on answer?","Cercare una soglia usando un test di fattibilità monotono."),("Cosa resta ordinato in un array ruotato distinto?","Almeno una metà intorno a mid."),("Come trovare primo e ultimo duplicato?","Cerca il primo >= target e il primo > target."),("Qual è il rischio di vector::size() con int?","È unsigned; confronti misti o sottrazioni possono avvolgersi."),("Che invariante aiuta una ricerca di confine?","Il confine minimo valido resta nell'intervallo candidato."),("Quando termina una ricerca semiaperta?","Quando left==right e il confine è determinato."),
]),
("ricerca", [
("Quale struttura modella aperture di parentesi?","Stack LIFO: l'ultima apertura deve chiudersi per prima."),("Perché deque per BFS in Python?","popleft è O(1); list.pop(0) sposta i rimanenti."),("Che cosa conserva uno stack monotono?","Candidati la cui risposta non è ancora stata determinata, mantenuti in ordine."),("Quando Daily Temperatures risolve una entry?","Quando arriva una temperatura più alta e l'indice in cima attendeva quella risposta."),("Che cosa contiene la coda all'inizio di un livello BFS?","Nodi alla stessa distanza dalla sorgente."),("A cosa serve deque oltre a una coda?","Consente aggiunta e rimozione efficienti a entrambe le estremità."),("Che costo ammortizzato ha lo stack in Daily Temperatures?","O(n), ciascun indice entra ed esce al massimo una volta."),("Perché valid parentheses controlla stack vuoto alla fine?","Per rilevare aperture rimaste senza chiusura."),("Come si configura una min-priority_queue C++?","priority_queue<T, vector<T>, greater<T>>."),("Perché un istogramma aggiunge spesso una barra sentinella zero?","Per scaricare dallo stack anche le altezze crescenti rimaste."),
]),
("strutture", [
("Tre puntatori per invertire una lista?","previous, current e next salvato prima di sovrascrivere il link."),("Come Floyd trova un ciclo con O(1) spazio?","slow fa un passo e fast due; in un ciclo prima o poi coincidono."),("Perché un dummy node semplifica merge list?","Rende uniforme la creazione della testa e dei successivi."),("Profondità di un sottoalbero nullo?","Zero nodi."),("Che ordine produce inorder su un BST valido?","Valori crescenti: sinistra, nodo, destra."),("Perché BST validation richiede limiti globali?","Un discendente deve rispettare anche gli antenati, non solo il genitore diretto."),("Diametro di un albero: unità?","Numero di archi sul cammino semplice più lungo."),("Che cosa restituisce una DFS postorder per il diametro?","L'altezza del ramo; la somma delle due altezze aggiorna il diametro locale."),("Spazio BFS di un albero?","O(w), w larghezza massima del livello."),("Quando ricorsione sugli alberi è naturale?","Quando il risultato si combina dalle risposte dei figli con un caso base chiaro."),
]),
("strutture", [
("Come rappresentare un grafo sparso?","Adjacency list: una collezione di vicini per nodo."),("Quando segnare visited?","Quando un nodo entra in frontiera, per non accodarlo più volte."),("Come contare le componenti connesse?","Partire da ogni nodo non visitato e incrementare il conteggio di una DFS/BFS."),("Costo di BFS su adjacency list?","O(V+E) tempo e O(V+E) memoria per grafo e stato."),("Che cos'è indegree?","Numero di archi diretti che entrano in un nodo."),("Come Kahn rileva un ciclo?","Se elabora meno di V nodi, restano nodi con dipendenze cicliche."),("Quando BFS trova cammini minimi?","In un grafo non pesato, perché visita per distanza crescente."),("Che algoritmo usare con pesi non negativi?","Dijkstra con un min-heap."),("Perché Dijkstra non gestisce pesi negativi?","Una distanza estratta potrebbe poi essere migliorata da un cammino negativo."),("Come inizializzare una BFS multi-source?","Accodare tutte le sorgenti con distanza zero prima della visita."),
]),
("avanzato", [
("Come kth-largest con min-heap k?","Mantieni i k valori maggiori visti; la cima minima è il k-esimo."),("Costo top-k con heap limitato?","O(n log k), più il conteggio frequenze quando richiesto."),("Come rendere deterministico un pareggio?","Aggiungere esplicitamente una seconda chiave al comparatore."),("Qual è un greedy per intervalli compatibili?","Ordinare per fine crescente e prendere il prossimo intervallo compatibile."),("Come generare subsets?","Per ogni elemento, esplorare il caso incluso e quello saltato."),("Come evitare permutazioni duplicate in Combination Sum?","Ordinare e ricorrere dallo stesso indice consentendo riuso controllato."),("Che cos'è backtracking?","Esplorare una scelta, poi annullarla prima del ramo successivo."),("Perché permutazioni costano almeno n!?","L'output contiene n! ordini possibili."),("Quale coppia risolve top-k frequent?","HashMap per conteggi e heap/sort per priorità."),("Quando promuovere a int64 in C++?","Prima di moltiplicare valori che potrebbero superare la capienza di int."),
]),
("avanzato", [
("Che cosa sono sottoproblemi sovrapposti?","Stati uguali ricalcolati da più percorsi ricorsivi."),("Memoization vs tabulation?","Memoization salva le richieste ricorsive; tabulation riempie gli stati bottom-up."),("Ricorrenza Climbing Stairs?","ways[n]=ways[n-1]+ways[n-2], con basi definite dal contratto."),("Ricorrenza House Robber?","max(best[i-1], value[i]+best[i-2])."),("Come indicare importo irraggiungibile in Coin Change?","Un sentinel maggiore del massimo conteggio valido e controllo finale."),("Che significa dp[end] in Word Break?","Il prefisso fino a end è segmentabile con parole del dizionario."),("Quali operazioni compongono edit distance?","Inserimento, eliminazione e sostituzione."),("Quando comprimere una tabella DP?","Quando gli stati dipendono solo da una o poche righe precedenti."),("Quale domanda apre una DP?","Quale stato riassuntivo e quali stati precedenti consentono la decisione?"),("Perché definire le basi prima del loop?","Per rendere esplicito il caso vuoto e prevenire indici non validi."),
]),
("linguaggi", [
("Quando usare enumerate in Python?","Quando servono indice e valore nella stessa scansione."),("list e tuple: differenza pratica?","list mutabile; tuple immutabile e usabile come chiave se i membri sono hashable."),("Che costo ha s[::-1]?","Crea una nuova stringa/lista, quindi O(n) memoria."),("sorted(x) vs x.sort()?","sorted crea una nuova lista; sort modifica la lista esistente."),("Come leggere una frequenza mancante con Counter?","Counter restituisce zero per una chiave assente senza richiedere un ramo separato."),("Come simulare max-heap con heapq?","Inserire numeri negati e invertire il segno al prelievo."),("Perché defaultdict(list)?","Evita il ramo di inizializzazione di una lista per ogni chiave."),("Perché non affidarsi sempre a `x or fallback`?","Zero, stringa vuota e False sono falsy ma possono essere valori validi."),("Quando evitare una comprehension?","Quando la logica multi-step diventa meno leggibile di un ciclo esplicito."),("Che cosa fa zip?","Accoppia sequenze in parallelo e si ferma alla più corta."),
]),
("linguaggi", [
("Quale header C++ fornisce sort?","<algorithm>."),("Quale header contiene accumulate?","<numeric>."),("Quale header definisce INT_MAX?","<climits>."),("Come passare un vector grande in sola lettura?","const vector<T>& per evitare copia e mutazione attraverso il parametro."),("Perché const auto& nel range-for?","Evita copie di elementi e impedisce modifiche accidentali."),("Che valore rappresenta nullptr?","Nessun oggetto puntato valido."),("Quale contenitore fornisce lookup hash?","unordered_map o unordered_set."),("Quale contenitore ha ordine e costo logaritmico?","map o set."),("A cosa serve upper_bound in C++?","Trova il primo elemento strettamente maggiore del valore in un range ordinato."),("A cosa serve lower_bound?","Trova il primo elemento >= valore in un range ordinato."),
]),
("repository", [
("Da dove iniziare in una repository sconosciuta?","README, package/CMake manifest, cartelle e comando test."),("Che cosa annotare per un test fallito?","Input, expected, actual e primo frame applicativo utile."),("Che rischio ha una Promise non awaited?","Il chiamante riceve l'oggetto Promise anziché il valore risolto."),("Il frame del test identifica sempre la causa?","No: spesso la causa sta in un componente a monte del punto osservato."),("Che cosa fa un fix minimo?","Cambia il comportamento responsabile preservando i contratti non coinvolti."),("Perché rieseguire tutta la suite?","Una correzione locale può rompere una regressione coperta altrove."),("Come leggere uno stack trace?","Trova il primo frame del codice applicativo e risali al percorso chiamante."),("Quale script lancia i test Node del lab?","`npm test`, dichiarato in package.json."),("Cosa controllare per API C++ modificata?","Header, definizione, call sites, include e test che compilano tutti i source."),("Perché testare input non mutato?","Una lettura side-effect può alterare chiamate successive o cache condivise."),
]),
("repository", [
("Prompt AI utile per seguire il flusso?","Chiedi di spiegare route → service → repository senza modificare il codice."),("A cosa serve citare @README.md?","A collegare il requisito documentato a una funzione specifica senza chiedere il fix completo."),("Come formulare un'ipotesi verificabile?","Il test vuole ID esatto, mentre il repository usa un confronto di soglia."),("Come usare AI su uno stack trace?","Chiedere cosa indica il frame, poi verificare nel codice e nei test."),("Rischio di accettare una patch AI ampia?","Può cambiare API, introdurre regressioni o risolvere un sintomo diverso."),("Workflow minimo di debugging?","Brief, test, expected/actual, ipotesi, modifica piccola, suite di regressione."),("A cosa serve IntelliSense nel repository OA?","Navigare firme e definizioni; non decide quale comportamento è corretto."),("Quando chiedere aiuto di sintassi?","Quando la causa è chiara ma un costrutto o un'API blocca la verifica."),("Come restare owner con un AI Assistant?","Tenere propria ipotesi, leggere il diff e validare la soluzione con i test."),("Quale prova segue un suggerimento AI?","Eseguire test e confrontare il risultato col contratto del README."),
]),
("comportamento", [
("Customer Obsession in pratica?","Partire dall'effetto sul cliente e verificare l'impatto con evidenze."),("Ownership in pratica?","Seguire il problema fino a una soluzione e coordinarsi oltre i confini quando serve."),("Dive Deep in pratica?","Passare dal sintomo a dati e meccanismo causale."),("Earn Trust in pratica?","Dire chiaramente ciò che si sa, rispettare impegni e riconoscere incertezze o errori."),("Have Backbone; Disagree and Commit?","Dissentire con rispetto e prove, poi sostenere la decisione condivisa."),("Bias for Action?","Agire rapidamente quando il costo dell'attesa è reale e la scelta è reversibile."),("Learn and Be Curious?","Cercare contesto e aggiornare una convinzione quando arrivano nuove prove."),("Insist on the Highest Standards?","Ridurre difetti ricorrenti invece di accettare qualità bassa come normale."),("Invent and Simplify?","Rimuovere passaggi senza perdere il risultato utile per chi usa il sistema."),("Come affrontare Work Style?","Leggere la frase intera e rispondere in coerenza con il proprio comportamento reale."),
]),
]


def build_flashcards():
    cards=[]
    for module,items in FLASHCARD_TOPICS:
        for question,answer in items:
            cards.append({"id":f"sde-fc-{len(cards)+1:03d}","module":module,"question":question,"answer":answer})
    return cards
LABS = [
 {"id":"lab-amazon-cpp-demo","module":"repository","title":"Repository di esempio · C++","minutes":25,"difficulty":"base","description":"Progetto CMake essenziale con header, sorgente e test. Segui la firma della funzione fino al risultato osservato.","requirements":["Leggi README, header e test prima di aprire il sorgente.","Confronta il risultato atteso con quello ottenuto.","Correggi il filtro degli elementi attivi e la ricerca per ID esatto.","Restituisci `optional` quando l'ID non esiste."],"rubric":["Correzione nel file sorgente appropriato","Casi attivo, inattivo e ID assente coperti","API invariata oltre le modifiche richieste"],"workspace_template":"amazon_cpp"},
 {"id":"lab-amazon-node-demo","module":"repository","title":"Repository di esempio · Node.js","minutes":25,"difficulty":"base","description":"Progetto equivalente a quello C++ in moduli JavaScript: filtro, ricerca e test, senza pacchetti esterni.","requirements":["Individua `package.json`, esportazioni e test.","Esegui `npm test` prima di modificare i file.","Correggi il predicato e il confronto dell'identificativo.","Mantieni la funzione di lettura senza modificare i dati."],"rubric":["Dati iniziali preservati","ID confrontato esattamente e assenza gestita","Tutti i test previsti superati"],"workspace_template":"amazon_node"},
 {"id":"lab-amazon-node-async","module":"repository","title":"Repository asincrona · Promise e controller","minutes":35,"difficulty":"intermedio","description":"Una route usa un repository asincrono. Segui il dato tra controller, servizio e test; distingui una `Promise`, un risultato assente (`null`) e lo status HTTP.","requirements":["Traccia il flusso route → servizio → repository.","Attendi il risultato prima di controllare se il profilo esiste.","Restituisci 404 per un profilo assente e 200 per uno trovato.","Inserisci nel body il valore restituito dal repository."],"rubric":["Errore asincrono riprodotto","Risposte 200 e 404 distinte","Modifica limitata al contratto richiesto"],"workspace_template":"amazon_node"},
 {"id":"lab-amazon-cpp-inventory","module":"repository","title":"Inventario · indici e riferimenti in C++","minutes":40,"difficulty":"intermedio","description":"Due file sorgente e due header condividono un vettore di articoli e un servizio che ne conta le unità.","requirements":["Controlla l'indice prima di chiamare `erase`: `size` indica il numero di elementi.","Cerca l'ID esatto, non il primo ID maggiore.","Segui `total_units` dalla dichiarazione alla definizione.","Se la rimozione viene rifiutata, lascia invariati i dati."],"rubric":["Nessun accesso oltre i limiti del vettore","Header e sorgente coerenti","Test sull'ultimo indice e su `index == size`"],"workspace_template":"amazon_cpp"},
 {"id":"lab-amazon-node-contract","module":"repository","title":"Ordini · filtro e contratto API","minutes":45,"difficulty":"intermedio","description":"Servizio e controller condividono righe d'ordine, stato, ordinamento e risposta 404. I test controllano anche che i dati non vengano modificati.","requirements":["Confronta test, servizio e controller.","Calcola totale e numero di righe secondo il contratto.","Includi soltanto lo stato richiesto e conserva l'ordine iniziale.","Distingui un ordine assente da uno vuoto e restituisci lo status corretto."],"rubric":["Dati in ingresso invariati","Status HTTP e JSON coerenti","Test sui casi limite e sull'ordine"],"workspace_template":"amazon_node"},
 {"id":"lab-amazon-mock-repository","module":"repository","title":"Debugging di un progetto · stato delle spedizioni","minutes":60,"difficulty":"hard","description":"Prova multi-file su route, servizio e repository. README e test descrivono il comportamento; dovrai individuare tu i file con i difetti.","requirements":["Esegui `npm test` prima di intervenire.","Per ogni errore annota il risultato atteso, quello ottenuto e il percorso seguito dal dato.","Formula un'ipotesi verificabile, applica una modifica circoscritta e conserva i contratti esistenti.","Ripeti i test e controlla i comportamenti vicini a quello corretto."],"rubric":["Tutti i test di accettazione superati","Regressioni coperte da test","Modifiche circoscritte e comprensibili","Nessun nuovo effetto collaterale"],"workspace_template":"amazon_node","repository_variants":{"node":"amazon_node","cpp":"amazon_cpp"}},
]

SIMULATIONS = [
 {"id":"sde-sim-coding-25","title":"Problema di coding · 25 min","minutes":25,"kind":"coding","coding_exercise_id":"sde-e-longest-substring","brief":"Risolvi un problema in un singolo file. Chiarisci il contratto, scegli una struttura dati e lascia tempo per provare almeno un caso limite. Durante il timer non sono disponibili indizi o soluzione.","checklist":["Leggi input, output e vincoli","Prova un esempio a mano","Scrivi una soluzione autonoma","Controlla duplicati e valore minimo","Descrivi tempo e spazio richiesti"]},
 {"id":"sde-sim-coding-40","title":"Problema di coding · 40 min","minutes":40,"kind":"coding","coding_exercise_id":"sde-e-coin-change","brief":"Risolvi un problema di algoritmi in un singolo file. Il controllo esegue il codice sui casi previsti; durante la prova non consultare gli indizi, la navigazione web o la soluzione.","checklist":["Definisci gli stati o l'invariante","Implementa senza assistenza","Esegui i test disponibili","Confronta costo e vincoli","Fermati al timer"]},
 {"id":"sde-sim-repository-60","title":"Debugging di una repository · 60 min","minutes":60,"kind":"repository","repository_lab_id":"lab-amazon-mock-repository","brief":"Esamina una repository che non conosci. Parti da README e test, ricostruisci il flusso tra route, servizi e repository, poi verifica ogni correzione con la suite.","checklist":["Leggi README e struttura dei file","Esegui `npm test`","Raggruppa gli errori per contratto","Verifica un'ipotesi alla volta","Esegui di nuovo tutta la suite"]},
 {"id":"sde-full-mock","title":"Simulazione completa · problema 40 + progetto 60","minutes":100,"kind":"full_mock","coding_exercise_id":"sde-e-three-sum","repository_lab_id":"lab-amazon-mock-repository","brief":"Due sezioni consecutive: 40 minuti per un problema di algoritmi, poi 60 minuti per un progetto multi-file. Il tempo non utilizzato nella prima sezione non si aggiunge alla seconda.","checklist":["Avvia quando sei pronto","Risolvi il problema senza aiuti","Il primo timer si ferma al cambio di sezione","Leggi README e test del progetto","Alla fine annota prove raccolte e dubbi rimasti"]},
]

SCENARIO_SEEDS = [
 ("Errore nella rotta checkout","Dopo il rilascio, una parte delle richieste checkout riceve 500. I log sono incompleti e i ticket aumentano.","Dive Deep · Customer Obsession · Bias for Action","contenere il checkout e isolare le richieste coinvolte","ABCD"),
 ("Dati associati al cliente sbagliato","Un cliente invia uno screenshot con un record di un altro account. Cache e filtro service sono entrambe ipotesi possibili.","Customer Obsession · Ownership · Earn Trust","ridurre l'esposizione e provare il confine tenant","ABCD"),
 ("Requisito urgente ma vago","Il ticket chiede di ridurre i passaggi dell'onboarding senza dire per quali utenti o quale metrica deve cambiare.","Customer Obsession · Are Right, A Lot · Bias for Action","chiarire l'esito e validare un flusso osservabile","BCAD"),
 ("Review su query lenta","Una review contesta una query che passa sui dati locali; in produzione la tabella è centinaia di volte più grande.","Dive Deep · Insist on the Highest Standards · Learn and Be Curious","confrontare piano e distribuzione dati con una misura riproducibile","BACD"),
 ("Disaccordo durante un incident","Un collega propone cache; tu sospetti un filtro incompleto. Il servizio è degradato ma disponibile.","Have Backbone; Disagree and Commit · Earn Trust · Dive Deep","confrontare le ipotesi in modo rapido e misurabile","ABCD"),
 ("Migrazione con rollback difficile","La correzione richiede schema change irreversibile nella finestra corrente; un workaround manuale limita l'impatto.","Ownership · Bias for Action · Insist on the Highest Standards","bilanciare contenimento reversibile e rischio della migrazione","ACBD"),
 ("Hotfix con duplicazione","L'hotfix ha ripristinato il flusso ma la stessa regola è ora copiata in due service. Il rilascio successivo è fra giorni.","Ownership · Invent and Simplify · Deliver Results","stabilizzare la correzione e pianificare il refactor con copertura","CABD"),
 ("Test intermittente in CI","Un test fallisce uno run su dieci. Il merge è bloccato e il gruppo propone di rilanciare finché diventa verde.","Insist on the Highest Standards · Dive Deep · Ownership","catturare stato condiviso, race o dipendenza instabile","BACD"),
 ("Rollback o patch","Una release ha aumentato la latenza solo per un tipo di richiesta. Il rollback è sicuro; la patch richiede una verifica mirata.","Bias for Action · Customer Obsession · Are Right, A Lot","ridurre l'impatto con decisione reversibile e dati tempestivi","ABCD"),
 ("Job dipendente da un altro team","Un endpoint gestito da un team vicino restituisce payload incompleti. L'owner non è raggiungibile nel canale usuale.","Ownership · Earn Trust · Deliver Results","raccogliere evidenze, mitigare il chiamante e trovare l'owner","BACD"),
 ("Richiesta di ETA certa","Una direzione chiede quando sarà chiuso un bug non ancora riprodotto. L'impatto è circoscritto ma visibile.","Earn Trust · Ownership · Customer Obsession","comunicare ciò che sai e concordare il prossimo update","CBAD"),
 ("Metriche contro l'intuizione","Una feature pensata per aumentare l'adozione coincide con un calo in una coorte piccola, durante una campagna parallela.","Are Right, A Lot · Dive Deep · Learn and Be Curious","segmentare e verificare cause alternative prima di estendere la feature","ACBD"),
 ("Errore introdotto da te","Scopri che una tua modifica esclude un segmento dai risultati. Il deploy è stato fatto da poco.","Ownership · Earn Trust · Customer Obsession","rendere visibile il problema e ripristinare il percorso cliente","ACBD"),
 ("Delete senza policy chiara","Il ticket chiede di eliminare account inattivi, ma retention, audit e recupero non sono specificati. È già pronta una query DELETE.","Customer Obsession · Insist on the Highest Standards · Dive Deep","fermare l'azione irreversibile e chiarire il contratto dati","ABCD"),
 ("Pull request troppo ampia","Una PR unisce refactor, API nuova e migrazione. I test passano, ma non è chiaro come isolare o annullare un errore.","Invent and Simplify · Insist on the Highest Standards · Deliver Results","ridurre la superficie e rendere leggibile il rollback","ABCD"),
 ("Edge case segnalato da una persona junior","Una revisora junior nota che ID zero viene interpretato come assente. I dati di test attuali non contengono zero.","Learn and Be Curious · Insist on the Highest Standards · Earn Trust","verificare il contratto e ringraziare per l'esempio concreto","ABCD"),
 ("Accessibilità contro la data di lancio","La navigazione da tastiera è bloccata in un passaggio usato dai clienti; il redesign dovrebbe uscire oggi.","Customer Obsession · Insist on the Highest Standards · Bias for Action","stimare l'impatto e rendere il flusso utilizzabile prima del rilascio","ACBD"),
 ("Provider esterno in timeout","Una dipendenza talvolta supera il timeout e blocca una richiesta interna. Il provider dichiara servizio sano.","Dive Deep · Ownership · Invent and Simplify","separare il guasto esterno dall'effetto sul chiamante e applicare limiti","BACD"),
]
SCENARIO_SEEDS += [
 ("Script operativo manuale","Ogni mattina un collega copia dati fra due sistemi per mezz'ora; errori di trascrizione sono già arrivati ai clienti.","Customer Obsession · Invent and Simplify · Bias for Action","osservare i passaggi e automatizzare il più rischioso","ABCD"),
 ("Due responsabili, una priorità","Due responsabili chiedono nello stesso pomeriggio modifiche incompatibili alla stessa rotta.","Ownership · Earn Trust · Deliver Results","esplicitare impatto e costo e ottenere una priorità condivisa","CBAD"),
 ("Duplicati dopo import","Un job ha creato duplicati in alcuni record. Non sai ancora se il processo sia stato avviato più di una volta.","Dive Deep · Ownership · Insist on the Highest Standards","fermare ulteriori duplicazioni e misurare l'estensione prima della pulizia","ABCD"),
 ("Allarme ignorato dal team","Un alert si attiva spesso senza impatto reale; il gruppo ha iniziato a ignorarlo. Un nuovo avviso arriva in una finestra critica.","Ownership · Insist on the Highest Standards · Customer Obsession","corroborare l'allarme con segnali indipendenti e correggerne la causa del rumore","BACD"),
 ("Race condition intermittente","Il bug non si riproduce con una richiesta; due richieste simultanee possono perdere un aggiornamento.","Dive Deep · Insist on the Highest Standards · Learn and Be Curious","riprodurre la concorrenza e localizzare la mutazione condivisa","BACD"),
 ("Producer e consumer fuori sincrono","Un campo API è stato rinominato; un consumer distribuito usa ancora il nome precedente.","Ownership · Earn Trust · Deliver Results","ripristinare compatibilità e coordinare un cambio a fasi","BCAD"),
 ("Caso raro lingua e fuso","Una persona segnala un errore solo con una lingua e un fuso orario specifici; le metriche globali restano normali.","Customer Obsession · Learn and Be Curious · Dive Deep","riprodurre la combinazione e misurare l'impatto per quel segmento","ABCD"),
 ("Pipeline E2E instabile durante incident","Il fix è piccolo, i test unitari sono verdi e il test end-to-end dipende da un servizio di test intermittente. L'impatto continua.","Bias for Action · Insist on the Highest Standards · Ownership","usare evidenza mirata, comunicare il rischio residuo e mitigare","ABCD"),
 ("Metriche con denominatori diversi","La tua query e quella di un collega danno tassi d'errore diversi perché contano richieste e utenti distintamente.","Have Backbone; Disagree and Commit · Are Right, A Lot · Dive Deep","allineare definizioni e campioni prima della decisione","BCAD"),
 ("Richiesta di togliere una feature flag","La flag aggiunge un ramo lento e il team vorrebbe eliminarla; protegge ancora una migrazione in corso.","Insist on the Highest Standards · Ownership · Customer Obsession","misurare costo e rischio e rimuoverla solo dopo aver verificato la migrazione","BACD"),
 ("Difetto UI di un altro gruppo","Un componente esterno blocca il completamento di un'operazione. L'owner è un'altra squadra e la release è vicina.","Ownership · Customer Obsession · Earn Trust","produrre una riproduzione e coordinare un workaround con l'owner","ACBD"),
 ("La nuova evidenza invalida la soluzione iniziata","Hai già scritto metà del fix; una prova con dati realistici mostra che l'ipotesi iniziale era falsa.","Are Right, A Lot · Learn and Be Curious · Ownership","aggiornare la decisione e condividere la prova prima di proseguire","ABCD"),
 ("Limite API non documentato","Un cliente raggiunge una soglia non citata nella guida pubblica, ma applicata dal server.","Customer Obsession · Think Big · Earn Trust","ripristinare un percorso funzionante e correggere insieme contratto e documentazione","ABCD"),
 ("Batch di pulizia con finestra breve","Il job notturno ha pochi minuti; record aggiornati mentre gira possono essere saltati o elaborati due volte.","Insist on the Highest Standards · Dive Deep · Ownership","definire idempotenza, checkpoint e conteggi prima dell'esecuzione","BACD"),
 ("Feature consegnata ma poco usata","Il team ha rispettato la data ma pochi utenti usano la funzione. La proposta è aggiungere altre opzioni senza osservare il flusso.","Customer Obsession · Think Big · Learn and Be Curious","capire bisogno e punto di abbandono prima di ampliare lo scope","ABCD"),
 ("Regressione dopo refactor","La suite passava prima; ora un input di confine fallisce. Il codice è più breve, ma la regressione è riproducibile.","Insist on the Highest Standards · Ownership · Dive Deep","ripristinare il contratto e isolare la modifica responsabile","ABCD"),
 ("Interruzione durante consegna","Una dipendenza critica chiede supporto mentre stai chiudendo un lavoro con scadenza oggi.","Ownership · Deliver Results · Earn Trust","valutare gravità e tempo necessario e concordare copertura per entrambe le attività","CBAD"),
 ("Stima accettata senza verificare un'assunzione","In retrospettiva emerge che una tua stima assumeva una API che non esisteva; il team ha perso due giorni.","Ownership · Learn and Be Curious · Earn Trust","riconoscere il passaggio mancato e introdurre una prova tecnica nelle stime","CBAD"),
]


def build_scenarios():
    actions={
      "incident": {
       "A":("Usa un feature flag per isolare il percorso impattato e controlla subito se il tasso d'errore cambia.","Una mitigazione circoscritta limita l'impatto e resta reversibile mentre l'indagine prosegue."),
       "B":("Confronta trace riuscite e fallite e riproduci una richiesta con lo stesso contesto.","La differenza fra due richieste simili aiuta a localizzare la regressione senza allargare il fix."),
       "C":("Avvisa l'on-call e il supporto con l'impatto osservato, l'azione temporanea e l'ora del prossimo aggiornamento.","Le persone coinvolte possono coordinare assistenza e diagnosi senza scambiare un'ipotesi per una causa certa."),
       "D":("Valuta il rollback dell'intera release confrontando prima quali altri cambiamenti contiene.","Il rollback può essere corretto, ma rimuovere modifiche non correlate può introdurre un secondo impatto."),
      },
      "rollback_patch": {
       "A":("Attiva il rollback già verificato e controlla subito la latenza per il tipo di richiesta coinvolto.","Una mitigazione sicura riduce l'impatto mentre la verifica della patch continua."),
       "B":("Riproduci la richiesta lenta e verifica la patch su dati rappresentativi prima di proporla.","Una prova mirata mostra se la modifica affronta il caso senza introdurre un'altra regressione."),
       "C":("Condividi l'ambito del rollback, l'owner della patch e quando deciderete se applicarla.","Ruoli e prossimo checkpoint rendono chiaro il percorso dopo il ripristino."),
       "D":("Prova la patch su una piccola coorte e controlla la latenza prima di decidere se effettuare il rollback.","Una canary limita il rischio della patch, ma prolunga l'impatto quando esiste già un rollback verificato."),
      },
      "hotfix_followup": {
       "A":("Aggiungi un test di regressione in entrambi i servizi e un caso adiacente prima di consolidare la logica duplicata.","La copertura stabilisce il comportamento atteso prima di cambiare struttura dopo l'hotfix."),
       "B":("Concorda con l'owner una funzione condivisa, il contratto e il momento in cui affrontarla.","Un refactor coordinato può ridurre la duplicazione senza sorprendere chi mantiene l'altro servizio."),
       "C":("Mantieni stretto l'hotfix e assegna il refactor a un follow-up con owner e test concordati.","Separare urgenza e pulizia limita il rischio immediato senza perdere il miglioramento strutturale."),
       "D":("Consolida ora la regola in una funzione condivisa e usa i test esistenti per controllare i due servizi.","La pulizia riduce divergenze future, ma i test esistenti potrebbero non coprire il caso che ha richiesto l'hotfix."),
      },
      "customer_data": {
       "A":("Blocca temporaneamente la risposta che attraversa il confine fra clienti e verifica che l'esposizione si fermi.","Contenere l'accesso ha priorità quando dati di un cliente possono raggiungerne un altro."),
       "B":("Riproduci il caso con due tenant distinti e traccia identità, query e filtri fino alla risposta.","Una prova sul confine reale chiarisce se il difetto nasce da autorizzazione, cache o selezione dei dati."),
       "C":("Coinvolgi subito l'owner del servizio e chi gestisce l'incidente, descrivendo ciò che è confermato e ciò che manca.","Un'escalation tempestiva coordina la valutazione dell'impatto e conserva una comunicazione accurata."),
       "D":("Nascondi i record non propri nel client mentre lasci invariata la risposta del servizio.","Il filtro UI può ridurre un sintomo visibile, ma non ripara un confine di accesso lato server."),
      },
      "ambiguous": {
       "A":("Scrivi due esempi di accettazione e proponi l'interpretazione minima che puoi verificare oggi.","Un esempio concreto trasforma parole vaghe in un comportamento che prodotto e sviluppo possono controllare."),
       "B":("Chiedi quale esito osservabile conta di più e quale caso deve restare fuori dallo scope.","Chiarire il criterio evita di investire tempo in due interpretazioni entrambe plausibili."),
       "C":("Concorda un breve checkpoint e comunica la parte che puoi consegnare con sicurezza.","Il checkpoint mantiene il lavoro in movimento e rende visibile l'incertezza residua."),
       "D":("Prepara un prototipo delle due interpretazioni e chiedi a prodotto di scegliere durante la demo.","Il prototipo rende tangibili le alternative, ma può costare più tempo di due esempi di accettazione concordati subito."),
      },
      "performance": {
       "A":("Riproduci la query con un campione rappresentativo e confronta il piano prima di scegliere un indice.","Il piano e la distribuzione dei dati distinguono una scansione costosa da altre attese nel percorso."),
       "B":("Misura latenza e righe lette per i casi lenti, separando dimensione del dataset e forma della query.","Una misura segmentata prova dove si concentra il costo e rende confrontabili le ipotesi."),
       "C":("Lascia nella review il benchmark ripetibile e chiedi che un'eventuale ottimizzazione sia legata a quel risultato.","La review diventa verificabile e riduce il rischio che una modifica nasconda una regressione altrove."),
       "D":("Prova in staging un indice sulle colonne del filtro e confronta la latenza media della query.","La prova è reversibile e può aiutare, ma la media in staging potrebbe non rappresentare il segmento lento in produzione."),
      },
      "migration": {
       "A":("Esegui una prova di rollback su una copia aggiornata e registra il tempo necessario a ripristinare i dati.","La reversibilità va dimostrata prima della finestra, soprattutto se lo schema cambia in modo incompatibile."),
       "B":("Mappa quali versioni leggono e scrivono ogni campo durante il rollout e quali passaggi non sono reversibili.","La compatibilità fra producer e consumer determina se un rollout graduale può funzionare."),
       "C":("Proponi fasi con checkpoint e un criterio misurabile per fermare o proseguire la migrazione.","Un rilascio graduale limita la superficie d'impatto e rende esplicita la decisione fra una fase e l'altra."),
       "D":("Usa la finestra disponibile per applicare subito la migrazione completa e controllare il risultato al termine.","La verifica finale arriva tardi se il primo passaggio modifica dati che non puoi ricostruire."),
      },
      "feature_flag_retirement": {
       "A":("Verifica quali coorti usano ancora la flag e controlla che ogni passaggio della migrazione sia completato.","Conoscere lo stato residuo impedisce di togliere una protezione ancora necessaria."),
       "B":("Misura il costo del ramo e individua una condizione osservabile che dimostri che la flag può essere rimossa.","La decisione lega la pulizia a un costo misurato e a una verifica della migrazione."),
       "C":("Prepara una modifica piccola con test, owner e una metrica per rilevare regressioni dopo la rimozione.","Un rilascio controllato rende visibili i rischi residui e assegna il follow-up."),
       "D":("Disattiva la flag per una coorte pilota e misura latenza ed errori prima di estendere la rimozione.","Il pilota riduce la superficie, ma scegliere una coorte prima di controllare lo stato della migrazione può coinvolgere utenti ancora dipendenti dalla flag."),
      },
      "adoption": {
       "A":("Ricostruisci il percorso principale con eventi e feedback disponibili e individua dove gli utenti abbandonano.","Capire il punto di attrito chiarisce se il problema è scoperta, comprensione o completamento."),
       "B":("Controlla che gli eventi rappresentino davvero l'uso riuscito e segmentali per bisogno e tipo di utente.","Un contatore generico può confondere un click con il valore che la funzione dovrebbe offrire."),
       "C":("Proponi un esperimento piccolo con una modifica e un criterio di successo concordato.","Un test limitato verifica una causa possibile senza ampliare subito lo scope."),
       "D":("Aggiungi le opzioni richieste dal team prima di capire il flusso che le persone non completano.","Più scelte non risolvono necessariamente il punto di abbandono e possono aggiungere altra complessità."),
      },
      "code_change": {
       "A":("Riproduci il difetto con un test di regressione e cambia il punto più vicino alla causa osservata.","Un fix piccolo e coperto riduce la probabilità di nascondere un secondo bug nel refactor."),
       "B":("Confronta il comportamento prima e dopo la modifica nei soli casi coinvolti e in un caso adiacente.","Il confronto delimita la regressione e offre una prova ripetibile per la review."),
       "C":("Sposta la pulizia strutturale in una proposta separata con owner e criterio di completamento.","Separare il refactor mantiene leggibile il hotfix senza perdere il lavoro di qualità."),
       "D":("Estendi la patch ai moduli vicini mentre li hai aperti, anche se il bug riprodotto è locale.","Un cambiamento più ampio può essere utile, ma in una correzione urgente aumenta review e rollback."),
      },
      "test_flake": {
       "A":("Registra seed, ordine, log e risorsa condivisa del test prima di ripetere il run.","Conservare lo stato che cambia fra run rende possibile distinguere una race da una dipendenza instabile."),
       "B":("Esegui il test isolato e poi insieme alla suite per vedere quale combinazione fa emergere il fallimento.","Il confronto controlla se il problema dipende dal test o da stato condiviso nella suite."),
       "C":("Se devi quarantinare il test, assegna un owner, un ticket e una data per rimuovere la quarantena.","La quarantena protegge il flusso di consegna soltanto se resta visibile e temporanea."),
       "D":("Aggiungi un retry e conserva gli output dei tentativi falliti per analizzarli dopo la consegna.","Il retry può sbloccare la pipeline e conserva evidenza, ma rimanda la verifica di eventuali race nel codice."),
      },
      "dependency": {
       "A":("Proteggi il confine con la dipendenza usando un timeout, una validazione minima e un fallback visibile.","Controlli al confine limitano gli effetti di risposte lente o incomplete e rendono esplicito il comportamento degradato."),
       "B":("Confronta trace del chiamante e metriche del provider per separare timeout, saturazione e richiesta malformata.","Le due viste localizzano il confine del guasto prima di attribuire la causa a un team."),
       "C":("Invia all'owner una riproduzione minima, gli orari e l'impatto, e concorda chi aggiorna il ticket.","Un handoff con evidenza riduce i tempi senza fingere di controllare il servizio altrui."),
       "D":("Aumenta temporaneamente il timeout del chiamante e confronta completamenti e latenza nelle ore successive.","Più attesa può recuperare richieste lente, ma trattiene risorse e non risolve risposte incomplete o saturazione."),
      },
      "operations": {
       "A":("Osserva un'esecuzione reale e annota il passaggio manuale che produce più errori o ritardi.","Automatizzare il punto misurato riduce il rischio senza codificare un flusso che nessuno ha verificato."),
       "B":("Prova lo script su una copia dei dati e confronta conteggi e risultato con il procedimento manuale.","Il confronto individua divergenze prima che il nuovo strumento tocchi dati operativi."),
       "C":("Coinvolgi chi esegue il processo e concorda un piccolo esperimento con un modo semplice per tornare indietro.","Chi usa il flusso può rivelare eccezioni che non compaiono nel documento iniziale."),
       "D":("Automatizza l'intero processo in una volta per eliminare subito il lavoro ripetitivo.","Un'automazione completa può risparmiare tempo, ma trasferisce gli errori manuali nel sistema prima di verificarli."),
      },
      "metrics": {
       "A":("Calcola lo stesso indicatore su segmenti e finestre temporali comparabili prima di estendere il rollout.","Una media globale può nascondere gruppi diversi; la segmentazione verifica se l'effetto è generalizzabile."),
       "B":("Allinea denominatore, esclusioni e definizione di errore con chi ha prodotto l'altra metrica.","Due query possono essere entrambe corrette e rispondere a domande differenti."),
       "C":("Prepara un esperimento limitato con una metrica primaria e una condizione di arresto concordata.","Un test circoscritto produce evidenza nuova e limita il costo di una conclusione sbagliata."),
       "D":("Estendi gradualmente il rollout con una soglia di arresto basata sull'indicatore medio.","Un rollout graduale limita il rischio, ma un gate medio può continuare a nascondere un peggioramento per alcuni segmenti."),
      },
      "personal_error": {
       "A":("Contieni il problema, conserva i dati utili alla diagnosi e comunica subito chi è coinvolto.","Rendere visibile un errore personale permette al team di proteggere gli utenti e reagire con informazioni corrette."),
       "B":("Descrivi il tuo contributo senza attenuanti e separa i fatti osservati dalle cause ancora da verificare.","Una spiegazione precisa mantiene fiducia e impedisce che l'ipotesi diventi una conclusione prematura."),
       "C":("Dopo la mitigazione, aggiungi una regressione e una modifica al processo che riduca la ripetizione.","Una correzione preventiva trasforma l'errore in un miglioramento condiviso, senza sostituire il ripristino immediato."),
       "D":("Prepara prima una patch verificata, poi comunica al gruppo causa e soluzione insieme.","Un aggiornamento completo è utile, ma aspettare la patch ritarda il coordinamento su un impatto già presente."),
      },
      "data_process": {
       "A":("Sospendi le nuove elaborazioni e salva un conteggio consistente prima di ripulire i record.","Fermare altre scritture protegge la diagnosi e riduce la possibilità di moltiplicare il difetto."),
       "B":("Esegui un dry run in sola lettura sui record selezionati e registra checkpoint e conteggi prima/dopo.","Il dry run verifica la regola e rende misurabile l'estensione del problema senza cambiare i dati."),
       "C":("Concorda con l'owner una regola idempotente e un piano di riconciliazione per gli elementi già elaborati.","Una regola condivisa evita che job concorrenti o retry ricreino la stessa anomalia."),
       "D":("Avvia la pulizia sui record visibili e correggi i casi mancanti nel giro successivo.","Una correzione parziale può lasciare il dataset in uno stato più difficile da riconciliare."),
      },
      "collaboration": {
       "A":("Porta alla decisione i fatti disponibili, l'impatto osservato e un'opzione di mitigazione circoscritta.","Un quadro concreto aiuta le persone coinvolte a scegliere senza confondere ipotesi e fatti."),
       "B":("Chiarisci chi può decidere e quale vincolo deve restare valido prima di concordare il passaggio successivo.","Owner e vincoli espliciti riducono attese e accordi incompatibili."),
       "C":("Rendi visibili priorità, costo e prossimo aggiornamento alle persone che devono scegliere lo scope.","Una decisione condivisa riduce richieste incompatibili e aspettative divergenti."),
       "D":("Attendi che il team proprietario abbia capacità prima di offrire una mitigazione o un piano alternativo.","Rispettare l'ownership è utile, ma l'attesa senza un accordo può prolungare l'impatto evitabile."),
      },
      "learning": {
       "A":("Aggiorna l'ipotesi alla luce del nuovo dato e ferma la modifica che non lo spiega più.","Cambiare idea quando cambiano le prove evita di investire altro tempo in una causa smentita."),
       "B":("Condividi il dato contrario e chiedi a un collega di provare la spiegazione alternativa sullo stesso campione.","Un controllo indipendente aiuta a scoprire un errore nel campione o nell'interpretazione."),
       "C":("Registra quale assunzione mancava e aggiungi una verifica tecnica piccola alla prossima stima o review.","Un cambiamento di processo mirato riduce la probabilità che la stessa assunzione resti invisibile."),
       "D":("Completa la modifica in una branch sperimentale e confrontala con l'ipotesi alternativa sul campione realistico.","Un confronto può chiarire il modello, ma completare una soluzione già smentita aumenta il costo prima di verificare la nuova causa."),
      },
      "incident_disagreement": {
       "A":("Riproduci richieste equivalenti e confronta chiave cache, filtro e risposta prima di scegliere una causa.","Un confronto controllato mette alla prova entrambe le ipotesi e dà al disaccordo una base osservabile."),
       "B":("Se il degrado cresce, applica una mitigazione reversibile a una porzione limitata e misura l'effetto.","Un esperimento circoscritto protegge il servizio mentre raccogli evidenza."),
       "C":("Condividi i dati con il collega e concordate owner, verifica successiva e condizione per cambiare strada.","Una decisione esplicita mantiene la collaborazione anche quando l'evidenza favorisce una delle ipotesi."),
       "D":("Prova la cache su una coorte limitata e misura il degrado per decidere se mantenere la modifica.","L'esperimento è circoscritto, ma il miglioramento della latenza non dimostra che il filtro sia corretto."),
      },
      "review_edge_case": {
       "A":("Aggiungi un test per ID zero e verifica quale comportamento definisce il contratto pubblico.","Il test separa un valore valido da un sentinel implicito prima di cambiare la logica."),
       "B":("Segui ID zero dal parsing al lookup e individua il punto in cui viene convertito o scartato.","La traccia del dato localizza l'errore e rende la correzione verificabile."),
       "C":("Ringrazia la revisora, aggiorna la fixture e riporta nella review quale assunzione è cambiata.","Riconoscere il contributo e registrare il caso rende la correzione riusabile dal team."),
       "D":("Aggiungi una validazione che rifiuti ID zero e proponi di documentare il vincolo nella API.","Un vincolo esplicito evita ambiguità, ma cambia il contratto prima di accertare se zero sia un ID valido."),
      },
      "accessibility_deadline": {
       "A":("Prova il flusso principale da tastiera e con screen reader e annota il passaggio che blocca il completamento.","La verifica su un compito reale distingue un blocco d'accesso da un dettaglio cosmetico."),
       "B":("Mostra al responsabile prodotto l'impatto osservato e chiedi una decisione esplicita sul criterio di rilascio.","Una decisione informata rende visibile il compromesso senza scaricare il rischio sugli utenti."),
       "C":("Fissa il blocco del flusso principale come requisito di rilascio e sposta i ritocchi non bloccanti in un follow-up assegnato.","Separare il requisito essenziale dalla rifinitura protegge l'accesso e mantiene uno scope consegnabile."),
       "D":("Rilascia alla data prevista e inserisci il problema di accessibilità nel backlog successivo.","Un blocker noto può escludere utenti dall'attività principale; la data da sola non misura quel costo."),
      },
      "alert_quality": {
       "A":("Esamina soglia, finestre e occorrenze recenti per trovare quando l'alert scatta senza impatto.","La cronologia aiuta a identificare una condizione rumorosa senza rimuovere il segnale utile."),
       "B":("Correla l'alert con errori cliente e metriche indipendenti prima di decidere se il nuovo evento è reale.","La corroborazione separa un falso positivo da un incidente che il team rischia ormai di ignorare."),
       "C":("Assegna un owner alla qualità dell'alert e concorda un indicatore per misurare il rumore dopo la correzione.","Un follow-up con owner impedisce che il problema torni invisibile appena finisce la finestra critica."),
       "D":("Aumenta temporaneamente la finestra di aggregazione e confronta il volume delle notifiche nelle ore successive.","La finestra può filtrare picchi brevi, ma da sola non dimostra che gli incidenti cliente restino rilevati in tempo."),
      },
      "delete_policy": {
       "A":("Metti in pausa la DELETE e salva in sola lettura l'elenco di ID e conteggi selezionati.","Fermare un'azione irreversibile conserva evidenza e dati finché il contratto di retention non è chiaro."),
       "B":("Esegui un dry run sicuro che mostri quali account e quale regola verrebbero coinvolti.","Un'anteprima verificabile rende concreta la richiesta senza cancellare record."),
       "C":("Concorda con owner e stakeholder retention, audit e procedura di recupero prima di definire la regola.","Il contratto deve includere gli obblighi e il percorso di recupero prima che il dato venga eliminato."),
       "D":("Converti la DELETE in un soft delete reversibile e mantieni gli account recuperabili per trenta giorni.","La reversibilità riduce il rischio, ma anche un soft delete può interrompere accessi e imporre una retention non concordata."),
      },
      "pipeline_incident": {
       "A":("Verifica l'impatto cliente con le metriche di produzione e applica una mitigazione circoscritta senza aspettare il servizio E2E instabile.","L'impatto attivo richiede una decisione basata su segnali di produzione mentre il test viene indagato separatamente."),
       "B":("Isola il test end-to-end attorno al servizio intermittente e registra una riproduzione del fallimento.","Una diagnosi separata chiarisce il rischio della pipeline senza scambiare il test instabile per prova sul servizio live."),
       "C":("Comunica il rischio residuo dei test, assegna un owner e indica il prossimo aggiornamento sull'impatto.","Un handoff chiaro mantiene visibili sia l'incidente sia l'incertezza della validazione."),
       "D":("Rilascia il fix a una piccola coorte basandoti sui test unitari verdi e monitora le metriche cliente.","Una canary raccoglie evidenza utile, ma richiede un criterio di arresto e non sostituisce una mitigazione già disponibile."),
      },
      "regional_bug": {
       "A":("Riproduci l'input con la lingua e il fuso esatti e controlla parsing, conversione e visualizzazione ai confini del giorno.","Il caso controllato rende osservabile la differenza che la media globale nasconde."),
       "B":("Misura quante richieste e quali utenti sono coinvolti, mantenendo separati i segmenti interessati.","La misura del segmento chiarisce l'impatto senza concludere che il problema non esista perché è raro."),
       "C":("Aggiungi un test di regressione per la combinazione e documenta quale fuso governa il dato salvato.","Un contratto esplicito protegge il caso raro dalle prossime modifiche di formato."),
       "D":("Proponi di normalizzare le date in UTC e verifica la modifica sui test di formato già presenti.","UTC semplifica l'istante salvato, ma i test esistenti potrebbero non coprire il giorno locale che il cliente intende rappresentare."),
      },
      "api_contract": {
       "A":("Conferma la soglia e il caso del cliente; valuta un workaround sicuro che ripristini il percorso senza superare la capacità del servizio.","Una mitigazione verificata riduce l'impatto senza promettere un limite che il sistema non può sostenere."),
       "B":("Confronta validazione server, guida pubblica e richieste rifiutate per ricostruire il contratto effettivo.","Le tre fonti chiariscono se manca documentazione, capacità o comportamento concordato."),
       "C":("Coinvolgi owner e supporto, comunica ciò che è confermato e aggiorna il contratto dopo la decisione.","Un messaggio accurato mantiene fiducia mentre la regola viene chiarita e resa visibile."),
       "D":("Concedi al cliente un aumento temporaneo della soglia e osserva il carico mentre aggiorni la guida.","Un'eccezione può ripristinare il flusso, ma serve prima verificare che la soglia non protegga una capacità critica."),
      },
      "broad_pr": {
       "A":("Separa refactor, API e migrazione in passaggi piccoli che possano essere verificati e annullati indipendentemente.","Una sequenza circoscritta rende chiari i contratti e riduce il costo di isolare una regressione."),
       "B":("Chiedi una review mirata sui confini a rischio e allega per ciascuno una prova e un piano di rollback.","La review diventa concreta anche prima che il cambiamento venga suddiviso."),
       "C":("Concorda ordine, owner e criterio di completamento, mantenendo nel primo rilascio soltanto lo scope necessario.","Un piano condiviso conserva il risultato richiesto senza far sparire il lavoro di pulizia."),
       "D":("Conserva la PR unita e prepara un rollback dell'intera release, usando la suite verde come gate.","Un rollback globale è una protezione, ma può essere insufficiente quando la migrazione modifica dati irreversibilmente."),
      },
      "concurrency": {
       "A":("Traccia le letture e scritture dello stato condiviso con identificativi di richiesta e ordine degli eventi.","L'ordine osservato aiuta a localizzare il punto in cui un aggiornamento viene sovrascritto."),
       "B":("Costruisci un riproduttore deterministico con due richieste simultanee e asserisci il risultato atteso.","Una riproduzione controllata trasforma un race raro in una prova ripetibile."),
       "C":("Aggiungi il caso concorrente alla suite e chiedi una review del confine che protegge la mutazione.","La regressione resta visibile e la garanzia viene condivisa con chi mantiene il codice."),
       "D":("Serializza temporaneamente le richieste al servizio e confronta errori e throughput sotto carico.","La serializzazione può contenere la race, ma può spostare il problema sulla capacità e lasciare non protetto lo stato condiviso fra istanze."),
      },
      "estimate_error": {
       "A":("Aggiorna la stima corrente e rendi esplicite le API e le ipotesi che devono ancora essere verificate.","Correggere subito l'aspettativa limita altro lavoro costruito su una premessa falsa."),
       "B":("Condividi la sequenza che ha portato alla stima e chiedi a un collega di rivedere il nuovo piano tecnico.","Una revisione aperta aiuta il team a verificare il cambiamento senza trasformarlo in una colpa altrui."),
       "C":("Assumiti la responsabilità del ritardo, prova l'API in una spike breve e aggiungi quel controllo alle stime future.","Un esperimento piccolo affronta l'assunzione mancante e rende il processo più affidabile."),
       "D":("Chiedi al team API una data per il nuovo endpoint e ricalcola la consegna sulla loro previsione.","La previsione della dipendenza aiuta il piano, ma lascia ancora non verificato il contratto su cui la stima si fondava."),
      },
    }
    actions["incomplete_payload"] = {
        "A": ("Raccogli una risposta incompleta e una valida, confronta campi, versione e richiesta, poi identifica quale contratto viene violato.", "Una riproduzione minima separa il dato assente da un'ipotesi sul trasporto o sul consumer."),
        "B": ("Impedisci al job di salvare record incompleti, conserva gli elementi da riprovare e comunica l'impatto osservato.", "Protegge i dati mentre la dipendenza viene diagnosticata; serve rendere visibile il lavoro sospeso."),
        "C": ("Cerca il referente di escalation concordato per il servizio e condividi evidenza, impatto e prossimo aggiornamento.", "La mancata risposta nel canale usuale richiede un percorso di coordinamento, senza scaricare il problema."),
        "D": ("Inserisci valori di default per i campi mancanti così il job può completarsi, documentando l'assunzione nel ticket.", "Può ripristinare l'elaborazione, ma trasformare assenze in dati apparentemente validi richiede una garanzia di contratto che qui manca."),
    }
    actions["metric_denominators"] = {
        "A": ("Concorda se la decisione riguarda richieste o utenti e confronta le due query sullo stesso periodo e sulla stessa popolazione.", "Prima di scegliere un numero, serve sapere quale domanda misura e rendere comparabili i campioni."),
        "B": ("Costruisci un dataset piccolo con un utente che fa molte richieste e calcola entrambi i tassi a mano.", "Un controesempio rende concreta la differenza fra pesare richieste e persone."),
        "C": ("Pubblica entrambi i risultati con denominatore, esclusioni e contesto, poi concorda quale metrica usare per la decisione.", "Mantiene trasparente l'incertezza e impedisce che due percentuali diverse sembrino contraddirsi senza spiegazione."),
        "D": ("Usa il tasso per richieste per il prossimo aggiornamento perché è quello già visibile nella dashboard.", "La continuità riduce confusione operativa, ma la metrica disponibile può non rappresentare l'impatto sugli utenti richiesto dalla decisione."),
    }
    families = [
      "incident", "customer_data", "ambiguous", "performance", "incident_disagreement", "migration",
      "hotfix_followup", "test_flake", "rollback_patch", "dependency", "collaboration", "metrics",
      "personal_error", "delete_policy", "broad_pr", "review_edge_case", "accessibility_deadline", "dependency",
      "operations", "collaboration", "data_process", "alert_quality", "concurrency", "migration",
      "regional_bug", "pipeline_incident", "metrics", "feature_flag_retirement", "collaboration", "learning",
      "api_contract", "data_process", "adoption", "code_change", "collaboration", "estimate_error",
    ]
    families[9] = "incomplete_payload"
    families[26] = "metric_denominators"
    scenarios=[]
    for i,(title,brief,principles,focus,order) in enumerate(SCENARIO_SEEDS,1):
        # Stable per-scenario permutation avoids a fixed or cyclic answer-position cue.
        labels = "".join(sorted("ABCD", key=lambda label: hashlib.sha256(f"ws-{i}:{label}".encode()).digest()))
        relabel = dict(zip("ABCD", labels))
        rank=[relabel[key] for key in order]
        actions_for_scenario=actions[families[i-1]]
        effectiveness=("Più efficace come prima mossa","Utile dopo la prima verifica","Da coordinare o applicare nel seguito","Debole o rischiosa in questo contesto")
        options=[]
        for key in "ABCD":
            rating=effectiveness[rank.index(relabel[key])]
            text,reasoning=actions_for_scenario[key]
            options.append({"id":relabel[key],"text":text,"effectiveness":rating,"reasoning":reasoning})
        options.sort(key=lambda option: option["id"])
        scenarios.append({"id":f"sde-ws-{i:02d}","module":"comportamento","title":title,"brief":brief,"options":options,"recommended_order":rank,"principles":[p.strip() for p in principles.split("·")],"learning_focus":focus})
    return scenarios

WORK_STYLE = [
 {"id":"sde-style-01","title":"Autonomia e supporto","prompt":"Ripensa a un'attività tecnica in cui hai provato a sbloccare il problema prima di chiedere aiuto. Quale segnale ti ha fatto coinvolgere un'altra persona?","reflection_prompts":["Quale evidenza avevi raccolto?","Che cosa hai comunicato a chi ti ha aiutato?"]},
 {"id":"sde-style-02","title":"Intuizione e dati","prompt":"Descrivi una scelta di lavoro in cui una misura ha modificato la tua prima impressione.","reflection_prompts":["Quanto era affidabile il campione?","Come hai spiegato l'incertezza?"]},
 {"id":"sde-style-03","title":"Qualità e scadenza","prompt":"Quando una consegna è vicina, come decidi quali verifiche non possono essere saltate?","reflection_prompts":["Quale rischio sarebbe difficile da annullare?","Come rendi visibile il compromesso?"]},
 {"id":"sde-style-04","title":"Disaccordo tecnico","prompt":"Ripensa a un disaccordo su una soluzione. Quale prova vi ha permesso di valutare le ipotesi?","reflection_prompts":["Che cosa hai imparato dall'altra prospettiva?","Come hai sostenuto la decisione finale?"]},
 {"id":"sde-style-05","title":"Errore personale","prompt":"Descrivi un errore concreto che hai commesso e il primo passo fatto dopo averlo scoperto.","reflection_prompts":["Chi doveva saperlo?","Quale cambiamento ha ridotto la probabilità che si ripetesse?"]},
 {"id":"sde-style-06","title":"Requisiti incompleti","prompt":"Quando una richiesta lascia aperti dettagli, quali chiarimenti chiedi e che cosa puoi imparare con una prova piccola?","reflection_prompts":["Quale assunzione costava di più sbagliare?","Come l'hai resa esplicita?"]},
 {"id":"sde-style-07","title":"Ownership oltre il ruolo","prompt":"Hai mai contribuito a un problema assegnato formalmente a un'altra area?","reflection_prompts":["Come hai coinvolto l'owner?","Quale confine era utile rispettare?"]},
 {"id":"sde-style-08","title":"Leggere con attenzione","prompt":"Prima di rispondere a un'affermazione che contiene 'sempre' o 'mai', quale differenza fa quella parola per il tuo comportamento abituale?","reflection_prompts":["Rispondi in modo personale e coerente.","Non esiste un profilo modello da imitare."]},
]
def build_catalog():
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    exercises = list({item["id"]: item for item in EXERCISES}.values())
    scenarios = build_scenarios()
    activity_sources = {
        "exercise": exercises,
        "lab": LABS,
        "simulation": SIMULATIONS,
        "scenario": scenarios,
        "work_style": WORK_STYLE,
    }
    activity_titles = {
        kind: {item["id"]: item["title"] for item in entries}
        for kind, entries in activity_sources.items()
    }
    lesson_ids = {item["id"] for item in LESSONS}
    if set(LESSON_DIDACTIC) != lesson_ids:
        missing = sorted(lesson_ids - set(LESSON_DIDACTIC))
        extra = sorted(set(LESSON_DIDACTIC) - lesson_ids)
        raise ValueError(f"Guide didattiche non allineate alle lezioni; mancanti={missing}, extra={extra}")
    lesson_bodies = {}
    for lesson_item in LESSONS:
        guide = LESSON_DIDACTIC[lesson_item["id"]]
        practice_titles = []
        for kind, activity_id in guide["practice"]:
            if activity_id not in activity_titles[kind]:
                raise ValueError(f"Attività {kind} {activity_id} non trovata per {lesson_item['id']}")
            practice_titles.append(activity_titles[kind][activity_id])
        body_parts = [lesson_item["body"].rstrip(), guide["notes"].strip()]
        body_parts.append(f"**Da ricordare.** {guide['recap']} **Per praticare:** {'; '.join(practice_titles)}.")
        lesson_bodies[lesson_item["id"]] = "\n\n".join(body_parts)
    lessons=[]
    for item in LESSONS:
        record={key:value for key,value in item.items() if key!="body"}
        path=CONTENT/record["body_file"]
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(lesson_bodies[item["id"]],encoding="utf-8")
        lessons.append(record)
    referenced_bodies = {CONTENT / item["body_file"] for item in lessons}
    for stale in LESSONS_DIR.glob("sde-l-*.md"):
        if stale not in referenced_bodies:
            stale.unlink()
    # The catalog is study material: expand one-line literals into readable code.
    for exercise in exercises:
        exercise["solution"] = python_solution(exercise["solution"])
        exercise["variants"]["python"]["solution"] = exercise["solution"]
        exercise["variants"]["cpp"]["solution"] = cpp_solution(exercise["variants"]["cpp"]["solution"])
    lesson_by_id = {item["id"]: item for item in lessons}
    exercise_by_id = {item["id"]: item for item in exercises}
    lab_by_id = {item["id"]: item for item in LABS}
    simulation_by_id = {item["id"]: item for item in SIMULATIONS}
    core_plan_minutes = 0
    for day in STUDY_PLAN:
        core_plan_minutes += sum(lesson_by_id[item_id]["minutes"] for item_id in day.get("lesson_ids", []))
        core_plan_minutes += sum(exercise_by_id[item_id]["minutes"] for item_id in day.get("exercise_ids", []))
        core_plan_minutes += sum(lab_by_id[item_id]["minutes"] for item_id in day.get("lab_ids", []))
        core_plan_minutes += sum(simulation_by_id[item_id]["minutes"] for item_id in day.get("simulation_ids", []))
        core_plan_minutes += int(day.get("practice_minutes", 0))
        for choice in day.get("choices", []):
            core_plan_minutes += max(
                sum(lesson_by_id[item_id]["minutes"] for item_id in branch.get("lesson_ids", []))
                + sum(lab_by_id[item_id]["minutes"] for item_id in branch.get("lab_ids", []))
                + int(branch.get("practice_minutes", 0))
                for branch in choice["options"].values()
            )
    catalog_minutes = (
        sum(item["minutes"] for item in lessons)
        + sum(item["minutes"] for item in exercises)
        + sum(item["minutes"] for item in LABS)
        + sum(item["minutes"] for item in SIMULATIONS)
    )
    raw={
      "meta":{
        "name":"Preparazione Amazon SDE-I OA","track_id":"amazon-sde-oa","version":"1.0","language":"it",
        "estimated_hours":round(catalog_minutes/60,1),"estimated_core_hours":round(core_plan_minutes/60,1),"study_plan":STUDY_PLAN,
        "assessment_note":"Il formato 40 + 60 è una simulazione di pratica; le prove effettive possono variare per ruolo e paese. Fai riferimento all'invito ricevuto.",
        "sources":["https://www.amazon.jobs/content/en/career-programs/university/sde","https://www.amazon.jobs/content/en/our-workplace/leadership-principles","https://candidatesupport.hackerrank.com/articles/8606305957-taking-front-end-back-end-full-stack-and-mobile-developer-assessments","https://candidatesupport.hackerrank.com/articles/7634558376-ai-assistant-in-tests","https://docs.python.org/3/tutorial/datastructures.html","https://isocpp.org/wiki/faq/containers"]
      },
      "modules":MODULES,"lessons":lessons,"exercises":exercises,"labs":LABS,"flashcards":build_flashcards(),
      "simulations":SIMULATIONS,"work_scenarios":scenarios,"work_style":WORK_STYLE
    }
    CATALOG_FILE.write_text(json.dumps(raw,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:len(raw[key]) for key in ("modules","lessons","exercises","labs","flashcards","simulations","work_scenarios","work_style")},ensure_ascii=False))
    return raw


if __name__ == "__main__":
    build_catalog()
