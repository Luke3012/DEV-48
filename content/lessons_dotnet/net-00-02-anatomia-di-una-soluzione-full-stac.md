# Anatomia di una soluzione Full-Stack Client-Server

Quando una persona apre un elenco nel browser, la pagina e il server che possiede i dati sono due programmi distinti. L'HTTP è il confine osservabile tra loro: la richiesta porta un metodo, un indirizzo e, quando serve, un body; la risposta porta uno status e un body, spesso JSON.

## Il confine tra due programmi

### Una lettura dal browser e il viaggio dei dati
```text
Persona seleziona “Soggetti”
  ↓
Browser: GET https://localhost:5001/api/subjects?zone=Centro
  ↓ HTTP attraverso la rete
ASP.NET Core: trova una route che corrisponde
  ↓ legge i dati e applica le regole
Risposta: HTTP 200 + JSON nel body
  ↓
Angular: interpreta il dato e aggiorna la vista
```

Il metodo e il percorso descrivono quale operazione chiedere; il body trasporta i dati della richiesta o della risposta. Il codice HTTP comunica l'esito, per esempio `200` per una lettura riuscita o `404` per una risorsa assente. Il server serializza il proprio oggetto in JSON; il browser riceve testo strutturato, non un oggetto C# condiviso in memoria.

`https://localhost:4200` e `https://localhost:5001` hanno schema e host uguali ma porte diverse: per il browser sono origini diverse. In sviluppo puoi usare un proxy oppure configurare una policy CORS specifica sull'API. CORS regola la lettura cross-origin nel browser, non autentica la persona.

All'inizio seguiamo solo una GET. Nelle lezioni successive il Router e `HttpClient` spiegheranno la parte Angular, mentre Minimal API mostrerà come una route raggiunge il suo gestore. In seguito il percorso continuerà dal gestore a service, `DbContext` e database.

## Dal click alla risposta JSON

```text
GET /api/subjects?zone=Centro → HTTP 200 → { "id": 7, "name": "Centro" }
```

### Ricostruisci il caso con i dati iniziali

1. La persona apre la pagina dei soggetti; l'interfaccia decide di chiedere al server i record della zona `Centro`.
2. Il browser invia il metodo `GET` e il percorso `/api/subjects?zone=Centro` all'host ASP.NET Core. La porta fa parte dell'origine, mentre il percorso identifica la risorsa.
3. ASP.NET Core trova un endpoint che corrisponde e produce una risposta. Il browser riceve uno status HTTP e un body JSON; non condivide direttamente le classi o gli oggetti in memoria del server.
4. Angular può interpretare il body secondo il tipo atteso e usarlo per renderizzare l'elenco. Un `404` indica un percorso non trovato; un errore CORS indica una policy del browser/API e va distinto da un errore dell'endpoint.

L'esercizio breve controlla la composizione di un URL, non apre una connessione HTTP. È un primo esercizio di lettura degli indirizzi; il laboratorio Monorepo e quello Minimal API verificheranno poi una richiesta reale da browser a server.

## Leggi status e origine prima di cercare il bug

- Il JSON trasporta dati, non tipi condivisi tra C# e TypeScript
- una porta diversa cambia l'origine del browser anche quando host e schema coincidono
- CORS non sostituisce autenticazione o autorizzazione.

> **Quale dato attraversa HTTP e quale resta dentro ciascun processo?** Qual è il ruolo rispettivo del client Angular e del server .NET nel ciclo di vita di una richiesta?
