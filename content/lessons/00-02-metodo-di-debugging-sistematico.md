# Metodo di debugging sistematico

## In parole semplici

L'obiettivo di questa lezione è passare da 'non funziona' a un'ipotesi falsificabile e a una correzione minima.

Un bug diventa gestibile quando sai riprodurlo. Parti da un caso che fallisce sempre, leggi l'errore fino in fondo e prova una sola ipotesi: così capisci davvero quale modifica lo ha risolto.

### Perché è utile

Qui non conta partire in fretta: conta rendere visibile il ragionamento. Chi ti osserva deve capire quali informazioni hai raccolto, quale ipotesi stai provando e come decidi se il risultato è corretto.

## Le parole da riconoscere

- `riproduzione`
- `messaggio di errore`
- `ipotesi`
- `isolamento`
- `regressione`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **riproduzione, messaggio di errore, ipotesi** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
function debug(value) {
  console.log({ value, type: typeof value });
  return value;
}
```

Usalo come una scaletta da dire ad alta voce. Ogni riga corrisponde a una decisione che anche l'intervistatore può seguire.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Cambiare più cose insieme
- Ignorare stack trace e condizioni di riproduzione

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Descrivi come indagheresti un bug che compare solo con dati vuoti.

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
