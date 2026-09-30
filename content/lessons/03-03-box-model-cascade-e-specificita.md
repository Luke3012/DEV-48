# Box model, cascade e specificità

## In parole semplici

Prevedere dimensioni e regole CSS effettivamente applicate.

Ogni elemento occupa spazio attraverso contenuto, padding, bordo e margine. Quando due regole competono, la cascade considera origine, importanza, specificità e ordine: aumentare sempre la specificità rende il CSS difficile da mantenere.

## Le parole da riconoscere

`content`; `padding`; `border`; `margin`; `box-sizing`; `cascade`; `specificità`; `inheritance`

## Un esempio concreto

```html
*, *::before, *::after { box-sizing: border-box; }
.card { padding: 1rem; border: 1px solid #334155; }
```

La cascade considera prima origine, importanza e livelli della cascade, poi specificità e ordine a parità delle condizioni precedenti. Una regola più specifica non vince sempre contro una regola importante. Controllo la regola applicata negli strumenti del browser prima di aggiungere !important.

## Prova tu

Una card larga 240px ha padding 16px e bordo 2px: con content-box occupa 276px. Scrivi HTML/CSS che mantenga la larghezza totale a 240px usando border-box. Il runner cerca le regole; misura la larghezza reale negli strumenti del browser.

## Dove ci si confonde spesso

- Compensare la specificità con !important
- Dimenticare box-sizing

## Domanda di verifica

> Come viene determinata la regola CSS vincente?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
