# Errori e validazione

## In parole semplici

L'obiettivo di questa lezione è rifiutare input invalidi e distinguere errore previsto da bug di programmazione.

Validare significa rifiutare presto un dato che non rispetta il contratto. Un errore utile dice che cosa non va e lascia al livello corretto la scelta tra mostrare un messaggio, riprovare o interrompere l'operazione.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `throw`
- `Error`
- `try/catch`
- `validazione`
- `guard clause`
- `messaggio utile`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **throw, Error, try/catch** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
function parseAge(value) {
  const age = Number(value);
  if (!Number.isFinite(age) || age < 0) throw new Error('Invalid age');
  return age;
}
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Catturare tutto e ignorare l'errore
- Mostrare dettagli sensibili all'utente

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quando è corretto lanciare un errore invece di restituire null?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
