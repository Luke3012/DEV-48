# Principi SOLID applicati allo sviluppo Full-Stack

## In parole semplici

L'obiettivo di questa lezione è applicare i principi Single Responsibility, Open/Closed, Liskov, Interface Segregation e Dependency Inversion.

I principi SOLID guidano la progettazione del software verso classi modulari, a basso accoppiamento e con responsabilità uniche, facili da mantenere ed estendere nel tempo.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `solid`
- `single responsibility`
- `open closed`
- `liskov`
- `interface segregation`
- `dependency inversion`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`solid`, `single responsibility`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### I 5 Principi SOLID in breve:
1. **S - Single Responsibility Principle (SRP)**: una classe deve avere una sola ragione per cambiare (es. un componente non deve occuparsi di chiamate HTTP, delega a un Servizio).
2. **O - Open/Closed Principle (OCP)**: aperto all'estensione, chiuso alla modifica (usare interfacce o polimorfismo invece di modificare classi esistenti).
3. **L - Liskov Substitution Principle (LSP)**: le classi derivate devono poter sostituire le classi base senza rompere il comportamento del programma.
4. **I - Interface Segregation Principle (ISP)**: meglio molte interfacce piccole e specifiche che un'unica interfaccia monolitica piena di metodi non necessari.
5. **D - Dependency Inversion Principle (DIP)**: i moduli di alto livello non devono dipendere dai dettagli di basso livello; entrambi devono dipendere da astrazioni (interfacce).

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```csharp
public sealed record User(string Name);

public static class UserValidator {
    public static bool IsValid(User user) => !string.IsNullOrWhiteSpace(user.Name);
}

public interface IUserRepository {
    void Save(User user);
}
```

### Seguilo passo per passo

1. Nel frammento SRP, `UserValidator` decide se i dati sono validi e `UserRepository` si occupa di salvarli: le responsabilità possono cambiare per motivi diversi.
2. La strategia `IDiscountStrategy` dell'esempio guida offre un contratto comune; `NoDiscount` ne è una implementazione concreta.
3. Il chiamante può dipendere dall'interfaccia e ricevere una strategia, invece di conoscere ogni classe concreta. Questo illustra Open/Closed e Dependency Inversion senza dimostrare da solo tutti i principi.
4. Aggiungi una strategia di sconto senza modificare il chiamante. Poi controlla che un sostituto rispetti lo stesso contratto e che l'interfaccia non obblighi classi a implementare metodi irrilevanti.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public interface IDiscountStrategy { decimal ApplyDiscount(decimal price); }
public class NoDiscount : IDiscountStrategy { public decimal ApplyDiscount(decimal p) => p; }
public class HalfPriceDiscount : IDiscountStrategy { public decimal ApplyDiscount(decimal p) => p * 0.5m; }
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Creare 'God Objects' (classi monolitiche con migliaia di righe che fanno tutto: routing, DB, validazione e UI)
- violare il principio di inversione delle dipendenze istanziando direttamente classi concrete.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quale principio SOLID viene violato quando una classe esegue contemporaneamente calcoli di business e interrogazioni dirette al database?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
