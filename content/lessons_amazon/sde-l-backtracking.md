# Backtracking: esplorare scelte e annullarle bene

Un backtracking percorre un albero di decisioni: includi o escludi un elemento, scegli il prossimo candidato, oppure chiudi una combinazione quando raggiunge il target. Il costo può crescere esponenzialmente; per questo serve sapere quanti risultati ci si aspetta e quando un ramo non potrà più funzionare.

Il bug più insidioso è condividere la stessa lista risultato tra rami. Quando aggiungi una scelta, dopo la chiamata ricorsiva devi toglierla; altrimenti le combinazioni successive ereditano dati del ramo precedente. In Python `path.copy()` serve quando salvi una risposta finale.

Per permutazioni, un set `used` o una modifica temporanea dell'array impedisce di riutilizzare lo stesso indice. Per subsets, la chiamata successiva parte dall'indice seguente, evitando permutazioni della stessa combinazione.

Con `[1,2]`, parti da `path=[]`. Scegli 1: salvi `[1]`; scegli 2 nel ramo seguente: salvi `[1,2]`; annulla 2, poi annulla 1. Ora il ramo che parte da 2 salva `[2]`. Includi anche `[]`. Se manca un `pop`, il secondo ramo eredita 1; se salvi il riferimento anziché una copia, tutte le risposte cambiano con l'ultimo ramo.

Per Combination Sum con riuso, dopo aver scelto il candidato all'indice `i`, la chiamata ricorsiva riparte da `i`, non da `i+1`. Con candidati positivi puoi fermarti quando il totale supera il target; ordinando, puoi interrompere il ciclo quando anche il più piccolo candidato rimasto è troppo grande. Lo spazio dello stack dipende dalla profondità e l'output può essere esponenziale: il costo non è sempre `O(2^n)` quando puoi riusare una scelta.
