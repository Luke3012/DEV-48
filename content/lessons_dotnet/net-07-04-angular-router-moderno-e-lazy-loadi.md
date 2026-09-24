# Angular Router moderno e Lazy Loading

## In parole semplici

L'obiettivo di questa lezione è configurare la navigazione a pagina singola (SPA) caricando moduli e componenti su richiesta.

L'Angular Router associa gli URL del browser ai componenti dell'applicazione, caricando il codice dei componenti solo quando l'utente visita la relativa pagina (Lazy Loading con loadComponent).

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `router`
- `routes`
- `loadcomponent`
- `router-outlet`
- `routerlink`
- `parametri rotta`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`router`, `routes`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class RouteMatcher {
    isMatch(pattern: string, url: string): boolean {
        return pattern.replace(/:\w+/g, '[^/]+') === url;
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare `href` standard sui link invece di `routerLink` (provoca il ricaricamento completo dell'applicazione e perdita dello stato in memoria).

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è il vantaggio di usare `loadComponent: () => import(...)` rispetto a importare direttamente la classe del componente nelle rotte?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
