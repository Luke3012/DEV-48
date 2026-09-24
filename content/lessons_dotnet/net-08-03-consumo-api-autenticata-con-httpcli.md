# Consumo API autenticata con HttpClient e HttpInterceptor

## In parole semplici

L'obiettivo di questa lezione è inviare automaticamente il token Bearer in tutte le chiamate HTTP con un HttpInterceptorFn di Angular.

Un HttpInterceptor può aggiungere `Authorization: Bearer <token>` alle richieste verso la propria API. Limitare l'interceptor all'origine attesa evita di inviare il token a server di terze parti. Il servizio d'esempio lo conserva solo in memoria: un ricaricamento lo elimina; non spostarlo in `localStorage` come scorciatoia per renderlo persistente.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `httpclient`
- `httpinterceptorfn`
- `bearer token`
- `authorization header`
- `req.clone`
- `withinterceptors`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`httpclient`, `httpinterceptorfn`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Creazione di un HttpInterceptor Funzionale in Angular:
```typescript
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  const apiOrigin = 'https://localhost:5001';
  const requestOrigin = new URL(req.url, apiOrigin).origin;
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

### Registrazione in `app.config.ts`:
```typescript
provideHttpClient(withInterceptors([authInterceptor]))
```

### Che cosa significa “in memoria”
Il campo privato di `TokenStorageService` vive finché l'applicazione resta caricata; un aggiornamento della pagina lo azzera. È una scelta esplicita per l'esercizio, non un sistema completo di sessione. `localStorage` e `sessionStorage` espongono i token agli script eseguiti nella pagina: per applicazioni reali segui un flusso OAuth/OIDC e la guida di sicurezza ASP.NET Core, scegliendo il modello adatto alla tua architettura.

Riferimento: [Configure JWT bearer authentication in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-10.0).

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class TokenStorageService {
    private token: string | null = null;
    setToken(t: string) { this.token = t; }
    getToken(): string | null { return this.token; }
    hasToken(): boolean { return Boolean(this.token); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Modificare direttamente l'oggetto `HttpRequest`
- aggiungere il token a URL esterni alla propria API
- trattare una guard Angular come controllo di autorizzazione lato server
- usare `localStorage` come soluzione automatica per mantenere un token.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché un interceptor dovrebbe aggiungere il Bearer token solo alle richieste dirette all'API prevista?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
