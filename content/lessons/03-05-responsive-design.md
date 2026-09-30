# Responsive design

## In parole semplici

Progettare layout fluidi che restano leggibili su viewport differenti.

Un layout responsive non è una versione desktop rimpicciolita. Parte da misure fluide, lascia che il contenuto occupi lo spazio disponibile e introduce un breakpoint soltanto quando il layout smette di funzionare bene.

## Le parole da riconoscere

`mobile first`; `media query`; `unità relative`; `max-width`; `overflow`; `viewport`

## Un esempio concreto

```html
.page { width:min(100% - 2rem, 72rem); margin-inline:auto; }
@media (min-width: 48rem) { .sidebar { display:block; } }
```

Mobile first significa partire dal layout per lo spazio ridotto e aggiungere regole quando più spazio permette una struttura diversa. Il breakpoint risponde al contenuto: provo larghezze intermedie, testo lungo e zoom, evitando di legarlo soltanto a un modello di telefono.

## Prova tu

Crea una pagina con viewport configurato, larghezza fluida e max-width, con un breakpoint min-width che passa da una a due colonne. Verifica a 320px, 768px e con zoom 200%. Il runner controlla la presenza delle regole, non overflow e leggibilità.

## Dove ci si confonde spesso

- Breakpoint legati a singoli dispositivi
- Larghezze fisse
- Overflow nascosto indiscriminato

## Domanda di verifica

> Cosa significa progettare mobile first?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
