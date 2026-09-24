# Validazione degli input e ProblemDetails standard

## In parole semplici

L'obiettivo di questa lezione è restituire errori semantici in formato Problem Details (RFC 9457) e mostrare gli errori per campo nel frontend Angular.

Lo standard ProblemDetails standardizza il formato JSON di errore per le API web, consentendo al frontend Angular di mostrare messaggi precisi per ciascun campo non valido.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `problemdetails`
- `rfc 9457`
- `validazione`
- `bad request`
- `400`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`problemdetails`, `rfc 9457`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

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

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Restituire semplici stringhe di testo grezzo in caso di errore invece di una risposta strutturata JSON
- usare status code 200 con messaggi di fallimento nel body.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché è fondamentale che un'API restituisca `ValidationProblem` anziché testo libero?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
