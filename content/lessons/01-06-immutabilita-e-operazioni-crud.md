# Immutabilità e operazioni CRUD

## In parole semplici

L'obiettivo di questa lezione è aggiungere, modificare ed eliminare elementi nel modo atteso da React.

Invece di modificare l'array esistente, ne produci uno nuovo: spread per aggiungere, `map` per aggiornare e `filter` per eliminare. React può così riconoscere il cambiamento e aggiornare la UI in modo prevedibile.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `spread`
- `map`
- `filter`
- `identità`
- `aggiornamento immutabile`
- `CRUD`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **spread, map, filter** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
const added = [...items, newItem];
const changed = items.map(x => x.id === id ? {...x, active: true} : x);
const removed = items.filter(x => x.id !== id);
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Push sullo state
- Cambiare direttamente una proprietà
- Perdere campi durante una copia

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Come aggiorni un elemento di un array senza modificarlo direttamente?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
