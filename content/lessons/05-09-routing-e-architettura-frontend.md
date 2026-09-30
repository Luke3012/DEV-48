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

La funzione pageFor dell'esempio decide quale pagina descrivere. Non gestisce URL nel browser, cronologia, refresh o parametri: questi sono comportamenti di un router e vanno valutati quando l'app li richiede. La struttura features/subjects raccoglie invece codice che cambia insieme alla stessa area di prodotto; separare il trasporto in un modulo aiuta a provarlo senza coinvolgere la UI.

Più avanti puoi riconoscere tre problemi diversi.

**Logica stateful ripetuta.** Immagina che StatusBar e SaveButton abbiano entrambi copiato lo stesso stato online e gli stessi listener online/offline. Quando due componenti duplicano quel comportamento, estrai la logica in un custom hook:

~~~text
StatusBar: useState + listener online/offline
SaveButton: useState + listener online/offline
                       ↓
                useOnlineStatus()
~~~

~~~jsx
import { useEffect, useState } from "react";

function useOnlineStatus() {
  const [online, setOnline] = useState(navigator.onLine);

  useEffect(() => {
    function handleOnline() { setOnline(true); }
    function handleOffline() { setOnline(false); }
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return online;
}
~~~

I due componenti possono chiamare useOnlineStatus(). Il hook riusa la logica e la cleanup; ciascuna chiamata possiede il proprio state. Se devono leggere un unico valore coordinato, scegli un proprietario comune o un contesto: estrarre il hook da solo non condivide lo stato.

**Dato che attraversa molti livelli senza essere usato nel mezzo.** Con le props esplicite, App passa currentUser a Layout, Layout lo passa a Toolbar e Toolbar ad Avatar. Se gli intermediari non lo leggono, è prop drilling. Context permette ad App di rendere un valore disponibile sotto di sé e ad Avatar di leggerlo direttamente:

~~~text
App fornisce currentUser
  └─ Layout
      └─ Toolbar
          └─ Avatar legge currentUser dal Context
~~~

~~~jsx
import { createContext, useContext } from "react";

const UserContext = createContext(null);

function Avatar() {
  const user = useContext(UserContext);
  return <span>{user.name}</span>;
}

function App({ user }) {
  return <UserContext.Provider value={user}>
    <Layout />
  </UserContext.Provider>;
}
~~~

Un esempio adatto è un account corrente o un tema usato in molti rami. Per pochi livelli, le props rendono il flusso più visibile; Context evita quei passaggi, ma non sceglie chi aggiorna lo state. Quando il valore cambia, i componenti che leggono quel Context ricevono il valore nuovo e possono renderizzare di nuovo.

**Transizioni coordinate.** Con due setter, una modifica semplice può restare in useState. Se invece molte azioni devono aggiornare insieme items, status ed error, più handler possono ripetere decisioni e dimenticare un campo. useReducer rende esplicita l'azione e centralizza il calcolo:

~~~text
evento → dispatch(action)
       → reducer(state, action)
       → nuovo state
       → render
~~~

~~~jsx
import { useReducer } from "react";

function archiveReducer(state, action) {
  if (action.type === "saveSucceeded") {
    return {
      ...state,
      items: [...state.items, action.subject],
      status: "success",
      error: ""
    };
  }
  return state;
}

const initialState = { items: [], status: "idle", error: "" };

function useArchiveState() {
  const [state, dispatch] = useReducer(archiveReducer, initialState);
  function handleSaveSuccess(subject) {
    dispatch({ type: "saveSucceeded", subject });
  }
  return { state, handleSaveSuccess };
}
~~~

Per esempio `saveSucceeded` può aggiungere il soggetto e impostare `status` a `success` in un unico passaggio. Il componente chiama `handleSaveSuccess` dopo che la richiesta è riuscita. Il reducer restituisce il nuovo stato, resta puro e non invia la richiesta: la richiesta appartiene all'handler o alla sincronizzazione con il sistema remoto. `useReducer` organizza transizioni articolate; non è automaticamente migliore di `useState`.

Anche useMemo, useCallback e memo rispondono a problemi misurati, non alla voglia di rendere un esempio più avanzato. La memoizzazione mantiene cache e confronti; un filtro semplice resta calcolato direttamente finché una misura non mostra un costo concreto.

Riferimenti: [custom hook](https://react.dev/learn/reusing-logic-with-custom-hooks), [Context](https://react.dev/learn/passing-data-deeply-with-context), [reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer).

## Prova tu

Implementa pageFor e prova una route sconosciuta. Per una navigazione reale, annota anche refresh su URL diretto e pulsante Indietro: il controllo breve non li esegue. Estrai poi un hook soltanto se riesci a indicare due utilizzatori con la stessa logica.

## Dove ci si confonde spesso

- Cartelle per tipo con centinaia di file
- Logica API dispersa nelle view

## Domanda di verifica

> Dove collocheresti la logica per caricare e aggiornare i soggetti?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.

Riferimento: [documentazione ufficiale](https://react.dev/learn/reusing-logic-with-custom-hooks).
