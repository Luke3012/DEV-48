# Data Binding moderno: interpolazione, property ed event binding

## In parole semplici

L'obiettivo di questa lezione è connettere classe e template con interpolazione `{{ }}`, property binding `[prop]` ed event binding `(event)`.

Il data binding permette lo scambio continuo di dati e interazioni tra l'interfaccia HTML nel browser e la classe TypeScript del componente.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `interpolazione`
- `property binding`
- `event binding`
- `two way binding`
- `signal call`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`interpolazione`, `property binding`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Le 3 Forme Fondamentali di Binding:
1. **Interpolazione `{{ espressione }}`**:
   - Inserisce testo dinamico nel DOM: `<h1>{{ title() }}</h1>`.
   - Con i Signals si invoca il segnale con le parentesi tonde `()`!
2. **Property Binding `[proprieta]="espressione"`**:
   - Collega un valore a una proprietà del DOM o a un input di un componente figlio:
     `<button [disabled]="isSubmitting()">Invia</button>`.
3. **Event Binding `(evento)="gestore()"`**:
   - Intercetta azioni dell'utente (click, input, submit):
     `<button (click)="increment()">Aggiungi</button>`.

```html
<input [value]="query()" (input)="onSearch($event)" />
<p>Risultati per: {{ query() }}</p>
```

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```html
<button [disabled]="!isValid()" (click)="onSubmit()">Salva</button>
<input [value]="searchTerm()" (input)="updateSearch($event)" />
```

### Seguilo passo per passo

1. `[disabled]="!isValid()"` imposta la proprietà DOM `disabled` in base allo stato del componente; quando il form non è valido, il pulsante non è attivabile.
2. `(click)="onSubmit()"` ascolta un evento del browser e chiama il metodo TypeScript.
3. Nell'input, `[value]` mostra il valore del Signal `searchTerm()`; `(input)` chiama `updateSearch($event)` quando la persona scrive.
4. Simula `isValid()` prima falso e poi vero. Digita nel campo e verifica che l'handler trasferisca il nuovo testo nel componente.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class SearchBarComponent {
    query = signal('');
    setQuery(text: string) { this.query.set(text.trim()); }
    clear() { this.query.set(''); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare le parentesi tonde quando si legge un segnale nel template (`{{ name }}` invece di `{{ name() }}`)
- usare property binding quando serve event binding.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché quando si legge un Signal in un template Angular bisogna includere le parentesi tonde `()`?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
