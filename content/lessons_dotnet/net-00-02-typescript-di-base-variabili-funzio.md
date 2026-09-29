# TypeScript di base: variabili, funzioni e array

## In parole semplici

L'obiettivo di questa lezione è scrivere una funzione TypeScript tipizzata e seguire un ciclo su una lista di numeri.

TypeScript aggiunge tipi controllati alla sintassi di JavaScript. Una funzione riceve valori, lavora su di essi e restituisce un risultato; un array raccoglie più valori dello stesso tipo.

### Nel percorso

Qui impari funzioni e array prima di usarli nei componenti. Il runner breve esegue la logica rimuovendo le annotazioni: nel laboratorio Modelli TypeScript e Contratti Web userai anche il compilatore per verificare i tipi.

## Le parole da riconoscere

- `const`
- `let`
- `parametro`
- `tipo restituito`
- `number`
- `array`
- `for`

## Anatomia e Sintassi del Codice

### Una variabile, una funzione e una lista
- Usa `const` quando il nome non verrà riassegnato; usa `let` quando il valore della variabile cambierà.
- Dopo il nome del parametro, `: number[]` dichiara un array di numeri.
- Dopo le parentesi della funzione, `: number` dichiara il tipo restituito.
- Un `for...of` legge un elemento alla volta. `total += value` aggiunge il valore al totale corrente.

I tipi sono controllati da TypeScript durante la compilazione; non trasformano né validano automaticamente dati JSON ricevuti a runtime.

## Un esempio concreto

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

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```typescript
export function countNames(names: string[]): number {
    let count = 0;
    for (const name of names) {
        if (name.trim().length > 0) count += 1;
    }
    return count;
}
```

## Dove ci si confonde spesso

- Usare `=` al posto di `===` in una condizione
- dimenticare che gli array vuoti non contengono valori da sommare
- confondere il tipo statico con la validazione dei dati esterni.

## Domanda di verifica

> Quali informazioni forniscono i tipi `number[]` e `: number` in una funzione?
