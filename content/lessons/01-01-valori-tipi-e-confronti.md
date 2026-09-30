# Valori, tipi e confronti

## In parole semplici

Capire cosa contiene una variabile e prevedere conversioni e confronti.

JavaScript può convertire automaticamente un valore durante un confronto. Usare `===` e controllare il tipo rende il risultato più prevedibile, soprattutto quando i dati arrivano da form o API.

La stessa schermata può consegnare valori che sembrano uguali ma hanno tipi diversi. Prima di scegliere un confronto, chiediti quale domanda vuoi fare: i valori hanno lo stesso tipo e lo stesso contenuto? Vuoi consentire una conversione? Oppure vuoi sapere se un ramo `if` verrà eseguito?

Considera `value` uguale alla stringa `"0"`. La variabile contiene tre caratteri, non il numero zero. Guardiamo la stessa variabile con tre operazioni: `===` confronta senza conversioni, `==` può convertire, mentre `Boolean(...)` chiede soltanto se il valore è truthy. Sono domande diverse e possono quindi dare risposte diverse.

## Le parole da riconoscere

`string`; `number`; `boolean`; `null`; `undefined`; `typeof`; `===`; `truthy e falsy`

## Un esempio concreto

```javascript
const value = "0";

console.log(typeof value);   // "string"
console.log(value === 0);    // false
console.log(value == 0);     // true
console.log(Boolean(value)); // true

if (value) {
  console.log("Il ramo viene eseguito");
}

console.log(Boolean(0));  // false
console.log(Boolean("")); // false
console.log(typeof null); // "object": particolarità storica
```

La prima riga conserva l'input come stringa. Perciò `value === 0` è `false`: una stringa e un numero non diventano uguali durante il confronto stretto. Con `value == 0` JavaScript converte la stringa numerica e confronta due zeri; il risultato è `true`. Questo mostra perché `==` può sorprendere, non perché sia la scelta da preferire.

`Boolean(value)` risponde a una terza domanda. Una stringa non vuota è truthy anche quando il suo contenuto è `"0"`; il numero `0` e la stringa vuota sono falsy. Truthy non significa “uguale a `true`” e falsy non significa “uguale a zero”.

Un campo HTML arriva come stringa. Se il programma deve usarlo come numero, controlla prima che non sia vuoto, convertilo esplicitamente e valida il risultato. Altrimenti un controllo come `if (!value)` confonde l'assenza con il numero zero, mentre un confronto permissivo può nascondere la conversione. `null` indica spesso un'assenza scelta dal programma; `undefined` può indicare una proprietà che non esiste. `typeof null` è un'eccezione storica, quindi non serve a distinguere i due casi.

## Prova tu

Prevedi prima l'esito di `'' === false`, `0 === false` e `null === undefined`. Poi eseguili. In `classifyValue`, prova anche `false`, zero e la stringa `'0'`: non devono essere classificati come mancanti.

## Dove ci si confonde spesso

- Usare ==
- Confondere null con undefined
- Considerare '0' come numero zero

## Domanda di verifica

> Qual è la differenza tra == e ===?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness).
