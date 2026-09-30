# Scegliere il linguaggio per i 40 minuti

La scelta tra Python e C++ dipende dalla familiarità operativa, dalla velocità di scrittura e dalla capacità di individuare gli errori. Una prova breve sugli stessi casi offre un confronto più utile della sola impressione o della conoscenza teorica del linguaggio.

L'esercizio propone una lista di interi e una dimensione `k`; la funzione deve restituire la somma massima di `k` elementi consecutivi. Dopo la somma della prima finestra, il totale si aggiorna sottraendo l'elemento in uscita e aggiungendo quello in entrata, senza ricalcolare ogni somma. La prova dura 8 minuti per linguaggio, con gli stessi input e casi e un editor vuoto.

Per ciascun linguaggio si possono confrontare il tempo di scrittura, le consultazioni di sintassi, gli errori introdotti e la rapidità nel verificare lista vuota, un solo elemento e finestre che avanzano. È preferibile la soluzione che lascia più tempo al ragionamento, non quella che appare più elegante sulla carta.

La scelta può restare provvisoria: aggiornala dopo aver confrontato altri esercizi e il tempo necessario a correggere gli errori. Python e C++ consentono entrambi di implementare gli stessi pattern; la familiarità quotidiana con il compilatore e le librerie conta più della brevità teorica della sintassi.

### Esempio svolto a mano: aggiornare una finestra

Prima di confrontare Python e C++, seguiamo un input piccolo che non è quello della mini-prova: `[1, 3, 2, 5]`, con finestre di `k=2` elementi consecutivi. La prima finestra è `[1, 3]`, la somma è 4. Per spostarla a destra non rifacciamo tutta l'addizione: togliamo il valore che esce e aggiungiamo quello che entra.

| Finestra | Calcolo rispetto alla precedente | Somma |
| --- | --- | ---: |
| `[1, 3]` | `1 + 3` | 4 |
| `[3, 2]` | `4 - 1 + 2` | 5 |
| `[2, 5]` | `5 - 3 + 5` | 7 |

Il massimo dell'esempio è 7. Nota il controllo manuale: le finestre sono tre, quindi devono comparire esattamente tre somme. Se il tuo programma ne producesse due o quattro, sospetteresti subito un errore nel confine del ciclo.

Ripeti poi la stessa mini-prova in entrambi i linguaggi. Annota non solo il tempo di scrittura, ma anche se hai aggiornato correttamente la finestra e quanto hai impiegato a trovare un eventuale errore. Così confronti la familiarità reale con l'editor, gli indici e gli strumenti, non la quantità di caratteri digitati.

**Da ricordare.** Scegli sulla base della soluzione corretta e del tempo rimasto per verificarla, non della brevità del codice. **Per praticare:** Mini-prova: finestra con somma massima.