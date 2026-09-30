# Routing e architettura frontend

## In parole semplici

Prima di iniziare, ripassa [Moduli ed organizzazione del codice](01-08-moduli-ed-organizzazione-del-codice.md) e [Caricamento dati e stati remoti](05-08-caricamento-dati-e-stati-remoti.md).

Dividere pagine, feature, componenti e accesso dati mantenendo dipendenze leggibili.

Le route organizzano le pagine; le feature raccolgono componenti e logica legati allo stesso problema. L'accesso alle API va separato dalla presentazione, così puoi cambiarlo e provarlo senza riscrivere la UI.

Questo approfondimento chiarisce i confini, senza imporre una libreria di routing. Una route associa un URL a una pagina; un router completo gestisce anche navigazione, parametri, cronologia e URL sconosciuti. Una struttura di cartelle da sola non dimostra quel comportamento. Prima estrai il trasporto e la logica condivisa, poi scegli uno strumento quando l'applicazione richiede davvero più pagine.

## Le parole da riconoscere

`route`; `layout`; `feature folder`; `service`; `hook`; `separation of concerns`; `lazy loading`

## Un esempio concreto

```text
// routes.mjs: sola selezione della pagina, non un router completo
export function pageFor(pathname) {
  if (pathname === '/subjects') return 'archive';
  if (pathname === '/subjects/new') return 'create';
  return 'not-found';
}
// Possibile struttura:
// features/subjects/Archive.jsx
// features/subjects/useSubjects.js
// services/subjectsApi.js
```

Un hook personalizzato può raccogliere il flusso di caricamento già studiato se più componenti ne hanno bisogno. Condivide logica, non automaticamente lo stesso stato: ogni chiamata ha il suo. Context può evitare il passaggio di un dato realmente trasversale; reducer può rendere esplicite transizioni numerose. Non servono per una lista con due stati locali e non sostituiscono la scelta del proprietario dei dati.

## Prova tu

Implementa pageFor e prova una route sconosciuta. Per una navigazione reale, annota anche refresh su URL diretto e pulsante Indietro: il controllo breve non li esegue. Estrai poi un hook soltanto se riesci a indicare due utilizzatori con la stessa logica.

## Dove ci si confonde spesso

- Cartelle per tipo con centinaia di file
- Logica API dispersa nelle view

## Domanda di verifica

> Dove collocheresti la logica per caricare e aggiornare i soggetti?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/reusing-logic-with-custom-hooks).
