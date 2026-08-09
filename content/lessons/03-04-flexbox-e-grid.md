# Flexbox e Grid

## In parole semplici

L'obiettivo di questa lezione è scegliere il sistema di layout in base alla relazione tra gli elementi.

Flexbox distribuisce elementi lungo un asse ed è ideale per righe e colonne di componenti. Grid controlla contemporaneamente righe e colonne ed è più adatto alla struttura complessiva di una pagina o di una griglia di card.

### Perché è utile

Una pagina ben costruita non è soltanto bella: comunica una struttura, funziona da tastiera e si adatta allo spazio disponibile. Parti dal significato degli elementi, poi occupati del loro aspetto.

## Le parole da riconoscere

- `asse principale`
- `asse trasversale`
- `gap`
- `flex-grow`
- `grid-template-columns`
- `minmax`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **asse principale, asse trasversale, gap** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
.toolbar { display:flex; align-items:center; gap:.75rem; }
.cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(16rem,1fr)); gap:1rem; }
```

Prima leggi la struttura HTML e prova a descriverla senza parlare di colori. Poi osserva come il CSS distribuisce lo spazio e che cosa succede restringendo la finestra.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare position absolute per layout ordinari
- Non capire quale sia l'asse attivo

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quando preferiresti Grid a Flexbox?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
