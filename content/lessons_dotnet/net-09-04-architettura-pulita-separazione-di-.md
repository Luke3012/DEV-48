# Architettura Pulita: separazione di Domain, Application e API

## In parole semplici

L'obiettivo di questa lezione è organizzare una soluzione enterprise isolando entità di dominio, casi d'uso e adapter infrastrutturali.

La Clean Architecture stabilisce che le regole di business e il dominio centrale non devono dipendere da nessun framework esterno, database o libreria UI. I dettagli dipendono dal dominio, mai il contrario.

### Nel percorso

Da conoscere: [Dependency Injection: Transient, Scoped e Singleton](net-03-02-dependency-injection-transient-scop.md); [Principi SOLID applicati allo sviluppo Full-Stack](net-09-03-principi-solid-applicati-allo-svilu.md).

Usa questa separazione quando regole e integrazioni cambiano in modo indipendente. Un CRUD piccolo può iniziare con cartelle e servizi nello stesso progetto: creare quattro progetti subito aggiunge configurazione senza necessariamente migliorare lo studio. Angular comunica con l'API via HTTP e non è un assembly dipendente da Domain. L'esercizio considera i riferimenti tra layer di business; il punto di composizione dell'API può conoscere Infrastructure per registrare le implementazioni.

## Le parole da riconoscere

- `clean architecture`
- `onion architecture`
- `domain layer`
- `application layer`
- `infrastructure`
- `dependency rule`

## Anatomia e Sintassi del Codice

### I Layer della Clean Architecture:
1. **Domain (Nucleo)**: Entità pure, Value Objects, eccezioni di dominio. Zero dipendenze esterne.
2. **Application (Casi d'Uso)**: DTO, interfacce dei repository, comandi e query di business. Dipende solo dal Domain.
3. **Infrastructure**: Implementazione concreta dei repository con EF Core, invio email, client HTTP esterni. Dipende da Application e Domain.
4. **API / Presentation**: Minimal API di ASP.NET Core o frontend Angular. Riceve le richieste e delega ai casi d'uso.

## Un esempio concreto

```text
API endpoint -> caso d'uso Application -> regole Domain

Infrastructure implementa i contratti dichiarati verso il centro. Domain non conosce database, ASP.NET Core o Angular.
```

### Seguilo passo per passo

1. Il Domain contiene regole e modelli centrali; non importa EF Core o ASP.NET Core.
2. Application coordina casi d'uso e dichiara le porte di cui ha bisogno; Infrastructure può implementare quelle porte usando EF Core.
3. API riceve richieste HTTP e compone i servizi. Le dipendenze puntano verso il centro: Domain non dipende dai dettagli esterni.
4. Segui una richiesta dal route handler al caso d'uso e al repository. Se trovi un `DbContext` nel Domain, sposta l'accesso al database verso Infrastructure.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```csharp
using System.Threading;
using System.Threading.Tasks;

public sealed record Subject(string Name);

public interface ISubjectRepository {
    Task SaveAsync(Subject subject, CancellationToken cancellationToken);
}

public sealed class RegisterSubject(ISubjectRepository repository) {
    public Task ExecuteAsync(Subject subject, CancellationToken cancellationToken) =>
        repository.SaveAsync(subject, cancellationToken);
}
```

## Dove ci si confonde spesso

- Far dipendere il Domain da EF Core o da librerie web
- saltare i layer e scrivere query SQL direttamente nei componenti UI.

## Domanda di verifica

> Qual è la regola cardinale della Clean Architecture riguardo alla direzione delle dipendenze?
