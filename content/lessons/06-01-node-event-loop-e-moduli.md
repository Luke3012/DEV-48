# Node, event loop e moduli

## In parole semplici

Comprendere perché JavaScript server gestisce bene operazioni I/O e dove può bloccarsi.

Node gestisce bene molte operazioni di I/O perché non aspetta in modo sincrono file e rete. Un calcolo CPU lungo, invece, occupa il thread principale e ritarda tutte le altre richieste.

## Le parole da riconoscere

`Node.js`; `event loop`; `I/O asincrono`; `CommonJS`; `ES modules`; `process`; `package.json`

## Un esempio concreto

```javascript
import { readFile } from 'node:fs/promises';
const config = JSON.parse(await readFile('config.json', 'utf8'));
```

Un calcolo sincrono lungo occupa il thread principale e ritarda callback, timer e gestione di altre richieste. L'I/O asincrono evita di aspettare inutilmente file o rete, ma non rende parallelo un calcolo CPU. Per carichi CPU rilevanti valuto un worker o un processo dedicato.

## Prova tu

Un endpoint esegue per tre secondi un calcolo sincrono; nello stesso processo un altro client chiede una lista piccola. Prevedi il ritardo e spiega perché aggiungere async al nome della funzione non rende parallelo il calcolo.

## Dove ci si confonde spesso

- Lavoro CPU pesante nel thread principale
- Callback bloccanti
- Moduli mescolati

## Domanda di verifica

> Che cosa succede se una route esegue un calcolo sincrono molto lungo?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
