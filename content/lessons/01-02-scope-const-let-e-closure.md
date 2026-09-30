# Scope, const, let e closure

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Comprendere dove vive una variabile e perché una funzione ricorda il contesto esterno.

Lo scope stabilisce da quali righe una variabile è visibile. Una closure nasce quando una funzione continua ad accedere alle variabili del luogo in cui è stata creata, anche dopo che quella funzione esterna è terminata.

Lo scope è l'insieme dei punti da cui un nome è accessibile. Le variabili `let` e `const` definite in un blocco restano in quel blocco. Una closure conserva l'accesso all'ambiente in cui la funzione è nata: non copia automaticamente tutti i valori. Chiamate diverse alla funzione esterna creano ambienti distinti.

## Le parole da riconoscere

`scope di blocco`; `const`; `let`; `closure`; `shadowing`; `funzione interna`

## Un esempio concreto

```javascript
function createCounter() {
  let value = 0;
  return () => { value += 1; return value; };
}
const first = createCounter();
const second = createCounter();
console.log(first(), first(), second()); // 1, 2, 1
function capture(value) { return () => value; }
let current = 1;
const oldRead = capture(current);
current = 9;
console.log(oldRead()); // 1
```

Il primo contatore legge e aggiorna la stessa variabile `value` a ogni chiamata. Il secondo ha un altro `value`. In `capture`, invece, il parametro riceve il numero 1: assegnare 9 a `current` non cambia quel parametro. React richiama il componente per ogni render; una callback creata in un render precedente accede all'ambiente di quel render. Questo spiega i valori precedenti nei timer.

## Prova tu

Implementa il contatore e verifica che due istanze siano indipendenti. Poi prevedi cosa accade se sposti `let value = 0` dentro la funzione restituita: ogni chiamata riparte da zero.

## Dove ci si confonde spesso

- Usare var senza motivo
- Credere che const renda immutabile un oggetto

## Domanda di verifica

> Che cos'è una closure e quando può essere utile?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures).
