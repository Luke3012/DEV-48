# Introduzione a signal() e aggiornamento stato con set() e update()

## In parole semplici

L'obiettivo di questa lezione è creare e gestire variabili reattive con il modello a segnali di Angular.

Un Signal contiene un valore leggibile e aggiornabile. Quando un template legge quel Signal, Angular registra la dipendenza e programma il controllo della vista interessata dopo un aggiornamento. Il Signal non garantisce che venga ridisegnata soltanto una singola riga: il lavoro dipende dalle dipendenze e dalla strategia di change detection.

### Nel percorso

Da conoscere: [TypeScript di base: variabili, funzioni e array](net-00-02-typescript-di-base-variabili-funzio.md).

Puoi leggere questa lezione prima del bootstrap Angular: l'esercizio breve richiede soltanto una classe e i valori reattivi. La registrazione del componente e il rendering verranno provati nel laboratorio Angular. Nel codice reale importa `signal` da `@angular/core`; l'editor breve lo mette a disposizione tramite un mock.

## Le parole da riconoscere

- `signal`
- `set`
- `update`
- `asreadonly`
- `reattivita fine grained`
- `zone.js`

## Anatomia e Sintassi del Codice

### Operazioni Fondamentali sui Signals:
1. **Creazione**:
   `count = signal(0);`
2. **Lettura (Getter)**:
   `const current = this.count();` (si invoca come una funzione senza argomenti)
3. **Sostituzione con `.set(value)`**:
   `this.count.set(10);` (imposta direttamente un nuovo valore)
4. **Aggiornamento basato sul valore precedente con `.update(fn)`**:
   `this.count.update(prev => prev + 1);` (ideale per incrementi, aggiunte a liste)
5. **Esposizione in sola lettura con `.asReadonly()`**:
   `readonlyCount = this.count.asReadonly();` (impedisce a chi riceve il Signal di chiamare `.set()` o `.update()`; non rende profondamente immutabile un oggetto contenuto).

Angular 22 usa il change detection zoneless per i nuovi progetti. I Signals sono uno dei modi con cui il framework riceve una notifica di aggiornamento; non sono loro a rimuovere `zone.js`. `computed()` è adatto ai valori derivati, mentre `effect()` serve soprattutto a sincronizzare effetti esterni e non a duplicare stato.

## Un esempio concreto

```typescript
const count = signal(0);
count.set(5);
count.update(n => n + 1);
console.log(count()); // 6
```

### Seguilo passo per passo

1. `signal(0)` crea `count` con valore iniziale zero; `count()` legge il valore.
2. `set(5)` sostituisce il valore con cinque. `update(n => n + 1)` calcola il nuovo valore a partire da quello corrente.
3. Dopo i due aggiornamenti, `count()` restituisce `6`, che viene stampato da `console.log`.
4. Riprova con `update(n => n - 10)`: il risultato diventa negativo perché qui non esiste alcuna regola che lo impedisca. La logica dei limiti va aggiunta dove serve.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class CounterComponent {
    count = signal(0);
    increment() { this.count.update(n => n + 1); }
    decrement() { this.count.update(n => Math.max(0, n - 1)); }
    reset() { this.count.set(0); }
}
```

## Dove ci si confonde spesso

- Tentare di riassegnare il segnale con l'uguale (`this.count = 5` invece di `this.count.set(5)`)
- dimenticare di invocarlo con le parentesi `this.count()`
- mutare in-place un array contenuto nel Signal.

## Domanda di verifica

> Qual è la differenza fondamentale tra `.set()` e `.update()` su un Signal?
