# CORS, Same-Origin, XSS e CSRF: scopi distinti

## In parole semplici

L'obiettivo di questa lezione è configurare una policy CORS precisa e distinguere CORS dai controlli anti-CSRF e dalla mitigazione XSS.

CORS permette al browser di leggere risposte cross-origin quando l'API autorizza l'origine. Non è autenticazione né protezione CSRF: il server può ricevere ed eseguire una richiesta anche se il browser poi ne blocca la risposta.

## Le parole da riconoscere

- `cors`
- `withorigins`
- `xss`
- `csrf`
- `samesite`
- `content security policy`
- `sanitizzazione`

## Anatomia e Sintassi del Codice

### Policy CORS per un client Angular:
```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(options => {
    options.AddPolicy("AllowAngularClient", policy => {
        policy.WithOrigins("http://localhost:4200", "https://academy.dev48.it")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Con endpoint routing, applica CORS prima dell'autorizzazione.
app.UseCors("AllowAngularClient");
```

Un header `Authorization` Bearer impostato da Angular richiede che CORS consenta l'header `Authorization`, ma non richiede `AllowCredentials()`. Quest'ultimo riguarda richieste con credenziali browser, per esempio cookie. In quel caso elenca origini esplicite e abilita anche la credenziale lato client.

CORS non sostituisce autenticazione, autorizzazione o difese CSRF. Per cookie usa anche una strategia anti-CSRF appropriata. Con credenziali non riflettere origini arbitrarie e non usare wildcard `*`.

## Un esempio concreto

```csharp
builder.Services.AddCors(options => {
  options.AddPolicy("Dev48Policy", p => p.WithOrigins("http://localhost:4200").AllowAnyMethod().AllowAnyHeader());
});
```

### Seguilo passo per passo

1. `WithOrigins("http://localhost:4200")` dichiara quale origine browser può leggere la risposta; origine significa schema, host e porta.
2. Il browser può inviare una richiesta cross-origin e poi impedire a JavaScript di leggerne la risposta: CORS non autentica la persona né sostituisce le regole del server.
3. XSS riguarda l'esecuzione di contenuto ostile nel contesto della pagina; CSRF riguarda richieste indesiderate che sfruttano credenziali inviate automaticamente, come cookie.
4. Confronta token Bearer in header e cookie di sessione: cambia il rischio CSRF e la protezione necessaria. Non usare origini arbitrarie insieme a credenziali.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Usare CORS come autenticazione o difesa CSRF
- confondere un blocco del browser con un endpoint non eseguito
- autorizzare origini arbitrarie per richieste con cookie.

## Domanda di verifica

> Che cosa blocca il browser quando la risposta non contiene i permessi CORS, e che cosa CORS non protegge?
