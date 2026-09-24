# Query con LINQ su Database: Tracking e AsNoTracking

## In parole semplici

L'obiettivo di questa lezione è capire quando una query EF Core di sola lettura può usare AsNoTracking e quali trade-off comporta.

Per una query di sola lettura, `AsNoTracking()` evita di conservare le entità nel Change Tracker e può ridurre lavoro e memoria. Il beneficio dipende dai dati e dalla forma della query; senza identity resolution, le entità ripetute possono diventare istanze separate. Misura prima di presentare un guadagno come certo.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `linq to entities`
- `asnotracking`
- `change tracker`
- `includi`
- `eager loading`
- `n+1`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`linq to entities`, `asnotracking`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Tracking vs NoTracking:
- **Query con Tracking (default per entità)**:
  EF Core registra le entità e rileva le modifiche. Se cambi una proprietà e chiami `SaveChangesAsync()`, può inviare al database l'aggiornamento corrispondente. Il tracking supporta anche l'identity resolution.
- **Query `AsNoTracking()` (sola lettura)**:
  EF Core non registra nel contesto le entità restituite. Può essere adatto a letture che non verranno salvate; non usa l'identity resolution del contesto.
  ```csharp
  var products = await db.Products
      .AsNoTracking()
      .Where(p => p.Price > 50)
      .ToListAsync();
  ```

### Caricamento delle Relazioni con `Include()` (Eager Loading):
```csharp
var orderWithItems = await db.Orders
    .AsNoTracking()
    .Include(o => o.Items) // Carica le misure correlate in questa query.
    .FirstOrDefaultAsync(o => o.Id == id);
```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```csharp
var users = await db.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .ToListAsync();
```

### Seguilo passo per passo

1. La query parte da `db.Users`, filtra le righe attive con `Where` e termina con `ToListAsync()`.
2. `AsNoTracking()` indica che EF Core non deve conservare quelle entità nel Change Tracker: è utile se la lettura non porterà a modifiche nello stesso contesto.
3. L'assenza di tracking può ridurre lavoro e memoria, ma il risultato dipende dalla query. Senza identity resolution, righe che rappresentano la stessa entità possono produrre istanze separate.
4. Seleziona un caso in cui vuoi aggiornare l'entità e confrontalo con una lettura solo per visualizzazione. Scegli in base al lavoro successivo, non al verbo HTTP.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class QueryOptionsHelper {
    public static bool ShouldUseNoTracking(bool willModifyEntities) =>
        !willModifyEntities;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Scegliere il tracking solo dal verbo HTTP: considera se aggiornerai le entità e se la query ha bisogno di identity resolution. `Include()` carica relazioni, ma controlla comunque la forma della query e i dati.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quando è adatto `AsNoTracking()` e quale comportamento del tracking rinunci a usare?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
