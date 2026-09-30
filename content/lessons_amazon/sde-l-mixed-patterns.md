# Problemi misti: scegliere il pattern partendo dal vincolo

Tre problemi possono dire «trova una coppia» e richiedere approcci diversi. Se l'array è ordinato, due puntatori possono bastare; se devi restituire indici in input non ordinato, una mappa può aiutare; se vuoi tutte le triple uniche, l'ordinamento e la gestione dei duplicati sono parte della soluzione.

Per ogni nuovo enunciato scrivi una versione semplice, poi cerca il collo di bottiglia. Se l'input è 80 elementi, un doppio ciclo può essere una scelta ragionevole. Se sale a 80.000, devi spiegare come scendi a un passaggio lineare o `n log n`.

Un test utile distingue due approcci concorrenti. Per una soluzione hash, usa un complemento che non esiste nell'input lungo: un algoritmo quadratico non si ferma al primo elemento. Per una finestra, usa un caso che obbliga il bordo sinistro a muoversi più di una volta.

### Stesso lessico, invarianti diverse

Considera tre richieste di coppia: «trova una coppia in un array crescente» suggerisce due puntatori perché l'ordine elimina candidati; «restituisci due indici nell'array originale non ordinato» può usare una mappa senza perdere l'identità degli indici; «trova tutte le triple uniche» richiede gestire duplicati oltre a trovare somme. La parola “coppia” da sola non seleziona il pattern.

Un modo rapido per decidere è annotare input, output, vincolo di ordine e dimensione: se l'input è piccolo, il doppio ciclo può essere chiaro e sufficiente; se n=100.000 e il prompt richiede tempo lineare atteso, memorizzare gli elementi visti cambia la scala. Prova poi a rompere la tua ipotesi: un duplicato, nessuna soluzione, valori negativi oppure molti dati senza risposta.

Le esercitazioni più utili per il confronto sono due con requisiti vicini ma invarianti diverse: **Two Sum** e **Two Sum Sorted**, poi **Subarray Sum** e **Merge Intervals**. Prima spiega perché il movimento o la memoria è valido; solo dopo scrivi il ciclo.

**Da ricordare.** Il pattern deriva da un invariante e dal contratto, non da una parola chiave isolata. **Per praticare:** Due valori che completano il target; Coppia con somma in una lista ordinata; Contare segmenti contigui con somma k.