# Test unitari, integrazione ed E2E

## In parole semplici

L'obiettivo di questa lezione è scegliere il livello di test più economico capace di coprire il rischio.

Un test unitario isola una piccola regola; un test di integrazione verifica la collaborazione tra parti; un E2E percorre il sistema come un utente. Servono livelli diversi perché trovano problemi diversi.

### Perché è utile

Questi strumenti servono a ridurre l'incertezza. Git rende leggibile la storia delle modifiche; test e debugger ti aiutano a dimostrare che un comportamento esiste davvero e continua a funzionare.

## Le parole da riconoscere

- `unit test`
- `integration test`
- `E2E`
- `arrange-act-assert`
- `mock`
- `regression`
- `test pyramid`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **unit test, integration test, E2E** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
it('filters active subjects', () => {
 const result = filterActive([{id:1,active:true},{id:2,active:false}]);
 expect(result).toEqual([{id:1,active:true}]);
});
```

Chiediti quale prova concreta offre questo comando o questo test. Se fallisse, il messaggio dovrebbe aiutarti a restringere il problema.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Testare dettagli interni
- Mockare tutto
- Test senza asserzioni significative

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Quando preferiresti un test di integrazione a uno unitario?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
