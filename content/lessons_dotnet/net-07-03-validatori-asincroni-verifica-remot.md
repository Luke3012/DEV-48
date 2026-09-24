# Validatori asincroni: verifica remota via API

## In parole semplici

L'obiettivo di questa lezione è controllare unicità di email o codici fiscali interrogando il backend prima dell'invio del form.

I validatori asincroni restituiscono una Promise o un Observable di ValidationErrors, permettendo di interrogare un endpoint REST prima che l'utente invii il modulo.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `asyncvalidator`
- `observable`
- `timer`
- `debounce`
- `verifica remota`
- `unicita`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`asyncvalidator`, `observable`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class AsyncCheckSimulator {
    takenEmails = new Set(['admin@dev48.it', 'test@dev48.it']);
    isEmailAvailable(email: string): boolean {
        return !this.takenEmails.has(email.toLowerCase().trim());
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Eseguire chiamate HTTP all'API a ogni singolo tasto premuto senza applicare `debounceTime` o `timer` (intasando la rete del server).

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché è indispensabile inserire un debounce prima di effettuare la verifica asincrona su una chiamata API?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
