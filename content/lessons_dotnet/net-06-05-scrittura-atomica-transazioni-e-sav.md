# Scrittura atomica, Transazioni e SaveChangesAsync

Aggiungere un oggetto al contesto cambia prima lo stato in memoria. Il database viene coinvolto quando chiami `SaveChangesAsync`: capire il confine fra queste due fasi aiuta a diagnosticare perché una modifica non è persistita o perché un gruppo di operazioni è stato confermato insieme.

## Dall'oggetto C# alla riga del database

### Traccia un inserimento
```csharp
var measure = new Measure { SubjectId = subjectId, Value = 12.5m };
db.Measures.Add(measure);

Console.WriteLine(db.Entry(measure).State); // Added; non è ancora stato inserito
var recordsAffected = await db.SaveChangesAsync(cancellationToken);
Console.WriteLine(db.Entry(measure).State); // Unchanged dopo il successo
Console.WriteLine(measure.Id);              // chiave generata dal provider
```

`Add` registra l'entità nel Change Tracker; la chiamata a `SaveChangesAsync` invia gli INSERT/UPDATE/DELETE pendenti. Con un provider relazionale, una singola chiamata usa normalmente una transazione, quindi le modifiche di quella chiamata vengono applicate insieme. `recordsAffected` è il numero di voci di stato scritte, non una misura del tempo né un ID.

Se un caso d'uso deve salvare in più chiamate o coordinare operazioni che la chiamata singola non include, apri una transazione esplicita con `Database.BeginTransactionAsync`, esegui il lavoro e conferma con `CommitAsync`; in caso di eccezione, la disposizione della transazione la annulla. Gestisci anche i conflitti di concorrenza: atomicità non significa che nessun altro possa aver modificato i dati.

## Segui il lavoro del DbContext

```csharp
db.Measures.Add(measure);
var savedEntries = await db.SaveChangesAsync(cancellationToken);
```

### Osserva che cosa ha fatto il contesto

1. `Add(measure)` porta l'entità allo stato `Added` nel contesto; osserva che la riga non è ancora nel database.
2. `SaveChangesAsync` invia l'INSERT. Il provider può valorizzare `measure.Id` con la chiave generata.
3. Se la chiamata riesce, il metodo restituisce il numero di entry scritte e il contesto accetta lo stato come `Unchanged`.
4. Prova un vincolo non valido e osserva l'eccezione. Poi raggruppa le modifiche prima della singola chiamata; usa una transazione esplicita solo quando l'unità di lavoro attraversa più salvataggi.

La pratica breve interpreta il numero restituito da `SaveChangesAsync`; nel laboratorio verifica che il dato esista con una query dopo il commit, non solo che `Add` sia stato chiamato.

## Che cosa resta responsabilità del database?

- Chiamare `SaveChangesAsync()` all'interno di un ciclo foreach invece di raggruppare le modifiche ed eseguire una singola chiamata finale.

> **Che cosa è stato caricato o salvato davvero?** Che cosa restituisce il metodo `SaveChangesAsync()` al suo completamento?
