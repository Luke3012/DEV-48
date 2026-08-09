# Valori, tipi e confronti

## In parole semplici

L'obiettivo di questa lezione è capire cosa contiene una variabile e prevedere conversioni e confronti.

JavaScript può convertire automaticamente un valore durante un confronto. Usare `===` e controllare il tipo rende il risultato più prevedibile, soprattutto quando i dati arrivano da form o API.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `string`
- `number`
- `boolean`
- `null`
- `undefined`
- `typeof`
- `===`
- `truthy e falsy`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **string, number, boolean** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
const age = 30;
const label = age >= 18 ? 'adult' : 'minor';
console.log(typeof age, label);
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare ==
- Confondere null con undefined
- Considerare '0' come numero zero

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Qual è la differenza tra == e ===?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
