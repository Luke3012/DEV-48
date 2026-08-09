# Form controllati

## In parole semplici

L'obiettivo di questa lezione è mantenere input, validazione e submit coerenti con lo state React.

In un input controllato, il valore mostrato viene dallo state e `onChange` aggiorna quello state. Hai così un'unica fonte di verità per validazione, invio e messaggi di errore.

### Perché è utile

In React la domanda principale è sempre la stessa: da quali dati dipende questa parte dell'interfaccia? Individua chi possiede quei dati e lascia che il rendering descriva ciò che l'utente deve vedere in quel momento.

## Le parole da riconoscere

- `controlled input`
- `value`
- `onChange`
- `onSubmit`
- `preventDefault`
- `validation`
- `error state`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **controlled input, value, onChange** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
const [name,setName]=useState('');
<form onSubmit={handleSubmit}><input value={name} onChange={e=>setName(e.target.value)} /></form>
```

Distingui props, stato e valori calcolati. Poi segui l'evento: quale setter viene chiamato e quale parte della UI cambia al rendering successivo?

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Mescolare input controllati e non controllati
- Validare soltanto dopo la chiamata API

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Che cosa rende controllato un input React?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
