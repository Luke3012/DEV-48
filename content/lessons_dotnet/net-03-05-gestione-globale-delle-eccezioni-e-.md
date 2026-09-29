# Gestione globale delle eccezioni e Logging strutturato

## In parole semplici

L'obiettivo di questa lezione è intercettare crash imprevisti e produrre log strutturati con ILogger.

Una gestione centralizzata delle eccezioni impedisce la fuga di dettagli sensibili di implementazione (stack trace) verso il client, registrando i dettagli nei log del server.

## Le parole da riconoscere

- `eccezioni globali`
- `useexceptionhandler`
- `ilogger`
- `serilog`
- `problem details 500`
- `telemetria`

## Anatomia e Sintassi del Codice

### Middleware Globale per le Eccezioni:
In ASP.NET Core 10 `UseExceptionHandler()` può restituire un Problem Details con status code 500:
```csharp
app.UseExceptionHandler(exceptionHandlerApp => {
    exceptionHandlerApp.Run(async context => {
        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        context.Response.ContentType = "application/problem+json";
        var problem = new {
            Type = "https://tools.ietf.org/html/rfc7231#section-6.6.1",
            Title = "Si è verificato un errore interno.",
            Status = 500
        };
        await context.Response.WriteAsJsonAsync(problem);
    });
});
```

### Logging Strutturato:
Evita la concatenazione di stringhe nei log; usa i segnaposto nominati per permettere a tool come Seq o Elastic di indicizzare i parametri:
```csharp
logger.LogInformation("Ordine {OrderId} creato con successo per l'utente {UserId}", orderId, userId);
```

## Un esempio concreto

```text
app.UseExceptionHandler("/error");
logger.LogInformation("Elaborazione richiesta per utente {UserId}", userId);
```

### Seguilo passo per passo

1. `UseExceptionHandler` registra il gestore che intercetta eccezioni non gestite nella pipeline; la sua posizione rispetto agli endpoint determina quali richieste copre.
2. `LogInformation` riceve un modello con `{UserId}` e il valore separato: il provider conserva un campo strutturato, utile per filtrare i log.
3. Un errore atteso di input va rappresentato con una risposta appropriata; il gestore globale è per errori imprevisti e non dovrebbe esporre lo stack trace al client.
4. Sostituisci il placeholder `{UserId}` con interpolazione e confronta il messaggio: la versione strutturata conserva meglio i campi interrogabili.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```csharp
public static class LogMessageFormatter {
    public static string FormatError(string operation, string error) =>
        $"[ERROR] Operazione '{operation}' fallita: {error}";
}
```

## Dove ci si confonde spesso

- Mostrare lo stack trace C# grezzo al browser in ambiente di produzione (grave falla di sicurezza)
- usare string interpolation in ILogger perdendo la struttura dei dati.

## Domanda di verifica

> Perché non si deve mai mostrare il messaggio completo di un'eccezione interna nel client Angular?
