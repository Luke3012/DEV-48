# Introduzione a EF Core e DbContext

Il database conserva righe e vincoli; il codice C# usa oggetti e proprietà. Entity Framework Core collega i due modelli, ma non nasconde la configurazione del provider, il ciclo di vita della connessione o il momento in cui una modifica viene salvata.

### Nel percorso

Da conoscere: [LINQ fondamentale: Where, Select e Aggregazioni](net-01-05-linq-fondamentale-where-select-e-ag.md); [Dependency Injection: Transient, Scoped e Singleton](net-03-02-dependency-injection-transient-scop.md).

Il laboratorio Persistenza con EF Core e SQLite usa soggetti e misure: ritroverai lo stesso contesto nel gestionale full-stack. Il contesto segue l'unità di lavoro; non condividerlo tra richieste o operazioni parallele.

## Dall'oggetto C# alla riga del database

### Quattro file raccontano il primo passaggio
```text
server/Models/Subject.cs       forma dell'entità
server/Data/AppDbContext.cs    insieme di entità e unità di lavoro
server/Program.cs              provider, DI ed endpoint
server/dev48.db                file SQLite creato dal provider
```

```csharp
// Models/Subject.cs
public sealed class Subject
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
}

// Data/AppDbContext.cs
using Microsoft.EntityFrameworkCore;

public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Subject> Subjects => Set<Subject>();
}
```

```csharp
// Program.cs
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=dev48.db"));
var app = builder.Build();

app.MapGet("/api/subjects", async (AppDbContext db, CancellationToken ct) =>
    await db.Subjects.AsNoTracking()
        .Select(subject => new { subject.Id, subject.Name })
        .ToListAsync(ct));
app.Run();
```

```text
C# Subject → DbSet / DbContext → provider SQLite → tabella Subjects
database rows → materializzazione EF Core → oggetti C# → DTO / JSON
```

`DbSet<Subject>` è l'ingresso tipizzato alla tabella; `DbContext` coordina query e tracking per una unità di lavoro. `AddDbContext` registra normalmente il contesto come Scoped in ASP.NET Core e costruisce le opzioni per richiesta. Il provider esegue SQL sul file SQLite: il contesto non crea né aggiorna lo schema senza una migrazione o un comando esplicito.

## Segui il lavoro del DbContext

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=dev48.db"));
```

### Osserva che cosa ha fatto il contesto

1. `Program.cs` registra il provider SQLite e le opzioni di `AppDbContext` nel contenitore.
2. Alla richiesta GET, ASP.NET Core crea lo scope e inietta il contesto nel gestore.
3. `db.Subjects` costruisce una query. `ToListAsync` la esegue; EF Core traduce le parti supportate in SQL, legge le righe e le proietta nei valori restituiti.
4. Osserva la query nel log EF Core o nel laboratorio SQLite. Se cambi `Subject` ma non chiami `SaveChangesAsync`, nessuna istruzione di scrittura viene inviata al database.

Il mini-esercizio controlla una stringa di connessione. Nel laboratorio EF configura il provider, genera una migrazione e verifica lettura e scrittura contro SQLite isolato nei test.

## Che cosa resta responsabilità del database?

- Creare istanze manuali con `new AppDbContext()` invece di ottenerle dalla Dependency Injection
- registrare il DbContext come Singleton.

> **Che cosa è stato caricato o salvato davvero?** Qual è il ruolo principale della classe DbContext in un'applicazione .NET?
