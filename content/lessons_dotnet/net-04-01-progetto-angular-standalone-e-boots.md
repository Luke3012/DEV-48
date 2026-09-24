# Progetto Angular Standalone e Bootstrap applicazione

## In parole semplici

L'obiettivo di questa lezione è avviare un'applicazione Angular moderna senza NgModule usando bootstrapApplication.

Nei nuovi progetti Angular i componenti standalone sono il modello predefinito e dichiarano direttamente le dipendenze del template. NgModule resta supportato: standalone evita di doverlo usare in molti casi, ma non lo elimina dal framework.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `standalone`
- `bootstrapapplication`
- `main.ts`
- `appconfig`
- `providehttpclient`
- `provide-router`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`standalone`, `bootstrapapplication`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class AppBootstrapStatus {
    isReady = signal(false);
    init() { this.isReady.set(true); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Cercare di dichiarare un componente Standalone dentro le `declarations` di un NgModule
- dimenticare `provideHttpClient()` nel bootstrap.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quale responsabilità dichiara un componente standalone nel proprio decoratore `@Component`?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
