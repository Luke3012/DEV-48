# Introduzione a signal() e aggiornamento stato con set() e update()

In una vista il numero mostrato dipende dallo stato della classe. Una proprietà normale può contenere `0`, ma quando Angular la legge non crea una dipendenza reattiva esplicita; un Signal rende leggibile quel valore e notifica il framework quando viene aggiornato.

### Nel percorso

Da conoscere: [TypeScript di base: variabili, funzioni e array](net-00-02-typescript-di-base-variabili-funzio.md).

Puoi leggere questa lezione prima del bootstrap Angular: l'esercizio breve richiede soltanto una classe e i valori reattivi. La registrazione del componente e il rendering verranno provati nel laboratorio Angular. Nel codice reale importa `signal` da `@angular/core`; l'editor breve lo mette a disposizione tramite un mock.

## Quale dato è sorgente e quale è derivato?

### Dal campo al Signal
Prima il componente tiene un valore ordinario:
```typescript
count = 0;
increment(): void { this.count += 1; }
```
Il template può leggere `{{ count }}`. Un evento può cambiare il campo e Angular può controllare la vista; però il campo non dichiara da sé una dipendenza che un computed o un consumer possa tracciare.

Con un Signal:
```typescript
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-counter',
  template: '<p>Hai aggiunto {{ count() }} articoli</p><button (click)="increment()">+</button>'
})
export class CounterComponent {
  readonly count = signal(0);

  increment(): void {
    this.count.update(value => value + 1);
  }
}
```

Il Signal è una funzione getter: `count()` restituisce il valore e registra chi lo legge. `set(value)` sostituisce lo stato; `update(current => next)` calcola il nuovo valore da quello corrente. `asReadonly()` consente di esporre una lettura senza `.set()` o `.update()`, ma non rende immutabile in profondità un oggetto contenuto.

Per liste e oggetti crea un nuovo valore: `items.update(current => [...current, newItem])`. Mutare l'array esistente con `push()` mantiene la stessa identità e non è un aggiornamento affidabile del Signal.

## Osserva come si propaga un aggiornamento

```typescript
count = signal(0);
increment(): void { this.count.update(value => value + 1); }
```

### Segui la modifica fino alla vista

1. All'avvio `count()` vale `0`; il template legge il Signal e registra la vista come consumatore di quel dato.
2. Il click invoca `increment()`, che usa `update` per calcolare `0 + 1` e memorizza `1`.
3. Angular riceve la notifica del Signal e aggiorna la vista che ne dipende; il template mostra `1`. Le parentesi appartengono alla lettura, non all'aggiornamento.
4. Confronta `set(5)` con `update(value => value + 1)`. Poi prova una lista: assegna una nuova lista con spread e osserva perché mutare quella esistente con `push` non costituisce un nuovo valore.

Il runner del mini-esercizio fornisce un mock dei Signals e verifica i valori; il laboratorio avvia Angular e controlla che i click aggiornino la vista reale.

## Quando usare un calcolo o un effetto

- Tentare di riassegnare il segnale con l'uguale (`this.count = 5` invece di `this.count.set(5)`)
- dimenticare di invocarlo con le parentesi `this.count()`
- mutare in-place un array contenuto nel Signal.

> **Quali dipendenze vengono lette?** Qual è la differenza fondamentale tra `.set()` e `.update()` su un Signal?
