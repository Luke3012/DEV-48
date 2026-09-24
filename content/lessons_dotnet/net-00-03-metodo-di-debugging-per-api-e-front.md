# Metodo di debugging per API e Frontend

## In parole semplici

L'obiettivo di questa lezione è isolare un errore distinguendo problemi di compilazione C#, errori HTTP di rete e bug di rendering Angular.

Il debugging sistematico richiede di isolare il perimetro: prima verifica la rete (DevTools Network), poi l'output del backend (log o eccezioni C#), infine lo stato del componente Angular. Qui usiamo un metodo con `if` e `return` per classificare pochi codici HTTP: ogni ramo è spiegato prima dell'esercizio.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `stack trace`
- `network tab`
- `status code`
- `console.log`
- `breakpoint`
- `falsificabile`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`stack trace`, `network tab`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
// 1. Guarda la Console del browser per errori JS/TS
// 2. Guarda il tab Network per vedere lo status code HTTP (400, 404, 500)
// 3. Guarda il terminale del server per lo stack trace C#
```

### Seguilo passo per passo

1. Parti dal sintomo osservabile nel browser: errore JavaScript, schermata vuota o richiesta fallita. Non modificare codice ancora.
2. Apri Network e leggi URL, metodo e status code. Un `404` indica una rotta non trovata; un `500` sposta l'indagine sul server.
3. Se la richiesta non parte, controlla Console e componente Angular; se parte ma fallisce, confronta la risposta con il log del backend.
4. Nel classificatore, prova i limiti `199`, `200`, `299`, `300`, `400`, `499`, `500`, `599` e `600`: ogni `if` controlla una fascia e `return` termina il metodo appena trova quella giusta.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

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

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Cercare l'errore nel componente Angular quando la richiesta fallisce con HTTP 500 nel server
- modificare file a caso senza leggere il messaggio.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Se un pulsante in Angular non aggiorna la tabella, quali tre controlli esegui in ordine?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
