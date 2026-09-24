# Valori derivati intelligenti con computed()

## In parole semplici

L'obiettivo di questa lezione è creare segnali dipendenti che si ricalcolano automaticamente e memorizzano il risultato.

`computed()` crea un valore derivato in sola lettura. Angular memorizza il calcolo e aggiorna le dipendenze in base ai Signals letti durante l'ultima esecuzione; la funzione viene valutata quando il valore serve.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `computed`
- `derivazione di stato`
- `memoization`
- `funzione pura`
- `dipendenze dinamiche`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`computed`, `derivazione di stato`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Caratteristiche di `computed()`:
1. **Memoization**: `computed()` calcola il valore quando serve e riusa il risultato finché le dipendenze lette non cambiano.
2. **Sola lettura**: un segnale `computed` non espone `.set()` o `.update()`; modifica i segnali sorgente e lascia derivare il valore.
3. **Dipendenze dinamiche**: Angular tiene conto dei Signals letti durante l'ultima esecuzione della funzione. Mantieni il calcolo puro: non aggiornare stato e non avviare richieste al suo interno.

```typescript
const price = signal(100);
const taxRate = signal(0.22);
const totalPrice = computed(() => price() * (1 + taxRate()));
```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```typescript
const items = signal([10, 20, 30]);
const total = computed(() => items().reduce((a, b) => a + b, 0));
const isFreeShipping = computed(() => total() >= 50);
```

### Seguilo passo per passo

1. `items()` restituisce `[10, 20, 30]`; `total` somma gli elementi e produce `60`.
2. `isFreeShipping` legge `total()`: dato che `60 >= 50`, il valore derivato è `true`.
3. `computed()` memorizza il risultato e ricalcola quando cambia un Signal effettivamente letto; non è il posto per chiamate HTTP o aggiornamenti di stato.
4. Aggiungi `5` agli articoli e verifica che il totale diventi `65`. Rimuovi un elemento e controlla come cambia la soglia della spedizione.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class CartStore {
    items = signal<{ price: number; quantity: number }[]>([]);
    total = computed(() => this.items().reduce((sum, item) => sum + item.price * item.quantity, 0));
    hasItems = computed(() => this.items().length > 0);
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Inserire effetti collaterali (chiamate HTTP, manipolazione manuale del DOM) dentro una funzione `computed()` (deve essere rigorosamente pura!).

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché una funzione passata a `computed()` deve essere rigorosamente pura e priva di side-effect?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
