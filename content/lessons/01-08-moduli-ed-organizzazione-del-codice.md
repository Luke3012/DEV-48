# Moduli ed organizzazione del codice

## In parole semplici

L'obiettivo di questa lezione è separare responsabilità usando export e import comprensibili.

Un modulo espone soltanto ciò che gli altri file devono usare. Import ed export ben scelti mostrano le dipendenze reali e impediscono che un singolo file diventi il contenitore di tutta l'applicazione.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `export nominato`
- `export default`
- `import`
- `modulo`
- `dipendenza`
- `API pubblica`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **export nominato, export default, import** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
// format.js
export function formatDate(value) { return new Date(value).toLocaleDateString('it-IT'); }
// app.js
import { formatDate } from './format.js';
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Dipendenze circolari
- Esportare dettagli interni
- File contenitore gigantesco

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Differenza tra export nominato ed export default?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
