# Architettura Pulita: separazione di Domain, Application e API

Se il dominio importa EF Core, un cambio del database si propaga alle regole che dovrebbero restare stabili. Clean Architecture rende esplicita la direzione delle dipendenze: il codice esterno può conoscere i contratti interni, mentre il nucleo non conosce framework e adapter.

### Nel percorso

Da conoscere: [Dependency Injection: Transient, Scoped e Singleton](net-03-02-dependency-injection-transient-scop.md); [Principi SOLID applicati allo sviluppo Full-Stack](net-09-03-principi-solid-applicati-allo-svilu.md).

Usa questa separazione quando regole e integrazioni cambiano in modo indipendente. Un CRUD piccolo può iniziare con cartelle e servizi nello stesso progetto: creare quattro progetti subito aggiunge configurazione senza necessariamente migliorare lo studio. Angular comunica con l'API via HTTP e non è un assembly dipendente da Domain. L'esercizio considera i riferimenti tra layer di business; il punto di composizione dell'API può conoscere Infrastructure per registrare le implementazioni.

## Il comportamento che vogliamo proteggere

### Dipendenze nel progetto, dati nella richiesta
```text
src/
  Domain/          Subject, regole e invarianti
  Application/     RegisterSubject, ISubjectRepository
  Infrastructure/  AppDbContext, repository EF Core
  Api/             route handler e composizione DI
```

```text
Runtime:   HTTP → API → Application → Domain
                         ↓ contratto
                     repository
                         ↑ implementato da
Build-time: Infrastructure → Application / Domain
            Api → Application / Infrastructure (composition root)
```

Application dichiara la porta che le serve; Infrastructure dipende da quel contratto e lo realizza con EF Core. L'API è il composition root: registra l'implementazione e traduce la richiesta HTTP in una chiamata al caso d'uso. Angular resta un processo separato e comunica con l'API via HTTP, non è un assembly del Domain.

La stessa idea può iniziare con quattro cartelle in un solo progetto. Dividere subito una piccola app in molti progetti aggiunge riferimenti e configurazione; fallo quando le dipendenze o i test diventano più chiari grazie al confine.

## Prepara, esegui, osserva

```text
POST /api/subjects → RegisterSubject → ISubjectRepository
EF Core repository → SQLite
```

### Rendi riproducibile il comportamento

1. API riceve JSON e costruisce un comando per `RegisterSubject`.
2. Application applica il caso d'uso e dipende dall'interfaccia `ISubjectRepository`, dichiarata verso il centro.
3. Il contenitore DI in Api fornisce l'implementazione Infrastructure; questa usa `DbContext` per salvare.
4. Verifica i riferimenti fra progetti: se `Domain` importa ASP.NET Core o EF Core, il dettaglio esterno è entrato nel nucleo. Se l'app è piccola, prima dimostra il valore del confine con test semplici.

La verifica dell'esercizio riguarda soltanto le dipendenze consentite. Nel portfolio, annota quale modifica rende più semplice questa separazione e quale costo di configurazione introduce.

## Che cosa rende il difetto osservabile?

- Far dipendere il Domain da EF Core o da librerie web
- saltare i layer e scrivere query SQL direttamente nei componenti UI.

> **Quale evidenza dimostra il comportamento?** Qual è la regola cardinale della Clean Architecture riguardo alla direzione delle dipendenze?
