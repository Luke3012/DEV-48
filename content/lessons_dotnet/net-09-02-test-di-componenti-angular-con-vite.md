# Testare componenti Angular con Vitest e TestBed

## In parole semplici

L'obiettivo di questa lezione è usare Vitest e TestBed per creare un componente standalone e verificare il comportamento osservabile nel DOM.

Vitest esegue i test; TestBed crea il contesto Angular e ComponentFixture permette di osservare il componente e il suo DOM. Un test di componente verifica ciò che vede o fa l'utente, non solo una classe costruita con `new`.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `vitest`
- `testbed`
- `componentfixture`
- `dom`
- `expect`
- `change detection`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`vitest`, `testbed`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class TestResultSummary {
    passed = signal(0);
    failed = signal(0);
    recordPass() { this.passed.update(n => n + 1); }
    recordFail() { this.failed.update(n => n + 1); }
    isAllPassed = computed(() => this.failed() === 0 && this.passed() > 0);
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Testare solo metodi privati senza osservare il DOM
- dimenticare di attivare la change detection quando serve
- costruire direttamente un componente Angular che usa dipendenze Angular.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quali parti di Angular prepara TestBed quando crea un componente per il test?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
