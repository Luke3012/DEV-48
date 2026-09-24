# Presentare il progetto: Git, README professionale e Portfolio

## In parole semplici

L'obiettivo di questa lezione è documentare architettura, comandi e decisioni tecniche in modo che un'altra persona possa avviare e valutare il progetto.

Un progetto brillante viene valorizzato solo se spiegato chiaramente: un README eccellente illustra l'architettura, le decisioni tecniche prese, i comandi di avvio e le future estensioni possibili.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `readme professionale`
- `architettura`
- `compromessi tecnici`
- `openapi`
- `swagger`
- `portfolio github`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`readme professionale`, `architettura`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Sezioni Indispensabili di un README Professionale:
1. **Titolo & Badge**: nome del progetto, versione di .NET e Angular.
2. **Architettura della Soluzione**: diagramma concettuale o elenco delle tecnologie adottate.
3. **Decisioni Tecniche e Compromessi**:
   - *Perché abbiamo scelto Minimal API invece dei Controller tradizionali?*
   - *Quale stato abbiamo rappresentato con Signals e quale configurazione di change detection usa il progetto?*
   - *Come abbiamo strutturato la sicurezza con JWT e Route Guards?*
4. **Istruzioni di Setup & Avvio Rapido**: comandi esatti per eseguire backend e frontend in locale.
5. **Suite di Test**: comandi per eseguire `dotnet test` e `npm test`.

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
# Archivio soggetti

## Architettura
- Frontend: Angular 22 standalone; Signals per lo stato derivato della schermata.
- Backend: API Minimal .NET 10; EF Core per l'accesso al database.

## Decisioni e compromessi
- Le query di sola lettura usano AsNoTracking dove non serve modificare le entità.
- L'autenticazione usa JWT firmati; il server valida token e autorizzazioni.

## Avvio e test
- `dotnet test server/Tests/Server.Tests.csproj`
- `npm test --prefix client`
```

### Seguilo passo per passo

1. Leggi ogni riga del README come un'affermazione verificabile: stack, comandi, decisioni e limiti devono corrispondere al progetto.
2. Descrivi Angular per lo stato e l'interfaccia, .NET per API e regole server, ed EF Core per la persistenza; specifica dove il codice è davvero eseguito.
3. Spiega un compromesso con un fatto osservabile. Signals gestisce stato reattivo; da solo non elimina Zone.js né garantisce un miglioramento prestazionale.
4. Segui i comandi di setup in una cartella pulita e verifica che il portfolio si avvii. Correggi ogni passaggio che richiede conoscenze non documentate.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class PortfolioSummaryHelper {
    public static string FormatBadge(string tech, string version) => $"[{tech.Trim()} v{version.Trim()}]";
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Lasciare il README di default generato dalla CLI
- non menzionare quali problemi risolve il progetto o nascondere i limiti noti.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Cosa non dovrebbe mai mancare nel README di un progetto open-source o di portfolio?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
