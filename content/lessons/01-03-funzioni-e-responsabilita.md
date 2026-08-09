# Funzioni e responsabilità

## In parole semplici

L'obiettivo di questa lezione è scrivere funzioni piccole, prevedibili e con input/output espliciti.

Una buona funzione riceve pochi dati, svolge un compito riconoscibile e restituisce un risultato chiaro. Se per descriverla servono molti verbi, probabilmente contiene più responsabilità da separare.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `parametri`
- `return`
- `arrow function`
- `funzione pura`
- `default parameter`
- `early return`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **parametri, return, arrow function** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
function fullName(first, last = '') {
  if (!first) return 'Unknown';
  return `${first} ${last}`.trim();
}
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Funzioni che modificano variabili globali
- Troppi rami e responsabilità

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Che differenza c'è tra restituire un valore e produrre un side effect?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
