# Programmazione Asincrona: Task, async/await ed Eccezioni

## In parole semplici

L'obiettivo di questa lezione è gestire operazioni I/O senza bloccare il thread del server e trattare gli errori con robustezza.

Durante una vera attesa I/O asincrona, `await` sospende il metodo senza bloccare il thread in attesa. Il codice dopo `await` riprende quando il `Task` termina; chiamare `.Result` o `.Wait()` blocca invece il chiamante.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `task`
- `async`
- `await`
- `try catch`
- `cancellation token`
- `non bloccante`
- `thread pool`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`task`, `async`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

> **Regola d'oro**: Non usare mai `.Result` o `.Wait()`, poiché bloccano il thread sincronicamente e possono causare deadlock nei server web!

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
using System.Threading.Tasks;

public static class AsyncDataService {
    public static async Task<string> GetUserGreetingAsync(string name) {
        await Task.Delay(10);
        return $"Benvenuto, {name}!";
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare `.Result` o `.Wait()` che possono causare deadlock bloccando il thread
- usare `async void` anziché `async Task` (consentito solo per eventi UI).

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché `async/await` è fondamentale per la scalabilità di un server web come ASP.NET Core?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
