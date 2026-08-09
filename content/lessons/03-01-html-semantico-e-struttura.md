# HTML semantico e struttura

## In parole semplici

L'obiettivo di questa lezione è scegliere elementi che descrivono il significato, non soltanto l'aspetto.

Gli elementi semantici descrivono il ruolo del contenuto. Un `button` comunica già a browser e tecnologie assistive che può ricevere focus ed essere attivato: un `div` con un click non offre automaticamente lo stesso comportamento.

### Perché è utile

Una pagina ben costruita non è soltanto bella: comunica una struttura, funziona da tastiera e si adatta allo spazio disponibile. Parti dal significato degli elementi, poi occupati del loro aspetto.

## Le parole da riconoscere

- `header`
- `nav`
- `main`
- `section`
- `article`
- `button`
- `heading`
- `semantica`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **header, nav, main** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
<main>
  <h1>Archivio soggetti</h1>
  <section aria-labelledby="active-title">...</section>
</main>
```

Prima leggi la struttura HTML e prova a descriverla senza parlare di colori. Poi osserva come il CSS distribuisce lo spazio e che cosa succede restringendo la finestra.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Div per ogni cosa
- Gerarchia heading incoerente
- Elementi cliccabili non accessibili

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Perché un button è preferibile a un div con onClick?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
