# LINQ fondamentale: Where, Select e Aggregazioni

## In parole semplici

L'obiettivo di questa lezione è interrogare e trasformare collezioni con sintassi dichiarativa LINQ e deferred execution.

La query LINQ non viene eseguita nel momento in cui viene definita, ma solo quando i risultati vengono effettivamente enumerati (ad esempio con un foreach, un ToList() o un'aggregazione).

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `linq`
- `where`
- `select`
- `orderby`
- `firstordefault`
- `tolist`
- `deferred execution`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`linq`, `where`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
using System.Linq;
using System.Collections.Generic;

public static class OrderAnalytics {
    public static decimal GetTotalHighValue(IEnumerable<decimal> orders, decimal threshold) =>
        orders.Where(o => o >= threshold).Sum();
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare che LINQ usa la valutazione ritardata (deferred execution) e richiamare query multiple senza materializzarle
- usare First() invece di FirstOrDefault() provocando crash se vuoto.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Che cosa si intende per esecuzione differita (deferred execution) in LINQ?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
