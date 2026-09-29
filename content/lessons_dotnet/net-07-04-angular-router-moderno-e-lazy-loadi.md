# Angular Router moderno e Lazy Loading

## In parole semplici

L'obiettivo di questa lezione è configurare la navigazione a pagina singola (SPA) caricando moduli e componenti su richiesta.

L'Angular Router associa gli URL del browser ai componenti dell'applicazione, caricando il codice dei componenti solo quando l'utente visita la relativa pagina (Lazy Loading con loadComponent).

## Le parole da riconoscere

- `router`
- `routes`
- `loadcomponent`
- `router-outlet`
- `routerlink`
- `parametri rotta`

## Anatomia e Sintassi del Codice

### Configurazione Rotte con Lazy Loading in `app.routes.ts`:
```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'users/:id',
    loadComponent: () => import('./features/user-detail.component').then(m => m.UserDetailComponent)
  },
  { path: '**', redirectTo: 'dashboard' } // Wildcard per 404
];
```

### Nel Template:
- `<router-outlet />`: punto di montaggio in cui viene renderizzato il componente della rotta attiva.
- `<a routerLink="/dashboard" routerLinkActive="active">`: navigazione SPA senza ricaricare la pagina.

## Un esempio concreto

```typescript
export const routes: Routes = [
  { path: 'catalog', loadComponent: () => import('./catalog').then(m => m.CatalogComponent) }
];
```

### Seguilo passo per passo

1. La route associa il percorso `catalog` a una funzione che importa il file del componente solo quando la navigazione lo richiede.
2. `then(m => m.CatalogComponent)` seleziona l'export da mostrare; il componente deve comparire in un `<router-outlet>` presente nell'app.
3. Visitando `/catalog`, il Router carica il componente e mantiene la navigazione nella SPA. Un `routerLink` evita il ricaricamento completo della pagina.
4. Prova un percorso inesistente e aggiungi una route di fallback. Poi osserva nel Network quando viene scaricato il chunk del catalogo.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Usare `href` standard sui link invece di `routerLink` (provoca il ricaricamento completo dell'applicazione e perdita dello stato in memoria).

## Domanda di verifica

> Qual è il vantaggio di usare `loadComponent: () => import(...)` rispetto a importare direttamente la classe del componente nelle rotte?
