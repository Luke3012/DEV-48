# Tipi primitivi, Any vs Unknown e Type Inference

## In parole semplici

L'obiettivo di questa lezione è sviluppare con tipi statici robusti evitando `any` e sfruttando l'inferenza di TypeScript.

L'inferenza di tipi permette a TypeScript di dedurre automaticamente il tipo di una variabile dal valore assegnato, rendendo il codice leggibile senza sacrificare la sicurezza.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `typescript`
- `primitivi`
- `any`
- `unknown`
- `type inference`
- `type assertion`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`typescript`, `primitivi`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export function safeStringLength(value: unknown): number {
    if (typeof value === "string") {
        return value.length;
    }
    return 0;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare `any` per silenziare i messaggi del compilatore
- dimenticare che `unknown` richiede un type guard.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché `unknown` è infinitamente più sicuro di `any` in TypeScript?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
