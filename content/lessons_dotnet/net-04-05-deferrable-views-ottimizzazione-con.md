# Deferrable Views: ottimizzazione con @defer

## In parole semplici

L'obiettivo di questa lezione è rinviare il caricamento di componenti pesanti nel browser con la direttiva nativa @defer.

Le Deferrable Views possono caricare alcune dipendenze solo quando una condizione è soddisfatta. Il beneficio sul codice iniziale dipende dai componenti e dalle altre importazioni dell'app.

## Le parole da riconoscere

- `@defer`
- `@placeholder`
- `@loading`
- `@error`
- `lazy loading template`
- `on viewport`

## Anatomia e Sintassi del Codice

### Sintassi dei Blocchi @defer:
```html
@defer (on viewport) {
  <app-heavy-chart [data]="chartData()" />
} @placeholder {
  <div class="skeleton">In attesa che il grafico diventi visibile...</div>
} @loading (minimum 300ms) {
  <div class="spinner">Caricamento grafico in corso...</div>
} @error {
  <div class="alert">Impossibile caricare il componente grafico.</div>
}
```

### Trigger comuni:
- `on viewport`: carica quando l'elemento entra nella schermata visibile (usando IntersectionObserver).
- `on interaction`: carica quando l'utente clicca o tocca l'area.
- `on hover`: carica al passaggio del mouse.
- `when condizione()`: carica in base al valore booleano di un Signal.

## Un esempio concreto

```html
@defer (on viewport) {
  <app-metrics-chart />
} @placeholder {
  <div>Caricamento al rendering...</div>
}
```

### Seguilo passo per passo

1. Prima che la vista entri nel viewport, `@placeholder` mostra un contenuto leggero al posto del grafico.
2. Quando la condizione `on viewport` si attiva, Angular carica il componente differito e sostituisce il placeholder.
3. Il caricamento ritardato può ridurre il codice iniziale solo se le dipendenze della vista sono effettivamente separabili e non vengono caricate altrove.
4. Prova `on interaction` e confronta quando parte il caricamento. Evita di differire un contenuto necessario subito o di lasciare uno stato vuoto senza indicazione.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class DeferSimulator {
    isLoaded = signal(false);
    triggerLoad() { this.isLoaded.set(true); }
}
```

## Dove ci si confonde spesso

- Dimenticare di fornire un `@placeholder` lasciando uno spazio vuoto che causa salti di layout (Cumulative Layout Shift)
- usare `@defer` per componenti critici 'above the fold'.

## Domanda di verifica

> Quale problema risolve il blocco `@placeholder` all'interno di una Deferrable View?
