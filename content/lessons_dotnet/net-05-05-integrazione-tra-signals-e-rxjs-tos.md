# Integrazione tra Signals e RxJS: toSignal e toObservable

## In parole semplici

L'obiettivo di questa lezione è far convivere la semplicità dei Signals con la potenza degli operatori asincroni di RxJS.

I Signals rappresentano valori correnti dell'interfaccia; RxJS offre operatori per comporre flussi asincroni come debounce, retry e WebSocket. `@angular/core/rxjs-interop` fornisce API per integrarli quando il caso lo richiede.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `rxjs`
- `observable`
- `tosignal`
- `toobservable`
- `interoperabilita`
- `debounce`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`rxjs`, `observable`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Le Due Funzioni di Interoperabilità:
1. **`toSignal(observable$, options)`**:
   - Converte un Observable (come una chiamata `httpClient.get()`) in un Signal!
   - Sottoscrive e distrugge automaticamente l'Observable quando il componente si chiude.
   ```typescript
   users = toSignal(this.http.get<User[]>('/api/users'), { initialValue: [] });
   ```
2. **`toObservable(signal)`**:
   - Converte un Signal in un Observable per applicare operatori potenti come `debounceTime`, `switchMap` o `distinctUntilChanged`.
   ```typescript
   query$ = toObservable(this.searchQuery).pipe(
     debounceTime(300),
     switchMap(q => this.api.search(q))
   );
   ```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```typescript
const searchSignal = signal('');
const resultsSignal = toSignal(
  toObservable(searchSignal).pipe(
    debounceTime(300),
    switchMap(q => http.get('/api/search?q=' + q))
  ),
  { initialValue: [] }
);
```

### Seguilo passo per passo

1. `toObservable(searchSignal)` espone le modifiche della query come un flusso RxJS.
2. `debounceTime(300)` attende una pausa di 300 ms; `switchMap` avvia la richiesta più recente e si disiscrive dal flusso precedente quando arriva un nuovo termine.
3. `toSignal(..., { initialValue: [] })` rende i risultati leggibili dal template fin da subito, prima della prima risposta.
4. Digita rapidamente due termini e poi fermati. La ricerca parte dopo la pausa; controlla inoltre errori HTTP e contesto d'iniezione prima di usare `toSignal`.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class SearchBridge {
    query = signal('');
    setQuery(text: string) { this.query.set(text); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare di passare `{ initialValue: ... }` a `toSignal` con Observable che non emettono istantaneamente, causando un tipo `T | undefined`.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quando è preferibile usare RxJS rispetto a un semplice Signal?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
