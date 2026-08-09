# Scope, const, let e closure

## In parole semplici

L'obiettivo di questa lezione è comprendere dove vive una variabile e perché una funzione ricorda il contesto esterno.

Lo scope stabilisce da quali righe una variabile è visibile. Una closure nasce quando una funzione continua ad accedere alle variabili del luogo in cui è stata creata, anche dopo che quella funzione esterna è terminata.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `scope di blocco`
- `const`
- `let`
- `closure`
- `shadowing`
- `funzione interna`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **scope di blocco, const, let** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
function counter() {
  let value = 0;
  return () => ++value;
}
const next = counter();
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare var senza motivo
- Credere che const renda immutabile un oggetto

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Che cos'è una closure e quando può essere utile?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
