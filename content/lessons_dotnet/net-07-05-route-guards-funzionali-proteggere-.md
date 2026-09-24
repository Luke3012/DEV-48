# Route Guards funzionali: Proteggere le rotte con canActivate

## In parole semplici

L'obiettivo di questa lezione è bloccare accessi non autorizzati a pagine sensibili con funzioni canActivateFn.

Le Route Guards funzionali decidono se Angular può completare una navigazione e possono restituire un UrlTree di reindirizzamento. Sono un controllo del flusso UI: l'API deve applicare l'autorizzazione sul server.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `route guard`
- `canactivatefn`
- `inject`
- `router`
- `autenticazione`
- `protezione rotte`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`route guard`, `canactivatefn`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```typescript
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  return auth.isLoggedIn() ? true : inject(Router).createUrlTree(['/login']);
};
```

### Seguilo passo per passo

1. La guard inietta il servizio di autenticazione e legge `isLoggedIn()` prima di consentire la navigazione.
2. Se la persona è autenticata, restituisce `true`; altrimenti crea un `UrlTree` per `/login`, così il Router esegue il reindirizzamento.
3. La guard migliora il flusso dell'interfaccia, ma non è un confine di sicurezza: il backend deve autorizzare ogni richiesta protetta.
4. Prova entrambi gli stati e aggiungi un ruolo richiesto. Poi invia direttamente una richiesta HTTP all'API per verificare che il server applichi la propria autorizzazione.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class GuardSimulator {
    checkAccess(isAuthenticated: boolean, requiredRole?: string, userRole?: string): boolean {
        if (!isAuthenticated) return false;
        if (!requiredRole) return true;
        return userRole === requiredRole;
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Restituire un semplice `false` nella guard lasciando l'utente su una schermata vuota senza feedback, invece di reindirizzarlo a `/login` con un UrlTree.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quale vantaggio offrono le guard funzionali (`CanActivateFn`) rispetto alle vecchie guard basate su classi e interfacce?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
