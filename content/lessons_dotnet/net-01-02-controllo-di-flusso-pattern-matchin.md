# Controllo di flusso, Pattern Matching e Switch Expressions

## In parole semplici

L'obiettivo di questa lezione è scrivere diramazioni logiche eleganti e sicure usando le nuove switch expressions di C#.

Una switch expression confronta un valore con più pattern e restituisce il risultato del primo ramo corrispondente; il ramo `_` fornisce il caso restante. Se nessun ramo corrisponde, a runtime viene sollevata un'eccezione.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `switch expression`
- `pattern matching`
- `is`
- `when`
- `guard condition`
- `discard`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`switch expression`, `pattern matching`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Sintassi della Switch Expression in C# 12:
```csharp
var risultato = espressione switch {
    pattern1 => valore1,
    pattern2 when condizione_guardia => valore2,
    _ => valore_default // Discard obbligatorio per esaustività
};
```

### Tipologie di Pattern Matching:
1. **Constant pattern**: `"admin" => ...`
2. **Relational pattern**: `> 100 and <= 500 => ...`
3. **Type pattern**: `string s => s.ToUpper()`
4. **Positional / Tuple pattern**: `(var role, true) => ...`
5. **Property pattern**: `{ Status: "Active", Age: >= 18 } => ...`

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

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

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Usare cascate di if/else annidati illeggibili
- dimenticare il ramo di scarto `_` (discard) provocando eccezioni a runtime.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quale vantaggio offre una switch expression rispetto a un blocco switch classico imperativo?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
