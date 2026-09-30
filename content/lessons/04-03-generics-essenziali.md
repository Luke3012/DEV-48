# Generics essenziali

## In parole semplici

Mantenere relazioni tra tipi senza ricorrere ad any.

Un generic conserva una relazione tra il tipo ricevuto e quello restituito. È utile quando la stessa logica funziona con dati diversi, ma vuoi evitare che `any` cancelli le informazioni sui tipi.

## Le parole da riconoscere

`generic`; `parametro di tipo`; `constraint`; `Array<T>`; `Promise<T>`; `riuso`

## Un esempio concreto

```typescript
function first<T>(items: T[]): T | undefined { return items[0]; }
const value = first<number>([10, 20]);
```

first<T> mantiene la relazione tra il tipo degli elementi e il risultato T oppure undefined. Una funzione con any perde quella informazione. Con un array di numeri il chiamante sa di dover gestire un numero o l'assenza, e non una qualunque proprietà arbitraria.

## Prova tu

Implementa `first<T>(items: T[]): T | undefined` senza any. Deve funzionare con numeri, stringhe e oggetti, e dare undefined su []. Node esegue la logica dopo aver rimosso i tipi; controlla separatamente la relazione generica con tsc.

## Dove ci si confonde spesso

- Generics inutilmente complessi
- Nomi incomprensibili
- Constraint mancanti

## Domanda di verifica

> Perché first<T> è più sicura di una funzione che restituisce any?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
