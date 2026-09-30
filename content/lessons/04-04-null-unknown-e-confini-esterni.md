# Null, unknown e confini esterni

## In parole semplici

Trattare dati esterni come non affidabili prima di usarli nel dominio.

`unknown` ti obbliga a controllare un valore prima di usarlo, mentre `any` disattiva quella protezione. È la scelta corretta per JSON, input utente e altri dati che entrano dall'esterno.

## Le parole da riconoscere

`unknown`; `null`; `undefined`; `type guard`; `validation`; `optional chaining`; `boundary`

## Un esempio concreto

```typescript
function isSubject(value: unknown): value is {id:number; name:string} {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false;
  return 'id' in value && typeof value.id === 'number' && Number.isFinite(value.id) &&
    'name' in value && typeof value.name === 'string';
}
console.log(isSubject({id:1,name:'Anna'})); // true
console.log(isSubject({id:'1',name:9})); // false
```

unknown obbliga a restringere il tipo prima di accedere a proprietà o chiamare metodi; any disattiva quei controlli. Un JSON esterno può avere qualsiasi forma, quindi unknown rende visibile il confine da validare invece di nasconderlo con un cast.

## Prova tu

Correggi `isSubject(value: unknown)`: deve riconoscere un oggetto con id numero finito e name stringa, rifiutando null, array e campi con tipi sbagliati. La sola presenza di 'id' e 'name' non prova il contratto. I test eseguono il guard a runtime; il type checking completo resta distinto.

## Dove ci si confonde spesso

- Convertire unknown in un tipo con as
- Fidarsi del JSON
- Usare ! senza prova

## Domanda di verifica

> Perché unknown è preferibile ad any per un input esterno?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
