# Git: working tree, staging e commit

## In parole semplici

Capire cosa viene registrato e produrre commit piccoli e descrittivi.

Il working tree contiene ciò che stai modificando; lo staging seleziona ciò che entrerà nel prossimo commit. Un commit piccolo e coerente racconta una modifica comprensibile e rende più semplice annullarla o revisionarla.

## Le parole da riconoscere

`working tree`; `staging area`; `commit`; `git status`; `git diff`; `git add`; `git restore`

## Un esempio concreto

```text
git status
git diff
git add src/subjects.js
git diff --staged
git commit -m "feat: add subject filtering"
```

git diff mostra le modifiche del working tree rispetto allo staging; git diff --staged mostra ciò che lo staging aggiungerà al prossimo commit rispetto a HEAD. Controllo entrambi: un file può avere contemporaneamente una parte già staged e altre modifiche non staged.

## Prova tu

Modifichi due righe, aggiungi il file allo staging e modifichi una terza riga. Prevedi cosa mostrano git diff e git diff --staged e quale contenuto entrerà nel commit. Verifica in una repository didattica separata.

## Dove ci si confonde spesso

- Git add . senza controllare
- Commit final version
- Credenziali versionate

## Domanda di verifica

> Differenza tra git diff e git diff --staged?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
