# Documentazione delle API con OpenAPI

## In parole semplici

L'obiettivo di questa lezione è esporre un documento OpenAPI generato da ASP.NET Core e aggiungere metadati alle rotte.

OpenAPI descrive in modo leggibile da strumenti il contratto di un'API. In .NET 10 `AddOpenApi()` registra il generatore e `MapOpenApi()` espone il documento JSON; un'interfaccia web come Swagger UI o Scalar è un pacchetto aggiuntivo.

## Le parole da riconoscere

- `openapi`
- `documento json`
- `addopenapi`
- `mapopenapi`
- `documentazione api`
- `route metadata`

## Anatomia e Sintassi del Codice

### Generare il documento OpenAPI in una Minimal API .NET 10:
Nel progetto aggiungi il pacchetto di generazione:
```powershell
dotnet add package Microsoft.AspNetCore.OpenApi --version 10.0.12
```

```csharp
builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment()) {
    app.MapOpenApi(); // In .NET 10 espone /openapi/v1.json
}
```

Gli endpoint possono essere arricchiti con nome, descrizione e tag:
```csharp
app.MapGet("/api/users", () => Results.Ok(new[] { "Ada", "Luca" }))
   .WithName("ListUsers")
   .WithTags("Utenti")
   .WithSummary("Restituisce l'elenco di tutti gli utenti registrati");
```

Per provare il documento con un'interfaccia web, scegli e installa una UI separata. La UI legge lo stesso documento OpenAPI e non sostituisce i test degli endpoint.

## Un esempio concreto

```csharp
app.MapGet("/api/items", () => Results.Ok())
   .WithTags("Catalogo")
   .WithSummary("Recupera tutti gli articoli");
```

### Seguilo passo per passo

1. `AddOpenApi()` registra il servizio che genera il documento; `MapOpenApi()` pubblica il documento JSON, normalmente su `/openapi/v1.json`.
2. `WithTags` organizza gli endpoint e `WithSummary` aggiunge una descrizione leggibile a strumenti e persone.
3. L'interfaccia web come Swagger UI o Scalar è un pacchetto separato: il documento OpenAPI può esistere anche senza una UI interattiva.
4. Avvia l'API, apri il documento e verifica che rotta, metodo e risposta corrispondano al codice. Non inserire dati segreti nella documentazione pubblica.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Non inserire descrizioni o status code attesi negli endpoint rendendo la documentazione poco utile per chi sviluppa il frontend.

## Domanda di verifica

> Quali ruoli svolgono `AddOpenApi()` e `MapOpenApi()`, e perché l'interfaccia web è un elemento separato?
