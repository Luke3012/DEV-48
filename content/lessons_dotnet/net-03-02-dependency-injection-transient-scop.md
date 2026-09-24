# Dependency Injection: Transient, Scoped e Singleton

## In parole semplici

L'obiettivo di questa lezione è conoscere i tre cicli di vita del contenitore DI di ASP.NET Core e scegliere in base alla condivisione e alla durata delle dipendenze.

La Dependency Injection disaccoppia le classi fornendo le dipendenze richieste dall'esterno, facilitando il testing e la gestione del ciclo di vita degli oggetti.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `dependency injection`
- `ioc container`
- `transient`
- `scoped`
- `singleton`
- `disposable`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`dependency injection`, `ioc container`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### I Tre Lifetimes di ASP.NET Core:
1. **`Transient` (`AddTransient<TService, TImpl>()`)**:
   - Viene creata una nuova istanza ogni volta che il servizio viene richiesto.
   - Ideale per servizi leggeri e stateless.
2. **`Scoped` (`AddScoped<TService, TImpl>()`)**:
   - Viene creata una sola istanza per ogni scope di servizio; nelle Web API, di solito lo scope coincide con una richiesta HTTP.
   - `AddDbContext` registra normalmente `DbContext` come scoped. Questo allinea la durata del contesto alla richiesta, ma non avvia da solo una transazione che copra più chiamate a `SaveChanges`.
3. **`Singleton` (`AddSingleton<TService, TImpl>()`)**:
   - Viene creata un'unica istanza condivisa per l'intera durata dell'applicazione.
   - Ideale per cache in memoria, logger o servizi di background thread-safe.

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```csharp
builder.Services.AddSingleton<ICache, MemoryCache>();
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddTransient<IEmailSender, EmailSender>();
```

### Seguilo passo per passo

1. Ogni riga registra un contratto (`ICache`, `IUserRepository`, `IEmailSender`) e la classe che lo implementa.
2. `Transient` crea un'istanza per ogni richiesta di servizio; `Scoped` riusa l'istanza nella richiesta web; `Singleton` mantiene un'istanza per la vita del contenitore.
3. ASP.NET Core risolve il servizio quando serve, per esempio nel costruttore di un endpoint o di un'altra classe. Il ciclo di vita influenza la condivisione dello stato.
4. Immagina due richieste HTTP e confronta cosa può essere condiviso. Non inserire una dipendenza `Scoped` in un `Singleton` senza progettare esplicitamente lo scope.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public interface ICounterService { int Next(); }
public class CounterService : ICounterService {
    private int _count = 0;
    public int Next() => ++_count;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Iniettare un servizio Scoped (come il DbContext) dentro un Singleton senza creare e gestire uno scope esplicito: il servizio conserva una dipendenza più breve del proprio lifetime.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché `DbContext` ha normalmente durata Scoped in una Web API, e che cosa non garantisce questo lifetime?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
