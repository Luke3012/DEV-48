# Reduce, Set e Map

## In parole semplici

L'obiettivo di questa lezione è aggregare valori e scegliere strutture dati adeguate per lookup e unicità.

`reduce` combina molti valori in un solo risultato. `Set` è comodo per eliminare duplicati, mentre `Map` associa chiavi a valori ed è utile quando cerchi spesso un elemento per identificatore.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `reduce`
- `accumulatore`
- `Set`
- `Map`
- `unicità`
- `lookup`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **reduce, accumulatore, Set** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
const total = orders.reduce((sum, order) => sum + order.amount, 0);
const zones = [...new Set(users.map(u => u.zone))];
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare reduce per rendere il codice inutilmente compatto
- Confondere Map con map

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quando preferiresti un oggetto Map rispetto a un array?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
