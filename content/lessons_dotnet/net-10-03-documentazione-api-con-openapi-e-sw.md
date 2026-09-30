# Documentazione delle API con OpenAPI

OpenAPI descrive in modo leggibile da strumenti il contratto di un'API. In .NET 10 `AddOpenApi()` registra il generatore e `MapOpenApi()` espone il documento JSON; un'interfaccia web come Swagger UI o Scalar è un pacchetto aggiuntivo.

## Il progetto visto da chi deve usarlo

### Il documento JSON nasce dal contratto delle route
In `Server.csproj` aggiungi il generatore della stessa major di ASP.NET Core:
```powershell
dotnet add package Microsoft.AspNetCore.OpenApi --version 10.0.12
dotnet restore
```

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOpenApi();
var app = builder.Build();

app.MapGet("/api/health", () => TypedResults.Ok(new HealthResponse("Healthy")))
   .WithName("Health")
   .WithTags("Sistema")
   .WithSummary("Controlla che l'API sia disponibile");

if (app.Environment.IsDevelopment()) app.MapOpenApi();
app.Run();

public sealed record HealthResponse(string Status);
```

Il route restituisce un `TypedResults.Ok<HealthResponse>`: ASP.NET Core conosce il tipo e può descrivere la risposta `200` nello schema. `WithName`, `WithTags` e `WithSummary` aggiungono metadati leggibili. Avvia in Development e visita `/openapi/v1.json`: il browser mostra il contratto generato, non una prova che ogni risposta futura del server lo rispetti.

`AddOpenApi()` registra il generatore e `MapOpenApi()` rende raggiungibile il documento JSON. Per esplorarlo con una UI installa Swagger UI o Scalar separatamente: una UI legge il documento, non lo crea e non sostituisce i test degli endpoint. [Documentazione ufficiale ASP.NET Core](https://learn.microsoft.com/aspnet/core/fundamentals/openapi/overview?view=aspnetcore-10.0).

## Attraversa i file e i processi coinvolti

```text
app.MapGet("/api/health", () => TypedResults.Ok(new HealthResponse("Healthy")));
```

### Racconta l'operazione dal file al risultato

1. `AddOpenApi()` registra il servizio che genera il documento; `MapOpenApi()` pubblica il documento JSON, normalmente su `/openapi/v1.json`.
2. `WithTags` organizza gli endpoint e `WithSummary` aggiunge una descrizione leggibile a strumenti e persone.
3. L'interfaccia web come Swagger UI o Scalar è un pacchetto separato: il documento OpenAPI può esistere anche senza una UI interattiva.
4. Avvia l'API, apri il documento e verifica che rotta, metodo e risposta corrispondano al codice. Non inserire dati segreti nella documentazione pubblica.

Il runner formatta metadati testuali, non avvia il generatore. Nel server apri `/openapi/v1.json` e confronta schema e route effettive.

## Che cosa deve poter verificare un'altra persona?

- Non inserire descrizioni o status code attesi negli endpoint rendendo la documentazione poco utile per chi sviluppa il frontend.

> **Quale decisione puoi motivare con il codice?** Quali ruoli svolgono `AddOpenApi()` e `MapOpenApi()`, e perché l'interfaccia web è un elemento separato?
