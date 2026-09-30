# Scegliere lo stack repository: C++ o Node.js

Le repository C++ e Node.js mettono in evidenza difficoltà diverse: la prima richiede di seguire header, source e target di compilazione; la seconda di orientarsi tra package, route, service e test. Una prova sulle due opzioni consente di confrontarne la leggibilità e il debugging.

I primi due laboratori sono equivalenti: entrambi espongono `visibleActive` e `findSubject`, entrambi hanno due difetti e gli stessi casi osservabili. Nel C++ si esaminano header, source e test; nel Node `package.json`, service e test. Il tempo di orientamento e il numero di passaggi necessari a ricostruire il flusso forniscono misure confrontabili.

La scelta finale considera leggibilità e correzione, oltre alla sintassi. Un repository reale può differire dagli esempi; restano centrali la capacità di riconoscere package e test, seguire un contratto e interpretare gli errori nel linguaggio selezionato.
