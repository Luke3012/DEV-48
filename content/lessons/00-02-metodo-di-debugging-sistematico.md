# Metodo di debugging sistematico

## In parole semplici

Passare da 'non funziona' a un'ipotesi falsificabile e a una correzione minima.

Un bug diventa gestibile quando sai riprodurlo. Parti da un caso che fallisce sempre, leggi l'errore fino in fondo e prova una sola ipotesi: così capisci davvero quale modifica lo ha risolto.

Una correzione utile parte da una differenza riproducibile tra risultato atteso e ottenuto. Registra input, output e messaggio d'errore prima di intervenire. Il debugger e `console.log` servono a controllare un'ipotesi precisa; stamparne molti senza una domanda aumenta il rumore.

## Le parole da riconoscere

`riproduzione`; `messaggio di errore`; `ipotesi`; `isolamento`; `regressione`

## Un esempio concreto

```text
function firstName(names) {
  return names[0].trim();
}
console.log(firstName([' Anna '])); // 'Anna'
console.log(firstName([])); // TypeError: il primo elemento non esiste
```

Con la lista vuota `names[0]` è `undefined`; l'errore compare quando chiami `.trim()`. Il sintomo non indica che `trim` sia difettoso: manca la gestione dell'assenza. Se il contratto vuole una stringa vuota, controlla la lunghezza prima di leggere il primo elemento.

## Prova tu

Scrivi il caso che fallisce, aggiungi la sola guardia necessaria e riprova entrambi gli input. Conserva il caso vuoto come test di regressione: deve fallire prima della correzione e passare dopo.

## Dove ci si confonde spesso

- Cambiare più cose insieme
- Ignorare stack trace e condizioni di riproduzione

## Domanda di verifica

> Descrivi come indagheresti un bug che compare solo con dati vuoti.

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
