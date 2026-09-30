# Collezioni moderne: List, Dictionary e Array

Un elenco di soggetti va attraversato e ordinato; una ricerca ripetuta per ID richiede invece una struttura pensata per le chiavi. `List<T>` e `Dictionary<TKey, TValue>` sono collezioni generiche: il tipo fra parentesi angolari lega la struttura ai dati ammessi e fa controllare accessi e assegnazioni dal compilatore.

## Dal problema alla regola del linguaggio

### Lo stesso dominio, due operazioni diverse
```csharp
public sealed record Subject(int Id, string Name);

var subjects = new List<Subject>
{
    new(1, "Anna"),
    new(2, "Luca")
};

var byId = new Dictionary<int, Subject>
{
    [1] = subjects[0],
    [2] = subjects[1]
};

if (byId.TryGetValue(2, out var selected))
{
    Console.WriteLine(selected.Name);
}
```

`List<Subject>` conserva una sequenza attraversabile e modificabile; `Dictionary<int, Subject>` associa chiavi intere a soggetti. `TryGetValue` rappresenta l'assenza come un risultato booleano, senza usare un'eccezione per il caso normale della chiave mancante.

La parte generica `<T>` è un parametro di tipo: `List<Subject>` e `List<string>` riusano la stessa collezione con contratti diversi. Dentro `List<Subject>`, il compilatore sa che ogni elemento ha `Id` e `Name`; non serve convertire da `object` o affidarsi a `dynamic`. Un metodo generico può applicare la stessa operazione a più tipi senza perdere l'informazione sul tipo ricevuto.

## Traccia i valori nel programma

```text
Dictionary<int, Subject> byId = subjects.ToDictionary(subject => subject.Id);
```

### Calcola il risultato prima di eseguirlo

1. `subjects` contiene due record e ne conserva l'ordine di inserimento.
2. `ToDictionary` estrae ogni `Id` e lo usa come chiave; il valore associato resta un `Subject` completo.
3. `TryGetValue(2, out var selected)` cerca la chiave. Se esiste, `selected` è un `Subject`; il compilatore controlla l'accesso a `Name`.
4. Prova l'ID `99`: il metodo restituisce `false` e non entra nel blocco. Scegli List per enumerare una sequenza e Dictionary quando l'operazione centrale è cercare tramite chiave.

Il mini-esercizio usa collezioni C# vere: controlla chiave presente, assente e input vuoto prima di passare al laboratorio CRUD, dove più operazioni condividono lo stesso archivio.

## Casi che cambiano il risultato

- Accedere a una chiave inesistente di un dizionario con l'indicizzatore anziché `TryGetValue`
- usare array a dimensione fissa quando serve aggiungere elementi dinamicamente.

> **Che cosa succede se cambia l'input?** In quale scenario un Dictionary è preferibile rispetto a una List per la ricerca di elementi?
