# Controllo di flusso, Pattern Matching e Switch Expressions

Un programma deve scegliere una risposta in base allo stato di un dato. Con pochi casi un `if` è chiaro; quando le condizioni descrivono forme e proprietà di un oggetto, i pattern di C# rendono esplicito che cosa si sta confrontando e fanno restituire il risultato direttamente.

## Una decisione diventa un valore

### Dalla condizione al caso dell'ordine
Per una stringa semplice si può partire con condizioni in sequenza:
```csharp
public static class StatusLabels
{
    public static string DescribeStatus(string status)
    {
        if (status == "open") return "Da gestire";
        if (status == "closed") return "Completato";
        return "Stato non riconosciuto";
    }
}
```

Quando la decisione dipende da più proprietà, una switch expression confronta il valore in un solo punto:
```csharp
public sealed record ServiceTicket(string Status, int DaysWaiting);

public static class TicketLabels
{
    public static string Describe(ServiceTicket ticket) => ticket switch
    {
        { Status: "open", DaysWaiting: >= 3 } => "In ritardo",
        { Status: "open" } => "In attesa",
        { Status: "closed" } => "Completato",
        _ => "Stato non riconosciuto"
    };
}
```

`{ Status: "open" }` è un property pattern; `DaysWaiting: >= 3` aggiunge un relational pattern. `_` copre i valori che non corrispondono ai casi precedenti. L'ordine è leggibile: prima l'ordine aperto in ritardo, poi il caso aperto generale. Se il caso generale fosse sopra, nasconderebbe quello più specifico.

Una switch expression produce un valore, quindi si adatta a etichette e classificazioni. Un normale `switch` resta adatto quando i rami eseguono più istruzioni. Non serve elencare ogni forma di pattern prima di saper seguire una decisione concreta.

## Quale pattern corrisponde per primo?

```csharp
TicketLabels.Describe(new ServiceTicket("open", 5)) // "In ritardo"
```

### Calcola il risultato prima di eseguirlo

1. Crea `ServiceTicket("open", 5)`: il primo pattern controlla contemporaneamente lo stato e i giorni di attesa.
2. Entrambe le condizioni sono vere, quindi il risultato è `"In ritardo"`; C# non prova i rami successivi.
3. Con `ServiceTicket("open", 1)` il primo caso non corrisponde, mentre `{ Status: "open" }` sì: il risultato è `"In attesa"`.
4. Prova lo stato `"closed"` e un valore nuovo. Segui il ramo specifico e poi il caso `_`; non lasciare una combinazione possibile senza una decisione esplicita.

La pratica breve usa una classificazione di sconti: prova prima una combinazione per volta e poi costruisci i casi. Non copiare lo schema esatto degli stati dell'esempio; nel laboratorio CRUD userai condizioni e validazione su record reali.

## Controlla ordine e copertura dei casi

- Un pattern generale prima di uno specifico rende irraggiungibile il caso dettagliato
- una switch expression senza copertura adeguata può fallire a runtime
- non usare un'espressione se i rami devono svolgere molte operazioni.

> **Quando la decisione può diventare un'espressione?** Quale vantaggio offre una switch expression rispetto a un blocco switch classico imperativo?
