# Route Guards funzionali: Proteggere le rotte con canActivate

Le Route Guards funzionali decidono se Angular può completare una navigazione e possono restituire un UrlTree di reindirizzamento. Sono un controllo del flusso UI: l'API deve applicare l'autorizzazione sul server.

## Lo stato che l'utente sta costruendo

### Creazione di una Route Guard Funzionale in Angular:
```typescript
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true; // Navigazione consentita!
  }

  // Reindirizza al login memorizzando l'URL a cui voleva accedere
  return router.createUrlTree(['/login'], { queryParams: { returnUrl: state.url } });
};
```

### Applicazione nella Rotta:
```typescript
{
  path: 'admin',
  loadComponent: () => import('./admin.component').then(m => m.AdminComponent),
  canActivate: [authGuard]
}
```

Il servizio usato dalla guard, in `auth.service.ts`, rappresenta qui soltanto lo stato locale della sessione:
```typescript
import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  readonly authenticated = signal(false);
  isAuthenticated(): boolean { return this.authenticated(); }
}
```
Il login aggiorna questo stato; la sua presenza non autorizza una richiesta sul server. La rotta lazy presume un file `admin.component.ts` che esporta `AdminComponent`: nel laboratorio trovi pagine e rotte già predisposte.

## Segui un campo o una navigazione

```typescript
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  return auth.isAuthenticated() ? true : inject(Router).createUrlTree(['/login']);
};
```

### Segui la persona mentre completa il flusso

1. La guard inietta il servizio di autenticazione e legge `isAuthenticated()` prima di consentire la navigazione.
2. Se la persona è autenticata, restituisce `true`; altrimenti crea un `UrlTree` per `/login`, così il Router esegue il reindirizzamento.
3. La guard migliora il flusso dell'interfaccia, ma non è un confine di sicurezza: il backend deve autorizzare ogni richiesta protetta.
4. Prova entrambi gli stati e aggiungi un ruolo richiesto. Poi invia direttamente una richiesta HTTP all'API per verificare che il server applichi la propria autorizzazione.

L'esercizio isola la decisione della guard e non configura il Router. Il laboratorio verifica la navigazione, mentre il backend deve autorizzare la risorsa.

## Rendi visibile lo stato che blocca il flusso

- Restituire un semplice `false` nella guard lasciando l'utente su una schermata vuota senza feedback, invece di reindirizzarlo a `/login` con un UrlTree.

> **Quale stato decide che cosa accade dopo?** Quale vantaggio offrono le guard funzionali (`CanActivateFn`) rispetto alle vecchie guard basate su classi e interfacce?
