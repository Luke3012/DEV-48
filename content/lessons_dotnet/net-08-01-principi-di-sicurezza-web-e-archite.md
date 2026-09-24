# Principi di sicurezza Web e architettura JWT

## In parole semplici

L'obiettivo di questa lezione è comprendere header, payload e firma di un JWT, e valutare cosa comporta usare token senza una sessione server tradizionale.

Un JWT è un formato di token. Un token firmato (JWS) contiene tre parti codificate in Base64URL, ma la firma non cifra il payload. Per autenticare una richiesta, il server deve validare il token e applicare le proprie regole di autorizzazione.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `jwt`
- `header`
- `payload`
- `signature`
- `claims`
- `revoca`
- `bearer token`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`jwt`, `header`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

```text
// Il token viaggia nell'header HTTP Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

### Seguilo passo per passo

1. L'header e il payload del JWT sono codificati in Base64URL: chi possiede il token può decodificarli e leggerli.
2. La firma consente al server di verificare che il token non sia stato alterato e che provenga da chi possiede la chiave; non cifra i dati.
3. Il client invia il token con `Authorization: Bearer ...`; il server controlla firma, issuer, audience e scadenza prima di usarne le claim.
4. Decodifica il payload di un token di prova e verifica che non contenga password o altri segreti. Considera come revocare un token prima della sua scadenza.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```csharp
public static class JwtHelper {
    public static string FormatBearerHeader(string token) => $"Bearer {token.Trim()}";
    public static bool HasValidParts(string token) => token.Split('.').Length == 3;
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Mettere password o altri dati riservati nel payload
- supporre che avere una firma renda valido il token senza convalidare le sue claim
- dimenticare la scadenza.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché non si devono mai memorizzare dati sensibili (come password o carte di credito) nel payload di un token JWT?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
