# Python 3 essenziale per gli esercizi DSA

Per un problema su array, `list[int]` basta quasi sempre. `enumerate(nums)` ti dà indice e valore senza una variabile contatore da aggiornare; `range(left, right)` esclude `right`, dettaglio che vale la pena controllare quando gli indici sono già stanchi. Lo slicing `s[::-1]` crea una copia invertita: comodo per una verifica, costoso se la stringa è enorme e la copia non serve.

`dict` e `set` risolvono membership e conteggi: `counts[x] = counts.get(x, 0) + 1`. Quando il default è una collezione, `defaultdict(list)` evita il ramo «chiave vista per la prima volta». `Counter` è ottimo per frequenze, ma anche sotto timer occorre saper spiegare cosa costa ogni passaggio.

Una lista va bene come stack con `append` e `pop`. Per BFS usa `collections.deque` e `popleft()`: togliere il primo elemento da una lista sposta il resto. `heapq` espone un min-heap; per ottenere un max-heap con numeri interi, spesso basta inserire `-value`.

`sorted(values)` crea una nuova lista; `values.sort()` modifica quella esistente. Preferisci la prima quando l'input fa parte del contratto e non deve cambiare. Comprehension e lambda sono strumenti, non una gara a scrivere la riga più corta.

### Esempio svolto: costruire un dizionario passo dopo passo

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

Infine confronta `sorted(values)`, che crea una nuova lista, con `values.sort()`, che modifica quella esistente. Prima di usare un'API, chiediti sempre quale dato cambia e quale rimane. Questo piccolo controllo evita bug difficili da vedere quando il caso di prova contiene un solo elemento.

**Da ricordare.** Scegli il contenitore in base all'operazione richiesta e ricorda quando un'API modifica o copia i dati. **Per praticare:** Mini-prova: finestra con somma massima; Due valori che completano il target.