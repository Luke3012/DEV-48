# Validatori asincroni: verifica remota via API

I validatori asincroni restituiscono una Promise o un Observable di ValidationErrors, permettendo di interrogare un endpoint REST prima che l'utente invii il modulo.

### Nel percorso

Approfondimento facoltativo: puoi riprenderlo dopo aver completato la pratica essenziale del modulo.

## Lo stato che l'utente sta costruendo

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

## Segui un campo o una navigazione

```text
return timer(300).pipe(
  switchMap(() => api.checkEmail(control.value)),
  map(taken => taken ? { emailTaken: true } : null)
);
```

### Segui la persona mentre completa il flusso

1. `timer(300)` aspetta una breve pausa prima di avviare il controllo, così la verifica remota non parte a ogni singolo tasto.
2. `switchMap` passa il valore al servizio API; quando il server risponde, `map` converte `taken` in un errore Angular oppure in `null`.
3. Angular mantiene il controllo in stato `pending` mentre attende. L'invio deve restare disabilitato finché il validatore non ha terminato.
4. Prova un indirizzo disponibile, uno già usato e una modifica rapida mentre la richiesta è in corso. Gestisci anche gli errori di rete senza presentare un indirizzo come sicuramente libero.

L'esercizio usa un set simulato, non invia richieste HTTP. Nel laboratorio prova lo stato `pending` e ricorda che un errore di rete non dimostra che il valore sia libero.

## Rendi visibile lo stato che blocca il flusso

- Eseguire chiamate HTTP all'API a ogni singolo tasto premuto senza applicare `debounceTime` o `timer` (intasando la rete del server).

> **Quale stato decide che cosa accade dopo?** Quando conviene ritardare la verifica remota, e che cosa mostri mentre il controllo è pending?
