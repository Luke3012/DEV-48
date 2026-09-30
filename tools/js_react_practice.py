"""Lesson-specific tasks; structural UI checks are explicitly labelled."""


def executable(kind, prompt, starter, solution, cases):
    return kind, prompt, starter, solution, [dict(name=name, expression=expression, expected=expected) for name, expression, expected in cases]


def component(prompt, solution, checks, starter="// Scrivi il componente JSX qui"):
    return ("react", prompt + "\n\nF5 controlla soltanto struttura e testo: non esegue React né eventi. "
            "Per verificare il comportamento, usa un nuovo progetto di laboratorio e prova i casi indicati nel browser. "
            "Un controllo verde non dimostra che gli handler funzionino.", starter, solution,
            [dict(name=name, mode="regex", value=value) for name, value in checks])


TASKS = {
    "Moduli ed organizzazione del codice": (
        "reflection",
        "Crea due file separati `subjects.mjs` e `app.mjs`: esporta activeNames come export nominato e count come default. "
        "Importali nel secondo file, anche rinominando il default. Prova [] e due soggetti di cui uno attivo con `node app.mjs`. "
        "Qui annota esempio, output e differenza tra export nominato ed export default. Il controllo cerca solo quei due termini; "
        "confronta i file con il modello e verifica l'esecuzione nel terminale.",
        "",
        "// subjects.mjs\nexport function activeNames(items) { return items.filter(item => item.active).map(item => item.name); }\n"
        "export default function count(items) { return items.length; }\n\n"
        "// app.mjs (file separato)\nimport countItems, { activeNames } from './subjects.mjs';\n"
        "console.log(countItems([]), activeNames([])); // 0, []\n"
        "const items = [{name:'Anna', active:true}, {name:'Mario', active:false}];\n"
        "console.log(countItems(items), activeNames(items)); // 2, ['Anna']\n\n"
        "L'esempio mostra un export nominato importato con graffe e un export default rinominato localmente.",
        [{"name": "export nominato", "alternatives": ["export nominato"]}, {"name": "export default", "alternatives": ["export default"]}],
    ),
    "Promise e async/await": executable(
        "javascript",
        "Implementa `async loadNames(load)`: load è una callback che restituisce una Promise di un array di soggetti. "
        "Attendi il risultato e restituisci i nomi in ordine. Se load rifiuta, propaga l'errore; [] deve produrre []. "
        "Prima di eseguire, prevedi cosa accade se dimentichi await. I test usano Promise reali, senza rete.",
        "async function loadNames(load) {\n  // TODO\n}",
        "async function loadNames(load) {\n  const items = await load();\n  return items.map(item => item.name);\n}",
        [("attende i dati", "loadNames(() => Promise.resolve([{name:'Anna'}, {name:'Mario'}]))", ["Anna", "Mario"]),
         ("successo vuoto", "loadNames(() => Promise.resolve([]))", []),
         ("non nasconde il fallimento", "(async () => { try { await loadNames(() => Promise.reject(new Error('rete'))); return false; } catch (error) { return error.message === 'rete'; } })()", True)]),
    "Fetch: loading, error e successo": executable(
        "javascript",
        "Completa `async fetchSubjects(url, request)`. request ha il contratto di fetch ma è fornita dai test: "
        "chiamala con url, controlla response.ok, leggi response.json e restituisci i dati solo se sono un array. "
        "Su status non riuscito lancia Error, senza leggere il JSON; propaga gli errori di rete e JSON. "
        "Qui verifichiamo il trasporto; loading/retry e concorrenza appartengono al laboratorio UI.",
        "async function fetchSubjects(url, request) {\n  // TODO\n}",
        "async function fetchSubjects(url, request) {\n  const response = await request(url);\n  if (!response.ok) throw new Error(`HTTP ${response.status}`);\n  const data = await response.json();\n  if (!Array.isArray(data)) throw new Error('Risposta non valida');\n  return data;\n}",
        [("usa URL e dati", "fetchSubjects('/subjects', async url => { if (url !== '/subjects') throw new Error('URL errato'); return {ok:true, json:async () => [{id:1,name:'Anna'}]}; })", [{"id": 1, "name": "Anna"}]),
         ("vuoto non è errore", "fetchSubjects('/', async () => ({ok:true,json:async () => []}))", []),
         ("404 prima del JSON", "(async () => { let read=false; try { await fetchSubjects('/', async () => ({ok:false,status:404,json:async () => { read=true; return []; }})); return false; } catch (error) { return !read && error.message.includes('404'); } })()", True),
         ("rete", "(async () => { try { await fetchSubjects('/', async () => { throw new Error('offline'); }); return false; } catch (error) { return error.message === 'offline'; } })()", True),
         ("JSON invalido", "(async () => { try { await fetchSubjects('/', async () => ({ok:true,json:async () => {throw new Error('json');}})); return false; } catch { return true; } })()", True),
         ("forma invalida", "(async () => { try { await fetchSubjects('/', async () => ({ok:true,json:async () => ({items:[]})})); return false; } catch { return true; } })()", True)]),
    "Modello mentale, componenti e JSX": component(
        "Implementa `Badge({ active })`: una prop booleana decide il testo Attivo/Inattivo dentro uno span. "
        "Non serve stato locale. Prova entrambi i valori e verifica che le props non vengano modificate.",
        "export default function Badge({ active }) {\n  return <span>{active ? 'Attivo' : 'Inattivo'}</span>;\n}",
        [("componente Badge", r"function\s+Badge\s*\("), ("span", r"<span\b"), ("due esiti", r"Attivo.*Inattivo")]),
    "Props e composizione": component(
        "Implementa `Card({ title, children, onClose })`: mostra titolo e children, con un pulsante accessibile "
        "che chiama onClose soltanto al click. Prova due contenuti diversi; osserva zero chiamate durante render e una per click.",
        "export default function Card({ title, children, onClose }) {\n  return <section><h2>{title}</h2>{children}\n    <button type=\"button\" aria-label=\"Chiudi scheda\" onClick={onClose}>×</button>\n  </section>;\n}",
        [("composizione", r"\{children\}"), ("callback passata", r"onClick\s*=\s*\{onClose\}"), ("nome accessibile", r"aria-label\s*=")]),
    "State ed eventi": component(
        "Correggi `Counter`: il pulsante Aggiungi tre deve aumentare di tre a ogni click. "
        "Prevedi il risultato del codice iniziale e spiega perché tre sostituzioni leggono lo stesso snapshot. "
        "Nel browser verifica 0 → 3 → 6 e non spostare gli aggiornamenti nel render.",
        "import { useState } from 'react';\nexport default function Counter() {\n  const [count, setCount] = useState(0);\n  function addThree() {\n    setCount(current => current + 1);\n    setCount(current => current + 1);\n    setCount(current => current + 1);\n  }\n  return <button onClick={addThree}>Aggiungi tre: {count}</button>;\n}",
        [("stato iniziale", r"useState\s*\(\s*0\s*\)"), ("updater funzionale", r"setCount\s*\(\s*\w+\s*=>"), ("interazione", r"onClick\s*=")],
        "import { useState } from 'react';\nexport default function Counter() {\n  const [count, setCount] = useState(0);\n  function addThree() {\n    setCount(count + 1); setCount(count + 1); setCount(count + 1);\n  }\n  return <button onClick={addThree}>Aggiungi tre: {count}</button>;\n}"),
    "Liste, key e rendering condizionale": component(
        "Implementa `SubjectList({ items })`: [] mostra Nessun soggetto, altrimenti mostra i nomi in una lista con ID stabili. "
        "In ogni riga inserisci un input inizializzato al nome. Modifica il secondo input, poi togli la prima riga dal genitore: "
        "il testo digitato deve restare associato allo stesso ID. Confronta il comportamento usando key={index}.",
        "export default function SubjectList({ items }) {\n  if (items.length === 0) return <p>Nessun soggetto</p>;\n  return <ul>{items.map(item => <li key={item.id}>\n    <label>{item.name}<input defaultValue={item.name} /></label>\n  </li>)}</ul>;\n}",
        [("caso vuoto", r"Nessun soggetto"), ("ID della riga", r"key\s*=\s*\{\w+\.id\}"), ("input nella riga", r"defaultValue\s*=")]),
    "Form controllati": component(
        "Implementa `SubjectForm({ onSave })` con campo Nome e pulsante Salva. "
        "Sul submit previeni la navigazione; il nome normalizzato non può essere vuoto. Associa l'errore al campo "
        "e chiama onSave solo con un nome valido. Verifica spazi, invio da tastiera e correzione dopo un errore.",
        "import { useState } from 'react';\nexport default function SubjectForm({ onSave }) {\n  const [name, setName] = useState('');\n  const [error, setError] = useState('');\n  function submit(event) {\n    event.preventDefault();\n    if (!name.trim()) { setError('Inserisci un nome'); return; }\n    onSave(name.trim()); setName(''); setError('');\n  }\n  return <form noValidate onSubmit={submit}>\n    <label htmlFor=\"name\">Nome</label>\n    <input id=\"name\" value={name} onChange={event => setName(event.target.value)}\n      aria-invalid={Boolean(error)} aria-describedby={error ? 'error' : undefined} />\n    {error && <p id=\"error\" role=\"alert\">{error}</p>}\n    <button type=\"submit\">Salva</button>\n  </form>;\n}",
        [("submit", r"onSubmit\s*="), ("input controllato", r"value\s*=.*onChange\s*="), ("errore associato", r"aria-describedby\s*="), ("previene navigazione", r"preventDefault\s*\(")]),
    "Progettare e sollevare lo stato": component(
        "Rifattorizza `Archive({ items })` con un componente Search controllato dal genitore. "
        "Conserva solo query nello stato e deriva visible da items e query durante render. Mostra conteggio e lista. "
        "Verifica ricerca senza distinzione di maiuscole e nuovi items mentre la ricerca resta attiva. "
        "Non aggiungere effect o useMemo per sincronizzare una seconda lista.",
        "import { useState } from 'react';\nfunction Search({ query, onChange }) {\n  return <label>Cerca<input value={query} onChange={event => onChange(event.target.value)} /></label>;\n}\nexport default function Archive({ items }) {\n  const [query, setQuery] = useState('');\n  const visible = items.filter(item => item.name.toLowerCase().includes(query.toLowerCase()));\n  return <main><Search query={query} onChange={setQuery} />\n    <p>{visible.length} risultati</p><ul>{visible.map(item => <li key={item.id}>{item.name}</li>)}</ul>\n  </main>;\n}",
        [("componente di ricerca", r"function\s+Search"), ("filtro derivato", r"\.filter\s*\("), ("query al figlio", r"<Search\b[^>]*query\s*="), ("conteggio", r"visible\.length")]),
    "Effect e sincronizzazione": component(
        "Implementa `PageTitle({ title })`: sincronizza document.title con la prop e ripristina il titolo precedente nella cleanup. "
        "Verifica cambio di prop e smontaggio in Strict Mode. Prima di eseguire, prevedi il difetto se usi [] come dipendenze.",
        "import { useEffect } from 'react';\nexport default function PageTitle({ title }) {\n  useEffect(() => {\n    const previous = document.title; document.title = title;\n    return () => { document.title = previous; };\n  }, [title]);\n  return <h1>{title}</h1>;\n}",
        [("sistema esterno", r"document\.title\s*="), ("cleanup", r"return\s*\(\s*\)\s*=>"), ("dipendenza letta", r"\[\s*title\s*\]")]),
    "Caricamento dati e stati remoti": component(
        "Implementa `RemoteState({ result, onRetry })` per gli stati loading, error, empty e success. "
        "Loading ha role=status, error ha role=alert e un pulsante Riprova; empty mostra Nessun soggetto; "
        "success mostra i nomi con key stabili. Prova tutti gli stati e il click su retry. "
        "La funzione che carica i dati viene integrata nel lab-react-api, dove si verificano anche risposte fuori ordine.",
        "export default function RemoteState({ result, onRetry }) {\n  if (result.status === 'loading') return <p role=\"status\">Caricamento…</p>;\n  if (result.status === 'error') return <div><p role=\"alert\">{result.error}</p>\n    <button onClick={onRetry}>Riprova</button></div>;\n  if (result.status === 'empty') return <p>Nessun soggetto</p>;\n  return <ul>{result.data.map(item => <li key={item.id}>{item.name}</li>)}</ul>;\n}",
        [("loading annunciato", r'role\s*=\s*[\'"]status[\'"]'), ("errore annunciato", r'role\s*=\s*[\'"]alert[\'"]'), ("retry", r"onClick\s*=\s*\{onRetry\}"), ("vuoto", r"Nessun soggetto")]),
    "Routing e architettura frontend": executable(
        "javascript",
        "Implementa `pageFor(pathname)`: /subjects → archive, /subjects/new → create, tutto il resto → not-found. "
        "Non usare includes: /subjects-archive non è /subjects. Questo esercizio esegue la sola selezione della pagina; "
        "non verifica un router, il refresh né la cronologia del browser.",
        "function pageFor(pathname) {\n  // TODO\n}",
        "function pageFor(pathname) {\n  if (pathname === '/subjects') return 'archive';\n  if (pathname === '/subjects/new') return 'create';\n  return 'not-found';\n}",
        [("archivio", "pageFor('/subjects')", "archive"), ("creazione", "pageFor('/subjects/new')", "create"),
         ("sconosciuta", "pageFor('/other')", "not-found"), ("prefisso simile", "pageFor('/subjects-archive')", "not-found")]),
    "Tipi, interface e type": executable(
        "typescript", "Definisci Subject con id:number, name:string, active:boolean e note opzionale. "
        "Implementa `label(subject: Subject): string` con il nome e la nota tra parentesi se presente. "
        "I test eseguono la logica TypeScript; non sostituiscono tsc né la validazione dei dati esterni.",
        "// Definisci Subject e label qui",
        "interface Subject { id: number; name: string; active: boolean; note?: string }\n"
        "function label(subject: Subject): string { return subject.note ? `${subject.name} (${subject.note})` : subject.name; }",
        [("nota assente", "label({id:1,name:'Anna',active:true})", "Anna"),
         ("nota presente", "label({id:1,name:'Anna',active:true,note:'Nord'})", "Anna (Nord)")]),
    "Union e narrowing": executable(
        "typescript", "Definisci LoadResult come union success con data:string[] oppure error con message:string. "
        "Implementa `describe(result)` restituendo il messaggio d'errore oppure il numero di elementi seguito da ' soggetti'. "
        "Non usare any o as. I test eseguono i rami; il controllo completo dei tipi richiede tsc.",
        "// Definisci union e funzione qui",
        "type LoadResult = {status:'success';data:string[]} | {status:'error';message:string};\n"
        "function describe(result: LoadResult): string { return result.status === 'error' ? result.message : `${result.data.length} soggetti`; }",
        [("successo", "describe({status:'success',data:['Anna','Mario']})", "2 soggetti"),
         ("vuoto", "describe({status:'success',data:[]})", "0 soggetti"),
         ("errore", "describe({status:'error',message:'offline'})", "offline")]),
    "Generics essenziali": executable(
        "typescript", "Implementa `first<T>(items: T[]): T | undefined` senza any. "
        "Deve funzionare con numeri, stringhe e oggetti, e dare undefined su []. "
        "Node esegue la logica dopo aver rimosso i tipi; controlla separatamente la relazione generica con tsc.",
        "// Implementa first qui",
        "function first<T>(items: T[]): T | undefined { return items[0]; }",
        [("numeri", "first([4,9])", 4), ("testo", "first(['Anna','Mario'])", "Anna"),
         ("oggetto", "first([{id:2}])", {"id": 2}), ("assenza", "first([]) === undefined", True)]),
    "Null, unknown e confini esterni": executable(
        "typescript", "Correggi `isSubject(value: unknown)`: deve riconoscere un oggetto con id numero finito e name stringa, "
        "rifiutando null, array e campi con tipi sbagliati. La sola presenza di 'id' e 'name' non prova il contratto. "
        "I test eseguono il guard a runtime; il type checking completo resta distinto.",
        "function isSubject(value: unknown): value is {id:number;name:string} {\n"
        "  return typeof value === 'object' && value !== null && 'id' in value && 'name' in value;\n}",
        "function isSubject(value: unknown): value is {id:number;name:string} {\n"
        "  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false;\n"
        "  return 'id' in value && typeof value.id === 'number' && Number.isFinite(value.id) &&\n"
        "    'name' in value && typeof value.name === 'string';\n}",
        [("valido", "isSubject({id:1,name:'Anna'})", True), ("null", "isSubject(null)", False),
         ("array", "isSubject([])", False), ("tipi errati", "isSubject({id:'1',name:9})", False),
         ("numero non finito", "isSubject({id:NaN,name:'Anna'})", False), ("campo mancante", "isSubject({id:1})", False)]),
}


HTML_TASKS = {
    "HTML semantico e struttura": (
        "Costruisci una pagina con main, h1, nav con un link e section con h2. Usa button per un'azione. "
        "Nel browser percorri link e pulsante con Tab. Il runner verifica tag, non focus e comportamento.",
        '<nav><a href="#archive">Archivio</a></nav><main id="archive"><h1>Soggetti</h1><section><h2>Attivi</h2><button type="button">Aggiorna</button></section></main>',
        [dict(name=f"elemento {tag}", mode="tag", value=tag) for tag in ["main", "h1", "nav", "a", "section", "h2", "button"]]),
    "Form e accessibilità": (
        "Crea un form con label Nome associata a input id=name e name=name, required, "
        "descrizione id=help collegata con aria-describedby e pulsante submit. "
        "Il runner controlla struttura; verifica label, focus e invio nel browser.",
        '<form><label for="name">Nome</label><input id="name" name="name" required aria-describedby="help"><p id="help">Usa il nome completo</p><button type="submit">Salva</button></form>',
        [dict(name="label associata a input esistente", mode="label_for", value="name"),
         dict(name="campo obbligatorio", mode="attribute", value="input:required"),
         dict(name="descrizione collegata", mode="regex", value=r'aria-describedby\s*=\s*[\'"]help[\'"]'),
         dict(name="submit", mode="regex", value=r'type\s*=\s*[\'"]submit[\'"]')]),
    "Box model, cascade e specificità": (
        "Una card larga 240px ha padding 16px e bordo 2px: con content-box occupa 276px. "
        "Scrivi HTML/CSS che mantenga la larghezza totale a 240px usando border-box. "
        "Il runner cerca le regole; misura la larghezza reale negli strumenti del browser.",
        '<main><div class="card">Anna</div></main><style>.card { box-sizing:border-box; width:240px; padding:16px; border:2px solid; }</style>',
        [dict(name="border-box", mode="regex", value=r"box-sizing\s*:\s*border-box"), dict(name="larghezza", mode="regex", value=r"width\s*:\s*240px")]),
    "Flexbox e Grid": (
        "Crea una toolbar flex con due pulsanti e una griglia di card responsive con gap. "
        "Usa grid-template-columns con repeat e minmax. Il runner cerca le regole; "
        "nel browser controlla allineamento e passaggio da una a più colonne.",
        '<main><div class="toolbar"><button>Attivi</button><button>Tutti</button></div><section class="cards"><article>Anna</article><article>Mario</article></section></main><style>.toolbar{display:flex;gap:1rem;align-items:center}.cards{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(12rem,1fr))}</style>',
        [dict(name="toolbar flex", mode="regex", value=r"display\s*:\s*flex"), dict(name="griglia", mode="regex", value=r"grid-template-columns\s*:\s*repeat"), dict(name="colonne flessibili", mode="contains", value="minmax")]),
    "Responsive design": (
        "Crea una pagina con viewport configurato, larghezza fluida e max-width, "
        "con un breakpoint min-width che passa da una a due colonne. Verifica a 320px, 768px e con zoom 200%. "
        "Il runner controlla la presenza delle regole, non overflow e leggibilità.",
        '<meta name="viewport" content="width=device-width,initial-scale=1"><main class="page"><section>Archivio</section><aside>Filtri</aside></main><style>.page{width:calc(100% - 2rem);max-width:72rem;margin:auto;display:grid;gap:1rem}@media(min-width:48rem){.page{grid-template-columns:2fr 1fr}}</style>',
        [dict(name="viewport", mode="regex", value=r'name\s*=\s*[\'"]viewport[\'"]'), dict(name="larghezza massima", mode="contains", value="max-width"), dict(name="breakpoint", mode="regex", value=r"@media\s*\(\s*min-width")]),
}
