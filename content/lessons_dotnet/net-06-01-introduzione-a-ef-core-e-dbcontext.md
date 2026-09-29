# Introduzione a EF Core e DbContext

## In parole semplici

L'obiettivo di questa lezione è configurare l'ORM standard di .NET, definire la classe DbContext e connettere il database relazionale.

Entity Framework Core mappa entità e relazioni e traduce le parti supportate delle query LINQ in SQL per il provider configurato. La connessione e la durata del contesto restano parte della configurazione dell'app.

### Nel percorso

Da conoscere: [LINQ fondamentale: Where, Select e Aggregazioni](net-01-05-linq-fondamentale-where-select-e-ag.md); [Dependency Injection: Transient, Scoped e Singleton](net-03-02-dependency-injection-transient-scop.md).

Il laboratorio Persistenza con EF Core e SQLite usa soggetti e misure: ritroverai lo stesso contesto nel gestionale full-stack. Il contesto segue l'unità di lavoro; non condividerlo tra richieste o operazioni parallele.

## Le parole da riconoscere

- `ef core`
- `dbcontext`
- `dbset`
- `orm`
- `sqlite`
- `connection string`

## Anatomia e Sintassi del Codice

### Struttura Tipica di un DbContext in EF Core:
```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext {
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {}

    // Ogni DbSet<T> corrisponde a una tabella nel database
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
}
```

### Registrazione in Program.cs (Minimal API):
```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=dev48.db"));
```

## Un esempio concreto

```csharp
public class AppDbContext : DbContext {
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {}
    public DbSet<User> Users => Set<User>();
}
```

### Seguilo passo per passo

1. `AppDbContext` eredita da `DbContext` e riceve le opzioni dal contenitore tramite il costruttore.
2. `DbSet<User> Users => Set<User>()` espone il punto di accesso tipizzato alle righe `User`; non crea da solo il database né sostituisce la configurazione del provider.
3. ASP.NET Core crea lo scope della richiesta e fornisce il contesto registrato con `AddDbContext`. Al termine dello scope, il contesto viene eliminato.
4. Segui una query da `db.Users` fino al provider SQLite configurato. Prova a registrare il contesto come singleton e spiega perché condividerlo tra richieste è pericoloso.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Creare istanze manuali con `new AppDbContext()` invece di ottenerle dalla Dependency Injection
- registrare il DbContext come Singleton.

## Domanda di verifica

> Qual è il ruolo principale della classe DbContext in un'applicazione .NET?
