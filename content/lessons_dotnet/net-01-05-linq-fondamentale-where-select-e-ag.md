# LINQ fondamentale: Where, Select e Aggregazioni

## In parole semplici

L'obiettivo di questa lezione è interrogare e trasformare collezioni con sintassi dichiarativa LINQ e deferred execution.

La query LINQ non viene eseguita nel momento in cui viene definita, ma solo quando i risultati vengono effettivamente enumerati (ad esempio con un foreach, un ToList() o un'aggregazione).

## Le parole da riconoscere

- `linq`
- `where`
- `select`
- `orderby`
- `firstordefault`
- `tolist`
- `deferred execution`

## Anatomia e Sintassi del Codice

### Leggere una lambda
`n => n % 2 == 0` è una funzione breve: riceve `n` e restituisce un booleano. `Where` la chiama per ogni elemento e conserva quelli per cui il risultato è true. In `Select(n => n * 2)` la funzione restituisce invece il nuovo valore. Il tipo del parametro è inferito dalla collezione.

### I Metodi LINQ Più Utilizzati:
- **`Where(predicate)`**: Filtra gli elementi che soddisfano la condizione booleana.
- **`Select(selector)`**: Mappa e trasforma ciascun elemento (proiezione).
- **`OrderBy(key)` / `OrderByDescending(key)`**: Ordina gli elementi.
- **`FirstOrDefault(predicate)`**: Restituisce il primo elemento che corrisponde o il valore di default (`null` per tipi riferimento, `0` per numeri). Non lancia eccezioni se la sequenza è vuota!
- **`Count()` / `Sum()` / `Average()`**: Aggregazioni matematiche immediate.
- **`ToList()` / `ToArray()`**: Materializza la sequenza differita in una collezione in memoria.

```csharp
using System.Linq;

var activeUsers = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => u.Email)
    .ToList();
```

## Un esempio concreto

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
var evensDoubled = numbers
    .Where(n => n % 2 == 0)
    .Select(n => n * 2)
    .ToList();
```

### Seguilo passo per passo

1. La lista iniziale contiene i numeri da 1 a 6. `Where` conserva quelli divisibili per 2: `2`, `4`, `6`.
2. `Select` trasforma ogni elemento rimasto moltiplicandolo per 2, quindi la sequenza diventa `4`, `8`, `12`.
3. `ToList()` esegue la query e materializza il risultato in una nuova lista; prima di quel punto, una query LINQ può essere valutata solo quando la enumeri.
4. Prova una lista vuota e poi rimuovi `ToList()`: descrivi quando viene eseguita la trasformazione e quante volte la enumerazione la ripete.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
using System.Linq;
using System.Collections.Generic;

public static class OrderAnalytics {
    public static decimal GetTotalHighValue(IEnumerable<decimal> orders, decimal threshold) =>
        orders.Where(o => o >= threshold).Sum();
}
```

## Dove ci si confonde spesso

- Dimenticare che LINQ usa la valutazione ritardata (deferred execution) e richiamare query multiple senza materializzarle
- usare First() invece di FirstOrDefault() provocando crash se vuoto.

## Domanda di verifica

> Che cosa si intende per esecuzione differita (deferred execution) in LINQ?
