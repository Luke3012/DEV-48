# Il primo metodo C#: parametri, variabili e valore restituito

## In parole semplici

L'obiettivo di questa lezione è leggere e scrivere un metodo C# semplice, riconoscendone input, istruzioni e risultato.

Un metodo è una parte nominata del programma: può ricevere dati attraverso i parametri e restituire un risultato. La classe raccoglie metodi correlati; per questo primo esempio non serve ancora conoscere oggetti o database.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `programma`
- `classe`
- `metodo`
- `parametro`
- `variabile`
- `return`
- `string`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`programma`, `classe`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class TextTools {
    public static string JoinWithComma(string first, string second) {
        return first + ", " + second;
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare `return`
- restituire un tipo diverso da quello dichiarato
- chiamare un metodo statico come se servisse un oggetto.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Che cosa riceve un metodo tramite un parametro e che cosa consegna tramite `return`?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
