# Minimal API da zero: Program.cs e WebApplication

## In parole semplici

L'obiettivo di questa lezione è creare endpoint RESTful con Minimal API in C# e .NET 10.

Minimal API permette di dichiarare endpoint HTTP con poco codice di contorno. Controller e Minimal API sono entrambi adatti a progetti reali; la sintassi scelta, da sola, non determina il throughput dell'applicazione.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `minimal api`
- `webapplication`
- `mapget`
- `mappost`
- `program.cs`
- `status codes`
- `typedresults`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`minimal api`, `webapplication`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Anatomia di un'applicazione Minimal API in Program.cs:
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/api/health", () => Results.Ok(new { status = "Healthy" }));
app.MapGet("/api/users/{id:int}", (int id) => Results.Ok(new { Id = id }));
app.Run();
```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/api/hello", () => Results.Ok(new { message = "Ciao da .NET!" }));
app.Run();
```

### Seguilo passo per passo

1. `WebApplication.CreateBuilder(args)` prepara configurazione e servizi; `Build()` produce l'applicazione che riceverà le richieste.
2. `MapGet` associa una richiesta GET su `/api/hello` a una funzione che restituisce un risultato HTTP con un oggetto JSON.
3. `Run()` avvia il server e mantiene il processo in ascolto. La porta effettiva dipende dalla configurazione di avvio.
4. Apri l'URL completo riportato dal terminale e prova un percorso diverso. Confronta la risposta con la rotta registrata.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class RouteRegistry {
    public static string HealthCheck() => "Healthy";
    public static int GetStatusCode(bool success) => success ? 200 : 400;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Confondere la registrazione dei servizi (`builder.Services`) con la configurazione della pipeline (`app.Use...`)
- pensare che Minimal API o TypedResults siano obbligatori per ogni progetto.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quali criteri, oltre alla quantità di codice, useresti per scegliere tra Minimal API e Controller?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
