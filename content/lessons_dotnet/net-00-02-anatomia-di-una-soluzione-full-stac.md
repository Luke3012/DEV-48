# Anatomia di una soluzione Full-Stack Client-Server

## In parole semplici

L'obiettivo di questa lezione è seguire una richiesta tra client Angular nel browser e server ASP.NET Core, distinguendo indirizzi, risposte e configurazione CORS.

Il frontend Angular mostra l'interfaccia nel browser; il backend ASP.NET Core applica regole e accesso ai dati. Si scambiano richieste e risposte HTTP, spesso con dati JSON. Nel primo esercizio C# si usano metodi e parametri già introdotti nella lezione precedente.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `architettura client server`
- `richiesta http`
- `json`
- `cors`
- `porta di ascolto`
- `stato della sessione`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`architettura client server`, `richiesta http`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class EndpointMapper {
    public static string FormatUrl(string baseUrl, string resource) {
        return $"{baseUrl.TrimEnd('/')}/{resource.TrimStart('/')}";
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Credere che Angular esegua codice C# nel browser
- ignorare che client e server girano su porte e processi separati.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è il ruolo rispettivo del client Angular e del server .NET nel ciclo di vita di una richiesta?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
