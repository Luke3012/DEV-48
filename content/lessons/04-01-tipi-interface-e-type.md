# Tipi, interface e type

## In parole semplici

L'obiettivo di questa lezione è descrivere il contratto dei dati e ottenere errori prima dell'esecuzione.

Un tipo descrive la forma che il codice si aspetta e permette all'editor di segnalare incoerenze prima dell'avvio. Non controlla però automaticamente un JSON ricevuto dalla rete: quel dato richiede validazione a runtime.

### Perché è utile

TypeScript ti aiuta a rendere esplicite le promesse del codice. Un tipo utile racconta quali dati accetti, quali casi sono possibili e quali controlli restano comunque necessari durante l'esecuzione.

## Le parole da riconoscere

- `type annotation`
- `interface`
- `type alias`
- `optional property`
- `readonly`
- `structural typing`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **type annotation, interface, type alias** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
interface Subject { id: number; name: string; active: boolean; note?: string }
function label(subject: Subject): string { return subject.name; }
```

Guarda quali errori il tipo può impedire prima dell'avvio e quali dati, soprattutto quelli esterni, richiedono ancora una verifica a runtime.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare any per silenziare errori
- Considerare i tipi come validazione runtime

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Interface TypeScript verifica davvero il JSON ricevuto dalla rete?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
