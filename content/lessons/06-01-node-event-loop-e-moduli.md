# Node, event loop e moduli

## In parole semplici

L'obiettivo di questa lezione è comprendere perché JavaScript server gestisce bene operazioni I/O e dove può bloccarsi.

Node gestisce bene molte operazioni di I/O perché non aspetta in modo sincrono file e rete. Un calcolo CPU lungo, invece, occupa il thread principale e ritarda tutte le altre richieste.

### Perché è utile

Sul backend ogni dato attraversa un confine: arriva da una richiesta, viene controllato, passa nella logica applicativa e produce una risposta. Tenere distinti questi passaggi rende più semplici sia gli errori sia la sicurezza.

## Le parole da riconoscere

- `Node.js`
- `event loop`
- `I/O asincrono`
- `CommonJS`
- `ES modules`
- `process`
- `package.json`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **Node.js, event loop, I/O asincrono** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
import { readFile } from 'node:fs/promises';
const config = JSON.parse(await readFile('config.json', 'utf8'));
```

Segui la richiesta nell'ordine reale: ingresso, controllo, logica, accesso ai dati e risposta. Nota anche dove finirebbe un errore.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Lavoro CPU pesante nel thread principale
- Callback bloccanti
- Moduli mescolati

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Che cosa succede se una route esegue un calcolo sincrono molto lungo?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
