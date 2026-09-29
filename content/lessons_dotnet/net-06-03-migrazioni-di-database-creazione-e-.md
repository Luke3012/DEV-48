# Migrazioni di Database: Creazione e Applicazione

## In parole semplici

L'obiettivo di questa lezione è versionare lo schema del database con codice C# e applicare modifiche senza perdere dati.

Le migrazioni di EF Core consentono di evolvere lo schema del database nel tempo in modo ripetibile e tracciabile nel repository Git.

## Le parole da riconoscere

- `dotnet ef migrations add`
- `dotnet ef database update`
- `versionamento schema`
- `snapshot`

## Anatomia e Sintassi del Codice

### Comandi Fondamentali della CLI `dotnet ef`:
Prima installa gli strumenti una volta e il pacchetto di design nel progetto. Mantieni la stessa major version di EF Core (10 in questo percorso):
```powershell
dotnet tool install --global dotnet-ef --version 10.0.12
dotnet add package Microsoft.EntityFrameworkCore.Design --version 10.0.12
dotnet ef --version
```

1. **Aggiunta migrazione**:
   `dotnet ef migrations add InitialCreate`
   Crea file C# nella cartella `Migrations/` con i metodi `Up()` (applica) e `Down()` (annulla).
2. **Applicazione al database**:
   `dotnet ef database update`
   Confronta lo storico nella tabella `__EFMigrationsHistory` ed esegue solo le migrazioni mancanti.
3. **Rimozione ultima migrazione non applicata**:
   `dotnet ef migrations remove`

### Applicazione automatica all'avvio (solo per sviluppo locale):
```csharp
using var scope = app.Services.CreateScope();
var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
db.Database.Migrate();
```
Usala soltanto per sviluppo locale. Per la produzione pianifica e rivedi l'applicazione delle migrazioni come parte della distribuzione, invece di farle partire automaticamente da ogni istanza dell'app.

## Un esempio concreto

```text
dotnet ef migrations add AddUserTable
dotnet ef database update
# Esamina la migrazione: rimozioni di colonne o tabelle possono perdere dati.
```

### Seguilo passo per passo

1. `dotnet ef migrations add AddUserTable` confronta il modello corrente con lo snapshot e genera una migrazione nominata.
2. Esamina il codice generato e lo snapshot prima di applicarlo: la migrazione descrive come evolve lo schema, non è una copia di backup dei dati.
3. `dotnet ef database update` applica le migrazioni pendenti al database configurato e aggiorna la cronologia delle migrazioni.
4. Aggiungi una proprietà e genera una nuova migrazione. In produzione applica le modifiche con un passaggio di deploy controllato; evita l'applicazione automatica all'avvio.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Modificare manualmente le tabelle del database da un tool esterno disallineando lo snapshot delle migrazioni di EF Core.

## Domanda di verifica

> A cosa serve la tabella interna `__EFMigrationsHistory` creata da EF Core?
