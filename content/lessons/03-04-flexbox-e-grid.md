# Flexbox e Grid

## In parole semplici

Scegliere il sistema di layout in base alla relazione tra gli elementi.

Flexbox distribuisce elementi lungo un asse ed è ideale per righe e colonne di componenti. Grid controlla contemporaneamente righe e colonne ed è più adatto alla struttura complessiva di una pagina o di una griglia di card.

## Le parole da riconoscere

`asse principale`; `asse trasversale`; `gap`; `flex-grow`; `grid-template-columns`; `minmax`

## Un esempio concreto

```html
.toolbar { display:flex; align-items:center; gap:.75rem; }
.cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(16rem,1fr)); gap:1rem; }
```

Uso Grid quando devo controllare righe e colonne insieme, come una griglia di card. Flexbox è adatto a una toolbar su un asse, con allineamento e distribuzione. Scelgo il layout in base alle relazioni tra gli elementi, non al numero di proprietà da ricordare.

## Prova tu

Crea una toolbar flex con due pulsanti e una griglia di card responsive con gap. Usa grid-template-columns con repeat e minmax. Il runner cerca le regole; nel browser controlla allineamento e passaggio da una a più colonne.

## Dove ci si confonde spesso

- Usare position absolute per layout ordinari
- Non capire quale sia l'asse attivo

## Domanda di verifica

> Quando preferiresti Grid a Flexbox?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
