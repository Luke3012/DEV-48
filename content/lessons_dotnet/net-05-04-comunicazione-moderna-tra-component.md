# Comunicazione moderna tra componenti: input() e output()

## In parole semplici

L'obiettivo di questa lezione è passare dati e notificare eventi tra componenti con i moderni signal inputs e output().

`input()` dichiara un input leggibile come Signal; `output()` dichiara un evento che il componente può emettere. Sono API moderne alternative: i decoratori `@Input()` e `@Output()` restano supportati.

## Le parole da riconoscere

- `input()`
- `input.required`
- `output()`
- `model()`
- `Input`
- `Output`
- `comunicazione`

## Anatomia e Sintassi del Codice

### Input basati su Signal ed eventi output:
```typescript
import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-user-badge',
  standalone: true,
  template: `
    <span (click)="deleteUser()">{{ name() }} ({{ role() }})</span>
  `
})
export class UserBadgeComponent {
  // Input standard con valore di default
  role = input('Guest');

  // Input obbligatorio che il genitore DEVE passare
  name = input.required<string>();

  // Output moderno per emettere eventi verso il genitore
  deleted = output<string>();

  deleteUser() {
    this.deleted.emit(this.name());
  }
}
```

## Un esempio concreto

```typescript
export class CardComponent {
  title = input.required<string>();
  selected = output<number>();
  onSelect(id: number) { this.selected.emit(id); }
}
```

### Seguilo passo per passo

1. `input.required<string>()` dichiara che il genitore deve fornire `title`; nel template il componente legge il valore con `title()`.
2. `output<number>()` dichiara un evento che trasporta un numero; non è un Signal che conserva lo stato.
3. `onSelect(id)` emette l'id con `selected.emit(id)`. Il genitore può ascoltarlo e decidere come aggiornare il proprio stato.
4. Prova a omettere `title` nel genitore e verifica il controllo Angular. Poi emetti un id diverso e controlla che arrivi al gestore del genitore.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class UserBadgeModel {
    role = input('Guest');
    name = input('Utente');
    selected = output<string>();
    select() { this.selected.emit(this.name()); }
}
```

## Dove ci si confonde spesso

- Trattare `output()` come un Signal: è un'API per emettere eventi, mentre `input()` fornisce un input leggibile come Signal. I decoratori `@Input()` e `@Output()` restano disponibili
- in un componente bisogna seguire lo stile già adottato.

## Domanda di verifica

> Che cosa restituiscono `input()` e `output()`, e quale compito svolge ciascuno?
