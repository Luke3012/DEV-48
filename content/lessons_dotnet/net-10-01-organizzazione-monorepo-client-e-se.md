# Organizzazione Monorepo: client/ e server/

## In parole semplici

L'obiettivo di questa lezione è gestire l'architettura monorepo unificando frontend Angular e backend .NET nello stesso repository.

Un monorepo racchiude client e server nello stesso repository e permette di versionare insieme modifiche collegate. Dipendenze, build e contratti tra i progetti restano da configurare e verificare.

### Nel percorso

Da conoscere: [Minimal API da zero: Program.cs e WebApplication](net-03-01-minimal-api-da-zero-programcs-e-web.md); [Progetto Angular Standalone e Bootstrap applicazione](net-04-01-progetto-angular-standalone-e-boots.md).

Ora collega il contesto dei soggetti: GET `/api/subjects` restituisce la lista, POST crea, PUT modifica e DELETE rimuove. Nel laboratorio Gestionale Full-Stack Monorepo completa prima la lettura dal server, poi collega al servizio i comandi di modifica della UI. Le suite separate non dimostrano da sole la comunicazione tra i due processi: prova anche un'operazione dal browser.

## Le parole da riconoscere

- `monorepo`
- `client`
- `server`
- `shared contracts`
- `git`
- `struttura cartelle`

## Anatomia e Sintassi del Codice

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

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Dare per scontato che il monorepo condivida automaticamente tipi o dipendenze
- mantenere i manifest nei progetti corretti e verificare il contratto HTTP tra client e server.

## Domanda di verifica

> Quale vantaggio pratico offre un Monorepo per il rilascio congiunto di modifiche a client e server?
