# Deferrable Views: ottimizzazione con @defer

Le Deferrable Views possono caricare alcune dipendenze solo quando una condizione è soddisfatta. Il beneficio sul codice iniziale dipende dai componenti e dalle altre importazioni dell'app.

## La vista che vogliamo costruire

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

## Segui il dato fino al DOM

```html
@defer (on viewport) {
  <app-metrics-chart />
} @placeholder {
  <div>Caricamento al rendering...</div>
}
```

### Dal modello alla schermata

1. Prima che la vista entri nel viewport, `@placeholder` mostra un contenuto leggero al posto del grafico.
2. Quando la condizione `on viewport` si attiva, Angular carica il componente differito e sostituisce il placeholder.
3. Il caricamento ritardato può ridurre il codice iniziale solo se le dipendenze della vista sono effettivamente separabili e non vengono caricate altrove.
4. Prova `on interaction` e confronta quando parte il caricamento. Evita di differire un contenuto necessario subito o di lasciare uno stato vuoto senza indicazione.

## Modifica lo stesso componente

Il runner modella la condizione di caricamento, ma non crea un chunk né misura il bundle. Verifica il caricamento differito con build e Network nel tuo progetto Angular.

```typescript
export class DeferSimulator {
    isLoaded = signal(false);
    triggerLoad() { this.isLoaded.set(true); }
}
```

## Che cosa deve conoscere il template?

- Dimenticare di fornire un `@placeholder` lasciando uno spazio vuoto che causa salti di layout (Cumulative Layout Shift)
- usare `@defer` per componenti critici 'above the fold'.

> **Che cosa collega classe e vista?** Quale problema risolve il blocco `@placeholder` all'interno di una Deferrable View?
