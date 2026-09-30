# Angular Router moderno e Lazy Loading

In una SPA, l'indirizzo del browser cambia senza ricaricare tutta la pagina. Il Router confronta l'URL con una route, crea il componente corrispondente e lo inserisce nel punto `router-outlet` dichiarato dal layout.

## Lo stato che l'utente sta costruendo

### URL, route e componente
```text
URL browser: /users/42?tab=measures
        ↓ provideRouter(routes)
match: path users/:id, parametro id = 42
        ↓ loadComponent()
UserDetailComponent
        ↓
<router-outlet> nel componente radice
```

```typescript
// src/app/app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'users', pathMatch: 'full' },
  {
    path: 'users/:id',
    loadComponent: () => import('./user-detail.component').then(m => m.UserDetailComponent)
  },
  { path: '**', loadComponent: () => import('./not-found.component').then(m => m.NotFoundComponent) }
];
```

Nel layout importa `RouterOutlet` e `RouterLink`; `provideRouter(routes)` va registrato nei provider applicativi. Il `:id` identifica la risorsa nel percorso; `tab=measures` è query string e può rappresentare un filtro o una scheda. `routerLink` naviga senza ricaricare il documento. `loadComponent` ritarda il caricamento del componente quando la route viene richiesta.

Una route guard può fermare o reindirizzare la navigazione locale; non sostituisce l'autorizzazione dell'API. La rotta wildcard si mette dopo le rotte più specifiche per fungere da pagina non trovata.

## Segui un campo o una navigazione

```typescript
{ path: 'users/:id', loadComponent: () => import('./user-detail.component').then(m => m.UserDetailComponent) }
```

### Segui la persona mentre completa il flusso

1. L'URL `/users/42?tab=measures` rimane nella barra del browser mentre il Router prova le route configurate.
2. `users/:id` corrisponde al percorso e fornisce `id = 42`; la query `tab` è un dato facoltativo distinto dal path.
3. Il Router carica il file `user-detail.component.ts` quando serve, crea `UserDetailComponent` e lo inserisce nel `router-outlet`.
4. Naviga a `/users/99` con `routerLink` e poi cambia `tab` con `router.navigate`. L'app aggiorna la vista senza ricaricare l'intero documento.

La funzione breve costruisce un URL di dettaglio. Nel laboratorio Router verifica configurazione, outlet, route lazy e navigazione anonima/autorizzata; la lezione successiva spiega la guard e i suoi limiti.

## Rendi visibile lo stato che blocca il flusso

- Usare `href` standard sui link invece di `routerLink` (provoca il ricaricamento completo dell'applicazione e perdita dello stato in memoria).

> **Quale stato decide che cosa accade dopo?** Qual è il vantaggio di usare `loadComponent: () => import(...)` rispetto a importare direttamente la classe del componente nelle rotte?
