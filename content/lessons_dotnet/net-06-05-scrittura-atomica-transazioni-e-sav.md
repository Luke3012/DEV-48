# Scrittura atomica, Transazioni e SaveChangesAsync

## In parole semplici

L'obiettivo di questa lezione è inserire, aggiornare ed eliminare record gestendo transazioni atomiche e concorrenza.

`SaveChangesAsync()` invia le modifiche tracciate. Con un provider relazionale EF Core usa di norma una transazione per la singola chiamata; provider e operazioni distribuite possono avere comportamenti diversi.

## Le parole da riconoscere

- `savechangesasync`
- `add`
- `update`
- `remove`
- `transazione`
- `concorrenza`

## Anatomia e Sintassi del Codice

### Flusso di Scrittura Standard con EF Core:
```csharp
// 1. Creazione
var product = new Product { Title = "Tastiera Meccanica", Price = 89.99m };
db.Products.Add(product);
await db.SaveChangesAsync(); // Genera INSERT e popola product.Id con la chiave autoincrementale!

// 2. Modifica
var existing = await db.Products.FindAsync(id);
if (existing is not null) {
    existing.Price = 79.99m;
    await db.SaveChangesAsync(); // Genera UPDATE solo sulle colonne modificate!
}

// 3. Rimozione
db.Products.Remove(existing);
await db.SaveChangesAsync(); // Genera DELETE
```

## Un esempio concreto

```text
db.Orders.Add(order);
await db.SaveChangesAsync(); // Salva e assegna automaticamente la chiave primaria generata dal DB.
```

### Seguilo passo per passo

1. `Add(order)` aggiunge l'ordine al Change Tracker; normalmente non invia ancora la modifica al database.
2. `await SaveChangesAsync()` invia le modifiche pendenti e, con un provider relazionale, EF Core usa di norma una transazione per rendere atomiche le modifiche di quella chiamata.
3. Se la chiamata riesce, il provider può valorizzare la chiave generata e il metodo restituisce il numero di entità interessate. La concorrenza può comunque produrre un conflitto.
4. Aggiungi due modifiche prima di salvare e poi provoca un errore di vincolo. Verifica quali modifiche vengono confermate e quando serve una transazione esplicita più ampia.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Chiamare `SaveChangesAsync()` all'interno di un ciclo foreach invece di raggruppare le modifiche ed eseguire una singola chiamata finale.

## Domanda di verifica

> Che cosa restituisce il metodo `SaveChangesAsync()` al suo completamento?
