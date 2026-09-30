# Sicurezza web essenziale

## In parole semplici

Riconoscere i rischi più comuni e applicare difese nei confini corretti.

La sicurezza va applicata a più livelli: query parametrizzate, output correttamente escapato, password sottoposte a hash e permessi minimi. La validazione del frontend migliora l'esperienza, ma non protegge il server.

## Le parole da riconoscere

`SQL injection`; `XSS`; `CSRF`; `hash password`; `least privilege`; `rate limit`; `secret`

## Un esempio concreto

```javascript
// Query parametrizzata
db.prepare('SELECT * FROM users WHERE email = ?').get(email);
```

Una query parametrizzata mantiene separati il testo SQL e i valori dell'utente, che vengono trattati come dati. Un apostrofo nel nome non deve diventare una parte eseguibile della query. Parametrizzazione e controllo dei permessi risolvono rischi diversi e servono entrambi.

## Prova tu

Un nome contiene un apostrofo. Confronta concatenazione SQL e parametro: mostra dove viene inserito il valore e spiega quale difesa manca ancora se il chiamante non ha il permesso di leggere il record.

## Dove ci si confonde spesso

- Concatenare SQL
- Memorizzare password
- Fidarsi della validazione frontend

## Domanda di verifica

> Perché una query parametrizzata riduce SQL injection?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
