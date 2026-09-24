# Migrazioni di Database: Creazione e Applicazione

## In parole semplici

L'obiettivo di questa lezione è versionare lo schema del database con codice C# e applicare modifiche senza perdere dati.

Le migrazioni di EF Core consentono di evolvere lo schema del database nel tempo in modo ripetibile e tracciabile nel repository Git.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `dotnet ef migrations add`
- `dotnet ef database update`
- `versionamento schema`
- `snapshot`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`dotnet ef migrations add`, `dotnet ef database update`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
dotnet ef migrations add AddUserTable
dotnet ef database update
# Applica le modifiche strutturali senza toccare i dati esistenti.
```

### Seguilo passo per passo

1. `dotnet ef migrations add AddUserTable` confronta il modello corrente con lo snapshot e genera una migrazione nominata.
2. Esamina il codice generato e lo snapshot prima di applicarlo: la migrazione descrive come evolve lo schema, non è una copia di backup dei dati.
3. `dotnet ef database update` applica le migrazioni pendenti al database configurato e aggiorna la cronologia delle migrazioni.
4. Aggiungi una proprietà e genera una nuova migrazione. In produzione applica le modifiche con un passaggio di deploy controllato; evita l'applicazione automatica all'avvio.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class MigrationNameHelper {
    public static string FormatMigrationName(string name) {
        var clean = System.Text.RegularExpressions.Regex.Replace(name ?? "", "[^a-zA-Z0-9]", "");
        return string.IsNullOrEmpty(clean) ? "InitialCreate" : clean;
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Modificare manualmente le tabelle del database da un tool esterno disallineando lo snapshot delle migrazioni di EF Core.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> A cosa serve la tabella interna `__EFMigrationsHistory` creata da EF Core?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
