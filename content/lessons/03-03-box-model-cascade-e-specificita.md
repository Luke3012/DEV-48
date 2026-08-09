# Box model, cascade e specificità

## In parole semplici

L'obiettivo di questa lezione è prevedere dimensioni e regole CSS effettivamente applicate.

Ogni elemento occupa spazio attraverso contenuto, padding, bordo e margine. Quando due regole competono, la cascade considera origine, importanza, specificità e ordine: aumentare sempre la specificità rende il CSS difficile da mantenere.

### Perché è utile

Una pagina ben costruita non è soltanto bella: comunica una struttura, funziona da tastiera e si adatta allo spazio disponibile. Parti dal significato degli elementi, poi occupati del loro aspetto.

## Le parole da riconoscere

- `content`
- `padding`
- `border`
- `margin`
- `box-sizing`
- `cascade`
- `specificità`
- `inheritance`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **content, padding, border** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
*, *::before, *::after { box-sizing: border-box; }
.card { padding: 1rem; border: 1px solid #334155; }
```

Prima leggi la struttura HTML e prova a descriverla senza parlare di colori. Poi osserva come il CSS distribuisce lo spazio e che cosa succede restringendo la finestra.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Compensare la specificità con !important
- Dimenticare box-sizing

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Come viene determinata la regola CSS vincente?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
