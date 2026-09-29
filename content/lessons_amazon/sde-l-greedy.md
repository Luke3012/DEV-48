# Greedy e scheduling: dimostrare la scelta locale

Per selezionare il massimo numero di intervalli compatibili, ordina per orario di fine e prendi il primo che non si sovrappone. Finire prima lascia più spazio alle scelte successive. La motivazione è più forte di «prendo quello che sembra migliore»: puoi trasformare una soluzione ottima qualsiasi sostituendo il suo primo intervallo con quello che finisce prima.

Greedy non funziona soltanto perché sembra intuitivo. Per ogni scelta locale, prova a costruire un input piccolo in cui quella scelta brucia una soluzione migliore. Se non riesci a dimostrare l'argomento di scambio o un'altra proprietà, valuta DP o ricerca esaustiva.

Gli intervalli che si toccano dipendono dalla convenzione del prompt. Riusa il criterio già chiarito in Merge Intervals, ma non copiare la stessa condizione se qui «fine uguale a inizio» è consentito.
