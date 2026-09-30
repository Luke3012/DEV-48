# Repository Node.js: package, moduli e test

`package.json` dice quale comando avvia la suite e se il progetto usa moduli ES (`type: module`) o CommonJS. Non cambiare formato di import per risolvere un errore di business: prima verifica la convenzione già usata dai file vicini.

Nei laboratori Node forniti con il materiale, `npm test` usa il runner integrato in Node, senza dipendenze di rete. In un repository reale il comando può essere diverso: il README o gli script del progetto ne indicano uno specifico. In caso di test bloccato, le cause frequenti includono Promise non attese, server lasciati aperti e timer.

Un servizio dovrebbe poter essere testato senza avviare tutta l'applicazione. Se la route restituisce status e body, un test mirato può verificare il contratto senza browser. Leggi anche il test del caso mancante: spesso rivela se si deve restituire `null`, un 404 o un errore propagato.

### Dal comando al test

Se `package.json` contiene `"type": "module"` e `"test": "node --test"`, il progetto usa moduli ES e il comando della suite è `npm test`. Una route importa il controller, che chiama un service; un test unitario può importare direttamente il service e passargli dati finti. Se `findActive` restituisce un archivio, confronta prima la regola e poi il test che la mostra: non cambiare `import` in `require` per correggere un filtro.

Un `Promise` deve essere atteso dal test: `await findActive(...)` confronta il valore finale, mentre omettere `await` confronta l'oggetto Promise. Quando un test rimane appeso, guarda timer, server e handle aperti; non aggiungere timeout crescenti prima di sapere che cosa resta attivo.

Il runner locale dei laboratori usa Node integrato e non richiede dipendenze di rete. Nei progetti reali controlla però script e versioni effettivi; la stessa cartella può avere comandi diversi.

**Da ricordare.** Segui gli script dichiarati e le convenzioni esistenti; un test diretto sul service isola la logica dal server HTTP. **Per praticare:** Repository di esempio · Node.js; Repository asincrona · Promise e controller.