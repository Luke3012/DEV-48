# Presentare il progetto: Git, README professionale e Portfolio

Un README permette di avviare e comprendere il progetto. Documenta l'architettura, le decisioni tecniche prese, i comandi di avvio e le future estensioni possibili.

## Il progetto visto da chi deve usarlo

### Sezioni Indispensabili di un README Professionale:
1. **Titolo & Badge**: nome del progetto, versione di .NET e Angular.
2. **Architettura della Soluzione**: diagramma concettuale o elenco delle tecnologie adottate.
3. **Decisioni Tecniche e Compromessi**:
   - *Perché abbiamo scelto Minimal API invece dei Controller tradizionali?*
   - *Quale stato abbiamo rappresentato con Signals e quale configurazione di change detection usa il progetto?*
   - *Come abbiamo strutturato la sicurezza con JWT e Route Guards?*
4. **Istruzioni di Setup & Avvio Rapido**: comandi esatti per eseguire backend e frontend in locale.
5. **Suite di Test**: comandi per eseguire `dotnet test` e `npm test`.

## Attraversa i file e i processi coinvolti

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

### Racconta l'operazione dal file al risultato

1. Leggi ogni riga del README come un'affermazione verificabile: stack, comandi, decisioni e limiti devono corrispondere al progetto.
2. Descrivi Angular per lo stato e l'interfaccia, .NET per API e regole server, ed EF Core per la persistenza; specifica dove il codice è davvero eseguito.
3. Spiega un compromesso con un fatto osservabile. Signals gestisce stato reattivo; da solo non elimina Zone.js né garantisce un miglioramento prestazionale.
4. Segui i comandi di setup in una cartella pulita e verifica che il portfolio si avvii. Correggi ogni passaggio che richiede conoscenze non documentate.

## Che cosa deve poter verificare un'altra persona?

- Lasciare il README di default generato dalla CLI
- non menzionare quali problemi risolve il progetto o nascondere i limiti noti.

> **Quale decisione puoi motivare con il codice?** Cosa non dovrebbe mai mancare nel README di un progetto open-source o di portfolio?
