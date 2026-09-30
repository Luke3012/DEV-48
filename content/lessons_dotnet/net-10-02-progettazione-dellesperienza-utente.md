# Progettazione dell'esperienza utente e feedback visivo

Un click che avvia una richiesta non produce subito un risultato. Se la vista non cambia, la persona può cliccare ancora; se il server rifiuta, lasciare il pulsante disabilitato sembra un blocco. La UI deve rappresentare l'intero ciclo, non soltanto il successo.

## Il progetto visto da chi deve usarlo

### Stati osservabili dal template
```typescript
import { signal } from '@angular/core';
import { firstValueFrom } from 'rxjs';

type SaveState = 'idle' | 'loading' | 'success' | 'error';
readonly state = signal<SaveState>('idle');

// Estratto del componente: il service e il form sono già stati iniettati.
async save(): Promise<void> {
  this.state.set('loading');
  try {
    await firstValueFrom(this.subjectsService.save(this.form.getRawValue()));
    this.state.set('success');
  } catch {
    this.state.set('error');
  }
}
```

Poiché `HttpClient` restituisce un Observable, `firstValueFrom` lo attende come Promise; in una UI reattiva puoi invece gestire la richiesta con `subscribe` o convertirla nello stato del template.

```html
<button [disabled]="state() === 'loading'" (click)="save()">
  @if (state() === 'loading') { <span>Salvataggio…</span> }
  @else { <span>Salva</span> }
</button>
@if (state() === 'success') { <p role="status">Modifiche salvate.</p> }
@if (state() === 'error') { <p role="alert">Salvataggio non riuscito. Riprova.</p> }
```

Il template disabilita il doppio invio durante l'attesa e rende visibile la conclusione. Collega gli errori di validazione del server ai campi; un errore di rete deve lasciare i dati ripristinabili. Usa `role="status"` per un aggiornamento informativo e `role="alert"` per un errore che richiede attenzione.

## Attraversa i file e i processi coinvolti

```text
state.set('loading');
try { await service.save(value); state.set('success'); }
catch { state.set('error'); }
```

### Racconta l'operazione dal file al risultato

1. Al click, lo stato passa da `idle` a `loading`; il pulsante si disabilita e mostra l'attesa.
2. Quando l'API risponde con successo, la lista si aggiorna e il template annuncia il completamento.
3. Se la richiesta fallisce, il `catch` porta lo stato a `error`; il pulsante si riattiva e un messaggio spiega come proseguire.
4. Prova una rete lenta, una risposta 400 di validazione, un errore 500 e un doppio click. Verifica tastiera e annunci screen reader oltre all'aspetto visivo.

La funzione breve modella solo le transizioni di stato. Nel laboratorio Monorepo e nel portfolio prova il flusso con richieste HTTP riuscite e fallite e conserva il form in caso di errore.

## Che cosa deve poter verificare un'altra persona?

- Non mostrare alcuno stato di caricamento lasciando credere all'utente che il click non sia stato registrato.

> **Quale decisione puoi motivare con il codice?** Quali problemi previeni disabilitando il pulsante durante una richiesta, e che cosa devi fare se fallisce?
