# Branch, merge e conflitti

## In parole semplici

L'obiettivo di questa lezione è isolare una modifica e integrare storie divergenti senza perdere lavoro.

Un branch separa una linea di lavoro. Un conflitto non è un errore automatico da cancellare: Git ti sta chiedendo quale combinazione delle due modifiche rappresenta il risultato corretto.

### Perché è utile

Questi strumenti servono a ridurre l'incertezza. Git rende leggibile la storia delle modifiche; test e debugger ti aiutano a dimostrare che un comportamento esiste davvero e continua a funzionare.

## Le parole da riconoscere

- `branch`
- `HEAD`
- `switch`
- `merge`
- `conflict`
- `rebase`
- `remote`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **branch, HEAD, switch** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
git switch -c feature/subject-search
# modifica, test, commit
git switch main
git merge feature/subject-search
```

Chiediti quale prova concreta offre questo comando o questo test. Se fallisse, il messaggio dovrebbe aiutarti a restringere il problema.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Risolvere un conflitto cancellando marcatori senza capire entrambe le versioni

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Che cosa rappresenta HEAD?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
