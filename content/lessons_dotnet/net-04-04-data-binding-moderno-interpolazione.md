# Data Binding moderno: interpolazione, property ed event binding

## In parole semplici

L'obiettivo di questa lezione è connettere classe e template con interpolazione `{{ }}`, property binding `[prop]` ed event binding `(event)`.

Il data binding permette lo scambio continuo di dati e interazioni tra l'interfaccia HTML nel browser e la classe TypeScript del componente.

## Le parole da riconoscere

- `interpolazione`
- `property binding`
- `event binding`
- `two way binding`
- `signal call`

## Anatomia e Sintassi del Codice

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

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class SearchBarComponent {
    query = signal('');
    setQuery(text: string) { this.query.set(text.trim()); }
    clear() { this.query.set(''); }
}
```

## Dove ci si confonde spesso

- Dimenticare le parentesi tonde quando si legge un segnale nel template (`{{ name }}` invece di `{{ name() }}`)
- usare property binding quando serve event binding.

## Domanda di verifica

> Perché quando si legge un Signal in un template Angular bisogna includere le parentesi tonde `()`?
