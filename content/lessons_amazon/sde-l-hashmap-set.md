# HashMap e Set: memoria utile, non magia

La mappa è utile quando puoi nominare la domanda che vuoi fare a ogni elemento: «ho già visto il suo complemento?», «quante volte è comparsa questa lettera?», «a quale gruppo appartiene questa firma?». In Two Sum, per il valore `x` cerchi `target - x` tra gli indici già incontrati. Salvare l'indice solo dopo la ricerca evita di usare lo stesso elemento due volte.

Un set risponde a «esiste già?» senza associarci un conteggio. Una mappa di frequenze conta con `counts[x] += 1`. Per raggruppare parole anagramma, una chiave possibile è la tupla delle 26 frequenze; ordinare ogni parola funziona pure, ma cambia il costo.

Le operazioni hash sono in media `O(1)`, non una garanzia matematica per ogni caso. Se serve ordine, usa una struttura ordinata e accetta `O(log n)`. Quando la mappa memorizza prefissi, stati o nodi, dichiara anche quanta memoria può crescere.

Un errore ricorrente è sovrascrivere una frequenza quando il problema richiede accumularla. Un altro è interrogare una mappa mutandola senza volerlo: in C++ `operator[]` inserisce una chiave mancante; `find` permette un lookup che non cambia il contenitore.
