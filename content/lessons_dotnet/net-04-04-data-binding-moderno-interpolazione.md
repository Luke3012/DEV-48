# Data Binding moderno: interpolazione, property ed event binding

Un input deve mostrare il valore corrente del componente e riportare al componente quello che la persona scrive. Il binding non è una collezione di parentesi da memorizzare: è la descrizione della direzione con cui viaggia ogni dato.

## La vista che vogliamo costruire

### Costruiamo la stessa schermata in passaggi
All'inizio la classe contiene soltanto stato e azione:
```typescript
username = 'Luca';

clear(): void {
  this.username = '';
}
```

Il testo scende dalla classe al template con l'interpolazione:
```html
<p>{{ username }}</p>
```

Il property binding manda il valore alla proprietà DOM `value`; l'event binding riporta l'input al componente:
```html
<input [value]="username" (input)="updateName($event)" />
<button type="button" (click)="clear()">Pulisci</button>
```
```typescript
updateName(event: Event): void {
  this.username = (event.target as HTMLInputElement).value;
}
```

Per un controllo di form, `[(ngModel)]` abbrevia il binding in entrambe le direzioni e richiede `FormsModule` negli `imports` del componente standalone:
```html
<input [(ngModel)]="username" aria-label="Nome utente" />
```
```text
Component → Template: {{ username }} e [value]
Template → Component: (input), (click)
Component ↔ Controllo: [(ngModel)]
```

Nel codice applicativo usa una sola strategia per quel controllo: i frammenti mostrano come si evolve il modello, non tre input da sovrapporre nella stessa schermata.

## Segui il dato fino al DOM

```html
<input [(ngModel)]="username" aria-label="Nome utente" />
<p>{{ username }}</p>
```

### Dal modello alla schermata

1. La classe inizializza `username` a `Luca`; interpolazione e property binding mostrano quel valore nel DOM.
2. Quando arriva `input`, il browser fornisce l'evento. Il metodo legge il testo dall'elemento e aggiorna la proprietà della classe.
3. Angular aggiorna il testo interpolato e il valore legato. Con `[(ngModel)]`, la direttiva coordina in breve le due direzioni.
4. Clicca Pulisci: l'evento chiama il metodo, la classe imposta `''` e la vista riflette il nuovo stato. Rimuovi `FormsModule` e osserva l'errore sul binding `ngModel`.

Il runner breve verifica la logica del componente, non il template. Nel laboratorio Standalone, controlla il valore iniziale, digita, cancella e osserva l'input e il DOM dopo ogni evento.

## Che cosa deve conoscere il template?

- Dimenticare le parentesi tonde quando si legge un segnale nel template (`{{ name }}` invece di `{{ name() }}`)
- usare property binding quando serve event binding.

> **Che cosa collega classe e vista?** Perché quando si legge un Signal in un template Angular bisogna includere le parentesi tonde `()`?
