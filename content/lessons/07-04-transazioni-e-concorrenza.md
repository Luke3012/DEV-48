# Transazioni e concorrenza

## In parole semplici

Rendere atomiche operazioni che devono riuscire o fallire insieme.

Una transazione raggruppa operazioni che devono riuscire insieme. Se una fallisce, il rollback evita uno stato parziale; tenerla aperta troppo a lungo può però bloccare altri accessi.

## Le parole da riconoscere

`transaction`; `BEGIN`; `COMMIT`; `ROLLBACK`; `atomicità`; `isolamento`; `lock`

## Un esempio concreto

```sql
BEGIN;
UPDATE accounts SET balance=balance-100 WHERE id=1;
UPDATE accounts SET balance=balance+100 WHERE id=2;
COMMIT;
```

Un trasferimento richiede che addebito e accredito siano atomici. Se il secondo passo fallisce eseguo rollback, altrimenti perderei denaro. Controllo anche l'esistenza dei conti e il saldo prima del commit: una transazione da sola non valida la regola applicativa.

## Prova tu

Nel lab-sql elimina un soggetto con record collegati e provoca un errore dopo il primo DELETE. Prima di eseguire, scrivi quali dati devono rimanere dopo il rollback e perché un commit parziale sarebbe scorretto.

## Dove ci si confonde spesso

- Commit parziale
- Transazioni troppo lunghe
- Nessuna gestione del rollback

## Domanda di verifica

> Perché un trasferimento richiede una transazione?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
