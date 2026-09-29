# Principi SOLID applicati allo sviluppo Full-Stack

## In parole semplici

L'obiettivo di questa lezione è applicare i principi Single Responsibility, Open/Closed, Liskov, Interface Segregation e Dependency Inversion.

I principi SOLID guidano la progettazione del software verso classi modulari, a basso accoppiamento e con responsabilità uniche, facili da mantenere ed estendere nel tempo.

## Le parole da riconoscere

- `solid`
- `single responsibility`
- `open closed`
- `liskov`
- `interface segregation`
- `dependency inversion`

## Anatomia e Sintassi del Codice

### I 5 Principi SOLID in breve:
1. **S - Single Responsibility Principle (SRP)**: una classe deve avere una sola ragione per cambiare (es. un componente non deve occuparsi di chiamate HTTP, delega a un Servizio).
2. **O - Open/Closed Principle (OCP)**: aperto all'estensione, chiuso alla modifica (usare interfacce o polimorfismo invece di modificare classi esistenti).
3. **L - Liskov Substitution Principle (LSP)**: le classi derivate devono poter sostituire le classi base senza rompere il comportamento del programma.
4. **I - Interface Segregation Principle (ISP)**: meglio molte interfacce piccole e specifiche che un'unica interfaccia monolitica piena di metodi non necessari.
5. **D - Dependency Inversion Principle (DIP)**: i moduli di alto livello non devono dipendere dai dettagli di basso livello; entrambi devono dipendere da astrazioni (interfacce).

## Un esempio concreto

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

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```csharp
public interface IDiscountStrategy { decimal ApplyDiscount(decimal price); }
public class NoDiscount : IDiscountStrategy { public decimal ApplyDiscount(decimal p) => p; }
public class HalfPriceDiscount : IDiscountStrategy { public decimal ApplyDiscount(decimal p) => p * 0.5m; }
```

## Dove ci si confonde spesso

- Creare 'God Objects' (classi monolitiche con migliaia di righe che fanno tutto: routing, DB, validazione e UI)
- violare il principio di inversione delle dipendenze istanziando direttamente classi concrete.

## Domanda di verifica

> Quale principio SOLID viene violato quando una classe esegue contemporaneamente calcoli di business e interrogazioni dirette al database?
