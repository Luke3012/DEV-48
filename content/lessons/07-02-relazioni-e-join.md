# Relazioni e JOIN

## In parole semplici

Combinare entità correlate comprendendo cardinalità e righe mancanti.

Una chiave esterna collega una riga a un'altra tabella. `INNER JOIN` conserva soltanto le corrispondenze; `LEFT JOIN` conserva tutte le righe della tabella a sinistra, anche quando la relazione manca.

## Le parole da riconoscere

`primary key`; `foreign key`; `INNER JOIN`; `LEFT JOIN`; `cardinalità`; `alias`

## Un esempio concreto

```sql
SELECT s.name, m.type
FROM subjects s
LEFT JOIN measures m ON m.subject_id = s.id;
```

INNER JOIN conserva le righe che hanno una corrispondenza; LEFT JOIN conserva tutte le righe di sinistra e usa NULL per i campi di destra mancanti. Un filtro sulla tabella destra in WHERE può eliminare quelle righe: controllo il caso del soggetto senza misura.

## Prova tu

Scrivi una LEFT JOIN che conservi anche il soggetto senza misure. Confronta il risultato con INNER JOIN: quale riga scompare e quale campo è NULL? Controlla il caso prima di aggiungere filtri.

## Dove ci si confonde spesso

- JOIN senza condizione
- INNER JOIN quando servono anche elementi senza relazione

## Domanda di verifica

> Differenza tra INNER JOIN e LEFT JOIN?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
