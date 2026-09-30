# Reactive Forms: FormGroup e FormControl

Per inviare un profilo servono nome, email ed età. Il form deve ricordare il valore corrente di ogni campo, sapere se l'utente l'ha toccato o modificato e decidere se i dati sono validi; `FormControl` modella un campo e `FormGroup` aggrega l'intero modulo.

### Nel percorso

Da conoscere: [Data Binding moderno: interpolazione, property ed event binding](net-04-04-data-binding-moderno-interpolazione.md).

Il laboratorio Form Reattivo con Validazione Remota collega le regole allo stato reale dei controlli. La panoramica Signal Forms è facoltativa: puoi proseguire con Reactive Forms senza implementare un secondo form.

## Lo stato che l'utente sta costruendo

### Il modello del form vive nel componente
```typescript
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-profile-form',
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <label>Nome <input formControlName="name" /></label>
      @if (form.controls.name.touched && form.controls.name.hasError('required')) {
        <p>Inserisci il nome.</p>
      }

      <label>Email <input type="email" formControlName="email" /></label>
      @if (form.controls.email.touched && form.controls.email.invalid) {
        <p>Controlla l'indirizzo email.</p>
      }

      <label>Età <input type="number" formControlName="age" /></label>
      <button type="submit" [disabled]="form.invalid">Salva</button>
    </form>
  `
})
export class ProfileFormComponent {
  private readonly fb = inject(FormBuilder);
  readonly form = this.fb.nonNullable.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    age: [18, [Validators.min(18)]]
  });

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    const profile = this.form.getRawValue();
    // Invia profile al servizio, poi mostra successo o errore.
  }
}
```

`ReactiveFormsModule` fornisce le direttive del template e va inserito negli `imports` standalone. `value` contiene i dati; `valid`/`invalid` sintetizzano i validator; `touched` indica che il focus è entrato ed è uscito dal controllo; `dirty` indica una modifica rispetto al valore iniziale; `pending` segnala una validazione asincrona in corso. Questi stati permettono di mostrare il messaggio nel momento utile, non al primo rendering.

### Un'alternativa per i nuovi progetti signal-based
Da Angular 22, Signal Forms è stabile e inclusa nel pacchetto `@angular/forms`. Il modello dati diventa un Signal; `form()` costruisce la struttura dei campi e `FormField` la collega ai controlli:
```typescript
import { Component, signal } from '@angular/core';
import { email, form, FormField, required } from '@angular/forms/signals';

@Component({
  selector: 'app-signal-login',
  imports: [FormField],
  template: `<label>Email <input type="email" [formField]="loginForm.email" /></label>`
})
export class SignalLoginComponent {
  readonly model = signal({ email: '' });
  readonly loginForm = form(this.model, path => {
    required(path.email);
    email(path.email);
  });
}
```
Reactive Forms resta stabile ed è una scelta solida, soprattutto per codice esistente o form complessi. Questo percorso insegna quel modello e il laboratorio lo applica; Signal Forms è una panoramica per confrontare i flussi, non un secondo esercizio da completare. [Confronto ufficiale Angular](https://angular.dev/guide/forms/signals/comparison).

## Segui un campo o una navigazione

```typescript
readonly form = this.fb.nonNullable.group({
  name: ['', Validators.required],
  email: ['', [Validators.required, Validators.email]],
  age: [18, Validators.min(18)]
});
```

### Segui la persona mentre completa il flusso

1. All'avvio `name` ed `email` sono vuoti: i controlli sono invalidi, ma `touched` è `false`, quindi gli errori non disturbano prima dell'interazione.
2. L'utente entra nel campo e poi lo lascia: `touched` diventa `true`; se manca il nome, il template mostra il messaggio richiesto.
3. Quando inserisce un'email valida e un'età di almeno 18, i controlli diventano validi e il gruppo aggrega `form.valid === true`. Una verifica remota aggiungerà `pending` mentre aspetta il server.
4. Il submit legge `getRawValue()` solo quando il form è valido. Se il server rifiuta la richiesta, mostra l'errore vicino al form e riattiva il pulsante; non interpretare un errore di rete come validità.

La funzione breve verifica soltanto una regola TypeScript e non istanzia Angular Forms. Il laboratorio collega validator, touched/pending e invio al modello reale del form e ai test TestBed.

## Rendi visibile lo stato che blocca il flusso

- Dimenticare di importare `ReactiveFormsModule` negli `imports` del componente Standalone, provocando l'errore 'formGroup is not a known property of form'.

> **Quale stato decide che cosa accade dopo?** Qual è la differenza fondamentale tra Template-Driven Forms e Reactive Forms in Angular?
