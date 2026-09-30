# Validatori sincroni nativi e personalizzati

Un validatore sincrono in Angular è una semplice funzione pura che riceve un AbstractControl e restituisce null se il campo è valido, oppure un oggetto ValidationErrors con il codice dell'errore.

## Lo stato che l'utente sta costruendo

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

## Segui un campo o una navigazione

```typescript
export function minAgeValidator(min: number): ValidatorFn {
  return (control) => control.value >= min ? null : { minAge: { required: min } };
}
```

### Segui la persona mentre completa il flusso

1. `minAgeValidator(18)` restituisce una funzione che Angular chiama con il controllo e il valore attuale.
2. Se il valore è almeno 18, il validatore restituisce `null`, che significa nessun errore; altrimenti restituisce un oggetto `minAge` con la soglia richiesta.
3. Il template può leggere quell'errore per mostrare un messaggio, ma `required` è un controllo separato: un campo opzionale vuoto non dovrebbe essere rifiutato per la sola età minima.
4. Prova `17`, `18` e un valore vuoto. Combina il validatore con `Validators.required` quando il campo è obbligatorio e osserva i due errori distinti.

Il runner prova il contratto della funzione validatrice; il laboratorio Forms mostra come `ValidationErrors` diventa stato e messaggio vicino al campo.

## Rendi visibile lo stato che blocca il flusso

- Restituire `false` invece di `null` quando il controllo è valido (in Angular qualsiasi valore diverso da null viene interpretato come errore!).

> **Quale stato decide che cosa accade dopo?** Perché un validatore di Angular deve restituire `null` (e non `true` o `false`) quando il valore è valido?
