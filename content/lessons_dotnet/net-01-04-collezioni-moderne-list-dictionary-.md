# Collezioni moderne: List, Dictionary e Array

## In parole semplici

L'obiettivo di questa lezione è scegliere e manipolare strutture dati fondamentali in memoria in base alle operazioni richieste.

Un Dictionary usa una chiave per trovare un valore. La ricerca ha costo medio vicino a O(1), mentre cercare in una List richiede in genere di esaminare gli elementi fino alla corrispondenza. Sono stime: la scelta dipende da come userai i dati.

## Le parole da riconoscere

- `list`
- `dictionary`
- `array`
- `lookup`
- `indice`
- `capacita`
- `collezione generica`

## Anatomia e Sintassi del Codice

### Principali Collezioni in C#:
1. **`T[]` (Array)**: Dimensione fissa allocata in memoria contigua. Minimo overhead, ideale quando il numero di elementi è noto a priori.
2. **`List<T>`**: Lista a dimensione dinamica. Permette `.Add()`, `.Remove()`, `.Insert()`. Internamente si ridimensiona automaticamente.
3. **`Dictionary<TKey, TValue>`**: Mappa chiave-valore basata su tabella hash. La ricerca ha costo medio vicino a $O(1)$; non è una garanzia per ogni caso.
   - Per accedere in sicurezza senza eccezioni si usa `TryGetValue`:
   ```csharp
   if (dict.TryGetValue(key, out var val)) { ... }
   ```

### Collection Expressions (C# 12):
Da C# 12 puoi inizializzare array, liste e insiemi con la sintassi uniforme a parentesi quadre:
```csharp
List<int> numbers = [1, 2, 3, 4];
string[] names = ["Anna", "Luca"];
```

## Un esempio concreto

```csharp
var subjects = new List<string> { "Mario", "Anna", "Paolo" };
var lookup = new Dictionary<int, string> { [1] = "Mario", [2] = "Anna" };
if (lookup.TryGetValue(1, out var found)) {
    Console.WriteLine(found);
}
```

### Seguilo passo per passo

1. `subjects` conserva tre nomi in ordine: una `List` si adatta quando l'elenco deve crescere o ridursi.
2. `lookup` associa la chiave intera `1` al valore `"Mario"`; `TryGetValue` prova la ricerca senza lanciare un'eccezione se la chiave manca.
3. Se la chiave esiste, `found` contiene il nome e il blocco stampa `Mario`; l'`if` non esegue il blocco per una chiave assente.
4. Cambia `1` in `99` e osserva il ramo non eseguito. Per ricerche ripetute, scegli una struttura in base alle operazioni necessarie, non solo alla complessità media.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
public static class CacheStore {
    private static readonly Dictionary<string, int> _items = new();
    public static void Set(string key, int value) => _items[key] = value;
    public static int GetOrDefault(string key, int fallback = 0) => _items.TryGetValue(key, out var v) ? v : fallback;
}
```

## Dove ci si confonde spesso

- Accedere a una chiave inesistente di un dizionario con l'indicizzatore anziché `TryGetValue`
- usare array a dimensione fissa quando serve aggiungere elementi dinamicamente.

## Domanda di verifica

> In quale scenario un Dictionary è preferibile rispetto a una List per la ricerca di elementi?
