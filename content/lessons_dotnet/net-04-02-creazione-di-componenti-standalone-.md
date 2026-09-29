# Creazione di componenti Standalone con @Component

## In parole semplici

L'obiettivo di questa lezione è definire componenti Standalone con decoratore @Component, imports espliciti e stili isolati.

Un componente Standalone dichiara nel proprio decoratore quali componenti, pipe o direttive usa. Le dipendenze esplicite rendono più chiari il template e il contesto di test.

## Le parole da riconoscere

- `standalone: true`
- `imports`
- `template`
- `styles`
- `selettore`
- `incapsulamento`

## Anatomia e Sintassi del Codice

### Anatomia del decoratore @Component:
```typescript
import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="card">
      <h3>{{ username() }}</h3>
    </div>
  `,
  styles: [`
    .card { padding: 1rem; border-radius: 8px; border: 1px solid #ccc; }
  `]
})
export class UserCardComponent {
  username = signal('Mario Rossi');
}
```

## Un esempio concreto

```typescript
@Component({
  selector: 'app-card',
  standalone: true,
  template: `<h3>{{ title() }}</h3>`
})
export class CardComponent { title = signal('Titolo'); }
```

### Seguilo passo per passo

1. `@Component` descrive il selettore e il template che Angular collega alla classe `CardComponent`.
2. Il template legge `title()` perché `title` è un Signal; le parentesi chiamano il getter del valore corrente.
3. Quando il genitore usa `<app-card>`, Angular crea il componente e mostra il titolo. Se il template usa altri componenti o pipe, il loro import va dichiarato.
4. Cambia il valore iniziale del Signal e prevedi il testo. Poi prova a leggere `title` senza parentesi e confronta il risultato col template.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class UserProfileComponent {
    name = signal('Ospite');
    setName(newName: string) { this.name.set(newName); }
}
```

## Dove ci si confonde spesso

- Dimenticare di inserire i componenti figli nell'array `imports` del decoratore `@Component`
- usare selettori generici che collidono con tag HTML standard.

## Domanda di verifica

> Cosa accade se utilizzi un componente figlio nel template senza averlo aggiunto nell'array `imports`?
