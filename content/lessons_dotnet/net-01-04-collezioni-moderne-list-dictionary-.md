# Collezioni moderne: List, Dictionary e Array

## In parole semplici

L'obiettivo di questa lezione è scegliere e manipolare strutture dati fondamentali in memoria in base alle operazioni richieste.

Un Dictionary usa una chiave per trovare un valore. La ricerca ha costo medio vicino a O(1), mentre cercare in una List richiede in genere di esaminare gli elementi fino alla corrispondenza. Sono stime: la scelta dipende da come userai i dati.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `list`
- `dictionary`
- `array`
- `lookup`
- `indice`
- `capacita`
- `collezione generica`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`list`, `dictionary`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class CacheStore {
    private static readonly Dictionary<string, int> _items = new();
    public static void Set(string key, int value) => _items[key] = value;
    public static int GetOrDefault(string key, int fallback = 0) => _items.TryGetValue(key, out var v) ? v : fallback;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Accedere a una chiave inesistente di un dizionario con l'indicizzatore anziché `TryGetValue`
- usare array a dimensione fissa quando serve aggiungere elementi dinamicamente.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> In quale scenario un Dictionary è preferibile rispetto a una List per la ricerca di elementi?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
