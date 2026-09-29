# Progetto Angular Standalone e Bootstrap applicazione

## In parole semplici

L'obiettivo di questa lezione è avviare un'applicazione Angular moderna senza NgModule usando bootstrapApplication.

Nei nuovi progetti Angular i componenti standalone sono il modello predefinito e dichiarano direttamente le dipendenze del template. NgModule resta supportato: standalone evita di doverlo usare in molti casi, ma non lo elimina dal framework.

### Nel percorso

Da conoscere: [TypeScript di base: variabili, funzioni e array](net-00-02-typescript-di-base-variabili-funzio.md); [HTML essenziale e CSS per leggere i template Angular](net-00-03-html-essenziale-e-css-per-leggere-i.md); [Introduzione a signal() e aggiornamento stato con set() e update()](net-05-01-introduzione-a-signal-e-aggiornamen.md); [Valori derivati intelligenti con computed()](net-05-02-valori-derivati-intelligenti-con-co.md).

Le basi di `signal()` e `computed()` precedono questa lezione: nei componenti useremo subito valori reattivi. Ripassale dai richiami qui sotto se necessario. Nel laboratorio Catalogo Standalone con Control Flow i file sono `src/main.ts`, `src/app/app.ts` e `src/app/app.config.ts`; gli esempi con `AppComponent` usano un nome illustrativo, da adattare all'export del tuo file.

## Le parole da riconoscere

- `standalone`
- `bootstrapapplication`
- `main.ts`
- `appconfig`
- `providehttpclient`
- `provide-router`

## Anatomia e Sintassi del Codice

### Bootstrap di un'applicazione Standalone (in `main.ts`):
```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));
```

### Configurazione Servizi Globali (in `app.config.ts`):
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient()
  ]
};
```

## Un esempio concreto

```typescript
bootstrapApplication(AppComponent, {
  providers: [provideHttpClient(), provideRouter(routes)]
});
```

### Seguilo passo per passo

1. `bootstrapApplication(AppComponent, ...)` crea la radice Angular senza richiedere un modulo applicativo.
2. L'array `providers` registra servizi disponibili nell'app: `provideHttpClient()` configura `HttpClient` e `provideRouter(routes)` configura le rotte.
3. `main.ts` passa il componente radice e i provider; l'HTML iniziale deve contenere il selettore del componente, spesso `<app-root>`.
4. Togli un provider alla volta e individua l'errore che compare quando il componente tenta di usare quel servizio. Ripristinalo prima di proseguire.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class AppBootstrapStatus {
    isReady = signal(false);
    init() { this.isReady.set(true); }
}
```

## Dove ci si confonde spesso

- Cercare di dichiarare un componente Standalone dentro le `declarations` di un NgModule
- dimenticare `provideHttpClient()` nel bootstrap.

## Domanda di verifica

> Quale responsabilità dichiara un componente standalone nel proprio decoratore `@Component`?
