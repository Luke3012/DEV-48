# Programmazione Asincrona: Task, async/await ed Eccezioni

## In parole semplici

L'obiettivo di questa lezione è gestire operazioni I/O senza bloccare il thread del server e trattare gli errori con robustezza.

Durante una vera attesa I/O asincrona, `await` sospende il metodo senza bloccare il thread in attesa. Il codice dopo `await` riprende quando il `Task` termina; chiamare `.Result` o `.Wait()` blocca invece il chiamante.

## Le parole da riconoscere

- `task`
- `async`
- `await`
- `try catch`
- `cancellation token`
- `non bloccante`
- `thread pool`

## Anatomia e Sintassi del Codice

### Anatomia del Modello Asincrono in C#:
1. **`async Task<T>`**: indica un metodo asincrono che restituirà un valore di tipo `T`.
2. **`await`**: sospende il metodo fino al completamento del Task; per operazioni I/O asincrone non tiene un thread occupato solo per aspettare.
3. **`try / catch / finally`**: intercetta eventuali eccezioni sollevate durante l'operazione asincrona.

```csharp
public class DataFetcher(HttpClient client) {
  public async Task<string> DownloadContentAsync(string url, CancellationToken ct) {
    try {
        return await client.GetStringAsync(url, ct);
    } catch (HttpRequestException ex) {
        throw new InvalidOperationException("Impossibile scaricare il contenuto.", ex);
    }
  }
}
```

In un'app ASP.NET Core configura il client con `IHttpClientFactory` e iniettalo, invece di creare un nuovo `HttpClient` per ogni richiesta.

Nei flussi asincroni usa `await` fino al chiamante. `.Result` e `.Wait()` bloccano il thread: sotto carico possono esaurire il thread pool. Il deadlock dipende dal contesto di sincronizzazione; ASP.NET Core non usa quello delle vecchie applicazioni ASP.NET.

## Un esempio concreto

```csharp
public async Task<string> FetchDataAsync(int id, CancellationToken ct = default)
{
    try {
        await Task.Delay(50, ct);
        return $"Dati per {id}";
    } catch (Exception ex) {
        Console.Error.WriteLine(ex.Message);
        throw;
    }
}
```

### Seguilo passo per passo

1. `FetchDataAsync` restituisce un `Task<string>`: il chiamante riceve un'operazione da attendere, non una stringa immediata.
2. `await Task.Delay(50, ct)` sospende quel metodo fino al completamento o alla cancellazione; non blocca il thread con `.Wait()`.
3. Se il ritardo termina, il metodo restituisce `Dati per {id}`. Se il token annulla l'operazione, si verifica `OperationCanceledException`, che va trattata come cancellazione attesa.
4. Chiama il metodo con un token già annullato e poi con uno attivo. Distingui la cancellazione dagli errori imprevisti invece di catturare ogni eccezione come se fosse un successo.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
using System.Threading.Tasks;

public static class AsyncDataService {
    public static async Task<string> GetUserGreetingAsync(string name) {
        await Task.Delay(10);
        return $"Benvenuto, {name}!";
    }
}
```

## Dove ci si confonde spesso

- Usare `.Result` o `.Wait()` che possono causare deadlock bloccando il thread
- usare `async void` anziché `async Task` (consentito solo per eventi UI).

## Domanda di verifica

> Perché `async/await` è fondamentale per la scalabilità di un server web come ASP.NET Core?
