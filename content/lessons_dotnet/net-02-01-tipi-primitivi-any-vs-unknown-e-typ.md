# Tipi primitivi, Any vs Unknown e Type Inference

## In parole semplici

L'obiettivo di questa lezione è sviluppare con tipi statici robusti evitando `any` e sfruttando l'inferenza di TypeScript.

L'inferenza di tipi permette a TypeScript di dedurre automaticamente il tipo di una variabile dal valore assegnato, rendendo il codice leggibile senza sacrificare la sicurezza.

## Le parole da riconoscere

- `typescript`
- `primitivi`
- `any`
- `unknown`
- `type inference`
- `type assertion`

## Anatomia e Sintassi del Codice

### Differenza Cruciale tra `any` e `unknown`:
- **`any`**: disattiva molti controlli statici su quel valore; un'operazione non valida può quindi emergere solo a runtime.
- **`unknown`**: indica un tipo sconosciuto ma sicuro. TypeScript costringe a effettuare un controllo a runtime (type narrowing con `typeof` o `instanceof`) prima di poter interagire con il valore.

```typescript
let input: unknown = "testo";
if (typeof input === "string") {
    console.log(input.toUpperCase()); // Il controllo typeof restringe il tipo in questo ramo.
}
```

## Un esempio concreto

```typescript
let age = 30; // Inferito come number
let rawData: unknown = JSON.parse('{"id":1}');
if (typeof rawData === 'object' && rawData !== null) {
  console.log('Oggetto valido');
}
```

### Seguilo passo per passo

1. TypeScript inferisce `age` come `number` dal valore `30`; non serve ripetere un tipo già evidente.
2. `JSON.parse` produce dati esterni: assegnarli a `unknown` impedisce di usarli come un tipo specifico prima di controllarli.
3. La condizione esclude `null` e verifica che il valore sia un oggetto. Questo esempio non dimostra però che l'oggetto contenga `id`: per quello serve una validazione del contratto.
4. Passa alla condizione una stringa, `null` e l'oggetto dell'esempio. Nota quali valori entrano nel blocco e quale controllo ulteriore servirebbe prima di leggere `id`.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```typescript
export function safeStringLength(value: unknown): number {
    if (typeof value === "string") {
        return value.length;
    }
    return 0;
}
```

## Dove ci si confonde spesso

- Usare `any` per silenziare i messaggi del compilatore
- dimenticare che `unknown` richiede un type guard.

## Domanda di verifica

> Quale controllo richiede unknown prima di usare un valore, e che cosa consente invece any?
