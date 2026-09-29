# Array e stringhe: scansione, indici e mutazioni

Una scansione ha tre domande concrete: da dove parto, quando mi fermo, cosa significa l'indice corrente? Scrivi l'intervallo `[left, right)` quando il bordo destro non è incluso. La sua lunghezza è `right - left`; l'ultimo elemento è `right - 1`. Questa convenzione si incastra bene con slicing Python e iteratori C++.

Se devi invertire un array senza spazio extra, scambia gli estremi e avvicinali. Se devi soltanto restituire una versione ordinata, una copia chiarisce il contratto. `sort` in-place è un'altra scelta: utile quando il prompt permette di modificare l'input, rischiosa quando un test successivo riusa i dati.

Per stringhe, distinguere una sequenza di byte da un carattere Unicode completo può essere importante fuori dalle interview standard. Nei problemi qui useremo caratteri ASCII dichiarati nel prompt, così l'attenzione resta sull'algoritmo. Gli indici restano comunque facili da sbagliare: prova sempre primo, ultimo e lunghezza zero.
