# Generics essenziali

## In parole semplici

L'obiettivo di questa lezione è mantenere relazioni tra tipi senza ricorrere ad any.

Un generic conserva una relazione tra il tipo ricevuto e quello restituito. È utile quando la stessa logica funziona con dati diversi, ma vuoi evitare che `any` cancelli le informazioni sui tipi.

### Perché è utile

TypeScript ti aiuta a rendere esplicite le promesse del codice. Un tipo utile racconta quali dati accetti, quali casi sono possibili e quali controlli restano comunque necessari durante l'esecuzione.

## Le parole da riconoscere

- `generic`
- `parametro di tipo`
- `constraint`
- `Array<T>`
- `Promise<T>`
- `riuso`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **generic, parametro di tipo, constraint** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
function first<T>(items: T[]): T | undefined { return items[0]; }
const value = first<number>([10, 20]);
```

Guarda quali errori il tipo può impedire prima dell'avvio e quali dati, soprattutto quelli esterni, richiedono ancora una verifica a runtime.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Generics inutilmente complessi
- Nomi incomprensibili
- Constraint mancanti

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Perché first<T> è più sicura di una funzione che restituisce any?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
