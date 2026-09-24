# Classi, Record e Costruttori Primari

## In parole semplici

L'obiettivo di questa lezione è confrontare class e record per uguaglianza e sintassi, senza assumere che ogni record sia immutabile in profondità.

I record generano uguaglianza per valore e una sintassi concisa per i dati. Un record posizionale usa proprietà init-only, ma i record non sono immutabili in profondità: membri mutabili e oggetti annidati possono comunque cambiare.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `record`
- `class`
- `costruttore primario`
- `immutabilita`
- `with expression`
- `uguaglianza per valore`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`record`, `class`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public record Customer(int Id, string Name, string Tier) {
    public Customer Upgrade() => this with { Tier = "Gold" };
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Confondere l'uguaglianza dei record (basata sui valori) con quella predefinita delle classi (basata sull'identità del riferimento)
- assumere che un record renda immutabili anche gli oggetti contenuti.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quando preferisci usare un `record` invece di una classica `class` in un'API?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
