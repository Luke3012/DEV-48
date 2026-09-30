# Branch, merge e conflitti

## In parole semplici

Isolare una modifica e integrare storie divergenti senza perdere lavoro.

Un branch separa una linea di lavoro. Un conflitto non è un errore automatico da cancellare: Git ti sta chiedendo quale combinazione delle due modifiche rappresenta il risultato corretto.

## Le parole da riconoscere

`branch`; `HEAD`; `switch`; `merge`; `conflict`; `rebase`; `remote`

## Un esempio concreto

```text
git switch -c feature/subject-search
# modifica, test, commit
git switch main
git merge feature/subject-search
```

HEAD indica il commit corrente, normalmente attraverso il branch attivo. In detached HEAD indica direttamente un commit. Un conflitto richiede scegliere la combinazione corretta delle modifiche e verificarla, non soltanto rimuovere i marcatori dal file.

## Prova tu

Due branch cambiano la stessa riga con requisiti entrambi validi. Descrivi come conservare le due intenzioni, controllare HEAD e verificare il risultato prima di registrare la risoluzione nel laboratorio Git.

## Dove ci si confonde spesso

- Risolvere un conflitto cancellando marcatori senza capire entrambe le versioni

## Domanda di verifica

> Che cosa rappresenta HEAD?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
