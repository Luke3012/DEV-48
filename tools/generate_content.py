from __future__ import annotations

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
LESSONS = CONTENT / "lessons"


TOPICS = [
    # module, title, gruppo editoriale, minuti, obbligatoria, riepilogo, concetti, esempio, errori, domanda
    ("orientamento", "Come affrontare un live coding", 1, 20, True,
     "Trasformare una richiesta vaga in passi verificabili senza precipitarsi sulla tastiera.",
     "requisiti;input e output;casi limite;pseudocodice;verifica incrementale",
     "// 1. Chiarisci input/output\n// 2. Scrivi un caso di esempio\n// 3. Implementa la versione minima\n// 4. Verifica e migliora",
     "Iniziare a programmare senza aver ripetuto il requisito; restare in silenzio quando ci si blocca.",
     "Cosa fai nei primi due minuti di un esercizio tecnico?"),
    ("orientamento", "Metodo di debugging sistematico", 1, 25, True,
     "Passare da 'non funziona' a un'ipotesi falsificabile e a una correzione minima.",
     "riproduzione;messaggio di errore;ipotesi;isolamento;regressione",
     "function debug(value) {\n  console.log({ value, type: typeof value });\n  return value;\n}",
     "Cambiare più cose insieme; ignorare stack trace e condizioni di riproduzione.",
     "Descrivi come indagheresti un bug che compare solo con dati vuoti."),

    ("javascript", "Valori, tipi e confronti", 1, 35, True,
     "Capire cosa contiene una variabile e prevedere conversioni e confronti.",
     "string;number;boolean;null;undefined;typeof;===;truthy e falsy",
     "const age = 30;\nconst label = age >= 18 ? 'adult' : 'minor';\nconsole.log(typeof age, label);",
     "Usare ==; confondere null con undefined; considerare '0' come numero zero.",
     "Qual è la differenza tra == e ===?"),
    ("javascript", "Scope, const, let e closure", 1, 40, True,
     "Comprendere dove vive una variabile e perché una funzione ricorda il contesto esterno.",
     "scope di blocco;const;let;closure;shadowing;funzione interna",
     "function counter() {\n  let value = 0;\n  return () => ++value;\n}\nconst next = counter();",
     "Usare var senza motivo; credere che const renda immutabile un oggetto.",
     "Che cos'è una closure e quando può essere utile?"),
    ("javascript", "Funzioni e responsabilità", 1, 40, True,
     "Scrivere funzioni piccole, prevedibili e con input/output espliciti.",
     "parametri;return;arrow function;funzione pura;default parameter;early return",
     "function fullName(first, last = '') {\n  if (!first) return 'Unknown';\n  return `${first} ${last}`.trim();\n}",
     "Funzioni che modificano variabili globali; troppi rami e responsabilità.",
     "Che differenza c'è tra restituire un valore e produrre un side effect?"),
    ("javascript", "Array: map, filter, find e some", 1, 55, True,
     "Trasformare e interrogare collezioni senza cicli confusi.",
     "map;filter;find;some;every;callback;array originale",
     "const activeNames = users\n  .filter(user => user.active)\n  .map(user => user.name);",
     "Usare map quando serve filter; dimenticare che find può restituire undefined.",
     "Quando useresti find invece di filter?"),
    ("javascript", "Oggetti, destructuring e spread", 1, 45, True,
     "Leggere e creare copie aggiornate di strutture dati applicative.",
     "proprietà;destructuring;spread;optional chaining;nullish coalescing;copia superficiale",
     "const updated = { ...user, profile: { ...user.profile, city: 'Milano' } };\nconst city = updated.profile?.city ?? 'N/D';",
     "Credere che spread faccia una copia profonda; modificare oggetti condivisi.",
     "Perché {...obj} non è sempre una copia completamente indipendente?"),
    ("javascript", "Immutabilità e operazioni CRUD", 1, 50, True,
     "Aggiungere, modificare ed eliminare elementi nel modo atteso da React.",
     "spread;map;filter;identità;aggiornamento immutabile;CRUD",
     "const added = [...items, newItem];\nconst changed = items.map(x => x.id === id ? {...x, active: true} : x);\nconst removed = items.filter(x => x.id !== id);",
     "push sullo state; cambiare direttamente una proprietà; perdere campi durante una copia.",
     "Come aggiorni un elemento di un array senza modificarlo direttamente?"),
    ("javascript", "Reduce, Set e Map", 1, 35, False,
     "Aggregare valori e scegliere strutture dati adeguate per lookup e unicità.",
     "reduce;accumulatore;Set;Map;unicità;lookup",
     "const total = orders.reduce((sum, order) => sum + order.amount, 0);\nconst zones = [...new Set(users.map(u => u.zone))];",
     "Usare reduce per rendere il codice inutilmente compatto; confondere Map con map.",
     "Quando preferiresti un oggetto Map rispetto a un array?"),
    ("javascript", "Moduli ed organizzazione del codice", 1, 30, False,
     "Separare responsabilità usando export e import comprensibili.",
     "export nominato;export default;import;modulo;dipendenza;API pubblica",
     "// format.js\nexport function formatDate(value) { return new Date(value).toLocaleDateString('it-IT'); }\n// app.js\nimport { formatDate } from './format.js';",
     "Dipendenze circolari; esportare dettagli interni; file contenitore gigantesco.",
     "Differenza tra export nominato ed export default?"),
    ("javascript", "Errori e validazione", 1, 40, True,
     "Rifiutare input invalidi e distinguere errore previsto da bug di programmazione.",
     "throw;Error;try/catch;validazione;guard clause;messaggio utile",
     "function parseAge(value) {\n  const age = Number(value);\n  if (!Number.isFinite(age) || age < 0) throw new Error('Invalid age');\n  return age;\n}",
     "Catturare tutto e ignorare l'errore; mostrare dettagli sensibili all'utente.",
     "Quando è corretto lanciare un errore invece di restituire null?"),

    ("async_http", "Promise e async/await", 1, 50, True,
     "Ragionare su operazioni che terminano in futuro senza bloccare il programma.",
     "Promise;pending;fulfilled;rejected;async;await;concorrenza",
     "async function load() {\n  try { return await getData(); }\n  catch (error) { console.error(error); throw error; }\n}",
     "Dimenticare await; mescolare then e await; perdere gli errori asincroni.",
     "Cosa restituisce sempre una funzione dichiarata async?"),
    ("async_http", "HTTP e API REST", 1, 45, True,
     "Collegare metodi, risorse e status code a operazioni applicative.",
     "GET;POST;PUT;PATCH;DELETE;status code;header;body;JSON",
     "GET /api/subjects/42\nPATCH /api/subjects/42\nContent-Type: application/json\n\n{\"active\": false}",
     "Usare GET per modificare dati; restituire sempre 200; confondere PUT e PATCH.",
     "Quale status useresti dopo la creazione riuscita di una risorsa?"),
    ("async_http", "Fetch: loading, error e successo", 1, 55, True,
     "Implementare una richiesta robusta e rappresentarne tutti gli stati nella UI.",
     "fetch;response.ok;response.json;loading;errore;finally;AbortController",
     "const response = await fetch('/api/subjects');\nif (!response.ok) throw new Error(`HTTP ${response.status}`);\nconst data = await response.json();",
     "Credere che fetch rifiuti automaticamente su 404; non gestire richieste obsolete.",
     "Perché bisogna controllare response.ok?"),
    ("async_http", "Autenticazione, CORS e segreti", 2, 40, True,
     "Distinguere identità, permessi, regole del browser e gestione delle credenziali.",
     "autenticazione;autorizzazione;token;cookie;CORS;variabile d'ambiente;segreto",
     "Authorization: Bearer <token>\n// Le chiavi private restano sul server, mai nel bundle frontend.",
     "Mettere API key nel frontend; usare CORS come sistema di autenticazione.",
     "CORS protegge una API da qualsiasi client malevolo?"),

    ("html_css", "HTML semantico e struttura", 1, 40, True,
     "Scegliere elementi che descrivono il significato, non soltanto l'aspetto.",
     "header;nav;main;section;article;button;heading;semantica",
     "<main>\n  <h1>Archivio soggetti</h1>\n  <section aria-labelledby=\"active-title\">...</section>\n</main>",
     "Div per ogni cosa; gerarchia heading incoerente; elementi cliccabili non accessibili.",
     "Perché un button è preferibile a un div con onClick?"),
    ("html_css", "Form e accessibilità", 1, 45, True,
     "Costruire form utilizzabili da tastiera e tecnologie assistive.",
     "form;label;name;required;fieldset;aria-describedby;focus;validazione",
     "<label for=\"email\">Email</label>\n<input id=\"email\" name=\"email\" type=\"email\" required>",
     "Placeholder al posto della label; focus invisibile; errori non associati al campo.",
     "Qual è la differenza tra validazione client e server?"),
    ("html_css", "Box model, cascade e specificità", 1, 45, True,
     "Prevedere dimensioni e regole CSS effettivamente applicate.",
     "content;padding;border;margin;box-sizing;cascade;specificità;inheritance",
     "*, *::before, *::after { box-sizing: border-box; }\n.card { padding: 1rem; border: 1px solid #334155; }",
     "Compensare la specificità con !important; dimenticare box-sizing.",
     "Come viene determinata la regola CSS vincente?"),
    ("html_css", "Flexbox e Grid", 1, 55, True,
     "Scegliere il sistema di layout in base alla relazione tra gli elementi.",
     "asse principale;asse trasversale;gap;flex-grow;grid-template-columns;minmax",
     ".toolbar { display:flex; align-items:center; gap:.75rem; }\n.cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(16rem,1fr)); gap:1rem; }",
     "Usare position absolute per layout ordinari; non capire quale sia l'asse attivo.",
     "Quando preferiresti Grid a Flexbox?"),
    ("html_css", "Responsive design", 1, 40, True,
     "Progettare layout fluidi che restano leggibili su viewport differenti.",
     "mobile first;media query;unità relative;max-width;overflow;viewport",
     ".page { width:min(100% - 2rem, 72rem); margin-inline:auto; }\n@media (min-width: 48rem) { .sidebar { display:block; } }",
     "Breakpoint legati a singoli dispositivi; larghezze fisse; overflow nascosto indiscriminato.",
     "Cosa significa progettare mobile first?"),

    ("typescript", "Tipi, interface e type", 2, 40, True,
     "Descrivere il contratto dei dati e ottenere errori prima dell'esecuzione.",
     "type annotation;interface;type alias;optional property;readonly;structural typing",
     "interface Subject { id: number; name: string; active: boolean; note?: string }\nfunction label(subject: Subject): string { return subject.name; }",
     "Usare any per silenziare errori; considerare i tipi come validazione runtime.",
     "Interface TypeScript verifica davvero il JSON ricevuto dalla rete?"),
    ("typescript", "Union e narrowing", 2, 40, True,
     "Rappresentare stati alternativi e restringere il tipo in modo sicuro.",
     "union;literal type;discriminated union;typeof;in;narrowing;never",
     "type Result = {status:'ok'; data:string[]} | {status:'error'; message:string};\nfunction render(r:Result){ return r.status === 'ok' ? r.data.join(', ') : r.message; }",
     "Asserzioni as usate per forzare; union troppo generiche; rami non esaustivi.",
     "Che vantaggio offre una discriminated union?"),
    ("typescript", "Generics essenziali", 2, 35, False,
     "Mantenere relazioni tra tipi senza ricorrere ad any.",
     "generic;parametro di tipo;constraint;Array<T>;Promise<T>;riuso",
     "function first<T>(items: T[]): T | undefined { return items[0]; }\nconst value = first<number>([10, 20]);",
     "Generics inutilmente complessi; nomi incomprensibili; constraint mancanti.",
     "Perché first<T> è più sicura di una funzione che restituisce any?"),
    ("typescript", "Null, unknown e confini esterni", 2, 40, True,
     "Trattare dati esterni come non affidabili prima di usarli nel dominio.",
     "unknown;null;undefined;type guard;validation;optional chaining;boundary",
     "function isSubject(value: unknown): value is {id:number; name:string} {\n  return typeof value === 'object' && value !== null && 'id' in value && 'name' in value;\n}",
     "Convertire unknown in un tipo con as; fidarsi del JSON; usare ! senza prova.",
     "Perché unknown è preferibile ad any per un input esterno?"),

    ("react", "Modello mentale, componenti e JSX", 1, 50, True,
     "Descrivere la UI come funzione di props e stato mediante componenti puri.",
     "component;JSX;render;purezza;composizione;albero UI;espressione",
     "function Badge({ active }) {\n  return <span className={active ? 'active' : 'idle'}>{active ? 'Attivo' : 'Inattivo'}</span>;\n}",
     "Modificare dati durante il render; componenti monolitici; confondere JSX con HTML.",
     "Perché il render di un componente dovrebbe essere puro?"),
    ("react", "Props e composizione", 1, 40, True,
     "Passare dati e comportamento dal genitore senza accoppiare i componenti.",
     "props;children;callback;one-way data flow;composizione;default value",
     "function Card({ title, children, onClose }) {\n return <section><button onClick={onClose}>×</button><h2>{title}</h2>{children}</section>;\n}",
     "Modificare le props; passare interi store quando bastano due valori.",
     "Come comunica un componente figlio un evento al genitore?"),
    ("react", "State ed eventi", 1, 55, True,
     "Aggiornare l'interfaccia in risposta alle interazioni usando useState.",
     "useState;setter;event handler;re-render;functional update;snapshot",
     "const [count, setCount] = useState(0);\n<button onClick={() => setCount(current => current + 1)}>{count}</button>",
     "Chiamare il setter durante il render; leggere state come variabile immediatamente mutabile.",
     "Quando serve la forma funzionale di setState?"),
    ("react", "Liste, key e rendering condizionale", 1, 50, True,
     "Renderizzare collezioni mantenendo correttamente identità e stato degli elementi.",
     "map;key;identità;conditional rendering;empty state;fragment",
     "{items.length === 0 ? <EmptyState /> : items.map(item => <Row key={item.id} item={item} />)}",
     "Usare l'indice come key in liste modificabili; dimenticare lo stato vuoto.",
     "Perché la key deve essere stabile e unica tra fratelli?"),
    ("react", "Form controllati", 2, 60, True,
     "Mantenere input, validazione e submit coerenti con lo state React.",
     "controlled input;value;onChange;onSubmit;preventDefault;validation;error state",
     "const [name,setName]=useState('');\n<form onSubmit={handleSubmit}><input value={name} onChange={e=>setName(e.target.value)} /></form>",
     "Mescolare input controllati e non controllati; validare soltanto dopo la chiamata API.",
     "Che cosa rende controllato un input React?"),
    ("react", "Progettare e sollevare lo stato", 2, 55, True,
     "Collocare ogni informazione nel proprietario comune più vicino evitando duplicazioni.",
     "single source of truth;lifting state;derived state;normalizzazione;prop drilling",
     "const visible = items.filter(item => item.name.toLowerCase().includes(query.toLowerCase()));\n// visible è derivato: non richiede un secondo useState.",
     "Duplicare stato derivabile; sincronizzare copie della stessa informazione con effect.",
     "Come riconosci uno state che dovrebbe essere derivato?"),
    ("react", "Effect e sincronizzazione", 2, 60, True,
     "Usare useEffect solo per sincronizzarsi con sistemi esterni e gestire cleanup.",
     "useEffect;dependency array;cleanup;subscription;fetch;race condition;Strict Mode",
     "useEffect(() => {\n const controller=new AbortController();\n load(controller.signal);\n return () => controller.abort();\n}, [subjectId]);",
     "Usare effect per calcoli derivabili; dipendenze mancanti; cleanup assente.",
     "Quali operazioni non richiedono useEffect?"),
    ("react", "Caricamento dati e stati remoti", 2, 60, True,
     "Rappresentare esplicitamente idle, loading, success, empty ed error.",
     "remote state;loading;error;retry;empty state;optimistic update;cache",
     "if (status === 'loading') return <Spinner />;\nif (status === 'error') return <ErrorPanel onRetry={load} />;\nreturn data.length ? <List data={data}/> : <EmptyState/>;",
     "Mostrare schermata vuota durante il caricamento; ignorare retry e richieste concorrenti.",
     "Quali stati UI devi considerare quando interroghi una API?"),
    ("react", "Routing e architettura frontend", 2, 45, False,
     "Dividere pagine, feature, componenti e accesso dati mantenendo dipendenze leggibili.",
     "route;layout;feature folder;service;hook;separation of concerns;lazy loading",
     "src/\n  app/\n  features/subjects/\n  components/ui/\n  services/api.ts",
     "Cartelle per tipo con centinaia di file; logica API dispersa nelle view.",
     "Dove collocheresti la logica per caricare e aggiornare i soggetti?"),

    ("backend", "Node, event loop e moduli", 2, 35, True,
     "Comprendere perché JavaScript server gestisce bene operazioni I/O e dove può bloccarsi.",
     "Node.js;event loop;I/O asincrono;CommonJS;ES modules;process;package.json",
     "import { readFile } from 'node:fs/promises';\nconst config = JSON.parse(await readFile('config.json', 'utf8'));",
     "Lavoro CPU pesante nel thread principale; callback bloccanti; moduli mescolati.",
     "Che cosa succede se una route esegue un calcolo sincrono molto lungo?"),
    ("backend", "Route, middleware e validazione", 2, 55, True,
     "Seguire il percorso request → middleware → handler → servizio → response.",
     "router;middleware;handler;service;repository;validation;error middleware",
     "app.post('/subjects', validateSubject, async (req,res,next) => {\n try { res.status(201).json(await service.create(req.body)); } catch(e) { next(e); }\n});",
     "Business logic nella route; input non validato; catch duplicati ovunque.",
     "Qual è la responsabilità di un middleware?"),
    ("backend", "Sicurezza web essenziale", 2, 45, True,
     "Riconoscere i rischi più comuni e applicare difese nei confini corretti.",
     "SQL injection;XSS;CSRF;hash password;least privilege;rate limit;secret",
     "// Query parametrizzata\ndb.prepare('SELECT * FROM users WHERE email = ?').get(email);",
     "Concatenare SQL; memorizzare password; fidarsi della validazione frontend.",
     "Perché una query parametrizzata riduce SQL injection?"),

    ("sql", "SELECT, filtri e ordinamento", 2, 45, True,
     "Estrarre solo righe e colonne necessarie con condizioni leggibili.",
     "SELECT;FROM;WHERE;AND;OR;ORDER BY;LIMIT;alias",
     "SELECT id, name, checks\nFROM subjects\nWHERE active = 1 AND zone = 'Centro'\nORDER BY checks DESC;",
     "SELECT * indiscriminato; condizioni ambigue; ordinamento dimenticato.",
     "In quale ordine logico vengono valutate FROM, WHERE, SELECT e ORDER BY?"),
    ("sql", "Relazioni e JOIN", 2, 55, True,
     "Combinare entità correlate comprendendo cardinalità e righe mancanti.",
     "primary key;foreign key;INNER JOIN;LEFT JOIN;cardinalità;alias",
     "SELECT s.name, m.type\nFROM subjects s\nLEFT JOIN measures m ON m.subject_id = s.id;",
     "JOIN senza condizione; INNER JOIN quando servono anche elementi senza relazione.",
     "Differenza tra INNER JOIN e LEFT JOIN?"),
    ("sql", "Vincoli, indici e normalizzazione", 2, 40, True,
     "Proteggere integrità e prestazioni senza duplicare dati inutilmente.",
     "NOT NULL;UNIQUE;CHECK;FOREIGN KEY;index;normalizzazione;query plan",
     "CREATE INDEX idx_subjects_zone_active ON subjects(zone, active);",
     "Indice su ogni colonna; duplicazione di dati derivabili; vincoli solo nell'app.",
     "Qual è il costo di mantenere un indice?"),
    ("sql", "Transazioni e concorrenza", 2, 40, True,
     "Rendere atomiche operazioni che devono riuscire o fallire insieme.",
     "transaction;BEGIN;COMMIT;ROLLBACK;atomicità;isolamento;lock",
     "BEGIN;\nUPDATE accounts SET balance=balance-100 WHERE id=1;\nUPDATE accounts SET balance=balance+100 WHERE id=2;\nCOMMIT;",
     "Commit parziale; transazioni troppo lunghe; nessuna gestione del rollback.",
     "Perché un trasferimento richiede una transazione?"),

    ("git_testing", "Git: working tree, staging e commit", 2, 35, True,
     "Capire cosa viene registrato e produrre commit piccoli e descrittivi.",
     "working tree;staging area;commit;git status;git diff;git add;git restore",
     "git status\ngit diff\ngit add src/subjects.js\ngit diff --staged\ngit commit -m \"feat: add subject filtering\"",
     "git add . senza controllare; commit final version; credenziali versionate.",
     "Differenza tra git diff e git diff --staged?"),
    ("git_testing", "Branch, merge e conflitti", 2, 40, True,
     "Isolare una modifica e integrare storie divergenti senza perdere lavoro.",
     "branch;HEAD;switch;merge;conflict;rebase;remote",
     "git switch -c feature/subject-search\n# modifica, test, commit\ngit switch main\ngit merge feature/subject-search",
     "Risolvere un conflitto cancellando marcatori senza capire entrambe le versioni.",
     "Che cosa rappresenta HEAD?"),
    ("git_testing", "Test unitari, integrazione ed E2E", 2, 50, True,
     "Scegliere il livello di test più economico capace di coprire il rischio.",
     "unit test;integration test;E2E;arrange-act-assert;mock;regression;test pyramid",
     "it('filters active subjects', () => {\n const result = filterActive([{id:1,active:true},{id:2,active:false}]);\n expect(result).toEqual([{id:1,active:true}]);\n});",
     "Testare dettagli interni; mockare tutto; test senza asserzioni significative.",
     "Quando preferiresti un test di integrazione a uno unitario?"),
    ("git_testing", "Code review e refactoring", 2, 45, True,
     "Migliorare struttura senza cambiare comportamento e comunicare rischi concreti.",
     "refactoring;behavior preservation;code smell;cohesion;coupling;review;technical debt",
     "// Prima caratterizza il comportamento con test, poi estrai una responsabilità alla volta.",
     "Grande riscrittura senza test; commenti sullo stile personale; nessuna priorità.",
     "Come rifattorizzeresti in sicurezza un file di migliaia di righe?"),

    ("wordpress", "PHP e ciclo di un plugin WordPress", 2, 30, False,
     "Riconoscere struttura, hook e confini minimi di un plugin custom.",
     "PHP;plugin header;action;filter;shortcode;activation hook;namespace",
     "<?php\n/** Plugin Name: Subject Tools */\nadd_action('init', function () { /* register */ });",
     "Modificare il core; eseguire codice globale pesante; nomi di funzione generici.",
     "Differenza tra action e filter in WordPress?"),
    ("wordpress", "Sicurezza WordPress", 2, 30, False,
     "Applicare sanitizzazione, escaping, nonce e capability nel punto corretto.",
     "sanitize_text_field;esc_html;nonce;current_user_can;$wpdb->prepare;capability",
     "$name = sanitize_text_field($_POST['name'] ?? '');\necho esc_html($name);",
     "Confondere sanitizzazione input ed escaping output; nonce usato come autorizzazione.",
     "Qual è la differenza tra sanitizzare ed eseguire escaping?"),

    ("portfolio", "Presentare l'architettura di un'app Electron", 2, 45, True,
     "Spiegare Electron main/preload/renderer, IPC, SQLite e trade-off offline-first.",
     "Electron main;preload;renderer;IPC;context isolation;repository;SQLite;offline-first",
     "Renderer React → API tipizzata del preload → IPC → service → repository SQLite",
     "Elencare librerie senza motivare; non riconoscere file troppo grandi e debito tecnico.",
     "Perché il renderer non accede direttamente a filesystem e database?"),
    ("portfolio", "Presentare una pipeline AI multimodale", 2, 45, True,
     "Raccontare un flusso AI distribuito, fallimenti parziali e scelte di deployment.",
     "Unity;Whisper;RAG;ChromaDB;Ollama;TTS;systemd;Caddy;fallback;observability",
     "Audio → STT → recupero memoria per avatar → generazione → TTS streaming → UI",
     "Dire soltanto 'usa IA'; non spiegare latenze, errori e separazione dei dati.",
     "Che cosa accade se il servizio TTS non è disponibile?"),
    ("portfolio", "Parlare onestamente dell'uso dell'IA", 2, 35, True,
     "Distinguere contributo personale, accelerazione assistita e responsabilità tecnica.",
     "ownership;verifica;debugging;trade-off;trasparenza;strumento;autonomia",
     "Ho usato l'IA per accelerare scaffolding e alternative; ho verificato integrazione, test e comportamento. Sto riallenando la prima implementazione autonoma.",
     "Negare l'uso; attribuirsi codice non compreso; descriversi come semplice esecutore dei prompt.",
     "Quale parte di un tuo progetto sapresti ricostruire senza assistenza?"),
    ("portfolio", "Comunicare decisioni tecniche e risultati", 2, 50, True,
     "Raccontare il lavoro svolto con contesto, decisioni, verifiche e risultati concreti.",
     "contesto;responsabilità;decisione;verifica;risultato;lezione appresa;collaborazione",
     "Situazione → problema osservabile → opzioni considerate → scelta → risultato misurabile → cosa migliorerei.",
     "Risposte astratte; parlare solo al plurale; non quantificare risultato o apprendimento.",
     "Raccontami un bug difficile che hai risolto."),
]


MODULES = [
    ("orientamento", "00", "Orientamento e diagnostico", "Imposta un metodo di studio pratico e un approccio sistematico al debugging."),
    ("javascript", "01", "JavaScript fondamentale", "Il linguaggio che devi saper scrivere senza assistenza."),
    ("async_http", "02", "Async, HTTP e API", "Dati remoti, errori e confini di sicurezza."),
    ("html_css", "03", "HTML e CSS", "Struttura semantica, accessibilità e layout."),
    ("typescript", "04", "TypeScript", "Contratti e dati affidabili."),
    ("react", "05", "React", "Componenti, stato, form, effect e CRUD."),
    ("backend", "06", "Backend e sicurezza", "Node, route, servizi e rischi web."),
    ("sql", "07", "SQL e database", "Query, relazioni, integrità e transazioni."),
    ("git_testing", "08", "Git, test e debugging", "Workflow professionale e qualità."),
    ("wordpress", "09", "WordPress essenziale", "Plugin custom e sicurezza di base."),
    ("portfolio", "10", "Progetti e comunicazione tecnica", "Racconta progetti complessi, decisioni tecniche e risultati in modo chiaro."),
]


JS_TASKS = [
    ("classifyValue", "Scrivi `classifyValue(value)` che restituisce `'missing'` per null/undefined, `'empty'` per stringa vuota e il risultato di `typeof` negli altri casi.",
     "function classifyValue(value) {\n  if (value === null || value === undefined) return 'missing';\n  if (value === '') return 'empty';\n  return typeof value;\n}",
     [("null", "classifyValue(null)", "missing"), ("empty", "classifyValue('')", "empty"), ("number", "classifyValue(3)", "number")]),
    ("createCounter", "Scrivi `createCounter()` che restituisce una funzione. Ogni chiamata deve restituire 1, poi 2, poi 3.",
     "function createCounter() {\n  let value = 0;\n  return function () { value += 1; return value; };\n}",
     [("prima chiamata", "(() => { const c=createCounter(); return c(); })()", 1), ("stato conservato", "(() => { const c=createCounter(); c(); return c(); })()", 2)]),
    ("fullName", "Scrivi `fullName(first, last)`; rimuovi spazi esterni e restituisci `'Unknown'` se first è vuoto.",
     "function fullName(first, last = '') {\n  const cleanFirst = String(first ?? '').trim();\n  if (!cleanFirst) return 'Unknown';\n  return `${cleanFirst} ${String(last ?? '').trim()}`.trim();\n}",
     [("nome completo", "fullName(' Giulia ', ' Rossi ')", "Giulia Rossi"), ("mancante", "fullName('', 'Rossi')", "Unknown")]),
    ("activeNames", "Scrivi `activeNames(users)` che restituisce i nomi degli utenti attivi, in ordine, senza modificare l'array.",
     "function activeNames(users) {\n  return users.filter(user => user.active).map(user => user.name);\n}",
     [("filtra e trasforma", "activeNames([{name:'A',active:true},{name:'B',active:false},{name:'C',active:true}])", ["A", "C"]), ("vuoto", "activeNames([])", [])]),
    ("moveUser", "Scrivi `moveUser(user, city)` che restituisce una copia con `profile.city` aggiornata senza modificare user.",
     "function moveUser(user, city) {\n  return { ...user, profile: { ...(user.profile ?? {}), city } };\n}",
     [("aggiorna annidato", "moveUser({id:1,profile:{city:'Roma',age:30}},'Milano')", {"id":1,"profile":{"city":"Milano","age":30}}), ("profile assente", "moveUser({id:2},'Milano')", {"id":2,"profile":{"city":"Milano"}})]),
    ("updateSubject", "Scrivi `updateSubject(items, id, patch)` con map e spread. Deve aggiornare solo l'elemento indicato.",
     "function updateSubject(items, id, patch) {\n  return items.map(item => item.id === id ? { ...item, ...patch } : item);\n}",
     [("aggiornamento", "updateSubject([{id:1,a:1},{id:2,a:2}],2,{a:9})", [{"id":1,"a":1},{"id":2,"a":9}]), ("id assente", "updateSubject([{id:1,a:1}],9,{a:2})", [{"id":1,"a":1}])]),
    ("sumActiveChecks", "Scrivi `sumActiveChecks(items)` che somma checks soltanto per gli elementi attivi.",
     "function sumActiveChecks(items) {\n  return items.filter(item => item.active).reduce((sum, item) => sum + item.checks, 0);\n}",
     [("somma", "sumActiveChecks([{active:true,checks:4},{active:false,checks:9},{active:true,checks:2}])", 6), ("vuoto", "sumActiveChecks([])", 0)]),
    ("uniqueZones", "Scrivi `uniqueZones(users)` che restituisce le zone uniche mantenendo l'ordine di prima apparizione.",
     "function uniqueZones(users) {\n  return [...new Set(users.map(user => user.zone))];\n}",
     [("uniche", "uniqueZones([{zone:'Centro'},{zone:'Nord'},{zone:'Centro'}])", ["Centro","Nord"])]),
    ("parsePositive", "Scrivi `parsePositive(value)` che converte il valore in numero e lancia Error se non è finito o è negativo.",
     "function parsePositive(value) {\n  const number = Number(value);\n  if (!Number.isFinite(number) || number < 0) throw new Error('Invalid positive number');\n  return number;\n}",
     [("converte", "parsePositive('12')", 12), ("zero", "parsePositive(0)", 0), ("errore", "(() => { try { parsePositive(-1); return false; } catch { return true; } })()", True)]),
]


SQL_TASKS = [
    ("Seleziona id, name e checks dei soggetti attivi, ordinati per checks decrescente.",
     "SELECT id, name, checks FROM subjects WHERE active = 1 ORDER BY checks DESC;",
     [[4,"Sara Neri",9],[1,"Mario Rossi",4],[3,"Paolo Verdi",2]]),
    ("Seleziona name e type di tutti i soggetti con una misura, ordinati per name.",
     "SELECT s.name, m.type FROM subjects s INNER JOIN measures m ON m.subject_id = s.id ORDER BY s.name;",
     [["Mario Rossi","Obbligo"],["Paolo Verdi","Controllo"],["Sara Neri","Obbligo"]]),
    ("Conta i soggetti per zona e restituisci zone e totale, ordinate alfabeticamente.",
     "SELECT zone, COUNT(*) AS total FROM subjects GROUP BY zone ORDER BY zone;",
     [["Centro",2],["Nord",1],["Sud",1]]),
    ("Seleziona nome e tipo delle sole misure ancora aperte, ordinate per nome.",
     "SELECT s.name, m.type FROM subjects s JOIN measures m ON m.subject_id=s.id WHERE m.end_date IS NULL ORDER BY s.name;",
     [["Mario Rossi","Obbligo"],["Sara Neri","Obbligo"]]),
]


def slugify(value: str) -> str:
    value = value.lower().replace("à", "a").replace("è", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


MODULE_PERSPECTIVES = {
    "orientamento": "Qui non conta partire in fretta: conta rendere visibile il ragionamento. Chi ti osserva deve capire quali informazioni hai raccolto, quale ipotesi stai provando e come decidi se il risultato è corretto.",
    "javascript": "In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.",
    "async_http": "Quando entra in gioco una richiesta di rete, il risultato non arriva subito e può anche non arrivare affatto. Per questo devi ragionare sia sul dato atteso sia sugli stati di attesa, errore e annullamento.",
    "html_css": "Una pagina ben costruita non è soltanto bella: comunica una struttura, funziona da tastiera e si adatta allo spazio disponibile. Parti dal significato degli elementi, poi occupati del loro aspetto.",
    "typescript": "TypeScript ti aiuta a rendere esplicite le promesse del codice. Un tipo utile racconta quali dati accetti, quali casi sono possibili e quali controlli restano comunque necessari durante l'esecuzione.",
    "react": "In React la domanda principale è sempre la stessa: da quali dati dipende questa parte dell'interfaccia? Individua chi possiede quei dati e lascia che il rendering descriva ciò che l'utente deve vedere in quel momento.",
    "backend": "Sul backend ogni dato attraversa un confine: arriva da una richiesta, viene controllato, passa nella logica applicativa e produce una risposta. Tenere distinti questi passaggi rende più semplici sia gli errori sia la sicurezza.",
    "sql": "Con SQL conviene tradurre la richiesta in una domanda precisa sui dati: quali righe servono, come sono collegate e in quale ordine devono uscire. Prima pensa al risultato, poi scrivi la query.",
    "git_testing": "Questi strumenti servono a ridurre l'incertezza. Git rende leggibile la storia delle modifiche; test e debugger ti aiutano a dimostrare che un comportamento esiste davvero e continua a funzionare.",
    "wordpress": "In WordPress il codice vive dentro un sistema già avviato. Devi capire in quale momento agganciare la tua funzione e trattare ogni dato ricevuto come non affidabile fino a quando non viene controllato.",
    "portfolio": "Non devi presentare un progetto come se fosse perfetto. Una risposta credibile spiega il problema, la scelta fatta, il compromesso accettato e ciò che oggi miglioreresti con più tempo o più esperienza.",
}


MODULE_EXAMPLE_GUIDES = {
    "orientamento": "Usalo come una scaletta da dire ad alta voce. Ogni riga corrisponde a una decisione che anche l'intervistatore può seguire.",
    "javascript": "Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.",
    "async_http": "Individua il momento in cui parte l'operazione, quello in cui arriva la risposta e il punto in cui viene gestito un fallimento.",
    "html_css": "Prima leggi la struttura HTML e prova a descriverla senza parlare di colori. Poi osserva come il CSS distribuisce lo spazio e che cosa succede restringendo la finestra.",
    "typescript": "Guarda quali errori il tipo può impedire prima dell'avvio e quali dati, soprattutto quelli esterni, richiedono ancora una verifica a runtime.",
    "react": "Distingui props, stato e valori calcolati. Poi segui l'evento: quale setter viene chiamato e quale parte della UI cambia al rendering successivo?",
    "backend": "Segui la richiesta nell'ordine reale: ingresso, controllo, logica, accesso ai dati e risposta. Nota anche dove finirebbe un errore.",
    "sql": "Leggi prima `FROM` e `JOIN`, poi i filtri e infine le colonne restituite. Immagina due o tre righe concrete per controllare il risultato.",
    "git_testing": "Chiediti quale prova concreta offre questo comando o questo test. Se fallisse, il messaggio dovrebbe aiutarti a restringere il problema.",
    "wordpress": "Individua l'hook, il dato ricevuto e il punto in cui viene sanitizzato o mostrato. Sono i tre passaggi che spiegano quasi tutto il frammento.",
    "portfolio": "Non impararlo a memoria. Usa la struttura per raccontare un episodio vero in meno di un minuto, con una decisione tecnica precisa.",
}


PLAIN_EXPLANATIONS = {
    "Come affrontare un live coding": "Prima di scrivere, ripeti il problema con parole tue e concorda un esempio. In questo modo eviti di risolvere bene la domanda sbagliata e dai all'intervistatore la possibilità di correggere subito un equivoco.",
    "Metodo di debugging sistematico": "Un bug diventa gestibile quando sai riprodurlo. Parti da un caso che fallisce sempre, leggi l'errore fino in fondo e prova una sola ipotesi: così capisci davvero quale modifica lo ha risolto.",
    "Valori, tipi e confronti": "JavaScript può convertire automaticamente un valore durante un confronto. Usare `===` e controllare il tipo rende il risultato più prevedibile, soprattutto quando i dati arrivano da form o API.",
    "Scope, const, let e closure": "Lo scope stabilisce da quali righe una variabile è visibile. Una closure nasce quando una funzione continua ad accedere alle variabili del luogo in cui è stata creata, anche dopo che quella funzione esterna è terminata.",
    "Funzioni e responsabilità": "Una buona funzione riceve pochi dati, svolge un compito riconoscibile e restituisce un risultato chiaro. Se per descriverla servono molti verbi, probabilmente contiene più responsabilità da separare.",
    "Array: map, filter, find e some": "Questi metodi rispondono a domande diverse: `map` trasforma tutti gli elementi, `filter` ne conserva alcuni, `find` cerca il primo e `some` verifica se ne esiste almeno uno. Scegli il metodo partendo dal risultato che ti serve.",
    "Oggetti, destructuring e spread": "Destructuring rende espliciti i campi che stai leggendo; spread aiuta a creare una copia con alcuni campi aggiornati. Ricorda però che la copia è superficiale: gli oggetti annidati restano condivisi se non li copi a loro volta.",
    "Immutabilità e operazioni CRUD": "Invece di modificare l'array esistente, ne produci uno nuovo: spread per aggiungere, `map` per aggiornare e `filter` per eliminare. React può così riconoscere il cambiamento e aggiornare la UI in modo prevedibile.",
    "Reduce, Set e Map": "`reduce` combina molti valori in un solo risultato. `Set` è comodo per eliminare duplicati, mentre `Map` associa chiavi a valori ed è utile quando cerchi spesso un elemento per identificatore.",
    "Moduli ed organizzazione del codice": "Un modulo espone soltanto ciò che gli altri file devono usare. Import ed export ben scelti mostrano le dipendenze reali e impediscono che un singolo file diventi il contenitore di tutta l'applicazione.",
    "Errori e validazione": "Validare significa rifiutare presto un dato che non rispetta il contratto. Un errore utile dice che cosa non va e lascia al livello corretto la scelta tra mostrare un messaggio, riprovare o interrompere l'operazione.",
    "Promise e async/await": "Una Promise rappresenta un risultato futuro: può essere ancora in attesa, completato oppure fallito. `await` sospende quella funzione, non l'intero programma, e rende più leggibile la sequenza delle operazioni asincrone.",
    "HTTP e API REST": "Una API REST espone risorse attraverso URL e usa i metodi HTTP per esprimere l'azione. Lo status code fa parte della risposta: permette al client di distinguere una creazione, un errore di input o una risorsa assente.",
    "Fetch: loading, error e successo": "`fetch` risolve la Promise anche quando il server risponde 404 o 500, quindi devi controllare `response.ok`. La UI deve inoltre distinguere attesa, dati disponibili, risultato vuoto ed errore.",
    "Autenticazione, CORS e segreti": "L'autenticazione stabilisce chi sei; l'autorizzazione stabilisce che cosa puoi fare. CORS è una regola del browser, non una protezione dell'API, e un segreto inserito nel frontend non è più segreto.",
    "HTML semantico e struttura": "Gli elementi semantici descrivono il ruolo del contenuto. Un `button` comunica già a browser e tecnologie assistive che può ricevere focus ed essere attivato: un `div` con un click non offre automaticamente lo stesso comportamento.",
    "Form e accessibilità": "Ogni campo deve avere una label riconoscibile e gli errori devono essere collegati al campo interessato. Prova sempre il form usando soltanto la tastiera: il percorso del focus rivela molti problemi.",
    "Box model, cascade e specificità": "Ogni elemento occupa spazio attraverso contenuto, padding, bordo e margine. Quando due regole competono, la cascade considera origine, importanza, specificità e ordine: aumentare sempre la specificità rende il CSS difficile da mantenere.",
    "Flexbox e Grid": "Flexbox distribuisce elementi lungo un asse ed è ideale per righe e colonne di componenti. Grid controlla contemporaneamente righe e colonne ed è più adatto alla struttura complessiva di una pagina o di una griglia di card.",
    "Responsive design": "Un layout responsive non è una versione desktop rimpicciolita. Parte da misure fluide, lascia che il contenuto occupi lo spazio disponibile e introduce un breakpoint soltanto quando il layout smette di funzionare bene.",
    "Tipi, interface e type": "Un tipo descrive la forma che il codice si aspetta e permette all'editor di segnalare incoerenze prima dell'avvio. Non controlla però automaticamente un JSON ricevuto dalla rete: quel dato richiede validazione a runtime.",
    "Union e narrowing": "Una union dichiara che un valore può assumere forme alternative. Controllando una proprietà discriminante, TypeScript restringe il tipo e ti permette di accedere soltanto ai campi validi per quel caso.",
    "Generics essenziali": "Un generic conserva una relazione tra il tipo ricevuto e quello restituito. È utile quando la stessa logica funziona con dati diversi, ma vuoi evitare che `any` cancelli le informazioni sui tipi.",
    "Null, unknown e confini esterni": "`unknown` ti obbliga a controllare un valore prima di usarlo, mentre `any` disattiva quella protezione. È la scelta corretta per JSON, input utente e altri dati che entrano dall'esterno.",
    "Modello mentale, componenti e JSX": "Un componente è una funzione che descrive la UI a partire da props e state. A parità di input dovrebbe produrre lo stesso JSX, senza modificare dati o avviare operazioni durante il render.",
    "Props e composizione": "Le props portano dati dal genitore al figlio. Per comunicare nella direzione opposta, il genitore passa una callback: il figlio segnala l'evento senza dover conoscere come verrà gestito.",
    "State ed eventi": "Lo state è la memoria locale del componente. Il setter pianifica un nuovo render; quando il nuovo valore dipende dal precedente, la forma funzionale evita di usare una fotografia ormai vecchia dello state.",
    "Liste, key e rendering condizionale": "React usa la `key` per riconoscere lo stesso elemento tra due render. Un identificatore stabile evita che stato e focus si spostino sulla riga sbagliata quando la lista viene riordinata o filtrata.",
    "Form controllati": "In un input controllato, il valore mostrato viene dallo state e `onChange` aggiorna quello state. Hai così un'unica fonte di verità per validazione, invio e messaggi di errore.",
    "Progettare e sollevare lo stato": "Lo state dovrebbe vivere nel componente comune più vicino a tutti quelli che lo usano. Un valore calcolabile da props e state esistenti non va duplicato: puoi ricalcolarlo durante il render.",
    "Effect e sincronizzazione": "`useEffect` serve a sincronizzare React con qualcosa di esterno, per esempio una richiesta, un timer o una subscription. Se l'operazione può continuare dopo un nuovo render, la cleanup deve annullarla o scollegarla.",
    "Caricamento dati e stati remoti": "I dati remoti hanno più stati di una semplice lista: non ancora richiesti, in caricamento, riusciti, vuoti o falliti. Rappresentarli esplicitamente evita spinner eterni e schermate bianche.",
    "Routing e architettura frontend": "Le route organizzano le pagine; le feature raccolgono componenti e logica legati allo stesso problema. L'accesso alle API va separato dalla presentazione, così puoi cambiarlo e provarlo senza riscrivere la UI.",
    "Node, event loop e moduli": "Node gestisce bene molte operazioni di I/O perché non aspetta in modo sincrono file e rete. Un calcolo CPU lungo, invece, occupa il thread principale e ritarda tutte le altre richieste.",
    "Route, middleware e validazione": "La route associa un URL a un handler; il middleware applica controlli o preparazione comuni. La logica di business resta in un servizio, così l'handler si limita a tradurre richiesta e risposta.",
    "Sicurezza web essenziale": "La sicurezza va applicata a più livelli: query parametrizzate, output correttamente escapato, password sottoposte a hash e permessi minimi. La validazione del frontend migliora l'esperienza, ma non protegge il server.",
    "SELECT, filtri e ordinamento": "Una query leggibile seleziona soltanto le colonne utili, filtra con condizioni esplicite e ordina quando l'ordine fa parte del requisito. Senza `ORDER BY`, il database non promette un ordine stabile.",
    "Relazioni e JOIN": "Una chiave esterna collega una riga a un'altra tabella. `INNER JOIN` conserva soltanto le corrispondenze; `LEFT JOIN` conserva tutte le righe della tabella a sinistra, anche quando la relazione manca.",
    "Vincoli, indici e normalizzazione": "I vincoli impediscono che nel database entrino dati incoerenti. Gli indici velocizzano alcune letture ma occupano spazio e rallentano le scritture, quindi vanno scelti osservando le query reali.",
    "Transazioni e concorrenza": "Una transazione raggruppa operazioni che devono riuscire insieme. Se una fallisce, il rollback evita uno stato parziale; tenerla aperta troppo a lungo può però bloccare altri accessi.",
    "Git: working tree, staging e commit": "Il working tree contiene ciò che stai modificando; lo staging seleziona ciò che entrerà nel prossimo commit. Un commit piccolo e coerente racconta una modifica comprensibile e rende più semplice annullarla o revisionarla.",
    "Branch, merge e conflitti": "Un branch separa una linea di lavoro. Un conflitto non è un errore automatico da cancellare: Git ti sta chiedendo quale combinazione delle due modifiche rappresenta il risultato corretto.",
    "Test unitari, integrazione ed E2E": "Un test unitario isola una piccola regola; un test di integrazione verifica la collaborazione tra parti; un E2E percorre il sistema come un utente. Servono livelli diversi perché trovano problemi diversi.",
    "Code review e refactoring": "La review controlla correttezza, chiarezza e rischi, non lo stile personale dell'autore. Il refactoring migliora la struttura senza cambiare il comportamento e richiede test che lo dimostrino.",
    "PHP e ciclo di un plugin WordPress": "Un plugin registra funzioni sugli hook offerti da WordPress. L'azione esegue un comportamento in un momento preciso; il filtro riceve un valore, lo trasforma e deve restituirlo.",
    "Sicurezza WordPress": "Sanitizzare significa pulire un dato in ingresso; fare escaping significa renderlo sicuro nel punto in cui viene mostrato. Un nonce aiuta a verificare l'intenzione della richiesta, ma non sostituisce il controllo dei permessi.",
    "Presentare l'architettura di un'app Electron": "Nel processo main vivono filesystem, database e funzioni privilegiate; il renderer mostra l'interfaccia. Il preload espone un ponte ristretto e l'IPC permette ai due lati di comunicare senza consegnare alla UI accesso completo al sistema.",
    "Presentare una pipeline AI multimodale": "Racconta la pipeline nell'ordine in cui scorrono i dati: input in un client interattivo, trascrizione con Whisper, recupero del contesto e risposta del modello. Per ogni passaggio chiarisci latenza, possibile errore e dato conservato.",
    "Parlare onestamente dell'uso dell'IA": "Puoi dire che l'IA ti ha aiutato a esplorare o produrre una prima versione, ma devi distinguere quel contributo dalle decisioni che hai verificato tu. La responsabilità finale resta tua: devi saper leggere, correggere e spiegare ciò che presenti.",
    "Comunicare decisioni tecniche e risultati": "Un racconto utile parte da una situazione reale, chiarisce la tua responsabilità e descrive una decisione specifica. Termina con il risultato e con ciò che hai imparato, senza trasformarsi in un elenco di tecnologie.",
}


def human_list(items: list[str]) -> str:
    if len(items) <= 1:
        return items[0] if items else ""
    return ", ".join(items[:-1]) + f" e {items[-1]}"


def term_list(items: list[str]) -> str:
    return "; ".join(f"`{item}`" for item in items)


def lesson_markdown(module: str, title: str, summary: str, concepts: str, example: str, pitfalls: str, review_question: str) -> str:
    keywords = [item.strip() for item in concepts.split(";")]
    concept_list = "\n".join(f"- `{item}`" for item in keywords)
    pitfall_items = [item.strip().rstrip(".") for item in pitfalls.split(";") if item.strip()]
    pitfalls_list = "\n".join(f"- {item[0].upper() + item[1:]}" for item in pitfall_items)
    first_terms = ", ".join(keywords[:3])
    if module == "portfolio":
        example_reading = "Usalo come traccia, non come frase da recitare. Sostituisci ogni affermazione generica con un fatto del tuo progetto: una scelta che hai fatto, una verifica che hai eseguito o un limite che hai riconosciuto."
        active_practice = "Adesso copri l'esempio e racconta lo stesso concetto usando un episodio reale. Una risposta imperfetta ma tua è più credibile di una formula elegante imparata a memoria."
        recovery = "Se la risposta suona generica, fermati e aggiungi un dettaglio verificabile: il nome di un componente, un errore incontrato, un'alternativa scartata oppure ciò che oggi cambieresti."
        checklist = """- Riesco a raccontarlo senza leggere la pagina?
- Distinguo chiaramente ciò che ho fatto io da ciò che ha prodotto uno strumento?
- Cito almeno una decisione tecnica e il relativo compromesso?
- So riconoscere un limite senza sminuire tutto il progetto?"""
    else:
        example_reading = MODULE_EXAMPLE_GUIDES[module]
        if title == "Effect e sincronizzazione":
            example_reading = "Segui il ciclo dell'effect: parte quando cambia `subjectId`, crea un controller e avvia il caricamento. Prima del nuovo effect o dello smontaggio, la cleanup chiama `abort()` e impedisce alla richiesta precedente di continuare inutilmente."
        active_practice = "Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite."
        recovery = "Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta."
        checklist = """- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?"""
    return f"""# {title}

## In parole semplici

L'obiettivo di questa lezione è {summary[0].lower() + summary[1:]}

{PLAIN_EXPLANATIONS[title]}

### Perché è utile

{MODULE_PERSPECTIVES[module]}

## Le parole da riconoscere

{concept_list}

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **{first_terms}** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
{example}
```

{example_reading}

{active_practice}

## Dove ci si confonde spesso

{pitfalls_list}

{recovery}

## Controllo rapido

{checklist}

## Domanda di verifica

> {review_question}

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
"""


def code_task(module: str, index: int, title: str):
    if module == "javascript":
        name, prompt, solution, checks = JS_TASKS[index % len(JS_TASKS)]
        tests = [{"name": n, "expression": e, "expected": x} for n, e, x in checks]
        return "javascript", prompt, f"function {name}() {{\n  // TODO\n}}", solution, tests
    if module == "sql":
        prompt, solution, expected = SQL_TASKS[index % len(SQL_TASKS)]
        return "sql", prompt, "-- Scrivi qui la query\nSELECT ...", solution, [{"name":"righe e ordine corretti","mode":"rows","expected":expected}]
    if module == "html_css":
        prompt = f"Costruisci una piccola pagina con cui mostrare **{title}**. Deve contenere `main`, un titolo, un form con label correttamente associata e almeno una regola responsive. Mantieni l'esempio essenziale: deve essere facile spiegare perché hai scelto ogni elemento."
        solution = """<main class="page">\n  <h1>Archivio soggetti</h1>\n  <form>\n    <label for="search">Cerca</label>\n    <input id="search" name="search" type="search" required>\n    <button type="submit">Cerca</button>\n  </form>\n</main>\n<style>\n.page{width:min(100% - 2rem,72rem);margin:auto;display:grid;gap:1rem}\n@media (min-width:48rem){.page{grid-template-columns:1fr 2fr}}\n</style>"""
        tests = [{"name":"main semantico","mode":"tag","value":"main"},{"name":"titolo","mode":"tag","value":"h1"},{"name":"label associata","mode":"attribute","value":"label:for"},{"name":"media query","mode":"contains","value":"@media"}]
        return "html", prompt, "<!-- Scrivi HTML e CSS qui -->", solution, tests
    if module == "typescript":
        prompt = f"Modella in TypeScript un risultato remoto per esercitarti su **{title}**. Definisci un tipo o un'interface, rappresenta almeno due possibili stati e scrivi una funzione che li gestisca senza usare `any`."
        solution = """interface Subject { id: number; name: string }
type LoadResult =
  | { status: 'success'; data: Subject[] }
  | { status: 'error'; message: string };

function describe(result: LoadResult): string {
  if (result.status === 'error') return result.message;
  return `${result.data.length} soggetti`;
}"""
        tests = [{"name":"contratto dichiarato","mode":"regex","value":"(interface|type)\\s+\\w+"},{"name":"stati alternativi","mode":"contains","value":"status"},{"name":"funzione di gestione","mode":"regex","value":"function\\s+\\w+"},{"name":"nessun any","mode":"not_contains","value":"any"}]
        return "typescript", prompt, "// Definisci qui i tipi e la funzione", solution, tests
    if module == "react":
        prompt = f"Crea un componente React piccolo con cui esercitarti su **{title}**. Usa un tipo per gli elementi, conserva la lista nello state, gestisci almeno un evento e usa una `key` stabile. Dopo averlo scritto, preparati a spiegare chi possiede lo stato e che cosa provoca il nuovo render."
        solution = """interface Item { id: number; name: string }\nfunction ItemList({ initialItems }: { initialItems: Item[] }) {\n  const [items, setItems] = useState<Item[]>(initialItems);\n  const remove = (id: number) => setItems(current => current.filter(item => item.id !== id));\n  return <ul>{items.map(item => <li key={item.id}>{item.name}<button onClick={() => remove(item.id)}>Elimina</button></li>)}</ul>;\n}"""
        tests = [{"name":"contratto tipizzato","mode":"regex","value":"(interface|type)\\s+\\w+"},{"name":"state","mode":"contains","value":"usestate"},{"name":"evento","mode":"contains","value":"onclick"},{"name":"key stabile","mode":"regex","value":"key\\s*=\\s*\\{[^}]*\\.id"}]
        return "react", prompt, "// Scrivi qui il componente", solution, tests
    prompt = f"Spiega **{title}** come lo racconteresti a un collega. Parti da un esempio o da un episodio concreto, descrivi la decisione che prenderesti, segnala un rischio e termina spiegando come verificheresti il risultato."
    keys = [word.strip() for word in TOPICS[index][6].split(";")[:3]] if index < len(TOPICS) else ["verifica", "errore"]
    topic_summary = TOPICS[index][5]
    solution = f"{PLAIN_EXPLANATIONS[title]} In un caso concreto renderei espliciti {term_list(keys[:2])}, spiegherei il rischio che voglio evitare e concluderei con una verifica osservabile, non con un'affermazione generica."
    tests = [{"name":f"usa il concetto: {key}","alternatives":[key]} for key in keys[:2]]
    return "short", prompt, "", solution, tests


def build() -> None:
    LESSONS.mkdir(parents=True, exist_ok=True)
    module_lookup = {item[0]: item for item in MODULES}
    module_counts: dict[str, int] = {}
    lessons = []
    exercises = []
    flashcards = []

    for global_index, topic in enumerate(TOPICS):
        module, title, _group, minutes, mandatory, summary, concepts, example, pitfalls, review_question = topic
        module_counts[module] = module_counts.get(module, 0) + 1
        lesson_id = f"{module_lookup[module][1]}-{module_counts[module]:02d}-{slugify(title)[:38]}"
        body_file = f"lessons/{lesson_id}.md"
        (CONTENT / body_file).write_text(lesson_markdown(module, title, summary, concepts, example, pitfalls, review_question), encoding="utf-8")
        lessons.append({
            "id": lesson_id, "module": module, "title": title,
            "minutes": minutes, "difficulty": "base" if mandatory else "approfondimento",
            "mandatory": mandatory, "objectives": [x.strip() for x in concepts.split(";")[:4]],
            "summary": summary, "body_file": body_file,
        })

        # Esercizio di richiamo, specifico per la lezione.
        keywords = [x.strip() for x in concepts.split(";")]
        recall_id = f"ex-{lesson_id}-recall"
        first_pitfall = pitfalls.split(";")[0].strip().rstrip(".")
        recall_solution = (
            f"{PLAIN_EXPLANATIONS[title]} Per usare il vocabolario della lezione, i due riferimenti principali sono {term_list(keywords[:2])}. "
            f"Un errore da evitare è {first_pitfall.lower()}. Completerei la risposta con un esempio concreto e direi come controllerei il risultato."
        )
        exercises.append({
            "id": recall_id, "lesson_id": lesson_id, "title": f"Richiamo: {title}", "kind": "short",
            "difficulty": "breve", "minutes": 8, "xp": 15,
            "prompt": f"Prepara una spiegazione breve su **{title}**, come se dovessi insegnarlo a un'altra persona. Usa {term_list(keywords[:2])}, aggiungi un esempio concreto e indica un errore che eviteresti. Cinque–otto frasi sono sufficienti.",
            "starter": "", "solution": recall_solution,
            "hints": [
                f"Parti dall'idea più semplice: {PLAIN_EXPLANATIONS[title].split('.')[0].lower()}.",
                f"Controlla di aver usato entrambi i termini richiesti: {term_list(keywords[:2])}.",
                "Aggiungi un episodio, un dato o un frammento concreto: evita di chiudere la risposta con la sola definizione.",
            ],
            "tests": [{"name":f"usa il concetto: {keywords[0]}","alternatives":[keywords[0]]},{"name":f"usa il concetto: {keywords[1]}","alternatives":[keywords[1]]}],
            "explanation": "Il controllo automatico cerca i concetti richiesti, ma la verifica importante resta la tua: rileggi la risposta ad alta voce e controlla che contenga una regola, un esempio e un possibile errore.",
        })

        kind, prompt, starter, solution, tests = code_task(module, global_index, title)
        if kind == "short":
            practice_hints = [
                "Scegli prima una situazione concreta: una decisione presa, un errore trovato oppure un limite del progetto.",
                "Dedica una frase alla scelta, una al rischio e una al modo in cui hai verificato il risultato.",
                f"Rileggi ad alta voce e controlla che compaiano {term_list(keywords[:2])} senza sembrare parole inserite a forza.",
            ]
            practice_explanation = "La risposta modello è una traccia, non un testo da imparare. La tua versione è migliore se usa un episodio vero, distingue ciò che hai deciso tu e spiega una verifica concreta."
        else:
            practice_hints = [
                "Prima di scrivere, annota un input concreto e il risultato che vuoi ottenere.",
                "Fai funzionare il caso più semplice. Solo dopo aggiungi controlli e casi limite.",
                f"Se sei bloccato, torna a questi concetti: {term_list(keywords[:3])}. Quale manca nella tua soluzione?",
            ]
            practice_explanation = f"La soluzione usa {term_list(keywords[:3])} senza aggiungere passaggi inutili. Confronta il comportamento, non la formattazione, e verifica soprattutto i casi limite."
        exercises.append({
            "id": f"ex-{lesson_id}-practice", "lesson_id": lesson_id,
            "title": f"Pratica: {title}", "kind": kind,
            "difficulty": "media", "minutes": 18 if kind not in {"short"} else 12, "xp": 30,
            "prompt": prompt, "starter": starter, "solution": solution,
            "hints": practice_hints,
            "tests": tests, "explanation": practice_explanation,
        })

        cards = [
            (f"Qual è l'idea principale di **{title}** e dove entra `{keywords[0]}`?", PLAIN_EXPLANATIONS[title]),
            (review_question, f"Una risposta solida usa {term_list(keywords[:2])}, li collega a un esempio e termina con una verifica o un caso limite."),
            (f"Qual è un errore tipico legato a **{title}**?", "I rischi più comuni sono: " + pitfalls[0].lower() + pitfalls[1:]),
        ]
        for card_index, (question, answer) in enumerate(cards, 1):
            flashcards.append({"id":f"fc-{lesson_id}-{card_index}","module":module,"question":question,"answer":answer})

    labs_spec = [
        ("lab-js-crud", "javascript", "CRUD immutabile di soggetti", 1, 55, "Implementa aggiunta, modifica, eliminazione, filtro e riepilogo su un dataset."),
        ("lab-js-debug", "javascript", "Debugging di funzioni difettose", 1, 45, "Ripara sei bug su tipi, ricerca, mutazioni ed edge case."),
        ("lab-html-dashboard", "html_css", "Dashboard responsive accessibile", 1, 60, "Costruisci una dashboard da zero senza framework CSS."),
        ("lab-fetch", "async_http", "Client API resiliente", 1, 55, "Gestisci loading, success, empty, error, retry e annullamento."),
        ("lab-react-list", "react", "Archivio React con ricerca", 1, 75, "Crea componenti, filtri, empty state ed eliminazione immutabile."),
        ("lab-ts-model", "typescript", "Contratti TypeScript", 2, 45, "Modella dati e stati remoti con union discriminate."),
        ("lab-react-form", "react", "Form controllato con validazione", 2, 75, "Implementa creazione e modifica con errori accessibili."),
        ("lab-react-api", "react", "CRUD React collegato a API", 2, 100, "Integra lista, form, fetch, errori e aggiornamenti ottimistici."),
        ("lab-sql", "sql", "Database gestionale", 2, 60, "Progetta schema e query per soggetti, misure e controlli."),
        ("lab-git", "git_testing", "Workflow Git e conflitto", 2, 40, "Esegui branch, commit piccoli, merge e risoluzione guidata."),
        ("lab-debug-app", "git_testing", "Diagnosi applicazione rotta", 2, 70, "Parti da test falliti e correggi una regressione alla volta."),
        ("lab-final", "portfolio", "Mini gestionale finale", 2, 120, "Simula il test tecnico completo con React, API, validazione e README."),
    ]
    labs = []
    for lab_id, module, title, _group, minutes, description in labs_spec:
        labs.append({
            "id":lab_id,"module":module,"title":title,"minutes":minutes,"difficulty":"laboratorio",
            "description":description,
            "requirements":[
                "Prima di scrivere codice, riassumi il risultato atteso con un esempio normale e un caso limite.",
                "Costruisci prima la versione minima che funziona; aggiungi i miglioramenti uno alla volta.",
                "Esegui i test dopo ogni passaggio e, quando uno fallisce, correggi una sola causa per volta.",
                "Nel README annota i comandi necessari, le decisioni principali e almeno un limite rimasto.",
            ],
            "rubric":["Il comportamento richiesto funziona anche nei casi limite","Il codice si legge facilmente e ogni parte ha una responsabilità chiara","Gli errori vengono gestiti in modo esplicito e utile","I test dimostrano le scelte descritte nel README"],
            "workspace_template":"react" if "react" in lab_id or lab_id == "lab-final" else "plain",
        })

    simulations = [
        {"id":"sim-js-30","title":"Live coding JavaScript — 30 minuti","minutes":30,"brief":"Ricevi una collezione di soggetti. Devi filtrarla, aggiornare un elemento e calcolare un riepilogo senza modificare i dati originali.","checklist":["Ripeti il requisito con parole tue","Scrivi un esempio normale e un caso limite","Dividi la soluzione in funzioni piccole","Prova anche un array vuoto","Spiega il costo della soluzione e un possibile compromesso"]},
        {"id":"sim-react-60","title":"Live coding React — 60 minuti","minutes":60,"brief":"Costruisci una lista ricercabile, un form controllato e un'eliminazione con conferma. Mostra chiaramente anche lo stato vuoto.","checklist":["Definisci la forma dei dati","Decidi quale componente possiede lo state","Gestisci la lista vuota","Usa una key stabile","Prova gli eventi come farebbe un utente"]},
        {"id":"sim-debug-45","title":"Debugging guidato — 45 minuti","minutes":45,"brief":"Hai davanti una piccola applicazione con errori e test falliti. Trova le cause senza riscrivere tutto da capo.","checklist":["Riproduci il problema","Leggi per intero errore e stack trace","Formula un'ipotesi verificabile","Applica la correzione più piccola possibile","Esegui di nuovo tutti i test per evitare regressioni"]},
        {"id":"sim-complete-60","title":"Sfida completa — 60 minuti","minutes":60,"brief":"Completa una sessione che unisce spiegazione tecnica, domande web, analisi di due progetti e riflessione sull'uso consapevole dell'IA.","checklist":["Riassumi il tuo approccio in circa 90 secondi","Racconta due decisioni tecniche concrete","Descrivi un bug che hai realmente affrontato","Riconosci un limite e spiega come lo miglioreresti","Annota due domande da approfondire"]},
    ]

    catalog = {
        "meta":{"name":"DEV//48","version":"1.0","estimated_hours":"12–16","language":"it"},
        "modules":[{"id":m,"order":order,"title":title,"description":description} for m,order,title,description in MODULES],
        "lessons":lessons,"exercises":exercises,"labs":labs,"flashcards":flashcards,"simulations":simulations,
    }
    CONTENT.mkdir(exist_ok=True)
    (CONTENT / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(lessons)} lessons, {len(exercises)} exercises, {len(labs)} labs, {len(flashcards)} flashcards, {len(simulations)} simulations")


if __name__ == "__main__":
    build()
