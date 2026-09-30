# Migrazioni di Database: Creazione e Applicazione

Le migrazioni di EF Core consentono di evolvere lo schema del database nel tempo in modo ripetibile e tracciabile nel repository Git.

## Dall'oggetto C# alla riga del database

### Comandi Fondamentali della CLI `dotnet ef`:
Nel laboratorio, esegui i comandi dalla cartella `server/`: lo starter include un manifest locale con EF Tools 10.0.12. `dotnet restore` prepara il progetto perché il tool possa costruire il `DbContext` al momento del design:
```powershell
dotnet tool restore
dotnet restore
dotnet ef --version
```
Per un progetto nuovo, crea un manifest locale con `dotnet new tool-manifest`, aggiungi `dotnet tool install dotnet-ef --version 10.0.12` e il pacchetto `Microsoft.EntityFrameworkCore.Design` della stessa major version. Un manifest versionato fa usare a tutto il team lo stesso tool, senza installarlo globalmente.

1. **Aggiunta migrazione**:
   `dotnet ef migrations add InitialCreate`
   Crea file C# nella cartella `Migrations/` con i metodi `Up()` (applica) e `Down()` (annulla).
2. **Applicazione al database**:
   `dotnet ef database update`
   Confronta lo storico nella tabella `__EFMigrationsHistory` ed esegue solo le migrazioni mancanti.
3. **Rimozione ultima migrazione non applicata**:
   `dotnet ef migrations remove`

Per controllare il SQL prima di una distribuzione, genera un artefatto revisionabile:
```powershell
dotnet ef migrations script --idempotent --output migrations.sql
```
Ispeziona sempre le operazioni, soprattutto `DropColumn` o `DropTable`: una migrazione non è un backup. In produzione usa un passaggio controllato con script o bundle invece di far aggiornare lo schema automaticamente da ogni istanza dell'applicazione.

Il laboratorio usa le migrazioni per creare SQLite. Non applicare `Database.EnsureCreated()` allo stesso database: crea lo schema senza la cronologia delle migrazioni e i due flussi non vanno mescolati.

### Applicazione automatica all'avvio (solo per sviluppo locale):
```csharp
using var scope = app.Services.CreateScope();
var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
db.Database.Migrate();
```
Usala soltanto per sviluppo locale. Per la produzione pianifica e rivedi l'applicazione delle migrazioni come parte della distribuzione, invece di farle partire automaticamente da ogni istanza dell'app.

## Segui il lavoro del DbContext

```text
dotnet tool restore
dotnet restore
dotnet ef migrations add AddUserTable
dotnet ef migrations script --idempotent --output migrations.sql
dotnet ef database update
# Esamina la migrazione e lo script prima di applicarli.
```

### Osserva che cosa ha fatto il contesto

1. Dalla cartella `server/`, `dotnet tool restore` recupera il tool locale dal manifest e `dotnet restore` prepara il progetto per il design-time.
2. `dotnet ef migrations add AddUserTable` confronta il modello corrente con lo snapshot e genera una migrazione nominata.
3. Esamina `Up`, `Down`, lo snapshot e lo script SQL prima di applicarli: rinominare una proprietà può produrre una rimozione dati, e la migrazione non è un backup.
4. In locale `dotnet ef database update` applica le migrazioni pendenti e aggiorna la cronologia. Per la produzione usa una revisione e un passaggio di deploy controllato; non migrare automaticamente a ogni avvio.

## Che cosa resta responsabilità del database?

- Modificare manualmente le tabelle del database da un tool esterno disallineando lo snapshot delle migrazioni di EF Core.

> **Che cosa è stato caricato o salvato davvero?** A cosa serve la tabella interna `__EFMigrationsHistory` creata da EF Core?
