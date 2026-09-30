# Test unitari, integrazione ed E2E

## In parole semplici

Scegliere il livello di test più economico capace di coprire il rischio.

Un test unitario isola una piccola regola; un test di integrazione verifica la collaborazione tra parti; un E2E percorre il sistema come un utente. Servono livelli diversi perché trovano problemi diversi.

## Le parole da riconoscere

`unit test`; `integration test`; `E2E`; `arrange-act-assert`; `mock`; `regression`; `test pyramid`

## Un esempio concreto

```text
it('filters active subjects', () => {
 const result = filterActive([{id:1,active:true},{id:2,active:false}]);
 expect(result).toEqual([{id:1,active:true}]);
});
```

Preferisco un test di integrazione quando il rischio è nella collaborazione tra parti, per esempio un submit che valida e aggiorna la lista. Un test della sola funzione di validazione non prova quel collegamento. Un E2E aggiunge browser e sistema reale, con un costo e una copertura differenti.

## Prova tu

La validazione del nome passa, ma il pulsante Salva non aggiorna la lista. Scegli il livello di test che scopre il collegamento mancante; scrivi azione e risultato atteso senza riferirti al nome di un hook.

## Dove ci si confonde spesso

- Testare dettagli interni
- Mockare tutto
- Test senza asserzioni significative

## Domanda di verifica

> Quando preferiresti un test di integrazione a uno unitario?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
