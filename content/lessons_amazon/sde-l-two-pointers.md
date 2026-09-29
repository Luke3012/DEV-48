# Two Pointers: far incontrare due scansioni

Con un array ordinato, due indici ai bordi possono cercare una somma senza provare tutte le coppie. Se la somma è troppo piccola, muovere il sinistro verso destra è l'unico modo per aumentarla; se è troppo grande, arretrare il destro la riduce. Ogni passo scarta una famiglia di coppie, non un'ipotesi a caso.

Il pattern fast/slow ha un'altra funzione. Un puntatore avanza di uno, l'altro di due; incontrarsi rivela un ciclo, oppure il lento può raggiungere il punto medio mentre il veloce percorre una lista. Non richiede un array ordinato, ma ha bisogno di una relazione tra i passi.

In-place deduplication usa spesso un indice di scrittura e uno di lettura. L'indice lento indica il prefisso già pulito; quello veloce esplora il resto. Se non riesci a dire cosa garantisce la zona tra i due, fermati prima di codificare.
