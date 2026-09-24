# Architettura Pulita: separazione di Domain, Application e API

## In parole semplici

L'obiettivo di questa lezione è organizzare una soluzione enterprise isolando entità di dominio, casi d'uso e adapter infrastrutturali.

La Clean Architecture stabilisce che le regole di business e il dominio centrale non devono dipendere da nessun framework esterno, database o libreria UI. I dettagli dipendono dal dominio, mai il contrario.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `clean architecture`
- `onion architecture`
- `domain layer`
- `application layer`
- `infrastructure`
- `dependency rule`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`clean architecture`, `onion architecture`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### I Layer della Clean Architecture:
1. **Domain (Nucleo)**: Entità pure, Value Objects, eccezioni di dominio. Zero dipendenze esterne.
2. **Application (Casi d'Uso)**: DTO, interfacce dei repository, comandi e query di business. Dipende solo dal Domain.
3. **Infrastructure**: Implementazione concreta dei repository con EF Core, invio email, client HTTP esterni. Dipende da Application e Domain.
4. **API / Presentation**: Minimal API di ASP.NET Core o frontend Angular. Riceve le richieste e delega ai casi d'uso.

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
API endpoint -> caso d'uso Application -> regole Domain

Infrastructure implementa i contratti dichiarati verso il centro. Domain non conosce database, ASP.NET Core o Angular.
```

### Seguilo passo per passo

1. Il Domain contiene regole e modelli centrali; non importa EF Core o ASP.NET Core.
2. Application coordina casi d'uso e dichiara le porte di cui ha bisogno; Infrastructure può implementare quelle porte usando EF Core.
3. API riceve richieste HTTP e compone i servizi. Le dipendenze puntano verso il centro: Domain non dipende dai dettagli esterni.
4. Segui una richiesta dal route handler al caso d'uso e al repository. Se trovi un `DbContext` nel Domain, sposta l'accesso al database verso Infrastructure.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
using System.Threading;
using System.Threading.Tasks;

public sealed record Subject(string Name);

public interface ISubjectRepository {
    Task SaveAsync(Subject subject, CancellationToken cancellationToken);
}

public sealed class RegisterSubject(ISubjectRepository repository) {
    public Task ExecuteAsync(Subject subject, CancellationToken cancellationToken) =>
        repository.SaveAsync(subject, cancellationToken);
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Far dipendere il Domain da EF Core o da librerie web
- saltare i layer e scrivere query SQL direttamente nei componenti UI.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è la regola cardinale della Clean Architecture riguardo alla direzione delle dipendenze?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
