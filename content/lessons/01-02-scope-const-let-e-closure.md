# Scope, const, let e closure

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Comprendere dove vive una variabile e perché una funzione ricorda il contesto esterno.

Lo scope stabilisce da quali righe una variabile è visibile. Una closure nasce quando una funzione continua ad accedere alle variabili del luogo in cui è stata creata, anche dopo che quella funzione esterna è terminata.

Lo scope risponde a una domanda concreta: da quale parte del programma posso leggere o cambiare questo nome? `let` e `const` dichiarati in una funzione appartengono a quella chiamata. Se una funzione interna usa un nome dello scope esterno, JavaScript risolve il nome risalendo gli ambienti lessicali.

Si parte da una variabile condivisa visibile a `increment`. Poi spostiamo `count` dentro `createCounter`: ogni chiamata esterna ottiene una variabile locale diversa. Se la funzione esterna restituisce una funzione che usa quella variabile, la funzione restituita conserva l'accesso al suo ambiente anche dopo che `createCounter` è terminata. Questo accesso mantenuto è la closure.

## Le parole da riconoscere

`scope di blocco`; `const`; `let`; `closure`; `shadowing`; `funzione interna`

## Un esempio concreto

```javascript
let count = 0;

function increment() {
  count += 1;
  return count;
}

console.log(increment()); // 1: l'ambiente condiviso viene aggiornato

function createCounter() {
  let count = 0;
  return function incrementLocal() {
    count += 1;
    return count;
  };
}

const first = createCounter();
const second = createCounter();
console.log(first(), first(), second()); // 1, 2, 1

const user = { name: "Anna" };
user.name = "Marco"; // consentito: il binding user non cambia
// user = {};        // TypeError: riassegnazione di const
```

La prima versione usa il `count` esterno: ogni chiamata a `increment` modifica la stessa variabile. Nel contatore vero, invece, `count` nasce dentro `createCounter`; al ritorno, `incrementLocal` conserva un riferimento a quell'ambiente:

~~~text
createCounter()
│
├─ ambiente della prima chiamata: count = 0
│    └─ first continua a leggere e aggiornare questo count
│
└─ ambiente della seconda chiamata: count = 0
     └─ second continua a leggere e aggiornare questo count
~~~

Quando esegui `first()` due volte, il primo ambiente passa da 0 a 1 e poi a 2. `second()` consulta un altro ambiente e parte ancora da 0, quindi restituisce 1. La closure non congela una copia: conserva l'accesso alla variabile, che può cambiare.

`const` protegge il binding: non permette di ricollegare `user` a un altro oggetto. Non rende immutabile l'oggetto raggiungibile da `user`; perciò `user.name = "Marco"` è consentito. Le copie necessarie quando si aggiornano oggetti annidati sono il passo successivo in Oggetti, destructuring e spread.

Questo è un comportamento JavaScript generale. React lo riusa: ogni render crea nuove funzioni e handler che accedono ai valori di quello specifico render. Per capire perché un timer può leggere un valore precedente, prima serve distinguere “la closure conserva l'accesso” da “la variabile viene sostituita in tutti gli ambienti”.

## Prova tu

Implementa il contatore e verifica che due istanze siano indipendenti. Poi prevedi cosa accade se sposti `let value = 0` dentro la funzione restituita: ogni chiamata riparte da zero.

## Dove ci si confonde spesso

- Usare var senza motivo
- Credere che const renda immutabile un oggetto

## Domanda di verifica

> Che cos'è una closure e quando può essere utile?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures).
