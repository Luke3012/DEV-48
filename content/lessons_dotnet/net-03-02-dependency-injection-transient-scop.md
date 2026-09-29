# Dependency Injection: Transient, Scoped e Singleton

## In parole semplici

L'obiettivo di questa lezione è conoscere i tre cicli di vita del contenitore DI di ASP.NET Core e scegliere in base alla condivisione e alla durata delle dipendenze.

La Dependency Injection disaccoppia le classi fornendo le dipendenze richieste dall'esterno, facilitando il testing e la gestione del ciclo di vita degli oggetti.

### Nel percorso

Da conoscere: [Classi, Record e Costruttori Primari](net-01-03-classi-record-e-costruttori-primari.md); [Minimal API da zero: Program.cs e WebApplication](net-03-01-minimal-api-da-zero-programcs-e-web.md).

La scelta del ciclo di vita dipende dallo stato del servizio. Un repository che usa DbContext deve restare nella richiesta; un singleton condiviso richiede stato sicuro per accessi concorrenti. Evita di scegliere Singleton soltanto per risparmiare istanze.

## Le parole da riconoscere

- `dependency injection`
- `ioc container`
- `transient`
- `scoped`
- `singleton`
- `disposable`

## Anatomia e Sintassi del Codice

### I Tre Lifetimes di ASP.NET Core:
1. **`Transient` (`AddTransient<TService, TImpl>()`)**:
   - Viene creata una nuova istanza ogni volta che il servizio viene richiesto.
   - Ideale per servizi leggeri e stateless.
2. **`Scoped` (`AddScoped<TService, TImpl>()`)**:
   - Viene creata una sola istanza per ogni scope di servizio; nelle Web API, di solito lo scope coincide con una richiesta HTTP.
   - `AddDbContext` registra normalmente `DbContext` come scoped. Questo allinea la durata del contesto alla richiesta, ma non avvia da solo una transazione che copra più chiamate a `SaveChanges`.
3. **`Singleton` (`AddSingleton<TService, TImpl>()`)**:
   - Viene creata un'unica istanza condivisa per l'intera durata dell'applicazione.
   - Ideale per cache in memoria, logger o servizi di background thread-safe.

## Un esempio concreto

```csharp
builder.Services.AddSingleton<ICache, MemoryCache>();
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddTransient<IEmailSender, EmailSender>();
```

### Seguilo passo per passo

1. Ogni riga registra un contratto (`ICache`, `IUserRepository`, `IEmailSender`) e la classe che lo implementa.
2. `Transient` crea un'istanza per ogni richiesta di servizio; `Scoped` riusa l'istanza nella richiesta web; `Singleton` mantiene un'istanza per la vita del contenitore.
3. ASP.NET Core risolve il servizio quando serve, per esempio nel costruttore di un endpoint o di un'altra classe. Il ciclo di vita influenza la condivisione dello stato.
4. Immagina due richieste HTTP e confronta cosa può essere condiviso. Non inserire una dipendenza `Scoped` in un `Singleton` senza progettare esplicitamente lo scope.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```csharp
public interface ICounterService { int Next(); }
public class CounterService : ICounterService {
    private int _count = 0;
    public int Next() => ++_count;
}
```

## Dove ci si confonde spesso

- Iniettare un servizio Scoped (come il DbContext) dentro un Singleton senza creare e gestire uno scope esplicito: il servizio conserva una dipendenza più breve del proprio lifetime.

## Domanda di verifica

> Perché `DbContext` ha normalmente durata Scoped in una Web API, e che cosa non garantisce questo lifetime?
