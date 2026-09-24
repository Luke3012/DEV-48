# Modellazione Entità e Relazioni 1:N e N:N

## In parole semplici

L'obiettivo di questa lezione è mappare chiavi primarie, foreign key e relazioni tra tabelle usando Fluent API e convenzioni.

Le navigation properties consentono di navigare tra entità correlate (es. da un Ordine ai suoi Articoli) in modo naturale orientato agli oggetti.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `entita`
- `primary key`
- `foreign key`
- `relazione 1 a molti`
- `onmodelcreating`
- `navigation property`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`entita`, `primary key`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class EntityRelationHelper {
    public static bool IsForeignKeyValid(int fk) => fk > 0;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare la Foreign Key esplicita lasciando che EF crei 'shadow properties' con nomi automatici difficili da interrogare.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Che cos'è una navigation property in Entity Framework Core?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
