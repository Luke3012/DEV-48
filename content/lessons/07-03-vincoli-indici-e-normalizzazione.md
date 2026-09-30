# Vincoli, indici e normalizzazione

## In parole semplici

Proteggere integrità e prestazioni senza duplicare dati inutilmente.

I vincoli impediscono che nel database entrino dati incoerenti. Gli indici velocizzano alcune letture ma occupano spazio e rallentano le scritture, quindi vanno scelti osservando le query reali.

## Le parole da riconoscere

`NOT NULL`; `UNIQUE`; `CHECK`; `FOREIGN KEY`; `index`; `normalizzazione`; `query plan`

## Un esempio concreto

```sql
CREATE INDEX idx_subjects_zone_active ON subjects(zone, active);
```

Un indice occupa spazio e va aggiornato quando cambiano i dati, aumentando il costo delle scritture. Può accelerare letture adatte alla sua struttura. Scelgo un indice da query reali e verifico il piano, evitando di indicizzare ogni colonna automaticamente.

## Prova tu

La query frequente cerca gli attivi di una zona. Proponi un indice e descrivi la lettura che può aiutare e la scrittura che deve mantenerlo. Nel lab-sql verifica anche un vincolo con un INSERT invalido.

## Dove ci si confonde spesso

- Indice su ogni colonna
- Duplicazione di dati derivabili
- Vincoli solo nell'app

## Domanda di verifica

> Qual è il costo di mantenere un indice?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
