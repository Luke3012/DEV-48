# Moduli ed organizzazione del codice

## In parole semplici

Prima di iniziare, ripassa [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Separare responsabilità usando export e import comprensibili.

Un modulo espone soltanto ciò che gli altri file devono usare. Import ed export ben scelti mostrano le dipendenze reali e impediscono che un singolo file diventi il contenitore di tutta l'applicazione.

Import ed export sono prerequisiti dei file React del laboratorio. Un export nominato espone un nome preciso; un export default espone un valore principale che il chiamante può rinominare. I percorsi relativi partono dal file che importa. Nei moduli browser serve uno script di tipo module; Vite configura il caricamento per il progetto React.

## Le parole da riconoscere

`export nominato`; `export default`; `import`; `modulo`; `dipendenza`; `API pubblica`

## Un esempio concreto

```javascript
// subjects.mjs
export function activeNames(items) {
  return items.filter(item => item.active).map(item => item.name);
}
export default function count(items) { return items.length; }

// app.mjs (file separato nella stessa cartella)
import count, { activeNames } from './subjects.mjs';
console.log(count([]), activeNames([])); // 0, []
```

Il nome tra graffe deve corrispondere all'export nominato, salvo un alias con `as`. `count` è il nome locale scelto per il default. Crea davvero due file: concatenare entrambi i frammenti nello stesso editor non verifica la risoluzione del modulo. Con Node esegui `node app.mjs`; nel browser usa un server locale e `<script type="module">`.

## Prova tu

Sposta `activeNames` in un modulo, importalo e prova un input vuoto. Rinomina poi solo l'import default. Se compare 'export not found', confronta il nome importato e quello esportato prima di modificare la funzione.

## Dove ci si confonde spesso

- Dipendenze circolari
- Esportare dettagli interni
- File contenitore gigantesco

## Domanda di verifica

> Differenza tra export nominato ed export default?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules).
