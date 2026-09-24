# Test unitari in C# con xUnit

## In parole semplici

L'obiettivo di questa lezione è scrivere test unitari affidabili e manutenibili per i servizi e la logica di business .NET.

I test unitari verificano che singoli metodi o componenti producano il risultato atteso per diversi input, proteggendo il codice da regressioni durante i refactoring.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `xunit`
- `[fact]`
- `[theory]`
- `assert`
- `arrange act assert`
- `red green refactor`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`xunit`, `[fact]`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Il Pattern Arrange - Act - Assert (AAA):
Ogni test professionale segue 3 fasi distinte:
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
    [InlineData(0, true)]
    [InlineData(-5, false)]
    public void IsPositive_VariousInputs_ReturnsExpected(int number, bool expected) {
        var calc = new Calculator();
        Assert.Equal(expected, calc.IsPositive(number));
    }
}
```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```csharp
[Fact]
public void Calculate_ValidInput_ReturnsExpected() {
    var result = Service.Process(5);
    Assert.Equal(10, result);
}
```

### Seguilo passo per passo

1. Nella fase Arrange prepara l'input `5` e il servizio; non introdurre database o rete in un test unitario semplice.
2. La fase Act chiama `Service.Process(5)` una sola volta e conserva il risultato.
3. `Assert.Equal(10, result)` confronta il comportamento osservato con il valore atteso. Se il metodo restituisce un altro numero, xUnit indica il test fallito.
4. Prova un input limite con una seconda `[Theory]` o un altro `[Fact]`. Mantieni un solo comportamento principale per test, così un errore resta facile da diagnosticare.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class TestEvaluationHelper {
    public static bool EvaluateAssertion(int actual, int expected) => actual == expected;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Scrivere test che dipendono dal database reale o dalla rete (rallentano la suite e falliscono a intermittenza)
- inserire troppe verifiche non correlate nello stesso test.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è la differenza fondamentale tra l'attributo `[Fact]` e `[Theory]` in xUnit?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
