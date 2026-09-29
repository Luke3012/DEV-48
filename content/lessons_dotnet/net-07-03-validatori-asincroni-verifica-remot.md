# Validatori asincroni: verifica remota via API

## In parole semplici

L'obiettivo di questa lezione è controllare unicità di email o codici fiscali interrogando il backend prima dell'invio del form.

I validatori asincroni restituiscono una Promise o un Observable di ValidationErrors, permettendo di interrogare un endpoint REST prima che l'utente invii il modulo.

### Nel percorso

Approfondimento facoltativo: puoi riprenderlo dopo aver completato la pratica essenziale del modulo.

## Le parole da riconoscere

- `asyncvalidator`
- `observable`
- `timer`
- `debounce`
- `verifica remota`
- `unicita`

## Anatomia e Sintassi del Codice

### Validatore Asincrono con Debounce:
```typescript
import { AbstractControl, AsyncValidatorFn, ValidationErrors } from '@angular/forms';
import { Observable, timer, of } from 'rxjs';
import { switchMap, map } from 'rxjs/operators';

export function uniqueEmailValidator(checkApi: (email: string) => Observable<boolean>): AsyncValidatorFn {
  return (control: AbstractControl): Observable<ValidationErrors | null> => {
    if (!control.value) return of(null);

    // Attende 300ms prima di chiamare l'API per evitare chiamate a ogni tasto
    return timer(300).pipe(
      switchMap(() => checkApi(control.value)),
      map(isTaken => isTaken ? { emailTaken: true } : null)
    );
  };
}
```

## Un esempio concreto

```text
return timer(300).pipe(
  switchMap(() => api.checkEmail(control.value)),
  map(taken => taken ? { emailTaken: true } : null)
);
```

### Seguilo passo per passo

1. `timer(300)` aspetta una breve pausa prima di avviare il controllo, così la verifica remota non parte a ogni singolo tasto.
2. `switchMap` passa il valore al servizio API; quando il server risponde, `map` converte `taken` in un errore Angular oppure in `null`.
3. Angular mantiene il controllo in stato `pending` mentre attende. L'invio deve restare disabilitato finché il validatore non ha terminato.
4. Prova un indirizzo disponibile, uno già usato e una modifica rapida mentre la richiesta è in corso. Gestisci anche gli errori di rete senza presentare un indirizzo come sicuramente libero.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Eseguire chiamate HTTP all'API a ogni singolo tasto premuto senza applicare `debounceTime` o `timer` (intasando la rete del server).

## Domanda di verifica

> Quando conviene ritardare la verifica remota, e che cosa mostri mentre il controllo è pending?
