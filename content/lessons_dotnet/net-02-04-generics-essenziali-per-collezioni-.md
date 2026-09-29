# Generics essenziali per Collezioni e Risposte API

## In parole semplici

L'obiettivo di questa lezione è creare interfacce e funzioni riutilizzabili con parametri di tipo generici.

I generics consentono di scrivere componenti, servizi e modelli che operano su tipi diversi pur mantenendo la garanzia di sicurezza statica del compilatore.

## Le parole da riconoscere

- `generics`
- `type parameter`
- `t`
- `vincoli extends`
- `api response`
- `paginazione`

## Anatomia e Sintassi del Codice

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

## Un esempio concreto

```typescript
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
}

export function wrapData<T>(data: T): { payload: T } {
  return { payload: data };
}
```

### Seguilo passo per passo

1. In `PaginatedResponse<T>`, `T` rappresenta il tipo degli elementi contenuti in `items`; il totale resta un numero indipendente.
2. Quando usi `PaginatedResponse<UserDto>`, `items` diventa `UserDto[]` senza duplicare la struttura per ogni risorsa.
3. `wrapData<T>` riceve un valore e lo restituisce dentro `payload` conservando il tipo: se passa una stringa, `payload` è ancora una stringa.
4. Prova il wrapper con un numero e con un oggetto. Verifica che TypeScript segnali l'accesso a una proprietà che il tipo ricevuto non possiede.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```typescript
export interface ApiResponseEnvelope<T> {
    data: T;
    status: number;
    success: boolean;
}
```

## Dove ci si confonde spesso

- Scrivere codice duplicato per ogni modello invece di usare un wrapper generico
- usare generics complessi non necessari.

## Domanda di verifica

> Cosa significa il parametro `<T>` nella dichiarazione di una funzione o interfaccia?
