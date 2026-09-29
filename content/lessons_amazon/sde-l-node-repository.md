# Repository Node.js: package, moduli e test

`package.json` dice quale comando avvia la suite e se il progetto usa moduli ES (`type: module`) o CommonJS. Non cambiare formato di import per risolvere un errore di business: prima verifica la convenzione già usata dai file vicini.

Nei laboratori di questo percorso `npm test` usa il runner integrato in Node, senza dipendenze di rete. In un repository reale il comando può essere diverso: copia quello del README o degli script. Se un test si blocca, controlla Promise non attese, server lasciati aperti e timer.

Un servizio dovrebbe poter essere testato senza avviare tutta l'applicazione. Se la route restituisce status e body, un test mirato può verificare il contratto senza browser. Leggi anche il test del caso mancante: spesso rivela se si deve restituire `null`, un 404 o un errore propagato.
