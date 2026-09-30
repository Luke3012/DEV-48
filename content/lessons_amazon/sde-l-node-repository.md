# Repository Node.js: package, moduli e test

`package.json` dice quale comando avvia la suite e se il progetto usa moduli ES (`type: module`) o CommonJS. Non cambiare formato di import per risolvere un errore di business: prima verifica la convenzione già usata dai file vicini.

Nei laboratori Node forniti con il materiale, `npm test` usa il runner integrato in Node, senza dipendenze di rete. In un repository reale il comando può essere diverso: il README o gli script del progetto ne indicano uno specifico. In caso di test bloccato, le cause frequenti includono Promise non attese, server lasciati aperti e timer.

Un servizio dovrebbe poter essere testato senza avviare tutta l'applicazione. Se la route restituisce status e body, un test mirato può verificare il contratto senza browser. Leggi anche il test del caso mancante: spesso rivela se si deve restituire `null`, un 404 o un errore propagato.
