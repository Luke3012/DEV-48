# Programmazione Asincrona: Task, async/await ed Eccezioni

Quando il server attende una risposta dal database o da un servizio HTTP, il risultato non è disponibile subito. L'obiettivo dell'asincronia è rappresentare quell'attesa senza tenere occupato il thread soltanto per aspettare: non significa avviare automaticamente un nuovo thread né eseguire il calcolo più in fretta.

## Dal problema alla regola del linguaggio

### Una chiamata I/O e il valore che arriva dopo
```csharp
using System.Net;
using System.Net.Http.Json;

public sealed class UserClient(HttpClient http)
{
    public async Task<UserDto?> GetUserAsync(int id, CancellationToken cancellationToken)
    {
        using var response = await http.GetAsync($"/api/users/{id}", cancellationToken);
        if (response.StatusCode == HttpStatusCode.NotFound) return null;
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<UserDto>(cancellationToken);
    }
}

public sealed record UserDto(int Id, string Name);
```

`Task<UserDto?>` rappresenta un'operazione futura il cui risultato può essere un utente o `null`; non contiene già l'utente. `await` restituisce il controllo al chiamante mentre l'I/O è in corso e riprende il metodo quando la risposta arriva. Nei progetti ASP.NET Core configura `HttpClient` con `IHttpClientFactory` e passa il `CancellationToken` della richiesta quando è disponibile.

Un metodo asincrono che fa soltanto calcolo CPU-bound non diventa non bloccante grazie alla parola `async`. Il parallelismo è un tema separato: più operazioni possono sovrapporsi, ma `await` da solo non le avvia tutte.

## Traccia i valori nel programma

```csharp
Task<string> pending = httpClient.GetStringAsync(url, cancellationToken);
string body = await pending;
```

### Calcola il risultato prima di eseguirlo

1. La chiamata HTTP restituisce un `Task<string>` che rappresenta la risposta ancora attesa; il server non ha già ricevuto il testo.
2. `await` sospende questa continuazione. Durante l'attesa I/O il thread può servire altro lavoro, invece di restare bloccato su `.Wait()`.
3. Se la rete risponde, `body` riceve il testo. Se il token annulla l'operazione o la rete fallisce, l'attesa propaga un'eccezione al chiamante.
4. Gestisci `OperationCanceledException` come cancellazione quando è quella richiesta e registra gli errori inattesi al confine appropriato. Non trasformare ogni errore in un risultato vuoto.

L'esercizio breve restituisce un `Task` per farti osservare il contratto; nel laboratorio e negli endpoint del corso segui `await` fino al chiamante e passa la cancellazione quando l'operazione dipende dalla richiesta HTTP.

## Casi che cambiano il risultato

- Usare `.Result` o `.Wait()` che possono causare deadlock bloccando il thread
- usare `async void` anziché `async Task` (consentito solo per eventi UI).

> **Che cosa succede se cambia l'input?** Perché `async/await` è fondamentale per la scalabilità di un server web come ASP.NET Core?
