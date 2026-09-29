# Prefix Sum e HashMap per intervalli e sottosequenze

Definisci `prefix[i]` come la somma dei primi `i` elementi. La somma dell'intervallo `[left, right)` è `prefix[right] - prefix[left]`. Con un prefisso iniziale pari a zero, anche gli intervalli che partono dal primo elemento seguono la stessa formula.

Per contare subarray con somma `k`, mentre avanzi con somma corrente `s`, cerchi quante volte è apparso `s - k`. La mappa dei prefissi si inizializza con `{0: 1}`: senza quella voce perdi i segmenti che cominciano a indice zero. Qui torna la stessa idea di Two Sum: la mappa ricorda un valore già visto che completa quello corrente.

La differenza tra due prefissi funziona anche con numeri negativi, mentre la sliding window per somme spesso no. Questo è un buon esempio di pattern riconosciuto dal motivo matematico, non dalla parola “subarray”.
