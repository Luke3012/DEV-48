# Caricamento dati e stati remoti

## In parole semplici

L'obiettivo di questa lezione è rappresentare esplicitamente idle, loading, success, empty ed error.

I dati remoti hanno più stati di una semplice lista: non ancora richiesti, in caricamento, riusciti, vuoti o falliti. Rappresentarli esplicitamente evita spinner eterni e schermate bianche.

### Perché è utile

In React la domanda principale è sempre la stessa: da quali dati dipende questa parte dell'interfaccia? Individua chi possiede quei dati e lascia che il rendering descriva ciò che l'utente deve vedere in quel momento.

## Le parole da riconoscere

- `remote state`
- `loading`
- `error`
- `retry`
- `empty state`
- `optimistic update`
- `cache`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **remote state, loading, error** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
if (status === 'loading') return <Spinner />;
if (status === 'error') return <ErrorPanel onRetry={load} />;
return data.length ? <List data={data}/> : <EmptyState/>;
```

Distingui props, stato e valori calcolati. Poi segui l'evento: quale setter viene chiamato e quale parte della UI cambia al rendering successivo?

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Mostrare schermata vuota durante il caricamento
- Ignorare retry e richieste concorrenti

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quali stati UI devi considerare quando interroghi una API?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
