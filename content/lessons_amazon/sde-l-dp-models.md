# DP essenziale: House Robber, Coin Change e Word Break

House Robber decide se prendere la casa `i`: se la prende, la precedente non può essere scelta; altrimenti conserva il massimo già raggiunto. Due variabili possono bastare perché la transizione legge soltanto gli ultimi stati.

Coin Change chiede il minimo numero di monete. Per ogni importo, provi una moneta e riusi la risposta all'importo più piccolo. Il valore “impossibile” va distinto da zero monete: importo zero richiede zero monete, mentre un importo irraggiungibile non ha soluzione.

Word Break considera se il prefisso fino a `i` può essere segmentato. Una posizione è raggiungibile se esiste un taglio precedente raggiungibile e la parte fra i due tagli è nel dizionario. Il set velocizza il lookup, ma il numero dei tagli provati determina il costo.

Scegli il problema DP in base al verbo del prompt: minimo, massimo, numero di modi o esistenza. Stati simili possono avere output diversi e casi base diversi.

### Costruire lo stato su casi piccoli

Per House Robber, `best[i]` è il massimo sulle prime `i` case. `best[0]=0`, `best[1]=valore[0]`, poi `best[i]=max(best[i-1], best[i-2]+valore[i-1])`. Con `[2,7,9,3,1]` ottieni `0,2,7,11,11,12`: ogni passaggio confronta saltare e prendere. Non aggiornare la variabile del penultimo stato prima di averla usata.

Per Coin Change, `dp[x]` è il minimo per raggiungere **esattamente** l'importo `x`; `dp[0]=0`. Da ogni moneta `c <= x` ottieni il candidato `1+dp[x-c]`, se il precedente è raggiungibile. Con monete `[1,3,4]` e importo 6, il greedy prende 4+1+1, mentre lo stato trova 3+3. Questo controesempio spiega perché serve esplorare le scelte, anche senza generare tutte le combinazioni.

Per Word Break, `reachable[i]` riguarda il prefisso `s[:i]`; `reachable[0]=True`. Con `s='catsand'` e parole `{'cat','cats','and'}`, il taglio dopo `cat` lascia `sand`, che non funziona; il taglio dopo `cats` lascia `and`. Non impegnarti nel primo prefisso valido: conserva tutte le posizioni raggiungibili. Per ciascuno stato scrivi significato, caso base, transizione e ordine di calcolo prima del codice.
