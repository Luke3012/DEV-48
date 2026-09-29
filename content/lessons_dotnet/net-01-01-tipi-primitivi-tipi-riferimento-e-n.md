# Tipi primitivi, tipi riferimento e nullable in C#

## In parole semplici

L'obiettivo di questa lezione è riconoscere tipi valore e riferimento, usare nullable e leggere i warning di nullabilità senza basarsi su una regola stack/heap.

Un tipo valore viene copiato come valore; una variabile di tipo riferimento contiene un riferimento a un oggetto. La posizione fisica in memoria dipende dal contesto: non si può dedurre soltanto dalla categoria del tipo.

## Le parole da riconoscere

- `int`
- `string`
- `bool`
- `tipo valore`
- `tipo riferimento`
- `nullable`
- `operatore null-coalescing`

## Anatomia e Sintassi del Codice

### Tipi Valore vs Tipi Riferimento:
- **Tipi Valore (`struct`)**: `int`, `double`, `bool`, `DateTime`, `decimal`.
  - Una copia della variabile copia il valore. I tipi valore non sono `null` per impostazione predefinita.
  - Per renderli nullable, si aggiunge `?`: `int? age = null;`.
- **Tipi Riferimento (`class`)**: `string`, `object`, classi personalizzate, array.
  - La variabile contiene un riferimento; copiare la variabile copia il riferimento, non l'oggetto.
  - Con i **Nullable Reference Types** abilitati, `string` dichiara l'intenzione di non usare `null`, mentre `string?` dichiara che `null` è previsto. Sono controlli statici del compilatore, non una protezione runtime.

### Operatori per gestire `null`:
- **Null-coalescing (`??`)**: `name ?? "Default"` restituisce `name` se valorizzato, altrimenti `"Default"`.
- **Null-conditional (`?.`)**: `user?.Address?.City` accede alla proprietà solo se `user` e `Address` non sono null, evitando `NullReferenceException`.

## Un esempio concreto

```text
string? name = null;
string displayName = name ?? "Utente Ospite";
int age = 25;
Console.WriteLine($"{displayName} ha {age} anni");
```

### Seguilo passo per passo

1. Assegna `null` a `name`: con nullable reference types attivi, `string?` dichiara esplicitamente che l'assenza è prevista.
2. L'operatore `??` sceglie `"Utente Ospite"` solo quando `name` è `null`; altrimenti conserva il nome ricevuto.
3. `age` è un `int` e vale `25`; l'interpolazione inserisce entrambi i valori nella frase stampata.
4. Sostituisci `null` con `"Ada"` e controlla il risultato. Prova anche `int? age = null`: il punto interrogativo ha un ruolo diverso per un tipo valore.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
public static class UserFormatter {
    public static string FormatName(string? firstName, string? lastName) {
        var first = firstName?.Trim();
        var last = lastName?.Trim();
        if (string.IsNullOrEmpty(first) && string.IsNullOrEmpty(last)) return "Anonimo";
        return $"{first} {last}".Trim();
    }
}
```

## Dove ci si confonde spesso

- Ignorare i warning sui nullable reference types (`string?`)
- dimenticare che i tipi valore non possono essere null a meno di dichiararli esplicitamente con `?`.

## Domanda di verifica

> Qual è la differenza fondamentale tra un tipo per valore e un tipo per riferimento in C#?
