# Union e narrowing

## In parole semplici

L'obiettivo di questa lezione è rappresentare stati alternativi e restringere il tipo in modo sicuro.

Una union dichiara che un valore può assumere forme alternative. Controllando una proprietà discriminante, TypeScript restringe il tipo e ti permette di accedere soltanto ai campi validi per quel caso.

### Perché è utile

TypeScript ti aiuta a rendere esplicite le promesse del codice. Un tipo utile racconta quali dati accetti, quali casi sono possibili e quali controlli restano comunque necessari durante l'esecuzione.

## Le parole da riconoscere

- `union`
- `literal type`
- `discriminated union`
- `typeof`
- `in`
- `narrowing`
- `never`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **union, literal type, discriminated union** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
type Result = {status:'ok'; data:string[]} | {status:'error'; message:string};
function render(r:Result){ return r.status === 'ok' ? r.data.join(', ') : r.message; }
```

Guarda quali errori il tipo può impedire prima dell'avvio e quali dati, soprattutto quelli esterni, richiedono ancora una verifica a runtime.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Asserzioni as usate per forzare
- Union troppo generiche
- Rami non esaustivi

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Che vantaggio offre una discriminated union?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
