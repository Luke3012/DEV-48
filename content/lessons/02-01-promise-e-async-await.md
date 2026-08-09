# Promise e async/await

## In parole semplici

L'obiettivo di questa lezione è ragionare su operazioni che terminano in futuro senza bloccare il programma.

Una Promise rappresenta un risultato futuro: può essere ancora in attesa, completato oppure fallito. `await` sospende quella funzione, non l'intero programma, e rende più leggibile la sequenza delle operazioni asincrone.

### Perché è utile

Quando entra in gioco una richiesta di rete, il risultato non arriva subito e può anche non arrivare affatto. Per questo devi ragionare sia sul dato atteso sia sugli stati di attesa, errore e annullamento.

## Le parole da riconoscere

- `Promise`
- `pending`
- `fulfilled`
- `rejected`
- `async`
- `await`
- `concorrenza`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **Promise, pending, fulfilled** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
async function load() {
  try { return await getData(); }
  catch (error) { console.error(error); throw error; }
}
```

Individua il momento in cui parte l'operazione, quello in cui arriva la risposta e il punto in cui viene gestito un fallimento.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Dimenticare await
- Mescolare then e await
- Perdere gli errori asincroni

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Cosa restituisce sempre una funzione dichiarata async?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
