# Tipi, interface e type

## In parole semplici

Descrivere il contratto dei dati e ottenere errori prima dell'esecuzione.

Un tipo descrive la forma che il codice si aspetta e permette all'editor di segnalare incoerenze prima dell'avvio. Non controlla però automaticamente un JSON ricevuto dalla rete: quel dato richiede validazione a runtime.

## Le parole da riconoscere

`type annotation`; `interface`; `type alias`; `optional property`; `readonly`; `structural typing`

## Un esempio concreto

```typescript
interface Subject { id: number; name: string; active: boolean; note?: string }
function label(subject: Subject): string { return subject.name; }
```

Una interface descrive un contratto a compile time, ma non valida il JSON a runtime. Un server può restituire un nome numerico anche se il tipo promette una stringa. Tratto il dato esterno come unknown e controllo la sua forma prima di usarlo.

## Prova tu

Definisci Subject con id:number, name:string, active:boolean e note opzionale. Implementa `label(subject: Subject): string` con il nome e la nota tra parentesi se presente. I test eseguono la logica TypeScript; non sostituiscono tsc né la validazione dei dati esterni.

## Dove ci si confonde spesso

- Usare any per silenziare errori
- Considerare i tipi come validazione runtime

## Domanda di verifica

> Interface TypeScript verifica davvero il JSON ricevuto dalla rete?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
