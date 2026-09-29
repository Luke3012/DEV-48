# Anatomia di una soluzione Full-Stack Client-Server

## In parole semplici

L'obiettivo di questa lezione è seguire una richiesta tra client Angular nel browser e server ASP.NET Core, distinguendo indirizzi, risposte e configurazione CORS.

Il frontend Angular mostra l'interfaccia nel browser; il backend ASP.NET Core applica regole e accesso ai dati. Si scambiano richieste e risposte HTTP, spesso con dati JSON. Nel primo esercizio C# si usano metodi e parametri già introdotti nella lezione precedente.

## Le parole da riconoscere

- `architettura client server`
- `richiesta http`
- `json`
- `cors`
- `porta di ascolto`
- `stato della sessione`

## Anatomia e Sintassi del Codice

### Flusso della Richiesta Full-Stack:
1. **Client (Browser/Angular)**:
   - Utente clicca un pulsante -> Angular invia una richiesta HTTP (GET, POST, PUT, DELETE) serializzando i dati in JSON.
   - Resta in attesa asincrona della risposta (Promise/Observable/Signal).
2. **Rete e Porte**:
   - Client e Server girano su porte differenti (es. Angular su `localhost:4200`, API .NET su `localhost:5001`).
   - Il server deve abilitare il CORS (Cross-Origin Resource Sharing) per consentire le chiamate dal frontend.
3. **Backend (.NET Minimal API)**:
   - Riceve la richiesta HTTP, deserializza il JSON nel relativo DTO C#.
   - Esegue la logica di business, legge o scrive su SQLite/EF Core.
   - Restituisce uno Status Code HTTP (200 OK, 201 Created, 400 Bad Request) con payload JSON.

### Unire le parti di un endpoint in C#
`TrimEnd('/')` rimuove le barre finali dall'indirizzo base; `TrimStart('/')` rimuove quelle iniziali dal percorso. La stringa `$"{baseClean}/{resourceClean}"` inserisce i due valori nel testo.

```csharp
var baseClean = baseUrl.TrimEnd('/');
var resourceClean = resource.TrimStart('/');
var endpoint = $"{baseClean}/{resourceClean}";
```

## Un esempio concreto

```text
// Frontend (Angular) invia richiesta GET a https://localhost:5001/api/items
// Backend (ASP.NET Core) elabora, legge dal DB e risponde con JSON [ { id: 1, name: 'Item' } ]
```

### Seguilo passo per passo

1. Leggi l'URL `https://localhost:5001/api/items`: identifica protocollo, host, porta e percorso. Il browser invia la richiesta a quell'indirizzo.
2. Segui il percorso nel server: ASP.NET Core riceve la richiesta, esegue il gestore e può leggere dati prima di produrre la risposta JSON.
3. L'oggetto `{ id: 1, name: 'Item' }` è il corpo di risposta; il browser lo riceve e Angular può trasformarlo in una vista.
4. Nel codice C#, `TrimEnd('/')` e `TrimStart('/')` rimuovono barre nei punti adiacenti; prova `https://localhost:5001/` con `/api/items` e controlla l'URL risultante.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
public static class EndpointMapper {
    public static string FormatUrl(string baseUrl, string resource) {
        return $"{baseUrl.TrimEnd('/')}/{resource.TrimStart('/')}";
    }
}
```

## Dove ci si confonde spesso

- Credere che Angular esegua codice C# nel browser
- ignorare che client e server girano su porte e processi separati.

## Domanda di verifica

> Qual è il ruolo rispettivo del client Angular e del server .NET nel ciclo di vita di una richiesta?
