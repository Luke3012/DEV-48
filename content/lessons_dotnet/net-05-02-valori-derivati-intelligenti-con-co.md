# Valori derivati intelligenti con computed()

Se un carrello contiene righe e quantità, il totale dipende da quei dati. Memorizzare sia le righe sia un totale modificabile richiede di ricordare ogni punto di aggiornamento: basta dimenticarne uno per mostrare una cifra incoerente.

### Nel percorso

Da conoscere: [Introduzione a signal() e aggiornamento stato con set() e update()](net-05-01-introduzione-a-signal-e-aggiornamen.md).

Un totale dipende dagli elementi: mantenere due valori modificabili separati obbliga a sincronizzarli. Il laboratorio Dashboard Reattiva con Angular Signals verifica l'aggiornamento dei totali quando la lista cambia.

## Quale dato è sorgente e quale è derivato?

### Stato sorgente e stato derivato
```typescript
import { computed, signal } from '@angular/core';

type CartItem = { id: number; name: string; price: number; quantity: number };

export class CartStore {
  private readonly _items = signal<CartItem[]>([]);
  readonly items = this._items.asReadonly();

  readonly subtotal = computed(() =>
    this._items().reduce((sum, item) => sum + item.price * item.quantity, 0)
  );
  readonly itemCount = computed(() =>
    this._items().reduce((sum, item) => sum + item.quantity, 0)
  );
  readonly hasItems = computed(() => this._items().length > 0);

  add(item: CartItem): void {
    this._items.update(current => [...current, item]);
  }
}
```

`_items` è stato sorgente, posseduto e modificato dal servizio. `subtotal`, `itemCount` e `hasItems` sono proiezioni in sola lettura. `computed` osserva le letture fatte dalla funzione, memorizza il risultato e lo ricalcola quando una dipendenza cambia; il calcolo deve essere sincrono e senza effetti esterni.

Se aggiorni manualmente sia `_items` sia un Signal `total`, ogni operazione di aggiunta, rimozione e modifica deve ricordarsi di aggiornare entrambi. Una derivazione centrale elimina questa duplicazione e rende visibile la relazione fra dati e risultato.

## Osserva come si propaga un aggiornamento

```typescript
const total = computed(() => items().reduce((sum, item) => sum + item.price * item.quantity, 0));
```

### Segui la modifica fino alla vista

1. Con due articoli da `10 € × 2` e `5 € × 1`, `subtotal()` deriva `25` da `_items()`.
2. `itemCount()` produce `3`; non è un secondo contatore da incrementare manualmente.
3. `add()` sostituisce l'array con una nuova lista. Angular invalida i computed che hanno letto `_items()`; il prossimo accesso ricalcola il risultato.
4. Rimuovi un articolo aggiornando solo `_items`. Se totale e conteggio cambiano correttamente, lo stato derivato ha una sola fonte di verità.

La pratica breve verifica una derivazione isolata. Nel laboratorio Dashboard prova lista vuota, aggiunta e rimozione con array immutabili, quindi osserva totali e percentuali nel componente reale.

## Quando usare un calcolo o un effetto

- Inserire effetti collaterali (chiamate HTTP, manipolazione manuale del DOM) dentro una funzione `computed()` (deve essere rigorosamente pura!).

> **Quali dipendenze vengono lette?** Perché una funzione passata a `computed()` deve essere rigorosamente pura e priva di side-effect?
