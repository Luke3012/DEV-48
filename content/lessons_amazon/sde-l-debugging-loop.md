# Dal bug distribuito al fix minimo

Un bug tra più file raramente si risolve cercando una riga “sbagliata”. Confronta requisito e comportamento, individua un input piccolo che li separa e annota dove il dato entra, cambia e viene restituito. Se la failure è su un filtro, controlla sia il predicato sia il punto in cui quel filtro viene applicato.

Modifica il componente responsabile più vicino alla causa. Un fallback aggiunto in una route può far passare il test senza correggere il service; la stessa anomalia riapparirà in un'altra chiamata. Dopo il test mirato, riesegui la suite intera e guarda i file modificati.

Per gli edge case pensa a `null`, lista vuota, ultimo indice, ID assente, Promise rifiutata e input riutilizzato dopo la chiamata. Se la funzione deve essere pura, confronta l'input con una copia prima e dopo.
