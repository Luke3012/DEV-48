# Effetti collaterali controllati con effect()

Un valore calcolato appartiene allo stato dell'applicazione; scrivere su `localStorage`, inviare telemetria o aggiornare una libreria esterna è invece un effetto collaterale. Separare le due cose evita che un calcolo apparentemente innocuo inizi richieste o mutazioni.

## Quale dato è sorgente e quale è derivato?

### Un calcolo non è un effetto
Usa `computed` per ricavare il nome visibile da un valore sorgente; usa `effect` quando occorre sincronizzare un'API esterna.
```typescript
import { Component, computed, effect, signal } from '@angular/core';

@Component({ selector: 'app-theme', template: '<button (click)="toggle()">{{ themeName() }}</button>' })
export class ThemeComponent {
  private readonly dark = signal(false);
  readonly themeName = computed(() => this.dark() ? 'dark' : 'light');

  constructor() {
    effect(() => {
      console.info('Tema selezionato:', this.themeName());
    });
  }

  toggle(): void { this.dark.update(value => !value); }
}
```

L'effetto viene eseguito almeno una volta e legge `themeName()`, quindi segue le dipendenze lette. Viene creato nel contesto di iniezione del componente e Angular lo distrugge con il componente. Gli effetti sono asincroni nel ciclo di change detection.

Per storage o DOM considera il ciclo di vita del browser: non accedere a `localStorage` durante il rendering server-side. Se l'effetto avvia un timer o una sottoscrizione, registra la pulizia prima della prossima esecuzione o della distruzione. Evita di copiare un Signal in un altro con `effect`: usa `computed` o, per stato derivato che l'utente può anche impostare, valuta `linkedSignal`.

## Osserva come si propaga un aggiornamento

```typescript
effect(() => console.info('Tema selezionato:', themeName()));
```

### Segui la modifica fino alla vista

1. Alla creazione il componente inizializza `dark` a `false`; `computed` ricava `light` senza modificare altri dati.
2. `effect` legge `themeName()` e registra quella dipendenza; il primo log viene eseguito dal ciclo reattivo di Angular.
3. Al click, `toggle()` aggiorna solo lo stato sorgente. Il nome derivato cambia e l'effetto sincronizza il log esterno.
4. Se il componente viene distrutto, il suo effetto viene terminato. Per una risorsa avviata dall'effetto, aggiungi cleanup; per un totale o un'etichetta, resta su `computed`.

L'esercizio riguarda una regola pura di tema; non richiede di copiare `themeName` in un altro Signal. Nel laboratorio usa `effect` soltanto se sincronizzi davvero una risorsa esterna.

## Quando usare un calcolo o un effetto

- Usare `effect()` per derivare nuovo stato (per questo scopo si DEVE usare `computed()`)
- creare loop di aggiornamenti infiniti.

> **Quali dipendenze vengono lette?** Qual è la differenza concettuale fondamentale tra un `computed()` e un `effect()`?
