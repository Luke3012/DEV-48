# Responsive design

## In parole semplici

L'obiettivo di questa lezione è progettare layout fluidi che restano leggibili su viewport differenti.

Un layout responsive non è una versione desktop rimpicciolita. Parte da misure fluide, lascia che il contenuto occupi lo spazio disponibile e introduce un breakpoint soltanto quando il layout smette di funzionare bene.

### Perché è utile

Una pagina ben costruita non è soltanto bella: comunica una struttura, funziona da tastiera e si adatta allo spazio disponibile. Parti dal significato degli elementi, poi occupati del loro aspetto.

## Le parole da riconoscere

- `mobile first`
- `media query`
- `unità relative`
- `max-width`
- `overflow`
- `viewport`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **mobile first, media query, unità relative** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
.page { width:min(100% - 2rem, 72rem); margin-inline:auto; }
@media (min-width: 48rem) { .sidebar { display:block; } }
```

Prima leggi la struttura HTML e prova a descriverla senza parlare di colori. Poi osserva come il CSS distribuisce lo spazio e che cosa succede restringendo la finestra.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Breakpoint legati a singoli dispositivi
- Larghezze fisse
- Overflow nascosto indiscriminato

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Cosa significa progettare mobile first?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
