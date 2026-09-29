# Python 3 essenziale per l'interview

Per un problema su array, `list[int]` basta quasi sempre. `enumerate(nums)` ti dà indice e valore senza una variabile contatore da aggiornare; `range(left, right)` esclude `right`, dettaglio che vale la pena controllare quando gli indici sono già stanchi. Lo slicing `s[::-1]` crea una copia invertita: comodo per una verifica, costoso se la stringa è enorme e la copia non serve.

`dict` e `set` risolvono membership e conteggi: `counts[x] = counts.get(x, 0) + 1`. Quando il default è una collezione, `defaultdict(list)` evita il ramo «chiave vista per la prima volta». `Counter` è ottimo per frequenze, ma per un colloquio devi comunque saper spiegare cosa costa ogni passaggio.

Una lista va bene come stack con `append` e `pop`. Per BFS usa `collections.deque` e `popleft()`: togliere il primo elemento da una lista sposta il resto. `heapq` espone un min-heap; per ottenere un max-heap con numeri interi, spesso basta inserire `-value`.

`sorted(values)` crea una nuova lista; `values.sort()` modifica quella esistente. Preferisci la prima quando l'input fa parte del contratto e non deve cambiare. Comprehension e lambda sono strumenti, non una gara a scrivere la riga più corta.
