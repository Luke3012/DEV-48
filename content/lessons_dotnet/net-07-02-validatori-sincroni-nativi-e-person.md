# Validatori sincroni nativi e personalizzati

## In parole semplici

L'obiettivo di questa lezione è applicare vincoli di validazione ed estendere Angular con funzioni di controllo custom.

Un validatore sincrono in Angular è una semplice funzione pura che riceve un AbstractControl e restituisce null se il campo è valido, oppure un oggetto ValidationErrors con il codice dell'errore.

## Le parole da riconoscere

- `validator`
- `validationerrors`
- `required`
- `minlength`
- `validatorfn`
- `custom validator`

## Anatomia e Sintassi del Codice

### Anatomia di un Validatore Personalizzato:
```typescript
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

// Validatore che vieta l'uso di parole riservate (es. 'admin')
export function forbiddenNameValidator(forbiddenName: string): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value as string;
    const isForbidden = value?.toLowerCase().includes(forbiddenName.toLowerCase());
    return isForbidden ? { forbiddenName: { value: control.value } } : null;
  };
}
```

### Regola Fondamentale del Ritorno:
- **`null`**: il controllo è valido! Non ci sono errori.
- **`{ [errorKey]: true }`**: il controllo ha fallito la validazione. La chiave `errorKey` apparirà nell'oggetto `control.errors`.

## Un esempio concreto

```typescript
export function minAgeValidator(min: number): ValidatorFn {
  return (control) => control.value >= min ? null : { minAge: { required: min } };
}
```

### Seguilo passo per passo

1. `minAgeValidator(18)` restituisce una funzione che Angular chiama con il controllo e il valore attuale.
2. Se il valore è almeno 18, il validatore restituisce `null`, che significa nessun errore; altrimenti restituisce un oggetto `minAge` con la soglia richiesta.
3. Il template può leggere quell'errore per mostrare un messaggio, ma `required` è un controllo separato: un campo opzionale vuoto non dovrebbe essere rifiutato per la sola età minima.
4. Prova `17`, `18` e un valore vuoto. Combina il validatore con `Validators.required` quando il campo è obbligatorio e osserva i due errori distinti.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Restituire `false` invece di `null` quando il controllo è valido (in Angular qualsiasi valore diverso da null viene interpretato come errore!).

## Domanda di verifica

> Perché un validatore di Angular deve restituire `null` (e non `true` o `false`) quando il valore è valido?
