# Validazione degli input e ProblemDetails standard

Quando arriva una POST, ASP.NET Core prima deve associare il body JSON a un tipo C#. Solo dopo il route handler può applicare regole del dominio. Separare binding e validazione aiuta a capire perché una richiesta è rifiutata e permette ad Angular di collegare l'errore al campo giusto.

## Dal body JSON alla decisione del server

### Il body diventa un DTO, poi il server decide se accettarlo
Il client invia JSON secondo il contratto stabilito:
```json
{ "email": "ada@example.com", "name": "Ada" }
```

Il parametro complesso `CreateUserRequest` è associato al body. Le regole del gestore controllano i valori prima di qualsiasi scrittura:
```csharp
using System.Collections.Generic;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapPost("/api/users", (CreateUserRequest input) =>
{
    var errors = new Dictionary<string, string[]>();
    if (string.IsNullOrWhiteSpace(input.Email) || !input.Email.Contains('@'))
        errors["Email"] = ["Inserisci un indirizzo email valido."];
    if (string.IsNullOrWhiteSpace(input.Name))
        errors["Name"] = ["Il nome è obbligatorio."];

    if (errors.Count > 0) return Results.ValidationProblem(errors);

    // Il service e il database entreranno nel percorso nelle lezioni successive.
    var created = new UserResponse(42, input.Email, input.Name);
    return Results.Created($"/api/users/{created.Id}", created);
});
app.Run();

public sealed record CreateUserRequest(string Email, string Name);
public sealed record UserResponse(int Id, string Email, string Name);
```

Se una regola fallisce, `ValidationProblem` produce status `400` con un oggetto JSON e una mappa `errors` indicizzata per campo. Per esempio, una richiesta senza email ha una risposta di questa forma:
```json
{
  "status": 400,
  "errors": { "Email": ["Inserisci un indirizzo email valido."] }
}
```
Se la richiesta è accettata, `Created` restituisce `201` e il percorso della risorsa. Il controllo `Contains('@')` è volutamente solo illustrativo: una regola reale deve dichiarare con precisione che cosa accetta, e non può verificare che la casella esista.

Il body malformato o incompatibile col DTO può essere rifiutato durante il binding prima che il gestore venga chiamato. Un errore di validazione applicativa nasce invece dopo il binding: nel browser confronta status e body per distinguere i due casi.

## Segui validazione ed esito HTTP

```csharp
return errors.Count > 0
    ? Results.ValidationProblem(errors)
    : Results.Created($"/api/users/{created.Id}", created);
```

### Una richiesta valida e una da rifiutare

1. Il browser invia JSON; il model binder crea `CreateUserRequest` se nomi e tipi sono compatibili.
2. Il gestore controlla email e nome, accumulando gli errori per campo senza scrivere sul database.
3. Con un errore, `ValidationProblem` restituisce `400` e `errors.Email` o `errors.Name`; con dati accettati, il service potrà salvare e restituire `201 Created`.
4. Quando Angular riceve il `400`, mostra ciascun messaggio vicino al controllo corrispondente. Se il body JSON non può essere associato al record, l'handler potrebbe non partire: usa Network per vedere status e risposta effettivi.

Il mini-runner prova una funzione pura che costruisce il dizionario e non avvia HTTP. Nel laboratorio Minimal API collega la stessa decisione al body JSON reale, verifica status 400/201 e controlla che una richiesta invalida non scriva dati.

## Binding ed errore di campo non sono lo stesso passaggio

- Usare status 200 per un rifiuto rende ambiguo il risultato
- restituire soltanto una stringa impedisce al client di associare il messaggio al campo
- un controllo email elementare non prova che la casella sia valida o raggiungibile.

> **In quale momento il server può ancora evitare la scrittura?** Quale vantaggio offre ValidationProblem al client che deve mostrare errori per campo?
