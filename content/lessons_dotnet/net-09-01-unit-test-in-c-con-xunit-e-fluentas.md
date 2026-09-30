# Test unitari in C# con xUnit

Un metodo di servizio contiene una regola che deve restare vera quando il codice cambia. Un test unitario prepara dipendenze controllabili, invoca una sola operazione e confronta il risultato; quando la domanda riguarda invece routing, binding e status HTTP, serve una prova d'integrazione che avvii la pipeline.

## Il comportamento che vogliamo proteggere

### Un test unitario di servizio
```csharp
using System.Collections.Generic;
using System.Linq;

public sealed record OrderLine(int Price, int Quantity);

public sealed class OrderTotalService
{
    public int Calculate(IEnumerable<OrderLine> lines) =>
        lines.Sum(line => line.Price * line.Quantity);
}
```

```csharp
using Xunit;

public sealed class OrderTotalServiceTests
{
    [Theory]
    [InlineData(10, 2, 20)]
    [InlineData(0, 3, 0)]
    public void Calculate_ReturnsTheSum(int price, int quantity, int expected)
    {
        // Arrange
        var service = new OrderTotalService();
        var lines = new[] { new OrderLine(price, quantity) };

        // Act
        var total = service.Calculate(lines);

        // Assert
        Assert.Equal(expected, total);
    }
}
```

`[Fact]` rappresenta un caso nominato; `[Theory]` ripete la stessa regola con più righe di dati. Arrange prepara, Act esegue, Assert verifica: se l'asserzione fallisce, il test indica quale comportamento è cambiato.

### Una prova d'integrazione per la pipeline HTTP
Per verificare che l'endpoint trasformi davvero una richiesta in `404`, il progetto di test può usare `Microsoft.AspNetCore.Mvc.Testing` e `WebApplicationFactory<Program>`. Dalla cartella `tests/` aggiungi il pacchetto e un riferimento al progetto API:
```powershell
dotnet add package Microsoft.AspNetCore.Mvc.Testing --version 10.0.12
dotnet add reference ../server/Server.csproj
```
Con le istruzioni top-level, rendi accessibile il punto d'ingresso aggiungendo questa riga alla fine di `server/Program.cs`:
```csharp
public partial class Program { }
```

Il codice seguente va invece in `tests/SubjectEndpointTests.cs`:
```csharp
using System.Net;
using System.Net.Http;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

public sealed class SubjectEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient client;
    public SubjectEndpointTests(WebApplicationFactory<Program> factory) => client = factory.CreateClient();

    [Fact]
    public async Task MissingSubject_ReturnsNotFound()
    {
        // Arrange: il client punta all'host di test in memoria.
        // Act
        var response = await client.GetAsync("/api/subjects/999");
        // Assert
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}
```

Un test unitario non apre un server e può usare dipendenze controllabili; il test d'integrazione esegue routing, binding, middleware e endpoint in un host di test. Se l'endpoint usa un database, sostituiscilo con un archivio isolato per il test. Usa la prova più piccola che risponde alla domanda e aggiungi la persistenza solo quando è parte del comportamento da verificare.

## Prepara, esegui, osserva

```csharp
var total = new OrderTotalService().Calculate(new[] { new OrderLine(10, 2) });
Assert.Equal(20, total);
```

### Rendi riproducibile il comportamento

1. Arrange crea il servizio e una riga con prezzo `10` e quantità `2`.
2. Act chiama `Calculate` una volta; il metodo moltiplica prezzo e quantità e restituisce `20`.
3. Assert confronta il risultato con l'atteso. Se un difetto restituisce `10`, il test fallisce mostrando atteso ed effettivo.
4. La seconda riga della Theory copre quantità con prezzo zero. Per l'endpoint, invia invece una vera GET a `WebApplicationFactory` e verifica status e body senza dipendere da una porta locale.

La pratica breve del laboratorio inizia da un caso limite che fallisce. Correggi il metodo senza cambiare l'atteso; poi aggiungi una prova d'integrazione solo per i comportamenti che attraversano davvero la pipeline ASP.NET Core.

## Che cosa rende il difetto osservabile?

- Scrivere test che dipendono dal database reale o dalla rete (rallentano la suite e falliscono a intermittenza)
- inserire troppe verifiche non correlate nello stesso test.

> **Quale evidenza dimostra il comportamento?** Qual è la differenza fondamentale tra l'attributo `[Fact]` e `[Theory]` in xUnit?
