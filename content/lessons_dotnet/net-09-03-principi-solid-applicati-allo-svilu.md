# Principi SOLID applicati allo sviluppo Full-Stack

Una rotta che valida, interroga EF Core, calcola lo sconto e invia email può funzionare finché nessun requisito cambia. Quando la regola dello sconto cambia, il database o il provider email può far fallire la stessa classe per motivi indipendenti: SOLID aiuta a individuare questi accoppiamenti e a scioglierli dove dà un beneficio concreto.

## Il comportamento che vogliamo proteggere

### Prima: una classe con troppe ragioni per cambiare
```csharp
public sealed class OrderEndpoint(AppDbContext db, IEmailSender email)
{
    public async Task<IResult> Create(CreateOrderRequest request, CancellationToken ct)
    {
        if (request.Lines.Count == 0) return Results.BadRequest();
        var total = request.Lines.Sum(line => line.Price * line.Quantity);
        var order = new Order { Total = total };
        db.Orders.Add(order);
        await db.SaveChangesAsync(ct);
        await email.SendAsync(request.Email, $"Ordine {order.Id} creato", ct);
        return Results.Created($"/api/orders/{order.Id}", new OrderResponse(order.Id, total));
    }
}
```

Questa classe conosce trasporto HTTP, validazione, calcolo, EF Core, email e risposta. Una modifica al contratto HTTP o al provider di email tocca lo stesso flusso, e per testare il totale serve costruire dipendenze non pertinenti.

### Dopo: le dipendenze seguono le responsabilità
```text
POST endpoint → RegisterOrder (caso d'uso)
                  ├─ IOrderRepository
                  ├─ IDiscountPolicy
                  └─ INotificationSender
Infrastructure implementa le interfacce con EF Core e il provider email
```

Ora il caso d'uso coordina la regola; il repository persiste e il sender notifica. Una nuova policy implementa `IDiscountPolicy` senza infilare un altro ramo nella rotta. Per un'applicazione piccola puoi mantenere i tipi nello stesso progetto e separare solo le responsabilità che hanno motivi reali per cambiare.

## Prepara, esegui, osserva

```csharp
public interface IDiscountStrategy { decimal Apply(decimal price); }
public sealed class HalfPriceDiscount : IDiscountStrategy { public decimal Apply(decimal price) => price * 0.5m; }
```

### Rendi riproducibile il comportamento

1. Nell'endpoint iniziale una richiesta HTTP attiva validazione, calcolo, accesso al database, email e serializzazione.
2. SRP separa le responsabilità che cambiano per ragioni diverse; non significa creare una classe per ogni riga.
3. OCP e DIP emergono quando la rotta dipende da un contratto e una nuova policy può sostituire l'implementazione senza modificare il chiamante.
4. Prima di estrarre un layer, chiedi quale variazione o test diventerebbe più semplice. Verifica che un sostituto rispetti davvero lo stesso comportamento: è la parte pratica di Liskov.

La pratica chiede una strategia di sconto intercambiabile. Nel laboratorio portfolio applica la separazione soltanto dove endpoint, regole e infrastruttura oggi si ostacolano nei test o nelle modifiche.

## Che cosa rende il difetto osservabile?

- Creare 'God Objects' (classi monolitiche con migliaia di righe che fanno tutto: routing, DB, validazione e UI)
- violare il principio di inversione delle dipendenze istanziando direttamente classi concrete.

> **Quale evidenza dimostra il comportamento?** Quale principio SOLID viene violato quando una classe esegue contemporaneamente calcoli di business e interrogazioni dirette al database?
