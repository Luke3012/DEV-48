# Minimal API da zero: Program.cs e WebApplication

## In parole semplici

L'obiettivo di questa lezione è creare endpoint RESTful con Minimal API in C# e .NET 10.

Minimal API permette di dichiarare endpoint HTTP con poco codice di contorno. Controller e Minimal API sono entrambi adatti a progetti reali; la sintassi scelta, da sola, non determina il throughput dell'applicazione.

### Nel percorso

Da conoscere: [Il primo metodo C#: parametri, variabili e valore restituito](net-00-01-il-primo-metodo-c-parametri-variabi.md); [Anatomia di una soluzione Full-Stack Client-Server](net-00-02-anatomia-di-una-soluzione-full-stac.md).

Crea un progetto con `dotnet new web -n FirstApi`, entra con `cd FirstApi` e sostituisci `Program.cs` con l'esempio. Avvia con `dotnet run --urls http://localhost:5000`, poi apri `http://localhost:5000/api/hello`. Il terminale resta occupato dal server; usa una seconda finestra per le richieste e Ctrl+C per fermarlo. Il laboratorio Web API con Minimal API e DTO estenderà questa risposta a operazioni CRUD.

## Le parole da riconoscere

- `minimal api`
- `webapplication`
- `mapget`
- `mappost`
- `program.cs`
- `status codes`
- `typedresults`

## Anatomia e Sintassi del Codice

### Anatomia di un'applicazione Minimal API in Program.cs:
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/api/health", () => Results.Ok(new { status = "Healthy" }));
app.MapGet("/api/users/{id:int}", (int id) => Results.Ok(new { Id = id }));
app.Run();
```

## Un esempio concreto

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/api/hello", () => Results.Ok(new { message = "Ciao da .NET!" }));
app.Run();
```

### Seguilo passo per passo

1. `WebApplication.CreateBuilder(args)` prepara configurazione e servizi; `Build()` produce l'applicazione che riceverà le richieste.
2. `MapGet` associa una richiesta GET su `/api/hello` a una funzione che restituisce un risultato HTTP con un oggetto JSON.
3. `Run()` avvia il server e mantiene il processo in ascolto. La porta effettiva dipende dalla configurazione di avvio.
4. Apri l'URL completo riportato dal terminale e prova un percorso diverso. Confronta la risposta con la rotta registrata.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```csharp
public static class RouteRegistry {
    public static string HealthCheck() => "Healthy";
    public static int GetStatusCode(bool success) => success ? 200 : 400;
}
```

## Dove ci si confonde spesso

- Confondere la registrazione dei servizi (`builder.Services`) con la configurazione della pipeline (`app.Use...`)
- pensare che Minimal API o TypedResults siano obbligatori per ogni progetto.

## Domanda di verifica

> Quali criteri, oltre alla quantità di codice, useresti per scegliere tra Minimal API e Controller?
