# BST, profondità e antenati: usare la struttura dichiarata

In un BST, tutti i valori nel sottoalbero sinistro sono minori della radice e quelli a destra maggiori, se il contratto non ammette duplicati. Per validare l'intero albero, controllare soltanto i figli immediati non basta: ogni nodo deve rispettare i limiti ereditati dagli antenati.

L'antenato comune più basso di due valori in un BST si trova seguendo il confronto con la radice: se entrambi sono a sinistra, scendi a sinistra; se entrambi a destra, vai a destra; quando si separano, sei al punto di incrocio.

Per profondità o somma di un percorso, decidi cosa restituisce la ricorsione: una misura del sottoalbero, oppure un flag di esistenza. Questa scelta previene condizioni speciali sparse e bug quando manca un figlio.
