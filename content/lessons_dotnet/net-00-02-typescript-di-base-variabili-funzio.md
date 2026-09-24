# TypeScript di base: variabili, funzioni e array

## In parole semplici

L'obiettivo di questa lezione è scrivere una funzione TypeScript tipizzata e seguire un ciclo su una lista di numeri.

TypeScript aggiunge tipi controllati alla sintassi di JavaScript. Una funzione riceve valori, lavora su di essi e restituisce un risultato; un array raccoglie più valori dello stesso tipo.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `const`
- `let`
- `parametro`
- `tipo restituito`
- `number`
- `array`
- `for`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`const`, `let`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Una variabile, una funzione e una lista
- Usa `const` quando il nome non verrà riassegnato; usa `let` quando il valore della variabile cambierà.
- Dopo il nome del parametro, `: number[]` dichiara un array di numeri.
- Dopo le parentesi della funzione, `: number` dichiara il tipo restituito.
- Un `for...of` legge un elemento alla volta. `total += value` aggiunge il valore al totale corrente.

I tipi sono controllati da TypeScript durante la compilazione; non trasformano né validano automaticamente dati JSON ricevuti a runtime.

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```typescript
const initialValues: number[] = [2, 3];

export function sum(values: number[]): number {
    let total = 0;
    for (const value of values) {
        total += value;
    }
    return total;
}

console.log(sum(initialValues)); // 5
```

### Seguilo passo per passo

1. `initialValues` è un array di numeri con valori `2` e `3`; l'annotazione `number[]` descrive il tipo degli elementi.
2. `sum` parte da `0` e il ciclo legge un valore alla volta, aggiungendolo a `total`.
3. Dopo il ciclo `total` vale `5`, quindi la funzione restituisce `5` e `console.log` lo mostra.
4. Prova `[]`: il ciclo non aggiunge nulla e il risultato resta `0`. Prova un array con tre valori per seguire tre aggiornamenti dell'accumulatore.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export function countNames(names: string[]): number {
    let count = 0;
    for (const name of names) {
        if (name.trim().length > 0) count += 1;
    }
    return count;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare `=` al posto di `===` in una condizione
- dimenticare che gli array vuoti non contengono valori da sommare
- confondere il tipo statico con la validazione dei dati esterni.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quali informazioni forniscono i tipi `number[]` e `: number` in una funzione?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
