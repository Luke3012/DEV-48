# Classi, Record e Costruttori Primari

I record generano uguaglianza per valore e una sintassi concisa per i dati. Un record posizionale usa proprietà init-only, ma i record non sono immutabili in profondità: membri mutabili e oggetti annidati possono comunque cambiare.

## Dal problema alla regola del linguaggio

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

## Traccia i valori nel programma

```csharp
public record SubjectDto(int Id, string Name, string Zone);

var s1 = new SubjectDto(1, "Mario", "Centro");
var s2 = s1 with { Zone = "Nord" }; // Crea copia modificata senza mutare s1
```

### Calcola il risultato prima di eseguirlo

1. `new SubjectDto(1, "Mario", "Centro")` crea un record con tre proprietà inizializzate.
2. L'espressione `s1 with { Zone = "Nord" }` crea un nuovo record copiando gli altri valori e cambiando solo `Zone`.
3. `s1` conserva `"Centro"`; `s2` contiene `"Nord"`. I record confrontano i valori dichiarati, ma la copia è superficiale se una proprietà contiene un oggetto mutabile.
4. Confronta `s1` con un altro record creato con gli stessi tre valori. Poi cambia un valore e prevedi come cambia l'uguaglianza.

## Prova una seconda forma

```csharp
public record Customer(int Id, string Name, string Tier) {
    public Customer Upgrade() => this with { Tier = "Gold" };
}
```

## Casi che cambiano il risultato

- Confondere l'uguaglianza dei record (basata sui valori) con quella predefinita delle classi (basata sull'identità del riferimento)
- assumere che un record renda immutabili anche gli oggetti contenuti.

> **Che cosa succede se cambia l'input?** Quando preferisci usare un `record` invece di una classica `class` in un'API?
