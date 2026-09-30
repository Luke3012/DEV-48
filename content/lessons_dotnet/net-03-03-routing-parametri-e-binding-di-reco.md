# Routing, Parametri e Binding di Record DTO

Il browser invia byte, header, percorso e query string; il gestore .NET lavora invece con valori C# tipizzati. Il model binding collega questi due lati e i DTO definiscono la forma ammessa dei dati in ingresso e in uscita.

## La richiesta che dobbiamo servire

### Dal JSON alla risposta
La richiesta `GET` usa path e query string come fonti distinte:
```text
GET /api/products/4?category=books
                 └ id dalla route; category dalla query
```

Per creare un utente, il body JSON diventa un record C#. L'API costruisce un DTO pubblico invece di restituire l'entity persistita:
```json
{ "name": "Anna", "email": "anna@example.com" }
```

In `Program.cs`, il parametro `CreateUserRequest` viene costruito dal body JSON. Questo estratto mostra il binding e la forma della risposta; la lezione successiva aggiunge la validazione:
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/api/products/{id:int}", (int id, string? category) =>
    Results.Ok(new { id, category }));

app.MapPost("/api/users", (CreateUserRequest request) =>
{
    var response = new UserResponse(Guid.NewGuid(), request.Name.Trim(), request.Email.Trim());
    return Results.Created($"/api/users/{response.Id}", response);
});
app.Run();

public record CreateUserRequest(string Name, string Email);
public record UserResponse(Guid Id, string Name, string Email);
```

L'entity del database può contenere chiavi interne o proprietà di audit che non devono essere restituite. Il DTO rende visibile il contratto HTTP e permette al modello persistito di evolvere separatamente. Questo handler assume valori validi e non scrive ancora su un database: fra binding e creazione serve una validazione, che vedrai subito dopo.

## Segui la richiesta attraverso il server

```csharp
app.MapGet("/api/products/{id:int}", (int id, string? category) =>
    Results.Ok(new { id, category }));
```

### Segui la richiesta con valori concreti

1. In `/api/products/4?category=books`, il routing applica il vincolo `int` e assegna `4` a `id`; `category` arriva invece dalla query.
2. Per la POST, il browser serializza il body in JSON. Il model binder deserializza `name` ed `email` nel record `CreateUserRequest`.
3. Il route handler usa quei valori per costruire `UserResponse`, che contiene soltanto i dati scelti per il client; non espone direttamente la forma interna di un'entity.
4. `Results.Created` serializza il DTO e restituisce `201` con il percorso della risorsa. Qui i dati sono dimostrativi: prima di persisterli, la prossima lezione aggiungerà una decisione di validazione.

La pratica breve verifica una trasformazione pura. Nel laboratorio Minimal API costruisci endpoint reali e aggiungi casi HTTP per DTO validi, non validi e risorsa assente.

## Leggi il sintomo prima di cambiare codice

- Dimenticare di definire vincoli di rotta (`{id:int}`) consentendo l'invio di stringhe arbitrarie
- non validare i campi del DTO.

> **Racconta il percorso fino alla risposta** In che modo Minimal API distingue se un parametro deve essere letto dalla rotta, dalla query string o dal body JSON?
