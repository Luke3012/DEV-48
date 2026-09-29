# Linked List: cambiare collegamenti senza perdere la lista

Una lista collegata non offre accesso casuale: per arrivare al nodo `k` devi seguire i collegamenti precedenti. Il vantaggio di certi esercizi non è “la lista è più veloce”, ma che puoi cambiare i link senza spostare un blocco di elementi.

Per invertire la lista, conserva tre riferimenti: precedente, corrente e prossimo. Salva il prossimo prima di sovrascrivere `current.next`; altrimenti perdi il resto della struttura. In C++ `nullptr` rappresenta la fine; in Python il campo può essere `None`.

Per fondere due liste ordinate, confronta le teste e collega la minore, avanzando solo quella lista. Per cercare un ciclo, i puntatori lento e veloce si incontrano se il giro esiste. Disegna due o tre nodi e segui il puntatore prima di scrivere la condizione.
