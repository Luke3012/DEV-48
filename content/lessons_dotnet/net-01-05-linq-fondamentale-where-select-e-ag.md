# LINQ fondamentale: Where, Select e Aggregazioni

Hai una lista di utenti e vuoi mostrare soltanto quelli attivi e maggiorenni, ordinati per nome, con i campi che servono alla tabella. Un ciclo esplicito rende visibile il lavoro; LINQ permette di esprimere lo stesso percorso come una trasformazione leggibile.

## Dal problema alla regola del linguaggio

### Prima: descrivere il lavoro passo per passo
```csharp
public sealed record User(int Id, string Name, int Age, bool IsActive, string Email);
public sealed record UserRow(string Name, string Email);

var rows = new List<UserRow>();
var users = new List<User>
{
    new(1, "Anna", 35, true, "anna@example.com"),
    new(2, "Marco", 16, true, "marco@example.com"),
    new(3, "Luca", 42, false, "luca@example.com")
};
foreach (var user in users)
{
    if (!user.IsActive || user.Age < 18) continue;
    rows.Add(new UserRow(user.Name, user.Email));
}
rows.Sort((a, b) => string.Compare(a.Name, b.Name, StringComparison.Ordinal));
```

### Poi: nominare i passaggi con LINQ
```csharp
var rows = users
    .Where(user => user.IsActive && user.Age >= 18)
    .OrderBy(user => user.Name)
    .Select(user => new UserRow(user.Name, user.Email))
    .ToList();
```

`Where` decide quali elementi restano; `OrderBy` decide in quale ordine; `Select` costruisce il dato destinato alla vista. In un progetto, il tipo `User` e la query vivono nel server, mentre `UserRow` può diventare un DTO se attraversa il confine HTTP. LINQ to Objects e LINQ to Entities condividono la forma, ma EF Core può tradurre in SQL soltanto le espressioni supportate dal provider.

## Traccia i valori nel programma

```csharp
var evenNumbers = numbers.Where(n => n % 2 == 0).Select(n => n * 2).ToList();
```

### Calcola il risultato prima di eseguirlo

1. Con i numeri `[1, 2, 3, 4]`, `Where` conserva `[2, 4]` perché solo quei valori soddisfano la condizione.
2. `Select` trasforma la sequenza in `[4, 8]`; non modifica la lista originale.
3. Gli operatori di filtro e proiezione costruiscono una query differita. `ToList()` la enumera e conserva qui il risultato.
4. Applica lo stesso ragionamento agli utenti: prima scegli le righe, poi ordinale, poi proietta i campi necessari. Se la fonte è `IQueryable`, verifica che ogni espressione sia traducibile dal provider.

Per l'esercizio, prima prevedi l'insieme dopo ogni trasformazione e solo dopo componi la query. Il laboratorio CRUD usa un archivio vero in memoria e aggiunge casi vuoti e identificativi assenti.

## Casi che cambiano il risultato

- Dimenticare che LINQ usa la valutazione ritardata (deferred execution) e richiamare query multiple senza materializzarle
- usare First() invece di FirstOrDefault() provocando crash se vuoto.

> **Che cosa succede se cambia l'input?** Che cosa si intende per esecuzione differita (deferred execution) in LINQ?
