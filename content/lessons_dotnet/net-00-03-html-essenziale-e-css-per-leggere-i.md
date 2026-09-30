# HTML essenziale e CSS per leggere i template Angular

Un template Angular usa elementi HTML. Gli elementi descrivono la struttura; gli attributi danno informazioni o collegano il template al componente. CSS definisce l'aspetto senza cambiare il significato del documento.

## Partiamo da quello che puoi osservare

### Struttura HTML di una schermata
- `<main>` racchiude il contenuto principale della pagina.
- `<label for="email">` collega il testo visibile al controllo che ha `id="email"`.
- `type="email"` comunica il tipo di dato al browser; non sostituisce la validazione server.
- `<button type="button">` non invia un form per errore. Per inviare un modulo si usa `type="submit"`.

### Una regola CSS
```css
.page { max-width: 40rem; margin-inline: auto; padding: 1rem; }
button:focus-visible { outline: 3px solid currentColor; }
```
La classe `.page` seleziona gli elementi con `class="page"`; `:focus-visible` mantiene visibile l'indicatore quando si naviga da tastiera.

## Segui un caso dall'inizio alla fine

```typescript
<main class="page">
  <h1>Profilo</h1>
  <form>
    <label for="email">Email</label>
    <input id="email" name="email" type="email" required>
    <button type="submit">Salva</button>
  </form>
</main>
```

### Ricostruisci il caso con i dati iniziali

1. `<main>` racchiude il contenuto principale della pagina e `<h1>` ne identifica il titolo.
2. `label for="email"` punta all'`id="email"` dell'input: cliccare l'etichetta porta il focus al campo e uno screen reader ne legge il nome.
3. `type="email"` e `required` forniscono semantica e vincoli HTML di base; il pulsante invia il form, ma la logica Angular non è ancora presente.
4. Rimuovi temporaneamente `id` o cambia il valore di `for` e verifica perché l'associazione non funziona. Poi usa Tab e controlla che il focus resti visibile.

## Una variante da provare

```css
.page { max-width: 40rem; margin-inline: auto; padding: 1rem; }
input, button { font: inherit; }
button:focus-visible { outline: 3px solid currentColor; }
```

## Se il risultato non è quello atteso

- Associare il testo del campo alla relativa `id`
- usare un elemento soltanto per il suo aspetto invece che per il suo significato
- rimuovere l'indicatore di focus da tastiera.

> **Fermati e ricostruisci il passaggio** Quale coppia collega una label a un campo, e perché il CSS non sostituisce la struttura semantica?
