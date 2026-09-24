# Generics essenziali per Collezioni e Risposte API

## In parole semplici

L'obiettivo di questa lezione è creare interfacce e funzioni riutilizzabili con parametri di tipo generici.

I generics consentono di scrivere componenti, servizi e modelli che operano su tipi diversi pur mantenendo la garanzia di sicurezza statica del compilatore.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `generics`
- `type parameter`
- `t`
- `vincoli extends`
- `api response`
- `paginazione`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`generics`, `type parameter`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export interface ApiResponseEnvelope<T> {
    data: T;
    status: number;
    success: boolean;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Scrivere codice duplicato per ogni modello invece di usare un wrapper generico
- usare generics complessi non necessari.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Cosa significa il parametro `<T>` nella dichiarazione di una funzione o interfaccia?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
