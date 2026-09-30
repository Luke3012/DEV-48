# Sicurezza WordPress

## In parole semplici

Applicare sanitizzazione, escaping, nonce e capability nel punto corretto.

Sanitizzare significa pulire un dato in ingresso; fare escaping significa renderlo sicuro nel punto in cui viene mostrato. Un nonce aiuta a verificare l'intenzione della richiesta, ma non sostituisce il controllo dei permessi.

## Le parole da riconoscere

`sanitize_text_field`; `esc_html`; `nonce`; `current_user_can`; `$wpdb->prepare`; `capability`

## Un esempio concreto

```text
$name = sanitize_text_field($_POST['name'] ?? '');
echo esc_html($name);
```

Sanitizzo l'input per adeguarlo al formato previsto ed eseguo escaping al momento dell'output secondo il contesto HTML, attributo o URL. Il nonce non sostituisce current_user_can: controllo anche che l'utente abbia il permesso richiesto.

## Prova tu

Un form riceve un nome e aggiorna una voce amministrativa. Indica dove sanitizzi, dove fai escaping e dove verifichi capability e nonce. Spiega perché un nonce valido non basta ad autorizzare la modifica.

## Dove ci si confonde spesso

- Confondere sanitizzazione input ed escaping output
- Nonce usato come autorizzazione

## Domanda di verifica

> Qual è la differenza tra sanitizzare ed eseguire escaping?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
