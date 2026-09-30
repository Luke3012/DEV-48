"""Topic-specific editorial source used by generate_content.py.

Keep Markdown generated: examples, reasoning and review answers live here.
Prerequisites reference stable lesson titles, resolved to existing IDs by build().
"""

from textwrap import dedent


def guide(prerequisites, reasoning, example, reading, practice, answer, source=""):
    return dict(prerequisites=prerequisites,
                reasoning=dedent(reasoning).strip(),
                example=dedent(example).strip(),
                reading=dedent(reading).strip(),
                practice=dedent(practice).strip(),
                answer=dedent(answer).strip(), source=source)


GUIDES = {
    "Come affrontare un live coding": guide(
        [],
        "Affronta il live coding come una sessione di costruzione: prima rendi preciso il problema, poi prova una soluzione. Non serve un interlocutore: anche quando studi da solo, scrivere un esempio di input e output evita di lavorare sul requisito sbagliato. Qui useremo un archivio di soggetti, ripreso in alcuni esercizi e laboratori.",
        "// Richiesta: mostrare solo i soggetti attivi.\n// Input: [{name: 'Anna', active: true}, {name: 'Mario', active: false}]\n// Output atteso: ['Anna']\n// Caso limite: [] deve produrre []\n// Passi: selezionare gli attivi, poi estrarre i nomi.",
        "La parola 'mostrare' non basta: l'output stabilisce se servono oggetti o soltanto nomi. Il caso vuoto chiarisce che non è un errore. Prima di implementare, annota anche se l'input può essere modificato; nel percorso lo conserveremo quando il contratto lo richiede.",
        "Ricevi una richiesta diversa: cercare un soggetto per ID. Scrivi il risultato per un ID presente e uno assente, senza ancora programmare. Decidi se l'assenza deve dare `undefined` oppure un errore, e motivala.",
        "Nei primi due minuti chiarisco il risultato atteso, scrivo input e output per un caso normale e uno limite, poi divido il lavoro in passi verificabili. Per esempio, prima filtro gli attivi e poi estraggo i nomi; verifico anche l'array vuoto."),
    "Metodo di debugging sistematico": guide(
        [],
        "Una correzione utile parte da una differenza riproducibile tra risultato atteso e ottenuto. Registra input, output e messaggio d'errore prima di intervenire. Il debugger e `console.log` servono a controllare un'ipotesi precisa; stamparne molti senza una domanda aumenta il rumore.",
        "function firstName(names) {\n  return names[0].trim();\n}\nconsole.log(firstName([' Anna '])); // 'Anna'\nconsole.log(firstName([])); // TypeError: il primo elemento non esiste",
        "Con la lista vuota `names[0]` è `undefined`; l'errore compare quando chiami `.trim()`. Il sintomo non indica che `trim` sia difettoso: manca la gestione dell'assenza. Se il contratto vuole una stringa vuota, controlla la lunghezza prima di leggere il primo elemento.",
        "Scrivi il caso che fallisce, aggiungi la sola guardia necessaria e riprova entrambi gli input. Conserva il caso vuoto come test di regressione: deve fallire prima della correzione e passare dopo.",
        "Riproduco il bug con una lista vuota, leggo lo stack trace e controllo quale valore riceve il metodo. Formulo l'ipotesi che manchi un elemento, aggiungo una guardia coerente con il contratto e verifico anche il caso normale."),
    "Valori, tipi e confronti": guide(
        [],
        """La stessa schermata può consegnare valori che sembrano uguali ma hanno tipi diversi. Prima di scegliere un confronto, chiediti quale domanda vuoi fare: i valori hanno lo stesso tipo e lo stesso contenuto? Vuoi consentire una conversione? Oppure vuoi sapere se un ramo `if` verrà eseguito?

Considera `value` uguale alla stringa `"0"`. La variabile contiene tre caratteri, non il numero zero. Guardiamo la stessa variabile con tre operazioni: `===` confronta senza conversioni, `==` può convertire, mentre `Boolean(...)` chiede soltanto se il valore è truthy. Sono domande diverse e possono quindi dare risposte diverse.""",
        """const value = "0";

console.log(typeof value);   // "string"
console.log(value === 0);    // false
console.log(value == 0);     // true
console.log(Boolean(value)); // true

if (value) {
  console.log("Il ramo viene eseguito");
}

console.log(Boolean(0));  // false
console.log(Boolean("")); // false
console.log(typeof null); // "object": particolarità storica""",
        """La prima riga conserva l'input come stringa. Perciò `value === 0` è `false`: una stringa e un numero non diventano uguali durante il confronto stretto. Con `value == 0` JavaScript converte la stringa numerica e confronta due zeri; il risultato è `true`. Questo mostra perché `==` può sorprendere, non perché sia la scelta da preferire.

`Boolean(value)` risponde a una terza domanda. Una stringa non vuota è truthy anche quando il suo contenuto è `"0"`; il numero `0` e la stringa vuota sono falsy. Truthy non significa “uguale a `true`” e falsy non significa “uguale a zero”.

Un campo HTML arriva come stringa. Se il programma deve usarlo come numero, controlla prima che non sia vuoto, convertilo esplicitamente e valida il risultato. Altrimenti un controllo come `if (!value)` confonde l'assenza con il numero zero, mentre un confronto permissivo può nascondere la conversione. `null` indica spesso un'assenza scelta dal programma; `undefined` può indicare una proprietà che non esiste. `typeof null` è un'eccezione storica, quindi non serve a distinguere i due casi.""",
        "Prevedi prima l'esito di `'' === false`, `0 === false` e `null === undefined`. Poi eseguili. In `classifyValue`, prova anche `false`, zero e la stringa `'0'`: non devono essere classificati come mancanti.",
        "`==` può convertire i valori prima del confronto; `===` non lo fa. Per esempio `'0' == 0` è vero, mentre `'0' === 0` è falso. Se accetto un numero da un input HTML, lo converto e valido esplicitamente prima del confronto.",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness"),
    "Funzioni e responsabilità": guide(
        ["Valori, tipi e confronti"],
        """Una funzione trasforma input in output. Quando la chiami, gli argomenti diventano parametri; il corpo esegue i passaggi e `return` consegna un risultato al chiamante. Tenere visibili questi tre momenti rende più facile capire chi possiede i dati e dove aspettarsi un effetto.

Prendiamo `calculateTotal(12, 2)`: i due numeri sono gli input, la moltiplicazione è l'elaborazione e il valore restituito è `24`. Una funzione diversa può stampare quel risultato. Calcolare un valore e scrivere nella console sono responsabilità diverse.""",
        """function calculateTotal(unitPrice, quantity) {
  return unitPrice * quantity;
}

function printTotal(total) {
  console.log("Totale: " + total + " euro");
}

const total = calculateTotal(12, 2);
console.log(total); // 24: valore restituito
printTotal(total);  // Totale: 24 euro: effetto sulla console""",
        """Nella chiamata `calculateTotal(12, 2)`, `unitPrice` riceve 12 e `quantity` riceve 2. Il corpo calcola `12 * 2`; `return` passa 24 al punto in cui la funzione è stata chiamata, quindi `total` diventa 24. La funzione non ha modificato i due input né scritto altrove.

`printTotal` usa invece `console.log`, che produce un effetto osservabile fuori dal valore restituito. Non ha un `return`, quindi il suo risultato è `undefined`: stampare “24 euro” non restituisce la stringa al chiamante. Anche una funzione con un side effect può essere utile; basta sapere quando lo esegue. Un handler React può chiamare una funzione di salvataggio in risposta a un click, mentre il calcolo della UI durante il render dovrebbe limitarsi a produrre JSX.

Con un arrow function, `value => value.trim()` restituisce implicitamente l'espressione. Se apri un blocco, `value => { value.trim(); }`, occorre scrivere `return value.trim()`: senza, il chiamante riceve `undefined`. Una callback è semplicemente una funzione passata a un'altra funzione, che decide quando invocarla.""",
        "Scrivi `fullName` partendo dal contratto dell'esercizio. Poi sostituisci la callback di `apply` con una che rende il testo maiuscolo. Spiega la differenza tra `transform` e `transform(value)`.",
        "Restituire un valore permette al chiamante di usarlo; un side effect modifica qualcosa di esterno, come una variabile condivisa o il DOM. Una funzione che formatta un nome può restituire la stringa senza modificare l'oggetto originale."),
    "Scope, const, let e closure": guide(
        ["Funzioni e responsabilità"],
        """Lo scope risponde a una domanda concreta: da quale parte del programma posso leggere o cambiare questo nome? `let` e `const` dichiarati in una funzione appartengono a quella chiamata. Se una funzione interna usa un nome dello scope esterno, JavaScript risolve il nome risalendo gli ambienti lessicali.

Si parte da una variabile condivisa visibile a `increment`. Poi spostiamo `count` dentro `createCounter`: ogni chiamata esterna ottiene una variabile locale diversa. Se la funzione esterna restituisce una funzione che usa quella variabile, la funzione restituita conserva l'accesso al suo ambiente anche dopo che `createCounter` è terminata. Questo accesso mantenuto è la closure.""",
        """let count = 0;

function increment() {
  count += 1;
  return count;
}

console.log(increment()); // 1: l'ambiente condiviso viene aggiornato

function createCounter() {
  let count = 0;
  return function incrementLocal() {
    count += 1;
    return count;
  };
}

const first = createCounter();
const second = createCounter();
console.log(first(), first(), second()); // 1, 2, 1

const user = { name: "Anna" };
user.name = "Marco"; // consentito: il binding user non cambia
// user = {};        // TypeError: riassegnazione di const""",
        """La prima versione usa il `count` esterno: ogni chiamata a `increment` modifica la stessa variabile. Nel contatore vero, invece, `count` nasce dentro `createCounter`; al ritorno, `incrementLocal` conserva un riferimento a quell'ambiente:

~~~text
createCounter()
│
├─ ambiente della prima chiamata: count = 0
│    └─ first continua a leggere e aggiornare questo count
│
└─ ambiente della seconda chiamata: count = 0
     └─ second continua a leggere e aggiornare questo count
~~~

Quando esegui `first()` due volte, il primo ambiente passa da 0 a 1 e poi a 2. `second()` consulta un altro ambiente e parte ancora da 0, quindi restituisce 1. La closure non congela una copia: conserva l'accesso alla variabile, che può cambiare.

`const` protegge il binding: non permette di ricollegare `user` a un altro oggetto. Non rende immutabile l'oggetto raggiungibile da `user`; perciò `user.name = "Marco"` è consentito. Le copie necessarie quando si aggiornano oggetti annidati sono il passo successivo in Oggetti, destructuring e spread.

Questo è un comportamento JavaScript generale. React lo riusa: ogni render crea nuove funzioni e handler che accedono ai valori di quello specifico render. Per capire perché un timer può leggere un valore precedente, prima serve distinguere “la closure conserva l'accesso” da “la variabile viene sostituita in tutti gli ambienti”.""",
        "Implementa il contatore e verifica che due istanze siano indipendenti. Poi prevedi cosa accade se sposti `let value = 0` dentro la funzione restituita: ogni chiamata riparte da zero.",
        "Una closure è una funzione con accesso al suo ambiente lessicale. In un contatore conserva la variabile privata tra chiamate. Due chiamate a `createCounter` producono due ambienti indipendenti; una closure non significa necessariamente una copia congelata dei valori.",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures"),
    "Array: map, filter, find e some": guide(
        ["Funzioni e responsabilità"],
        """Prima di scegliere un metodo, decidi che forma deve avere la risposta. Vuoi un elemento per ciascun input, soltanto gli elementi che passano una condizione, il primo corrispondente o una risposta sì/no? Questa domanda porta al metodo giusto più facilmente della memorizzazione di quattro nomi.

Usiamo sempre le stesse tre persone. `filter` visita ogni oggetto e conserva quelli per cui la callback restituisce `true`; `map` trasforma ciascun oggetto rimasto in un nome. Leggiamo prima i due passaggi da soli, poi li componiamo.""",
        """const users = [
  { id: 1, name: "Anna", active: true },
  { id: 2, name: "Luca", active: false },
  { id: 3, name: "Sara", active: true }
];

const activeUsers = users.filter(user => user.active);
console.log(activeUsers.map(user => user.name)); // ["Anna", "Sara"]

const activeNames = users
  .filter(user => user.active)
  .map(user => user.name);
console.log(activeNames); // ["Anna", "Sara"]

console.log(users.find(user => user.id === 2)); // l'oggetto Luca
console.log(users.find(user => user.id === 9)); // undefined
console.log(users.some(user => user.active));   // true
console.log(users.every(user => user.active));  // false""",
        """Seguiamo prima `filter`. La callback viene chiamata una volta per ogni utente: Anna produce `true`, Luca `false`, Sara `true`. Entra l'array con tre oggetti ed esce un nuovo array con Anna e Sara; non abbiamo cambiato `users`.

Ora `map` riceve quei due oggetti e restituisce la proprietà `name` per ciascuno: esce un array di due stringhe. Il numero di elementi è ancora due, ma la forma dei valori è cambiata. Per questo la pipeline si legge da sinistra a destra: `users` → utenti attivi → nomi degli utenti attivi.

`find` dà un solo oggetto, il primo che soddisfa la condizione, oppure `undefined` se non ne trova uno. `some` e `every` restituiscono invece un booleano: il primo chiede se almeno uno passa, il secondo se li superano tutti. Prima di leggere una proprietà del risultato di `find`, gestisci l'eventuale `undefined`.

`filter` crea un array nuovo, ma gli oggetti selezionati sono gli stessi riferimenti presenti nell'array originale. Mutare `user.name` dentro una callback può quindi modificare anche l'input. “Nuovo array” non significa “copia profonda”.""",
        "Implementa il filtro senza modificare l'input. Aggiungi un caso in cui nessuno è attivo e uno in cui lo sono tutti. Correggi poi `users.map(user => { user.name; })`: spiega perché produce elementi `undefined`.",
        "Uso `find` quando serve un singolo elemento oppure `undefined` se manca. Uso `filter` per ottenere tutte le corrispondenze, anche zero. Per un ID univoco `find` esprime meglio il requisito; controllo l'assenza prima di leggere il nome."),
    "Oggetti, destructuring e spread": guide(
        ["Array: map, filter, find e some"],
        """Gli oggetti contengono proprietà; il valore di una proprietà può essere a sua volta un riferimento a un altro oggetto. Perciò due oggetti distinti possono ancora condividere una parte della loro struttura.

`{ ...user }` copia le proprietà del primo livello. Se `user.address` punta a un altro oggetto, la copia riceve lo stesso riferimento. Per aggiornare la città senza toccare l'originale, devi ricreare sia l'oggetto esterno sia `address`; gli altri campi dell'indirizzo restano copiati.""",
        """const user = {
  name: "Anna",
  address: {
    city: "Napoli",
    postalCode: "80100"
  }
};

const shallow = { ...user };
console.log(shallow !== user); // true: oggetto esterno nuovo
console.log(shallow.address === user.address); // true: indirizzo condiviso

const updated = {
  ...user,
  address: { ...user.address, city: "Milano" }
};

console.log(user.address.city); // "Napoli"
console.log(updated.address.city); // "Milano"
console.log(updated.address.postalCode); // "80100"

const { name, address } = updated;
console.log(name, address.city); // "Anna", "Milano"
console.log(updated.address?.city ?? "N/D"); // città mostrata: Milano""",
        """Dopo il primo spread, `shallow` e `user` sono due oggetti esterni, ma la proprietà `address` conduce allo stesso oggetto:

~~~text
user   ──────→ { name, address } ──────→ { city: "Napoli", postalCode: "80100" }
                                          ↑
shallow ─────→ { name, address } ─────────┘
~~~

Quindi una scrittura come `shallow.address.city = "Milano"` cambierebbe anche `user.address.city`. Non basta copiare il contenitore che sta sopra: si deve copiare ogni oggetto lungo il percorso modificato. In `updated`, il secondo spread crea un nuovo `address`; `postalCode` viene conservato, mentre `city` riceve il nuovo valore.

Il destructuring estrae proprietà dai dati già ottenuti: `const { name, address } = updated` non fa una copia profonda. L'optional chaining `?.` interrompe la lettura se il valore a sinistra è `null` o `undefined`; `??` applica il default soltanto in quei due casi, quindi conserva valori come `0` e stringa vuota.

La stessa regola servirà in React: lo state può contenere più livelli di oggetti e array, e un aggiornamento deve produrre riferimenti nuovi per i livelli modificati senza alterare i dati precedenti.""",
        "Implementa `moveUser` e controlla sia il risultato sia la città originale. Aggiungi una proprietà a `profile`: deve sopravvivere all'aggiornamento. Confronta i riferimenti esterni e annidati.",
        "`{...obj}` copia le proprietà di primo livello; un oggetto annidato rimane condiviso. Per cambiare `profile.city` senza mutare l'originale creo anche un nuovo `profile` e conservo le altre proprietà tramite spread."),
    "Immutabilità e operazioni CRUD": guide(
        ["Oggetti, destructuring e spread"],
        """L'immutabilità qui è un modo per tenere distinguibili lo stato precedente e quello successivo. Non significa vietare ogni mutazione locale: significa che una trasformazione dei dati applicativi produce una nuova collezione e non altera quella che ha ricevuto.

Per creare una riga, aggiungila a un nuovo array; per rimuoverla, filtra gli ID che restano; per cambiare una riga, usa `map` e copia l'oggetto corrispondente. Se non cambi un oggetto, puoi conservarne il riferimento. Questo schema prepara direttamente agli aggiornamenti dello state React.""",
        """const items = [
  { id: 1, name: "Anna", active: false },
  { id: 2, name: "Mario", active: true }
];

const added = [...items, { id: 3, name: "Sara", active: true }];
const changed = items.map(item =>
  item.id === 1 ? { ...item, active: true } : item
);
const removed = items.filter(item => item.id !== 2);

console.log(added.length, items.length); // 3, 2
console.log(changed[0].active, items[0].active); // true, false
console.log(changed !== items); // true: array nuovo
console.log(changed[1] === items[1]); // true: riga non modificata""",
        """L'inserimento produce `added`, senza allungare `items`. Per l'aggiornamento, `map` restituisce l'oggetto copiato per Anna e riusa quello di Mario. Il confronto mostra due livelli distinti: il contenitore è nuovo (`changed !== items`), mentre la riga non toccata conserva la sua identità.

Ora confronta questo con il bug React:

~~~jsx
items.push(newItem);
setItems(items);
~~~

push ha già cambiato l'array esistente e poi setItems riceve lo stesso riferimento. React confronta il valore precedente e quello richiesto; se sono lo stesso array, può saltare il render. Anche copiando l'array dopo aver mutato un oggetto, l'oggetto precedente è già stato alterato: la copia del solo contenitore non annulla quella scrittura.

Una trasformazione immutabile mantiene un “prima” leggibile e consegna un riferimento nuovo a React, per esempio `setItems(current => [...current, newItem])`. Per un elemento annidato copia l'array, la riga modificata e il percorso degli oggetti annidati che cambi. `sort()` invece modifica l'array su cui lavora: ordina una copia o usa `toSorted()` se l'ambiente del progetto lo supporta.""",
        "Scrivi un aggiornamento per ID assente: il contenuto deve rimanere equivalente e nessun oggetto deve essere mutato. Riprendi poi la stessa regola nel laboratorio React: il nuovo contesto allena il collegamento tra trasformazione dei dati e rendering.",
        "Uso `map` per selezionare l'elemento da cambiare e spread per crearne una copia aggiornata. Gli altri elementi restano invariati. Verifico il nuovo contenuto e che l'input non sia stato mutato."),
    "Reduce, Set e Map": guide(
        ["Array: map, filter, find e some"],
        """Questo è un approfondimento: per iniziare React bastano le trasformazioni con `map` e `filter`. `reduce` è utile quando molti elementi devono diventare un risultato solo, ma è più facile leggerlo dopo aver visto il ciclo equivalente.

Il ciclo mantiene due informazioni: il totale accumulato finora e il valore corrente. Con `[10, 20, 5]`, partiamo da `total = 0`; leggendo 10 otteniamo 10, poi 30, poi 35. In `reduce`, il primo parametro della callback è quell'accumulatore e il secondo è l'elemento letto.""",
        """const values = [10, 20, 5];
const total = values.reduce((accumulator, currentValue) => {
  return accumulator + currentValue;
}, 0);
console.log(total); // 35

const regions = [...new Set(["Nord", "Centro", "Nord"])];
console.log(regions); // ["Nord", "Centro"]

const byId = new Map([[1, { name: "Anna" }]]);
console.log(byId.get(1).name, byId.has(9)); // "Anna", false""",
        """Il ciclo esplicito fa lo stesso lavoro prima che lo comprimiamo in reduce:

~~~javascript
let total = 0;
for (const value of [10, 20, 5]) {
  total += value;
}
~~~

Seguiamo le iterazioni:

~~~text
inizio: total = 0
leggo 10: total = 0 + 10 = 10
leggo 20: total = 10 + 20 = 30
leggo 5:  total = 30 + 5 = 35
~~~

In `reduce`, `accumulator` è il `total` conservato dal ciclo e `currentValue` è il valore letto in quel giro. Il valore iniziale `0` definisce anche il risultato per un array vuoto, la cui somma è zero. Usa un ciclo quando rende i passaggi più chiari: `reduce` non è automaticamente una forma migliore.

`Set` risponde a una domanda diversa: quali valori distinti sono presenti? Conserva l'ordine della prima occorrenza. `Map` associa chiavi a valori; `array.map` invece costruisce un array trasformato. Una `Map` è utile se la ricerca per chiave ricorre, ma non serve costruirla per consultare una sola volta una lista minuscola.""",
        "Calcola la somma dei controlli degli attivi, poi riscrivila con un ciclo. Scegli la versione che riesci a spiegare meglio; entrambe devono restituire zero sull'array vuoto.",
        "Preferisco Map quando devo recuperare ripetutamente elementi per chiave e mantenere un indice. Per una sola ricerca su pochi elementi, `find` può essere più semplice. Map e il metodo array.map risolvono problemi diversi."),
    "Moduli ed organizzazione del codice": guide(
        ["Funzioni e responsabilità"],
        "Import ed export sono prerequisiti dei file React del laboratorio. Un export nominato espone un nome preciso; un export default espone un valore principale che il chiamante può rinominare. I percorsi relativi partono dal file che importa. Nei moduli browser serve uno script di tipo module; Vite configura il caricamento per il progetto React.",
        "// subjects.mjs\nexport function activeNames(items) {\n  return items.filter(item => item.active).map(item => item.name);\n}\nexport default function count(items) { return items.length; }\n\n// app.mjs (file separato nella stessa cartella)\nimport count, { activeNames } from './subjects.mjs';\nconsole.log(count([]), activeNames([])); // 0, []",
        "Il nome tra graffe deve corrispondere all'export nominato, salvo un alias con `as`. `count` è il nome locale scelto per il default. Crea davvero due file: concatenare entrambi i frammenti nello stesso editor non verifica la risoluzione del modulo. Con Node esegui `node app.mjs`; nel browser usa un server locale e `<script type=\"module\">`.",
        "Sposta `activeNames` in un modulo, importalo e prova un input vuoto. Rinomina poi solo l'import default. Se compare 'export not found', confronta il nome importato e quello esportato prima di modificare la funzione.",
        "Un export nominato si importa con graffe e con il nome esposto, eventualmente usando `as`. Un default si importa senza graffe scegliendo il nome locale. Un modulo può avere molti export nominati ma un solo default.",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules"),
    "Errori e validazione": guide(
        ["Valori, tipi e confronti", "Funzioni e responsabilità"],
        "La conversione non basta a rendere valido un input: `Number('')` è zero e `Number('abc')` è NaN. Decidi prima il contratto. L'esempio accetta numeri e stringhe numeriche non vuote, rifiuta booleani e assenze, poi controlla che il risultato sia finito e non negativo. La UI potrà trasformare un errore previsto in un messaggio utile.",
        "function parseAge(value) {\n  if ((typeof value !== 'number' && typeof value !== 'string') ||\n      (typeof value === 'string' && value.trim() === '')) {\n    throw new Error('Età mancante o non numerica');\n  }\n  const age = Number(value);\n  if (!Number.isFinite(age) || age < 0) throw new Error('Età non valida');\n  return age;\n}\ntry { console.log(parseAge('abc')); }\ncatch (error) { console.log(error.message); }",
        "`throw` interrompe il percorso normale e risale fino a un catch. Il catch non deve fingere un successo: un errore di parsing non è l'età zero. Quando il contratto permette un risultato assente può essere adatto `null`; quando l'input viola il contratto, un errore distingue il fallimento da un risultato valido.",
        "Implementa la validazione per non negativi e prova zero, stringa numerica, negativo, Infinity, testo e stringa vuota. Scrivi quale caso distingue una funzione corretta da una che restituisce sempre zero.",
        "Lancio un errore quando il dato viola il contratto e il chiamante deve gestire il fallimento. Restituisco null se l'assenza è un risultato previsto. Un'età negativa è invalida; una ricerca senza corrispondenza può invece restituire null."),
    "Promise e async/await": guide(
        ["Funzioni e responsabilità", "Errori e validazione"],
        """Una `Promise` non è il dato futuro: è un oggetto che rappresenta un'operazione e il suo esito. Durante l'attesa è `pending`; poi diventa `fulfilled` con un valore oppure `rejected` con un errore. Una Promise completata non torna `pending`.

Prima puoi riceverla in una variabile e collegare una callback; il valore non si legge come se fosse già un array. `async` e `await` rendono più lineare il passo successivo: `async` fa restituire una Promise alla funzione, e `await` sospende quel flusso asincrono finché la Promise si assesta. Nel frattempo il resto del programma può continuare.""",
        """async function getData() {
  return ["Anna"];
}

async function load() {
  const data = await getData();
  return data.length;
}

load().then(count => console.log(count)); // 1
console.log("richiesta avviata"); // appare prima di 1""",
        """Quando chiami `getData`, ottieni una Promise, non direttamente l'array. La funzione `async` avvolge il valore restituito in una Promise. `load` si ferma alla sua `await`: quando `getData` si completa, `data` riceve l'array e la funzione restituisce 1. Anche `load` è `async`, quindi il suo chiamante riceve un'altra Promise e deve attenderla oppure usare `then`/`catch`.

Per visualizzare che cosa succede intorno alle Promise, seguiamo questo esempio:

~~~javascript
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
~~~

Il codice sincrono stampa A, pianifica il timer e registra il lavoro della Promise, poi stampa D. Solo quando questo codice ha finito, JavaScript esegue la callback Promise accodata e stampa C; in seguito il timer stampa B. L'ordine è `A, D, C, B`. `await` non blocca il thread fino alla risposta: sospende la funzione che lo contiene, e il suo seguito riprende quando il risultato è pronto.

Asincronia significa poter proseguire mentre un'operazione attende; concorrenza significa che più operazioni sono in corso nello stesso intervallo; parallelismo significa eseguire lavoro nello stesso istante su più risorse di calcolo. Avviare due richieste indipendenti prima di aspettarle, per esempio con `Promise.all`, permette concorrenza; `async` non crea automaticamente un thread né rende parallelo un calcolo CPU.""",
        "Sostituisci getData con una funzione che lancia Error. Prevedi quale catch lo riceve e aggiungi la gestione al chiamante. Non restituire un array vuoto per nascondere l'errore: vuoto e fallimento sono esiti diversi.",
        "Una funzione async restituisce sempre una Promise, anche quando il return contiene un numero. `await` ne ottiene il valore risolto oppure propaga il rifiuto come errore. Per esempio load può risolvere a 1 o rifiutare con un messaggio.",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises"),
    "Fetch: loading, error e successo": guide(
        ["Promise e async/await", "HTTP e API REST"],
        """Una richiesta attraversa passaggi distinti: contatto con il server, risposta HTTP, lettura del corpo e controllo della forma dei dati. Se mostri tutto come “successo o errore” senza sapere a quale passaggio sei arrivato, è difficile capire il guasto.

Costruiamo quindi la funzione a piccoli passi. `fetch` restituisce una `Promise<Response>`, non il JSON. Prima controlliamo `response.ok` perché un `404` è comunque una risposta HTTP; dopo aver accettato la risposta leggiamo il corpo con `response.json()`. Questa lettura è a sua volta asincrona e può fallire se il corpo non è JSON valido. Infine controlliamo il contratto minimo che l'app si aspetta.""",
        """async function readSubjects(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("HTTP " + response.status);
  }

  const data = await response.json();
  if (!Array.isArray(data)) {
    throw new Error("La risposta non è una lista");
  }

  return data;
}""",
        """La prima `await` aspetta la risposta del trasporto. Un errore di rete, un URL irraggiungibile o una richiesta annullata rifiutano la Promise; un `404` invece arriva come `Response` e richiede il controllo esplicito di `ok`. Quando `ok` è `false`, lanciamo l'errore prima di leggere il corpo.

Solo dopo passiamo alla seconda `await`. `response.json()` può rifiutare durante il parsing: ricevere byte dal server non garantisce che siano JSON leggibile. Se il parse riesce, `data` è ancora un valore esterno non fidato. `Array.isArray` controlla il contenitore, ma non dimostra che ogni elemento abbia `id` e `name` validi; per quel contratto serve la stessa validazione runtime introdotta ai confini dei dati esterni.

La funzione trasforma il trasporto in due esiti per il chiamante: una lista valida, anche vuota, oppure un errore che può essere gestito più in alto. La UI può rappresentare una richiesta in caricamento, un errore recuperabile, un successo vuoto o una lista piena. Una lista vuota non dice se la richiesta sia partita né se sia fallita, quindi questi stati vanno tenuti distinti.

Qui non aggiungiamo ancora `AbortController`. Prima rendiamo chiari risposta, status, parsing ed errore; la lezione sul caricamento remoto aggiungerà cleanup e richieste fuori ordine.""",
        "Prova la funzione con risposte controllate: 200 con [], 404, JSON non valido e un oggetto al posto dell'array. Annota quale caso è successo vuoto e quali sono errori. Nel lab la rete sarà sostituita da un trasporto riproducibile.",
        "Controllo response.ok perché fetch risolve anche per status HTTP di errore. Se è falso lancio un errore prima di consumare i dati; una lista [] con status 200 è invece un successo vuoto. Gestisco separatamente anche rete e JSON non valido.",
        "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch"),
    "Modello mentale, componenti e JSX": guide(
        ["Funzioni e responsabilità", "Moduli ed organizzazione del codice", "HTML semantico e struttura"],
        """Una schermata React parte da dati, non da modifiche manuali al DOM. Il componente legge props e state e restituisce JSX: una descrizione della UI che React può calcolare di nuovo quando quegli input cambiano.

Pensala in due casi. Se ricevo il nome Anna, la funzione produce una descrizione con “Ciao Anna”; se il nome cambia in Luca, React richiama la funzione e ottiene un nuovo JSX. JSX non è una stringa HTML: le graffe inseriscono un'espressione JavaScript dentro la descrizione.""",
        """function Greeting({ name }) {
  return <p>Ciao {name}</p>;
}

function App() {
  const name = "Anna";
  return <Greeting name={name} />;
}""",
        """In `<p>Ciao {name}</p>`, `Ciao` è testo letterale e `name` è un'espressione: React inserisce il valore della variabile. In `<p>name</p>`, invece, vedresti proprio le lettere “name”. Le graffe accettano espressioni che producono un valore, come `name` o `active ? "Attivo" : "Inattivo"`; un `if` è un'istruzione e può stare prima del `return`.

Quando `App` restituisce `<Greeting name={name} />`, passa una prop al componente figlio. `App` e `Greeting` sono normali funzioni JavaScript che descrivono parti dell'albero UI; il nome con iniziale maiuscola distingue un componente da un elemento nativo. JSX viene trasformato dagli strumenti del progetto, quindi il browser non lo interpreta da solo come un file HTML.

Il ciclo essenziale è:

~~~text
props + state
     ↓
React richiama il componente
     ↓
il componente restituisce JSX
     ↓
render: React calcola che cosa mostrare
     ↓
commit: React applica al DOM le differenze necessarie
     ↓
il browser dipinge la schermata
~~~

Render e commit sono passaggi distinti. React può richiamare il componente senza modificare il DOM se il JSX risultante non richiede cambiamenti. Per questo il render deve essere una funzione pura: con gli stessi input produce la stessa descrizione, senza modificare oggetti esterni, avviare richieste o registrare handler nel browser. Gli effetti di un click appartengono a un handler; la sincronizzazione con un sistema esterno verrà trattata più avanti.""",
        "Scrivi un badge che mostri anche 'Inattivo'. Passagli false e true dal genitore senza creare stato. Nel laboratorio verifica il testo nel DOM; il controllo breve verifica soltanto la struttura del codice.",
        "Il render deve essere puro perché React può richiamarlo più volte e deve ottenere la stessa UI con gli stessi input. Una richiesta o una mutazione durante render può duplicarsi o cambiare dati condivisi. Un componente legge le props e restituisce JSX senza modificarle.",
        "https://react.dev/learn/render-and-commit"),
    "Props e composizione": guide(
        ["Modello mentale, componenti e JSX", "Funzioni e responsabilità"],
        """Pensa a una prop come all'argomento con cui il genitore configura una funzione componente. Partiamo da `Greeting(name)`, poi la chiamiamo da `App`. Il dato viaggia in una direzione precisa:

~~~text
App
 │
 └─ name="Anna"
        ↓
    Greeting
~~~

La risposta a un'interazione segue il percorso opposto attraverso una funzione. Il genitore passa una callback; il figlio la invoca quando accade l'evento. Il figlio non decide come il genitore aggiornerà i propri dati.""",
        """function Greeting({ name }) {
  return <p>Ciao {name}</p>;
}

function SaveButton({ onSave }) {
  return <button type="button" onClick={onSave}>Salva</button>;
}

function Panel({ children }) {
  return <section>{children}</section>;
}

export default function App() {
  function handleSave() {
    console.log("Richiesta di salvataggio");
  }

  return <>
    <Greeting name="Anna" />
    <Panel><p>Dettagli del soggetto</p></Panel>
    <SaveButton onSave={handleSave} />
  </>;
}""",
        """`App` passa `name` a `Greeting`; il figlio lo riceve come dato di sola lettura. `Panel` mostra un'altra forma di composizione: ciò che metti tra i suoi tag diventa la prop `children`, quindi il contenitore non deve conoscere in anticipo il contenuto che ospiterà.

`App` passa anche `handleSave` a `SaveButton`. L'handler lo conserva in `onClick` e lo chiama solo al click: l'evento risale al genitore attraverso la callback. Scrivere `onClick={handleSave()}` la eseguirebbe subito durante il render e passerebbe a React il risultato della chiamata, spesso `undefined`. Se il figlio deve segnalare quale riga è stata scelta, può chiamare `onSelect(item.id)`; il genitore resta proprietario della decisione e dello state.""",
        "Sostituisci il contenuto con una lista mantenendo Card invariata. Poi passa una callback che registra un contatore di chiamate: la costruzione della UI non deve chiamarla; un click deve chiamarla una volta.",
        "Il genitore passa una callback nelle props. Il figlio la chiama nell'handler dell'evento, eventualmente con l'ID interessato. Il genitore conserva il controllo sullo stato. Con onClick passo una funzione, evitando di chiamarla durante render.",
        "https://react.dev/learn/passing-props-to-a-component"),
    "State ed eventi": guide(
        ["Props e composizione", "Scope, const, let e closure"],
        """Una variabile locale normale verrebbe ricreata ogni volta che React richiama il componente. `useState` conserva invece il valore tra render e lo consegna come snapshot alla chiamata corrente.

Al primo render, `count` vale 0. Un click avvia l'handler creato da quel render; se l'handler chiama `setCount(1)`, chiede a React un aggiornamento. La variabile `count` dentro l'handler in corso resta 0. React poi richiama il componente e il secondo render riceve `count = 1`.""",
        """import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  function addThree() {
    setCount(current => current + 1);
    setCount(current => current + 1);
    setCount(current => current + 1);
    console.log(count);
  }

  return <button onClick={addThree}>Conteggio: {count}</button>;
}""",
        """Il primo click usa un handler nato nel render #1:

~~~text
render #1: count = 0
    │
    └─ click → handler del render #1
                 legge count = 0
                 chiama setCount(1)
                 legge ancora count = 0
                           ↓
                    React pianifica un render
                           ↓
render #2: count = 1
~~~

Il setter non è un'assegnazione immediata alla variabile locale. La UI passa al valore nuovo nel render successivo; `console.log` nello stesso handler stampa ancora 0. Un timeout creato da quel handler è una closure JavaScript e conserva lo snapshot del render #1 anche se nel frattempo la UI è già al render #2.

Ora chiediamo tre incrementi. Tre chiamate `setCount(count + 1)` leggono tutte lo stesso `count` dello snapshot; ognuna chiede quindi il valore 1 e il contatore aumenta una volta. Con `setCount(current => current + 1)`, React accoda invece trasformazioni: la prima riceve 0 e produce 1, la seconda riceve 1 e produce 2, la terza riceve 2 e produce 3. Usa la forma funzionale quando il calcolo dipende dal valore precedente. Non aggiorna retroattivamente le closure già create: per quello ogni nuovo render crea nuovi handler.""",
        "Prevedi testo e console per due click consecutivi, poi verifica nel progetto React. Aggiungi un decremento che non scenda sotto zero. Chiama gli hook al livello superiore del componente, nello stesso ordine, senza inserirli in if o handler.",
        "Uso la forma funzionale quando il prossimo stato dipende dal precedente, soprattutto per più aggiornamenti accodati. Tre updater current => current + 1 aumentano di tre; tre setCount(count + 1) usano lo stesso snapshot e aumentano di uno.",
        "https://react.dev/learn/state-as-a-snapshot"),
    "Liste, key e rendering condizionale": guide(
        ["State ed eventi", "Array: map, filter, find e some"],
        """Quando una lista cambia, React deve capire quali righe sono rimaste, quali sono nuove e quali sono state rimosse. Il posto nell'array non basta a descrivere l'identità di una persona. Per esempio:

~~~text
prima:  id 10 → Anna     id 20 → Luca     id 30 → Sara
dopo:   id 10 → Anna     id 15 → Marco    id 20 → Luca    id 30 → Sara
~~~

L'ID 15 è nuovo; Luca è sempre la persona con ID 20, anche se ora occupa un'altra posizione. La key comunica questa identità tra un render e il successivo e aiuta React a conservare lo stato del componente figlio corretto.""",
        """function SubjectList({ items }) {
  if (items.length === 0) return <p>Nessun soggetto</p>;

  return <ul>{items.map(item =>
    <li key={item.id}>
      <label>{item.name} <input defaultValue={item.name} /></label>
    </li>
  )}</ul>;
}""",
        """Immagina un input in ogni riga. All'inizio ci sono Anna (10), Luca (20) e Sara (30). Scrivi un testo nell'input di Luca, poi inserisci Marco (15) tra Anna e Luca. Con key={index}, la seconda posizione aveva la key 1 per Luca e continua ad avere la key 1 per Marco: React può riusare per Marco il nodo input che conteneva il testo di Luca. La riga ha cambiato persona, ma la key dice il contrario.

Con key={item.id}, Marco ottiene una nuova identità 15; Luca conserva 20 anche quando passa dalla seconda alla terza posizione, e il suo input resta associato a Luca. Lo stesso problema può apparire riordinando, filtrando o rimuovendo righe. Le key devono essere uniche tra fratelli e stabili nel tempo; Math.random() a ogni render crea identità sempre nuove, facendo ricreare i nodi e perdendo stato o focus.

La key è un suggerimento per React, non una prop ricevuta dal componente. Se una riga ha bisogno dell'ID nel proprio codice, passa anche item.id come normale prop. Il caso items vuoto va descritto esplicitamente; per una condizione booleana evita items.length && ..., che può mostrare lo zero numerico.""",
        "Riproduci il caso con due ID e un input modificato, poi passa dalle key posizionali agli ID. Prova anche [] e un riordinamento. Per una quantità numerica usa `items.length > 0 && ...`: con `items.length && ...` potresti renderizzare 0.",
        "La key deve essere unica tra fratelli e stabile per lo stesso elemento tra render. Permette a React di conservare l'identità della riga, incluso lo stato locale. In una lista modificabile uso l'ID dei dati, evitando indice e numeri casuali.",
        "https://react.dev/learn/preserving-and-resetting-state"),
    "Form controllati": guide(
        ["State ed eventi", "Form e accessibilità", "Errori e validazione"],
        """Un input controllato crea un giro completo tra React e il browser:

~~~text
state React
   ↓
value mostrato nell'input
   ↑
utente digita → onChange → setState → nuovo render
~~~

Il valore parte dallo state, quindi React sa che cosa mostrare. Quando l'utente digita, onChange legge il testo corrente dall'evento e aggiorna lo state; il render successivo restituisce quel testo come value. Se il gestore non aggiorna lo state, React continua a fornire il valore precedente e il campo sembra bloccato.

Il submit è un evento distinto. L'handler può impedire il ricaricamento predefinito, validare i dati e inviare solo ciò che rispetta il contratto.""",
        "import { useState } from 'react';\nexport default function SubjectForm({ onSave }) {\n  const [name, setName] = useState('');\n  const [error, setError] = useState('');\n  function submit(event) {\n    event.preventDefault();\n    if (!name.trim()) { setError('Inserisci un nome'); return; }\n    onSave(name.trim());\n    setName(''); setError('');\n  }\n  return <form onSubmit={submit} noValidate>\n    <label htmlFor=\"name\">Nome</label>\n    <input id=\"name\" value={name} onChange={event => setName(event.target.value)}\n      aria-invalid={Boolean(error)} aria-describedby={error ? 'name-error' : undefined} />\n    {error && <p id=\"name-error\" role=\"alert\">{error}</p>}\n    <button type=\"submit\">Salva</button>\n  </form>;\n}",
        """Il campo parte da una stringa vuota, non da `undefined`: resta controllato fin dal primo render. `value={name}` mostra lo state; `onChange` legge `event.target.value`, che è una stringa, e `setName` richiede il render che la mostrerà. La `label` fornisce il nome accessibile del campo, mentre `aria-invalid` e `aria-describedby` comunicano errore e messaggio associato.

La validazione avviene dentro `submit` perché è l'utente ad aver chiesto di salvare. `trim()` rimuove gli spazi esterni: una stringa composta solo da spazi produce un errore e non chiama `onSave`. `noValidate` rende esplicito questo ramo dell'esempio senza lasciare che la validazione nativa del browser lo intercetti prima. `preventDefault()` impedisce la normale navigazione/invio del form, così è il gestore React a elaborare il submit.

Questo esempio salva in modo sincrono. Con un server, conserviamo il testo e gli errori se la richiesta fallisce e svuotiamo il campo solo dopo il successo. Anche quando il client valida, il server deve controllare di nuovo il contratto e i permessi.""",
        "Verifica submit con Invio, nome vuoto e nome con spazi esterni. L'errore deve essere leggibile, il campo deve conservare il testo invalido e onSave deve ricevere il nome normalizzato una sola volta. Nel lab estendi alla modifica di un record.",
        "Un input è controllato quando value viene dallo stato React e onChange aggiorna quel valore. Il submit può così leggere lo stesso dato mostrato, validarlo e chiamare onSave. Inizializzo lo stato a '' e associo label ed errore al campo."),
    "Progettare e sollevare lo stato": guide(
        ["Props e composizione", "Immutabilità e operazioni CRUD", "Form controllati"],
        """Immagina che SearchBox tenga query="ann" in uno state e Results abbia una propria copia query="anna". Le due parti possono divergere: ogni modifica deve essere copiata manualmente da una all'altra, e un aggiornamento dimenticato mostra conteggio e lista incoerenti.

Quando due componenti devono leggere lo stesso valore, spostane la proprietà nel loro genitore comune. Il genitore passa query e una callback al campo; passa i risultati calcolati alla lista. Così c'è una sola fonte di verità:

~~~text
             Archive
          query = "anna"
            /       \
           ↓         ↓
     SearchBox     Results
       valore       lista filtrata
~~~

La lista filtrata dipende interamente da items e query: non è un terzo stato da mantenere. Calcolala durante il render, come una formula sui valori correnti.""",
        """import { useState } from "react";

function SearchBox({ query, onChange }) {
  return <label>Cerca
    <input value={query} onChange={event => onChange(event.target.value)} />
  </label>;
}

function Results({ items, query }) {
  return <section>
    <p>Risultati per: {query || "tutti"}</p>
    <ul>{items.map(item => <li key={item.id}>{item.name}</li>)}</ul>
  </section>;
}

export default function Archive({ items }) {
  const [query, setQuery] = useState("");
  const normalizedQuery = query.trim().toLowerCase();
  const visibleItems = items.filter(item =>
    item.name.toLowerCase().includes(normalizedQuery)
  );

  return <>
    <SearchBox query={query} onChange={setQuery} />
    <Results items={visibleItems} query={query} />
  </>;
}""",
        """SearchBox non possiede una seconda `query`: mostra quella ricevuta e segnala il testo nuovo con `onChange`. Archive conserva lo state condiviso e lo passa ai componenti che ne hanno bisogno. Se la ricerca è vuota, `includes("")` conserva tutti i nomi; altrimenti il filtro crea l'array che Results mostra. Quando `items` cambia, il render rifà lo stesso calcolo e lista e conteggio restano basati sui dati correnti.

Confrontalo con `visibleItems` salvato in `useState` e sincronizzato da un Effect. Quando `items` o `query` cambiano, React può prima renderizzare con il vecchio `visibleItems`; solo dopo il commit l'Effect lo aggiorna e provoca un altro render. Se la sincronizzazione dimentica una dipendenza, i risultati possono restare vecchi. Qui `visibleItems` è una formula, quindi lo stato duplicato non aggiunge informazione e può divergere.

Un filtro così piccolo non richiede `useMemo`. Una cache introduce complessità e serve solo se una misurazione mostra un costo rilevante. “Lifting state up” risolve chi possiede il valore condiviso; non significa spostare tutto lo state in cima all'applicazione.""",
        "Aggiungi un pulsante che azzera query e mostra di nuovo tutti i risultati. Poi sostituisci items dal genitore: conteggio e lista devono aggiornarsi senza setter dedicati a visible. Nel lab integra eliminazione e ricerca insieme.",
        "Uno stato è derivato se posso calcolarlo interamente da props e altro stato. La lista filtrata dipende da items e query: la calcolo durante render. Non uso un effect per sincronizzarne una copia, evitando un secondo aggiornamento e dati incoerenti.",
        "https://react.dev/learn/you-might-not-need-an-effect"),
    "Effect e sincronizzazione": guide(
        ["State ed eventi", "Scope, const, let e closure", "Progettare e sollevare lo stato"],
        """In un archivio dei soggetti chiediti prima che tipo di lavoro devi fare. L'elenco filtrato è un calcolo a partire da `items` e `query`: si esegue durante il render. Eliminare una riga avviene perché l'utente ha premuto un pulsante: si gestisce nell'event handler. Sincronizzare `document.title` con il conteggio mostrato tocca invece una API del browser, esterna al flusso di React: qui serve un Effect.

`useEffect` descrive un processo di sincronizzazione dopo che React ha aggiornato il DOM. Non è una callback generica per “quando il componente parte”; `setup` e `cleanup` seguono i valori reattivi che il processo usa.""",
        "import { useEffect } from 'react';\nexport default function PageTitle({ title }) {\n  useEffect(() => {\n    const previous = document.title;\n    document.title = title;\n    return () => { document.title = previous; };\n  }, [title]);\n  return <h1>{title}</h1>;\n}",
        """Per il componente dell'esempio, React segue questo ciclo:

~~~text
render → commit → setup: document.title = title

title cambia
render → commit → cleanup con il vecchio title
                 → nuovo setup con il nuovo title

il componente viene rimosso
→ cleanup finale
~~~

La cleanup salva il titolo che c'era prima di questo collegamento e lo ripristina; non annulla lo state React. Questa simmetria descrive anche altri sistemi:

~~~text
subscribe → unsubscribe
setInterval → clearInterval
addEventListener → removeEventListener
start → stop
~~~

Le dipendenze non sono un timer scelto a tentativi. Se il setup legge la prop `title`, `title` deve comparire in `[title]`; quando cambia, React pulisce la sincronizzazione vecchia e ne avvia una nuova. Se lasci l'array vuoto, il setup continua a usare la closure del primo render e il titolo del browser resta obsoleto. Le dipendenze sono quindi i valori reattivi letti dal setup.

In sviluppo, `Strict Mode` può provare un ciclo `setup → cleanup → setup` in più. Se questo produce un effetto visibile scorretto, la cleanup non sta davvero annullando il collegamento; disattivare Strict Mode nasconderebbe il difetto invece di correggerlo.

Per un timer, la cleanup cancella l'ID restituito da `setInterval`. Per un listener, rimuove lo stesso handler dallo stesso target. Per una richiesta remota, la cleanup può abortire o ignorare una risposta diventata obsoleta: lo vedrai nella lezione seguente.""",
        "Aggiorna title dal genitore e poi smonta PageTitle. Verifica document.title nei due momenti. Confronta tre operazioni: filtrare items nel render, salvare nel submit, collegare il titolo con un effect. Motiva la collocazione prima di usare l'hook.",
        "Non richiedono useEffect i calcoli derivabili da props e stato, né le azioni direttamente causate da un evento come submit. Un effect serve per sincronizzare un sistema esterno; include tutte le dipendenze reattive lette e una cleanup quando il collegamento va annullato.",
        "https://react.dev/reference/react/useEffect"),
    "Caricamento dati e stati remoti": guide(
        ["Fetch: loading, error e successo", "Effect e sincronizzazione"],
        """Il risultato di una richiesta non è soltanto una lista. Prima che arrivi c'è il caricamento; la richiesta può fallire; può riuscire senza righe; oppure può riuscire con dati. Una lista vuota non può rappresentare tutti questi casi, perché non dice se il server sia stato contattato o se ci sia stato un errore.

Modelliamo il risultato come una piccola macchina a stati. Lo status dice quale esito è attuale, e ogni esito porta i dati che servono:

~~~text
loading ── successo con righe ─→ success(data)
   │
   ├──── successo senza righe ─→ empty
   └──────────── errore ───────→ error(message)
~~~

Questa è anche la forma di una discriminated union TypeScript: dopo aver controllato `status`, il codice sa se può leggere `data` oppure `message`. In React la UI sceglie un ramo per ciascuno stato.""",
        """import { useEffect, useState } from "react";

export default function RemoteList({ url }) {
  const [attempt, setAttempt] = useState(0);
  const [result, setResult] = useState({ url, attempt: 0, status: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    let ignore = false;
    setResult({ url, attempt, status: "loading" });

    async function load() {
      try {
        const response = await fetch(url, { signal: controller.signal });
        if (!response.ok) {
          throw new Error("HTTP " + response.status);
        }

        const data = await response.json();
        if (!Array.isArray(data)) {
          throw new Error("Risposta non valida");
        }

        if (!ignore) {
          setResult(data.length === 0
            ? { url, attempt, status: "empty" }
            : { url, attempt, status: "success", data });
        }
      } catch (error) {
        if (!ignore) {
          const message = error instanceof Error ? error.message : String(error);
          setResult({ url, attempt, status: "error", message });
        }
      }
    }

    load();
    return () => {
      ignore = true;
      controller.abort();
    };
  }, [url, attempt]);

  if (result.url !== url || result.attempt !== attempt || result.status === "loading") {
    return <p role="status">Caricamento…</p>;
  }
  if (result.status === "error") return <div>
    <p role="alert">{result.message}</p>
    <button onClick={() => {
      setAttempt(value => value + 1);
    }}>Riprova</button>
  </div>;
  if (result.status === "empty") return <p>Nessun soggetto</p>;
  return <ul>{result.data.map(item =>
    <li key={item.id}>{item.name}</li>
  )}</ul>;
}""",
        """Al primo render `result` è `loading` e la UI può annunciarlo con `role="status"`. Se il server restituisce una lista vuota, passiamo a `empty`; se contiene righe, `success` conserva `data`. L'errore è un quarto valore distinto e include il messaggio per `role="alert"`. Non lasciamo `data: []` sia in attesa sia in errore, così `empty` significa davvero “richiesta riuscita, nessun risultato”.

La richiesta viene avviata dall'Effect perché deve seguire la prop `url` anche quando la pagina si apre o cambia URL senza un click specifico. Il codice riusa i passaggi della lezione Fetch: attende `Response`, controlla `ok`, legge il JSON e verifica il contenitore. Per dati esterni il controllo va approfondito fino ai campi usati dalla UI.

La cleanup affronta una gara temporale:

~~~text
richiesta A ─────────────────────────→ risposta A
     richiesta B ───────→ risposta B

ordine di completamento: B, poi A
~~~

Quando parte B, React esegue la cleanup di A. Il flag di A diventa `true` e `abort()` prova a fermare il trasporto. Se A termina comunque più tardi, non può chiamare il setter; B resta il risultato corrente. Abort riduce lavoro quando è possibile, il flag protegge la UI anche se il trasporto ignora l'annullamento.

Ogni risultato conserva anche i valori `url` e `attempt` con cui è stato ottenuto. Se la prop `url` cambia o riprovi, il render rileva che il risultato appartiene alla richiesta precedente e mostra loading subito, prima che parta il nuovo Effect. In questo modo non compare per un frame la lista dell'indirizzo precedente.

Riprova incrementa `attempt` con un updater funzionale; il nuovo valore fa ripartire la sincronizzazione e mostra loading mentre la risposta arriva. `url` e `attempt` sono tutte le dipendenze reattive lette dall'Effect. `idle` serve solo se la richiesta non parte subito, per esempio dopo un'azione esplicita dell'utente.""",
        "Nel laboratorio risolvi prima B e poi A, simulando un trasporto che ignora signal. Devono restare i risultati B. Prova poi errore, retry riuscito e successo con []. Cache e aggiornamenti ottimistici sono estensioni: introducili soltanto dopo aver verificato il flusso base e il recupero dal fallimento.",
        "Distinguo caricamento, errore recuperabile, successo con dati e successo vuoto; idle serve se la richiesta non è ancora partita. Verifico anche retry e risultati fuori ordine: una risposta di una richiesta obsoleta non deve sostituire quella corrente.",
        "https://react.dev/reference/react/useEffect"),
    "Routing e architettura frontend": guide(
        ["Moduli ed organizzazione del codice", "Caricamento dati e stati remoti"],
        "Questo approfondimento chiarisce i confini, senza imporre una libreria di routing. Una route associa un URL a una pagina; un router completo gestisce anche navigazione, parametri, cronologia e URL sconosciuti. Una struttura di cartelle da sola non dimostra quel comportamento. Prima estrai il trasporto e la logica condivisa, poi scegli uno strumento quando l'applicazione richiede davvero più pagine.",
        "// routes.mjs: sola selezione della pagina, non un router completo\nexport function pageFor(pathname) {\n  if (pathname === '/subjects') return 'archive';\n  if (pathname === '/subjects/new') return 'create';\n  return 'not-found';\n}\n// Possibile struttura:\n// features/subjects/Archive.jsx\n// features/subjects/useSubjects.js\n// services/subjectsApi.js",
        """La funzione pageFor dell'esempio decide quale pagina descrivere. Non gestisce URL nel browser, cronologia, refresh o parametri: questi sono comportamenti di un router e vanno valutati quando l'app li richiede. La struttura features/subjects raccoglie invece codice che cambia insieme alla stessa area di prodotto; separare il trasporto in un modulo aiuta a provarlo senza coinvolgere la UI.

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

Riferimenti: [custom hook](https://react.dev/learn/reusing-logic-with-custom-hooks), [Context](https://react.dev/learn/passing-data-deeply-with-context), [reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer).""",
        "Implementa pageFor e prova una route sconosciuta. Per una navigazione reale, annota anche refresh su URL diretto e pulsante Indietro: il controllo breve non li esegue. Estrai poi un hook soltanto se riesci a indicare due utilizzatori con la stessa logica.",
        "Colloco il trasporto in un modulo API e, quando il flusso è riusato, in un hook specifico della feature. La view presenta stato e callback. Estrarre un hook condivide logica ma ogni chiamata mantiene stato proprio; routing e cronologia richiedono una verifica separata.",
        "https://react.dev/learn/reusing-logic-with-custom-hooks"),
}

# Concrete answers for topics whose examples remain useful as originally written.
REVIEW_ANSWERS = {
    "HTTP e API REST": "Dopo una creazione riuscita uso normalmente 201 Created, spesso con Location per la nuova risorsa. Uno status 200 indica successo ma non comunica la creazione; uno status 400 indica input invalido. Il client deve distinguere questi esiti prima di mostrare un risultato.",
    "Autenticazione, CORS e segreti": "CORS è applicato dai browser e regola l'accesso alla risposta da origini diverse. Un client server o da terminale può chiamare l'API senza quel vincolo. L'API deve comunque autenticare il chiamante e autorizzare l'operazione; un segreto non può essere protetto dentro il bundle frontend.",
    "HTML semantico e struttura": "Un button riceve focus e offre attivazione da tastiera e semantica di pulsante. Un div con onClick richiede implementare separatamente queste capacità. Per un'azione uso button; per navigare a una risorsa uso un link con href.",
    "Form e accessibilità": "La validazione client dà feedback prima dell'invio ma può essere aggirata. Il server deve verificare di nuovo il contratto e i permessi. Per esempio un campo required aiuta l'utente, ma non impedisce a un altro client di inviare una richiesta senza quel campo.",
    "Box model, cascade e specificità": "La cascade considera prima origine, importanza e livelli della cascade, poi specificità e ordine a parità delle condizioni precedenti. Una regola più specifica non vince sempre contro una regola importante. Controllo la regola applicata negli strumenti del browser prima di aggiungere !important.",
    "Flexbox e Grid": "Uso Grid quando devo controllare righe e colonne insieme, come una griglia di card. Flexbox è adatto a una toolbar su un asse, con allineamento e distribuzione. Scelgo il layout in base alle relazioni tra gli elementi, non al numero di proprietà da ricordare.",
    "Responsive design": "Mobile first significa partire dal layout per lo spazio ridotto e aggiungere regole quando più spazio permette una struttura diversa. Il breakpoint risponde al contenuto: provo larghezze intermedie, testo lungo e zoom, evitando di legarlo soltanto a un modello di telefono.",
    "Tipi, interface e type": "Una interface descrive un contratto a compile time, ma non valida il JSON a runtime. Un server può restituire un nome numerico anche se il tipo promette una stringa. Tratto il dato esterno come unknown e controllo la sua forma prima di usarlo.",
    "Union e narrowing": dedent("""Un risultato remoto può essere in caricamento, riuscire con dati, riuscire senza righe oppure fallire. Un oggetto con tutti i campi opzionali non spiega quali combinazioni siano ammesse. Una discriminated union associa invece ogni status alla forma valida per quello stato:

~~~typescript
type Subject = { id: number; name: string };

type ArchiveState =
  | { status: "loading" }
  | { status: "success"; data: Subject[] }
  | { status: "empty" }
  | { status: "error"; message: string };
~~~

Quando controlli result.status, TypeScript restringe i casi possibili:

~~~typescript
function assertNever(value: never): never {
  throw new Error("Stato non gestito");
}

function labelForState(state: ArchiveState): string {
  switch (state.status) {
    case "loading": return "Caricamento…";
    case "error": return state.message;
    case "empty": return "Nessun soggetto";
    case "success": return state.data.length + " soggetti";
    default: return assertNever(state);
  }
}
~~~

Nel ramo `error` esiste `message`; nel ramo `success` esiste `data`. Il controllo su `status` restringe `state` al caso corrente. `assertNever` rende esplicita l'esaustività: se aggiungi un nuovo status e dimentichi il relativo ramo, TypeScript segnala il valore che non è più `never`.

Il tipo rende più difficile scrivere una UI che tenta di mostrare una proprietà assente.

Questa garanzia vale durante il controllo TypeScript del programma. I tipi vengono rimossi a runtime: una risposta JSON non diventa valida solo perché la variabile è annotata ArchiveState. Prima di usarla bisogna controllare i dati esterni con una guardia runtime, come nella lezione Null, unknown e confini esterni.""").strip(),
    "Generics essenziali": "first<T> mantiene la relazione tra il tipo degli elementi e il risultato T oppure undefined. Una funzione con any perde quella informazione. Con un array di numeri il chiamante sa di dover gestire un numero o l'assenza, e non una qualunque proprietà arbitraria.",
    "Null, unknown e confini esterni": "unknown obbliga a restringere il tipo prima di accedere a proprietà o chiamare metodi; any disattiva quei controlli. Un JSON esterno può avere qualsiasi forma, quindi unknown rende visibile il confine da validare invece di nasconderlo con un cast.",
    "Node, event loop e moduli": "Un calcolo sincrono lungo occupa il thread principale e ritarda callback, timer e gestione di altre richieste. L'I/O asincrono evita di aspettare inutilmente file o rete, ma non rende parallelo un calcolo CPU. Per carichi CPU rilevanti valuto un worker o un processo dedicato.",
    "Route, middleware e validazione": "Il middleware prepara o controlla una richiesta e poi passa al passo successivo, oppure termina la risposta. Per esempio verifica l'input prima dell'handler. Il servizio applica la regola di business; il middleware degli errori traduce i fallimenti in risposte coerenti.",
    "Sicurezza web essenziale": "Una query parametrizzata mantiene separati il testo SQL e i valori dell'utente, che vengono trattati come dati. Un apostrofo nel nome non deve diventare una parte eseguibile della query. Parametrizzazione e controllo dei permessi risolvono rischi diversi e servono entrambi.",
    "SELECT, filtri e ordinamento": "Nel modello logico parto da FROM e JOIN, filtro con WHERE, scelgo le colonne con SELECT e ordino con ORDER BY. L'ottimizzatore può eseguire fisicamente un piano diverso. Se l'ordine fa parte del requisito lo dichiaro, invece di fidarmi delle righe ottenute in una prova.",
    "Relazioni e JOIN": "INNER JOIN conserva le righe che hanno una corrispondenza; LEFT JOIN conserva tutte le righe di sinistra e usa NULL per i campi di destra mancanti. Un filtro sulla tabella destra in WHERE può eliminare quelle righe: controllo il caso del soggetto senza misura.",
    "Vincoli, indici e normalizzazione": "Un indice occupa spazio e va aggiornato quando cambiano i dati, aumentando il costo delle scritture. Può accelerare letture adatte alla sua struttura. Scelgo un indice da query reali e verifico il piano, evitando di indicizzare ogni colonna automaticamente.",
    "Transazioni e concorrenza": "Un trasferimento richiede che addebito e accredito siano atomici. Se il secondo passo fallisce eseguo rollback, altrimenti perderei denaro. Controllo anche l'esistenza dei conti e il saldo prima del commit: una transazione da sola non valida la regola applicativa.",
    "Git: working tree, staging e commit": "git diff mostra le modifiche del working tree rispetto allo staging; git diff --staged mostra ciò che lo staging aggiungerà al prossimo commit rispetto a HEAD. Controllo entrambi: un file può avere contemporaneamente una parte già staged e altre modifiche non staged.",
    "Branch, merge e conflitti": "HEAD indica il commit corrente, normalmente attraverso il branch attivo. In detached HEAD indica direttamente un commit. Un conflitto richiede scegliere la combinazione corretta delle modifiche e verificarla, non soltanto rimuovere i marcatori dal file.",
    "Test unitari, integrazione ed E2E": "Preferisco un test di integrazione quando il rischio è nella collaborazione tra parti, per esempio un submit che valida e aggiorna la lista. Un test della sola funzione di validazione non prova quel collegamento. Un E2E aggiunge browser e sistema reale, con un costo e una copertura differenti.",
    "Code review e refactoring": "Prima caratterizzo il comportamento del file con casi rilevanti. Estraggo una responsabilità per volta, mantenendo invariati input e output, poi eseguo i test. Distinguo il refactoring da una correzione funzionale per poter attribuire ogni regressione a una modifica circoscritta.",
    "PHP e ciclo di un plugin WordPress": "Un'action esegue un comportamento quando WordPress annuncia un evento; un filtro riceve un valore e deve restituire il valore trasformato. Per esempio un filtro può modificare un titolo. Non modifico il core e uso nomi distinti per evitare collisioni con altri plugin.",
    "Sicurezza WordPress": "Sanitizzo l'input per adeguarlo al formato previsto ed eseguo escaping al momento dell'output secondo il contesto HTML, attributo o URL. Il nonce non sostituisce current_user_can: controllo anche che l'utente abbia il permesso richiesto.",
    "Presentare l'architettura di un'app Electron": "Il renderer esegue la UI e può ricevere contenuto non affidabile; offrirgli filesystem e database amplia le conseguenze di un bug. Il preload espone operazioni ristrette e l'IPC attraversa il confine verso main, che valida gli argomenti prima di invocare servizi e repository.",
    "Presentare una pipeline AI multimodale": "Se TTS fallisce, la risposta testuale può rimanere disponibile mentre l'audio mostra un errore recuperabile. Conservo l'ID della richiesta per evitare che un retry associ audio a una risposta diversa. Distinguo il fallimento di un servizio dal fallimento dell'intera conversazione.",
    "Parlare onestamente dell'uso dell'IA": "Scelgo una parte piccola, per esempio il filtro di un archivio, e la ricostruisco dal contratto senza leggere la soluzione. Verifico i casi limite e spiego le decisioni. Distinguo ciò che ho progettato o corretto dal codice proposto dallo strumento e non compreso inizialmente.",
    "Comunicare decisioni tecniche e risultati": "Descrivo un bug attraverso input, risultato atteso e sintomo osservato. Racconto l'ipotesi controllata, la correzione minima e il test di regressione aggiunto. Il risultato deve essere verificabile: evito di limitarmi a dire che il codice è diventato migliore.",
}
REVIEW_ANSWERS.update({title: item['answer'] for title, item in GUIDES.items()})
