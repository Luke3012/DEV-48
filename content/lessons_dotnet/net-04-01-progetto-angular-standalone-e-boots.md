# Progetto Angular Standalone e Bootstrap applicazione

Angular non parte da un componente trovato per caso: una catena di file indica al browser quale elemento ospita l'app, quale componente è la radice e quali servizi sono disponibili quando i componenti vengono creati.

### Nel percorso

Da conoscere: [TypeScript di base: variabili, funzioni e array](net-00-02-typescript-di-base-variabili-funzio.md); [HTML essenziale e CSS per leggere i template Angular](net-00-03-html-essenziale-e-css-per-leggere-i.md); [Introduzione a signal() e aggiornamento stato con set() e update()](net-05-01-introduzione-a-signal-e-aggiornamen.md); [Valori derivati intelligenti con computed()](net-05-02-valori-derivati-intelligenti-con-co.md).

Le basi di `signal()` e `computed()` precedono questa lezione: nei componenti useremo subito valori reattivi. Ripassale dai richiami qui sotto se necessario. Nel laboratorio Catalogo Standalone con Control Flow ritroverai `src/index.html`, `src/main.ts`, `src/app/app.ts` e `src/app/app.config.ts`; qui usiamo gli stessi nomi ed export dello starter.

## La vista che vogliamo costruire

### Dall'HTML al componente radice
Nel progetto generato dal laboratorio, i file essenziali sono `src/index.html`, `src/main.ts`, `src/app/app.ts`, `src/app/app.config.ts` e `src/app/app.routes.ts`.

`src/index.html` fornisce l'elemento host:
```html
<body><app-root></app-root></body>
```

`src/main.ts` avvia il componente esportato da `app.ts` e gli passa la configurazione:
```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { appConfig } from './app/app.config';

bootstrapApplication(App, appConfig).catch(error => console.error(error));
```

`src/app/app.ts` collega la classe al selettore presente nell'HTML:
```typescript
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  template: '<h1>Catalogo</h1><router-outlet />',
  styleUrl: './app.css'
})
export class App {}
```

`src/app/app.config.ts` registra i servizi applicativi:
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes), provideHttpClient()]
};
```

Un provider configura il contenitore d'iniezione: `provideRouter` rende disponibile il Router con queste route; `provideHttpClient` rende iniettabile `HttpClient`. Togli il secondo e un servizio che lo richiede può fallire con `NullInjectorError`. `imports` del componente, invece, rende direttive o componenti disponibili nel suo template: provider e template import non sono la stessa cosa. Nei nuovi componenti `standalone` è il default; `NgModule` resta supportato per codice esistente.

## Segui il dato fino al DOM

```typescript
bootstrapApplication(App, appConfig).catch(error => console.error(error));
```

### Dal modello alla schermata

1. Il browser legge `index.html` e crea `<app-root>`; il bundler esegue il file d'ingresso `main.ts`.
2. `bootstrapApplication(App, appConfig)` crea l'injector applicativo con i provider e istanzia `App` sull'elemento `app-root`.
3. Angular compila il template della radice e inserisce `router-outlet`; il Router vi mostra il componente associato all'URL corrente.
4. Rimuovi `provideHttpClient()` e segui l'errore dal componente che usa `HttpClient` all'injector. Ripristinalo e controlla che la richiesta parta; se rimuovi `RouterOutlet` da `imports`, il compilatore segnala che il template non riconosce quell'elemento.

Il laboratorio Standalone usa proprio `main.ts`, `app.ts` e `app.config.ts`. Prova la pagina nel browser: la pratica breve non avvia Angular e quindi non può dimostrare il bootstrap o il rendering.

## Che cosa deve conoscere il template?

- Cercare di dichiarare un componente Standalone dentro le `declarations` di un NgModule
- dimenticare `provideHttpClient()` nel bootstrap.

> **Che cosa collega classe e vista?** Quale responsabilità dichiara un componente standalone nel proprio decoratore `@Component`?
