# HTML semantico e struttura

## In parole semplici

Scegliere elementi che descrivono il significato, non soltanto l'aspetto.

Gli elementi semantici descrivono il ruolo del contenuto. Un `button` comunica già a browser e tecnologie assistive che può ricevere focus ed essere attivato: un `div` con un click non offre automaticamente lo stesso comportamento.

## Le parole da riconoscere

`header`; `nav`; `main`; `section`; `article`; `button`; `heading`; `semantica`

## Un esempio concreto

```html
<main>
  <h1>Archivio soggetti</h1>
  <section aria-labelledby="active-title">
    <h2 id="active-title">Attivi</h2>
    <p>Anna Bianchi</p>
  </section>
</main>
```

Un button riceve focus e offre attivazione da tastiera e semantica di pulsante. Un div con onClick richiede implementare separatamente queste capacità. Per un'azione uso button; per navigare a una risorsa uso un link con href.

## Prova tu

Costruisci una pagina con main, h1, nav con un link e section con h2. Usa button per un'azione. Nel browser percorri link e pulsante con Tab. Il runner verifica tag, non focus e comportamento.

## Dove ci si confonde spesso

- Div per ogni cosa
- Gerarchia heading incoerente
- Elementi cliccabili non accessibili

## Domanda di verifica

> Perché un button è preferibile a un div con onClick?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
