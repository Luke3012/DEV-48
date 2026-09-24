# Interfacce vs Type Alias e Contratti di Dati

## In parole semplici

L'obiettivo di questa lezione è modellare contratti di dati coerenti tra client Angular e DTO del backend .NET.

Le interfacce e i type alias consentono di stabilire contratti rigorosi per gli oggetti scambiati via API, prevenendo errori di battitura nei nomi dei campi o incongruenze nei tipi.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `interface`
- `type alias`
- `extends`
- `readonly`
- `optional`
- `contratto dati`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`interface`, `type alias`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### `interface` vs `type`:
- **`interface`**: ideale per descrivere la forma di oggetti e dati DTO. Supporta l'estensione con `extends` e la dichiarazione incrementale.
- **`type`**: ideale per unioni, tuple, tipi primitivi o tipi composti.

```typescript
export interface UserDto {
    readonly id: number;      // Immutabile dopo la creazione
    name: string;
    email: string;
    phoneNumber?: string;     // Proprietà opzionale con ?
}

export type UserRole = "Admin" | "Manager" | "Guest";
```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```typescript
export interface UserDto {
  readonly id: number;
  name: string;
  role?: string;
}

export type Status = 'active' | 'inactive';
```

### Seguilo passo per passo

1. `UserDto` richiede `id` numerico e `name` testuale; `readonly` impedisce di riassegnare `id` attraverso quel tipo.
2. `role?` è facoltativo: un oggetto valido può ometterlo, ma se lo include deve fornire una stringa.
3. `Status` ammette soltanto i valori letterali `active` e `inactive`; una stringa diversa produce un errore TypeScript.
4. Aggiungi un oggetto con `role` assente e uno con `role: 7`. Poi prova `status: 'pending'` per distinguere i campi facoltativi dall'unione chiusa.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export interface ApiResponse<T> {
    success: boolean;
    data: T;
    timestamp: string;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Creare interfacce con proprietà senza tipo esplicito
- non sincronizzare i nomi dei campi tra backend C# e interfaccia TS.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è la differenza pratica tra una proprietà obbligatoria e una opzionale in un'interfaccia?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
