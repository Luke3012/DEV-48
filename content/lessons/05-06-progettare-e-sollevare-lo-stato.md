# Progettare e sollevare lo stato

## In parole semplici

L'obiettivo di questa lezione è collocare ogni informazione nel proprietario comune più vicino evitando duplicazioni.

Lo state dovrebbe vivere nel componente comune più vicino a tutti quelli che lo usano. Un valore calcolabile da props e state esistenti non va duplicato: puoi ricalcolarlo durante il render.

### Perché è utile

In React la domanda principale è sempre la stessa: da quali dati dipende questa parte dell'interfaccia? Individua chi possiede quei dati e lascia che il rendering descriva ciò che l'utente deve vedere in quel momento.

## Le parole da riconoscere

- `single source of truth`
- `lifting state`
- `derived state`
- `normalizzazione`
- `prop drilling`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **single source of truth, lifting state, derived state** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
const visible = items.filter(item => item.name.toLowerCase().includes(query.toLowerCase()));
// visible è derivato: non richiede un secondo useState.
```

Distingui props, stato e valori calcolati. Poi segui l'evento: quale setter viene chiamato e quale parte della UI cambia al rendering successivo?

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Duplicare stato derivabile
- Sincronizzare copie della stessa informazione con effect

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Come riconosci uno state che dovrebbe essere derivato?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
