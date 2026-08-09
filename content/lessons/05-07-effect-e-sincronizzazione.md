# Effect e sincronizzazione

## In parole semplici

L'obiettivo di questa lezione è usare useEffect solo per sincronizzarsi con sistemi esterni e gestire cleanup.

`useEffect` serve a sincronizzare React con qualcosa di esterno, per esempio una richiesta, un timer o una subscription. Se l'operazione può continuare dopo un nuovo render, la cleanup deve annullarla o scollegarla.

### Perché è utile

In React la domanda principale è sempre la stessa: da quali dati dipende questa parte dell'interfaccia? Individua chi possiede quei dati e lascia che il rendering descriva ciò che l'utente deve vedere in quel momento.

## Le parole da riconoscere

- `useEffect`
- `dependency array`
- `cleanup`
- `subscription`
- `fetch`
- `race condition`
- `Strict Mode`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **useEffect, dependency array, cleanup** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
useEffect(() => {
 const controller=new AbortController();
 load(controller.signal);
 return () => controller.abort();
}, [subjectId]);
```

Segui il ciclo dell'effect: parte quando cambia `subjectId`, crea un controller e avvia il caricamento. Prima del nuovo effect o dello smontaggio, la cleanup chiama `abort()` e impedisce alla richiesta precedente di continuare inutilmente.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Usare effect per calcoli derivabili
- Dipendenze mancanti
- Cleanup assente

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quali operazioni non richiedono useEffect?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
