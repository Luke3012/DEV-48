# Dai primi due minuti a una soluzione verificabile

Quando il cronometro parte, la tentazione è digitare subito. Fai invece un esempio piccolo con le mani. Per una lista `[4, 1, 7]` e una ricerca del valore `1`, scrivi quale risultato deve uscire e cosa succede se la lista è vuota. Una domanda fatta ora costa pochi secondi; una supposizione errata può costarti l'intero tentativo.

Poi scegli la versione più semplice che rispetta il contratto e misurane il costo. Se la prima idea confronta ogni coppia, con `n` elementi esegue circa `n²` confronti. Non è un difetto se `n` è piccolo; diventa un problema quando il vincolo arriva a decine di migliaia. Solo a quel punto cerca l'informazione che manca: una mappa, un ordinamento, una finestra mantenuta tra un passo e il successivo.

Mentre implementi, tieni un'invariante in una frase: «la mappa contiene gli elementi già attraversati». Dopo ogni cambiamento, verifica un caso che avrebbe fatto fallire la versione precedente. Se il codice non va, riduci l'input e formula una causa precisa; cambiare tre righe insieme cancella le prove.

Un ritmo realistico per 40 minuti è: chiarimento e casi, 4–6 minuti; scelta e implementazione, circa 25; test manuali e rifinitura, il tempo restante. Se una strada è bloccata, conserva la soluzione parziale e prova un'alternativa con costo chiaro.
