# Effetti collaterali controllati con effect()

## In parole semplici

L'obiettivo di questa lezione è eseguire operazioni esterne (localStorage, logging, sincronizzazione) in risposta a cambi di stato.

La funzione `effect()` esegue codice esterno quando cambiano i Signals letti al suo interno. Può sincronizzare il browser storage o registrare log; per derivare valori è preferibile `computed()`.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `effect`
- `side effect`
- `cleanup`
- `localstorage`
- `injection context`
- `oncleanup`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`effect`, `side effect`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

> **Attenzione**: Non modificare segnali all'interno di un `effect()` a meno di non abilitare esplicitamente `{ allowSignalWrites: true }`, poiché rischierebbe di creare loop infiniti di aggiornamento!

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class ThemeManager {
    isDark = signal(false);
    themeName = computed(() => this.isDark() ? 'dark' : 'light');
    toggle() { this.isDark.update(v => !v); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare `effect()` per derivare nuovo stato (per questo scopo si DEVE usare `computed()`)
- creare loop di aggiornamenti infiniti.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è la differenza concettuale fondamentale tra un `computed()` e un `effect()`?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
