# Array: map, filter, find e some

## In parole semplici

L'obiettivo di questa lezione è trasformare e interrogare collezioni senza cicli confusi.

Questi metodi rispondono a domande diverse: `map` trasforma tutti gli elementi, `filter` ne conserva alcuni, `find` cerca il primo e `some` verifica se ne esiste almeno uno. Scegli il metodo partendo dal risultato che ti serve.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `map`
- `filter`
- `find`
- `some`
- `every`
- `callback`
- `array originale`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **map, filter, find** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
const activeNames = users
  .filter(user => user.active)
  .map(user => user.name);
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare map quando serve filter
- Dimenticare che find può restituire undefined

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quando useresti find invece di filter?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
