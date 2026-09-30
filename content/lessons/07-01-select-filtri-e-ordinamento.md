# SELECT, filtri e ordinamento

## In parole semplici

Estrarre solo righe e colonne necessarie con condizioni leggibili.

Una query leggibile seleziona soltanto le colonne utili, filtra con condizioni esplicite e ordina quando l'ordine fa parte del requisito. Senza `ORDER BY`, il database non promette un ordine stabile.

## Le parole da riconoscere

`SELECT`; `FROM`; `WHERE`; `AND`; `OR`; `ORDER BY`; `LIMIT`; `alias`

## Un esempio concreto

```sql
SELECT id, name, checks
FROM subjects
WHERE active = 1 AND zone = 'Centro'
ORDER BY checks DESC;
```

Nel modello logico parto da FROM e JOIN, filtro con WHERE, scelgo le colonne con SELECT e ordino con ORDER BY. L'ottimizzatore può eseguire fisicamente un piano diverso. Se l'ordine fa parte del requisito lo dichiaro, invece di fidarmi delle righe ottenute in una prova.

## Prova tu

Scrivi una query che restituisca id, name e checks dei soli soggetti attivi, ordinati per checks decrescente. Prevedi le righe prima di eseguirla e spiega perché l'ordine deve essere esplicito.

## Dove ci si confonde spesso

- SELECT * indiscriminato
- Condizioni ambigue
- Ordinamento dimenticato

## Domanda di verifica

> In quale ordine logico vengono valutate FROM, WHERE, SELECT e ORDER BY?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
