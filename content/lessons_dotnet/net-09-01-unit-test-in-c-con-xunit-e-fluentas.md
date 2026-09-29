# Test unitari in C# con xUnit

## In parole semplici

L'obiettivo di questa lezione è scrivere test unitari affidabili e manutenibili per i servizi e la logica di business .NET.

I test unitari verificano che singoli metodi o componenti producano il risultato atteso per diversi input, proteggendo il codice da regressioni durante i refactoring.

## Le parole da riconoscere

- `xunit`
- `[fact]`
- `[theory]`
- `assert`
- `arrange act assert`
- `red green refactor`

## Anatomia e Sintassi del Codice

### Il Pattern Arrange - Act - Assert (AAA):
Il modello Arrange–Act–Assert rende distinguibili tre responsabilità:
1. **Arrange (Prepara)**: inizializza le variabili, crea gli oggetti e prepara l'ambiente di test.
2. **Act (Esegui)**: invoca il metodo sotto test con i parametri stabiliti.
3. **Assert (Verifica)**: controlla che il valore restituito o lo stato coincida con il risultato atteso.

### Esempio con xUnit:
```csharp
using Xunit;

public class CalculatorTests {
    [Fact]
    public void Add_TwoNumbers_ReturnsCorrectSum() {
        // 1. Arrange
        var calc = new Calculator();

        // 2. Act
        var result = calc.Add(10, 20);

        // 3. Assert
        Assert.Equal(30, result);
    }

    [Theory]
    [InlineData(0, false)]
    [InlineData(-5, false)]
    public void IsPositive_VariousInputs_ReturnsExpected(int number, bool expected) {
        var calc = new Calculator();
        Assert.Equal(expected, calc.IsPositive(number));
    }
}
```

Nel progetto di test aggiungi la classe usata dall’esempio (oppure referenzia il progetto che la contiene):
```csharp
public class Calculator {
    public int Add(int a, int b) => a + b;
    public bool IsPositive(int number) => number > 0;
}
```
Esegui `dotnet test Tests/Server.Tests.csproj` dalla cartella `server/` del laboratorio Suite di Test xUnit e Vitest. Prima fai fallire un test con un difetto controllato, poi correggi il metodo e verifica di nuovo.

## Un esempio concreto

```csharp
using Xunit;

public static class Service {
    public static int Process(int value) => value * 2;
}

public class ServiceTests {
    [Fact]
    public void Calculate_ValidInput_ReturnsExpected() {
        var result = Service.Process(5);
        Assert.Equal(10, result);
    }
}
```

### Seguilo passo per passo

1. Nella fase Arrange prepara l'input `5` e il servizio; non introdurre database o rete in un test unitario semplice.
2. La fase Act chiama `Service.Process(5)` una sola volta e conserva il risultato.
3. `Assert.Equal(10, result)` confronta il comportamento osservato con il valore atteso. Se il metodo restituisce un altro numero, xUnit indica il test fallito.
4. Prova un input limite con una seconda `[Theory]` o un altro `[Fact]`. Mantieni un solo comportamento principale per test, così un errore resta facile da diagnosticare.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Scrivere test che dipendono dal database reale o dalla rete (rallentano la suite e falliscono a intermittenza)
- inserire troppe verifiche non correlate nello stesso test.

## Domanda di verifica

> Qual è la differenza fondamentale tra l'attributo `[Fact]` e `[Theory]` in xUnit?
