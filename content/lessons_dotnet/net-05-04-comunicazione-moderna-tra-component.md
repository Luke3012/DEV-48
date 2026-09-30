# Comunicazione moderna tra componenti: input() e output()

`input()` dichiara un input leggibile come Signal; `output()` dichiara un evento che il componente può emettere. Sono API moderne alternative: i decoratori `@Input()` e `@Output()` restano supportati.

## Quale dato è sorgente e quale è derivato?

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

## Osserva come si propaga un aggiornamento

```typescript
export class CardComponent {
  title = input.required<string>();
  selected = output<number>();
  onSelect(id: number) { this.selected.emit(id); }
}
```

### Segui la modifica fino alla vista

1. `input.required<string>()` dichiara che il genitore deve fornire `title`; nel template il componente legge il valore con `title()`.
2. `output<number>()` dichiara un evento che trasporta un numero; non è un Signal che conserva lo stato.
3. `onSelect(id)` emette l'id con `selected.emit(id)`. Il genitore può ascoltarlo e decidere come aggiornare il proprio stato.
4. Prova a omettere `title` nel genitore e verifica il controllo Angular. Poi emetti un id diverso e controlla che arrivi al gestore del genitore.

## Prova una modifica senza mutare i dati

La pratica breve modella dati ed eventi; verifica il collegamento reale tra genitore e figlio nel componente del laboratorio Standalone.

```typescript
export class UserBadgeModel {
    role = input('Guest');
    name = input('Utente');
    selected = output<string>();
    select() { this.selected.emit(this.name()); }
}
```

## Quando usare un calcolo o un effetto

- Trattare `output()` come un Signal: è un'API per emettere eventi, mentre `input()` fornisce un input leggibile come Signal. I decoratori `@Input()` e `@Output()` restano disponibili
- in un componente bisogna seguire lo stile già adottato.

> **Quali dipendenze vengono lette?** Che cosa restituiscono `input()` e `output()`, e quale compito svolge ciascuno?
