# Come affrontare un live coding

## In parole semplici

Trasformare una richiesta vaga in passi verificabili senza precipitarsi sulla tastiera.

Prima di scrivere, ripeti il problema con parole tue e concorda un esempio. In questo modo eviti di risolvere bene la domanda sbagliata e dai all'intervistatore la possibilità di correggere subito un equivoco.

Affronta il live coding come una sessione di costruzione: prima rendi preciso il problema, poi prova una soluzione. Non serve un interlocutore: anche quando studi da solo, scrivere un esempio di input e output evita di lavorare sul requisito sbagliato. Qui useremo un archivio di soggetti, ripreso in alcuni esercizi e laboratori.

## Le parole da riconoscere

`requisiti`; `input e output`; `casi limite`; `pseudocodice`; `verifica incrementale`

## Un esempio concreto

```text
// Richiesta: mostrare solo i soggetti attivi.
// Input: [{name: 'Anna', active: true}, {name: 'Mario', active: false}]
// Output atteso: ['Anna']
// Caso limite: [] deve produrre []
// Passi: selezionare gli attivi, poi estrarre i nomi.
```

La parola 'mostrare' non basta: l'output stabilisce se servono oggetti o soltanto nomi. Il caso vuoto chiarisce che non è un errore. Prima di implementare, annota anche se l'input può essere modificato; nel percorso lo conserveremo quando il contratto lo richiede.

## Prova tu

Ricevi una richiesta diversa: cercare un soggetto per ID. Scrivi il risultato per un ID presente e uno assente, senza ancora programmare. Decidi se l'assenza deve dare `undefined` oppure un errore, e motivala.

## Dove ci si confonde spesso

- Iniziare a programmare senza aver ripetuto il requisito
- Restare in silenzio quando ci si blocca

## Domanda di verifica

> Cosa fai nei primi due minuti di un esercizio tecnico?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
