# Testare componenti Angular con Vitest e TestBed

## In parole semplici

L'obiettivo di questa lezione è usare Vitest e TestBed per creare un componente standalone e verificare il comportamento osservabile nel DOM.

Vitest esegue i test; TestBed crea il contesto Angular e ComponentFixture permette di osservare il componente e il suo DOM. Un test di componente verifica ciò che vede o fa l'utente, non solo una classe costruita con `new`.

## Le parole da riconoscere

- `vitest`
- `testbed`
- `componentfixture`
- `dom`
- `expect`
- `change detection`

## Anatomia e Sintassi del Codice

### Test di un componente Standalone con TestBed:
```typescript
import { TestBed } from '@angular/core/testing';
import { CounterComponent } from './counter.component';

describe('CounterComponent', () => {
  it('mostra il valore e lo aggiorna dopo un click', async () => {
    await TestBed.configureTestingModule({ imports: [CounterComponent] }).compileComponents();
    const fixture = TestBed.createComponent(CounterComponent);
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.querySelector('[data-count]')?.textContent).toContain('0');
    element.querySelector('button')?.click();
    fixture.detectChanges();
    expect(element.querySelector('[data-count]')?.textContent).toContain('1');
  });
});
```

## Un esempio concreto

```text
describe('Component', () => {
  it('mostra il titolo nel DOM', async () => {
    await TestBed.configureTestingModule({ imports: [MyComponent] }).compileComponents();
    const fixture = TestBed.createComponent(MyComponent);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Home');
  });
});
```

### Seguilo passo per passo

1. `TestBed.configureTestingModule({ imports: [MyComponent] })` prepara il contesto Angular e importa il componente standalone.
2. `createComponent` crea il componente; `detectChanges()` esegue il primo ciclo e aggiorna il DOM.
3. L'asserzione cerca il titolo nell'interfaccia visibile. Il test osserva ciò che la persona usa, non un metodo privato isolato.
4. Cambia un input o clicca un pulsante, attiva di nuovo la change detection e verifica il nuovo DOM. Se il componente usa servizi, fornisci un mock esplicito.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Testare solo metodi privati senza osservare il DOM
- dimenticare di attivare la change detection quando serve
- costruire direttamente un componente Angular che usa dipendenze Angular.

## Domanda di verifica

> Quali parti di Angular prepara TestBed quando crea un componente per il test?
