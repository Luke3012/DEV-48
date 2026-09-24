# Creazione di componenti Standalone con @Component

## In parole semplici

L'obiettivo di questa lezione è definire componenti Standalone con decoratore @Component, imports espliciti e stili isolati.

Un componente Standalone dichiara nel proprio decoratore quali componenti, pipe o direttive usa. Le dipendenze esplicite rendono più chiari il template e il contesto di test.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `standalone: true`
- `imports`
- `template`
- `styles`
- `selettore`
- `incapsulamento`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`standalone: true`, `imports`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class UserProfileComponent {
    name = signal('Ospite');
    setName(newName: string) { this.name.set(newName); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare di inserire i componenti figli nell'array `imports` del decoratore `@Component`
- usare selettori generici che collidono con tag HTML standard.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Cosa accade se utilizzi un componente figlio nel template senza averlo aggiunto nell'array `imports`?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
