# Query con LINQ su Database: Tracking e AsNoTracking

Quando EF Core materializza un'entità tracciata, il `DbContext` conserva i valori originali e può riconoscere le modifiche successive. Per una schermata di sola lettura, `AsNoTracking` evita quel lavoro; dopo aver scelto, il codice deve essere coerente con il fatto che la modifica verrà o non verrà salvata.

## Dall'oggetto C# alla riga del database

### Guarda lo stato dell'entità
```csharp
var subject = await db.Subjects.SingleAsync(item => item.Id == id, cancellationToken);
Console.WriteLine(db.Entry(subject).State); // Unchanged

subject.Name = "Marco";
db.ChangeTracker.DetectChanges();
Console.WriteLine(db.Entry(subject).State); // Modified

await db.SaveChangesAsync(cancellationToken); // UPDATE ...
Console.WriteLine(db.Entry(subject).State); // Unchanged
```

Una query di entità è tracked per default. Il contesto mantiene la stessa istanza e rileva che `Name` è cambiato. Dopo `SaveChangesAsync`, EF Core invia l'aggiornamento e accetta i valori come nuova base.

Per una lettura che non verrà modificata nello stesso contesto:
```csharp
var rows = await db.Subjects
    .AsNoTracking()
    .Where(subject => subject.Name.StartsWith("A"))
    .Select(subject => new SubjectRow(subject.Id, subject.Name))
    .ToListAsync(cancellationToken);

public sealed record SubjectRow(int Id, string Name);
```

Questo risultato non viene registrato nel Change Tracker. Modificare l'oggetto materializzato e chiamare `SaveChangesAsync` non lo aggiorna. Le proiezioni in DTO sono spesso adatte alle API read-only; il vantaggio prestazionale di `AsNoTracking` dipende dalla query e va misurato.

## Segui il lavoro del DbContext

```csharp
var subject = await db.Subjects.SingleAsync(item => item.Id == id, cancellationToken);
db.ChangeTracker.DetectChanges();
subject.Name = "Marco";
await db.SaveChangesAsync(cancellationToken);
```

### Osserva che cosa ha fatto il contesto

1. La query tracked materializza il soggetto e il suo stato iniziale è `Unchanged`.
2. L'assegnazione `Name = "Marco"` cambia l'oggetto in memoria; EF rileva `Modified` quando aggiorna lo stato.
3. `SaveChangesAsync` traduce la differenza in un `UPDATE` e dopo il salvataggio lo stato torna `Unchanged`.
4. Ripeti la query con `AsNoTracking`. Il soggetto torna leggibile, ma una modifica successiva non produce un `UPDATE` da quel contesto. Scegli in base all'uso successivo, non al verbo HTTP.

L'esercizio breve classifica la politica di tracking; nel laboratorio modifica un'entità letta dal contesto e verifica il database dopo `SaveChangesAsync`, poi confronta una proiezione read-only.

## Che cosa resta responsabilità del database?

- Scegliere il tracking solo dal verbo HTTP: considera se aggiornerai le entità e se la query ha bisogno di identity resolution. `Include()` carica relazioni, ma controlla comunque la forma della query e i dati.

> **Che cosa è stato caricato o salvato davvero?** Quando è adatto `AsNoTracking()` e quale comportamento del tracking rinunci a usare?
