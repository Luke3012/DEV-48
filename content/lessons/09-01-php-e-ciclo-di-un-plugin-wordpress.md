# PHP e ciclo di un plugin WordPress

## In parole semplici

L'obiettivo di questa lezione è riconoscere struttura, hook e confini minimi di un plugin custom.

Un plugin registra funzioni sugli hook offerti da WordPress. L'azione esegue un comportamento in un momento preciso; il filtro riceve un valore, lo trasforma e deve restituirlo.

### Perché è utile

In WordPress il codice vive dentro un sistema già avviato. Devi capire in quale momento agganciare la tua funzione e trattare ogni dato ricevuto come non affidabile fino a quando non viene controllato.

## Le parole da riconoscere

- `PHP`
- `plugin header`
- `action`
- `filter`
- `shortcode`
- `activation hook`
- `namespace`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **PHP, plugin header, action** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
<?php
/** Plugin Name: Subject Tools */
add_action('init', function () { /* register */ });
```

Individua l'hook, il dato ricevuto e il punto in cui viene sanitizzato o mostrato. Sono i tre passaggi che spiegano quasi tutto il frammento.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Modificare il core
- Eseguire codice globale pesante
- Nomi di funzione generici

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Differenza tra action e filter in WordPress?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
