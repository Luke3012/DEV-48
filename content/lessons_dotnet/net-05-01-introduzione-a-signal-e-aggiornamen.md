# Introduzione a signal() e aggiornamento stato con set() e update()

## In parole semplici

L'obiettivo di questa lezione è creare e gestire variabili reattive con il modello a segnali di Angular.

Un Signal contiene un valore leggibile e aggiornabile. Quando un template legge quel Signal, Angular registra la dipendenza e programma il controllo della vista interessata dopo un aggiornamento. Il Signal non garantisce che venga ridisegnata soltanto una singola riga: il lavoro dipende dalle dipendenze e dalla strategia di change detection.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `signal`
- `set`
- `update`
- `asreadonly`
- `reattivita fine grained`
- `zone.js`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`signal`, `set`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class CounterComponent {
    count = signal(0);
    increment() { this.count.update(n => n + 1); }
    decrement() { this.count.update(n => Math.max(0, n - 1)); }
    reset() { this.count.set(0); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Tentare di riassegnare il segnale con l'uguale (`this.count = 5` invece di `this.count.set(5)`)
- dimenticare di invocarlo con le parentesi `this.count()`
- mutare in-place un array contenuto nel Signal.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è la differenza fondamentale tra `.set()` e `.update()` su un Signal?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
