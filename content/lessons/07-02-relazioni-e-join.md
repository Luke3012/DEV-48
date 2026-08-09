# Relazioni e JOIN

## In parole semplici

L'obiettivo di questa lezione è combinare entità correlate comprendendo cardinalità e righe mancanti.

Una chiave esterna collega una riga a un'altra tabella. `INNER JOIN` conserva soltanto le corrispondenze; `LEFT JOIN` conserva tutte le righe della tabella a sinistra, anche quando la relazione manca.

### Perché è utile

Con SQL conviene tradurre la richiesta in una domanda precisa sui dati: quali righe servono, come sono collegate e in quale ordine devono uscire. Prima pensa al risultato, poi scrivi la query.

## Le parole da riconoscere

- `primary key`
- `foreign key`
- `INNER JOIN`
- `LEFT JOIN`
- `cardinalità`
- `alias`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **primary key, foreign key, INNER JOIN** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
SELECT s.name, m.type
FROM subjects s
LEFT JOIN measures m ON m.subject_id = s.id;
```

Leggi prima `FROM` e `JOIN`, poi i filtri e infine le colonne restituite. Immagina due o tre righe concrete per controllare il risultato.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- JOIN senza condizione
- INNER JOIN quando servono anche elementi senza relazione

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Differenza tra INNER JOIN e LEFT JOIN?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
