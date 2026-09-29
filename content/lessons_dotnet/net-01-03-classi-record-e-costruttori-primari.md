# Classi, Record e Costruttori Primari

## In parole semplici

L'obiettivo di questa lezione è confrontare class e record per uguaglianza e sintassi, senza assumere che ogni record sia immutabile in profondità.

I record generano uguaglianza per valore e una sintassi concisa per i dati. Un record posizionale usa proprietà init-only, ma i record non sono immutabili in profondità: membri mutabili e oggetti annidati possono comunque cambiare.

## Le parole da riconoscere

- `record`
- `class`
- `costruttore primario`
- `immutabilita`
- `with expression`
- `uguaglianza per valore`

## Anatomia e Sintassi del Codice

### Differenze tra `class` e `record`:
- **`class`**: Uguaglianza per riferimento (due istanze con le stesse proprietà sono diverse in memoria). Pensata per oggetti con stato mutabile e logica di business complessa.
- **`record`**: implementa uguaglianza per valore. Due record con gli stessi valori confrontati con `==` risultano uguali.
  - Le proprietà di un record posizionale sono normalmente `init`-only; un record può comunque contenere membri mutabili o riferimenti a oggetti mutabili.
  - L'espressione `with` crea una copia superficiale e permette di sostituire proprietà:
    `var updated = original with { Price = 29.99m };`

### Sintassi del Costruttore Primario:
```csharp
// Record posizionale: uguaglianza per valore e proprietà init-only.
public record ProductDto(int Id, string Title, decimal Price);
```

## Un esempio concreto

```csharp
public record SubjectDto(int Id, string Name, string Zone);

var s1 = new SubjectDto(1, "Mario", "Centro");
var s2 = s1 with { Zone = "Nord" }; // Crea copia modificata senza mutare s1
```

### Seguilo passo per passo

1. `new SubjectDto(1, "Mario", "Centro")` crea un record con tre proprietà inizializzate.
2. L'espressione `s1 with { Zone = "Nord" }` crea un nuovo record copiando gli altri valori e cambiando solo `Zone`.
3. `s1` conserva `"Centro"`; `s2` contiene `"Nord"`. I record confrontano i valori dichiarati, ma la copia è superficiale se una proprietà contiene un oggetto mutabile.
4. Confronta `s1` con un altro record creato con gli stessi tre valori. Poi cambia un valore e prevedi come cambia l'uguaglianza.

## Pattern Guida per gli Esercizi

Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava.

```csharp
public record Customer(int Id, string Name, string Tier) {
    public Customer Upgrade() => this with { Tier = "Gold" };
}
```

## Dove ci si confonde spesso

- Confondere l'uguaglianza dei record (basata sui valori) con quella predefinita delle classi (basata sull'identità del riferimento)
- assumere che un record renda immutabili anche gli oggetti contenuti.

## Domanda di verifica

> Quando preferisci usare un `record` invece di una classica `class` in un'API?
