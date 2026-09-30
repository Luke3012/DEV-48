# Orientarsi in una repository sconosciuta

L'apertura dei file in ordine alfabetico non è una strategia efficace. La struttura iniziale si ricostruisce da manifest, script, README, cartelle principali e test. Dal simbolo o dalla route citata nel requisito si può seguire una chiamata alla volta e disegnare il percorso dei dati, per esempio `route → controller → service → repository`.

Il README descrive come si avvia il progetto, ma il comportamento reale può essere nei test. Prima di cambiare codice, esegui il comando dichiarato e conserva il primo errore completo. Un log lungo contiene spesso una causa utile nelle prime righe o un test con expected e actual molto specifici.

La Code Repository Question verifica la manutenzione di un progetto locale: il file difettoso non è noto in anticipo e lo spazio di ricerca va ridotto con indizi verificabili. Un orientamento iniziale accurato può evitare modifiche premature al file sbagliato.

### Seguire un requisito tra file

Supponi che `GET /orders/42` restituisca un ordine archiviato. Parti dal test che dichiara se gli ordini archiviati vadano nascosti; poi segui il simbolo della route al controller, al service e al repository. Un disegno possibile è `routes → controller → orderService → repository`; annota il tipo e il valore a ogni freccia. Se il test riceve l'ordine, controlla se il filtro manca nel service o se la route richiama un servizio diverso. Non leggere tutto il repository per intero: README, manifest, test e ricerca del simbolo riducono lo spazio.

Esegui prima il comando di test indicato dal progetto e conserva l'errore completo. Un README può essere incompleto o non aggiornato; confrontalo con `package.json`, CMake e comandi effettivi. Le cartelle `test`, `src`, `include` o `app` suggeriscono ruoli, ma i riferimenti fra file danno la prova del flusso.

**Da ricordare.** La repository è una rete di contratti e chiamate: parti dal test e segui un simbolo fino alla produzione del valore. **Per praticare:** Repository di esempio · C++; Repository di esempio · Node.js.