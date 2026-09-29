# Setup dell'ambiente moderno per Angular e .NET

## In parole semplici

L'obiettivo di questa lezione è verificare la presenza di .NET SDK, Node.js, Angular CLI e impostare VS Code con estensioni essenziali.

Installa il .NET SDK 10 per compilare C# e Node.js per usare npm e gli strumenti Angular. Il browser esegue l'app Angular; Node.js serve durante lo sviluppo e i test. L'Angular CLI può essere richiamata con npx, quindi non occorre installarla globalmente.

### Nel percorso

Il percorso procede da metodi e dati a endpoint HTTP, componenti, stato, database e integrazione. I laboratori sono il punto in cui proverai framework e browser reali. Le sessioni finali servono a consolidare il lavoro; il tempo indicato è una stima, non una soglia di valutazione.

## Le parole da riconoscere

- `dotnet sdk`
- `node.js`
- `angular cli`
- `vs code`
- `terminale`
- `toolchain`

## Anatomia e Sintassi del Codice

### 1. Installa gli strumenti
1. Scarica il **.NET 10 SDK** dal [sito ufficiale .NET](https://dotnet.microsoft.com/download/dotnet/10.0). Scegli l'SDK, non soltanto il Runtime.
2. Installa una versione Node supportata da Angular 22. Per iniziare è comoda la linea LTS 24; consulta la [tabella di compatibilità Angular](https://angular.dev/reference/versions) prima di cambiare versione.
3. Installa Git e Visual Studio Code se vuoi usare il controllo versione e l'editor grafico. Sono consigliati, ma non richiesti per leggere le lezioni.
4. Dopo l'installazione, apri una nuova finestra di PowerShell così il `PATH` viene ricaricato.

### 2. Verifica le versioni in PowerShell
```bash
dotnet --list-sdks  # deve comparire una versione 10.0.x
node --version      # Angular 22: 22.22.3+, 24.15.0+ o 26.0.0+
npm --version
```

`dotnet --version` mostra l'SDK selezionato nella cartella corrente; `dotnet --list-sdks` mostra tutti quelli installati. Il runtime da solo non compila il codice del corso.

### 3. Controlla Angular CLI senza installazione globale
In un progetto Angular usa `npx ng version`: npm esegue la CLI dichiarata dal progetto. Per verificare il download iniziale senza avere ancora un progetto, puoi eseguire `npx --yes @angular/cli@22.2.0 version`.

## Un esempio concreto

```text
Comandi da provare in PowerShell:
dotnet --list-sdks
node --version
npm --version
npx --yes @angular/cli@22.2.0 version
```

### Seguilo passo per passo

1. Esegui `dotnet --list-sdks`, `node --version` e `npm --version`: ogni comando controlla uno strumento diverso. Per compilare C# serve l'SDK, non basta il Runtime.
2. Lancia la CLI con `npx --yes @angular/cli@22.2.0 version`: npm scarica ed esegue la versione richiesta senza installazione globale.
3. Confronta le versioni stampate con quelle richieste dall'esercizio. Se il comando non viene trovato, riapri PowerShell dopo l'installazione e verifica il `PATH`.
4. Prova una seconda volta dopo aver aperto una nuova finestra del terminale: così distingui un problema di installazione da un `PATH` non ancora aggiornato.

## Pattern Guida per gli Esercizi

Annota ciò che osservi sul tuo computer. Il confronto automatico è concettuale: non esegue i comandi al posto tuo.

```text
Gli output devono mostrare .NET SDK 10, una versione Node supportata da Angular 22 e una Angular CLI 22. Se un comando non viene trovato, controlla l'installazione e apri una nuova finestra di PowerShell.
```

## Dove ci si confonde spesso

- Dimenticare di riavviare il terminale dopo l'installazione del SDK
- confondere Runtime con SDK di .NET.

## Domanda di verifica

> Come verifichi dal terminale che il compilatore .NET e l'interprete Node siano installati e pronti all'uso?
