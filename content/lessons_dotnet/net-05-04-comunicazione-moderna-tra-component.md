# Comunicazione moderna tra componenti: input() e output()

## In parole semplici

L'obiettivo di questa lezione è passare dati e notificare eventi tra componenti con i moderni signal inputs e output().

`input()` dichiara un input leggibile come Signal; `output()` dichiara un evento che il componente può emettere. Sono API moderne alternative: i decoratori `@Input()` e `@Output()` restano supportati.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `input()`
- `input.required`
- `output()`
- `model()`
- `Input`
- `Output`
- `comunicazione`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`input()`, `input.required`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class UserBadgeModel {
    role = input('Guest');
    name = input('Utente');
    selected = output<string>();
    select() { this.selected.emit(this.name()); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Trattare `output()` come un Signal: è un'API per emettere eventi, mentre `input()` fornisce un input leggibile come Signal. I decoratori `@Input()` e `@Output()` restano disponibili
- in un componente bisogna seguire lo stile già adottato.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Che cosa restituiscono `input()` e `output()`, e quale compito svolge ciascuno?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
