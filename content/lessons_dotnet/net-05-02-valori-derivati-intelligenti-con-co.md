# Valori derivati intelligenti con computed()

## In parole semplici

L'obiettivo di questa lezione è creare segnali dipendenti che si ricalcolano automaticamente e memorizzano il risultato.

`computed()` crea un valore derivato in sola lettura. Angular memorizza il calcolo e aggiorna le dipendenze in base ai Signals letti durante l'ultima esecuzione; la funzione viene valutata quando il valore serve.

### Nel percorso

Da conoscere: [Introduzione a signal() e aggiornamento stato con set() e update()](net-05-01-introduzione-a-signal-e-aggiornamen.md).

Un totale dipende dagli elementi: mantenere due valori modificabili separati obbliga a sincronizzarli. Il laboratorio Dashboard Reattiva con Angular Signals verifica l'aggiornamento dei totali quando la lista cambia.

## Le parole da riconoscere

- `computed`
- `derivazione di stato`
- `memoization`
- `funzione pura`
- `dipendenze dinamiche`

## Anatomia e Sintassi del Codice

### Caratteristiche di `computed()`:
1. **Memoization**: `computed()` calcola il valore quando serve e riusa il risultato finché le dipendenze lette non cambiano.
2. **Sola lettura**: un segnale `computed` non espone `.set()` o `.update()`; modifica i segnali sorgente e lascia derivare il valore.
3. **Dipendenze dinamiche**: Angular tiene conto dei Signals letti durante l'ultima esecuzione della funzione. Mantieni il calcolo puro: non aggiornare stato e non avviare richieste al suo interno.

```typescript
const price = signal(100);
const taxRate = signal(0.22);
const totalPrice = computed(() => price() * (1 + taxRate()));
```

## Un esempio concreto

```typescript
const items = signal([10, 20, 30]);
const total = computed(() => items().reduce((a, b) => a + b, 0));
const isFreeShipping = computed(() => total() >= 50);
```

### Seguilo passo per passo

1. `items()` restituisce `[10, 20, 30]`; `total` somma gli elementi e produce `60`.
2. `isFreeShipping` legge `total()`: dato che `60 >= 50`, il valore derivato è `true`.
3. `computed()` memorizza il risultato e ricalcola quando cambia un Signal effettivamente letto; non è il posto per chiamate HTTP o aggiornamenti di stato.
4. Aggiungi `5` agli articoli e verifica che il totale diventi `65`. Rimuovi un elemento e controlla come cambia la soglia della spedizione.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class CartStore {
    items = signal<{ price: number; quantity: number }[]>([]);
    total = computed(() => this.items().reduce((sum, item) => sum + item.price * item.quantity, 0));
    hasItems = computed(() => this.items().length > 0);
}
```

## Dove ci si confonde spesso

- Inserire effetti collaterali (chiamate HTTP, manipolazione manuale del DOM) dentro una funzione `computed()` (deve essere rigorosamente pura!).

## Domanda di verifica

> Perché una funzione passata a `computed()` deve essere rigorosamente pura e priva di side-effect?
