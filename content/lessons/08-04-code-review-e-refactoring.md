# Code review e refactoring

## In parole semplici

Migliorare struttura senza cambiare comportamento e comunicare rischi concreti.

La review controlla correttezza, chiarezza e rischi, non lo stile personale dell'autore. Il refactoring migliora la struttura senza cambiare il comportamento e richiede test che lo dimostrino.

## Le parole da riconoscere

`refactoring`; `behavior preservation`; `code smell`; `cohesion`; `coupling`; `review`; `technical debt`

## Un esempio concreto

```text
// Prima caratterizza il comportamento con test, poi estrai una responsabilità alla volta.
```

Prima caratterizzo il comportamento del file con casi rilevanti. Estraggo una responsabilità per volta, mantenendo invariati input e output, poi eseguo i test. Distinguo il refactoring da una correzione funzionale per poter attribuire ogni regressione a una modifica circoscritta.

## Prova tu

Vuoi estrarre la ricerca da un componente che mostra anche form e lista. Definisci prima i casi da preservare, poi una singola estrazione e una prova di regressione. Distingui il refactoring da un cambio del requisito.

## Dove ci si confonde spesso

- Grande riscrittura senza test
- Commenti sullo stile personale
- Nessuna priorità

## Domanda di verifica

> Come rifattorizzeresti in sicurezza un file di migliaia di righe?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
