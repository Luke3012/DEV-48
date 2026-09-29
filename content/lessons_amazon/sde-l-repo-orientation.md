# Orientarsi in una repository che non hai mai visto

Non aprire tutti i file in ordine alfabetico. Parti dalla struttura: manifest e script, README, cartelle principali, test. Cerca il simbolo o la route menzionata nel requisito, poi segui una chiamata alla volta. Il tuo obiettivo è disegnare un percorso breve, per esempio `route → controller → service → repository`.

Il README descrive come si avvia il progetto, ma il comportamento reale può essere nei test. Prima di cambiare codice, esegui il comando dichiarato e conserva il primo errore completo. Un log lungo contiene spesso una causa utile nelle prime righe o un test con expected e actual molto specifici.

La Code Repository Question è una prova di manutenzione locale: non devi sapere già quale file è rotto. Devi ridurre lo spazio di ricerca usando indizi verificabili. Tre minuti per orientarsi bene possono risparmiarne venti di modifiche al file sbagliato.
