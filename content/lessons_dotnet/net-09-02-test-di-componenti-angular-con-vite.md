# Testare componenti Angular con Vitest e TestBed

Un componente Angular dipende da template, injector e ciclo di rendering. Costruirlo con `new` non prepara queste parti: `TestBed` configura il contesto, `ComponentFixture` guida il rendering e il test osserva ciò che compare nel DOM dopo un'azione.

## Il comportamento che vogliamo proteggere

### Il test segue l'uso della persona
Componente standalone:
```typescript
@Component({
  selector: 'app-counter',
  template: '<p data-count>{{ count() }}</p><button (click)="increment()">Aggiungi</button>'
})
export class CounterComponent {
  readonly count = signal(0);
  increment(): void { this.count.update(value => value + 1); }
}
```

Spec eseguita da Vitest:
```typescript
import { TestBed } from '@angular/core/testing';
import { CounterComponent } from './counter.component';

describe('CounterComponent', () => {
  it('mostra il conteggio dopo un click', async () => {
    // Arrange: prepara import Angular e crea l'istanza.
    await TestBed.configureTestingModule({ imports: [CounterComponent] }).compileComponents();
    const fixture = TestBed.createComponent(CounterComponent);
    fixture.detectChanges();

    // Act
    (fixture.nativeElement.querySelector('button') as HTMLButtonElement).click();
    fixture.detectChanges();

    // Assert: controlla il risultato visibile.
    expect(fixture.nativeElement.querySelector('[data-count]').textContent).toContain('1');
  });
});
```

`TestBed` crea il contesto d'iniezione e risolve i componenti dichiarati in `imports`; `createComponent` restituisce fixture e istanza; `detectChanges()` applica lo stato al DOM. Se il componente usa un service, fornisci un mock con `providers` e osserva l'effetto dell'azione, non un dettaglio privato.

## Prepara, esegui, osserva

```typescript
fixture.nativeElement.querySelector('button').click();
fixture.detectChanges();
expect(fixture.nativeElement.textContent).toContain('1');
```

### Rendi riproducibile il comportamento

1. Arrange importa il componente standalone nel modulo di test e crea una fixture.
2. Il primo `detectChanges()` renderizza il valore iniziale e collega l'handler del pulsante.
3. Act clicca il pulsante: il metodo aggiorna il Signal; un nuovo ciclo applica il testo aggiornato al DOM.
4. Assert cerca `1` nell'elemento visibile. Se il test osserva ancora `0`, controlla prima evento, Signal e ciclo di rendering; se usa un service, verifica che il provider di test sia stato registrato.

Nel laboratorio TestBed verifica il DOM dopo un'interazione e aggiungi un caso che riproduce il difetto iniziale. Il runner dell'esercizio breve non compila il template Angular.

## Che cosa rende il difetto osservabile?

- Testare solo metodi privati senza osservare il DOM
- dimenticare di attivare la change detection quando serve
- costruire direttamente un componente Angular che usa dipendenze Angular.

> **Quale evidenza dimostra il comportamento?** Quali parti di Angular prepara TestBed quando crea un componente per il test?
