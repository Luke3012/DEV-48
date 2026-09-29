# Binary Search on Answer: trovare la soglia fattibile

Qui non cerchi un valore già presente nell'array. Definisci un intervallo di risposte candidate e una funzione `feasible(x)` che dica se il vincolo si può rispettare con `x`. Se tutte le risposte oltre una soglia sono fattibili, il risultato è il primo `true` della sequenza `false false true true`.

La parte delicata è giustificare la monotonia e scegliere estremi che contengano davvero la risposta. Nel problema della velocità, per esempio, una velocità più alta non richiede più ore. La verifica simula il lavoro e costa `O(n)`; la ricerca sulle velocità da 1 a `M` porta quindi a `O(n log M)`.

Scrivi e prova il predicato prima del ciclo. Se `feasible(x)` può passare da vero a falso tornando a crescere `x`, la binary search non è applicabile. Puoi usare l'intervallo chiuso `[low, high]`, con una risposta ammissibile dentro: se `feasible(mid)` è vero, poni `high = mid`; altrimenti `low = mid + 1`. Quando `low == high`, quel valore è la prima risposta fattibile. Non mescolare questa convenzione con la variante che mantiene un bordo falso escluso e uno vero incluso.

Con carichi `[3, 6, 7, 11]` e 8 ore, le ore a velocità `v` sono `sum(ceil(carico/v))`. A `v=3` servono 10 ore; a `v=4` ne servono 8. Parti da `[1,11]`: provi 6 (fattibile), poi 3 (non fattibile), poi 5 e 4 (fattibili). Rimane `[4,4]`. In C++ calcola l'arrotondamento con `(carico + v - 1) / v`, usando un tipo abbastanza largo per la somma. Se le ore disponibili sono meno del numero dei carichi non vuoti, neppure la velocità massima è fattibile: chiarisci quel caso nel contratto.
