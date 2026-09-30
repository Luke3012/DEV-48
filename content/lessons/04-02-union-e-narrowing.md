# Union e narrowing

## In parole semplici

Rappresentare stati alternativi e restringere il tipo in modo sicuro.

Una union dichiara che un valore può assumere forme alternative. Controllando una proprietà discriminante, TypeScript restringe il tipo e ti permette di accedere soltanto ai campi validi per quel caso.

## Le parole da riconoscere

`union`; `literal type`; `discriminated union`; `typeof`; `in`; `narrowing`; `never`

## Un esempio concreto

```typescript
type Result = {status:'ok'; data:string[]} | {status:'error'; message:string};
function render(r:Result){ return r.status === 'ok' ? r.data.join(', ') : r.message; }
```

Una discriminated union collega lo status ai campi validi. Dopo aver controllato status === 'error' posso leggere message, mentre nel ramo success posso leggere data. Rappresento stati alternativi senza rendere opzionali tutti i campi e senza asserzioni che nascondono errori.

## Prova tu

Definisci LoadResult come union success con data:string[] oppure error con message:string. Implementa `describe(result)` restituendo il messaggio d'errore oppure il numero di elementi seguito da ' soggetti'. Non usare any o as. I test eseguono i rami; il controllo completo dei tipi richiede tsc.

## Dove ci si confonde spesso

- Asserzioni as usate per forzare
- Union troppo generiche
- Rami non esaustivi

## Domanda di verifica

> Che vantaggio offre una discriminated union?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
