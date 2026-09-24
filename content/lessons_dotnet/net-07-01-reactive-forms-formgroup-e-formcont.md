# Reactive Forms: FormGroup e FormControl

## In parole semplici

L'obiettivo di questa lezione è costruire form reattivi complessi e controllati gestendo stato, valori e validità dal TypeScript.

Reactive Forms mantengono valori, stato e validatori in un modello TypeScript esplicito; sono ancora una scelta solida per form complessi e codice esistente. Angular 22 offre anche Signal Forms, stabili e vicine al modello basato su signals: qui le confrontiamo per riconoscere quale approccio usare.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `reactive forms`
- `formgroup`
- `formcontrol`
- `formbuilder`
- `formcontrolname`
- `stato validita`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`reactive forms`, `formgroup`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### Creazione di un FormGroup con FormBuilder:
```typescript
import { Component } from '@angular/core';
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
  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  constructor(private fb: FormBuilder) {}

  onSubmit() {
    if (this.loginForm.valid) {
      console.log('Dati form:', this.loginForm.value);
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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class LoginFormRules {
    canSubmit(email: string, password: string): boolean {
        return email.trim().includes('@') && password.length >= 8;
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare di importare `ReactiveFormsModule` negli `imports` del componente Standalone, provocando l'errore 'formGroup is not a known property of form'.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Qual è la differenza fondamentale tra Template-Driven Forms e Reactive Forms in Angular?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
