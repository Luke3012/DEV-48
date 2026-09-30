# Dependency Injection: Transient, Scoped e Singleton

Una classe che esegue `new UserRepository()` decide da sola quale implementazione usare, come costruirla e quanto a lungo conservarla. Quando l'endpoint deve poter usare un archivio reale o uno sostituto di test, conviene dichiarare la dipendenza e lasciare al contenitore la creazione e la durata degli oggetti.

### Nel percorso

Da conoscere: [Classi, Record e Costruttori Primari](net-01-03-classi-record-e-costruttori-primari.md); [Minimal API da zero: Program.cs e WebApplication](net-03-01-minimal-api-da-zero-programcs-e-web.md).

La scelta del ciclo di vita dipende dallo stato del servizio. Un repository che usa DbContext deve restare nella richiesta; un singleton condiviso richiede stato sicuro per accessi concorrenti. Evita di scegliere Singleton soltanto per risparmiare istanze.

## Un oggetto non deve costruirsi tutte le dipendenze

### Prima la dipendenza, poi la registrazione
Un costruttore che crea direttamente il repository è legato a quell'implementazione. Con DI il consumer chiede un'interfaccia e il contenitore fornisce la classe registrata. Questo esempio minimale può vivere in `Program.cs`:
```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddScoped<IUserRepository, InMemoryUserRepository>();
builder.Services.AddScoped<UserService>();
var app = builder.Build();

app.MapGet("/api/users/{id:int}", (int id, UserService service) =>
    service.Find(id) is { } user ? Results.Ok(user) : Results.NotFound());
app.Run();

public sealed record User(int Id, string Name);
public interface IUserRepository { User? Find(int id); }

public sealed class InMemoryUserRepository : IUserRepository
{
    private readonly User[] users = [new(1, "Anna"), new(2, "Luca")];
    public User? Find(int id) => users.FirstOrDefault(user => user.Id == id);
}

public sealed class UserService(IUserRepository users)
{
    public User? Find(int id) => users.Find(id);
}
```

La registrazione dice quale oggetto consegnare; il parametro dell'handler dichiara chi lo richiede. Un test può registrare un repository finto senza riscrivere il servizio.

### Visualizzare le durate con un identificatore
```csharp
public interface ITransientId { Guid Id { get; } }
public interface IScopedId { Guid Id { get; } }
public interface ISingletonId { Guid Id { get; } }

public sealed class OperationId : ITransientId, IScopedId, ISingletonId
{
    public Guid Id { get; } = Guid.NewGuid();
}

builder.Services.AddTransient<ITransientId, OperationId>();
builder.Services.AddScoped<IScopedId, OperationId>();
builder.Services.AddSingleton<ISingletonId, OperationId>();
```

Ogni registrazione rappresenta una durata diversa. In un endpoint inietta due istanze dello stesso contratto e confronta gli identificatori:
```text
Richiesta HTTP A       Transient: A1, A2    Scoped: S1, S1    Singleton: G1
Richiesta HTTP B       Transient: B1, B2    Scoped: S2, S2    Singleton: G1
```

Il contenitore ASP.NET Core crea uno scope per richiesta. Un `DbContext` è normalmente Scoped e rappresenta un'unità di lavoro; non è thread-safe. Un Singleton non deve catturare una dipendenza Scoped.

## Confronta le istanze nella stessa richiesta e tra richieste

```csharp
builder.Services.AddScoped<IUserRepository, SqlUserRepository>();
```

### Segui la richiesta con valori concreti

1. Nella stessa richiesta HTTP chiedi due volte `ITransientId`: il contenitore crea due oggetti e gli ID sono diversi.
2. Chiedi due volte `IScopedId`: la richiesta condivide il medesimo scope, quindi i due ID coincidono.
3. In una seconda richiesta cambiano i due ID Scoped; l'ID Singleton resta uguale perché appartiene alla vita dell'applicazione.
4. Se un Singleton richiede un servizio Scoped, in sviluppo ASP.NET Core può segnalare `InvalidOperationException` per il lifetime incompatibile. Correggi il grafo delle dipendenze invece di disabilitare la convalida.

L'esercizio isola una decisione sul lifetime. Nel laboratorio API, usa `AddScoped` per il repository che dipende dal `DbContext` e prova il servizio tramite l'endpoint HTTP.

## Lifetimes che non possono convivere

- Iniettare un servizio Scoped (come il DbContext) dentro un Singleton senza creare e gestire uno scope esplicito: il servizio conserva una dipendenza più breve del proprio lifetime.

> **Per quanto tempo deve vivere questo servizio?** Perché `DbContext` ha normalmente durata Scoped in una Web API, e che cosa non garantisce questo lifetime?
