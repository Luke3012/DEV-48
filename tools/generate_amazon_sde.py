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
    {"id": "orientamento", "order": "00", "title": "Orientamento all'OA", "description": "Formato dichiarato, metodo di problem solving e pratica senza dipendere dall'AI."},
    {"id": "linguaggi", "order": "01", "title": "C++ e Python per il coding interview", "description": "Una prova equivalente per scegliere il linguaggio in base a velocità, memoria e debugging."},
    {"id": "fondamenti", "order": "02", "title": "Fondamenti DSA", "description": "Complessità, array, stringhe, mappe e insiemi."},
    {"id": "pattern", "order": "03", "title": "Pattern fondamentali", "description": "Two pointers, finestre mobili, prefissi, ordinamento e intervalli."},
    {"id": "ricerca", "order": "04", "title": "Ricerca e strutture lineari", "description": "Stack, queue, deque e varianti della ricerca binaria."},
    {"id": "strutture", "order": "05", "title": "Liste, alberi e grafi", "description": "Puntatori, ricorsione, BFS, DFS e ordinamento topologico."},
    {"id": "avanzato", "order": "06", "title": "Pattern avanzati da interview", "description": "Heap, greedy, backtracking e dynamic programming essenziale."},
    {"id": "repository", "order": "07", "title": "Code Repository Question", "description": "Orientamento, test, stack trace, debugging e fix minimi in C++ o Node.js."},
    {"id": "comportamento", "order": "08", "title": "Componenti comportamentali", "description": "Leadership Principles, Work Simulation e familiarizzazione Work Style."},
    {"id": "simulazioni", "order": "09", "title": "Prove a tempo", "description": "Simulazioni indipendenti e mock sequenziale 40 + 60 minuti."},
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
           "Separare la pratica richiesta per la Coding Question da quella richiesta per il repository debugging.", r'''
La Coding Question e la Code Repository Question sono due sezioni distinte: la prima presenta un problema circoscritto, in genere su un singolo file; la seconda richiede di comprendere e modificare un progetto articolato in più file. Nel formato di riferimento, le sezioni durano rispettivamente 40 e 60 minuti, con timer indipendenti.

Questi tempi descrivono un formato specifico, non una struttura universale. La pagina ufficiale Amazon per studenti e neolaureati precisa che struttura e componenti variano in base al paese e rimanda alle istruzioni dell'assessment. Anche la pagina pubblica per i ruoli full-time riporta tempi medi e componenti diversi. Per una prova concreta fanno fede l'invito ricevuto e le indicazioni mostrate dalla piattaforma.

La sezione di coding richiede di chiarire il contratto, scegliere una struttura dati, implementare una soluzione e verificarne i casi limite entro il tempo disponibile. La sezione repository richiede invece di orientarsi in un progetto esistente, ricostruendo il flusso dai README e dai test prima di intervenire su controller, funzioni `main` o componenti equivalenti.

Le esercitazioni marcate **NO AI · NO INTERNET · TIMED** si svolgono senza assistente e senza accesso a Internet. Questa modalità serve a esercitare il lavoro autonomo, ma non definisce le regole di un assessment reale, che dipendono dalle istruzioni ricevute. I materiali riservati e le domande trapelate non vanno utilizzati.

### Risorse e attività

- Il curriculum contiene lezioni brevi con un argomento riconoscibile; ogni lezione è riapribile da sola.
- Gli esercizi DSA hanno test eseguibili in Python 3 e C++20, con soluzioni e complessità.
- I sei repository lab sono cartelle modificabili, con test che partono da failure realistiche.
- Work Simulation e Work Style sono attività distinte: la prima richiede decisioni di lavoro, la seconda familiarizzazione senza ricette per manipolare le risposte.
'''),
    lesson("problem-solving", "orientamento", "Dai primi due minuti a una soluzione verificabile", 1, 20, "base",
           ["contratto input/output", "esempio manuale", "invariante", "complessità"],
           "Arrivare a una soluzione corretta passando da un requisito a casi che la possono smentire.", r'''
Quando il cronometro parte, la tentazione è digitare subito. Fai invece un esempio piccolo con le mani. Per una lista `[4, 1, 7]` e una ricerca del valore `1`, scrivi quale risultato deve uscire e cosa succede se la lista è vuota. Una domanda fatta ora costa pochi secondi; una supposizione errata può costarti l'intero tentativo.

Poi scegli la versione più semplice che rispetta il contratto e misurane il costo. Se la prima idea confronta ogni coppia, con `n` elementi esegue circa `n²` confronti. Non è un difetto se `n` è piccolo; diventa un problema quando il vincolo arriva a decine di migliaia. Solo a quel punto cerca l'informazione che manca: una mappa, un ordinamento, una finestra mantenuta tra un passo e il successivo.

Mentre implementi, tieni un'invariante in una frase: «la mappa contiene gli elementi già attraversati». Dopo ogni cambiamento, verifica un caso che avrebbe fatto fallire la versione precedente. Se il codice non va, riduci l'input e formula una causa precisa; cambiare tre righe insieme cancella le prove.

Un ritmo realistico per 40 minuti è: chiarimento e casi, 4–6 minuti; scelta e implementazione, circa 25; test manuali e rifinitura, il tempo restante. Se una strada è bloccata, conserva la soluzione parziale e prova un'alternativa con costo chiaro.
'''),
    lesson("language-choice", "linguaggi", "Scegliere il linguaggio per i 40 minuti", 1, 20, "base",
           ["mini-prova equivalente", "velocità di scrittura", "debugging", "strutture standard"],
           "Confrontare Python 3 e C++ su una prova breve prima di impegnare tutta la preparazione.", r'''
La scelta tra Python e C++ dipende dalla familiarità operativa, dalla velocità di scrittura e dalla capacità di individuare gli errori. Una prova breve sugli stessi casi offre un confronto più utile della sola impressione o della conoscenza teorica del linguaggio.

L'esercizio propone una lista di interi e una dimensione `k`; la funzione deve restituire la somma massima di `k` elementi consecutivi. Dopo la somma della prima finestra, il totale si aggiorna sottraendo l'elemento in uscita e aggiungendo quello in entrata, senza ricalcolare ogni somma. La prova dura 8 minuti per linguaggio, con gli stessi input e casi e un editor vuoto.

Per ciascun linguaggio si possono confrontare il tempo di scrittura, le consultazioni di sintassi, gli errori introdotti e la rapidità nel verificare lista vuota, un solo elemento e finestre che avanzano. È preferibile la soluzione che lascia più tempo al ragionamento, non quella che appare più elegante sulla carta.

La lingua degli esercizi si seleziona con `L`; DEV//48 conserva risposte e tentativi separatamente per Python e C++. La preferenza può essere aggiornata dopo una prova pratica. Il runner C++ usa C++20 con GCC o Clang; senza un compilatore installato gli esercizi restano leggibili, ma non eseguibili nell'app.
'''),
    lesson("python-toolkit", "linguaggi", "Python 3 essenziale per l'interview", 1, 25, "base",
           ["list, tuple, dict e set", "enumerate e range", "Counter e defaultdict", "deque e heapq"],
           "Recuperare soltanto la sintassi Python che fa risparmiare tempo nei problemi DSA.", r'''
Per un problema su array, `list[int]` basta quasi sempre. `enumerate(nums)` ti dà indice e valore senza una variabile contatore da aggiornare; `range(left, right)` esclude `right`, dettaglio che vale la pena controllare quando gli indici sono già stanchi. Lo slicing `s[::-1]` crea una copia invertita: comodo per una verifica, costoso se la stringa è enorme e la copia non serve.

`dict` e `set` risolvono membership e conteggi: `counts[x] = counts.get(x, 0) + 1`. Quando il default è una collezione, `defaultdict(list)` evita il ramo «chiave vista per la prima volta». `Counter` è ottimo per frequenze, ma per un colloquio devi comunque saper spiegare cosa costa ogni passaggio.

Una lista va bene come stack con `append` e `pop`. Per BFS usa `collections.deque` e `popleft()`: togliere il primo elemento da una lista sposta il resto. `heapq` espone un min-heap; per ottenere un max-heap con numeri interi, spesso basta inserire `-value`.

`sorted(values)` crea una nuova lista; `values.sort()` modifica quella esistente. Preferisci la prima quando l'input fa parte del contratto e non deve cambiare. Comprehension e lambda sono strumenti, non una gara a scrivere la riga più corta.
'''),
    lesson("cpp-toolkit", "linguaggi", "C++ moderno e STL senza rumore", 1, 30, "base",
           ["vector e string", "hash e contenitori ordinati", "iteratori e confini", "reference e const"],
           "Riprendere la parte di C++ che compare davvero in una coding interview.", r'''
Un `vector<int>` è la scelta normale per una sequenza modificabile; `string` è una sequenza di caratteri con indici da zero. Per lookup medio costante scegli `unordered_map` o `unordered_set`; `map` e `set` mantengono l'ordine e costano `O(log n)`. `pair<int,int>` è utile per portare insieme due coordinate senza creare una classe.

`stack`, `queue` e `deque` esprimono LIFO, FIFO e accesso a entrambe le estremità. `priority_queue<int>` è un max-heap; per il min-heap usa `greater<int>`. `sort`, `lower_bound` e `upper_bound` stanno in `<algorithm>`. Una lambda per ordinare intervalli è spesso sufficiente: `[](const auto& a, const auto& b) { return a[0] < b[0]; }`.

Una reference `const vector<int>&` evita una copia e impedisce alla funzione di modificare l'input. Il range-based `for (const auto& x : values)` è più sicuro che incrementare un indice quando non ti serve l'indice. `size()` restituisce un tipo unsigned: confrontarlo con `int` può produrre sorprese, soprattutto sottraendo uno da una sequenza vuota.

Per alberi e liste, un `struct TreeNode` con puntatori `left/right` e `nullptr` basta. Usa ricorsione quando il problema segue naturalmente i figli; conserva uno stato locale chiaro e valuta la profondità massima. Non serve ripassare template avanzati per risolvere un OA.
'''),
    lesson("complexity", "fondamenti", "Big-O e vincoli: capire quando una risposta è troppo lenta", 1, 25, "base",
           ["O(1), O(log n), O(n)", "O(n log n) e O(n²)", "spazio ausiliario", "dimensione dei vincoli"],
           "Stimare il lavoro prima di affidarsi a una soluzione che supera i casi di esempio.", r'''
Se raddoppi `n`, un passaggio lineare fa circa il doppio del lavoro; due cicli annidati spesso ne fanno quattro volte tanto. Quella differenza diventa visibile quando i vincoli passano da 100 a 100.000. L'esempio non deve essere cronometrato al millisecondo: serve a scartare una famiglia di soluzioni incompatibile con la scala.

Una ricerca binaria dimezza lo spazio a ogni confronto e richiede `O(log n)`, ma l'array deve essere ordinato o la condizione deve essere monotona. Ordinare prima costa `O(n log n)`. Una mappa può portare lookup medio a `O(1)` pagando spazio `O(n)`; non è «gratis», è uno scambio esplicito.

Quando leggi i constraints, cerca numeri massimi, valori negativi, duplicati e input vuoti. Se `n` arriva a 200.000, `O(n²)` è quasi sempre un segnale d'allarme. Un esercizio del catalogo include un caso grande costruito proprio per separare una scansione lineare da un doppio ciclo.

La complessità spaziale conta quanto quella temporale: una soluzione che copia una matrice può passare i test piccoli e superare la memoria. Specifica se lo spazio ausiliario cresce con l'input o se stai modificando la struttura ricevuta.
'''),
    lesson("arrays-strings", "fondamenti", "Array e stringhe: scansione, indici e mutazioni", 1, 20, "base",
           ["traversal", "indici inclusivi ed esclusivi", "in-place", "copie e memoria extra"],
           "Ridurre off-by-one e mutazioni accidentali durante una scansione lineare.", r'''
Una scansione ha tre domande concrete: da dove parto, quando mi fermo, cosa significa l'indice corrente? Scrivi l'intervallo `[left, right)` quando il bordo destro non è incluso. La sua lunghezza è `right - left`; l'ultimo elemento è `right - 1`. Questa convenzione si incastra bene con slicing Python e iteratori C++.

Se devi invertire un array senza spazio extra, scambia gli estremi e avvicinali. Se devi soltanto restituire una versione ordinata, una copia chiarisce il contratto. `sort` in-place è un'altra scelta: utile quando il prompt permette di modificare l'input, rischiosa quando un test successivo riusa i dati.

Per le stringhe, distinguere una sequenza di byte da un carattere Unicode completo può essere importante fuori dai problemi standard di interview. Gli esercizi considerano caratteri ASCII dichiarati nel prompt, così l'attenzione resta sull'algoritmo. Gli indici restano comunque facili da sbagliare: vanno verificati il primo, l'ultimo e la lunghezza zero.
'''),
    lesson("hashmap-set", "fondamenti", "HashMap e Set: memoria utile, non magia", 1, 30, "base",
           ["lookup e complementi", "frequenze", "duplicati e raggruppamento", "chiavi e spazio"],
           "Usare una struttura per ricordare ciò che serve senza ripassare tutto l'input.", r'''
La mappa è utile quando puoi nominare la domanda che vuoi fare a ogni elemento: «ho già visto il suo complemento?», «quante volte è comparsa questa lettera?», «a quale gruppo appartiene questa firma?». In Two Sum, per il valore `x` cerchi `target - x` tra gli indici già incontrati. Salvare l'indice solo dopo la ricerca evita di usare lo stesso elemento due volte.

Un set risponde a «esiste già?» senza associarci un conteggio. Una mappa di frequenze conta con `counts[x] += 1`. Per raggruppare parole anagramma, una chiave possibile è la tupla delle 26 frequenze; ordinare ogni parola funziona pure, ma cambia il costo.

Le operazioni hash sono in media `O(1)`, non una garanzia matematica per ogni caso. Se serve ordine, usa una struttura ordinata e accetta `O(log n)`. Quando la mappa memorizza prefissi, stati o nodi, dichiara anche quanta memoria può crescere.

Un errore ricorrente è sovrascrivere una frequenza quando il problema richiede accumularla. Un altro è interrogare una mappa mutandola senza volerlo: in C++ `operator[]` inserisce una chiave mancante; `find` permette un lookup che non cambia il contenitore.
'''),
    lesson("two-pointers", "pattern", "Two Pointers: far incontrare due scansioni", 2, 25, "base",
           ["estremi opposti", "fast/slow", "array ordinati", "invariante del movimento"],
           "Eliminare candidati in coppia quando l'ordine consente di motivare ogni spostamento.", r'''
Con un array ordinato, due indici ai bordi possono cercare una somma senza provare tutte le coppie. Se la somma è troppo piccola, muovere il sinistro verso destra è l'unico modo per aumentarla; se è troppo grande, arretrare il destro la riduce. Ogni passo scarta una famiglia di coppie, non un'ipotesi a caso.

Il pattern fast/slow ha un'altra funzione. Un puntatore avanza di uno, l'altro di due; incontrarsi rivela un ciclo, oppure il lento può raggiungere il punto medio mentre il veloce percorre una lista. Non richiede un array ordinato, ma ha bisogno di una relazione tra i passi.

In-place deduplication usa spesso un indice di scrittura e uno di lettura. L'indice lento indica il prefisso già pulito; quello veloce esplora il resto. Se non riesci a dire cosa garantisce la zona tra i due, fermati prima di codificare.
'''),
    lesson("sliding-window", "pattern", "Sliding Window: aggiornare una finestra senza rifarla", 2, 30, "intermedio",
           ["finestra fissa", "finestra variabile", "frequenze", "condizione monotona"],
           "Riutilizzare il lavoro tra finestre contigue e riconoscere quando il pattern non vale.", r'''
Provare ogni substring da capo ripete gli stessi conteggi. Una finestra conserva i dati del tratto `[left, right]`: quando `right` avanza aggiungi un elemento, e quando la condizione non regge sposta `left`, rimuovendo ciò che esce. Il costo scende a `O(n)` perché ciascun bordo attraversa l'array al massimo una volta.

Per una finestra di dimensione fissa, prima accumuli i primi `k` valori, poi aggiungi il nuovo e sottrai quello che lascia. Per una finestra variabile, serve che la proprietà migliori o peggiori in modo prevedibile quando restringi. L'esempio classico usa numeri non negativi: con valori negativi, avanzare `left` non garantisce di diminuire la somma e la logica si rompe.

Con frequenze di caratteri, non basta muovere i due indici: aggiorna la mappa alla stessa operazione in cui cambia il bordo. `Longest Substring Without Repeating Characters` restringe finché la frequenza di un carattere supera uno. `Minimum Window` aggiunge invece un contatore dei requisiti ancora mancanti.
'''),
    lesson("prefix-sum", "pattern", "Prefix Sum e HashMap per intervalli e sottosequenze", 2, 25, "intermedio",
           ["somme cumulative", "intervalli", "subarray sum", "prefix map"],
           "Rispondere a domande su segmenti usando la differenza tra due prefissi.", r'''
Definisci `prefix[i]` come la somma dei primi `i` elementi. La somma dell'intervallo `[left, right)` è `prefix[right] - prefix[left]`. Con un prefisso iniziale pari a zero, anche gli intervalli che partono dal primo elemento seguono la stessa formula.

Per contare subarray con somma `k`, mentre avanzi con somma corrente `s`, cerchi quante volte è apparso `s - k`. La mappa dei prefissi si inizializza con `{0: 1}`: senza quella voce perdi i segmenti che cominciano a indice zero. Qui torna la stessa idea di Two Sum: la mappa ricorda un valore già visto che completa quello corrente.

La differenza tra due prefissi funziona anche con numeri negativi, mentre la sliding window per somme spesso no. Questo è un buon esempio di pattern riconosciuto dal motivo matematico, non dalla parola “subarray”.
'''),
    lesson("sorting-intervals", "pattern", "Sorting e intervalli: ordinare per scoprire sovrapposizioni", 2, 25, "intermedio",
           ["comparatore", "merge intervals", "confini aperti e chiusi", "scheduling"],
           "Usare l'ordinamento per rendere locale un problema che altrimenti richiede confronti incrociati.", r'''
Se ordini gli intervalli per inizio, quando leggi il prossimo sai che nessun intervallo futuro inizierà prima. Puoi quindi confrontarlo con il risultato appena costruito: se si sovrappone, estendi la fine; altrimenti aggiungi un nuovo intervallo. Il costo è dominato dall'ordinamento, `O(n log n)`.

Il dettaglio che decide i test è il confine: `[1, 3]` e `[3, 5]` si toccano. Il requisito può considerarli sovrapposti (`start <= end`) o separati (`start < end`). Non scegliere una delle due convenzioni senza leggerla nell'enunciato.

Un comparatore C++ deve definire un ordinamento coerente; Python `sort(key=...)` spesso basta. L'ordinamento muta l'input: se il contratto vieta la mutation, copia prima oppure costruisci una sequenza ordinata nuova.
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
Uno stack risponde all'ultimo elemento aggiunto; una queue al primo. Le parentesi sono LIFO: l'ultima parentesi aperta deve chiudersi per prima. La BFS è FIFO: i nodi a distanza `d` entrano in coda prima di quelli a distanza `d+1`, perciò il primo arrivo è un cammino minimo nei grafi non pesati.

Il tipo di contenitore evita lavoro superfluo. In Python `deque.popleft()` non sposta gli elementi rimasti. In C++ `queue.pop()` rimuove la testa e `front()` la legge; non invertire l'ordine delle due operazioni.

Per parentesi corrette, scarta subito una chiusura senza apertura e alla fine controlla che lo stack sia vuoto. Se verifichi soltanto il conteggio delle parentesi, `)(` passa per errore: il loro ordine è proprio l'informazione che lo stack conserva.
'''),
    lesson("monotonic-stack", "ricerca", "Monotonic Stack: conservare candidati ancora utili", 3, 25, "intermedio",
           ["stack monotono", "prossimo maggiore", "temperatura successiva", "ammortizzato"],
           "Risolvere domande sul prossimo valore maggiore o minore senza riesaminare ogni coppia.", r'''
Per ogni giorno, vuoi sapere il prossimo giorno più caldo. Il doppio ciclo visita tutte le coppie. Uno stack monotono conserva gli indici ancora in attesa: quando arriva una temperatura più alta, risolve i giorni più freddi in cima. Gli indici che restano non hanno ancora trovato risposta.

Ogni indice entra una volta ed esce una volta, quindi il lavoro totale è `O(n)` anche se un singolo elemento può attivare più pop. È un caso in cui “niente cicli annidati” non è la prova della complessità: conta quante volte ogni elemento attraversa lo stack.

Prima di partire, decidi se vuoi il successivo strettamente maggiore o maggiore/uguale. Cambia la condizione di pop. Se il testo chiede distanza, salva gli indici; se vuole solo il valore, può bastare salvare i valori.
'''),
    lesson("binary-search", "ricerca", "Binary Search classica: dimezzare uno spazio ordinato", 3, 20, "base",
           ["array ordinato", "mid sicuro", "intervallo residuo", "O(log n)"],
           "Mantenere la garanzia che la risposta, se esiste, resti nell'intervallo di ricerca.", r'''
La ricerca binaria è corta solo dopo avere stabilito l'invariante. Con l'intervallo chiuso `[left, right]`, calcola il medio e conserva la metà che può ancora contenere il valore. Quando `left > right`, non è rimasto alcun candidato.

Su `[1, 3, 5, 8, 12]`, la ricerca di `8` inizia dal valore medio `5`: i tre valori a sinistra vengono esclusi e resta `[8, 12]`. Il nuovo valore medio è `8`, che individua l'indice cercato. A ogni confronto si elimina metà dei candidati; l'ordinamento dell'array rende valido questo taglio.

In C++ scrivere `left + (right - left) / 2` evita l'overflow della somma quando i bordi sono grandi. Con `vector::size()` fai attenzione ai tipi unsigned e al caso vuoto. In Python gli interi non traboccano, ma l'off-by-one resta.

L'array ordinato non è un dettaglio decorativo: la decisione «vai a sinistra» scarta elementi perché sai come sono ordinati. Se manca l'ordine, cerca una proprietà monotona diversa o usa un'altra struttura.
'''),
    lesson("binary-boundaries", "ricerca", "Lower Bound e Upper Bound: trovare un confine, non un elemento", 3, 25, "intermedio",
           ["primo valore non minore", "ultimo valore ammesso", "duplicati", "intervallo semiaperto"],
           "Trasformare la ricerca binaria in una ricerca del primo punto che soddisfa una condizione.", r'''
Con duplicati, `binary_search` conferma che un valore è presente, ma non individua quale copia. `lower_bound` restituisce il primo elemento non minore del target; `upper_bound` il primo strettamente maggiore. La differenza tra gli iteratori è il numero di occorrenze.

Una formulazione pulita è cercare un punto di taglio in `[0, n)`. Se `nums[mid] < target`, il confine è a destra; altrimenti può essere `mid` o prima. Il ciclo termina quando i due bordi coincidono. Questo schema evita di restituire un indice fuori range quando il target è minore del minimo o maggiore del massimo.

In C++ le due funzioni sono in `<algorithm>`. In Python `bisect_left` e `bisect_right` fanno lo stesso lavoro. Impara il significato del confine: la libreria non elimina la necessità di verificare che l'indice sia valido.
'''),
    lesson("binary-variants", "ricerca", "Ricerca binaria in un array ruotato", 3, 20, "intermedio",
           ["metà ordinata", "intervallo candidato", "array vuoto", "duplicati nel contratto"],
           "Adattare la ricerca quando una sola porzione dell'array è ordinata.", r'''
Una rotazione sposta un prefisso in fondo, ma lascia ordinate le due porzioni risultanti. A ogni passo almeno una metà attorno a `mid` è ordinata: confronta il target con i suoi estremi e scarta l'altra metà soltanto quando puoi dimostrare che lì non c'è.

Il caso vuoto termina subito. Gli array distinti permettono di riconoscere sempre la metà ordinata; se il prompt ammette duplicati, valori uguali agli estremi possono nascondere il punto di rotazione e il caso peggiore può richiedere una scansione lineare. Non promettere `O(log n)` senza specificare il contratto.

Questo resta binary search su elementi. La lezione seguente usa invece la monotonia di una risposta possibile: sono due motivazioni diverse per dimezzare un intervallo, ed è utile saperle distinguere.
'''),
    lesson("binary-answer", "ricerca", "Binary Search on Answer: trovare la soglia fattibile", 3, 25, "intermedio",
           ["dominio delle risposte", "predicato monotono", "estremi fattibili", "costo della verifica"],
           "Cercare il minimo o massimo valore che rende fattibile una soluzione.", r'''
Qui non cerchi un valore già presente nell'array. Definisci un intervallo di risposte candidate e una funzione `feasible(x)` che dica se il vincolo si può rispettare con `x`. Se tutte le risposte oltre una soglia sono fattibili, il risultato è il primo `true` della sequenza `false false true true`.

La parte delicata è giustificare la monotonia e scegliere estremi che contengano davvero la risposta. Nel problema della velocità, per esempio, una velocità più alta non richiede più ore. La verifica simula il lavoro e costa `O(n)`; la ricerca sulle velocità da 1 a `M` porta quindi a `O(n log M)`.

Scrivi e prova il predicato prima del ciclo. Se `feasible(x)` può passare da vero a falso tornando a crescere `x`, la binary search non è applicabile. Puoi usare l'intervallo chiuso `[low, high]`, con una risposta ammissibile dentro: se `feasible(mid)` è vero, poni `high = mid`; altrimenti `low = mid + 1`. Quando `low == high`, quel valore è la prima risposta fattibile. Non mescolare questa convenzione con la variante che mantiene un bordo falso escluso e uno vero incluso.

Con carichi `[3, 6, 7, 11]` e 8 ore, le ore a velocità `v` sono `sum(ceil(carico/v))`. A `v=3` servono 10 ore; a `v=4` ne servono 8. Parti da `[1,11]`: provi 6 (fattibile), poi 3 (non fattibile), poi 5 e 4 (fattibili). Rimane `[4,4]`. In C++ calcola l'arrotondamento con `(carico + v - 1) / v`, usando un tipo abbastanza largo per la somma. Se le ore disponibili sono meno del numero dei carichi non vuoti, neppure la velocità massima è fattibile: chiarisci quel caso nel contratto.
'''),
    lesson("linked-lists", "strutture", "Linked List: cambiare collegamenti senza perdere la lista", 4, 25, "intermedio",
           ["ListNode", "reverse", "merge", "fast/slow", "cycle"],
           "Ragionare su riferimenti e puntatori aggiornando un nodo alla volta.", r'''
Una lista collegata non offre accesso casuale: per arrivare al nodo `k` devi seguire i collegamenti precedenti. Il vantaggio di certi esercizi non è “la lista è più veloce”, ma che puoi cambiare i link senza spostare un blocco di elementi.

Per invertire la lista, conserva tre riferimenti: precedente, corrente e prossimo. Salva il prossimo prima di sovrascrivere `current.next`; altrimenti perdi il resto della struttura. In C++ `nullptr` rappresenta la fine; in Python il campo può essere `None`.

Per fondere due liste ordinate, confronta le teste e collega la minore, avanzando solo quella lista. Per cercare un ciclo, i puntatori lento e veloce si incontrano se il giro esiste. Disegna due o tre nodi e segui il puntatore prima di scrivere la condizione.
'''),
    lesson("recursion", "strutture", "Ricorsione: caso base, progresso e costo dello stack", 4, 20, "intermedio",
           ["caso base", "sottoproblema più piccolo", "stack di chiamate", "memoization"],
           "Scrivere una chiamata ricorsiva che si avvicina davvero alla terminazione.", r'''
Una funzione ricorsiva è una funzione che delega un problema più piccolo a sé stessa. Per fidarti del risultato, trova il caso base e dimostra che ogni chiamata lo raggiunge. In una lista, per esempio, il passo può spostarsi al nodo successivo finché il riferimento diventa nullo.

L'albero delle chiamate rende visibile il costo. Fibonacci ingenuo ricalcola gli stessi numeri molte volte; la memoization conserva il risultato già ottenuto. Così il numero di stati scende da crescita esponenziale a `O(n)`, pagando `O(n)` di memoria.

Il call stack consuma spazio e ha un limite pratico. Per DFS su un grafo profondo, una versione iterativa con stack può essere più robusta. La ricorsione non è automaticamente più elegante: deve rendere più chiara la struttura del problema.
'''),
    lesson("tree-traversal", "strutture", "Alberi binari: preorder, inorder, postorder e livelli", 4, 25, "intermedio",
           ["TreeNode", "visite DFS", "BFS per livelli", "visita vuota"],
           "Scegliere l'ordine di visita in base a quando serve il nodo rispetto ai figli.", r'''
Preorder visita nodo, sinistra, destra; inorder visita sinistra, nodo, destra; postorder visita i figli prima del nodo. Su un BST, inorder restituisce valori in ordine crescente. Il nome è un promemoria dell'istante in cui elabori il nodo rispetto alle chiamate ai figli.

La visita per livelli usa una queue. Memorizza la dimensione della coda prima di iniziare il livello: così elabori esattamente i nodi già presenti, senza includere quelli appena aggiunti. Un albero vuoto è un input normale, non un'eccezione.

In C++ un puntatore `const TreeNode*` rende esplicito che la visita legge l'albero; in Python il nodo può essere una piccola classe con `left` e `right`. Prima di copiare una ricorsione, definisci il valore restituito da ciascun sottoalbero.
'''),
    lesson("bst-paths", "strutture", "BST, profondità e antenati: usare la struttura dichiarata", 4, 25, "intermedio",
           ["proprietà BST", "min/max ricorsivi", "LCA", "percorso radice-foglia"],
           "Sfruttare l'ordinamento dell'albero senza dare per vera una proprietà non garantita.", r'''
In un BST, tutti i valori nel sottoalbero sinistro sono minori della radice e quelli a destra maggiori, se il contratto non ammette duplicati. Per validare l'intero albero, controllare soltanto i figli immediati non basta: ogni nodo deve rispettare i limiti ereditati dagli antenati.

L'antenato comune più basso di due valori in un BST si trova seguendo il confronto con la radice: se entrambi sono a sinistra, scendi a sinistra; se entrambi a destra, vai a destra; quando si separano, sei al punto di incrocio.

Per profondità o somma di un percorso, decidi cosa restituisce la ricorsione: una misura del sottoalbero, oppure un flag di esistenza. Questa scelta previene condizioni speciali sparse e bug quando manca un figlio.
'''),
    lesson("bfs-dfs-grid", "strutture", "BFS e DFS su una griglia: una cella è un nodo", 4, 30, "intermedio",
           ["visited", "quattro direzioni", "componenti", "distanza non pesata"],
           "Trasformare una griglia in un grafo e visitare ogni cella senza ripassarla.", r'''
Una griglia è un grafo implicito: i vicini di `(r,c)` sono coordinate a distanza uno. Una matrice `visited` evita di aggiungere la stessa cella alla frontiera più volte. Controlla i limiti prima di indicizzare, soprattutto ai quattro bordi.

DFS esplora una diramazione in profondità; BFS espande in ordine di distanza. Per il numero di isole, entrambe funzionano. Per il numero minimo di mosse in una griglia senza pesi, la BFS è naturale: la prima visita alla destinazione ha il cammino più corto.

In una griglia `S . # / . . E`, partendo da `S` la prima frontiera contiene la cella sotto e quella a destra. Entrambe portano alla cella centrale, ma segnandola `visited` appena la accodi eviti di inserirla due volte. Da lì `E` è a una mossa: la distanza totale è tre.

Se il runner o il servizio riusa la matrice, non mutarla per segnare le celle visitate senza che il contratto lo consenta. Una struttura `visited` separata costa spazio, ma rende visibile la scelta.
'''),
    lesson("graphs", "strutture", "Grafi: adjacency list, visited e componenti", 4, 25, "intermedio",
           ["lista di adiacenza", "grafo diretto e non diretto", "componenti connesse", "nodi isolati"],
           "Leggere il modello dei collegamenti prima di scegliere la visita.", r'''
Una lista di adiacenza conserva, per ogni nodo, i vicini raggiungibili. Se gli archi sono pochi rispetto a `V²`, occupa molto meno di una matrice. In un grafo non diretto, ogni arco appare in entrambe le liste; dimenticare il verso cambia la domanda.

DFS o BFS marcano un nodo come visto quando lo mettono in frontiera, non quando lo estraggono. Così un nodo raggiunto da più vicini non viene accodato molte volte. Per contare componenti, avvia una visita da ogni nodo non ancora visto; i nodi isolati contano comunque.

La stessa mappa che in Two Sum ricordava gli elementi precedenti ora associa un ID alla sua lista di vicini. La struttura si riusa, ma la ragione è diversa: qui non stai cercando un complemento, stai rappresentando connessioni.
'''),
    lesson("topological-sort", "strutture", "Topological Sort e cicli: dipendenze prima dei dipendenti", 4, 25, "intermedio",
           ["DAG", "indegree", "Kahn", "ciclo"],
           "Verificare se un insieme di prerequisiti ammette un ordine completo.", r'''
Un ordinamento topologico esiste soltanto in un grafo diretto aciclico. Con l'algoritmo di Kahn si inseriscono in coda i nodi con indegree zero; dopo l'estrazione di un nodo, l'indegree dei vicini diminuisce. Se al termine sono stati estratti meno di `V` nodi, una parte del grafo è bloccata da un ciclo.

Con gli archi `A → C`, `B → C`, `C → D`, la coda iniziale contiene `A` e `B`. Dopo averli rimossi, `C` scende a indegree zero; soltanto dopo `C` può entrare `D`. Aggiungere anche `D → A` crea un ciclo: Kahn lascia nodi nella coda d'attesa e l'estrazione finale è incompleta.

L'ordine d'inserimento nella queue può cambiare tra soluzioni valide. Se il test confronta una risposta esatta, il requisito deve chiedere un ordine deterministico; altrimenti controlla le precedenze, non una singola sequenza arbitraria.

Per un task di corsi, rappresenta l'arco come `prerequisito → corso`. Invertire la direzione spesso supera esempi con una sola dipendenza e fallisce su catene di tre nodi.
'''),
    lesson("heap", "avanzato", "Heap e Priority Queue: tenere in vista il prossimo estremo", 5, 25, "intermedio",
           ["min e max heap", "top K", "k-esimo", "streaming"],
           "Mantenere pochi candidati quando non serve ordinare l'intera collezione.", r'''
Un heap non mantiene tutti gli elementi ordinati: garantisce soltanto che l'estremo sia in cima. Se ti servono i `k` valori più grandi, un min-heap di dimensione `k` conserva i migliori finora. Ogni nuovo valore entra; se il heap supera `k`, rimuovi il minimo.

Con `[9, 1, 7, 3, 5]` e `k = 2`, dopo avere inserito `9` e `1` il minimo è `1`. Inserendo `7`, lo elimini e restano `7` e `9`; `3` e `5` vengono poi scartati allo stesso modo. Il valore in cima, `7`, è il secondo più grande: il resto del heap non promette un ordine completo.

Il costo diventa `O(n log k)` e lo spazio `O(k)`, utile quando `k` è piccolo rispetto a `n`. Se ti serve l'ordine completo, ordinare una volta può essere più semplice. Se i dati arrivano in streaming, il heap evita di conservare tutto.

In C++ `priority_queue` è max-heap di default; in Python `heapq` è min-heap. Esplicita i pareggi nel comparatore: il test può aspettarsi una regola deterministica quando due frequenze sono uguali.
'''),
    lesson("greedy", "avanzato", "Greedy e scheduling: dimostrare la scelta locale", 5, 25, "intermedio",
           ["scelta locale", "intervalli", "controesempio", "ordinamento per fine"],
           "Riconoscere un greedy corretto e cercare un caso che lo smentisca.", r'''
Per selezionare il massimo numero di intervalli compatibili, ordina per orario di fine e prendi il primo che non si sovrappone. Finire prima lascia più spazio alle scelte successive. La motivazione è più forte di «prendo quello che sembra migliore»: puoi trasformare una soluzione ottima qualsiasi sostituendo il suo primo intervallo con quello che finisce prima.

Greedy non funziona soltanto perché sembra intuitivo. Per ogni scelta locale, prova a costruire un input piccolo in cui quella scelta brucia una soluzione migliore. Se non riesci a dimostrare l'argomento di scambio o un'altra proprietà, valuta DP o ricerca esaustiva.

Gli intervalli che si toccano dipendono dalla convenzione del prompt. Riusa il criterio già chiarito in Merge Intervals, ma non copiare la stessa condizione se qui «fine uguale a inizio» è consentito.
'''),
    lesson("backtracking", "avanzato", "Backtracking: esplorare scelte e annullarle bene", 5, 25, "intermedio",
           ["decision tree", "subsets e permutazioni", "pruning", "stato ripristinato"],
           "Costruire tutte le risposte valide controllando lo stato che ogni ramo lascia dietro di sé.", r'''
Un backtracking percorre un albero di decisioni: includi o escludi un elemento, scegli il prossimo candidato, oppure chiudi una combinazione quando raggiunge il target. Il costo può crescere esponenzialmente; per questo serve sapere quanti risultati ci si aspetta e quando un ramo non potrà più funzionare.

Il bug più insidioso è condividere la stessa lista risultato tra rami. Quando aggiungi una scelta, dopo la chiamata ricorsiva devi toglierla; altrimenti le combinazioni successive ereditano dati del ramo precedente. In Python `path.copy()` serve quando salvi una risposta finale.

Per permutazioni, un set `used` o una modifica temporanea dell'array impedisce di riutilizzare lo stesso indice. Per subsets, la chiamata successiva parte dall'indice seguente, evitando permutazioni della stessa combinazione.

Con `[1,2]`, parti da `path=[]`. Scegli 1: salvi `[1]`; scegli 2 nel ramo seguente: salvi `[1,2]`; annulla 2, poi annulla 1. Ora il ramo che parte da 2 salva `[2]`. Includi anche `[]`. Se manca un `pop`, il secondo ramo eredita 1; se salvi il riferimento anziché una copia, tutte le risposte cambiano con l'ultimo ramo.

Per Combination Sum con riuso, dopo aver scelto il candidato all'indice `i`, la chiamata ricorsiva riparte da `i`, non da `i+1`. Con candidati positivi puoi fermarti quando il totale supera il target; ordinando, puoi interrompere il ciclo quando anche il più piccolo candidato rimasto è troppo grande. Lo spazio dello stack dipende dalla profondità e l'output può essere esponenziale: il costo non è sempre `O(2^n)` quando puoi riusare una scelta.
'''),
    lesson("dp-memoization", "avanzato", "Dynamic Programming: recursion, memoization, tabulation", 5, 30, "intermedio",
           ["stato", "sottoproblemi sovrapposti", "memoization", "ordine tabulato"],
           "Trasformare ricorsione ripetuta in un calcolo che risolve ogni stato una volta.", r'''
Dynamic programming non è una formula da riconoscere a vista. Parti da una decisione ricorsiva: quale stato descrive abbastanza il problema perché il resto non dipenda dalla storia? In Climbing Stairs lo stato è il gradino `i`; per arrivarci puoi fare uno o due passi.

Se più chiamate chiedono lo stesso stato, i sottoproblemi si sovrappongono. Una mappa di memoization registra la risposta alla prima visita. La tabulation calcola quegli stati in un ordine che rende già disponibile ciò che serve; talvolta basta conservare gli ultimi due valori.

Prima di dichiarare `O(n)`, conta gli stati e il lavoro per stato. Coin Change ha circa `n` importi e prova ogni moneta; Word Break considera posizioni e prefissi possibili. La transizione è il cuore della spiegazione, non il nome “DP”.
'''),
    lesson("dp-models", "avanzato", "DP essenziale: House Robber, Coin Change e Word Break", 5, 30, "intermedio",
           ["massimo con vincolo", "minimo numero di scelte", "segmentazione", "casi impossibili"],
           "Confrontare tre stati DP per vedere come cambia la transizione al cambiare della domanda.", r'''
House Robber decide se prendere la casa `i`: se la prende, la precedente non può essere scelta; altrimenti conserva il massimo già raggiunto. Due variabili possono bastare perché la transizione legge soltanto gli ultimi stati.

Coin Change chiede il minimo numero di monete. Per ogni importo, provi una moneta e riusi la risposta all'importo più piccolo. Il valore “impossibile” va distinto da zero monete: importo zero richiede zero monete, mentre un importo irraggiungibile non ha soluzione.

Word Break considera se il prefisso fino a `i` può essere segmentato. Una posizione è raggiungibile se esiste un taglio precedente raggiungibile e la parte fra i due tagli è nel dizionario. Il set velocizza il lookup, ma il numero dei tagli provati determina il costo.

Scegli il problema DP in base al verbo del prompt: minimo, massimo, numero di modi o esistenza. Stati simili possono avere output diversi e casi base diversi.

### Costruire lo stato su casi piccoli

Per House Robber, `best[i]` è il massimo sulle prime `i` case. `best[0]=0`, `best[1]=valore[0]`, poi `best[i]=max(best[i-1], best[i-2]+valore[i-1])`. Con `[2,7,9,3,1]` ottieni `0,2,7,11,11,12`: ogni passaggio confronta saltare e prendere. Non aggiornare la variabile del penultimo stato prima di averla usata.

Per Coin Change, `dp[x]` è il minimo per raggiungere **esattamente** l'importo `x`; `dp[0]=0`. Da ogni moneta `c <= x` ottieni il candidato `1+dp[x-c]`, se il precedente è raggiungibile. Con monete `[1,3,4]` e importo 6, il greedy prende 4+1+1, mentre lo stato trova 3+3. Questo controesempio spiega perché serve esplorare le scelte, anche senza generare tutte le combinazioni.

Per Word Break, `reachable[i]` riguarda il prefisso `s[:i]`; `reachable[0]=True`. Con `s='catsand'` e parole `{'cat','cats','and'}`, il taglio dopo `cat` lascia `sand`, che non funziona; il taglio dopo `cats` lascia `and`. Non impegnarti nel primo prefisso valido: conserva tutte le posizioni raggiungibili. Per ciascuno stato scrivi significato, caso base, transizione e ordine di calcolo prima del codice.
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
Un Leadership Principle non è uno slogan da inserire in ogni risposta. In un incidente, Customer Obsession porta a capire chi è colpito; Dive Deep chiede dati che distinguano un sintomo da una causa; Bias for Action può giustificare un rollback reversibile mentre la diagnosi continua. La scelta dipende dal rischio e da ciò che sai davvero.

Ownership significa seguire il problema fino a un esito e coinvolgere chi ha il controllo tecnico, anche se il servizio appartiene a un altro team. Earn Trust richiede comunicare l'incertezza e aggiornare gli stakeholder; Insist on the Highest Standards impedisce di dichiarare “risolto” soltanto perché il grafico è tornato normale per cinque minuti.

Amazon elenca oggi sedici Leadership Principles: Customer Obsession, Ownership, Invent and Simplify, Are Right, A Lot, Learn and Be Curious, Hire and Develop the Best, Insist on the Highest Standards, Think Big, Bias for Action, Frugality, Earn Trust, Dive Deep, Have Backbone; Disagree and Commit, Deliver Results, Strive to be Earth's Best Employer e Success and Scale Bring Broad Responsibility. La pagina ufficiale può cambiare; controllala prima di usare i nomi in un colloquio.

Nel lavoro quotidiano entrano in tensione in modi diversi: Frugality chiede di usare bene le risorse, ma non giustifica tagliare una verifica che protegge i clienti; Hire and Develop the Best si vede quando condividi contesto e feedback utili; Strive to be Earth's Best Employer e Success and Scale Bring Broad Responsibility allargano lo sguardo a persone e impatti oltre il team immediato. Non serve forzare ogni principio in ogni decisione.

Negli scenari, valuta ogni azione per impatto sul cliente, qualità delle prove, reversibilità, responsabilità e comunicazione. Poi leggi il ragionamento: non c'è una formula da recitare, e opzioni diverse possono diventare migliori quando cambia il contesto.
'''),
    lesson("work-simulation", "comportamento", "Work Simulation: scegliere un'azione e spiegare il compromesso", 6, 20, "base",
           ["opzioni plausibili", "valutazione di efficacia", "tradeoff", "debrief"],
           "Allenarsi su decisioni di lavoro SDE senza ridurre gli scenari a risposte ovvie.", r'''
Ogni scenario propone azioni che potrebbero sembrare ragionevoli a prima vista. Prima di ordinarle, chiediti quale informazione manca, quale danno potrebbe continuare mentre indaghi e chi deve sapere cosa. A volte la risposta forte unisce una misura immediata reversibile e una verifica più profonda.

Ordina le opzioni dalla più alla meno efficace; DEV//48 non assegna un punteggio né pretende di conoscere la chiave Amazon. Il debrief spiega quale rischio ogni scelta riduce e quale lascia aperto. Se la tua classifica differisce, cerca l'assunzione diversa: gravità, tempo, autorità, impatto o qualità dei dati.

Gli scenari sono originali e ispirati a decisioni quotidiane SDE: release, incidenti, review, requisiti incompleti, colleghi, test instabili, rollback e debito tecnico. Non sono domande reali né materiali riservati.
'''),
    lesson("work-style", "comportamento", "Work Style: familiarizzarsi senza recitare un personaggio", 6, 15, "base",
           ["leggere ogni frase", "coerenza", "riflessione personale", "nessuna manipolazione"],
           "Prendersi il tempo di leggere e rispondere con coerenza, senza ottimizzare un profilo inventato.", r'''
Gli item Work Style possono presentare affermazioni o scelte ripetute. Leggi ogni frase per intero, inclusi avverbi come “sempre” e “raramente”; una parola cambia il significato. Se una risposta richiede un episodio, pensa a un fatto concreto invece di scegliere il tratto che sembra più apprezzato.

La familiarizzazione serve a ridurre errori di fretta e risposte che si contraddicono per distrazione. Non costruire un sistema per manipolare il personality assessment e non memorizzare un profilo ideale. Le note di questa schermata restano private nel database locale e non ricevono punteggio.

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
anche ordine e archi ripetuti. L'esercizio Clone Graph è Extra dopo il Core BFS/DFS.
"""
next(item for item in LESSONS if item["id"] == "sde-l-heap")["body"] += """

### Extra: distanze con pesi positivi

La BFS minimizza il numero di archi; con pesi diversi quel numero non è il costo.
Dijkstra mantiene distanze provvisorie e un min-heap `(distanza,nodo)`. Dal nodo
estratto prova ogni arco: se `distanza[u]+peso < distanza[v]`, aggiorna v e accoda
la nuova coppia. Una vecchia coppia può restare nel heap: scartala se la distanza
non coincide più con quella registrata. Con A->C di costo 10 e A->B->C di costi
1 e 2, C viene prima proposto a 10, poi migliorato a 3. Non segnare C definitivamente
quando lo inserisci. La correttezza della scelta minima richiede pesi non negativi;
il lab Network Delay usa pesi positivi. È un challenge dopo il Core, non una nuova
priorità da inserire nell'ultimo giorno.
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



LESSONS[0]["body"] += """
### Core e Extra nei sei giorni

Il Core è il piano essenziale mostrato nella dashboard: un solo linguaggio DSA,
uno stack repository dopo le due demo iniziali e le attività elencate per ciascun
giorno. Nel Giorno 1 prova la stessa mini-finestra per 8 minuti in entrambe le lingue,
poi scegli con L e studia il toolkit della lingua principale. Non rifare tutta la banca
nell'altra lingua. Nei lab demo premi **USA QUESTO STACK** dopo il confronto.

Giorno 1: orientamento, metodo, scelta, Big-O, array/mappe; mini-prova, Two Sum,
Contains Duplicate, Valid Anagram e le due demo. Giorno 2: pattern lineari e primo
sprint da 25 minuti; poi il lab intermedio dello stack scelto. Giorno 3: stack e
ricerca, un secondo lab Node oppure rifacimento C++ da starter senza suggerimenti.
Giorno 4: liste, alberi, BST, grafi e dipendenze. Giorno 5: heap, greedy,
backtracking e DP, poi Coding Question da 40 minuti. Giorno 6: debugging,
AI Assistant, behavioral, full mock 40+60 ed error review: nessun nuovo pattern DSA.

Riserva ogni giorno 15 minuti al recall delle flashcard e 20 al registro degli errori.
Prova prima le carte del giorno precedente, poi quelle del modulo nuovo; non leggere
subito il retro. Il giorno 6 include altri 30 minuti per scenari e riflessione Work Style.
Le stime sono circa 5h56–6h01, 6h10–6h30, 6h05–6h10, 6h50, 6h40 e 5h35,
secondo lingua e stack, senza pause. Con pause pianifica una giornata di 7–8 ore;
se un argomento richiede più tempo, conserva il Core e rinuncia agli Extra.

Extra sono gli esercizi fuori dal piano, il toolkit non scelto, i lab dell'altro stack,
lo sprint repository standalone prima di ripetere il full mock, e gli altri scenari.
LRU, Dijkstra, Word Ladder, istogramma e DP bidimensionale sono challenge utili dopo
il Core; non devono sottrarre la prima implementazione autonoma dei pattern principali.
Dopo ogni tentativo descrivi brute force, costo, collo di bottiglia, miglioramento e
un caso che smentisce l'implementazione. Il giorno 6 riserva il full mock come prova
chiusa: non studiare prima la soluzione di Three Sum o la repository Parcel.
"""



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
 {"id":"lab-amazon-cpp-demo","module":"repository","title":"Demo repository · C++","minutes":25,"difficulty":"base","description":"Progetto CMake minimo con header, source e test di accettazione. Segui la firma pubblica fino al comportamento osservato.","requirements":["Leggi README, header e test prima del source.","Esegui o ricostruisci expected e actual.","Correggi il filtro degli elementi attivi e il lookup per ID esatto.","Mantieni optional quando l'ID non esiste."],"rubric":["Fix nel source corretto","Attivi/inattivi e ID assente coperti","Nessun cambio non richiesto all'API"],"workspace_template":"amazon_cpp"},
 {"id":"lab-amazon-node-demo","module":"repository","title":"Demo repository · Node.js","minutes":25,"difficulty":"base","description":"Esercizio equivalente al demo C++ in moduli ES: filtro di record, lookup e test senza dipendenze esterne.","requirements":["Individua package.json, export e test.","Usa npm test prima di modificare.","Correggi predicate e confronto dell'identificativo.","Mantieni la funzione di lettura senza mutazioni."],"rubric":["Input preservato","ID esatto e null esplicito","Suite verde"],"workspace_template":"amazon_node"},
 {"id":"lab-amazon-node-async","module":"repository","title":"Repository asincrona · Promise e controller","minutes":35,"difficulty":"intermedio","description":"Una route dipende da un repository asincrono. Segui il valore fra controller, service e test; distingui Promise, null e status HTTP.","requirements":["Disegna il flusso route → service → repository.","Attendi il risultato asincrono prima del controllo not-found.","Restituisci 404 soltanto per un profilo assente e 200 per quello trovato.","Restituisci il valore risolto nel body."],"rubric":["Failure async riprodotta","Branch 200/404 distinti","Fix limitato al contratto"],"workspace_template":"amazon_node"},
 {"id":"lab-amazon-cpp-inventory","module":"repository","title":"Inventario · indice, reference e test","minutes":40,"difficulty":"intermedio","description":"Due source e due header condividono un vector di articoli e un servizio di conteggio stock.","requirements":["Controlla l'indice prima di erase: size è esclusivo.","Cerca l'ID esatto, non il primo maggiore.","Traccia total_units tra dichiarazione e definizione.","Se la rimozione è rifiutata, lascia l'input invariato."],"rubric":["Nessun accesso fuori indice","Header/source coerenti","Test sull'ultimo indice e index == size"],"workspace_template":"amazon_cpp"},
 {"id":"lab-amazon-node-contract","module":"repository","title":"Ordini · filtro e contratto API","minutes":45,"difficulty":"intermedio","description":"Service e controller condividono righe ordine, stato, ordinamento e risposta not-found. I test controllano anche mutazioni.","requirements":["Confronta test, service e controller.","Calcola totale prezzo × quantità e numero righe secondo il contratto.","Includi soltanto lo status richiesto senza riordinare l'input.","Distingui ordine assente da oggetto vuoto e restituisci status coerente."],"rubric":["Nessun side effect su input","Status e JSON coerenti","Test coprono boundary e ordine"],"workspace_template":"amazon_node"},
 {"id":"lab-amazon-mock-repository","module":"repository","title":"Mock repository · Parcel status service","minutes":60,"difficulty":"hard","description":"Prova finale multi-file su route, service e repository. README e test definiscono il comportamento; la cartella non segnala quali file contengono i difetti.","requirements":["Esegui npm test prima di intervenire.","Per ogni failure annota expected, actual e il percorso seguito dal dato.","Formula un'ipotesi verificabile, modifica il minimo indispensabile e conserva i contratti.","Riesegui la suite e controlla i comportamenti adiacenti."],"rubric":["Suite di accettazione completa","Regressioni coperte da test","Diff circoscritto e comprensibile","Nessuna perdita di isolamento o side effect"],"workspace_template":"amazon_node","repository_variants":{"node":"amazon_node","cpp":"amazon_cpp"}},
]

SIMULATIONS = [
 {"id":"sde-sim-coding-25","title":"Coding Sprint · 25 minuti","minutes":25,"kind":"coding","coding_exercise_id":"sde-e-longest-substring","brief":"Prova single-file breve. Definisci il contratto, scegli una struttura e lascia tempo per un edge case. Hint e soluzione restano chiusi durante il timer.","checklist":["Leggi input, output e vincoli","Prova un esempio a mano","Scrivi una soluzione autonoma","Controlla duplicati e minimo","Dichiara tempo e spazio"]},
 {"id":"sde-sim-coding-40","title":"Coding Question · 40 minuti","minutes":40,"kind":"coding","coding_exercise_id":"sde-e-coin-change","brief":"Un problema DSA in editor single-file e quaranta minuti autonomi. Il runner locale controlla solo il codice; non consultare hint, browsing o soluzione durante la prova.","checklist":["Definisci gli stati o l'invariante","Implementa senza assistenza","Esegui i test locali","Confronta costo e vincoli","Ferma al timer"]},
 {"id":"sde-sim-repository-60","title":"Code Repository · 60 minuti","minutes":60,"kind":"repository","repository_lab_id":"lab-amazon-mock-repository","brief":"Apri la repository sconosciuta. README e test sono il punto di partenza; ricostruisci il flusso fra route, service e repository, poi verifica ogni fix.","checklist":["Leggi README e struttura","Esegui npm test","Raggruppa le failure per contratto","Verifica un'ipotesi alla volta","Rilancia tutta la suite"]},
 {"id":"sde-full-mock","title":"Full Mock · Coding 40 + Repository 60","minutes":100,"kind":"full_mock","coding_exercise_id":"sde-e-three-sum","repository_lab_id":"lab-amazon-mock-repository","brief":"Due sezioni in sequenza: quaranta minuti per un problema DSA, poi stop e sessanta minuti autonomi per una repository multi-file. Il tempo inutilizzato non passa alla seconda sezione.","checklist":["Avvia quando sei pronto","Coding single-file senza aiuti","Il primo timer si chiude al cambio","Leggi README e test del repository","Concludi e annota prove e incertezze"]},
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
    lessons=[]
    for item in LESSONS:
        record={key:value for key,value in item.items() if key!="body"}
        path=CONTENT/record["body_file"]
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(item["body"],encoding="utf-8")
        lessons.append(record)
    referenced_bodies = {CONTENT / item["body_file"] for item in lessons}
    for stale in LESSONS_DIR.glob("sde-l-*.md"):
        if stale not in referenced_bodies:
            stale.unlink()
    exercise_by_id = {item["id"]: item for item in EXERCISES}
    exercises = list(exercise_by_id.values())
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
        "name":"Amazon SDE-I OA Bootcamp","track_id":"amazon-sde-oa","version":"1.0","language":"it",
        "estimated_hours":round(catalog_minutes/60,1),"estimated_core_hours":round(core_plan_minutes/60,1),"study_plan":STUDY_PLAN,
        "assessment_note":"Il mock 40+60 è un formato di pratica richiesto; assessment reali variano per ruolo e paese. Fa fede l'invito ricevuto.",
        "sources":["https://www.amazon.jobs/content/cs/how-we-hire/university/sde-oa","https://www.amazon.jobs/content/en-gb/our-workplace/leadership-principles","https://candidatesupport.hackerrank.com/articles/8606305957-taking-front-end-back-end-full-stack-and-mobile-developer-assessments","https://candidatesupport.hackerrank.com/articles/7634558376-ai-assistant-in-tests","https://docs.python.org/3/tutorial/datastructures.html","https://isocpp.org/wiki/faq/containers"]
      },
      "modules":MODULES,"lessons":lessons,"exercises":exercises,"labs":LABS,"flashcards":build_flashcards(),
      "simulations":SIMULATIONS,"work_scenarios":build_scenarios(),"work_style":WORK_STYLE
    }
    CATALOG_FILE.write_text(json.dumps(raw,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:len(raw[key]) for key in ("modules","lessons","exercises","labs","flashcards","simulations","work_scenarios","work_style")},ensure_ascii=False))
    return raw


if __name__ == "__main__":
    build_catalog()
