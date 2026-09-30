# PHP e ciclo di un plugin WordPress

## In parole semplici

Riconoscere struttura, hook e confini minimi di un plugin custom.

Un plugin registra funzioni sugli hook offerti da WordPress. L'azione esegue un comportamento in un momento preciso; il filtro riceve un valore, lo trasforma e deve restituirlo.

## Le parole da riconoscere

`PHP`; `plugin header`; `action`; `filter`; `shortcode`; `activation hook`; `namespace`

## Un esempio concreto

```text
<?php
/** Plugin Name: Subject Tools */
add_action('init', function () { /* register */ });
```

Un'action esegue un comportamento quando WordPress annuncia un evento; un filtro riceve un valore e deve restituire il valore trasformato. Per esempio un filtro può modificare un titolo. Non modifico il core e uso nomi distinti per evitare collisioni con altri plugin.

## Prova tu

Un plugin deve cambiare il titolo di una pagina senza modificare il core. Scegli action o filter e mostra un frammento che restituisce il valore trasformato; spiega l'errore di dimenticare return.

## Dove ci si confonde spesso

- Modificare il core
- Eseguire codice globale pesante
- Nomi di funzione generici

## Domanda di verifica

> Differenza tra action e filter in WordPress?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
