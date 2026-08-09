# Sicurezza WordPress

## In parole semplici

L'obiettivo di questa lezione è applicare sanitizzazione, escaping, nonce e capability nel punto corretto.

Sanitizzare significa pulire un dato in ingresso; fare escaping significa renderlo sicuro nel punto in cui viene mostrato. Un nonce aiuta a verificare l'intenzione della richiesta, ma non sostituisce il controllo dei permessi.

### Perché è utile

In WordPress il codice vive dentro un sistema già avviato. Devi capire in quale momento agganciare la tua funzione e trattare ogni dato ricevuto come non affidabile fino a quando non viene controllato.

## Le parole da riconoscere

- `sanitize_text_field`
- `esc_html`
- `nonce`
- `current_user_can`
- `$wpdb->prepare`
- `capability`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **sanitize_text_field, esc_html, nonce** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
$name = sanitize_text_field($_POST['name'] ?? '');
echo esc_html($name);
```

Individua l'hook, il dato ricevuto e il punto in cui viene sanitizzato o mostrato. Sono i tre passaggi che spiegano quasi tutto il frammento.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Confondere sanitizzazione input ed escaping output
- Nonce usato come autorizzazione

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Qual è la differenza tra sanitizzare ed eseguire escaping?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
