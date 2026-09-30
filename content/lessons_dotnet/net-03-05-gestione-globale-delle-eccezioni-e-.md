# Gestione globale delle eccezioni e Logging strutturato

Una richiesta non passa direttamente dall'URL alla lambda. I middleware formano una pipeline: ciascuno può preparare la richiesta, chiamare il passaggio successivo e osservare la risposta mentre questa risale. Per questo l'ordine cambia il comportamento.

## La richiesta che dobbiamo servire

### La pipeline e il percorso di ritorno
```text
Request
  ↓
Exception handler
  ↓
Logging: prima di next
  ↓
Routing / endpoint
  ↑
Logging: dopo next
  ↑
Response
```

In `Program.cs`, registra prima il gestore che deve poter intercettare gli errori successivi. Questo middleware minimo rende visibile il lavoro prima e dopo `next`:
```csharp
var app = builder.Build();
var logger = app.Logger;

app.UseExceptionHandler(errorApp => errorApp.Run(async context =>
{
    context.Response.StatusCode = StatusCodes.Status500InternalServerError;
    await context.Response.WriteAsJsonAsync(new { title = "Errore interno", status = 500 });
}));

app.Use(async (context, next) =>
{
    logger.LogInformation("Inizio {Method} {Path}", context.Request.Method, context.Request.Path);
    await next(context);
    logger.LogInformation("Fine richiesta con {StatusCode}", context.Response.StatusCode);
});

app.MapGet("/api/failure", () => throw new InvalidOperationException("Dettaglio solo server"));
```

Il gestore delle eccezioni è esterno al middleware di logging, così può trasformare un errore non gestito in una risposta pubblica controllata. Il messaggio dettagliato resta nei log del server; non includere stack trace o dati sensibili nel body.

## Segui la richiesta attraverso il server

```text
logger.LogInformation("Ordine {OrderId} creato per {UserId}", orderId, userId);
```

### Segui la richiesta con valori concreti

1. La richiesta attraversa `UseExceptionHandler` e poi il middleware di logging dall'alto verso il basso.
2. Il logging scrive l'evento iniziale e `await next(context)` passa il controllo alla route.
3. Dopo l'endpoint, il controllo torna al middleware: viene registrato lo status della risposta. Se il downstream lancia, il gestore esterno converte l'eccezione in un `500`.
4. Prova una route che riesce e una che fallisce. I log strutturati conservano i campi `{Method}`, `{Path}` e `{StatusCode}` separati dal testo del messaggio.

La pratica breve controlla la formattazione dei campi. Nel server del laboratorio aggiungi log al percorso reale e verifica che una risposta 500 non riveli l'eccezione al client.

## Leggi il sintomo prima di cambiare codice

- Mostrare lo stack trace C# grezzo al browser in ambiente di produzione (grave falla di sicurezza)
- usare string interpolation in ILogger perdendo la struttura dei dati.

> **Racconta il percorso fino alla risposta** Perché non si deve mai mostrare il messaggio completo di un'eccezione interna nel client Angular?
