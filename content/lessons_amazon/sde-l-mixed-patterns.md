# Problemi misti: scegliere il pattern partendo dal vincolo

Tre problemi possono dire «trova una coppia» e richiedere approcci diversi. Se l'array è ordinato, due puntatori possono bastare; se devi restituire indici in input non ordinato, una mappa può aiutare; se vuoi tutte le triple uniche, l'ordinamento e la gestione dei duplicati sono parte della soluzione.

Per ogni nuovo enunciato scrivi una versione semplice, poi cerca il collo di bottiglia. Se l'input è 80 elementi, un doppio ciclo può essere una scelta ragionevole. Se sale a 80.000, devi spiegare come scendi a un passaggio lineare o `n log n`.

Un test utile distingue due approcci concorrenti. Per una soluzione hash, usa un complemento che non esiste nell'input lungo: un algoritmo quadratico non si ferma al primo elemento. Per una finestra, usa un caso che obbliga il bordo sinistro a muoversi più di una volta.
