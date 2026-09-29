# Integrazione tra Signals e RxJS: toSignal e toObservable

## In parole semplici

L'obiettivo di questa lezione è far convivere la semplicità dei Signals con la potenza degli operatori asincroni di RxJS.

I Signals rappresentano valori correnti dell'interfaccia; RxJS offre operatori per comporre flussi asincroni come debounce, retry e WebSocket. `@angular/core/rxjs-interop` fornisce API per integrarli quando il caso lo richiede.

### Nel percorso

Approfondimento facoltativo: puoi riprenderlo dopo aver completato la pratica essenziale del modulo.

Da conoscere: [Valori derivati intelligenti con computed()](net-05-02-valori-derivati-intelligenti-con-co.md); [Effetti collaterali controllati con effect()](net-05-03-effetti-collaterali-controllati-con.md).

Un Observable descrive emissioni nel tempo; `subscribe` avvia l'ascolto e `unsubscribe` lo interrompe. `pipe` compone operatori; `switchMap` sostituisce l'ascolto della richiesta precedente. Le richieste HttpClient partono alla sottoscrizione. `toSignal` e `toObservable` vanno creati in un contesto di iniezione, per esempio nei campi di un componente. La conversione è utile per ricerca remota e flussi asincroni; per un totale locale basta `computed`.

## Le parole da riconoscere

- `rxjs`
- `observable`
- `tosignal`
- `toobservable`
- `interoperabilita`
- `debounce`

## Anatomia e Sintassi del Codice

### Le Due Funzioni di Interoperabilità:
1. **`toSignal(observable$, options)`**:
   - Converte un Observable (come una chiamata `httpClient.get()`) in un Signal!
   - Sottoscrive il flusso e rilascia la sottoscrizione alla distruzione del contesto Angular.
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

Nell’esempio il recupero dell’errore è dentro `switchMap`: una richiesta fallita produce una lista vuota ma lascia attive le ricerche successive. È una semplificazione per studiare il flusso; in un’interfaccia completa distingui errore e nessun risultato. `params` codifica il termine senza concatenarlo nell’URL.

## Un esempio concreto

```typescript
import { Component, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { catchError, debounceTime, distinctUntilChanged, of, switchMap } from 'rxjs';

@Component({
  selector: 'app-search',
  template: `<input #field (input)="searchSignal.set(field.value)" aria-label="Ricerca" />
    @for (name of resultsSignal(); track name) { <p>{{ name }}</p> }`
})
export class SearchComponent {
  private readonly http = inject(HttpClient);
  readonly searchSignal = signal('');
  readonly resultsSignal = toSignal(
    toObservable(this.searchSignal).pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(q => this.http.get<string[]>('/api/search', { params: { q } }).pipe(
        catchError(() => of([] as string[]))
      ))
    ),
    { initialValue: [] as string[] }
  );
}
// Registra provideHttpClient() in app.config.ts.
// L’API GET /api/search?q=... deve restituire un array di nomi univoci.
// L’URL relativo richiede stesso host o proxy verso il backend.
```

### Seguilo passo per passo

1. `toObservable(searchSignal)` espone le modifiche della query come un flusso RxJS.
2. `debounceTime(300)` attende una pausa di 300 ms; `switchMap` avvia la richiesta più recente e si disiscrive dal flusso precedente quando arriva un nuovo termine.
3. `toSignal(..., { initialValue: [] })` rende i risultati leggibili dal template fin da subito, prima della prima risposta.
4. Digita rapidamente due termini e poi fermati. La ricerca parte dopo la pausa; controlla inoltre errori HTTP e contesto d'iniezione prima di usare `toSignal`.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class SearchBridge {
    query = signal('');
    setQuery(text: string) { this.query.set(text); }
}
```

## Dove ci si confonde spesso

- Leggere il valore prima della prima emissione senza gestire `undefined` o fornire un valore iniziale
- creare una nuova sottoscrizione toSignal a ogni lettura.

## Domanda di verifica

> Quando è preferibile usare RxJS rispetto a un semplice Signal?
