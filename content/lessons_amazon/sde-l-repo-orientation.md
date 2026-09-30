# Orientarsi in una repository sconosciuta

L'apertura dei file in ordine alfabetico non è una strategia efficace. La struttura iniziale si ricostruisce da manifest, script, README, cartelle principali e test. Dal simbolo o dalla route citata nel requisito si può seguire una chiamata alla volta e disegnare il percorso dei dati, per esempio `route → controller → service → repository`.

Il README descrive come si avvia il progetto, ma il comportamento reale può essere nei test. Prima di cambiare codice, esegui il comando dichiarato e conserva il primo errore completo. Un log lungo contiene spesso una causa utile nelle prime righe o un test con expected e actual molto specifici.

La Code Repository Question verifica la manutenzione di un progetto locale: il file difettoso non è noto in anticipo e lo spazio di ricerca va ridotto con indizi verificabili. Un orientamento iniziale accurato può evitare modifiche premature al file sbagliato.
