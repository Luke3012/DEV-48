# Valori, tipi e confronti

## In parole semplici

Capire cosa contiene una variabile e prevedere conversioni e confronti.

JavaScript può convertire automaticamente un valore durante un confronto. Usare `===` e controllare il tipo rende il risultato più prevedibile, soprattutto quando i dati arrivano da form o API.

Una variabile contiene un valore, e il tipo influenza ciò che puoi farci. `const` dichiara un riferimento che non puoi riassegnare; `let` consente la riassegnazione. `if` sceglie un ramo in base a una condizione e `return`, che useremo nelle funzioni, termina la chiamata restituendo un valore. Parti da confronti espliciti quando il requisito riguarda un tipo preciso.

## Le parole da riconoscere

`string`; `number`; `boolean`; `null`; `undefined`; `typeof`; `===`; `truthy e falsy`

## Un esempio concreto

```javascript
const fromInput = '0';
console.log(typeof fromInput); // 'string'
console.log(fromInput === 0); // false
console.log(Number(fromInput) === 0); // true
if (fromInput) console.log('stringa non vuota');
console.log(typeof null); // 'object': particolarità storica
```

`'0'` è una stringa non vuota, quindi è truthy; il numero `0` è falsy. `===` confronta senza la conversione implicita di `==`. `null` esprime spesso un'assenza intenzionale; `undefined` compare, per esempio, leggendo una proprietà che manca. Non usare soltanto `typeof` per distinguerli.

## Prova tu

Prevedi prima l'esito di `'' === false`, `0 === false` e `null === undefined`. Poi eseguili. In `classifyValue`, prova anche `false`, zero e la stringa `'0'`: non devono essere classificati come mancanti.

## Dove ci si confonde spesso

- Usare ==
- Confondere null con undefined
- Considerare '0' come numero zero

## Domanda di verifica

> Qual è la differenza tra == e ===?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
