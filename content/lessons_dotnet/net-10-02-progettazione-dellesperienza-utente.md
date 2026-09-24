# Progettazione dell'esperienza utente e feedback visivo

## In parole semplici

L'obiettivo di questa lezione è creare interfacce piacevoli con stati di caricamento skeleton, toast di notifica e micro-interazioni.

Per operazioni che richiedono attesa o possono fallire, un feedback chiaro aiuta a capire se l'azione è stata avviata e come è terminata.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `ux`
- `skeleton loader`
- `toast`
- `accessibilita`
- `micro-interazioni`
- `feedback visivo`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`ux`, `skeleton loader`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

### I Tre Stati di Qualsiasi Operazione Asincrona:
1. **Pending (In Corso)**: disabilita il pulsante di submit per prevenire doppi invii e mostra un indicatore visivo.
2. **Success (Completata)**: mostra un toast o messaggio temporaneo di successo e aggiorna la lista.
3. **Error (Fallita)**: evidenzia il campo errato o mostra una notifica chiara con ProblemDetails.

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class UiFeedbackModel {
    status = signal('idle');
    start() { this.status.set('busy'); }
    finishSuccess() { this.status.set('success'); }
    finishError() { this.status.set('error'); }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Non mostrare alcuno stato di caricamento lasciando credere all'utente che il click non sia stato registrato.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché disabilitare il pulsante di invio durante una chiamata HTTP è una best-practice essenziale di UX?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
