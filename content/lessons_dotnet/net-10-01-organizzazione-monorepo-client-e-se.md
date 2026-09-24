# Organizzazione Monorepo: client/ e server/

## In parole semplici

L'obiettivo di questa lezione è gestire l'architettura monorepo unificando frontend Angular e backend .NET nello stesso repository.

Un monorepo racchiude client e server nello stesso repository e permette di versionare insieme modifiche collegate. Dipendenze, build e contratti tra i progetti restano da configurare e verificare.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `monorepo`
- `client`
- `server`
- `shared contracts`
- `git`
- `struttura cartelle`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`monorepo`, `client`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Struttura Standard di un Monorepo Full-Stack:
```text
mio-progetto/
├── client/                     # Applicazione Angular 22 Standalone
│   ├── src/app/
│   ├── package.json
│   └── tsconfig.json
├── server/                     # Web API ASP.NET Core (.NET 10)
│   ├── Program.cs
│   ├── Controllers/ o Endpoints/
│   └── Server.csproj
├── README.md                   # Documentazione di avvio e architettura
└── .gitignore
```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
# Terminale 1, dalla cartella server/:
dotnet run

# Terminale 2, dalla cartella client/:
npm start
```

### Seguilo passo per passo

1. `client/` contiene progetto Angular e manifest npm; `server/` contiene progetto ASP.NET Core e file .NET.
2. Apri un terminale nella cartella `server/` e avvia `dotnet run`; in un secondo terminale, entra in `client/` e avvia `npm start`.
3. I due processi condividono il repository e la cronologia Git, ma hanno dipendenze e comandi di avvio distinti. Il contratto HTTP deve restare coerente tra DTO C# e tipi TypeScript.
4. Cambia il nome di un campo nel backend senza aggiornare il client e osserva il mismatch. Documenta come verificare o generare il contratto condiviso.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class MonorepoStructureValidator {
    public static bool HasClientAndServer(bool hasClient, bool hasServer) => hasClient && hasServer;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dare per scontato che il monorepo condivida automaticamente tipi o dipendenze
- mantenere i manifest nei progetti corretti e verificare il contratto HTTP tra client e server.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quale vantaggio pratico offre un Monorepo per il rilascio congiunto di modifiche a client e server?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
