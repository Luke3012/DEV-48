# Progettazione dell'esperienza utente e feedback visivo

## In parole semplici

L'obiettivo di questa lezione è creare interfacce piacevoli con stati di caricamento skeleton, toast di notifica e micro-interazioni.

Per operazioni che richiedono attesa o possono fallire, un feedback chiaro aiuta a capire se l'azione è stata avviata e come è terminata.

## Le parole da riconoscere

- `ux`
- `skeleton loader`
- `toast`
- `accessibilita`
- `micro-interazioni`
- `feedback visivo`

## Anatomia e Sintassi del Codice

### I Tre Stati di Qualsiasi Operazione Asincrona:
1. **Pending (In Corso)**: disabilita il pulsante di submit per prevenire doppi invii e mostra un indicatore visivo.
2. **Success (Completata)**: mostra un toast o messaggio temporaneo di successo e aggiorna la lista.
3. **Error (Fallita)**: evidenzia il campo errato o mostra una notifica chiara con ProblemDetails.

## Un esempio concreto

```html
<!-- Disabilitare pulsante e mostrare spinner mentre isSaving() è true -->
<button [disabled]="isSaving()">
  @if (isSaving()) { <span>Salvataggio...</span> } @else { <span>Salva</span> }
</button>
```

### Seguilo passo per passo

1. Quando parte il salvataggio, `isSaving()` disabilita il pulsante per evitare invii ripetuti.
2. Il template mostra `Salvataggio...` durante l'attesa e `Salva` quando l'operazione termina; la persona riceve un'indicazione visibile.
3. Al successo o all'errore, mostra un messaggio associato allo stato. Per i cambiamenti annunciabili aggiungi un'area `role="status"` o `role="alert"` con il comportamento appropriato.
4. Prova una rete lenta, un errore e un doppio click. Controlla tastiera e screen reader, non solo l'aspetto visivo.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Non mostrare alcuno stato di caricamento lasciando credere all'utente che il click non sia stato registrato.

## Domanda di verifica

> Quali problemi previeni disabilitando il pulsante durante una richiesta, e che cosa devi fare se fallisce?
