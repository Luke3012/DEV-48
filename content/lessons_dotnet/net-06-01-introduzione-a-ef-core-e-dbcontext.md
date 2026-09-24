# Introduzione a EF Core e DbContext

## In parole semplici

L'obiettivo di questa lezione è configurare l'ORM standard di .NET, definire la classe DbContext e connettere il database relazionale.

Entity Framework Core mappa entità e relazioni e traduce le parti supportate delle query LINQ in SQL per il provider configurato. La connessione e la durata del contesto restano parte della configurazione dell'app.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `ef core`
- `dbcontext`
- `dbset`
- `orm`
- `sqlite`
- `connection string`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`ef core`, `dbcontext`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class DbContextHelper {
    public static string BuildSqliteConnectionString(string dbName) =>
        $"Data Source={dbName.TrimEnd('/')}.db";
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Creare istanze manuali con `new AppDbContext()` invece di ottenerle dalla Dependency Injection
- registrare il DbContext come Singleton.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è il ruolo principale della classe DbContext in un'applicazione .NET?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
