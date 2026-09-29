# Query con LINQ su Database: Tracking e AsNoTracking

## In parole semplici

L'obiettivo di questa lezione è capire quando una query EF Core di sola lettura può usare AsNoTracking e quali trade-off comporta.

Per una query di sola lettura, `AsNoTracking()` evita di conservare le entità nel Change Tracker e può ridurre lavoro e memoria. Il beneficio dipende dai dati e dalla forma della query; senza identity resolution, le entità ripetute possono diventare istanze separate. Misura prima di presentare un guadagno come certo.

## Le parole da riconoscere

- `linq to entities`
- `asnotracking`
- `change tracker`
- `includi`
- `eager loading`
- `n+1`

## Anatomia e Sintassi del Codice

### Tracking vs NoTracking:
- **Query con Tracking (default per entità)**:
  EF Core registra le entità e rileva le modifiche. Se cambi una proprietà e chiami `SaveChangesAsync()`, può inviare al database l'aggiornamento corrispondente. Il tracking supporta anche l'identity resolution.
- **Query `AsNoTracking()` (sola lettura)**:
  EF Core non registra nel contesto le entità restituite. Può essere adatto a letture che non verranno salvate; non usa l'identity resolution del contesto.
  ```csharp
  var products = await db.Products
      .AsNoTracking()
      .Where(p => p.Price > 50)
      .ToListAsync();
  ```

### Caricamento delle Relazioni con `Include()` (Eager Loading):
```csharp
var orderWithItems = await db.Orders
    .AsNoTracking()
    .Include(o => o.Items) // Carica gli articoli correlati in questa query.
    .FirstOrDefaultAsync(o => o.Id == id);
```

## Un esempio concreto

```csharp
var users = await db.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .ToListAsync();
```

### Seguilo passo per passo

1. La query parte da `db.Users`, filtra le righe attive con `Where` e termina con `ToListAsync()`.
2. `AsNoTracking()` indica che EF Core non deve conservare quelle entità nel Change Tracker: è utile se la lettura non porterà a modifiche nello stesso contesto.
3. L'assenza di tracking può ridurre lavoro e memoria, ma il risultato dipende dalla query. Senza identity resolution, righe che rappresentano la stessa entità possono produrre istanze separate.
4. Seleziona un caso in cui vuoi aggiornare l'entità e confrontalo con una lettura solo per visualizzazione. Scegli in base al lavoro successivo, non al verbo HTTP.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Scegliere il tracking solo dal verbo HTTP: considera se aggiornerai le entità e se la query ha bisogno di identity resolution. `Include()` carica relazioni, ma controlla comunque la forma della query e i dati.

## Domanda di verifica

> Quando è adatto `AsNoTracking()` e quale comportamento del tracking rinunci a usare?
