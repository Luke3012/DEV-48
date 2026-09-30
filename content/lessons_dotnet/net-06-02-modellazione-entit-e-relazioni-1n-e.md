# Modellazione Entità e Relazioni 1:N e N:N

Un soggetto può avere molte misure; molte misure possono riferirsi allo stesso soggetto. Nel database la relazione è memorizzata con chiavi, mentre in C# le navigation property rendono raggiungibili gli oggetti collegati quando EF Core li carica.

## Dall'oggetto C# alla riga del database

### Prima capisci cardinalità e chiavi
```text
Subject 1 ───────── * Measure
Tag     * ───────── * Subject
```

`Subject.Id` è la chiave primaria. In `Measure`, `SubjectId` è la foreign key che conserva la relazione; `Measure.Subject` e `Subject.Measures` sono navigation property. Una navigation descrive il collegamento tra oggetti, ma non significa che la riga correlata sia già stata caricata.

```csharp
public sealed class Subject
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<Measure> Measures { get; set; } = [];
    public List<Tag> Tags { get; set; } = [];
}

public sealed class Measure
{
    public int Id { get; set; }
    public decimal Value { get; set; }
    public int SubjectId { get; set; }
    public Subject Subject { get; set; } = null!;
}

public sealed class Tag
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<Subject> Subjects { get; set; } = [];
}
```

Per 1:N EF Core riconosce normalmente la chiave `SubjectId` per convenzione. Per N:N può creare una tabella di join implicita; se la relazione stessa ha dati, come data di assegnazione o autore, modella una join entity esplicita. La Fluent API rende le regole chiare quando i nomi non seguono le convenzioni.

## Segui il lavoro del DbContext

```csharp
modelBuilder.Entity<Subject>()
    .HasMany(subject => subject.Measures)
    .WithOne(measure => measure.Subject)
    .HasForeignKey(measure => measure.SubjectId);
```

### Osserva che cosa ha fatto il contesto

1. Una riga `Subject` ha `Id` come chiave primaria; più righe `Measure` possono contenere quel valore in `SubjectId`.
2. EF Core usa la foreign key per collegare `Measure.Subject` al soggetto e `Subject.Measures` alla collezione inversa.
3. Per leggere la navigazione nel risultato, chiedi esplicitamente il caricamento, ad esempio con `Include(subject => subject.Measures)`, oppure proietta i campi nella query.
4. Nel laboratorio salva due misure per lo stesso soggetto, poi prova un riferimento a un ID inesistente. Distingui il comportamento del modello C# dal vincolo di integrità che applica il database.

La pratica breve controlla una relazione isolata. Il laboratorio usa proprio Subject e Measure: aggiungi test che leggono il dato correlato dal database SQLite, non soltanto una property in memoria.

## Che cosa resta responsabilità del database?

- Dimenticare la Foreign Key esplicita lasciando che EF crei 'shadow properties' con nomi automatici difficili da interrogare.

> **Che cosa è stato caricato o salvato davvero?** Che cos'è una navigation property in Entity Framework Core?
