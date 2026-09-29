# Big-O e vincoli: capire quando una risposta è troppo lenta

Se raddoppi `n`, un passaggio lineare fa circa il doppio del lavoro; due cicli annidati spesso ne fanno quattro volte tanto. Quella differenza diventa visibile quando i vincoli passano da 100 a 100.000. L'esempio non deve essere cronometrato al millisecondo: serve a scartare una famiglia di soluzioni incompatibile con la scala.

Una ricerca binaria dimezza lo spazio a ogni confronto e richiede `O(log n)`, ma l'array deve essere ordinato o la condizione deve essere monotona. Ordinare prima costa `O(n log n)`. Una mappa può portare lookup medio a `O(1)` pagando spazio `O(n)`; non è «gratis», è uno scambio esplicito.

Quando leggi i constraints, cerca numeri massimi, valori negativi, duplicati e input vuoti. Se `n` arriva a 200.000, `O(n²)` è quasi sempre un segnale d'allarme. Un esercizio del catalogo include un caso grande costruito proprio per separare una scansione lineare da un doppio ciclo.

La complessità spaziale conta quanto quella temporale: una soluzione che copia una matrice può passare i test piccoli e superare la memoria. Specifica se lo spazio ausiliario cresce con l'input o se stai modificando la struttura ricevuta.
