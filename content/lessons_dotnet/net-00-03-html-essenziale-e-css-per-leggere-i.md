# HTML essenziale e CSS per leggere i template Angular

## In parole semplici

L'obiettivo di questa lezione è riconoscere struttura semantica, label dei campi e regole CSS essenziali prima di usare template Angular.

Un template Angular usa elementi HTML. Gli elementi descrivono la struttura; gli attributi danno informazioni o collegano il template al componente. CSS definisce l'aspetto senza cambiare il significato del documento.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `html`
- `elemento`
- `attributo`
- `label`
- `id`
- `classe css`
- `focus`
- `template`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`html`, `elemento`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

### Seguilo passo per passo

1. `<main>` racchiude il contenuto principale della pagina e `<h1>` ne identifica il titolo.
2. `label for="email"` punta all'`id="email"` dell'input: cliccare l'etichetta porta il focus al campo e uno screen reader ne legge il nome.
3. `type="email"` e `required` forniscono semantica e vincoli HTML di base; il pulsante invia il form, ma la logica Angular non è ancora presente.
4. Rimuovi temporaneamente `id` o cambia il valore di `for` e verifica perché l'associazione non funziona. Poi usa Tab e controlla che il focus resti visibile.

## Pattern Guida per gli Esercizi

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```css
.page { max-width: 40rem; margin-inline: auto; padding: 1rem; }
input, button { font: inherit; }
button:focus-visible { outline: 3px solid currentColor; }
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Associare il testo del campo alla relativa `id`
- usare un elemento soltanto per il suo aspetto invece che per il suo significato
- rimuovere l'indicatore di focus da tastiera.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Quale coppia collega una label a un campo, e perché il CSS non sostituisce la struttura semantica?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
