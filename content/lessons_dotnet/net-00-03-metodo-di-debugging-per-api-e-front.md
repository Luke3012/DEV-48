# Metodo di debugging per API e Frontend

Il debugging sistematico richiede di isolare il perimetro: prima verifica la rete (DevTools Network), poi l'output del backend (log o eccezioni C#), infine lo stato del componente Angular. Qui usiamo un metodo con `if` e `return` per classificare pochi codici HTTP: ogni ramo è spiegato prima dell'esercizio.

## Partiamo da quello che puoi osservare

### Matrice Diagnostica degli Errori:
- **Errore di Compilazione C# (`error CS...`)**: il backend non compila per sintassi errata, tipi non corrispondenti o riferimenti mancanti.
- **Errore HTTP 4xx (Client Error)**:
  - `400 Bad Request`: il JSON inviato da Angular non rispetta il formato atteso dal DTO .NET.
  - `401 Unauthorized`: token JWT assente o non valido (per esempio scaduto); `403 Forbidden`: identità autenticata senza il ruolo o permesso richiesto.
  - `404 Not Found`: l'URL o la rotta dell'API è errata.
- **Errore HTTP 500 (Internal Server Error)**: eccezione non gestita nel backend .NET (es. `NullReferenceException`, errore di query DB). Controlla il terminale del server per lo stack trace.
- **CORS Error nel browser**: il server .NET non ha abilitato la policy per l'origine Angular (`http://localhost:4200`).

### Un metodo C# con `if`
`if (condizione)` esegue il ramo quando la condizione è vera. `&&` significa “entrambe le condizioni sono vere”; `return` restituisce il testo e termina il metodo, quindi il primo ramo soddisfatto è quello usato.

```csharp
public static string Classify(int statusCode) {
    if (statusCode >= 200 && statusCode <= 299) return "Success";
    if (statusCode >= 400 && statusCode <= 499) return "ClientError";
    if (statusCode >= 500 && statusCode <= 599) return "ServerError";
    return "Other";
}
```

## Segui un caso dall'inizio alla fine

```text
// 1. Guarda la Console del browser per errori JS/TS
// 2. Guarda il tab Network per vedere lo status code HTTP (400, 404, 500)
// 3. Guarda il terminale del server per lo stack trace C#
```

### Ricostruisci il caso con i dati iniziali

1. Parti dal sintomo osservabile nel browser: errore JavaScript, schermata vuota o richiesta fallita. Non modificare codice ancora.
2. Apri Network e leggi URL, metodo e status code. Un `404` indica una rotta non trovata; un `500` sposta l'indagine sul server.
3. Se la richiesta non parte, controlla Console e componente Angular; se parte ma fallisce, confronta la risposta con il log del backend.
4. Nel classificatore, prova i limiti `199`, `200`, `299`, `300`, `400`, `499`, `500`, `599` e `600`: ogni `if` controlla una fascia e `return` termina il metodo appena trova quella giusta.

## Una variante da provare

```csharp
public static class HttpErrorClassifier {
    public static string Classify(int statusCode) {
        if (statusCode >= 200 && statusCode <= 299) return "Success";
        if (statusCode >= 400 && statusCode <= 499) return "ClientError";
        if (statusCode >= 500 && statusCode <= 599) return "ServerError";
        return "Other";
    }
}
```

## Se il risultato non è quello atteso

- Cercare l'errore nel componente Angular quando la richiesta fallisce con HTTP 500 nel server
- modificare file a caso senza leggere il messaggio.

> **Fermati e ricostruisci il passaggio** Se un pulsante in Angular non aggiorna la tabella, quali tre controlli esegui in ordine?
