# Reactive Forms: FormGroup e FormControl

## In parole semplici

L'obiettivo di questa lezione è costruire form reattivi complessi e controllati gestendo stato, valori e validità dal TypeScript.

Reactive Forms mantengono valori, stato e validatori in un modello TypeScript esplicito; sono ancora una scelta solida per form complessi e codice esistente. Angular 22 offre anche Signal Forms, stabili e vicine al modello basato su signals: qui le confrontiamo per riconoscere quale approccio usare.

### Nel percorso

Da conoscere: [Data Binding moderno: interpolazione, property ed event binding](net-04-04-data-binding-moderno-interpolazione.md).

Il laboratorio Form Reattivo con Validazione Remota collega le regole allo stato reale dei controlli. La panoramica Signal Forms è facoltativa: puoi proseguire con Reactive Forms senza implementare un secondo form.

## Le parole da riconoscere

- `reactive forms`
- `formgroup`
- `formcontrol`
- `formbuilder`
- `formcontrolname`
- `stato validita`

## Anatomia e Sintassi del Codice

### Creazione di un FormGroup con FormBuilder:
```typescript
import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
      <input formControlName="email" placeholder="Email" />
      <input type="password" formControlName="password" />
      <button type="submit" [disabled]="loginForm.invalid">Accedi</button>
    </form>
  `
})
export class LoginFormComponent {
  private readonly fb = inject(FormBuilder);
  loginForm = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  onSubmit() {
    if (this.loginForm.valid) {
      // Invia i dati al servizio di login; evita di registrare password nei log.
      const credentials = this.loginForm.getRawValue();
    }
  }
}
```

### Signal Forms in Angular 22
Signal Forms sono incluse in `@angular/forms/signals`. Un modello signal diventa la fonte dei dati; `form()` crea l'albero dei campi e `FormField` collega un campo al template.

```typescript
import { Component, signal } from '@angular/core';
import { email, form, FormField, required } from '@angular/forms/signals';

@Component({
  selector: 'app-signal-login',
  imports: [FormField],
  template: `<label>Email <input type="email" [formField]="loginForm.email" /></label>`
})
export class SignalLoginComponent {
  model = signal({ email: '' });
  loginForm = form(this.model, path => {
    required(path.email);
    email(path.email);
  });
}
```

Scegli Signal Forms per familiarizzare con form nuovi basati su signals; scegli Reactive Forms quando vuoi il modello esplicito già usato negli esempi e nei progetti esistenti, soprattutto se i form sono complessi o dinamici. In questo corso il laboratorio prosegue con Reactive Forms; Signal Forms è una panoramica, non un secondo insieme di esercizi da completare. [Confronto ufficiale Angular](https://angular.dev/guide/forms/signals/comparison).

## Un esempio concreto

```typescript
loginForm = fb.group({
  email: ['', [Validators.required, Validators.email]],
  age: [18, [Validators.min(18)]]
});
```

### Seguilo passo per passo

1. `fb.group` crea due controlli: `email` parte vuoto e `age` parte da `18`.
2. `Validators.required` e `Validators.email` controllano il valore email; `Validators.min(18)` controlla il minimo dell'età.
3. Il `FormGroup` aggrega valori e stato dei controlli. Un'età sotto 18 o un indirizzo non valido rende il form non valido; il template deve mostrare gli errori e impedire l'invio.
4. Confronta l'idea con il breve esempio Signal Forms: in Angular 22 è stabile e usa un modello signal; il laboratorio del corso continua con Reactive Forms per esercitare il modello esplicito.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Dimenticare di importare `ReactiveFormsModule` negli `imports` del componente Standalone, provocando l'errore 'formGroup is not a known property of form'.

## Domanda di verifica

> Qual è la differenza fondamentale tra Template-Driven Forms e Reactive Forms in Angular?
