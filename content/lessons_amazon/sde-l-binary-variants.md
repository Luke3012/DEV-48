# Ricerca binaria in un array ruotato

Una rotazione sposta un prefisso in fondo, ma lascia ordinate le due porzioni risultanti. A ogni passo almeno una metà attorno a `mid` è ordinata: confronta il target con i suoi estremi e scarta l'altra metà soltanto quando puoi dimostrare che lì non c'è.

Il caso vuoto termina subito. Gli array distinti permettono di riconoscere sempre la metà ordinata; se il prompt ammette duplicati, valori uguali agli estremi possono nascondere il punto di rotazione e il caso peggiore può richiedere una scansione lineare. Non promettere `O(log n)` senza specificare il contratto.

Questo resta binary search su elementi. La lezione seguente usa invece la monotonia di una risposta possibile: sono due motivazioni diverse per dimezzare un intervallo, ed è utile saperle distinguere.
