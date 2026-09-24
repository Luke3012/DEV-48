# Setup dell'ambiente moderno per Angular e .NET

## In parole semplici

L'obiettivo di questa lezione è verificare la presenza di .NET SDK, Node.js, Angular CLI e impostare VS Code con estensioni essenziali.

Installa il .NET SDK 10 per compilare C# e Node.js per usare npm e gli strumenti Angular. Il browser esegue l'app Angular; Node.js serve durante lo sviluppo e i test. L'Angular CLI può essere richiamata con npx, quindi non occorre installarla globalmente.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `dotnet sdk`
- `node.js`
- `angular cli`
- `vs code`
- `terminale`
- `toolchain`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`dotnet sdk`, `node.js`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```text
Gli output devono mostrare .NET SDK 10, una versione Node supportata da Angular 22 e una Angular CLI 22. Se un comando non viene trovato, controlla l'installazione e apri una nuova finestra di PowerShell.
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare di riavviare il terminale dopo l'installazione del SDK
- confondere Runtime con SDK di .NET.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Come verifichi dal terminale che il compilatore .NET e l'interprete Node siano installati e pronti all'uso?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
