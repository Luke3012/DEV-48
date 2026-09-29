# Union Discriminate e Type Narrowing

## In parole semplici

L'obiettivo di questa lezione è gestire stati complessi (caricamento, successo, errore) con union discriminate eleganti e sicure.

Una union discriminata usa una proprietà comune (tag) per distinguere quale variante del tipo è presente, permettendo al compilatore di restringere il tipo automaticamente.

## Le parole da riconoscere

- `discriminated union`
- `tag`
- `switch`
- `type narrowing`
- `exhaustive check`
- `never`

## Anatomia e Sintassi del Codice

### Esempio di Union Discriminata per Stato di Caricamento:
```typescript
export type RequestState<T> =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: T }
    | { status: "error"; message: string };

function renderState<T>(state: RequestState<T>): string {
    switch (state.status) {
        case "idle": return "In attesa";
        case "loading": return "Caricamento in corso...";
        case "success": return `Caricato: ${JSON.stringify(state.data)}`;
        case "error": return `Errore: ${state.message}`;
    }
}
```
All'interno di ogni ramo del `switch`, TypeScript sa esattamente quali proprietà esistono (es. `data` esiste solo in `success`!).

## Un esempio concreto

```typescript
export type State =
  | { status: 'loading' }
  | { status: 'success'; data: string[] }
  | { status: 'error'; message: string };
```

### Seguilo passo per passo

1. Il campo `status` distingue i tre stati: `loading`, `success` ed `error`. Ogni variante espone solo i dati che le servono.
2. Con `status === 'success'`, TypeScript rende disponibile `data`; con `status === 'error'`, rende disponibile `message`.
3. Nel ramo `loading` non esiste né `data` né `message`. Una `switch` su `status` rende visibili i casi mancanti e può essere resa esaustiva con `never`.
4. Aggiungi uno stato `cancelled` con una propria proprietà e aggiorna il gestore. Controlla che non sia possibile leggere `message` da quello stato.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```typescript
export type AuthState =
    | { authenticated: true; user: string }
    | { authenticated: false; reason: string };
```

## Dove ci si confonde spesso

- Usare flag booleani multipli come `isLoading: boolean
- isError: boolean
- isSuccess: boolean` che possono generare stati impossibili.

## Domanda di verifica

> Perché una union discriminata evita bug rispetto a molteplici flag booleani indipendenti?
