# Generics essenziali per Collezioni e Risposte API

I generics consentono di scrivere componenti, servizi e modelli che operano su tipi diversi pur mantenendo la garanzia di sicurezza statica del compilatore.

## Che cosa sa il compilatore del dato

### Modello Generico per Risposte Paginate:
```typescript
export interface PaginatedList<T> {
    items: T[];
    pageNumber: number;
    pageSize: number;
    totalCount: number;
}
```
Possiamo ora riutilizzare `PaginatedList<UserDto>`, `PaginatedList<OrderDto>`, ecc., senza duplicare codice!

### Vincoli con `extends`:
```typescript
export interface HasId { id: number; }

export function findById<T extends HasId>(list: T[], id: number): T | undefined {
    return list.find(item => item.id === id);
}
```

## Segui il tipo mentre il dato cambia forma

```typescript
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
}

export function wrapData<T>(data: T): { payload: T } {
  return { payload: data };
}
```

### Controlla il contratto su un dato reale

1. In `PaginatedResponse<T>`, `T` rappresenta il tipo degli elementi contenuti in `items`; il totale resta un numero indipendente.
2. Quando usi `PaginatedResponse<UserDto>`, `items` diventa `UserDto[]` senza duplicare la struttura per ogni risorsa.
3. `wrapData<T>` riceve un valore e lo restituisce dentro `payload` conservando il tipo: se passa una stringa, `payload` è ancora una stringa.
4. Prova il wrapper con un numero e con un oggetto. Verifica che TypeScript segnali l'accesso a una proprietà che il tipo ricevuto non possiede.

## Estendi il contratto

```typescript
export interface ApiResponseEnvelope<T> {
    data: T;
    status: number;
    success: boolean;
}
```

## Dove il controllo statico si ferma

- Scrivere codice duplicato per ogni modello invece di usare un wrapper generico
- usare generics complessi non necessari.

> **Quale garanzia hai davvero?** Cosa significa il parametro `<T>` nella dichiarazione di una funzione o interfaccia?
