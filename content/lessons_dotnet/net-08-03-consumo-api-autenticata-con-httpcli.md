# Consumo API autenticata con HttpClient e HttpInterceptor

## In parole semplici

L'obiettivo di questa lezione è inviare il token Bearer nelle chiamate dirette alla propria API con un HttpInterceptorFn di Angular.

Un HttpInterceptor può aggiungere `Authorization: Bearer <token>` alle richieste verso la propria API. Limitare l'interceptor all'origine attesa evita di inviare il token a server di terze parti. Il servizio d'esempio lo conserva solo in memoria: un ricaricamento lo elimina; non spostarlo in `localStorage` come scorciatoia per renderlo persistente.

### Nel percorso

Da conoscere: [Generazione e convalida token JWT in ASP.NET Core](net-08-02-generazione-e-convalida-token-jwt-i.md); [Interfacce vs Type Alias e Contratti di Dati](net-02-02-interfacce-vs-type-alias-e-contratt.md).

Prima dell'interceptor serve una richiesta reale: `provideHttpClient()` registra il servizio, `inject(HttpClient)` lo ottiene e `http.get<Profile>(url).subscribe(...)` avvia la GET. Il tipo `Profile` descrive il risultato atteso ma non valida il JSON ricevuto. Nel laboratorio Autenticazione JWT Full-Stack collegherai la sessione all'header; nel Gestionale Full-Stack Monorepo seguirai il caricamento dei dati.

## Le parole da riconoscere

- `httpclient`
- `httpinterceptorfn`
- `bearer token`
- `authorization header`
- `req.clone`
- `withinterceptors`

## Anatomia e Sintassi del Codice

### Creazione di un HttpInterceptor Funzionale in Angular:
```typescript
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { SessionService } from './session.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(SessionService).token();

  const apiOrigin = 'https://localhost:5001';
  const requestOrigin = new URL(req.url, inject(DOCUMENT).baseURI).origin;
  if (token && requestOrigin === apiOrigin) {
    // La richiesta HTTP è immutabile: va clonata aggiungendo gli headers!
    const clonedReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next(clonedReq);
  }

    return next(req);
};
```

### Servizio della sessione in `session.service.ts`:
```typescript
import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SessionService {
  readonly token = signal<string | null>(null);
}
```
Dopo il login imposta `session.token.set(response.token)`. Un URL relativo è risolto rispetto alla pagina, non all'origine API: se client e server usano porte diverse, passa l'URL assoluto dell'API oppure configura un proxy di sviluppo.

### Registrazione in `app.config.ts`:
```typescript
provideHttpClient(withInterceptors([authInterceptor]))
```

### Che cosa significa “in memoria”
Il campo privato di `TokenStorageService` vive finché l'applicazione resta caricata; un aggiornamento della pagina lo azzera. È una scelta esplicita per l'esercizio, non un sistema completo di sessione. `localStorage` e `sessionStorage` espongono i token agli script eseguiti nella pagina: per applicazioni reali segui un flusso OAuth/OIDC e la guida di sicurezza ASP.NET Core, scegliendo il modello adatto alla tua architettura.

Riferimento: [Configure JWT bearer authentication in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-10.0).

## Un esempio concreto

```text
const cloned = req.clone({
  setHeaders: { Authorization: `Bearer ${token}` }
});
return next(cloned);
```

### Seguilo passo per passo

1. L'interceptor legge il token dal servizio in memoria e controlla l'origine della richiesta prima di modificarla.
2. `req.clone({ setHeaders: ... })` crea una nuova richiesta con `Authorization: Bearer ...`; `HttpRequest` è immutabile.
3. Per l'API configurata, `next(cloned)` inoltra la richiesta autenticata. Per un'origine diversa o un token assente, il codice inoltra la richiesta originale.
4. Prova la chiamata alla tua API e una chiamata a un host esterno. Verifica che il token compaia solo nella prima; ricarica la pagina per osservare che questo esercizio in memoria non persiste e non copiarlo in `localStorage` senza valutare il modello di sicurezza.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Modificare direttamente l'oggetto `HttpRequest`
- aggiungere il token a URL esterni alla propria API
- trattare una guard Angular come controllo di autorizzazione lato server
- usare `localStorage` come soluzione automatica per mantenere un token.

## Domanda di verifica

> Perché un interceptor dovrebbe aggiungere il Bearer token solo alle richieste dirette all'API prevista?
