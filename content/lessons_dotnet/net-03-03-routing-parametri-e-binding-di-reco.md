# Routing, Parametri e Binding di Record DTO

## In parole semplici

L'obiettivo di questa lezione è raccogliere dati da route, query string, header e body JSON mappandoli in record C#.

ASP.NET Core associa automaticamente i dati della richiesta HTTP ai parametri della lambda o dell'action tramite model binding trasparente.

## Le parole da riconoscere

- `routing`
- `route parameters`
- `query string`
- `request body`
- `dto`
- `frombody`
- `fromquery`

## Anatomia e Sintassi del Codice

### Origini di Binding in Minimal API:
- **Route param**: `app.MapGet("/items/{id:int}", (int id) => ...)`
- **Query param**: `app.MapGet("/items", (string? search) => ...)`
- **Body JSON**: `app.MapPost("/items", (CreateItemDto dto) => ...)`
- **Servizi DI**: `app.MapGet("/items", (IItemService service) => ...)`

```csharp
public record CreateUserRequest(string Email, string Name);
public record UserResponse(int Id, string Email, string Name);

app.MapPost("/api/users", (CreateUserRequest req) => {
    var user = new UserResponse(1, req.Email, req.Name);
    return Results.Created($"/api/users/{user.Id}", user);
});
```

## Un esempio concreto

```csharp
app.MapGet("/api/products/{id:int}", (int id, string? category) => {
    return Results.Ok(new { id, category });
});
```

### Seguilo passo per passo

1. La rotta `/api/products/{id:int}` accetta un segmento numerico come `id`; `/api/products/abc` non soddisfa il vincolo.
2. `category` può arrivare dalla query string, ad esempio `/api/products/4?category=books`; il binding associa i valori ai parametri del gestore.
3. `Results.Ok` restituisce status 200 e un JSON con `id` e `category`. Un endpoint POST può invece ricevere un DTO dal body.
4. Prova a omettere `category`, poi invia un `id` non numerico. Osserva come cambia il binding e non confondere l'estrazione dei valori con la loro validazione.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```csharp
public record CreateProductDto(string Name, decimal Price);
public static class ProductValidator {
    public static bool IsValid(CreateProductDto dto) =>
        !string.IsNullOrWhiteSpace(dto.Name) && dto.Price > 0;
}
```

## Dove ci si confonde spesso

- Dimenticare di definire vincoli di rotta (`{id:int}`) consentendo l'invio di stringhe arbitrarie
- non validare i campi del DTO.

## Domanda di verifica

> In che modo Minimal API distingue se un parametro deve essere letto dalla rotta, dalla query string o dal body JSON?
