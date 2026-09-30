# CORS, Same-Origin, XSS e CSRF: scopi distinti

CORS permette al browser di leggere risposte cross-origin quando l'API autorizza l'origine. Non è autenticazione né protezione CSRF: il server può ricevere ed eseguire una richiesta anche se il browser poi ne blocca la risposta.

## Il confine di fiducia della richiesta

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

## Segui identità, token e decisione del server

```csharp
builder.Services.AddCors(options => {
  options.AddPolicy("Dev48Policy", p => p.WithOrigins("http://localhost:4200").AllowAnyMethod().AllowAnyHeader());
});
```

### Verifica identità, permessi e risposta

1. `WithOrigins("http://localhost:4200")` dichiara quale origine browser può leggere la risposta; origine significa schema, host e porta.
2. Il browser può inviare una richiesta cross-origin e poi impedire a JavaScript di leggerne la risposta: CORS non autentica la persona né sostituisce le regole del server.
3. XSS riguarda l'esecuzione di contenuto ostile nel contesto della pagina; CSRF riguarda richieste indesiderate che sfruttano credenziali inviate automaticamente, come cookie.
4. Confronta token Bearer in header e cookie di sessione: cambia il rischio CSRF e la protezione necessaria. Non usare origini arbitrarie insieme a credenziali.

La funzione dell'esercizio confronta origini ammesse; solo il browser dimostra l'effetto CORS e solo il server applica autenticazione e autorizzazione.

## Quale parte può fidarsi di questo dato?

- Usare CORS come autenticazione o difesa CSRF
- confondere un blocco del browser con un endpoint non eseguito
- autorizzare origini arbitrarie per richieste con cookie.

> **Chi prende la decisione finale?** Che cosa blocca il browser quando la risposta non contiene i permessi CORS, e che cosa CORS non protegge?
