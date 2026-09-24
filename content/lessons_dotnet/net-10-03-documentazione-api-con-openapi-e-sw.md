# Documentazione delle API con OpenAPI

## In parole semplici

L'obiettivo di questa lezione è esporre un documento OpenAPI generato da ASP.NET Core e aggiungere metadati alle rotte.

OpenAPI descrive in modo leggibile da strumenti il contratto di un'API. In .NET 10 `AddOpenApi()` registra il generatore e `MapOpenApi()` espone il documento JSON; un'interfaccia web come Swagger UI o Scalar è un pacchetto aggiuntivo.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `openapi`
- `documento json`
- `addopenapi`
- `mapopenapi`
- `documentazione api`
- `route metadata`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`openapi`, `documento json`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Generare il documento OpenAPI in una Minimal API .NET 10:
Nel progetto aggiungi il pacchetto di generazione:
```powershell
dotnet add package Microsoft.AspNetCore.OpenApi --version 10.0.12
```

```csharp
builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment()) {
    app.MapOpenApi(); // In .NET 10 espone /openapi/v1.json
}
```

Gli endpoint possono essere arricchiti con nome, descrizione e tag:
```csharp
app.MapGet("/api/users", () => Results.Ok(new[] { "Ada", "Luca" }))
   .WithName("ListUsers")
   .WithTags("Utenti")
   .WithSummary("Restituisce l'elenco di tutti gli utenti registrati");
```

Per provare il documento con un'interfaccia web, scegli e installa una UI separata. La UI legge lo stesso documento OpenAPI e non sostituisce i test degli endpoint.

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```csharp
app.MapGet("/api/items", () => Results.Ok())
   .WithTags("Catalogo")
   .WithSummary("Recupera tutti gli articoli");
```

### Seguilo passo per passo

1. `AddOpenApi()` registra il servizio che genera il documento; `MapOpenApi()` pubblica il documento JSON, normalmente su `/openapi/v1.json`.
2. `WithTags` organizza gli endpoint e `WithSummary` aggiunge una descrizione leggibile a strumenti e persone.
3. L'interfaccia web come Swagger UI o Scalar è un pacchetto separato: il documento OpenAPI può esistere anche senza una UI interattiva.
4. Avvia l'API, apri il documento e verifica che rotta, metodo e risposta corrispondano al codice. Non inserire dati segreti nella documentazione pubblica.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class OpenApiDocHelper {
    public static string FormatEndpointTitle(string tag, string summary) => $"[{tag.Trim()}] {summary.Trim()}";
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Non inserire descrizioni o status code attesi negli endpoint rendendo la documentazione poco utile per chi sviluppa il frontend.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quali ruoli svolgono `AddOpenApi()` e `MapOpenApi()`, e perché l'interfaccia web è un elemento separato?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
