# Deferrable Views: ottimizzazione con @defer

## In parole semplici

L'obiettivo di questa lezione è rinviare il caricamento di componenti pesanti nel browser con la direttiva nativa @defer.

Le Deferrable Views possono caricare alcune dipendenze solo quando una condizione è soddisfatta. Il beneficio sul codice iniziale dipende dai componenti e dalle altre importazioni dell'app.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `@defer`
- `@placeholder`
- `@loading`
- `@error`
- `lazy loading template`
- `on viewport`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`@defer`, `@placeholder`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class DeferSimulator {
    isLoaded = signal(false);
    triggerLoad() { this.isLoaded.set(true); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare di fornire un `@placeholder` lasciando uno spazio vuoto che causa salti di layout (Cumulative Layout Shift)
- usare `@defer` per componenti critici 'above the fold'.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quale problema risolve il blocco `@placeholder` all'interno di una Deferrable View?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
