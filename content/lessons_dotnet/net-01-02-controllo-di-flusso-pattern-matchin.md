# Controllo di flusso, Pattern Matching e Switch Expressions

## In parole semplici

L'obiettivo di questa lezione è scrivere diramazioni logiche eleganti e sicure usando le nuove switch expressions di C#.

Una switch expression confronta un valore con più pattern e restituisce il risultato del primo ramo corrispondente; il ramo `_` fornisce il caso restante. Se nessun ramo corrisponde, a runtime viene sollevata un'eccezione.

## Le parole da riconoscere

- `switch expression`
- `pattern matching`
- `is`
- `when`
- `guard condition`
- `discard`

## Anatomia e Sintassi del Codice

### Sintassi della Switch Expression in C# 12:
```csharp
var risultato = espressione switch {
    pattern1 => valore1,
    pattern2 when condizione_guardia => valore2,
    _ => valore_default // Caso restante per i valori non coperti
};
```

### Tipologie di Pattern Matching:
1. **Constant pattern**: `"admin" => ...`
2. **Relational pattern**: `> 100 and <= 500 => ...`
3. **Type pattern**: `string s => s.ToUpper()`
4. **Positional / Tuple pattern**: `(var role, true) => ...`
5. **Property pattern**: `{ Status: "Active", Age: >= 18 } => ...`

## Un esempio concreto

```text
string GetRoleDescription(string role, bool isSuperUser) => (role, isSuperUser) switch
{
    ("admin", true) => "Super Amministratore",
    ("admin", false) => "Amministratore standard",
    ("user", _) => "Utente registrato",
    _ => "Ospite sconosciuto"
};
```

### Seguilo passo per passo

1. Leggi insieme `role` e `isSuperUser`: la switch expression confronta la coppia, non soltanto il primo valore.
2. Il primo ramo applicabile produce la descrizione; per `("admin", true)` il risultato è `"Super Amministratore"`.
3. Il ramo `("user", _)` accetta qualunque secondo valore per l'utente. `_` significa che quel valore non serve alla decisione.
4. Prova una coppia non elencata: controlla se esiste un ramo che la gestisce o se il metodo deve rendere esplicita l'assenza di un caso valido.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
public static class PricingEngine {
    public static decimal CalculateDiscount(decimal amount, bool isPremium) => (amount, isPremium) switch {
        ( >= 500, true) => 0.25m,
        ( >= 500, false) => 0.15m,
        ( >= 100, true) => 0.10m,
        _ => 0.00m
    };
}
```

## Dove ci si confonde spesso

- Usare cascate di if/else annidati illeggibili
- dimenticare il ramo di scarto `_` (discard) provocando eccezioni a runtime.

## Domanda di verifica

> Quale vantaggio offre una switch expression rispetto a un blocco switch classico imperativo?
