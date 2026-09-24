# CORS, Same-Origin, XSS e CSRF: scopi distinti

## In parole semplici

L'obiettivo di questa lezione è configurare una policy CORS precisa e distinguere CORS dai controlli anti-CSRF e dalla mitigazione XSS.

CORS permette al browser di leggere risposte cross-origin quando l'API autorizza l'origine. Non è autenticazione né protezione CSRF: il server può ricevere ed eseguire una richiesta anche se il browser poi ne blocca la risposta.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `cors`
- `withorigins`
- `xss`
- `csrf`
- `samesite`
- `content security policy`
- `sanitizzazione`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`cors`, `withorigins`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class CorsSecurityHelper {
    public static bool IsOriginAllowed(string origin, string[] allowedOrigins) {
        return System.Array.Exists(allowedOrigins, o => string.Equals(o, origin?.Trim(), System.StringComparison.OrdinalIgnoreCase));
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare CORS come autenticazione o difesa CSRF
- confondere un blocco del browser con un endpoint non eseguito
- autorizzare origini arbitrarie per richieste con cookie.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Che cosa blocca il browser quando la risposta non contiene i permessi CORS, e che cosa CORS non protegge?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
