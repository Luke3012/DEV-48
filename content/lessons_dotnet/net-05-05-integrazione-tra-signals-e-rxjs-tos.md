# Integrazione tra Signals e RxJS: toSignal e toObservable

Un Signal risponde bene alla domanda «qual è il valore corrente?». Un Observable descrive valori che possono arrivare nel tempo e compone attese, cancellazioni e trasformazioni. Una ricerca remota mostra perché servono entrambi: l'input è stato corrente, mentre le risposte HTTP formano un flusso asincrono.

### Nel percorso

Approfondimento facoltativo: puoi riprenderlo dopo aver completato la pratica essenziale del modulo.

Da conoscere: [Valori derivati intelligenti con computed()](net-05-02-valori-derivati-intelligenti-con-co.md); [Effetti collaterali controllati con effect()](net-05-03-effetti-collaterali-controllati-con.md).

Un Observable descrive emissioni nel tempo; `subscribe` avvia l'ascolto e `unsubscribe` lo interrompe. `pipe` compone operatori; `switchMap` sostituisce l'ascolto della richiesta precedente. Le richieste HttpClient partono alla sottoscrizione. `toSignal` e `toObservable` vanno creati in un contesto di iniezione, per esempio nei campi di un componente. La conversione è utile per ricerca remota e flussi asincroni; per un totale locale basta `computed`.

## Il valore corrente e gli eventi che arrivano nel tempo

### Sposta la responsabilità quando i dati arrivano dalla rete
Un contratto piccolo può vivere in `user.model.ts` ed essere riusato dai due file che seguono:
```typescript
export type User = { id: number; name: string };
```

All'inizio una lista locale basta per disegnare il template:
```typescript
import { Component, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import type { User } from './user.model';

@Component({ selector: 'app-user-search', template: '' })
export class UserSearchComponent {
  readonly users = signal<User[]>([{ id: 1, name: 'Anna' }]);
  private readonly http = inject(HttpClient);

  load(): void {
    this.http.get<User[]>('/api/users').subscribe(users => this.users.set(users));
  }
}
```
Il flusso è valido, ma il componente ora conosce URL, trasporto e aggiornamento dei dati. Un service possiede la responsabilità HTTP; il componente resta interessato al valore e a ciò che mostra. `provideHttpClient()` deve essere registrato in `app.config.ts`, altrimenti l'iniezione fallisce con `NullInjectorError`.

### La richiesta HTTP vive in un service
```typescript
// user.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { User } from './user.model';

@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly http = inject(HttpClient);

  search(query: string): Observable<User[]> {
    return this.http.get<User[]>('/api/users', { params: { q: query } });
  }
}
```

### Nel componente: valore corrente e flusso delle risposte
```typescript
// user-search.component.ts
import { Component, inject, signal } from '@angular/core';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { catchError, debounceTime, distinctUntilChanged, map, of, startWith, switchMap } from 'rxjs';
import { UserService } from './user.service';
import type { User } from './user.model';

type SearchState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; users: User[] }
  | { status: 'error'; message: string };

@Component({
  selector: 'app-user-search',
  template: `
    <label>Utente <input #search (input)="setQuery(search.value)" /></label>
    @let current = state();
    @switch (current.status) {
      @case ('loading') { <p role="status">Ricerca in corso…</p> }
      @case ('error') { <p role="alert">{{ current.message }}</p> }
      @case ('success') {
        <ul>
          @for (user of current.users; track user.id) { <li>{{ user.name }}</li> }
          @empty { <li>Nessun utente trovato.</li> }
        </ul>
      }
      @default { <p>Inserisci un nome per iniziare.</p> }
    }
  `
})
export class UserSearchComponent {
  private readonly users = inject(UserService);
  readonly query = signal('');
  readonly state = toSignal(
    toObservable(this.query).pipe(
      debounceTime(250),
      distinctUntilChanged(),
      switchMap(query => query.trim()
        ? this.users.search(query).pipe(
            map(users => ({ status: 'success', users }) as const),
            startWith({ status: 'loading' } as const),
            catchError(() => of({ status: 'error', message: 'Ricerca non disponibile' } as const))
          )
        : of({ status: 'idle' } as const)
      )
    ),
    { initialValue: { status: 'idle' } as SearchState }
  );

  setQuery(query: string): void {
    this.query.set(query);
  }
}
```

`HttpClient` è fornito in `app.config.ts` con `provideHttpClient()`. Il componente dipende da `UserService`, che usa `HttpClient`: la UI non costruisce la richiesta né conosce i dettagli del backend. Il tipo `<User[]>` documenta il JSON atteso, ma non valida a runtime il contenuto ricevuto. `toSignal` sottoscrive nel contesto di iniezione e offre lo stato corrente al template; `switchMap` abbandona la richiesta precedente quando cambia la query. Gli Observable di `HttpClient` sono freddi: la richiesta parte quando qualcuno si sottoscrive.

## Dalla digitazione alla risposta JSON

```text
toObservable(this.query).pipe(
  debounceTime(250),
  switchMap(query => this.users.search(query))
)
```

### Segui la modifica fino alla vista

1. La persona digita e `query.set(...)` aggiorna lo stato sorgente. `toObservable` rende le variazioni disponibili al flusso RxJS.
2. `debounceTime(250)` attende una pausa; `distinctUntilChanged` elimina query consecutive uguali.
3. `switchMap` chiama il service. Il service usa `HttpClient` per `GET /api/users?q=...`; l'Observable HTTP invia la richiesta quando viene sottoscritto.
4. La risposta JSON diventa `User[]`, poi uno stato `success` leggibile come `state()` nel template. Nel frattempo appare `loading`; se la richiesta fallisce, il flusso emette `error` senza confonderlo con una lista vuota.

Il mini-runner controlla una trasformazione TypeScript e non avvia HTTP. Nel laboratorio Monorepo verifica il confine reale tra service, backend e template; nel laboratorio JWT osserva invece come l'interceptor modifica la richiesta in uscita e lascia risalire la risposta.

## Distingui attesa, risultato vuoto ed errore

- Leggere il valore prima della prima emissione senza gestire `undefined` o fornire un valore iniziale
- creare una nuova sottoscrizione toSignal a ogni lettura.

> **Quale valore c'è ora e quale arriverà dopo?** Quando è preferibile usare RxJS rispetto a un semplice Signal?
