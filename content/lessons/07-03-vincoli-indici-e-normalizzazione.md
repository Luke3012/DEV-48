# Vincoli, indici e normalizzazione

## In parole semplici

L'obiettivo di questa lezione è proteggere integrità e prestazioni senza duplicare dati inutilmente.

I vincoli impediscono che nel database entrino dati incoerenti. Gli indici velocizzano alcune letture ma occupano spazio e rallentano le scritture, quindi vanno scelti osservando le query reali.

### Perché è utile

Con SQL conviene tradurre la richiesta in una domanda precisa sui dati: quali righe servono, come sono collegate e in quale ordine devono uscire. Prima pensa al risultato, poi scrivi la query.

## Le parole da riconoscere

- `NOT NULL`
- `UNIQUE`
- `CHECK`
- `FOREIGN KEY`
- `index`
- `normalizzazione`
- `query plan`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **NOT NULL, UNIQUE, CHECK** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
CREATE INDEX idx_subjects_zone_active ON subjects(zone, active);
```

Leggi prima `FROM` e `JOIN`, poi i filtri e infine le colonne restituite. Immagina due o tre righe concrete per controllare il risultato.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Indice su ogni colonna
- Duplicazione di dati derivabili
- Vincoli solo nell'app

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Qual è il costo di mantenere un indice?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
