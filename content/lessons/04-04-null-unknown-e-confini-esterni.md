# Null, unknown e confini esterni

## In parole semplici

L'obiettivo di questa lezione è trattare dati esterni come non affidabili prima di usarli nel dominio.

`unknown` ti obbliga a controllare un valore prima di usarlo, mentre `any` disattiva quella protezione. È la scelta corretta per JSON, input utente e altri dati che entrano dall'esterno.

### Perché è utile

TypeScript ti aiuta a rendere esplicite le promesse del codice. Un tipo utile racconta quali dati accetti, quali casi sono possibili e quali controlli restano comunque necessari durante l'esecuzione.

## Le parole da riconoscere

- `unknown`
- `null`
- `undefined`
- `type guard`
- `validation`
- `optional chaining`
- `boundary`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **unknown, null, undefined** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
function isSubject(value: unknown): value is {id:number; name:string} {
  return typeof value === 'object' && value !== null && 'id' in value && 'name' in value;
}
```

Guarda quali errori il tipo può impedire prima dell'avvio e quali dati, soprattutto quelli esterni, richiedono ancora una verifica a runtime.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Convertire unknown in un tipo con as
- Fidarsi del JSON
- Usare ! senza prova

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Perché unknown è preferibile ad any per un input esterno?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
