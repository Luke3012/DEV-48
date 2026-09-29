# Validazione degli input e ProblemDetails standard

## In parole semplici

L'obiettivo di questa lezione è restituire errori semantici in formato Problem Details (RFC 9457) e mostrare gli errori per campo nel frontend Angular.

Lo standard ProblemDetails standardizza il formato JSON di errore per le API web, consentendo al frontend Angular di mostrare messaggi precisi per ciascun campo non valido.

## Le parole da riconoscere

- `problemdetails`
- `rfc 9457`
- `validazione`
- `bad request`
- `400`

## Anatomia e Sintassi del Codice

### Struttura di una risposta Problem Details (RFC 9457):
```json
{
  "type": "about:blank",
  "title": "Richiesta non valida",
  "status": 400,
  "errors": {
    "Email": ["Il campo Email non è un indirizzo valido."],
    "Age": ["L'età minima deve essere 18 anni."]
  }
}
```

### Utilizzo in Minimal API con `Results.ValidationProblem`:
```csharp
var errors = new Dictionary<string, string[]>();
if (string.IsNullOrWhiteSpace(user.Email)) {
    errors["Email"] = ["L'email è obbligatoria."];
}
if (errors.Count > 0) {
    return Results.ValidationProblem(errors);
}
return Results.Ok();
```

## Un esempio concreto

```csharp
var errors = new Dictionary<string, string[]>();
if (string.IsNullOrWhiteSpace(input.Email)) {
    errors["Email"] = new[] { "L'email è obbligatoria." };
    return Results.ValidationProblem(errors);
}
```

### Seguilo passo per passo

1. Il dizionario `errors` parte vuoto. Se `Email` è mancante o composta solo da spazi, il controllo registra un errore associato al campo.
2. `Results.ValidationProblem(errors)` costruisce una risposta di validazione con status 400 e struttura Problem Details.
3. Angular può leggere gli errori del body e mostrarli accanto al campo corrispondente; la risposta deve restare coerente con il contratto documentato.
4. Prova una email presente e una vuota. Per la prima il ramo di errore non deve scattare; per la seconda verifica status e nome del campo nella risposta.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```csharp
using System.Collections.Generic;

public static class ValidationHelper {
    public static Dictionary<string, string[]> ValidateEmail(string? email) {
        var errors = new Dictionary<string, string[]>();
        if (string.IsNullOrWhiteSpace(email) || !email.Contains("@")) {
            errors["Email"] = new[] { "Formato email non valido" };
        }
        return errors;
    }
}
```

## Dove ci si confonde spesso

- Restituire semplici stringhe di testo grezzo in caso di errore invece di una risposta strutturata JSON
- usare status code 200 con messaggi di fallimento nel body.

## Domanda di verifica

> Quale vantaggio offre ValidationProblem al client che deve mostrare errori per campo?
