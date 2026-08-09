# Git: working tree, staging e commit

## In parole semplici

L'obiettivo di questa lezione è capire cosa viene registrato e produrre commit piccoli e descrittivi.

Il working tree contiene ciò che stai modificando; lo staging seleziona ciò che entrerà nel prossimo commit. Un commit piccolo e coerente racconta una modifica comprensibile e rende più semplice annullarla o revisionarla.

### Perché è utile

Questi strumenti servono a ridurre l'incertezza. Git rende leggibile la storia delle modifiche; test e debugger ti aiutano a dimostrare che un comportamento esiste davvero e continua a funzionare.

## Le parole da riconoscere

- `working tree`
- `staging area`
- `commit`
- `git status`
- `git diff`
- `git add`
- `git restore`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **working tree, staging area, commit** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
git status
git diff
git add src/subjects.js
git diff --staged
git commit -m "feat: add subject filtering"
```

Chiediti quale prova concreta offre questo comando o questo test. Se fallisse, il messaggio dovrebbe aiutarti a restringere il problema.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Git add . senza controllare
- Commit final version
- Credenziali versionate

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Differenza tra git diff e git diff --staged?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
