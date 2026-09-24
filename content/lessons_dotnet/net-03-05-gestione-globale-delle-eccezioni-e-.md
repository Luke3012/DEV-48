# Gestione globale delle eccezioni e Logging strutturato

## In parole semplici

L'obiettivo di questa lezione è intercettare crash imprevisti e produrre log strutturati con ILogger.

Una gestione centralizzata delle eccezioni impedisce la fuga di dettagli sensibili di implementazione (stack trace) verso il client, registrando i dettagli nei log del server.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `eccezioni globali`
- `useexceptionhandler`
- `ilogger`
- `serilog`
- `problem details 500`
- `telemetria`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`eccezioni globali`, `useexceptionhandler`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class LogMessageFormatter {
    public static string FormatError(string operation, string error) =>
        $"[ERROR] Operazione '{operation}' fallita: {error}";
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Mostrare lo stack trace C# grezzo al browser in ambiente di produzione (grave falla di sicurezza)
- usare string interpolation in ILogger perdendo la struttura dei dati.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché non si deve mai mostrare il messaggio completo di un'eccezione interna nel client Angular?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
