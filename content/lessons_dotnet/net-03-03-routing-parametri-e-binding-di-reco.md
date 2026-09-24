# Routing, Parametri e Binding di Record DTO

## In parole semplici

L'obiettivo di questa lezione è raccogliere dati da route, query string, header e body JSON mappandoli in record C#.

ASP.NET Core associa automaticamente i dati della richiesta HTTP ai parametri della lambda o dell'action tramite model binding trasparente.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `routing`
- `route parameters`
- `query string`
- `request body`
- `dto`
- `frombody`
- `fromquery`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`routing`, `route parameters`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public record CreateProductDto(string Name, decimal Price);
public static class ProductValidator {
    public static bool IsValid(CreateProductDto dto) =>
        !string.IsNullOrWhiteSpace(dto.Name) && dto.Price > 0;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare di definire vincoli di rotta (`{id:int}`) consentendo l'invio di stringhe arbitrarie
- non validare i campi del DTO.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> In che modo Minimal API distingue se un parametro deve essere letto dalla rotta, dalla query string o dal body JSON?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
