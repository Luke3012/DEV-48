# Union e narrowing

## In parole semplici

Rappresentare stati alternativi e restringere il tipo in modo sicuro.

Una risposta remota può essere in caricamento, vuota, riuscita o fallita. Una discriminated union collega ogni status ai soli campi validi per quello stato, così il controllo di status restringe il tipo prima che la UI legga data o message.

## Le parole da riconoscere

`union`; `literal type`; `discriminated union`; `typeof`; `in`; `narrowing`; `never`

## Un esempio concreto

```typescript
type Result = {status:'ok'; data:string[]} | {status:'error'; message:string};
function render(r:Result){ return r.status === 'ok' ? r.data.join(', ') : r.message; }
```

Un risultato remoto può essere in caricamento, riuscire con dati, riuscire senza righe oppure fallire. Un oggetto con tutti i campi opzionali non spiega quali combinazioni siano ammesse. Una discriminated union associa invece ogni status alla forma valida per quello stato:

~~~typescript
type Subject = { id: number; name: string };

type ArchiveState =
  | { status: "loading" }
  | { status: "success"; data: Subject[] }
  | { status: "empty" }
  | { status: "error"; message: string };
~~~

Quando controlli result.status, TypeScript restringe i casi possibili:

~~~typescript
function assertNever(value: never): never {
  throw new Error("Stato non gestito");
}

function labelForState(state: ArchiveState): string {
  switch (state.status) {
    case "loading": return "Caricamento…";
    case "error": return state.message;
    case "empty": return "Nessun soggetto";
    case "success": return state.data.length + " soggetti";
    default: return assertNever(state);
  }
}
~~~

Nel ramo `error` esiste `message`; nel ramo `success` esiste `data`. Il controllo su `status` restringe `state` al caso corrente. `assertNever` rende esplicita l'esaustività: se aggiungi un nuovo status e dimentichi il relativo ramo, TypeScript segnala il valore che non è più `never`.

Il tipo rende più difficile scrivere una UI che tenta di mostrare una proprietà assente.

Questa garanzia vale durante il controllo TypeScript del programma. I tipi vengono rimossi a runtime: una risposta JSON non diventa valida solo perché la variabile è annotata ArchiveState. Prima di usarla bisogna controllare i dati esterni con una guardia runtime, come nella lezione Null, unknown e confini esterni.

## Prova tu

Definisci LoadResult come union success con data:string[] oppure error con message:string. Implementa `describe(result)` restituendo il messaggio d'errore oppure il numero di elementi seguito da ' soggetti'. Non usare any o as. I test eseguono i rami; il controllo completo dei tipi richiede tsc.

## Dove ci si confonde spesso

- Asserzioni as usate per forzare
- Union troppo generiche
- Rami non esaustivi

## Domanda di verifica

> Che vantaggio offre una discriminated union?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
