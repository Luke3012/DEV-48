# Interfacce vs Type Alias e Contratti di Dati

Interfacce e type alias descrivono gli oggetti attesi e aiutano il compilatore a rilevare campi e tipi incoerenti. Non verificano i dati ricevuti a runtime: un JSON esterno può violare il contratto e richiedere validazione.

## Che cosa sa il compilatore del dato

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

## Segui il tipo mentre il dato cambia forma

```typescript
export interface UserDto {
  readonly id: number;
  name: string;
  role?: string;
}

export type Status = 'active' | 'inactive';
```

### Controlla il contratto su un dato reale

1. `UserDto` richiede `id` numerico e `name` testuale; `readonly` impedisce di riassegnare `id` attraverso quel tipo.
2. `role?` è facoltativo: un oggetto valido può ometterlo, ma se lo include deve fornire una stringa.
3. `Status` ammette soltanto i valori letterali `active` e `inactive`; una stringa diversa produce un errore TypeScript.
4. Aggiungi un oggetto con `role` assente e uno con `role: 7`. Poi prova `status: 'pending'` per distinguere i campi facoltativi dall'unione chiusa.

## Estendi il contratto

```typescript
export interface ApiResponse<T> {
    success: boolean;
    data: T;
    timestamp: string;
}
```

## Dove il controllo statico si ferma

- Creare interfacce con proprietà senza tipo esplicito
- non sincronizzare i nomi dei campi tra backend C# e interfaccia TS.

> **Quale garanzia hai davvero?** Qual è la differenza pratica tra una proprietà obbligatoria e una opzionale in un'interfaccia?
