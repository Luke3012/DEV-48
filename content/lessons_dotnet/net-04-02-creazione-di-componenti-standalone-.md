# Creazione di componenti Standalone con @Component

Un componente nasce quando una parte della schermata ha dati, interazioni o responsabilità visive proprie. La classe contiene stato e metodi; `@Component` dice ad Angular quale selettore, template, stile e dipendenze assemblare.

## La vista che vogliamo costruire

### Un componente e il punto in cui viene usato
```text
src/app/user-card/user-card.ts   classe, stato e metodi
src/app/user-card/user-card.css  stile della scheda
src/app/app.ts                   componente genitore che importa la scheda
```

```typescript
// src/app/user-card/user-card.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [],
  template: `
    <article class="card">
      <h2>{{ username }}</h2>
      <button type="button" (click)="clearName()">Pulisci</button>
    </article>
  `,
  styleUrl: './user-card.css'
})
export class UserCardComponent {
  username = 'Luca';

  clearName(): void {
    this.username = '';
  }
}
```

Il genitore rende disponibile il figlio nel suo template importandolo:
```typescript
@Component({
  selector: 'app-root',
  imports: [UserCardComponent],
  template: '<app-user-card />'
})
export class App {}
```

Il selector deve corrispondere al tag usato dal genitore. Ogni direttiva, pipe o componente non nativo usato nel template appartiene a `imports`; `styles` o `styleUrl` definiscono l'aspetto associato. In Angular moderno la classe standalone è il default, mentre `standalone: true` rende esplicita l'intenzione nell'esempio. `NgModule` resta supportato nei progetti esistenti: lì i componenti non standalone si dichiarano nel modulo, mentre un componente standalone si importa. Qui seguiamo la struttura corrente senza cancellare il modello che incontrerai nel codice legacy.

## Segui il dato fino al DOM

```typescript
username = 'Luca';
clearName(): void { this.username = ''; }
```

### Dal modello alla schermata

1. Angular crea `App` come radice e legge `<app-user-card>` nel template.
2. Poiché `App` dichiara `UserCardComponent` in `imports`, il selettore trova una definizione e Angular crea quell'istanza figlia.
3. Il template figlio legge `username`; il click chiama `clearName()`, che cambia lo stato della classe.
4. Angular aggiorna la vista e il titolo diventa vuoto. Se togli il figlio da `imports`, il template non può risolvere il selettore e la compilazione segnala l'elemento sconosciuto.

Il runner controlla il modello TypeScript isolato; nel laboratorio Catalogo Standalone, verifica anche che il componente figlio venga importato e che il DOM reagisca al click.

## Che cosa deve conoscere il template?

- Dimenticare di inserire i componenti figli nell'array `imports` del decoratore `@Component`
- usare selettori generici che collidono con tag HTML standard.

> **Che cosa collega classe e vista?** Cosa accade se utilizzi un componente figlio nel template senza averlo aggiunto nell'array `imports`?
