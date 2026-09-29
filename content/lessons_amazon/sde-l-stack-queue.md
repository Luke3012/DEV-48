# Stack, Queue e Deque: scegliere l'ordine delle visite

Uno stack risponde all'ultimo elemento aggiunto; una queue al primo. Le parentesi sono LIFO: l'ultima parentesi aperta deve chiudersi per prima. La BFS è FIFO: i nodi a distanza `d` entrano in coda prima di quelli a distanza `d+1`, perciò il primo arrivo è un cammino minimo nei grafi non pesati.

Il tipo di contenitore evita lavoro superfluo. In Python `deque.popleft()` non sposta gli elementi rimasti. In C++ `queue.pop()` rimuove la testa e `front()` la legge; non invertire l'ordine delle due operazioni.

Per parentesi corrette, scarta subito una chiusura senza apertura e alla fine controlla che lo stack sia vuoto. Se verifichi soltanto il conteggio delle parentesi, `)(` passa per errore: il loro ordine è proprio l'informazione che lo stack conserva.
