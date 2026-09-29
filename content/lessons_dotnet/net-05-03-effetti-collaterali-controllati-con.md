# Effetti collaterali controllati con effect()

## In parole semplici

L'obiettivo di questa lezione è eseguire operazioni esterne (localStorage, logging, sincronizzazione) in risposta a cambi di stato.

La funzione `effect()` esegue codice esterno quando cambiano i Signals letti al suo interno. Può sincronizzare il browser storage o registrare log; per derivare valori è preferibile `computed()`.

## Le parole da riconoscere

- `effect`
- `side effect`
- `cleanup`
- `localstorage`
- `injection context`
- `oncleanup`

## Anatomia e Sintassi del Codice

### Regole e Uso Corretto di `effect()`:
1. **Injection Context**: `effect()` deve essere chiamato all'interno del costruttore del componente o come inizializzatore di proprietà.
2. **Tracciamento automatico**: Angular traccia automaticamente tutti i segnali letti dentro l'effetto:
```typescript
import { Component, effect, signal } from '@angular/core';

@Component({ selector: 'app-theme', template: '' })
export class ThemeComponent {
  darkMode = signal(false);

  constructor() {
    effect(() => {
      // Si riesegue ogni volta che darkMode() cambia!
      localStorage.setItem('theme', this.darkMode() ? 'dark' : 'light');
    });
  }
}
```

In Angular 22 scrivere Signals dentro un effect è consentito; `allowSignalWrites` è deprecato e non serve ([riferimento Angular](https://angular.dev/api/core/CreateEffectOptions)). Il rischio di cicli rimane: per calcolare uno stato a partire da altro stato preferisci `computed()`. Usa effect per sincronizzare una risorsa esterna, prevedendo la pulizia quando necessario.

## Un esempio concreto

```typescript
effect(() => {
  console.log('Nuovo tema selezionato:', theme());
});
```

### Seguilo passo per passo

1. L'effect legge `theme()`: questa lettura registra il Signal come dipendenza dell'effetto.
2. Quando l'effect viene creato, esegue il corpo e scrive nel log il tema corrente; una modifica successiva del Signal provoca una nuova esecuzione.
3. `console.log` è un effetto esterno, quindi è adatto a un effect. Il calcolo del nome del tema, invece, dovrebbe stare in `computed()`.
4. Cambia il tema due volte e osserva il log. Se l'effetto avvia una risorsa o un abbonamento, aggiungi una cleanup invece di crearne uno nuovo a ogni esecuzione.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class ThemeManager {
    isDark = signal(false);
    themeName = computed(() => this.isDark() ? 'dark' : 'light');
    toggle() { this.isDark.update(v => !v); }
}
```

## Dove ci si confonde spesso

- Usare `effect()` per derivare nuovo stato (per questo scopo si DEVE usare `computed()`)
- creare loop di aggiornamenti infiniti.

## Domanda di verifica

> Qual è la differenza concettuale fondamentale tra un `computed()` e un `effect()`?
