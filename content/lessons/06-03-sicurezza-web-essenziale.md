# Sicurezza web essenziale

## In parole semplici

L'obiettivo di questa lezione è riconoscere i rischi più comuni e applicare difese nei confini corretti.

La sicurezza va applicata a più livelli: query parametrizzate, output correttamente escapato, password sottoposte a hash e permessi minimi. La validazione del frontend migliora l'esperienza, ma non protegge il server.

### Perché è utile

Sul backend ogni dato attraversa un confine: arriva da una richiesta, viene controllato, passa nella logica applicativa e produce una risposta. Tenere distinti questi passaggi rende più semplici sia gli errori sia la sicurezza.

## Le parole da riconoscere

- `SQL injection`
- `XSS`
- `CSRF`
- `hash password`
- `least privilege`
- `rate limit`
- `secret`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **SQL injection, XSS, CSRF** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
// Query parametrizzata
db.prepare('SELECT * FROM users WHERE email = ?').get(email);
```

Segui la richiesta nell'ordine reale: ingresso, controllo, logica, accesso ai dati e risposta. Nota anche dove finirebbe un errore.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Concatenare SQL
- Memorizzare password
- Fidarsi della validazione frontend

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Perché una query parametrizzata riduce SQL injection?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
