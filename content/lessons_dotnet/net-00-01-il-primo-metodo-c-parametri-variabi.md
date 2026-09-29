# Il primo metodo C#: parametri, variabili e valore restituito

## In parole semplici

L'obiettivo di questa lezione è leggere e scrivere un metodo C# semplice, riconoscendone input, istruzioni e risultato.

Un metodo è una parte nominata del programma: può ricevere dati attraverso i parametri e restituire un risultato. La classe raccoglie metodi correlati; per questo primo esempio non serve ancora conoscere oggetti o database.

### Nel percorso

Per eseguire l'esempio fuori dall'editor, crea un progetto con `dotnet new console -n FirstMethod`, entra con `cd FirstMethod`, sostituisci `Program.cs` con il codice dell'esempio ed esegui `dotnet run`. Nell'editor dell'esercizio scrivi soltanto la classe richiesta: il runner fornisce il chiamante.

## Le parole da riconoscere

- `programma`
- `classe`
- `metodo`
- `parametro`
- `variabile`
- `return`
- `string`

## Anatomia e Sintassi del Codice

### Leggere la firma di un metodo
```csharp
public static string SayHello(string name)
```
- `public` rende il metodo accessibile da altre classi.
- `static` permette di chiamarlo sulla classe senza creare un oggetto.
- `string` prima del nome è il tipo del risultato.
- `name` è un parametro: il valore arriva a ogni chiamata.

Il corpo tra `{ }` contiene istruzioni. `return` termina il metodo e consegna il valore al chiamante.

## Un esempio concreto

```csharp
var greeting = Greeter.SayHello("Ada");
Console.WriteLine(greeting);

public static class Greeter {
    public static string SayHello(string name) {
        var message = "Ciao, " + name + "!";
        return message;
    }
}
```

### Seguilo passo per passo

1. Nella chiamata `Greeter.SayHello("Ada")`, il testo `Ada` è l'argomento che riempie il parametro `name`.
2. Dentro il metodo, la stringa viene unita a `"Ciao, "` e a `"!"`; il risultato diventa il valore della variabile locale `message`.
3. `return message` riporta `Ciao, Ada!` al punto chiamante, che lo assegna a `greeting` e lo stampa.
4. Prova un nome vuoto e poi un nome con spazi: il metodo concatena i caratteri ricevuti, non li valida né li ripulisce.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
public static class TextTools {
    public static string JoinWithComma(string first, string second) {
        return first + ", " + second;
    }
}
```

## Dove ci si confonde spesso

- Dimenticare `return`
- restituire un tipo diverso da quello dichiarato
- chiamare un metodo statico come se servisse un oggetto.

## Domanda di verifica

> Che cosa riceve un metodo tramite un parametro e che cosa consegna tramite `return`?
