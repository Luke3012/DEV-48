# Dynamic Programming: recursion, memoization, tabulation

Dynamic programming non è una formula da riconoscere a vista. Parti da una decisione ricorsiva: quale stato descrive abbastanza il problema perché il resto non dipenda dalla storia? In Climbing Stairs lo stato è il gradino `i`; per arrivarci puoi fare uno o due passi.

Se più chiamate chiedono lo stesso stato, i sottoproblemi si sovrappongono. Una mappa di memoization registra la risposta alla prima visita. La tabulation calcola quegli stati in un ordine che rende già disponibile ciò che serve; talvolta basta conservare gli ultimi due valori.

Prima di dichiarare `O(n)`, conta gli stati e il lavoro per stato. Coin Change ha circa `n` importi e prova ogni moneta; Word Break considera posizioni e prefissi possibili. La transizione è il cuore della spiegazione, non il nome “DP”.
