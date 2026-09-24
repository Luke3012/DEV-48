# Union Discriminate e Type Narrowing

## In parole semplici

L'obiettivo di questa lezione è gestire stati complessi (caricamento, successo, errore) con union discriminate eleganti e sicure.

Una union discriminata usa una proprietà comune (tag) per distinguere con certezza matematica quale forma di dato è presente, permettendo al compilatore di restringere il tipo automaticamente.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `discriminated union`
- `tag`
- `switch`
- `type narrowing`
- `exhaustive check`
- `never`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`discriminated union`, `tag`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export type AuthState =
    | { authenticated: true; user: string }
    | { authenticated: false; reason: string };
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare flag booleani multipli come `isLoading: boolean
- isError: boolean
- isSuccess: boolean` che possono generare stati impossibili.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché una union discriminata evita bug rispetto a molteplici flag booleani indipendenti?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
