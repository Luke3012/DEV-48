# Autenticazione, CORS e segreti

## In parole semplici

Distinguere identità, permessi, regole del browser e gestione delle credenziali.

L'autenticazione stabilisce chi sei; l'autorizzazione stabilisce che cosa puoi fare. CORS è una regola del browser, non una protezione dell'API, e un segreto inserito nel frontend non è più segreto.

## Le parole da riconoscere

`autenticazione`; `autorizzazione`; `token`; `cookie`; `CORS`; `variabile d'ambiente`; `segreto`

## Un esempio concreto

```text
Authorization: Bearer <token>
// Le chiavi private restano sul server, mai nel bundle frontend.
```

CORS è applicato dai browser e regola l'accesso alla risposta da origini diverse. Un client server o da terminale può chiamare l'API senza quel vincolo. L'API deve comunque autenticare il chiamante e autorizzare l'operazione; un segreto non può essere protetto dentro il bundle frontend.

## Prova tu

Un client da terminale chiama l'API anche se l'origine non è ammessa dal browser. Spiega perché CORS non blocca quel client e quali controlli devono rimanere sul server. Usa un esempio di permesso negato.

## Dove ci si confonde spesso

- Mettere API key nel frontend
- Usare CORS come sistema di autenticazione

## Domanda di verifica

> CORS protegge una API da qualsiasi client malevolo?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
