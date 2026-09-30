# Minimal API da zero: Program.cs e WebApplication

Un endpoint è una funzione che ASP.NET Core invoca quando una richiesta corrisponde a una rotta. Prima di aggiungere database, servizi o autenticazione, seguiamo una risposta completa e piccola: una GET che restituisce una stringa.

### Nel percorso

Da conoscere: [Il primo metodo C#: parametri, variabili e valore restituito](net-00-01-il-primo-metodo-c-parametri-variabi.md); [Anatomia di una soluzione Full-Stack Client-Server](net-00-02-anatomia-di-una-soluzione-full-stac.md).

Crea un progetto con `dotnet new web -n FirstApi`, entra con `cd FirstApi` e sostituisci `Program.cs` con l'esempio. Avvia con `dotnet run --urls http://localhost:5000`, poi apri `http://localhost:5000/hello`. Il terminale resta occupato dal server; usa una seconda finestra per le richieste e Ctrl+C per fermarlo. Il laboratorio Web API con Minimal API e DTO estenderà questa risposta a operazioni CRUD.

## Prima di avviare il server

### `Program.cs`, prima della prima richiesta
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/hello", () => "Hello");

app.Run();
```

`CreateBuilder` prepara configurazione, logging e raccolta dei servizi. Qui non registriamo servizi perché l'endpoint non ne richiede. `Build` costruisce l'applicazione con le registrazioni e le route dichiarate fino a quel punto. `MapGet` associa metodo e percorso a un handler, ma non esegue ancora il corpo della lambda. `Run` avvia l'host e resta in ascolto: l'handler viene invocato più tardi, per ogni richiesta GET che corrisponde a `/hello`.

Quando la route deve restituire un codice e un corpo JSON, l'helper rende esplicita la risposta:
```csharp
app.MapGet("/api/health", () => TypedResults.Ok(new { status = "Healthy" }));
```
`TypedResults.Ok` restituisce un risultato concreto con metadati utili anche a OpenAPI. `Results.Ok` è comodo quando un handler restituisce rami diversi che condividono `IResult`; con `TypedResults` i tipi dei rami vanno dichiarati, per esempio con `Results<Ok<T>, NotFound>`. Nessuna delle due forme è necessaria per restituire direttamente un oggetto serializzabile.

In una Minimal API, `Program.cs` può iniziare come file unico. Quando endpoint, regole e accesso ai dati crescono, sposta responsabilità in servizi e file separati senza cambiare il ciclo HTTP.

## La richiesta incontra un handler

```text
app.MapGet("/hello", () => "Hello");
```

### Segui la richiesta con valori concreti

1. Avvia il progetto con `dotnet run`; il processo resta in ascolto sull'indirizzo indicato dal terminale.
2. In un secondo terminale invia `GET /hello`. Il routing confronta metodo e percorso con la route registrata.
3. Solo adesso ASP.NET Core chiama la lambda. Il valore `Hello` diventa una risposta HTTP, normalmente con status `200` e contenuto testuale.
4. Prova `GET /other` e poi `POST /hello`: nessuna delle due richieste corrisponde alla route, quindi l'handler non viene chiamato.

La pratica breve controlla la logica helper; il laboratorio invece avvia il server, invia richieste HTTP e verifica body e status code delle operazioni CRUD.

## Confronta metodo e percorso

- Confondere la registrazione dei servizi (`builder.Services`) con la configurazione della pipeline (`app.Use...`)
- pensare che Minimal API o TypedResults siano obbligatori per ogni progetto.

> **Che cosa viene registrato e che cosa viene eseguito?** Quali criteri, oltre alla quantità di codice, useresti per scegliere tra Minimal API e Controller?
