# Principi di sicurezza Web e architettura JWT

## In parole semplici

L'obiettivo di questa lezione è comprendere header, payload e firma di un JWT, e valutare cosa comporta usare token senza una sessione server tradizionale.

Un JWT è un formato di token. Un token firmato (JWS) contiene tre parti codificate in Base64URL, ma la firma non cifra il payload. Per autenticare una richiesta, il server deve validare il token e applicare le proprie regole di autorizzazione.

## Le parole da riconoscere

- `jwt`
- `header`
- `payload`
- `signature`
- `claims`
- `revoca`
- `bearer token`

## Anatomia e Sintassi del Codice

### Anatomia del JWT compatto firmato (JWS):
1. **Header**: dichiara il tipo di token e l'algoritmo di firma. Il server deve accettare solo gli algoritmi previsti dalla configurazione.
2. **Payload (Claims)**: contiene le affermazioni sull'identità dell'utente:
   - `sub`: identificativo utente (Subject)
   - `email`: indirizzo email
   - `role`: ruoli di autorizzazione
   - `exp`: timestamp di scadenza (Expiration)
3. **Signature (Firma crittografica)**:
   - Protegge l'integrità dei dati firmati. Il server rifiuta un token alterato solo se verifica correttamente firma, emittente, destinatario e scadenza.

Le parti sono **Base64URL, non cifrate**: chi possiede il token può leggere il payload. Un token con `exp` breve riduce la finestra di utilizzo; la revoca immediata richiede una strategia aggiuntiva.

## Un esempio concreto

```text
// Il token viaggia nell'header HTTP Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

### Seguilo passo per passo

1. L'header e il payload del JWT sono codificati in Base64URL: chi possiede il token può decodificarli e leggerli.
2. La firma consente al server di verificare che il token non sia stato alterato e che provenga da chi possiede la chiave; non cifra i dati.
3. Il client invia il token con `Authorization: Bearer ...`; il server controlla firma, issuer, audience e scadenza prima di usarne le claim.
4. Decodifica il payload di un token di prova e verifica che non contenga password o altri segreti. Considera come revocare un token prima della sua scadenza.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione .NET. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

## Dove ci si confonde spesso

- Mettere password o altri dati riservati nel payload
- supporre che avere una firma renda valido il token senza convalidare le sue claim
- dimenticare la scadenza.

## Domanda di verifica

> Perché non si devono mai memorizzare dati sensibili (come password o carte di credito) nel payload di un token JWT?
