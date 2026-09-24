# Validatori sincroni nativi e personalizzati

## In parole semplici

L'obiettivo di questa lezione è applicare vincoli di validazione ed estendere Angular con funzioni di controllo custom.

Un validatore sincrono in Angular è una semplice funzione pura che riceve un AbstractControl e restituisce null se il campo è valido, oppure un oggetto ValidationErrors con il codice dell'errore.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `validator`
- `validationerrors`
- `required`
- `minlength`
- `validatorfn`
- `custom validator`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`validator`, `validationerrors`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class CustomValidationService {
    validateTaxCode(code: string): { valid: boolean; error?: string } {
        if (!code || code.length !== 16) return { valid: false, error: 'Lunghezza errata' };
        return { valid: true };
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Restituire `false` invece di `null` quando il controllo è valido (in Angular qualsiasi valore diverso da null viene interpretato come errore!).

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché un validatore di Angular deve restituire `null` (e non `true` o `false`) quando il valore è valido?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
