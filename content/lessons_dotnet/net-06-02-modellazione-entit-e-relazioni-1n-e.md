# Modellazione Entità e Relazioni 1:N e N:N

## In parole semplici

L'obiettivo di questa lezione è mappare chiavi primarie, foreign key e relazioni tra tabelle usando Fluent API e convenzioni.

Le navigation properties consentono di navigare tra entità correlate (es. da un Ordine ai suoi Articoli) in modo naturale orientato agli oggetti.

## Le parole da riconoscere

- `entita`
- `primary key`
- `foreign key`
- `relazione 1 a molti`
- `onmodelcreating`
- `navigation property`

## Anatomia e Sintassi del Codice

### Convenzione per Relazione 1 a Molti (1:N):
```csharp
public class Category {
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;

    // Navigation property: una categoria ha molti prodotti
    public List<Product> Products { get; set; } = new();
}

public class Product {
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;

    // Foreign Key verso Category
    public int CategoryId { get; set; }
    public Category? Category { get; set; }
}
```

In `OnModelCreating` si può personalizzare il comportamento di cancellazione (es. `OnDelete(DeleteBehavior.Cascade)`).

## Un esempio concreto

```html
modelBuilder.Entity<Order>()
    .HasMany(o => o.Items)
    .WithOne(i => i.Order)
    .HasForeignKey(i => i.OrderId);
```

### Seguilo passo per passo

1. `Order` è il lato principale della relazione; `HasMany(o => o.Items)` dichiara che un ordine può avere molti articoli.
2. `WithOne(i => i.Order)` dichiara che ogni articolo appartiene a un ordine; `HasForeignKey(i => i.OrderId)` indica la colonna che conserva la chiave esterna.
3. EF Core usa la configurazione per creare lo schema e materializzare le navigation properties; le classi `Order` e `Item` devono esistere e avere chiavi valide.
4. Prova a salvare due articoli per un ordine e poi un articolo con chiave esterna inesistente. Individua quale vincolo applica il database.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Dimenticare la Foreign Key esplicita lasciando che EF crei 'shadow properties' con nomi automatici difficili da interrogare.

## Domanda di verifica

> Che cos'è una navigation property in Entity Framework Core?
