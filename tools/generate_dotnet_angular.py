"""
Generatore di contenuti per il percorso DEV//48: Angular & .NET Enterprise Academy.
Genera il catalogo e i file Markdown del percorso Angular e .NET con:
- spiegazioni, esempi, passaggi di studio e casi limite
- esercizi con verifiche comportamentali o strutturali esplicite
"""

from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
LESSONS_DOTNET = CONTENT / "lessons_dotnet"


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", value.lower())
    return re.sub(r"[\s-]+", "-", cleaned).strip("-")


MODULES = [
    ("00_orientamento", "00", "Orientamento & Toolchain", "Configura .NET SDK, Node.js, Angular CLI e imposta un metodo di studio ingegneristico."),
    ("00_fondamenti", "01", "Fondamenti C#, TypeScript, HTML e CSS", "Primi metodi, variabili, funzioni, array e struttura dei template prima dei framework."),
    ("01_csharp", "02", "C# Moderno", "Tipi primitivi, record, pattern matching, LINQ, async/await ed eccezioni."),
    ("02_typescript", "03", "TypeScript & Contratti per il Web", "Tipi statici, interfacce, union discriminate e generics."),
    ("03_aspnet_api", "04", "Web API con ASP.NET Core", "Minimal API, dependency injection, pipeline middleware, DTO e validazione HTTP."),
    ("04_angular_core", "05", "Angular Moderno: Standalone & Control Flow", "Componenti Standalone, blocchi @if, @for, @switch e data binding."),
    ("05_angular_signals", "06", "Reattività con Angular Signals & State", "signal(), computed(), effect(), input/output e interoperabilità con RxJS."),
    ("06_efcore", "07", "Database con Entity Framework Core", "DbContext, migrazioni, mapping delle relazioni, query LINQ e tracking."),
    ("07_angular_forms_routing", "08", "Form Reattivi & Routing", "Reactive Forms, introduzione a Signal Forms, validatori, Angular Router e guard funzionali."),
    ("08_security_fullstack", "09", "Autenticazione JWT & Sicurezza Full-Stack", "Token JWT, autorizzazione, HTTP Interceptors e CORS."),
    ("09_quality_testing", "10", "Testing e Architettura", "Test automatici, principi SOLID e separazione dei layer."),
    ("10_portfolio_monorepo", "11", "Monorepo & Portfolio", "Architettura client/server, documentazione e progetto finale."),
]

# Preserve generated lesson IDs while making the first coding practice follow a
# short C# introduction. The remaining lessons keep their authored sequence.
INITIAL_LESSON_SEQUENCE = [
    "Setup dell'ambiente moderno per Angular e .NET",
    "Il primo metodo C#: parametri, variabili e valore restituito",
    "Anatomia di una soluzione Full-Stack Client-Server",
    "Metodo di debugging per API e Frontend",
]

# Argomenti e relative prove del percorso
# Ogni voce:
# (module, title, minutes, mandatory, summary, concepts, simple_exp, syntax_anatomy, example, pattern_guide, pitfalls, review_q, code_ex)
TOPICS = [
    # ==========================================
    # MODULO 00: Orientamento & Toolchain
    # ==========================================
    (
        "00_orientamento", "Setup dell'ambiente moderno per Angular e .NET", 25, True,
        "Verificare la presenza di .NET SDK, Node.js, Angular CLI e impostare VS Code con estensioni essenziali.",
        "dotnet sdk;node.js;angular cli;vs code;terminale;toolchain",
        "Installa il .NET SDK 10 per compilare C# e Node.js per usare npm e gli strumenti Angular. Il browser esegue l'app Angular; Node.js serve durante lo sviluppo e i test. L'Angular CLI può essere richiamata con npx, quindi non occorre installarla globalmente.",
        """### 1. Installa gli strumenti
1. Scarica il **.NET 10 SDK** dal [sito ufficiale .NET](https://dotnet.microsoft.com/download/dotnet/10.0). Scegli l'SDK, non soltanto il Runtime.
2. Installa una versione Node supportata da Angular 22. Per iniziare è comoda la linea LTS 24; consulta la [tabella di compatibilità Angular](https://angular.dev/reference/versions) prima di cambiare versione.
3. Installa Git e Visual Studio Code se vuoi usare il controllo versione e l'editor grafico. Sono consigliati, ma non richiesti per leggere le lezioni.
4. Dopo l'installazione, apri una nuova finestra di PowerShell così il `PATH` viene ricaricato.

### 2. Verifica le versioni in PowerShell
```bash
dotnet --list-sdks  # deve comparire una versione 10.0.x
node --version      # Angular 22: 22.22.3+, 24.15.0+ o 26.0.0+
npm --version
```

`dotnet --version` mostra l'SDK selezionato nella cartella corrente; `dotnet --list-sdks` mostra tutti quelli installati. Il runtime da solo non compila il codice del corso.

### 3. Controlla Angular CLI senza installazione globale
In un progetto Angular usa `npx ng version`: npm esegue la CLI dichiarata dal progetto. Per verificare il download iniziale senza avere ancora un progetto, puoi eseguire `npx --yes @angular/cli@22.2.0 version`.""",
        """Comandi da provare in PowerShell:
dotnet --list-sdks
node --version
npm --version
npx --yes @angular/cli@22.2.0 version""",
        "Gli output devono mostrare .NET SDK 10, una versione Node supportata da Angular 22 e una Angular CLI 22. Se un comando non viene trovato, controlla l'installazione e apri una nuova finestra di PowerShell.",
        "Dimenticare di riavviare il terminale dopo l'installazione del SDK; confondere Runtime con SDK di .NET.",
        "Come verifichi dal terminale che il compilatore .NET e l'interprete Node siano installati e pronti all'uso?",
        {
            "kind": "reflection",
            "title": "Prova pratica della toolchain",
            "prompt": "Esegui nel terminale i quattro comandi mostrati nella lezione. In 4 righe annota il risultato di `dotnet --list-sdks`, `node --version`, `npm --version` e `npx --yes @angular/cli@22.2.0 version`; indica quale versione deve comparire e che cosa controlleresti se un comando non fosse disponibile. Questa autoverifica cerca solo i nomi dei comandi nella risposta: non esegue il terminale e non controlla le versioni riportate. Confronta il risultato con il modello.",
            "starter": "",
            "solution": """dotnet --list-sdks: deve mostrare un SDK 10.0.x.
node --version: per Angular 22 usare una versione compatibile indicata nella lezione.
npm --version: deve mostrare una versione di npm installata insieme a Node.js.
npx --yes @angular/cli@22.2.0 version: deve mostrare Angular CLI 22. Se un comando non esiste, verifica l'installazione e riapri PowerShell per aggiornare il PATH.""",
            "tests": [
                {"name": "Riporta il controllo dell'SDK", "alternatives": ["dotnet --list-sdks"]},
                {"name": "Riporta il controllo di Node", "alternatives": ["node --version"]},
                {"name": "Riporta il controllo di npm", "alternatives": ["npm --version"]},
                {"name": "Riporta il controllo della CLI", "alternatives": ["npx --yes @angular/cli@22.2.0 version"]},
            ],
            "hints": [
                "Esegui un comando per volta nella cartella di lavoro.",
                "Confronta `dotnet --list-sdks` e `node --version` con i requisiti del corso.",
                "L'autoverifica controlla soltanto che tu abbia annotato i quattro comandi; confronta i risultati reali con il modello."
            ],
            "creative_goals": [],
            "xp": 0,
            "bonus_xp": 0
        }
    ),
    (
        "00_orientamento", "Anatomia di una soluzione Full-Stack Client-Server", 30, True,
        "Seguire una richiesta tra client Angular nel browser e server ASP.NET Core, distinguendo indirizzi, risposte e configurazione CORS.",
        "architettura client server;richiesta http;json;cors;porta di ascolto;stato della sessione",
        "Il frontend Angular mostra l'interfaccia nel browser; il backend ASP.NET Core applica regole e accesso ai dati. Si scambiano richieste e risposte HTTP, spesso con dati JSON. Nel primo esercizio C# si usano metodi e parametri già introdotti nella lezione precedente.",
        """### Flusso della Richiesta Full-Stack:
1. **Client (Browser/Angular)**:
   - Utente clicca un pulsante -> Angular invia una richiesta HTTP (GET, POST, PUT, DELETE) serializzando i dati in JSON.
   - Resta in attesa asincrona della risposta (Promise/Observable/Signal).
2. **Rete e Porte**:
   - Client e Server girano su porte differenti (es. Angular su `localhost:4200`, API .NET su `localhost:5001`).
   - Il server deve abilitare il CORS (Cross-Origin Resource Sharing) per consentire le chiamate dal frontend.
3. **Backend (.NET Minimal API)**:
   - Riceve la richiesta HTTP, deserializza il JSON nel relativo DTO C#.
   - Esegue la logica di business, legge o scrive su SQLite/EF Core.
   - Restituisce uno Status Code HTTP (200 OK, 201 Created, 400 Bad Request) con payload JSON.

### Unire le parti di un endpoint in C#
`TrimEnd('/')` rimuove le barre finali dall'indirizzo base; `TrimStart('/')` rimuove quelle iniziali dal percorso. La stringa `$"{baseClean}/{resourceClean}"` inserisce i due valori nel testo.

```csharp
var baseClean = baseUrl.TrimEnd('/');
var resourceClean = resource.TrimStart('/');
var endpoint = $"{baseClean}/{resourceClean}";
```""",
        "// Frontend (Angular) invia richiesta GET a https://localhost:5001/api/items\n// Backend (ASP.NET Core) elabora, legge dal DB e risponde con JSON [ { id: 1, name: 'Item' } ]",
        """public static class EndpointMapper {
    public static string FormatUrl(string baseUrl, string resource) {
        return $"{baseUrl.TrimEnd('/')}/{resource.TrimStart('/')}";
    }
}""",
        "Credere che Angular esegua codice C# nel browser; ignorare che client e server girano su porte e processi separati.",
        "Qual è il ruolo rispettivo del client Angular e del server .NET nel ciclo di vita di una richiesta?",
        {
            "kind": "csharp",
            "title": "Compositore URL Endpoint API",
            "prompt": "Implementa il metodo `EndpointMapper.FormatUrl(string baseUrl, string resource)` che combina un URL base e il nome della risorsa rimuovendo barre duplicate.",
            "starter": """public static class EndpointMapper {
    /// <summary>
    /// Combina baseUrl e resource evitando doppie barre (es. 'https://api.com/' + '/users' -> 'https://api.com/users').
    /// </summary>
    public static string FormatUrl(string baseUrl, string resource) {
        // TODO: Scrivi qui la tua logica
        return "";
    }
}""",
            "solution": """public static class EndpointMapper {
    public static string FormatUrl(string baseUrl, string resource) {
        if (string.IsNullOrWhiteSpace(baseUrl)) return resource ?? "";
        if (string.IsNullOrWhiteSpace(resource)) return baseUrl;
        return $"{baseUrl.TrimEnd('/')}/{resource.TrimStart('/')}";
    }
}""",
            "tests": [
                {"name": "Formattazione con barre duplicate", "expression": 'EndpointMapper.FormatUrl("https://localhost:5001/", "/api/users")', "expected": "https://localhost:5001/api/users"},
                {"name": "Formattazione senza barre", "expression": 'EndpointMapper.FormatUrl("https://localhost:5001", "api/users")', "expected": "https://localhost:5001/api/users"},
            ],
            "hints": [
                "Usa `.TrimEnd('/')` sull'URL base e `.TrimStart('/')` sulla risorsa per normalizzare le barre.",
                "Combina poi i valori con l'interpolazione di stringhe: `$\"{baseClean}/{resourceClean}\"`.",
                "Snippet: `return $\"{baseUrl.TrimEnd('/')}/{resource.TrimStart('/')}\";`."
            ],
            "creative_goals": ["Gestisci con eleganza input nulli o composti da soli spazi", "Usa string interpolation con expression body"],
            "bonus_xp": 20
        }
    ),
    (
        "00_orientamento", "Metodo di debugging per API e Frontend", 30, True,
        "Isolare un errore distinguendo problemi di compilazione C#, errori HTTP di rete e bug di rendering Angular.",
        "stack trace;network tab;status code;console.log;breakpoint;falsificabile",
        "Il debugging sistematico richiede di isolare il perimetro: prima verifica la rete (DevTools Network), poi l'output del backend (log o eccezioni C#), infine lo stato del componente Angular. Qui usiamo un metodo con `if` e `return` per classificare pochi codici HTTP: ogni ramo è spiegato prima dell'esercizio.",
        """### Matrice Diagnostica degli Errori:
- **Errore di Compilazione C# (`error CS...`)**: il backend non compila per sintassi errata, tipi non corrispondenti o riferimenti mancanti.
- **Errore HTTP 4xx (Client Error)**:
  - `400 Bad Request`: il JSON inviato da Angular non rispetta il formato atteso dal DTO .NET.
  - `401 Unauthorized`: token JWT assente o non valido (per esempio scaduto); `403 Forbidden`: identità autenticata senza il ruolo o permesso richiesto.
  - `404 Not Found`: l'URL o la rotta dell'API è errata.
- **Errore HTTP 500 (Internal Server Error)**: eccezione non gestita nel backend .NET (es. `NullReferenceException`, errore di query DB). Controlla il terminale del server per lo stack trace.
- **CORS Error nel browser**: il server .NET non ha abilitato la policy per l'origine Angular (`http://localhost:4200`).

### Un metodo C# con `if`
`if (condizione)` esegue il ramo quando la condizione è vera. `&&` significa “entrambe le condizioni sono vere”; `return` restituisce il testo e termina il metodo, quindi il primo ramo soddisfatto è quello usato.

```csharp
public static string Classify(int statusCode) {
    if (statusCode >= 200 && statusCode <= 299) return "Success";
    if (statusCode >= 400 && statusCode <= 499) return "ClientError";
    if (statusCode >= 500 && statusCode <= 599) return "ServerError";
    return "Other";
}
```""",
        "// 1. Guarda la Console del browser per errori JS/TS\n// 2. Guarda il tab Network per vedere lo status code HTTP (400, 404, 500)\n// 3. Guarda il terminale del server per lo stack trace C#",
        """public static class HttpErrorClassifier {
    public static string Classify(int statusCode) {
        if (statusCode >= 200 && statusCode <= 299) return "Success";
        if (statusCode >= 400 && statusCode <= 499) return "ClientError";
        if (statusCode >= 500 && statusCode <= 599) return "ServerError";
        return "Other";
    }
}""",
        "Cercare l'errore nel componente Angular quando la richiesta fallisce con HTTP 500 nel server; modificare file a caso senza leggere il messaggio.",
        "Se un pulsante in Angular non aggiorna la tabella, quali tre controlli esegui in ordine?",
        {
            "kind": "csharp",
            "title": "Classificatore di Status Code HTTP",
            "prompt": "Implementa il metodo `HttpErrorClassifier.Classify(int statusCode)` che categorizza uno status code in 'Success' (200-299), 'ClientError' (400-499), 'ServerError' (500-599), o 'Other' per tutti gli altri codici.",
            "starter": """public static class HttpErrorClassifier {
    /// <summary>
    /// Restituisce la categoria dello status code HTTP.
    /// </summary>
    public static string Classify(int statusCode) {
        // TODO: Scrivi qui la logica di classificazione
        return "Unknown";
    }
}""",
            "solution": """public static class HttpErrorClassifier {
    public static string Classify(int statusCode) {
        if (statusCode >= 200 && statusCode <= 299) return "Success";
        if (statusCode >= 400 && statusCode <= 499) return "ClientError";
        if (statusCode >= 500 && statusCode <= 599) return "ServerError";
        return "Other";
    }
}""",
            "tests": [
                {"name": "199 è fuori dalle fasce", "expression": "HttpErrorClassifier.Classify(199)", "expected": "Other"},
                {"name": "200 OK è Success", "expression": "HttpErrorClassifier.Classify(200)", "expected": "Success"},
                {"name": "299 è l'ultimo Success", "expression": "HttpErrorClassifier.Classify(299)", "expected": "Success"},
                {"name": "300 è fuori dalle fasce", "expression": "HttpErrorClassifier.Classify(300)", "expected": "Other"},
                {"name": "400 è il primo ClientError", "expression": "HttpErrorClassifier.Classify(400)", "expected": "ClientError"},
                {"name": "499 è l'ultimo ClientError", "expression": "HttpErrorClassifier.Classify(499)", "expected": "ClientError"},
                {"name": "500 è il primo ServerError", "expression": "HttpErrorClassifier.Classify(500)", "expected": "ServerError"},
                {"name": "599 è l'ultimo ServerError", "expression": "HttpErrorClassifier.Classify(599)", "expected": "ServerError"},
                {"name": "600 è fuori dalle fasce", "expression": "HttpErrorClassifier.Classify(600)", "expected": "Other"},
            ],
            "hints": [
                "Controlla prima se `statusCode` è compreso tra 200 e 299, estremi inclusi.",
                "Usa `&&` per chiedere che siano vere entrambe le condizioni del limite inferiore e superiore.",
                "Ripeti il controllo per le altre due fasce; per ogni altro valore restituisci `Other`."
            ],
            "creative_goals": ["Riduci le condizioni ripetute senza cambiare i limiti inclusivi", "Aggiungi una descrizione XML del contratto"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 01: C# Moderno da Zero
    # ==========================================
    (
        "00_fondamenti", "Il primo metodo C#: parametri, variabili e valore restituito", 40, True,
        "Leggere e scrivere un metodo C# semplice, riconoscendone input, istruzioni e risultato.",
        "programma;classe;metodo;parametro;variabile;return;string",
        "Un metodo è una parte nominata del programma: può ricevere dati attraverso i parametri e restituire un risultato. La classe raccoglie metodi correlati; per questo primo esempio non serve ancora conoscere oggetti o database.",
        """### Leggere la firma di un metodo
```csharp
public static string SayHello(string name)
```
- `public` rende il metodo accessibile da altre classi.
- `static` permette di chiamarlo sulla classe senza creare un oggetto.
- `string` prima del nome è il tipo del risultato.
- `name` è un parametro: il valore arriva a ogni chiamata.

Il corpo tra `{ }` contiene istruzioni. `return` termina il metodo e consegna il valore al chiamante.""",
        """var greeting = Greeter.SayHello("Ada");
Console.WriteLine(greeting);

public static class Greeter {
    public static string SayHello(string name) {
        var message = \"Ciao, \" + name + \"!\";
        return message;
    }
}""",
        """public static class TextTools {
    public static string JoinWithComma(string first, string second) {
        return first + \", \" + second;
    }
}""",
        "Dimenticare `return`; restituire un tipo diverso da quello dichiarato; chiamare un metodo statico come se servisse un oggetto.",
        "Che cosa riceve un metodo tramite un parametro e che cosa consegna tramite `return`?",
        {
            "kind": "csharp",
            "title": "Metodo di saluto",
            "prompt": "Completa `Greeter.SayHello(string name)` affinché restituisca `Ciao, ` seguito dal nome e da `!`. Per esempio, `SayHello(\"Luca\")` deve restituire `Ciao, Luca!`.",
            "starter": "public static class Greeter {\n    public static string SayHello(string name) {\n        // TODO: crea e restituisci il saluto\n        return \"\";\n    }\n}",
            "solution": "public static class Greeter {\n    public static string SayHello(string name) {\n        return \"Ciao, \" + name + \"!\";\n    }\n}",
            "tests": [
                {"name": "Nome inserito nel saluto", "expression": 'Greeter.SayHello("Luca")', "expected": "Ciao, Luca!"},
                {"name": "Nome composto mantenuto", "expression": 'Greeter.SayHello("Ada Lovelace")', "expected": "Ciao, Ada Lovelace!"}
            ],
            "hints": ["Il metodo restituisce una stringa, quindi il risultato deve essere una sequenza di testo.", "Concatena le tre parti: prefisso, `name`, punto esclamativo.", "Usa `return \"Ciao, \" + name + \"!\";`."],
            "creative_goals": [],
            "xp": 20,
            "bonus_xp": 0
        }
    ),
    (
        "01_csharp", "Tipi primitivi, tipi riferimento e nullable in C#", 35, True,
        "Riconoscere tipi valore e riferimento, usare nullable e leggere i warning di nullabilità senza basarsi su una regola stack/heap.",
        "int;string;bool;tipo valore;tipo riferimento;nullable;operatore null-coalescing",
        "Un tipo valore viene copiato come valore; una variabile di tipo riferimento contiene un riferimento a un oggetto. La posizione fisica in memoria dipende dal contesto: non si può dedurre soltanto dalla categoria del tipo.",
        """### Tipi Valore vs Tipi Riferimento:
- **Tipi Valore (`struct`)**: `int`, `double`, `bool`, `DateTime`, `decimal`.
  - Una copia della variabile copia il valore. I tipi valore non sono `null` per impostazione predefinita.
  - Per renderli nullable, si aggiunge `?`: `int? age = null;`.
- **Tipi Riferimento (`class`)**: `string`, `object`, classi personalizzate, array.
  - La variabile contiene un riferimento; copiare la variabile copia il riferimento, non l'oggetto.
  - Con i **Nullable Reference Types** abilitati, `string` dichiara l'intenzione di non usare `null`, mentre `string?` dichiara che `null` è previsto. Sono controlli statici del compilatore, non una protezione runtime.

### Operatori per gestire `null`:
- **Null-coalescing (`??`)**: `name ?? "Default"` restituisce `name` se valorizzato, altrimenti `"Default"`.
- **Null-conditional (`?.`)**: `user?.Address?.City` accede alla proprietà solo se `user` e `Address` non sono null, evitando `NullReferenceException`.""",
        "string? name = null;\nstring displayName = name ?? \"Utente Ospite\";\nint age = 25;\nConsole.WriteLine($\"{displayName} ha {age} anni\");",
        """public static class UserFormatter {
    public static string FormatName(string? firstName, string? lastName) {
        var first = firstName?.Trim();
        var last = lastName?.Trim();
        if (string.IsNullOrEmpty(first) && string.IsNullOrEmpty(last)) return "Anonimo";
        return $"{first} {last}".Trim();
    }
}""",
        "Ignorare i warning sui nullable reference types (`string?`); dimenticare che i tipi valore non possono essere null a meno di dichiararli esplicitamente con `?`.",
        "Qual è la differenza fondamentale tra un tipo per valore e un tipo per riferimento in C#?",
        {
            "kind": "csharp",
            "title": "Gestione Nullable e Valori di Default",
            "prompt": "Implementa `UserFormatter.GetDisplayName(string? name, string fallback)` che restituisce `name` pulito da spazi bianchi esterni se non è nullo né vuoto, altrimenti restituisce `fallback`.",
            "starter": """public static class UserFormatter {
    /// <summary>
    /// Restituisce il nome pulito oppure il valore di fallback se nullo o vuoto.
    /// </summary>
    public static string GetDisplayName(string? name, string fallback) {
        // TODO: Scrivi qui il tuo codice
        return fallback;
    }
}""",
            "solution": """public static class UserFormatter {
    public static string GetDisplayName(string? name, string fallback) {
        if (string.IsNullOrWhiteSpace(name)) return fallback;
        return name.Trim();
    }
}""",
            "tests": [
                {"name": "Nome valido", "expression": 'UserFormatter.GetDisplayName("  Mario  ", "Anonimo")', "expected": "Mario"},
                {"name": "Nome nullo usa fallback", "expression": 'UserFormatter.GetDisplayName(null, "Ospite")', "expected": "Ospite"},
                {"name": "Nome vuoto usa fallback", "expression": 'UserFormatter.GetDisplayName("   ", "Anonimo")', "expected": "Anonimo"},
            ],
            "hints": [
                "Usa `string.IsNullOrWhiteSpace(name)` per verificare contemporaneamente valori nulli, vuoti o composti da soli spazi.",
                "Se non è nullo né vuoto, applica `name.Trim()` per rimuovere gli spazi superflui.",
                "Snippet: `return string.IsNullOrWhiteSpace(name) ? fallback : name.Trim();`."
            ],
            "creative_goals": ["Usa l'operatore ternario `condition ? a : b`", "Evita qualsiasi rischio di NullReferenceException"],
            "bonus_xp": 20
        }
    ),
    (
        "01_csharp", "Controllo di flusso, Pattern Matching e Switch Expressions", 40, True,
        "Scrivere diramazioni logiche eleganti e sicure usando le nuove switch expressions di C#.",
        "switch expression;pattern matching;is;when;guard condition;discard",
        "Una switch expression confronta un valore con più pattern e restituisce il risultato del primo ramo corrispondente; il ramo `_` fornisce il caso restante. Se nessun ramo corrisponde, a runtime viene sollevata un'eccezione.",
        """### Sintassi della Switch Expression in C# 12:
```csharp
var risultato = espressione switch {
    pattern1 => valore1,
    pattern2 when condizione_guardia => valore2,
    _ => valore_default // Caso restante per i valori non coperti
};
```

### Tipologie di Pattern Matching:
1. **Constant pattern**: `"admin" => ...`
2. **Relational pattern**: `> 100 and <= 500 => ...`
3. **Type pattern**: `string s => s.ToUpper()`
4. **Positional / Tuple pattern**: `(var role, true) => ...`
5. **Property pattern**: `{ Status: "Active", Age: >= 18 } => ...`""",
        "string GetRoleDescription(string role, bool isSuperUser) => (role, isSuperUser) switch\n{\n    (\"admin\", true) => \"Super Amministratore\",\n    (\"admin\", false) => \"Amministratore standard\",\n    (\"user\", _) => \"Utente registrato\",\n    _ => \"Ospite sconosciuto\"\n};",
        """public static class PricingEngine {
    public static decimal CalculateDiscount(decimal amount, bool isPremium) => (amount, isPremium) switch {
        ( >= 500, true) => 0.25m,
        ( >= 500, false) => 0.15m,
        ( >= 100, true) => 0.10m,
        _ => 0.00m
    };
}""",
        "Usare cascate di if/else annidati illeggibili; dimenticare il ramo di scarto `_` (discard) provocando eccezioni a runtime.",
        "Quale vantaggio offre una switch expression rispetto a un blocco switch classico imperativo?",
        {
            "kind": "csharp",
            "title": "Motore di Sconto con Pattern Matching",
            "prompt": "Implementa `PricingEngine.CalculateDiscount(decimal total, bool isVip)` con una switch expression che restituisce la percentuale intera di sconto: 20 se total >= 200 e isVip; 10 se total >= 200 e non è vip; 5 se total >= 50 e isVip; altrimenti 0.",
            "starter": """public static class PricingEngine {
    /// <summary>
    /// Calcola la percentuale intera di sconto applicata a un ordine.
    /// </summary>
    public static int CalculateDiscount(decimal total, bool isVip) {
        // TODO: Implementa la logica con una switch expression
        return 0;
    }
}""",
            "solution": """public static class PricingEngine {
    public static int CalculateDiscount(decimal total, bool isVip) => (total, isVip) switch {
        ( >= 200m, true) => 20,
        ( >= 200m, false) => 10,
        ( >= 50m, true) => 5,
        _ => 0
    };
}""",
            "tests": [
                {"name": "Ordine 250 VIP -> 20%", "expression": "PricingEngine.CalculateDiscount(250m, true)", "expected": 20},
                {"name": "Ordine 250 non VIP -> 10%", "expression": "PricingEngine.CalculateDiscount(250m, false)", "expected": 10},
                {"name": "Ordine 80 VIP -> 5%", "expression": "PricingEngine.CalculateDiscount(80m, true)", "expected": 5},
                {"name": "Ordine 30 standard -> 0%", "expression": "PricingEngine.CalculateDiscount(30m, false)", "expected": 0},
            ],
            "hints": [
                "Abbina i due valori creando una tupla: `(total, isVip) switch { ... }`.",
                "Usa pattern relazionali sulle tuple: `( >= 200m, true) => 0.20m`.",
                "Non dimenticare il ramo di fallback per tutti gli altri casi: `_ => 0.00m`."
            ],
            "creative_goals": ["Usa una tupla posizionale con pattern relazionali", "Completa la soluzione come expression-bodied member `=>`"],
            "bonus_xp": 20
        }
    ),
    (
        "01_csharp", "Classi, Record e Costruttori Primari", 45, True,
        "Confrontare class e record per uguaglianza e sintassi, senza assumere che ogni record sia immutabile in profondità.",
        "record;class;costruttore primario;immutabilita;with expression;uguaglianza per valore",
        "I record generano uguaglianza per valore e una sintassi concisa per i dati. Un record posizionale usa proprietà init-only, ma i record non sono immutabili in profondità: membri mutabili e oggetti annidati possono comunque cambiare.",
        """### Differenze tra `class` e `record`:
- **`class`**: Uguaglianza per riferimento (due istanze con le stesse proprietà sono diverse in memoria). Pensata per oggetti con stato mutabile e logica di business complessa.
- **`record`**: implementa uguaglianza per valore. Due record con gli stessi valori confrontati con `==` risultano uguali.
  - Le proprietà di un record posizionale sono normalmente `init`-only; un record può comunque contenere membri mutabili o riferimenti a oggetti mutabili.
  - L'espressione `with` crea una copia superficiale e permette di sostituire proprietà:
    `var updated = original with { Price = 29.99m };`

### Sintassi del Costruttore Primario:
```csharp
// Record posizionale: uguaglianza per valore e proprietà init-only.
public record ProductDto(int Id, string Title, decimal Price);
```""",
        "public record SubjectDto(int Id, string Name, string Zone);\n\nvar s1 = new SubjectDto(1, \"Mario\", \"Centro\");\nvar s2 = s1 with { Zone = \"Nord\" }; // Crea copia modificata senza mutare s1",
        """public record Customer(int Id, string Name, string Tier) {
    public Customer Upgrade() => this with { Tier = "Gold" };
}""",
        "Confondere l'uguaglianza dei record (basata sui valori) con quella predefinita delle classi (basata sull'identità del riferimento); assumere che un record renda immutabili anche gli oggetti contenuti.",
        "Quando preferisci usare un `record` invece di una classica `class` in un'API?",
        {
            "kind": "csharp",
            "title": "Modellazione DTO Immutabile con Record",
            "prompt": "Dichiara il record `public record UserProfile(int Id, string Email, string Role)` e la classe statica `UserManager` con il metodo `PromoteToAdmin(UserProfile user)` che restituisce una nuova istanza con `Role = \"Admin\"` usando l'espressione `with`.",
            "starter": """// TODO: Definisci il record UserProfile(int Id, string Email, string Role)

public static class UserManager {
    public static UserProfile PromoteToAdmin(UserProfile user) {
        // TODO: Restituisci la copia modificata con Role = "Admin" usando `with`
        return user;
    }
}""",
            "solution": """public record UserProfile(int Id, string Email, string Role);

public static class UserManager {
    public static UserProfile PromoteToAdmin(UserProfile user) => user with { Role = "Admin" };
}""",
            "tests": [
                {"name": "Promozione ad Admin", "expression": 'UserManager.PromoteToAdmin(new UserProfile(1, "user@test.it", "User")).Role', "expected": "Admin"},
                {"name": "Mantiene Id intatto", "expression": 'UserManager.PromoteToAdmin(new UserProfile(42, "admin@test.it", "User")).Id', "expected": 42},
            ],
            "hints": [
                "Definisci il record prima della classe: `public record UserProfile(int Id, string Email, string Role);`.",
                "Nei record puoi creare copie modificate con la parola chiave `with`: `user with { Role = \"Admin\" }`.",
                "La nuova istanza conserverà `Id` ed `Email` invariati."
            ],
            "creative_goals": ["Usa la sintassi `with` per la mutazione non distruttiva", "Usa un costruttore primario sintetico posizionale"],
            "bonus_xp": 20
        }
    ),
    (
        "01_csharp", "Collezioni moderne: List, Dictionary e Array", 40, True,
        "Scegliere e manipolare strutture dati fondamentali in memoria in base alle operazioni richieste.",
        "list;dictionary;array;lookup;indice;capacita;collezione generica",
        "Un Dictionary usa una chiave per trovare un valore. La ricerca ha costo medio vicino a O(1), mentre cercare in una List richiede in genere di esaminare gli elementi fino alla corrispondenza. Sono stime: la scelta dipende da come userai i dati.",
        """### Principali Collezioni in C#:
1. **`T[]` (Array)**: Dimensione fissa allocata in memoria contigua. Minimo overhead, ideale quando il numero di elementi è noto a priori.
2. **`List<T>`**: Lista a dimensione dinamica. Permette `.Add()`, `.Remove()`, `.Insert()`. Internamente si ridimensiona automaticamente.
3. **`Dictionary<TKey, TValue>`**: Mappa chiave-valore basata su tabella hash. La ricerca ha costo medio vicino a $O(1)$; non è una garanzia per ogni caso.
   - Per accedere in sicurezza senza eccezioni si usa `TryGetValue`:
   ```csharp
   if (dict.TryGetValue(key, out var val)) { ... }
   ```

### Collection Expressions (C# 12):
Da C# 12 puoi inizializzare array, liste e insiemi con la sintassi uniforme a parentesi quadre:
```csharp
List<int> numbers = [1, 2, 3, 4];
string[] names = ["Anna", "Luca"];
```""",
        "var subjects = new List<string> { \"Mario\", \"Anna\", \"Paolo\" };\nvar lookup = new Dictionary<int, string> { [1] = \"Mario\", [2] = \"Anna\" };\nif (lookup.TryGetValue(1, out var found)) {\n    Console.WriteLine(found);\n}",
        """public static class CacheStore {
    private static readonly Dictionary<string, int> _items = new();
    public static void Set(string key, int value) => _items[key] = value;
    public static int GetOrDefault(string key, int fallback = 0) => _items.TryGetValue(key, out var v) ? v : fallback;
}""",
        "Accedere a una chiave inesistente di un dizionario con l'indicizzatore anziché `TryGetValue`; usare array a dimensione fissa quando serve aggiungere elementi dinamicamente.",
        "In quale scenario un Dictionary è preferibile rispetto a una List per la ricerca di elementi?",
        {
            "kind": "csharp",
            "title": "Lookup Veloce con Dictionary",
            "prompt": "Implementa la classe `InventoryTracker` con i metodi `AddStock(string item, int qty)` che aggiorna (sommando) o inserisce la quantità dell'articolo restituendo la nuova quantità totale, e `GetStock(string item)` che restituisce la quantità o 0 se l'articolo non esiste.",
            "starter": """using System.Collections.Generic;

public class InventoryTracker {
    private readonly Dictionary<string, int> _stock = new();

    public int AddStock(string item, int qty) {
        // TODO: Se l'articolo esiste somma qty, altrimenti impostalo. Restituisci il nuovo totale.
        return 0;
    }

    public int GetStock(string item) {
        // TODO: Restituisci la quantità oppure 0 se non presente
        return 0;
    }
}""",
            "solution": """using System.Collections.Generic;

public class InventoryTracker {
    private readonly Dictionary<string, int> _stock = new();

    public int AddStock(string item, int qty) {
        if (_stock.TryGetValue(item, out var current)) {
            _stock[item] = current + qty;
        } else {
            _stock[item] = qty;
        }
        return _stock[item];
    }

    public int GetStock(string item) => _stock.TryGetValue(item, out var qty) ? qty : 0;
}""",
            "tests": [
                {"name": "Articolo non presente restituisce 0", "expression": "(new InventoryTracker()).GetStock(\"Keyboard\")", "expected": 0},
                {"name": "Aggiunta e lettura articolo", "expression": "(new InventoryTracker()).AddStock(\"Mouse\", 5)", "expected": 5},
                {"name": "Somma cumulativa su stesso articolo", "expression": "new System.Func<int>(() => { var t = new InventoryTracker(); t.AddStock(\"Mouse\", 5); return t.AddStock(\"Mouse\", 3); })()", "expected": 8},
            ],
            "hints": [
                "Usa `_stock.TryGetValue(item, out var current)` per controllare se l'articolo è già memorizzato.",
                "Se presente, scrivi `_stock[item] = current + qty;`, altrimenti `_stock[item] = qty;`.",
                "Nel metodo `GetStock`, puoi usare l'operatore ternario per restituire `qty` oppure `0`."
            ],
            "creative_goals": ["Usa `TryGetValue` per evitare doppie scansioni", "Mantieni lo stato incapsulato con un campo privato `readonly`"],
            "bonus_xp": 20
        }
    ),
    (
        "01_csharp", "LINQ fondamentale: Where, Select e Aggregazioni", 50, True,
        "Interrogare e trasformare collezioni con sintassi dichiarativa LINQ e deferred execution.",
        "linq;where;select;orderby;firstordefault;tolist;deferred execution",
        "La query LINQ non viene eseguita nel momento in cui viene definita, ma solo quando i risultati vengono effettivamente enumerati (ad esempio con un foreach, un ToList() o un'aggregazione).",
        """### Leggere una lambda
`n => n % 2 == 0` è una funzione breve: riceve `n` e restituisce un booleano. `Where` la chiama per ogni elemento e conserva quelli per cui il risultato è true. In `Select(n => n * 2)` la funzione restituisce invece il nuovo valore. Il tipo del parametro è inferito dalla collezione.

### I Metodi LINQ Più Utilizzati:
- **`Where(predicate)`**: Filtra gli elementi che soddisfano la condizione booleana.
- **`Select(selector)`**: Mappa e trasforma ciascun elemento (proiezione).
- **`OrderBy(key)` / `OrderByDescending(key)`**: Ordina gli elementi.
- **`FirstOrDefault(predicate)`**: Restituisce il primo elemento che corrisponde o il valore di default (`null` per tipi riferimento, `0` per numeri). Non lancia eccezioni se la sequenza è vuota!
- **`Count()` / `Sum()` / `Average()`**: Aggregazioni matematiche immediate.
- **`ToList()` / `ToArray()`**: Materializza la sequenza differita in una collezione in memoria.

```csharp
using System.Linq;

var activeUsers = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => u.Email)
    .ToList();
```""",
        "var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };\nvar evensDoubled = numbers\n    .Where(n => n % 2 == 0)\n    .Select(n => n * 2)\n    .ToList();",
        """using System.Linq;
using System.Collections.Generic;

public static class OrderAnalytics {
    public static decimal GetTotalHighValue(IEnumerable<decimal> orders, decimal threshold) =>
        orders.Where(o => o >= threshold).Sum();
}""",
        "Dimenticare che LINQ usa la valutazione ritardata (deferred execution) e richiamare query multiple senza materializzarle; usare First() invece di FirstOrDefault() provocando crash se vuoto.",
        "Che cosa si intende per esecuzione differita (deferred execution) in LINQ?",
        {
            "kind": "csharp",
            "title": "Filtro e Aggregazione LINQ",
            "prompt": "Implementa `OrderAnalytics.GetTotalHighValue(IEnumerable<decimal> orders, decimal threshold)` che calcola e restituisce la somma di tutti gli importi maggiori o uguali alla soglia `threshold`.",
            "starter": """using System.Collections.Generic;
using System.Linq;

public static class OrderAnalytics {
    /// <summary>
    /// Restituisce la somma degli ordini con importo >= threshold.
    /// </summary>
    public static decimal GetTotalHighValue(IEnumerable<decimal> orders, decimal threshold) {
        // TODO: Usa i metodi LINQ Where e Sum
        return 0m;
    }
}""",
            "solution": """using System.Collections.Generic;
using System.Linq;

public static class OrderAnalytics {
    public static decimal GetTotalHighValue(IEnumerable<decimal> orders, decimal threshold) =>
        orders?.Where(o => o >= threshold).Sum() ?? 0m;
}""",
            "tests": [
                {"name": "Filtra ordini sopra 100", "expression": "OrderAnalytics.GetTotalHighValue(new decimal[] { 50m, 120m, 30m, 200m }, 100m)", "expected": 320},
                {"name": "Nessun ordine sopra soglia restituisce 0", "expression": "OrderAnalytics.GetTotalHighValue(new decimal[] { 10m, 20m }, 100m)", "expected": 0},
            ],
            "hints": [
                "Assicurati di includere la clausola `using System.Linq;`.",
                "Concatena i metodi LINQ: `orders.Where(o => o >= threshold).Sum()`.",
                "Puoi scrivere l'intero metodo in una riga usando `=>`."
            ],
            "creative_goals": ["Gestisci il caso di collezione nulla con null-conditional `?.`", "Usa la sintassi fluente concisa"],
            "bonus_xp": 20
        }
    ),
    (
        "01_csharp", "Programmazione Asincrona: Task, async/await ed Eccezioni", 50, True,
        "Gestire operazioni I/O senza bloccare il thread del server e trattare gli errori con robustezza.",
        "task;async;await;try catch;cancellation token;non bloccante;thread pool",
        "Durante una vera attesa I/O asincrona, `await` sospende il metodo senza bloccare il thread in attesa. Il codice dopo `await` riprende quando il `Task` termina; chiamare `.Result` o `.Wait()` blocca invece il chiamante.",
        """### Anatomia del Modello Asincrono in C#:
1. **`async Task<T>`**: indica un metodo asincrono che restituirà un valore di tipo `T`.
2. **`await`**: sospende il metodo fino al completamento del Task; per operazioni I/O asincrone non tiene un thread occupato solo per aspettare.
3. **`try / catch / finally`**: intercetta eventuali eccezioni sollevate durante l'operazione asincrona.

```csharp
public class DataFetcher(HttpClient client) {
  public async Task<string> DownloadContentAsync(string url, CancellationToken ct) {
    try {
        return await client.GetStringAsync(url, ct);
    } catch (HttpRequestException ex) {
        throw new InvalidOperationException("Impossibile scaricare il contenuto.", ex);
    }
  }
}
```

In un'app ASP.NET Core configura il client con `IHttpClientFactory` e iniettalo, invece di creare un nuovo `HttpClient` per ogni richiesta.

Nei flussi asincroni usa `await` fino al chiamante. `.Result` e `.Wait()` bloccano il thread: sotto carico possono esaurire il thread pool. Il deadlock dipende dal contesto di sincronizzazione; ASP.NET Core non usa quello delle vecchie applicazioni ASP.NET.""",
        "public async Task<string> FetchDataAsync(int id, CancellationToken ct = default)\n{\n    try {\n        await Task.Delay(50, ct);\n        return $\"Dati per {id}\";\n    } catch (Exception ex) {\n        Console.Error.WriteLine(ex.Message);\n        throw;\n    }\n}",
        """using System.Threading.Tasks;

public static class AsyncDataService {
    public static async Task<string> GetUserGreetingAsync(string name) {
        await Task.Delay(10);
        return $"Benvenuto, {name}!";
    }
}""",
        "Usare `.Result` o `.Wait()` che possono causare deadlock bloccando il thread; usare `async void` anziché `async Task` (consentito solo per eventi UI).",
        "Perché `async/await` è fondamentale per la scalabilità di un server web come ASP.NET Core?",
        {
            "kind": "csharp",
            "title": "Metodo Asincrono con Task",
            "prompt": "Implementa il metodo asincrono `AsyncDataService.ComputeAsync(int a, int b)` che attende `Task.Delay(10)` e restituisce la somma dei due numeri.",
            "starter": """using System.Threading.Tasks;

public static class AsyncDataService {
    /// <summary>
    /// Esegue una simulazione asincrona e restituisce la somma.
    /// </summary>
    public static async Task<int> ComputeAsync(int a, int b) {
        // TODO: attendi Task.Delay(10) e restituisci a + b
        return 0;
    }
}""",
            "solution": """using System.Threading.Tasks;

public static class AsyncDataService {
    public static async Task<int> ComputeAsync(int a, int b) {
        await Task.Delay(10);
        return a + b;
    }
}""",
            "tests": [
                {"name": "Calcolo asincrono somma 15 + 25", "expression": "AsyncDataService.ComputeAsync(15, 25).GetAwaiter().GetResult()", "expected": 40},
                {"name": "Calcolo con numeri negativi", "expression": "AsyncDataService.ComputeAsync(-5, 10).GetAwaiter().GetResult()", "expected": 5},
            ],
            "hints": [
                "Usa la parola chiave `await` prima di `Task.Delay(10);`.",
                "Dopo il delay, scrivi semplicemente `return a + b;`.",
                "La firma del metodo deve contenere `async Task<int>`."
            ],
            "creative_goals": ["Usa `await` in modo non bloccante", "Fornisci documentazione XML del Task restituito"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 02: TypeScript & Contratti per il Web
    # ==========================================
    (
        "00_fondamenti", "TypeScript di base: variabili, funzioni e array", 40, True,
        "Scrivere una funzione TypeScript tipizzata e seguire un ciclo su una lista di numeri.",
        "const;let;parametro;tipo restituito;number;array;for",
        "TypeScript aggiunge tipi controllati alla sintassi di JavaScript. Una funzione riceve valori, lavora su di essi e restituisce un risultato; un array raccoglie più valori dello stesso tipo.",
        """### Una variabile, una funzione e una lista
- Usa `const` quando il nome non verrà riassegnato; usa `let` quando il valore della variabile cambierà.
- Dopo il nome del parametro, `: number[]` dichiara un array di numeri.
- Dopo le parentesi della funzione, `: number` dichiara il tipo restituito.
- Un `for...of` legge un elemento alla volta. `total += value` aggiunge il valore al totale corrente.

I tipi sono controllati da TypeScript durante la compilazione; non trasformano né validano automaticamente dati JSON ricevuti a runtime.""",
        """const initialValues: number[] = [2, 3];

export function sum(values: number[]): number {
    let total = 0;
    for (const value of values) {
        total += value;
    }
    return total;
}

console.log(sum(initialValues)); // 5""",
        """export function countNames(names: string[]): number {
    let count = 0;
    for (const name of names) {
        if (name.trim().length > 0) count += 1;
    }
    return count;
}""",
        "Usare `=` al posto di `===` in una condizione; dimenticare che gli array vuoti non contengono valori da sommare; confondere il tipo statico con la validazione dei dati esterni.",
        "Quali informazioni forniscono i tipi `number[]` e `: number` in una funzione?",
        {
            "kind": "typescript",
            "title": "Somma di un array",
            "prompt": "Implementa `export function sum(values: number[]): number` con un ciclo `for...of`. Restituisci la somma dei valori e `0` quando l'array è vuoto.",
            "starter": "export function sum(values: number[]): number {\n    let total = 0;\n    // TODO: aggiungi ciascun valore a total\n    return total;\n}",
            "solution": "export function sum(values: number[]): number {\n    let total = 0;\n    for (const value of values) {\n        total += value;\n    }\n    return total;\n}",
            "tests": [
                {"name": "Somma due valori", "expression": "sum([2, 3])", "expected": 5},
                {"name": "Array vuoto restituisce zero", "expression": "sum([])", "expected": 0},
                {"name": "Somma valori negativi", "expression": "sum([-2, 5])", "expected": 3}
            ],
            "hints": ["`total` parte da zero.", "Usa `for (const value of values)` per leggere ogni elemento.", "All'interno del ciclo aggiorna `total` con `total + value`."],
            "creative_goals": [],
            "xp": 20,
            "bonus_xp": 0
        }
    ),
    (
        "02_typescript", "Tipi primitivi, Any vs Unknown e Type Inference", 35, True,
        "Sviluppare con tipi statici robusti evitando `any` e sfruttando l'inferenza di TypeScript.",
        "typescript;primitivi;any;unknown;type inference;type assertion",
        "L'inferenza di tipi permette a TypeScript di dedurre automaticamente il tipo di una variabile dal valore assegnato, rendendo il codice leggibile senza sacrificare la sicurezza.",
        """### Differenza Cruciale tra `any` e `unknown`:
- **`any`**: disattiva molti controlli statici su quel valore; un'operazione non valida può quindi emergere solo a runtime.
- **`unknown`**: indica un tipo sconosciuto ma sicuro. TypeScript costringe a effettuare un controllo a runtime (type narrowing con `typeof` o `instanceof`) prima di poter interagire con il valore.

```typescript
let input: unknown = "testo";
if (typeof input === "string") {
    console.log(input.toUpperCase()); // Il controllo typeof restringe il tipo in questo ramo.
}
```""",
        "let age = 30; // Inferito come number\nlet rawData: unknown = JSON.parse('{\"id\":1}');\nif (typeof rawData === 'object' && rawData !== null) {\n  console.log('Oggetto valido');\n}",
        """export function safeStringLength(value: unknown): number {
    if (typeof value === "string") {
        return value.length;
    }
    return 0;
}""",
        "Usare `any` per silenziare i messaggi del compilatore; dimenticare che `unknown` richiede un type guard.",
        "Quale controllo richiede unknown prima di usare un valore, e che cosa consente invece any?",
        {
            "kind": "typescript",
            "title": "Type Guard con Unknown",
            "prompt": "Definisci la funzione `export function safeUpperCase(value: unknown): string` che restituisce la stringa in maiuscolo se `value` è di tipo stringa, altrimenti restituisce una stringa vuota `\"\"`. Non usare mai `any`.",
            "starter": """// TODO: Implementa safeUpperCase senza usare any
export function safeUpperCase(value: unknown): string {
    return "";
}""",
            "solution": """export function safeUpperCase(value: unknown): string {
    if (typeof value === "string") {
        return value.toUpperCase();
    }
    return "";
}""",
            "tests": [
                {"name": "Una stringa viene convertita in maiuscolo", "expression": 'safeUpperCase("Angular")', "expected": "ANGULAR"},
                {"name": "Un numero produce stringa vuota", "expression": "safeUpperCase(42)", "expected": ""},
                {"name": "Un valore nullo produce stringa vuota", "expression": "safeUpperCase(null)", "expected": ""},
                {"name": "Firma tipizzata senza any", "mode": "regex", "value": "safeUpperCase\\s*\\(value:\\s*unknown\\):\\s*string"},
                {"name": "Nessun any utilizzato", "mode": "not_contains", "value": "any"},
            ],
            "hints": [
                "Usa `if (typeof value === \"string\")` per effettuare il type narrowing.",
                "All'interno del blocco `if`, TypeScript riconosce automaticamente `value` come stringa e consente `.toUpperCase()`.",
                "Al di fuori dell'if, restituisci `\"\"`."
            ],
            "creative_goals": ["Usa typeof per il type narrowing", "Assenza totale di `any`"],
            "bonus_xp": 15
        }
    ),
    (
        "02_typescript", "Interfacce vs Type Alias e Contratti di Dati", 40, True,
        "Modellare contratti di dati coerenti tra client Angular e DTO del backend .NET.",
        "interface;type alias;extends;readonly;optional;contratto dati",
        "Interfacce e type alias descrivono gli oggetti attesi e aiutano il compilatore a rilevare campi e tipi incoerenti. Non verificano i dati ricevuti a runtime: un JSON esterno può violare il contratto e richiedere validazione.",
        """### `interface` vs `type`:
- **`interface`**: ideale per descrivere la forma di oggetti e dati DTO. Supporta l'estensione con `extends` e la dichiarazione incrementale.
- **`type`**: ideale per unioni, tuple, tipi primitivi o tipi composti.

```typescript
export interface UserDto {
    readonly id: number;      // Immutabile dopo la creazione
    name: string;
    email: string;
    phoneNumber?: string;     // Proprietà opzionale con ?
}

export type UserRole = "Admin" | "Manager" | "Guest";
```""",
        "export interface UserDto {\n  readonly id: number;\n  name: string;\n  role?: string;\n}\n\nexport type Status = 'active' | 'inactive';",
        """export interface ApiResponse<T> {
    success: boolean;
    data: T;
    timestamp: string;
}""",
        "Creare interfacce con proprietà senza tipo esplicito; non sincronizzare i nomi dei campi tra backend C# e interfaccia TS.",
        "Qual è la differenza pratica tra una proprietà obbligatoria e una opzionale in un'interfaccia?",
        {'kind': 'typescript',
 'title': 'Interfaccia DTO per Risposta API',
 'prompt': "Definisci l'interfaccia `export interface ProductDto` con i campi: `readonly id: number`, "
           '`title: string`, `price: decimal` (in TS: `number`) e la proprietà opzionale `description?: '
           'string`. Assicurati che non contenga `any`. Il controllo è strutturale: riconosce le '
           'dichiarazioni richieste, ma non sostituisce tsc. Nel laboratorio Modelli TypeScript e Contratti '
           'Web verifica anche la compilazione.',
 'starter': "// TODO: Definisci qui l'interfaccia ProductDto\n"
            'export interface ProductDto {\n'
            '    // Aggiungi qui i campi richiesti\n'
            '}',
 'solution': 'export interface ProductDto {\n'
             '    readonly id: number;\n'
             '    title: string;\n'
             '    price: number;\n'
             '    description?: string;\n'
             '}',
 'tests': [{'name': 'Interfaccia esportata',
            'mode': 'regex',
            'value': 'export\\s+interface\\s+ProductDto\\b'},
           {'name': 'Identificativo numerico readonly',
            'mode': 'regex',
            'value': 'readonly\\s+id\\s*:\\s*number\\b'},
           {'name': 'Titolo testuale', 'mode': 'regex', 'value': 'title\\s*:\\s*string\\b'},
           {'name': 'Prezzo numerico', 'mode': 'regex', 'value': 'price\\s*:\\s*number\\b'},
           {'name': 'Descrizione opzionale testuale',
            'mode': 'regex',
            'value': 'description\\s*\\?\\s*:\\s*string\\b'},
           {'name': 'Nessun any', 'mode': 'not_contains', 'value': 'any'}],
 'hints': ['Usa la parola chiave `readonly` prima di `id: number`.',
           'I numeri in TypeScript usano il tipo `number` sia per interi che decimali.',
           'Aggiungi `?` dopo `description` per renderla opzionale: `description?: string;`.'],
 'creative_goals': ['Imposta id come readonly', 'Rendi description opzionale con ?'],
 'bonus_xp': 15}
    ),
    (
        "02_typescript", "Union Discriminate e Type Narrowing", 45, True,
        "Gestire stati complessi (caricamento, successo, errore) con union discriminate eleganti e sicure.",
        "discriminated union;tag;switch;type narrowing;exhaustive check;never",
        "Una union discriminata usa una proprietà comune (tag) per distinguere quale variante del tipo è presente, permettendo al compilatore di restringere il tipo automaticamente.",
        """### Esempio di Union Discriminata per Stato di Caricamento:
```typescript
export type RequestState<T> =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: T }
    | { status: "error"; message: string };

function renderState<T>(state: RequestState<T>): string {
    switch (state.status) {
        case "idle": return "In attesa";
        case "loading": return "Caricamento in corso...";
        case "success": return `Caricato: ${JSON.stringify(state.data)}`;
        case "error": return `Errore: ${state.message}`;
    }
}
```
All'interno di ogni ramo del `switch`, TypeScript sa esattamente quali proprietà esistono (es. `data` esiste solo in `success`!).""",
        "export type State =\n  | { status: 'loading' }\n  | { status: 'success'; data: string[] }\n  | { status: 'error'; message: string };",
        """export type AuthState =
    | { authenticated: true; user: string }
    | { authenticated: false; reason: string };""",
        "Usare flag booleani multipli come `isLoading: boolean; isError: boolean; isSuccess: boolean` che possono generare stati impossibili.",
        "Perché una union discriminata evita bug rispetto a molteplici flag booleani indipendenti?",
        {'kind': 'typescript',
 'title': 'Union Discriminata per Risultato Operazione',
 'prompt': 'Definisci il type `export type OperationResult<T>` come union discriminata con due varianti: `{ '
           'success: true; data: T }` e `{ success: false; error: string }`. Il controllo è strutturale: '
           'riconosce le dichiarazioni richieste, ma non sostituisce tsc. Nel laboratorio Modelli TypeScript '
           'e Contratti Web verifica anche la compilazione.',
 'starter': '// TODO: Definisci la union discriminata OperationResult<T>\n'
            'export type OperationResult<T> =\n'
            '    | { success: true; /* ... */ }\n'
            '    | { success: false; /* ... */ };',
 'solution': 'export type OperationResult<T> =\n'
             '    | { success: true; data: T }\n'
             '    | { success: false; error: string };',
 'tests': [{'name': 'Dichiarazione type OperationResult',
            'mode': 'regex',
            'value': 'type\\s+OperationResult\\s*<\\s*T\\s*>'},
           {'name': 'Variante success: true', 'mode': 'regex', 'value': '\\bsuccess\\s*:\\s*true\\b'},
           {'name': 'Variante success: false', 'mode': 'regex', 'value': '\\bsuccess\\s*:\\s*false\\b'},
           {'name': 'Dato presente solo nel successo', 'mode': 'regex', 'value': '\\bdata\\s*:\\s*T\\b'},
           {'name': "Messaggio presente solo nell'errore",
            'mode': 'regex',
            'value': '\\berror\\s*:\\s*string\\b'},
           {'name': 'Nessun any', 'mode': 'not_contains', 'value': 'any'}],
 'hints': ['Il campo discriminante comune è `success: true` nel primo caso e `success: false` nel secondo.',
           "Associa `data: T` al successo ed `error: string` all'insuccesso.",
           'Usa il pipe `|` tra le due definizioni di oggetto.'],
 'creative_goals': ['Usa il generico <T> per il payload',
                    'Evita stati inconsistenti con il campo tag boolean'],
 'bonus_xp': 15}
    ),
    (
        "02_typescript", "Generics essenziali per Collezioni e Risposte API", 45, True,
        "Creare interfacce e funzioni riutilizzabili con parametri di tipo generici.",
        "generics;type parameter;t;vincoli extends;api response;paginazione",
        "I generics consentono di scrivere componenti, servizi e modelli che operano su tipi diversi pur mantenendo la garanzia di sicurezza statica del compilatore.",
        """### Modello Generico per Risposte Paginate:
```typescript
export interface PaginatedList<T> {
    items: T[];
    pageNumber: number;
    pageSize: number;
    totalCount: number;
}
```
Possiamo ora riutilizzare `PaginatedList<UserDto>`, `PaginatedList<OrderDto>`, ecc., senza duplicare codice!

### Vincoli con `extends`:
```typescript
export interface HasId { id: number; }

export function findById<T extends HasId>(list: T[], id: number): T | undefined {
    return list.find(item => item.id === id);
}
```""",
        "export interface PaginatedResponse<T> {\n  items: T[];\n  total: number;\n}\n\nexport function wrapData<T>(data: T): { payload: T } {\n  return { payload: data };\n}",
        """export interface ApiResponseEnvelope<T> {
    data: T;
    status: number;
    success: boolean;
}""",
        "Scrivere codice duplicato per ogni modello invece di usare un wrapper generico; usare generics complessi non necessari.",
        "Cosa significa il parametro `<T>` nella dichiarazione di una funzione o interfaccia?",
        {'kind': 'typescript',
 'title': 'Busta di Risposta Generica API',
 'prompt': "Definisci l'interfaccia generica `export interface ApiResponseEnvelope<T>` con i campi: `data: "
           'T`, `status: number`, e `success: boolean`. Il controllo è strutturale: riconosce le '
           'dichiarazioni richieste, ma non sostituisce tsc. Nel laboratorio Modelli TypeScript e Contratti '
           'Web verifica anche la compilazione.',
 'starter': "// TODO: Definisci qui l'interfaccia generica ApiResponseEnvelope<T>\n"
            'export interface ApiResponseEnvelope<T> {\n'
            '    // aggiungi i campi data, status e success\n'
            '}',
 'solution': 'export interface ApiResponseEnvelope<T> {\n'
             '    data: T;\n'
             '    status: number;\n'
             '    success: boolean;\n'
             '}',
 'tests': [{'name': 'Dichiarazione interfaccia generica ApiResponseEnvelope<T>',
            'mode': 'regex',
            'value': 'interface\\s+ApiResponseEnvelope\\s*<\\s*T\\s*>'},
           {'name': 'Campo data: T', 'mode': 'regex', 'value': '\\bdata\\s*:\\s*T\\b'},
           {'name': 'Campo status: number', 'mode': 'regex', 'value': '\\bstatus\\s*:\\s*number\\b'},
           {'name': 'Nessun any', 'mode': 'not_contains', 'value': 'any'},
           {'name': 'Campo success booleano', 'mode': 'regex', 'value': 'success\\s*:\\s*boolean\\b'}],
 'hints': ["Dichiara `<T>` subito dopo il nome dell'interfaccia: `export interface ApiResponseEnvelope<T>`.",
           'Il campo `data` deve avere come tipo il parametro generico `T`.',
           'Non usare `any`.'],
 'creative_goals': ['Parametro generico T pulito', 'Interfaccia pienamente esportabile'],
 'bonus_xp': 15}
    ),

    # ==========================================
    # MODULO 03: Web API con ASP.NET Core
    # ==========================================
    (
        "03_aspnet_api", "Minimal API da zero: Program.cs e WebApplication", 40, True,
        "Creare endpoint RESTful con Minimal API in C# e .NET 10.",
        "minimal api;webapplication;mapget;mappost;program.cs;status codes;typedresults",
        "Minimal API permette di dichiarare endpoint HTTP con poco codice di contorno. Controller e Minimal API sono entrambi adatti a progetti reali; la sintassi scelta, da sola, non determina il throughput dell'applicazione.",
        """### Anatomia di un'applicazione Minimal API in Program.cs:
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/api/health", () => Results.Ok(new { status = "Healthy" }));
app.MapGet("/api/users/{id:int}", (int id) => Results.Ok(new { Id = id }));
app.Run();
```""",
        "var builder = WebApplication.CreateBuilder(args);\nvar app = builder.Build();\napp.MapGet(\"/api/hello\", () => Results.Ok(new { message = \"Ciao da .NET!\" }));\napp.Run();",
        """public static class RouteRegistry {
    public static string HealthCheck() => "Healthy";
    public static int GetStatusCode(bool success) => success ? 200 : 400;
}""",
        "Confondere la registrazione dei servizi (`builder.Services`) con la configurazione della pipeline (`app.Use...`); pensare che Minimal API o TypedResults siano obbligatori per ogni progetto.",
        "Quali criteri, oltre alla quantità di codice, useresti per scegliere tra Minimal API e Controller?",
        {
            "kind": "csharp",
            "title": "Registro Risposte Endpoint",
            "prompt": "Implementa `RouteRegistry.GetApiResponse(bool isOk, string message)` che restituisce una stringa formattata `\"200: {message}\"` se isOk è true, oppure `\"400: {message}\"` se false.",
            "starter": """public static class RouteRegistry {
    /// <summary>
    /// Restituisce la risposta HTTP formattata con status code e messaggio.
    /// </summary>
    public static string GetApiResponse(bool isOk, string message) {
        // TODO: restituisci "200: {message}" o "400: {message}"
        return "";
    }
}""",
            "solution": """public static class RouteRegistry {
    public static string GetApiResponse(bool isOk, string message) =>
        isOk ? $"200: {message}" : $"400: {message}";
}""",
            "tests": [
                {"name": "Risposta di successo 200", "expression": 'RouteRegistry.GetApiResponse(true, "Operazione completata")', "expected": "200: Operazione completata"},
                {"name": "Risposta di errore 400", "expression": 'RouteRegistry.GetApiResponse(false, "Dati non validi")', "expected": "400: Dati non validi"},
            ],
            "hints": [
                "Usa l'operatore ternario: `isOk ? ... : ...`.",
                "Interpola il messaggio con `$\"200: {message}\"`.",
                "Puoi scrivere il metodo con espressione sintetica `=>`."
            ],
            "creative_goals": ["Usa l'operatore ternario con interpolazione", "Fornisci documentazione XML del metodo"],
            "bonus_xp": 20
        }
    ),
    (
        "03_aspnet_api", "Dependency Injection: Transient, Scoped e Singleton", 45, True,
        "Conoscere i tre cicli di vita del contenitore DI di ASP.NET Core e scegliere in base alla condivisione e alla durata delle dipendenze.",
        "dependency injection;ioc container;transient;scoped;singleton;disposable",
        "La Dependency Injection disaccoppia le classi fornendo le dipendenze richieste dall'esterno, facilitando il testing e la gestione del ciclo di vita degli oggetti.",
        """### I Tre Lifetimes di ASP.NET Core:
1. **`Transient` (`AddTransient<TService, TImpl>()`)**:
   - Viene creata una nuova istanza ogni volta che il servizio viene richiesto.
   - Ideale per servizi leggeri e stateless.
2. **`Scoped` (`AddScoped<TService, TImpl>()`)**:
   - Viene creata una sola istanza per ogni scope di servizio; nelle Web API, di solito lo scope coincide con una richiesta HTTP.
   - `AddDbContext` registra normalmente `DbContext` come scoped. Questo allinea la durata del contesto alla richiesta, ma non avvia da solo una transazione che copra più chiamate a `SaveChanges`.
3. **`Singleton` (`AddSingleton<TService, TImpl>()`)**:
   - Viene creata un'unica istanza condivisa per l'intera durata dell'applicazione.
   - Ideale per cache in memoria, logger o servizi di background thread-safe.""",
        "builder.Services.AddSingleton<ICache, MemoryCache>();\nbuilder.Services.AddScoped<IUserRepository, UserRepository>();\nbuilder.Services.AddTransient<IEmailSender, EmailSender>();",
        """public interface ICounterService { int Next(); }
public class CounterService : ICounterService {
    private int _count = 0;
    public int Next() => ++_count;
}""",
        "Iniettare un servizio Scoped (come il DbContext) dentro un Singleton senza creare e gestire uno scope esplicito: il servizio conserva una dipendenza più breve del proprio lifetime.",
        "Perché `DbContext` ha normalmente durata Scoped in una Web API, e che cosa non garantisce questo lifetime?",
        {
            "kind": "csharp",
            "title": "Implementazione Servizio per Dependency Injection",
            "prompt": "Definisci l'interfaccia `public interface IIdGenerator { string Generate(); }` e la classe `public class GuidIdGenerator : IIdGenerator` che implementa il metodo restituendo un nuovo GUID formattato come stringa.",
            "starter": """// TODO: Definisci l'interfaccia IIdGenerator
public interface IIdGenerator {
    string Generate();
}

// TODO: Implementa GuidIdGenerator
public class GuidIdGenerator : IIdGenerator {
    public string Generate() {
        // restituisci un nuovo GUID in formato stringa
        return "";
    }
}""",
            "solution": """using System;

public interface IIdGenerator {
    string Generate();
}

public class GuidIdGenerator : IIdGenerator {
    public string Generate() => Guid.NewGuid().ToString("N");
}""",
            "tests": [
                {"name": "Generazione ID non vuoto", "expression": "(new GuidIdGenerator()).Generate().Length > 0", "expected": True},
                {"name": "Istanza implementa interfaccia", "expression": "new GuidIdGenerator() is IIdGenerator", "expected": True},
            ],
            "hints": [
                "Usa `Guid.NewGuid().ToString()` per generare un identificatore univoco.",
                "Fai ereditare la classe dall'interfaccia: `public class GuidIdGenerator : IIdGenerator`.",
                "Puoi usare la formattazione `\"N\"` per un GUID pulito senza trattini."
            ],
            "creative_goals": ["Usa expression-bodied member per Generate()", "Assicura il polimorfismo con l'interfaccia"],
            "bonus_xp": 20
        }
    ),
    (
        "03_aspnet_api", "Routing, Parametri e Binding di Record DTO", 45, True,
        "Raccogliere dati da route, query string, header e body JSON mappandoli in record C#.",
        "routing;route parameters;query string;request body;dto;frombody;fromquery",
        "ASP.NET Core associa automaticamente i dati della richiesta HTTP ai parametri della lambda o dell'action tramite model binding trasparente.",
        """### Origini di Binding in Minimal API:
- **Route param**: `app.MapGet("/items/{id:int}", (int id) => ...)`
- **Query param**: `app.MapGet("/items", (string? search) => ...)`
- **Body JSON**: `app.MapPost("/items", (CreateItemDto dto) => ...)`
- **Servizi DI**: `app.MapGet("/items", (IItemService service) => ...)`

```csharp
public record CreateUserRequest(string Email, string Name);
public record UserResponse(int Id, string Email, string Name);

app.MapPost("/api/users", (CreateUserRequest req) => {
    var user = new UserResponse(1, req.Email, req.Name);
    return Results.Created($"/api/users/{user.Id}", user);
});
```""",
        "app.MapGet(\"/api/products/{id:int}\", (int id, string? category) => {\n    return Results.Ok(new { id, category });\n});",
        """public record CreateProductDto(string Name, decimal Price);
public static class ProductValidator {
    public static bool IsValid(CreateProductDto dto) =>
        !string.IsNullOrWhiteSpace(dto.Name) && dto.Price > 0;
}""",
        "Dimenticare di definire vincoli di rotta (`{id:int}`) consentendo l'invio di stringhe arbitrarie; non validare i campi del DTO.",
        "In che modo Minimal API distingue se un parametro deve essere letto dalla rotta, dalla query string o dal body JSON?",
        {
            "kind": "csharp",
            "title": "Validatore e Binding DTO",
            "prompt": "Dichiara il record `public record CreateProductDto(string Name, decimal Price)` e il metodo `ProductValidator.IsValid(CreateProductDto? dto)` che restituisce true solo se il DTO non è nullo, Name non è vuoto e Price è strettamente maggiore di zero.",
            "starter": """// TODO: Definisci il record CreateProductDto(string Name, decimal Price)

public static class ProductValidator {
    public static bool IsValid(CreateProductDto? dto) {
        // TODO: Verifica che dto non sia null, Name non vuoto e Price > 0
        return false;
    }
}""",
            "solution": """public record CreateProductDto(string Name, decimal Price);

public static class ProductValidator {
    public static bool IsValid(CreateProductDto? dto) {
        if (dto is null) return false;
        return !string.IsNullOrWhiteSpace(dto.Name) && dto.Price > 0m;
    }
}""",
            "tests": [
                {"name": "Prodotto valido", "expression": 'ProductValidator.IsValid(new CreateProductDto("Monitor", 199.99m))', "expected": True},
                {"name": "Prezzo negativo non valido", "expression": 'ProductValidator.IsValid(new CreateProductDto("Monitor", -10m))', "expected": False},
                {"name": "Nome vuoto non valido", "expression": 'ProductValidator.IsValid(new CreateProductDto("  ", 50m))', "expected": False},
                {"name": "DTO nullo non valido", "expression": "ProductValidator.IsValid(null)", "expected": False},
            ],
            "hints": [
                "Controlla prima che `dto` non sia nullo: `if (dto is null) return false;`.",
                "Usa `!string.IsNullOrWhiteSpace(dto.Name)` per verificare il nome.",
                "Verifica che `dto.Price > 0m`."
            ],
            "creative_goals": ["Pattern matching `dto is not null`", "Validazione esaustiva dei campi"],
            "bonus_xp": 20
        }
    ),
    (
        "03_aspnet_api", "Validazione degli input e ProblemDetails standard", 40, True,
        "Restituire errori semantici in formato Problem Details (RFC 9457) e mostrare gli errori per campo nel frontend Angular.",
        "problemdetails;rfc 9457;validazione;bad request;400",
        "Lo standard ProblemDetails standardizza il formato JSON di errore per le API web, consentendo al frontend Angular di mostrare messaggi precisi per ciascun campo non valido.",
        """### Struttura di una risposta Problem Details (RFC 9457):
```json
{
  "type": "about:blank",
  "title": "Richiesta non valida",
  "status": 400,
  "errors": {
    "Email": ["Il campo Email non è un indirizzo valido."],
    "Age": ["L'età minima deve essere 18 anni."]
  }
}
```

### Utilizzo in Minimal API con `Results.ValidationProblem`:
```csharp
var errors = new Dictionary<string, string[]>();
if (string.IsNullOrWhiteSpace(user.Email)) {
    errors["Email"] = ["L'email è obbligatoria."];
}
if (errors.Count > 0) {
    return Results.ValidationProblem(errors);
}
return Results.Ok();
```""",
        "var errors = new Dictionary<string, string[]>();\nif (string.IsNullOrWhiteSpace(input.Email)) {\n    errors[\"Email\"] = new[] { \"L'email è obbligatoria.\" };\n    return Results.ValidationProblem(errors);\n}",
        """using System.Collections.Generic;

public static class ValidationHelper {
    public static Dictionary<string, string[]> ValidateEmail(string? email) {
        var errors = new Dictionary<string, string[]>();
        if (string.IsNullOrWhiteSpace(email) || !email.Contains("@")) {
            errors["Email"] = new[] { "Formato email non valido" };
        }
        return errors;
    }
}""",
        "Restituire semplici stringhe di testo grezzo in caso di errore invece di una risposta strutturata JSON; usare status code 200 con messaggi di fallimento nel body.",
        "Quale vantaggio offre ValidationProblem al client che deve mostrare errori per campo?",
        {
            "kind": "csharp",
            "title": "Generatore Errori ProblemDetails",
            "prompt": "Implementa `ValidationHelper.ValidateUser(string? username, int age)` che restituisce un `Dictionary<string, string[]>` di errori: aggiunge chiave \"Username\" con messaggio \"Username obbligatorio\" se vuoto, e chiave \"Age\" con messaggio \"Età non valida\" se age < 18.",
            "starter": """using System.Collections.Generic;

public static class ValidationHelper {
    public static Dictionary<string, string[]> ValidateUser(string? username, int age) {
        var errors = new Dictionary<string, string[]>();
        // TODO: Aggiungi gli errori se username è vuoto o age < 18
        return errors;
    }
}""",
            "solution": """using System.Collections.Generic;

public static class ValidationHelper {
    public static Dictionary<string, string[]> ValidateUser(string? username, int age) {
        var errors = new Dictionary<string, string[]>();
        if (string.IsNullOrWhiteSpace(username)) {
            errors["Username"] = new[] { "Username obbligatorio" };
        }
        if (age < 18) {
            errors["Age"] = new[] { "Età non valida" };
        }
        return errors;
    }
}""",
            "tests": [
                {"name": "Utente valido senza errori", "expression": 'ValidationHelper.ValidateUser("Mario", 25).Count', "expected": 0},
                {"name": "Username mancante genera errore", "expression": 'ValidationHelper.ValidateUser("", 25).ContainsKey("Username")', "expected": True},
                {"name": "Età minore di 18 genera errore", "expression": 'ValidationHelper.ValidateUser("Mario", 16).ContainsKey("Age")', "expected": True},
            ],
            "hints": [
                "Inizializza `var errors = new Dictionary<string, string[]>();`.",
                "Se `string.IsNullOrWhiteSpace(username)` è true, imposta `errors[\"Username\"] = new[] { \"Username obbligatorio\" };`.",
                "Se `age < 18`, imposta `errors[\"Age\"] = new[] { \"Età non valida\" };`."
            ],
            "creative_goals": ["Dizionario Problem Details RFC 9457", "Verifiche multiple isolate"],
            "bonus_xp": 20
        }
    ),
    (
        "03_aspnet_api", "Gestione globale delle eccezioni e Logging strutturato", 40, True,
        "Intercettare crash imprevisti e produrre log strutturati con ILogger.",
        "eccezioni globali;useexceptionhandler;ilogger;serilog;problem details 500;telemetria",
        "Una gestione centralizzata delle eccezioni impedisce la fuga di dettagli sensibili di implementazione (stack trace) verso il client, registrando i dettagli nei log del server.",
        """### Middleware Globale per le Eccezioni:
In ASP.NET Core 10 `UseExceptionHandler()` può restituire un Problem Details con status code 500:
```csharp
app.UseExceptionHandler(exceptionHandlerApp => {
    exceptionHandlerApp.Run(async context => {
        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        context.Response.ContentType = "application/problem+json";
        var problem = new {
            Type = "https://tools.ietf.org/html/rfc7231#section-6.6.1",
            Title = "Si è verificato un errore interno.",
            Status = 500
        };
        await context.Response.WriteAsJsonAsync(problem);
    });
});
```

### Logging Strutturato:
Evita la concatenazione di stringhe nei log; usa i segnaposto nominati per permettere a tool come Seq o Elastic di indicizzare i parametri:
```csharp
logger.LogInformation("Ordine {OrderId} creato con successo per l'utente {UserId}", orderId, userId);
```""",
        "app.UseExceptionHandler(\"/error\");\nlogger.LogInformation(\"Elaborazione richiesta per utente {UserId}\", userId);",
        """public static class LogMessageFormatter {
    public static string FormatError(string operation, string error) =>
        $"[ERROR] Operazione '{operation}' fallita: {error}";
}""",
        "Mostrare lo stack trace C# grezzo al browser in ambiente di produzione (grave falla di sicurezza); usare string interpolation in ILogger perdendo la struttura dei dati.",
        "Perché non si deve mai mostrare il messaggio completo di un'eccezione interna nel client Angular?",
        {
            "kind": "csharp",
            "title": "Sanitizzazione Messaggi di Errore",
            "prompt": "Implementa `LogMessageFormatter.SanitizeForClient(string rawException, bool isDevelopment)` che restituisce `rawException` se `isDevelopment` è true, altrimenti restituisce un messaggio opaco e sicuro: `\"Si è verificato un errore interno del server.\"`. ",
            "starter": """public static class LogMessageFormatter {
    /// <summary>
    /// Maschera i dettagli dell'eccezione in produzione per motivi di sicurezza.
    /// </summary>
    public static string SanitizeForClient(string rawException, bool isDevelopment) {
        // TODO: restituisci rawException in dev, altrimenti messaggio generico
        return "";
    }
}""",
            "solution": """public static class LogMessageFormatter {
    public static string SanitizeForClient(string rawException, bool isDevelopment) =>
        isDevelopment ? rawException : "Si è verificato un errore interno del server.";
}""",
            "tests": [
                {"name": "In Development mostra il messaggio reale", "expression": 'LogMessageFormatter.SanitizeForClient("NullReferenceException at line 42", true)', "expected": "NullReferenceException at line 42"},
                {"name": "In Production maschera l'errore", "expression": 'LogMessageFormatter.SanitizeForClient("SqlException: Database offline", false)', "expected": "Si è verificato un errore interno del server."},
            ],
            "hints": [
                "Usa l'operatore ternario: `isDevelopment ? rawException : ...`.",
                "In produzione restituisci la stringa esatta `\"Si è verificato un errore interno del server.\"`.",
                "Questo impedisce ai malintenzionati di conoscere la struttura del database o dei file interni."
            ],
            "creative_goals": ["Usa expression-bodied member sintetico", "Garantisci la protezione da information disclosure"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 04: Angular Moderno: Standalone & Control Flow
    # ==========================================
    (
        "00_fondamenti", "HTML essenziale e CSS per leggere i template Angular", 40, True,
        "Riconoscere struttura semantica, label dei campi e regole CSS essenziali prima di usare template Angular.",
        "html;elemento;attributo;label;id;classe css;focus;template",
        "Un template Angular usa elementi HTML. Gli elementi descrivono la struttura; gli attributi danno informazioni o collegano il template al componente. CSS definisce l'aspetto senza cambiare il significato del documento.",
        """### Struttura HTML di una schermata
- `<main>` racchiude il contenuto principale della pagina.
- `<label for=\"email\">` collega il testo visibile al controllo che ha `id=\"email\"`.
- `type=\"email\"` comunica il tipo di dato al browser; non sostituisce la validazione server.
- `<button type=\"button\">` non invia un form per errore. Per inviare un modulo si usa `type=\"submit\"`.

### Una regola CSS
```css
.page { max-width: 40rem; margin-inline: auto; padding: 1rem; }
button:focus-visible { outline: 3px solid currentColor; }
```
La classe `.page` seleziona gli elementi con `class=\"page\"`; `:focus-visible` mantiene visibile l'indicatore quando si naviga da tastiera.""",
        """<main class=\"page\">
  <h1>Profilo</h1>
  <form>
    <label for=\"email\">Email</label>
    <input id=\"email\" name=\"email\" type=\"email\" required>
    <button type=\"submit\">Salva</button>
  </form>
</main>""",
        """.page { max-width: 40rem; margin-inline: auto; padding: 1rem; }
input, button { font: inherit; }
button:focus-visible { outline: 3px solid currentColor; }""",
        "Associare il testo del campo alla relativa `id`; usare un elemento soltanto per il suo aspetto invece che per il suo significato; rimuovere l'indicatore di focus da tastiera.",
        "Quale coppia collega una label a un campo, e perché il CSS non sostituisce la struttura semantica?",
        {
            "kind": "html",
            "title": "Modulo HTML accessibile",
            "prompt": "Completa un modulo dentro `<main>` con un titolo, una label collegata tramite `for`/`id` a un campo email obbligatorio e un pulsante di invio.",
            "starter": "<main>\n  <!-- TODO: titolo e form -->\n</main>",
            "solution": "<main>\n  <h1>Contatto</h1>\n  <form>\n    <label for=\"email\">Email</label>\n    <input id=\"email\" name=\"email\" type=\"email\" required>\n    <button type=\"submit\">Invia</button>\n  </form>\n</main>",
            "tests": [
                {"name": "Contenuto principale presente", "mode": "tag", "value": "main"},
                {"name": "Titolo di primo livello presente", "mode": "tag", "value": "h1"},
                {"name": "Label collegata al campo email", "mode": "label_for", "value": "email"},
                {"name": "Campo email obbligatorio", "mode": "attribute", "value": "input:required"},
                {"name": "Invio esplicito del modulo", "mode": "regex", "value": "<button[^>]*type=\\\"submit\\\""}
            ],
            "hints": ["Apri e chiudi gli elementi: `<main>`, `<h1>` e `<form>`.", "Il valore di `for` sulla label deve essere uguale all'`id` dell'input.", "Usa `type=\"email\" required` e `type=\"submit\"`."],
            "creative_goals": [],
            "xp": 20,
            "bonus_xp": 0
        }
    ),
    (
        "04_angular_core", "Progetto Angular Standalone e Bootstrap applicazione", 35, True,
        "Avviare un'applicazione Angular moderna senza NgModule usando bootstrapApplication.",
        "standalone;bootstrapapplication;main.ts;appconfig;providehttpclient;provide-router",
        "Nei nuovi progetti Angular i componenti standalone sono il modello predefinito e dichiarano direttamente le dipendenze del template. NgModule resta supportato: standalone evita di doverlo usare in molti casi, ma non lo elimina dal framework.",
        """### Bootstrap di un'applicazione Standalone (in `main.ts`):
```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));
```

### Configurazione Servizi Globali (in `app.config.ts`):
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient()
  ]
};
```""",
        "bootstrapApplication(AppComponent, {\n  providers: [provideHttpClient(), provideRouter(routes)]\n});",
        """export class AppBootstrapStatus {
    isReady = signal(false);
    init() { this.isReady.set(true); }
}""",
        "Cercare di dichiarare un componente Standalone dentro le `declarations` di un NgModule; dimenticare `provideHttpClient()` nel bootstrap.",
        "Quale responsabilità dichiara un componente standalone nel proprio decoratore `@Component`?",
        {
            "kind": "angular",
            "title": "Stato di Inizializzazione Applicazione",
            "prompt": "Implementa `AppBootstrapStatus` con un segnale `isReady = signal(false)` e il metodo `initialize()` che imposta il segnale su `true`.",
            "starter": """export class AppBootstrapStatus {
    isReady = signal(false);

    initialize() {
        // TODO: imposta isReady su true
    }
}""",
            "solution": """export class AppBootstrapStatus {
    isReady = signal(false);

    initialize() {
        this.isReady.set(true);
    }
}""",
            "tests": [
                {"name": "Stato iniziale false", "expression": "(new AppBootstrapStatus()).isReady()", "expected": False},
                {"name": "Chiamata initialize() imposta true", "expression": "(() => { const s = new AppBootstrapStatus(); s.initialize(); return s.isReady(); })()", "expected": True},
            ],
            "hints": [
                "Per impostare un nuovo valore in un segnale, usa `.set(nuovoValore)`.",
                "All'interno della classe usa `this.isReady.set(true);`.",
                "I segnali si leggono invocandoli come funzioni: `this.isReady()`."
            ],
            "creative_goals": ["Usa il metodo `.set()` dei Signals", "Incapsula la mutazione dello stato"],
            "bonus_xp": 20
        }
    ),
    (
        "04_angular_core", "Creazione di componenti Standalone con @Component", 40, True,
        "Definire componenti Standalone con decoratore @Component, imports espliciti e stili isolati.",
        "standalone: true;imports;template;styles;selettore;incapsulamento",
        "Un componente Standalone dichiara nel proprio decoratore quali componenti, pipe o direttive usa. Le dipendenze esplicite rendono più chiari il template e il contesto di test.",
        """### Anatomia del decoratore @Component:
```typescript
import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="card">
      <h3>{{ username() }}</h3>
    </div>
  `,
  styles: [`
    .card { padding: 1rem; border-radius: 8px; border: 1px solid #ccc; }
  `]
})
export class UserCardComponent {
  username = signal('Mario Rossi');
}
```""",
        "@Component({\n  selector: 'app-card',\n  standalone: true,\n  template: `<h3>{{ title() }}</h3>`\n})\nexport class CardComponent { title = signal('Titolo'); }",
        """export class UserProfileComponent {
    name = signal('Ospite');
    setName(newName: string) { this.name.set(newName); }
}""",
        "Dimenticare di inserire i componenti figli nell'array `imports` del decoratore `@Component`; usare selettori generici che collidono con tag HTML standard.",
        "Cosa accade se utilizzi un componente figlio nel template senza averlo aggiunto nell'array `imports`?",
        {
            "kind": "angular",
            "title": "Gestore Profilo Componente",
            "prompt": "Crea la classe `UserProfileComponent` con un segnale `name = signal('Ospite')` e il metodo `setName(newName: string)` che aggiorna il segnale solo se `newName` non è vuoto.",
            "starter": """export class UserProfileComponent {
    name = signal("Ospite");

    setName(newName: string) {
        // TODO: aggiorna il segnale con newName se non è vuoto
    }
}""",
            "solution": """export class UserProfileComponent {
    name = signal("Ospite");

    setName(newName: string) {
        if (newName && newName.trim().length > 0) {
            this.name.set(newName.trim());
        }
    }
}""",
            "tests": [
                {"name": "Nome iniziale Ospite", "expression": "(new UserProfileComponent()).name()", "expected": "Ospite"},
                {"name": "Aggiornamento nome valido", "expression": "(() => { const c = new UserProfileComponent(); c.setName('Luigi'); return c.name(); })()", "expected": "Luigi"},
                {"name": "Nome vuoto viene ignorato", "expression": "(() => { const c = new UserProfileComponent(); c.setName('   '); return c.name(); })()", "expected": "Ospite"},
            ],
            "hints": [
                "Controlla che `newName` sia definito e contenga caratteri utili con `newName.trim().length > 0`.",
                "Aggiorna il valore con `this.name.set(newName.trim());`.",
                "Se la stringa è vuota, non modificare il segnale."
            ],
            "creative_goals": ["Pulisci gli spazi bianchi con .trim()", "Previeni sovrascritture accidentali con stringhe vuote"],
            "bonus_xp": 20
        }
    ),
    ('04_angular_core',
 'Nuovo Control Flow: @if, @else, @for e @switch',
 45,
 True,
 'Confrontare il Control Flow integrato (`@if`, `@for`, `@switch`) con le direttive strutturali più datate.',
 '@if;@else;@for;track;@empty;@switch;@case;nuovo control flow',
 'Il Control Flow integrato (`@if`, `@for`, `@switch`) è disponibile da Angular 17. Usa blocchi leggibili nel '
 "template e non richiede CommonModule per queste istruzioni; l'effetto sulle prestazioni dipende "
 "dall'applicazione e dal lavoro svolto.",
 '### Sintassi del Nuovo Control Flow nei Template:\n'
 '\n'
 '#### 1. Condizionale `@if / @else`:\n'
 '```html\n'
 '@if (isLoggedIn()) {\n'
 '  <p>Benvenuto, {{ username() }}!</p>\n'
 '} @else {\n'
 '  <button (click)="login()">Accedi</button>\n'
 '}\n'
 '```\n'
 '\n'
 '#### 2. Ciclo `@for` (con `track` obbligatorio e `@empty`):\n'
 '```html\n'
 '<ul>\n'
 '  @for (user of users(); track user.id) {\n'
 '    <li>{{ user.name }}</li>\n'
 '  } @empty {\n'
 '    <li>Nessun utente registrato.</li>\n'
 '  }\n'
 '</ul>\n'
 '```\n'
 '> `track` è obbligatorio e descrive come associare gli elementi della lista alle viste. Usa un identificatore '
 'stabile se gli elementi possono cambiare o riordinarsi; `track $index` è adatto soprattutto a liste statiche. '
 'Questo aiuta Angular a riutilizzare le viste correttamente, senza garantire un numero minimo di aggiornamenti '
 'in ogni situazione.\n'
 '\n'
 '### Scegliere una vista con `@switch`\n'
 '```html\n'
 '@switch (status) {\n'
 '  @case (\'loading\') { <p role="status">Caricamento…</p> }\n'
 '  @case (\'error\') { <p role="alert">Caricamento fallito</p> }\n'
 '  @default { <p>Pronto</p> }\n'
 '}\n'
 '```\n'
 "`status` è una proprietà della classe del componente, per esempio `status = 'loading'`. Se diventa un Signal, "
 'nel template leggilo con `status()`. Ogni caso mostra la propria vista; non serve `break`.',
 '@if (users().length > 0) {\n'
 '  @for (user of users(); track user.id) {\n'
 '    <div>{{ user.name }}</div>\n'
 '  }\n'
 '} @else {\n'
 '  <p>Lista vuota</p>\n'
 '}',
 'export class UserListManager {\n'
 '    users = signal<{ id: number; name: string }[]>([]);\n'
 '    addUser(id: number, name: string) {\n'
 '        this.users.update(list => [...list, { id, name }]);\n'
 '    }\n'
 '}',
 'Dimenticare la clausola `track` in `@for` (provoca errore del compilatore Angular); usare `track $index` quando '
 'gli elementi hanno un ID stabile.',
 'Perché la clausola `track` è obbligatoria nel nuovo blocco `@for`?',
 {'kind': 'angular',
  'title': 'Gestione Lista Utenti con Signals',
  'prompt': 'Implementa `UserListManager` con un segnale `users` inizializzato come array vuoto di `{ id: number; '
            "name: string }`, il metodo `addUser(id: number, name: string)` che aggiunge l'elemento in modo "
            'immutabile, e `count` come computed che restituisce la lunghezza della lista.',
  'starter': 'export class UserListManager {\n'
             '    users = signal<{ id: number; name: string }[]>([]);\n'
             '    // TODO: definisci count con computed()\n'
             '\n'
             '    addUser(id: number, name: string) {\n'
             "        // TODO: aggiungi l'elemento alla lista usando .update() in modo immutabile\n"
             '    }\n'
             '}',
  'solution': 'export class UserListManager {\n'
              '    users = signal<{ id: number; name: string }[]>([]);\n'
              '    count = computed(() => this.users().length);\n'
              '\n'
              '    addUser(id: number, name: string) {\n'
              '        this.users.update(current => [...current, { id, name }]);\n'
              '    }\n'
              '}',
  'tests': [{'name': 'Conteggio iniziale zero', 'expression': '(new UserListManager()).count()', 'expected': 0},
            {'name': 'Aggiunta utente aggiorna lista',
             'expression': "(() => { const m = new UserListManager(); m.addUser(1, 'Mario'); return m.count(); "
                           '})()',
             'expected': 1},
            {'name': 'Dato utente inserito correttamente',
             'expression': "(() => { const m = new UserListManager(); m.addUser(1, 'Mario'); return "
                           'm.users()[0].name; })()',
             'expected': 'Mario'}],
  'hints': ['Usa `computed(() => this.users().length)` per calcolare il totale in modo reattivo.',
            "Per aggiungere elementi preservando l'immutabilità, usa `this.users.update(list => [...list, { id, "
            'name }]);`.',
            "Non usare mai `.push()` diretto sull'array interno, per non rompere la reattività."],
  'creative_goals': ['Aggiunta immutabile con spread operator `[...list]`', 'Proprietà derivata con `computed()`'],
  'bonus_xp': 20}),
    (
        "04_angular_core", "Data Binding moderno: interpolazione, property ed event binding", 40, True,
        "Connettere classe e template con interpolazione `{{ }}`, property binding `[prop]` ed event binding `(event)`.",
        "interpolazione;property binding;event binding;two way binding;signal call",
        "Il data binding permette lo scambio continuo di dati e interazioni tra l'interfaccia HTML nel browser e la classe TypeScript del componente.",
        """### Le 3 Forme Fondamentali di Binding:
1. **Interpolazione `{{ espressione }}`**:
   - Inserisce testo dinamico nel DOM: `<h1>{{ title() }}</h1>`.
   - Con i Signals si invoca il segnale con le parentesi tonde `()`!
2. **Property Binding `[proprieta]="espressione"`**:
   - Collega un valore a una proprietà del DOM o a un input di un componente figlio:
     `<button [disabled]="isSubmitting()">Invia</button>`.
3. **Event Binding `(evento)="gestore()"`**:
   - Intercetta azioni dell'utente (click, input, submit):
     `<button (click)="increment()">Aggiungi</button>`.

```html
<input [value]="query()" (input)="onSearch($event)" />
<p>Risultati per: {{ query() }}</p>
```""",
        "<button [disabled]=\"!isValid()\" (click)=\"onSubmit()\">Salva</button>\n<input [value]=\"searchTerm()\" (input)=\"updateSearch($event)\" />",
        """export class SearchBarComponent {
    query = signal('');
    setQuery(text: string) { this.query.set(text.trim()); }
    clear() { this.query.set(''); }
}""",
        "Dimenticare le parentesi tonde quando si legge un segnale nel template (`{{ name }}` invece di `{{ name() }}`); usare property binding quando serve event binding.",
        "Perché quando si legge un Signal in un template Angular bisogna includere le parentesi tonde `()`?",
        {
            "kind": "angular",
            "title": "Stato Barra di Ricerca Reattiva",
            "prompt": "Implementa `SearchBarComponent` con il segnale `query = signal('')`, `hasQuery` come `computed` booleano che indica se la query non è vuota, `setQuery(text: string)` che aggiorna il segnale pulendo gli spazi, e `clear()` che lo azzera.",
            "starter": """export class SearchBarComponent {
    query = signal("");
    // TODO: definisci hasQuery con computed() che verifica se query non è vuota

    setQuery(text: string) {
        // TODO: aggiorna query con text.trim()
    }

    clear() {
        // TODO: azzera la query
    }
}""",
            "solution": """export class SearchBarComponent {
    query = signal("");
    hasQuery = computed(() => this.query().length > 0);

    setQuery(text: string) {
        this.query.set((text ?? "").trim());
    }

    clear() {
        this.query.set("");
    }
}""",
            "tests": [
                {"name": "Query iniziale vuota", "expression": "(new SearchBarComponent()).hasQuery()", "expected": False},
                {"name": "setQuery aggiorna hasQuery su true", "expression": "(() => { const s = new SearchBarComponent(); s.setQuery('angular'); return s.hasQuery(); })()", "expected": True},
                {"name": "clear() riporta hasQuery su false", "expression": "(() => { const s = new SearchBarComponent(); s.setQuery('angular'); s.clear(); return s.hasQuery(); })()", "expected": False},
            ],
            "hints": [
                "Usa `computed(() => this.query().length > 0)` per calcolare `hasQuery`.",
                "Nel metodo `setQuery`, usa `this.query.set(text.trim());`.",
                "Nel metodo `clear`, azzera con `this.query.set('');`."
            ],
            "creative_goals": ["Usa computed per la visibilità derivata", "Gestisci input nulli con fallback sicuro"],
            "bonus_xp": 20
        }
    ),
    (
        "04_angular_core", "Deferrable Views: ottimizzazione con @defer", 40, True,
        "Rinviare il caricamento di componenti pesanti nel browser con la direttiva nativa @defer.",
        "@defer;@placeholder;@loading;@error;lazy loading template;on viewport",
        "Le Deferrable Views possono caricare alcune dipendenze solo quando una condizione è soddisfatta. Il beneficio sul codice iniziale dipende dai componenti e dalle altre importazioni dell'app.",
        """### Sintassi dei Blocchi @defer:
```html
@defer (on viewport) {
  <app-heavy-chart [data]="chartData()" />
} @placeholder {
  <div class="skeleton">In attesa che il grafico diventi visibile...</div>
} @loading (minimum 300ms) {
  <div class="spinner">Caricamento grafico in corso...</div>
} @error {
  <div class="alert">Impossibile caricare il componente grafico.</div>
}
```

### Trigger comuni:
- `on viewport`: carica quando l'elemento entra nella schermata visibile (usando IntersectionObserver).
- `on interaction`: carica quando l'utente clicca o tocca l'area.
- `on hover`: carica al passaggio del mouse.
- `when condizione()`: carica in base al valore booleano di un Signal.""",
        "@defer (on viewport) {\n  <app-metrics-chart />\n} @placeholder {\n  <div>Caricamento al rendering...</div>\n}",
        """export class DeferSimulator {
    isLoaded = signal(false);
    triggerLoad() { this.isLoaded.set(true); }
}""",
        "Dimenticare di fornire un `@placeholder` lasciando uno spazio vuoto che causa salti di layout (Cumulative Layout Shift); usare `@defer` per componenti critici 'above the fold'.",
        "Quale problema risolve il blocco `@placeholder` all'interno di una Deferrable View?",
        {
            "kind": "angular",
            "title": "Simulatore di Caricamento Differito",
            "prompt": "Implementa `DeferSimulator` con un segnale `isLoaded = signal(false)` e il metodo `triggerLoad()` che attiva il caricamento impostandolo su true.",
            "starter": """export class DeferSimulator {
    isLoaded = signal(false);

    triggerLoad() {
        // TODO: imposta isLoaded su true
    }
}""",
            "solution": """export class DeferSimulator {
    isLoaded = signal(false);

    triggerLoad() {
        this.isLoaded.set(true);
    }
}""",
            "tests": [
                {"name": "Stato iniziale differito", "expression": "(new DeferSimulator()).isLoaded()", "expected": False},
                {"name": "Trigger attiva caricamento", "expression": "(() => { const s = new DeferSimulator(); s.triggerLoad(); return s.isLoaded(); })()", "expected": True},
            ],
            "hints": [
                "Usa `this.isLoaded.set(true);`.",
                "Questo simula l'attivazione del blocco `@defer` in base a una condizione reattiva.",
                "I Signals comunicano immediatamente il cambio di stato a tutto il template."
            ],
            "creative_goals": ["Utilizzo idiomatico di .set()", "Design minimalista e performante"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 05: Reattività con Angular Signals & State
    # ==========================================
    (
        "05_angular_signals", "Introduzione a signal() e aggiornamento stato con set() e update()", 40, True,
        "Creare e gestire variabili reattive con il modello a segnali di Angular.",
        "signal;set;update;asreadonly;reattivita fine grained;zone.js",
        "Un Signal contiene un valore leggibile e aggiornabile. Quando un template legge quel Signal, Angular registra la dipendenza e programma il controllo della vista interessata dopo un aggiornamento. Il Signal non garantisce che venga ridisegnata soltanto una singola riga: il lavoro dipende dalle dipendenze e dalla strategia di change detection.",
        """### Operazioni Fondamentali sui Signals:
1. **Creazione**:
   `count = signal(0);`
2. **Lettura (Getter)**:
   `const current = this.count();` (si invoca come una funzione senza argomenti)
3. **Sostituzione con `.set(value)`**:
   `this.count.set(10);` (imposta direttamente un nuovo valore)
4. **Aggiornamento basato sul valore precedente con `.update(fn)`**:
   `this.count.update(prev => prev + 1);` (ideale per incrementi, aggiunte a liste)
5. **Esposizione in sola lettura con `.asReadonly()`**:
   `readonlyCount = this.count.asReadonly();` (impedisce a chi riceve il Signal di chiamare `.set()` o `.update()`; non rende profondamente immutabile un oggetto contenuto).

Angular 22 usa il change detection zoneless per i nuovi progetti. I Signals sono uno dei modi con cui il framework riceve una notifica di aggiornamento; non sono loro a rimuovere `zone.js`. `computed()` è adatto ai valori derivati, mentre `effect()` serve soprattutto a sincronizzare effetti esterni e non a duplicare stato.""",
        "const count = signal(0);\ncount.set(5);\ncount.update(n => n + 1);\nconsole.log(count()); // 6",
        """export class CounterComponent {
    count = signal(0);
    increment() { this.count.update(n => n + 1); }
    decrement() { this.count.update(n => Math.max(0, n - 1)); }
    reset() { this.count.set(0); }
}""",
        "Tentare di riassegnare il segnale con l'uguale (`this.count = 5` invece di `this.count.set(5)`); dimenticare di invocarlo con le parentesi `this.count()`; mutare in-place un array contenuto nel Signal.",
        "Qual è la differenza fondamentale tra `.set()` e `.update()` su un Signal?",
        {
            "kind": "angular",
            "title": "Contatore Reattivo con Protezione Valori Negativi",
            "prompt": "Implementa `CounterComponent` con il segnale `count = signal(0)`, i metodi `increment()`, `decrement()` (che non deve mai scendere sotto 0), e `reset()` che riporta il conteggio a 0.",
            "starter": """export class CounterComponent {
    count = signal(0);

    increment() {
        // TODO: incrementa count di 1
    }

    decrement() {
        // TODO: decrementa count senza scendere sotto 0
    }

    reset() {
        // TODO: azzera count
    }
}""",
            "solution": """export class CounterComponent {
    count = signal(0);

    increment() {
        this.count.update(n => n + 1);
    }

    decrement() {
        this.count.update(n => Math.max(0, n - 1));
    }

    reset() {
        this.count.set(0);
    }
}""",
            "tests": [
                {"name": "Valore iniziale zero", "expression": "(new CounterComponent()).count()", "expected": 0},
                {"name": "Incremento a 1", "expression": "(() => { const c = new CounterComponent(); c.increment(); return c.count(); })()", "expected": 1},
                {"name": "Decremento non scende sotto zero", "expression": "(() => { const c = new CounterComponent(); c.decrement(); return c.count(); })()", "expected": 0},
                {"name": "Reset azzera il conteggio", "expression": "(() => { const c = new CounterComponent(); c.increment(); c.increment(); c.reset(); return c.count(); })()", "expected": 0},
            ],
            "hints": [
                "Usa `this.count.update(n => n + 1);` per incrementare.",
                "Per il decremento sicuro: `this.count.update(n => Math.max(0, n - 1));`.",
                "Per il reset: `this.count.set(0);`."
            ],
            "creative_goals": ["Usa Math.max per proteggere da valori negativi", "Usa .update con arrow functions pure"],
            "bonus_xp": 20
        }
    ),
    (
        "05_angular_signals", "Valori derivati intelligenti con computed()", 45, True,
        "Creare segnali dipendenti che si ricalcolano automaticamente e memorizzano il risultato.",
        "computed;derivazione di stato;memoization;funzione pura;dipendenze dinamiche",
        "`computed()` crea un valore derivato in sola lettura. Angular memorizza il calcolo e aggiorna le dipendenze in base ai Signals letti durante l'ultima esecuzione; la funzione viene valutata quando il valore serve.",
        """### Caratteristiche di `computed()`:
1. **Memoization**: `computed()` calcola il valore quando serve e riusa il risultato finché le dipendenze lette non cambiano.
2. **Sola lettura**: un segnale `computed` non espone `.set()` o `.update()`; modifica i segnali sorgente e lascia derivare il valore.
3. **Dipendenze dinamiche**: Angular tiene conto dei Signals letti durante l'ultima esecuzione della funzione. Mantieni il calcolo puro: non aggiornare stato e non avviare richieste al suo interno.

```typescript
const price = signal(100);
const taxRate = signal(0.22);
const totalPrice = computed(() => price() * (1 + taxRate()));
```""",
        "const items = signal([10, 20, 30]);\nconst total = computed(() => items().reduce((a, b) => a + b, 0));\nconst isFreeShipping = computed(() => total() >= 50);",
        """export class CartStore {
    items = signal<{ price: number; quantity: number }[]>([]);
    total = computed(() => this.items().reduce((sum, item) => sum + item.price * item.quantity, 0));
    hasItems = computed(() => this.items().length > 0);
}""",
        "Inserire effetti collaterali (chiamate HTTP, manipolazione manuale del DOM) dentro una funzione `computed()` (deve essere rigorosamente pura!).",
        "Perché una funzione passata a `computed()` deve essere rigorosamente pura e priva di side-effect?",
        {
            "kind": "angular",
            "title": "Store Carrello con Totale Derivato",
            "prompt": "Implementa `CartStore` con il segnale `items = signal<{ name: string; price: number }[]>([])`, la proprietà `total` calcolata con `computed()` (somma dei prezzi), e il metodo `addItem(name: string, price: number)` che aggiunge l'articolo in modo immutabile.",
            "starter": """export class CartStore {
    items = signal<{ name: string; price: number }[]>([]);
    // TODO: definisci total con computed()

    addItem(name: string, price: number) {
        // TODO: aggiungi l'articolo usando .update()
    }
}""",
            "solution": """export class CartStore {
    items = signal<{ name: string; price: number }[]>([]);
    total = computed(() => this.items().reduce((sum, item) => sum + item.price, 0));

    addItem(name: string, price: number) {
        this.items.update(list => [...list, { name, price }]);
    }
}""",
            "tests": [
                {"name": "Totale iniziale zero", "expression": "(new CartStore()).total()", "expected": 0},
                {"name": "Aggiunta singolo articolo aggiorna totale", "expression": "(() => { const s = new CartStore(); s.addItem('Libro', 25); return s.total(); })()", "expected": 25},
                {"name": "Aggiunta multipla calcola somma corretta", "expression": "(() => { const s = new CartStore(); s.addItem('Libro', 25); s.addItem('Penna', 5); return s.total(); })()", "expected": 30},
            ],
            "hints": [
                "Usa `computed(() => this.items().reduce((acc, curr) => acc + curr.price, 0))` per calcolare la somma.",
                "In `addItem`, usa `this.items.update(list => [...list, { name, price }]);`.",
                "Assicurati che la funzione di riduzione parta da `0`."
            ],
            "creative_goals": ["Usa reduce() per l'aggregazione numerica", "Aggiunta immutabile con spread operator"],
            "bonus_xp": 20
        }
    ),
    (
        "05_angular_signals", "Effetti collaterali controllati con effect()", 40, True,
        "Eseguire operazioni esterne (localStorage, logging, sincronizzazione) in risposta a cambi di stato.",
        "effect;side effect;cleanup;localstorage;injection context;oncleanup",
        "La funzione `effect()` esegue codice esterno quando cambiano i Signals letti al suo interno. Può sincronizzare il browser storage o registrare log; per derivare valori è preferibile `computed()`.",
        """### Regole e Uso Corretto di `effect()`:
1. **Injection Context**: `effect()` deve essere chiamato all'interno del costruttore del componente o come inizializzatore di proprietà.
2. **Tracciamento automatico**: Angular traccia automaticamente tutti i segnali letti dentro l'effetto:
```typescript
import { Component, effect, signal } from '@angular/core';

@Component({ selector: 'app-theme', template: '' })
export class ThemeComponent {
  darkMode = signal(false);

  constructor() {
    effect(() => {
      // Si riesegue ogni volta che darkMode() cambia!
      localStorage.setItem('theme', this.darkMode() ? 'dark' : 'light');
    });
  }
}
```

In Angular 22 scrivere Signals dentro un effect è consentito; `allowSignalWrites` è deprecato e non serve ([riferimento Angular](https://angular.dev/api/core/CreateEffectOptions)). Il rischio di cicli rimane: per calcolare uno stato a partire da altro stato preferisci `computed()`. Usa effect per sincronizzare una risorsa esterna, prevedendo la pulizia quando necessario.""",
        "effect(() => {\n  console.log('Nuovo tema selezionato:', theme());\n});",
        """export class ThemeManager {
    isDark = signal(false);
    themeName = computed(() => this.isDark() ? 'dark' : 'light');
    toggle() { this.isDark.update(v => !v); }
}""",
        "Usare `effect()` per derivare nuovo stato (per questo scopo si DEVE usare `computed()`); creare loop di aggiornamenti infiniti.",
        "Qual è la differenza concettuale fondamentale tra un `computed()` e un `effect()`?",
        {
            "kind": "angular",
            "title": "Gestore Temi con Proprietà Derivata",
            "prompt": "Implementa `ThemeManager` con il segnale `isDark = signal(false)`, la proprietà `themeName` calcolata con `computed()` che restituisce \"dark\" se isDark è true altrimenti \"light\", e il metodo `toggle()` che inverte il valore.",
            "starter": """export class ThemeManager {
    isDark = signal(false);
    // TODO: definisci themeName con computed()

    toggle() {
        // TODO: inverti il segnale isDark
    }
}""",
            "solution": """export class ThemeManager {
    isDark = signal(false);
    themeName = computed(() => this.isDark() ? "dark" : "light");

    toggle() {
        this.isDark.update(v => !v);
    }
}""",
            "tests": [
                {"name": "Tema iniziale light", "expression": "(new ThemeManager()).themeName()", "expected": "light"},
                {"name": "Toggle attiva tema dark", "expression": "(() => { const t = new ThemeManager(); t.toggle(); return t.themeName(); })()", "expected": "dark"},
                {"name": "Secondo toggle ritorna a light", "expression": "(() => { const t = new ThemeManager(); t.toggle(); t.toggle(); return t.themeName(); })()", "expected": "light"},
            ],
            "hints": [
                "Per `themeName`: `computed(() => this.isDark() ? 'dark' : 'light')`.",
                "Per `toggle`: `this.isDark.update(v => !v);`.",
                "L'operatore di negazione `!` inverte i booleani con immediatezza."
            ],
            "creative_goals": ["Inversione logica con .update(v => !v)", "Derivazione di stringa pura con computed"],
            "bonus_xp": 20
        }
    ),
    (
        "05_angular_signals", "Comunicazione moderna tra componenti: input() e output()", 45, True,
        "Passare dati e notificare eventi tra componenti con i moderni signal inputs e output().",
        "input();input.required;output();model();Input;Output;comunicazione",
        "`input()` dichiara un input leggibile come Signal; `output()` dichiara un evento che il componente può emettere. Sono API moderne alternative: i decoratori `@Input()` e `@Output()` restano supportati.",
        """### Input basati su Signal ed eventi output:
```typescript
import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-user-badge',
  standalone: true,
  template: `
    <span (click)="deleteUser()">{{ name() }} ({{ role() }})</span>
  `
})
export class UserBadgeComponent {
  // Input standard con valore di default
  role = input('Guest');

  // Input obbligatorio che il genitore DEVE passare
  name = input.required<string>();

  // Output moderno per emettere eventi verso il genitore
  deleted = output<string>();

  deleteUser() {
    this.deleted.emit(this.name());
  }
}
```""",
        "export class CardComponent {\n  title = input.required<string>();\n  selected = output<number>();\n  onSelect(id: number) { this.selected.emit(id); }\n}",
        """export class UserBadgeModel {
    role = input('Guest');
    name = input('Utente');
    selected = output<string>();
    select() { this.selected.emit(this.name()); }
}""",
        "Trattare `output()` come un Signal: è un'API per emettere eventi, mentre `input()` fornisce un input leggibile come Signal. I decoratori `@Input()` e `@Output()` restano disponibili; in un componente bisogna seguire lo stile già adottato.",
        "Che cosa restituiscono `input()` e `output()`, e quale compito svolge ciascuno?",
        {
            "kind": "angular",
            "title": "Modello Componente con Signal Input ed Output",
            "prompt": "Implementa `UserBadgeModel` con una proprietà `name = input('Ospite')`, una proprietà `role = input('User')`, e `badgeText` calcolato con `computed()` che restituisce `\"{name()} [{role()]}\"`. Aggiungi inoltre il metodo `select()` che emette `name()` sull'output `selected = output<string>()`.",
            "starter": """export class UserBadgeModel {
    name = input("Ospite");
    role = input("User");
    selected = output<string>();

    // TODO: definisci badgeText con computed()

    select() {
        // TODO: emetti il valore di name() tramite selected
    }
}""",
            "solution": """export class UserBadgeModel {
    name = input("Ospite");
    role = input("User");
    selected = output<string>();
    badgeText = computed(() => `${this.name()} [${this.role()}]`);

    select() {
        this.selected.emit(this.name());
    }
}""",
            "tests": [
                {"name": "Badge iniziale default", "expression": "(new UserBadgeModel()).badgeText()", "expected": "Ospite [User]"},
                {"name": "Metodo select non lancia errori", "expression": "(() => { const b = new UserBadgeModel(); b.select(); return true; })()", "expected": True},
            ],
            "hints": [
                "Usa l'interpolazione di stringhe in `computed`: `${this.name()} [${this.role()}]`.",
                "Per emettere l'evento sull'output: `this.selected.emit(this.name());`.",
                "Ricorda che `name` e `role` sono segnali e si leggono con `()`."
            ],
            "creative_goals": ["String interpolation reattiva", "Utilizzo combinato di input(), output() e computed()"],
            "bonus_xp": 20
        }
    ),
    (
        "05_angular_signals", "Integrazione tra Signals e RxJS: toSignal e toObservable", 40, False,
        "Far convivere la semplicità dei Signals con la potenza degli operatori asincroni di RxJS.",
        "rxjs;observable;tosignal;toobservable;interoperabilita;debounce",
        "I Signals rappresentano valori correnti dell'interfaccia; RxJS offre operatori per comporre flussi asincroni come debounce, retry e WebSocket. `@angular/core/rxjs-interop` fornisce API per integrarli quando il caso lo richiede.",
        "### Le Due Funzioni di Interoperabilità:\n1. **`toSignal(observable$, options)`**:\n   - Converte un Observable (come una chiamata `httpClient.get()`) in un Signal!\n   - Sottoscrive il flusso e rilascia la sottoscrizione alla distruzione del contesto Angular.\n   ```typescript\n   users = toSignal(this.http.get<User[]>('/api/users'), { initialValue: [] });\n   ```\n2. **`toObservable(signal)`**:\n   - Converte un Signal in un Observable per applicare operatori potenti come `debounceTime`, `switchMap` o `distinctUntilChanged`.\n   ```typescript\n   query$ = toObservable(this.searchQuery).pipe(\n     debounceTime(300),\n     switchMap(q => this.api.search(q))\n   );\n   ```\n\nNell’esempio il recupero dell’errore è dentro `switchMap`: una richiesta fallita produce una lista vuota ma lascia attive le ricerche successive. È una semplificazione per studiare il flusso; in un’interfaccia completa distingui errore e nessun risultato. `params` codifica il termine senza concatenarlo nell’URL.",
        'import { Component, inject, signal } from \'@angular/core\';\nimport { HttpClient } from \'@angular/common/http\';\nimport { toObservable, toSignal } from \'@angular/core/rxjs-interop\';\nimport { catchError, debounceTime, distinctUntilChanged, of, switchMap } from \'rxjs\';\n\n@Component({\n  selector: \'app-search\',\n  template: `<input #field (input)="searchSignal.set(field.value)" aria-label="Ricerca" />\n    @for (name of resultsSignal(); track name) { <p>{{ name }}</p> }`\n})\nexport class SearchComponent {\n  private readonly http = inject(HttpClient);\n  readonly searchSignal = signal(\'\');\n  readonly resultsSignal = toSignal(\n    toObservable(this.searchSignal).pipe(\n      debounceTime(300),\n      distinctUntilChanged(),\n      switchMap(q => this.http.get<string[]>(\'/api/search\', { params: { q } }).pipe(\n        catchError(() => of([] as string[]))\n      ))\n    ),\n    { initialValue: [] as string[] }\n  );\n}\n// Registra provideHttpClient() in app.config.ts.\n// L’API GET /api/search?q=... deve restituire un array di nomi univoci.\n// L’URL relativo richiede stesso host o proxy verso il backend.',
        """export class SearchBridge {
    query = signal('');
    setQuery(text: string) { this.query.set(text); }
}""",
        "Leggere il valore prima della prima emissione senza gestire `undefined` o fornire un valore iniziale; creare una nuova sottoscrizione toSignal a ogni lettura.",
        "Quando è preferibile usare RxJS rispetto a un semplice Signal?",
        {
            "kind": "angular",
            "title": "Ponte Reattivo per Ricerca",
            "prompt": "Implementa `SearchBridge` con il segnale `query = signal('')`, `cleanQuery` calcolato con `computed()` in minuscolo e pulito da spazi, e il metodo `setQuery(text: string)`.",
            "starter": """export class SearchBridge {
    query = signal("");
    // TODO: definisci cleanQuery con computed()

    setQuery(text: string) {
        // TODO: aggiorna query
    }
}""",
            "solution": """export class SearchBridge {
    query = signal("");
    cleanQuery = computed(() => (this.query() ?? "").trim().toLowerCase());

    setQuery(text: string) {
        this.query.set(text ?? "");
    }
}""",
            "tests": [
                {"name": "Query iniziale vuota", "expression": "(new SearchBridge()).cleanQuery()", "expected": ""},
                {"name": "Normalizzazione testo minuscolo", "expression": "(() => { const s = new SearchBridge(); s.setQuery('  AngUlAr  '); return s.cleanQuery(); })()", "expected": "angular"},
            ],
            "hints": [
                "Usa `.trim().toLowerCase()` dentro il blocco `computed`.",
                "Proteggi l'accesso gestendo possibili valori nulli con `(this.query() ?? \"\")`.",
                "In `setQuery`, usa `.set(text)`."
            ],
            "creative_goals": ["Normalizzazione stringa pura", "Nessun rischio di eccezione su valori nulli"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 06: Database con Entity Framework Core
    # ==========================================
    (
        "06_efcore", "Introduzione a EF Core e DbContext", 45, True,
        "Configurare l'ORM standard di .NET, definire la classe DbContext e connettere il database relazionale.",
        "ef core;dbcontext;dbset;orm;sqlite;connection string",
        "Entity Framework Core mappa entità e relazioni e traduce le parti supportate delle query LINQ in SQL per il provider configurato. La connessione e la durata del contesto restano parte della configurazione dell'app.",
        """### Struttura Tipica di un DbContext in EF Core:
```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext {
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {}

    // Ogni DbSet<T> corrisponde a una tabella nel database
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
}
```

### Registrazione in Program.cs (Minimal API):
```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=dev48.db"));
```""",
        "public class AppDbContext : DbContext {\n    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {}\n    public DbSet<User> Users => Set<User>();\n}",
        """public static class DbContextHelper {
    public static string BuildSqliteConnectionString(string dbName) =>
        $"Data Source={dbName.TrimEnd('/')}.db";
}""",
        "Creare istanze manuali con `new AppDbContext()` invece di ottenerle dalla Dependency Injection; registrare il DbContext come Singleton.",
        "Qual è il ruolo principale della classe DbContext in un'applicazione .NET?",
        {
            "kind": "csharp",
            "title": "Costruttore Stringa di Connessione SQLite",
            "prompt": "Implementa `DbContextHelper.BuildSqliteConnectionString(string filename)` che restituisce `\"Data Source={filename}.db\"` se il nome non finisce già con \".db\", altrimenti `\"Data Source={filename}\"`.",
            "starter": """public static class DbContextHelper {
    /// <summary>
    /// Genera la connection string standard per SQLite.
    /// </summary>
    public static string BuildSqliteConnectionString(string filename) {
        // TODO: formatta correttamente la connection string
        return "";
    }
}""",
            "solution": """public static class DbContextHelper {
    public static string BuildSqliteConnectionString(string filename) {
        if (string.IsNullOrWhiteSpace(filename)) filename = "app";
        var clean = filename.EndsWith(".db") ? filename : $"{filename}.db";
        return $"Data Source={clean}";
    }
}""",
            "tests": [
                {"name": "Aggiunge estensione .db mancante", "expression": 'DbContextHelper.BuildSqliteConnectionString("academy")', "expected": "Data Source=academy.db"},
                {"name": "Non raddoppia estensione se presente", "expression": 'DbContextHelper.BuildSqliteConnectionString("academy.db")', "expected": "Data Source=academy.db"},
            ],
            "hints": [
                "Usa `filename.EndsWith(\".db\")` per verificare se l'estensione è già presente.",
                "Combina la stringa con l'interpolazione `$\"Data Source={clean}\"`.",
                "Gestisci eventuali valori vuoti usando un default come `\"app\"`."
            ],
            "creative_goals": ["Protezione da doppie estensioni", "String interpolation pulita"],
            "bonus_xp": 20
        }
    ),
    (
        "06_efcore", "Modellazione Entità e Relazioni 1:N e N:N", 50, True,
        "Mappare chiavi primarie, foreign key e relazioni tra tabelle usando Fluent API e convenzioni.",
        "entita;primary key;foreign key;relazione 1 a molti;onmodelcreating;navigation property",
        "Le navigation properties consentono di navigare tra entità correlate (es. da un Ordine ai suoi Articoli) in modo naturale orientato agli oggetti.",
        """### Convenzione per Relazione 1 a Molti (1:N):
```csharp
public class Category {
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;

    // Navigation property: una categoria ha molti prodotti
    public List<Product> Products { get; set; } = new();
}

public class Product {
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;

    // Foreign Key verso Category
    public int CategoryId { get; set; }
    public Category? Category { get; set; }
}
```

In `OnModelCreating` si può personalizzare il comportamento di cancellazione (es. `OnDelete(DeleteBehavior.Cascade)`).""",
        "modelBuilder.Entity<Order>()\n    .HasMany(o => o.Items)\n    .WithOne(i => i.Order)\n    .HasForeignKey(i => i.OrderId);",
        """public static class EntityRelationHelper {
    public static bool IsForeignKeyValid(int fk) => fk > 0;
}""",
        "Dimenticare la Foreign Key esplicita lasciando che EF crei 'shadow properties' con nomi automatici difficili da interrogare.",
        "Che cos'è una navigation property in Entity Framework Core?",
        {
            "kind": "csharp",
            "title": "Verifica Integrità Foreign Key",
            "prompt": "Implementa `EntityRelationHelper.ValidateRelation(int parentId, int childId)` che restituisce true solo se sia `parentId` sia `childId` sono entrambi strettamente maggiori di zero.",
            "starter": """public static class EntityRelationHelper {
    public static bool ValidateRelation(int parentId, int childId) {
        // TODO: restituisci true se entrambi sono > 0
        return false;
    }
}""",
            "solution": """public static class EntityRelationHelper {
    public static bool ValidateRelation(int parentId, int childId) => parentId > 0 && childId > 0;
}""",
            "tests": [
                {"name": "Relazione valida con ID positivi", "expression": "EntityRelationHelper.ValidateRelation(1, 10)", "expected": True},
                {"name": "ParentId non valido", "expression": "EntityRelationHelper.ValidateRelation(0, 10)", "expected": False},
                {"name": "ChildId negativo non valido", "expression": "EntityRelationHelper.ValidateRelation(2, -1)", "expected": False},
            ],
            "hints": [
                "Un confronto logico `parentId > 0 && childId > 0` verifica entrambi i valori contemporaneamente.",
                "Puoi scrivere il metodo come un'espressione `=>`.",
                "Le chiavi autoincrementali partono sempre da valori positivi."
            ],
            "creative_goals": ["Usa expression-bodied member", "Verifica stretta delle chiavi"],
            "bonus_xp": 20
        }
    ),
    (
        "06_efcore", "Migrazioni di Database: Creazione e Applicazione", 40, True,
        "Versionare lo schema del database con codice C# e applicare modifiche senza perdere dati.",
        "dotnet ef migrations add;dotnet ef database update;versionamento schema;snapshot",
        "Le migrazioni di EF Core consentono di evolvere lo schema del database nel tempo in modo ripetibile e tracciabile nel repository Git.",
        """### Comandi Fondamentali della CLI `dotnet ef`:
Prima installa gli strumenti una volta e il pacchetto di design nel progetto. Mantieni la stessa major version di EF Core (10 in questo percorso):
```powershell
dotnet tool install --global dotnet-ef --version 10.0.12
dotnet add package Microsoft.EntityFrameworkCore.Design --version 10.0.12
dotnet ef --version
```

1. **Aggiunta migrazione**:
   `dotnet ef migrations add InitialCreate`
   Crea file C# nella cartella `Migrations/` con i metodi `Up()` (applica) e `Down()` (annulla).
2. **Applicazione al database**:
   `dotnet ef database update`
   Confronta lo storico nella tabella `__EFMigrationsHistory` ed esegue solo le migrazioni mancanti.
3. **Rimozione ultima migrazione non applicata**:
   `dotnet ef migrations remove`

### Applicazione automatica all'avvio (solo per sviluppo locale):
```csharp
using var scope = app.Services.CreateScope();
var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
db.Database.Migrate();
```
Usala soltanto per sviluppo locale. Per la produzione pianifica e rivedi l'applicazione delle migrazioni come parte della distribuzione, invece di farle partire automaticamente da ogni istanza dell'app.""",
        "dotnet ef migrations add AddUserTable\ndotnet ef database update\n# Esamina la migrazione: rimozioni di colonne o tabelle possono perdere dati.",
        """public static class MigrationNameHelper {
    public static string FormatMigrationName(string name) {
        var clean = System.Text.RegularExpressions.Regex.Replace(name ?? "", "[^a-zA-Z0-9]", "");
        return string.IsNullOrEmpty(clean) ? "InitialCreate" : clean;
    }
}""",
        "Modificare manualmente le tabelle del database da un tool esterno disallineando lo snapshot delle migrazioni di EF Core.",
        "A cosa serve la tabella interna `__EFMigrationsHistory` creata da EF Core?",
        {
            "kind": "csharp",
            "title": "Formattazione Nome Migrazione Sicuro",
            "prompt": "Implementa `MigrationNameHelper.FormatMigrationName(string rawName)` che rimuove tutti i caratteri non alfanumerici e restituisce \"InitialCreate\" se la stringa risultante è vuota.",
            "starter": """using System.Text.RegularExpressions;

public static class MigrationNameHelper {
    public static string FormatMigrationName(string rawName) {
        // TODO: rimuovi caratteri non alfanumerici e usa fallback "InitialCreate"
        return "";
    }
}""",
            "solution": """using System.Text.RegularExpressions;

public static class MigrationNameHelper {
    public static string FormatMigrationName(string rawName) {
        if (string.IsNullOrWhiteSpace(rawName)) return "InitialCreate";
        var clean = Regex.Replace(rawName, "[^a-zA-Z0-9]", "");
        return string.IsNullOrEmpty(clean) ? "InitialCreate" : clean;
    }
}""",
            "tests": [
                {"name": "Rimuove spazi e caratteri speciali", "expression": 'MigrationNameHelper.FormatMigrationName("Add User_Table!")', "expected": "AddUserTable"},
                {"name": "Stringa vuota usa fallback", "expression": 'MigrationNameHelper.FormatMigrationName("   ")', "expected": "InitialCreate"},
            ],
            "hints": [
                "Usa `Regex.Replace(rawName, \"[^a-zA-Z0-9]\", \"\")` per tenere solo lettere e numeri.",
                "Verifica se il risultato è vuoto con `string.IsNullOrEmpty` e restituisci `\"InitialCreate\"`.",
                "I nomi delle classi delle migrazioni devono essere identificatori C# validi."
            ],
            "creative_goals": ["Usa Regex per sanitizzare l'identificatore", "Garantisci sempre un nome valido per la classe"],
            "bonus_xp": 20
        }
    ),
    (
        "06_efcore", "Query con LINQ su Database: Tracking e AsNoTracking", 45, True,
        "Capire quando una query EF Core di sola lettura può usare AsNoTracking e quali trade-off comporta.",
        "linq to entities;asnotracking;change tracker;includi;eager loading;n+1",
        "Per una query di sola lettura, `AsNoTracking()` evita di conservare le entità nel Change Tracker e può ridurre lavoro e memoria. Il beneficio dipende dai dati e dalla forma della query; senza identity resolution, le entità ripetute possono diventare istanze separate. Misura prima di presentare un guadagno come certo.",
        """### Tracking vs NoTracking:
- **Query con Tracking (default per entità)**:
  EF Core registra le entità e rileva le modifiche. Se cambi una proprietà e chiami `SaveChangesAsync()`, può inviare al database l'aggiornamento corrispondente. Il tracking supporta anche l'identity resolution.
- **Query `AsNoTracking()` (sola lettura)**:
  EF Core non registra nel contesto le entità restituite. Può essere adatto a letture che non verranno salvate; non usa l'identity resolution del contesto.
  ```csharp
  var products = await db.Products
      .AsNoTracking()
      .Where(p => p.Price > 50)
      .ToListAsync();
  ```

### Caricamento delle Relazioni con `Include()` (Eager Loading):
```csharp
var orderWithItems = await db.Orders
    .AsNoTracking()
    .Include(o => o.Items) // Carica gli articoli correlati in questa query.
    .FirstOrDefaultAsync(o => o.Id == id);
```""",
        "var users = await db.Users\n    .AsNoTracking()\n    .Where(u => u.IsActive)\n    .ToListAsync();",
        """public static class QueryOptionsHelper {
    public static bool ShouldUseNoTracking(bool willModifyEntities) =>
        !willModifyEntities;
}""",
        "Scegliere il tracking solo dal verbo HTTP: considera se aggiornerai le entità e se la query ha bisogno di identity resolution. `Include()` carica relazioni, ma controlla comunque la forma della query e i dati.",
        "Quando è adatto `AsNoTracking()` e quale comportamento del tracking rinunci a usare?",
        {
            "kind": "csharp",
            "title": "Selettore Politica di Tracking Query",
            "prompt": "Implementa `QueryOptionsHelper.ShouldUseNoTracking(bool willModifyEntities)`: restituisce `true` quando le entità non verranno modificate e salvate, e `false` quando prevedi di modificarle.",
            "starter": """public static class QueryOptionsHelper {
    public static bool ShouldUseNoTracking(bool willModifyEntities) {
        // TODO: scegli no-tracking solo se non modificherai le entità
        return false;
    }
}""",
            "solution": """using System;

public static class QueryOptionsHelper {
    public static bool ShouldUseNoTracking(bool willModifyEntities) =>
        !willModifyEntities;
}""",
            "tests": [
                {"name": "Lettura senza modifiche usa no-tracking", "expression": "QueryOptionsHelper.ShouldUseNoTracking(false)", "expected": True},
                {"name": "Entità da modificare restano tracciate", "expression": "QueryOptionsHelper.ShouldUseNoTracking(true)", "expected": False},
            ],
            "hints": [
                "Domandati se modificherai le entità restituite e poi chiamerai `SaveChangesAsync()`.",
                "Se `willModifyEntities` è false, restituisci true per no-tracking.",
                "Non dedurre il tracking dal verbo HTTP: basati su come userai i risultati."
            ],
            "creative_goals": [],
            "bonus_xp": 20
        }
    ),
    (
        "06_efcore", "Scrittura atomica, Transazioni e SaveChangesAsync", 45, True,
        "Inserire, aggiornare ed eliminare record gestendo transazioni atomiche e concorrenza.",
        "savechangesasync;add;update;remove;transazione;concorrenza",
        "`SaveChangesAsync()` invia le modifiche tracciate. Con un provider relazionale EF Core usa di norma una transazione per la singola chiamata; provider e operazioni distribuite possono avere comportamenti diversi.",
        """### Flusso di Scrittura Standard con EF Core:
```csharp
// 1. Creazione
var product = new Product { Title = "Tastiera Meccanica", Price = 89.99m };
db.Products.Add(product);
await db.SaveChangesAsync(); // Genera INSERT e popola product.Id con la chiave autoincrementale!

// 2. Modifica
var existing = await db.Products.FindAsync(id);
if (existing is not null) {
    existing.Price = 79.99m;
    await db.SaveChangesAsync(); // Genera UPDATE solo sulle colonne modificate!
}

// 3. Rimozione
db.Products.Remove(existing);
await db.SaveChangesAsync(); // Genera DELETE
```""",
        "db.Orders.Add(order);\nawait db.SaveChangesAsync(); // Salva e assegna automaticamente la chiave primaria generata dal DB.",
        """public static class OperationResultHelper {
    public static string FormatResult(int recordsAffected) =>
        recordsAffected > 0 ? $"Success: {recordsAffected} record modificati" : "Nessuna modifica effettuata";
}""",
        "Chiamare `SaveChangesAsync()` all'interno di un ciclo foreach invece di raggruppare le modifiche ed eseguire una singola chiamata finale.",
        "Che cosa restituisce il metodo `SaveChangesAsync()` al suo completamento?",
        {
            "kind": "csharp",
            "title": "Verifica Risultato Scrittura Database",
            "prompt": "Implementa `OperationResultHelper.FormatResult(int recordsAffected)` che restituisce `$\"Success: {recordsAffected} record modificati\"` se `recordsAffected > 0`, altrimenti `\"Nessuna modifica effettuata\"`.",
            "starter": """public static class OperationResultHelper {
    public static string FormatResult(int recordsAffected) {
        // TODO: formatta il risultato in base al numero di record
        return "";
    }
}""",
            "solution": """public static class OperationResultHelper {
    public static string FormatResult(int recordsAffected) =>
        recordsAffected > 0 ? $"Success: {recordsAffected} record modificati" : "Nessuna modifica effettuata";
}""",
            "tests": [
                {"name": "Conferma 3 record salvati", "expression": "OperationResultHelper.FormatResult(3)", "expected": "Success: 3 record modificati"},
                {"name": "Zero modifiche", "expression": "OperationResultHelper.FormatResult(0)", "expected": "Nessuna modifica effettuata"},
            ],
            "hints": [
                "Usa l'operatore ternario: `recordsAffected > 0 ? ... : ...`.",
                "Interpola il numero di record con `$\"Success: {recordsAffected} record modificati\"`.",
                "`SaveChangesAsync()` restituisce esattamente il numero di righe modificate nel DB."
            ],
            "creative_goals": ["Usa expression-bodied member", "String interpolation pulita"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 07: Form Reattivi & Routing Avanzato
    # ==========================================
    (
        "07_angular_forms_routing", "Reactive Forms: FormGroup e FormControl", 45, True,
        "Costruire form reattivi complessi e controllati gestendo stato, valori e validità dal TypeScript.",
        "reactive forms;formgroup;formcontrol;formbuilder;formcontrolname;stato validita",
        "Reactive Forms mantengono valori, stato e validatori in un modello TypeScript esplicito; sono ancora una scelta solida per form complessi e codice esistente. Angular 22 offre anche Signal Forms, stabili e vicine al modello basato su signals: qui le confrontiamo per riconoscere quale approccio usare.",
        """### Creazione di un FormGroup con FormBuilder:
```typescript
import { Component, inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
      <input formControlName="email" placeholder="Email" />
      <input type="password" formControlName="password" />
      <button type="submit" [disabled]="loginForm.invalid">Accedi</button>
    </form>
  `
})
export class LoginFormComponent {
  private readonly fb = inject(FormBuilder);
  loginForm = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  onSubmit() {
    if (this.loginForm.valid) {
      // Invia i dati al servizio di login; evita di registrare password nei log.
      const credentials = this.loginForm.getRawValue();
    }
  }
}
```

### Signal Forms in Angular 22
Signal Forms sono incluse in `@angular/forms/signals`. Un modello signal diventa la fonte dei dati; `form()` crea l'albero dei campi e `FormField` collega un campo al template.

```typescript
import { Component, signal } from '@angular/core';
import { email, form, FormField, required } from '@angular/forms/signals';

@Component({
  selector: 'app-signal-login',
  imports: [FormField],
  template: `<label>Email <input type="email" [formField]="loginForm.email" /></label>`
})
export class SignalLoginComponent {
  model = signal({ email: '' });
  loginForm = form(this.model, path => {
    required(path.email);
    email(path.email);
  });
}
```

Scegli Signal Forms per familiarizzare con form nuovi basati su signals; scegli Reactive Forms quando vuoi il modello esplicito già usato negli esempi e nei progetti esistenti, soprattutto se i form sono complessi o dinamici. In questo corso il laboratorio prosegue con Reactive Forms; Signal Forms è una panoramica, non un secondo insieme di esercizi da completare. [Confronto ufficiale Angular](https://angular.dev/guide/forms/signals/comparison).""",
        "loginForm = fb.group({\n  email: ['', [Validators.required, Validators.email]],\n  age: [18, [Validators.min(18)]]\n});",
        """export class LoginFormRules {
    canSubmit(email: string, password: string): boolean {
        return email.trim().includes('@') && password.length >= 8;
    }
}""",
        "Dimenticare di importare `ReactiveFormsModule` negli `imports` del componente Standalone, provocando l'errore 'formGroup is not a known property of form'.",
        "Qual è la differenza fondamentale tra Template-Driven Forms e Reactive Forms in Angular?",
        {
            "kind": "typescript",
            "title": "Regola di invio per un form",
            "prompt": "Implementa la funzione pura `LoginFormRules.canSubmit(email: string, password: string): boolean`. Restituisce `true` quando l'email ripulita dagli spazi contiene `@` E la password ha almeno 8 caratteri; altrimenti restituisce `false`. Questo esercizio controlla solo la regola TypeScript: nel laboratorio la collegherai al vero stato del form Angular.",
            "starter": """export class LoginFormRules {
    canSubmit(email: string, password: string): boolean {
        // TODO: combina le due regole richieste
        return false;
    }
}""",
            "solution": """export class LoginFormRules {
    canSubmit(email: string, password: string): boolean {
        return email.trim().includes("@") && password.length >= 8;
    }
}""",
            "tests": [
                {"name": "Email e password valide", "expression": "(new LoginFormRules()).canSubmit('mario@test.it', 'password123')", "expected": True},
                {"name": "Email senza chiocciola", "expression": "(new LoginFormRules()).canSubmit('mario.test.it', 'password123')", "expected": False},
                {"name": "Password troppo corta", "expression": "(new LoginFormRules()).canSubmit('mario@test.it', 'short')", "expected": False},
                {"name": "Spazi intorno all'email vengono ignorati", "expression": "(new LoginFormRules()).canSubmit('  mario@test.it  ', 'password123')", "expected": True},
            ],
            "hints": [
                "Ripulisci l'email con `email.trim()` prima di controllare il contenuto.",
                "Usa `includes('@')` per il requisito email e `password.length >= 8` per la lunghezza.",
                "Combina le due condizioni con `&&`: devono essere vere entrambe."
            ],
            "creative_goals": [],
            "bonus_xp": 0
        }
    ),
    (
        "07_angular_forms_routing", "Validatori sincroni nativi e personalizzati", 40, True,
        "Applicare vincoli di validazione ed estendere Angular con funzioni di controllo custom.",
        "validator;validationerrors;required;minlength;validatorfn;custom validator",
        "Un validatore sincrono in Angular è una semplice funzione pura che riceve un AbstractControl e restituisce null se il campo è valido, oppure un oggetto ValidationErrors con il codice dell'errore.",
        """### Anatomia di un Validatore Personalizzato:
```typescript
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

// Validatore che vieta l'uso di parole riservate (es. 'admin')
export function forbiddenNameValidator(forbiddenName: string): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value as string;
    const isForbidden = value?.toLowerCase().includes(forbiddenName.toLowerCase());
    return isForbidden ? { forbiddenName: { value: control.value } } : null;
  };
}
```

### Regola Fondamentale del Ritorno:
- **`null`**: il controllo è valido! Non ci sono errori.
- **`{ [errorKey]: true }`**: il controllo ha fallito la validazione. La chiave `errorKey` apparirà nell'oggetto `control.errors`.""",
        "export function minAgeValidator(min: number): ValidatorFn {\n  return (control) => control.value >= min ? null : { minAge: { required: min } };\n}",
        """export class CustomValidationService {
    validateTaxCode(code: string): { valid: boolean; error?: string } {
        if (!code || code.length !== 16) return { valid: false, error: 'Lunghezza errata' };
        return { valid: true };
    }
}""",
        "Restituire `false` invece di `null` quando il controllo è valido (in Angular qualsiasi valore diverso da null viene interpretato come errore!).",
        "Perché un validatore di Angular deve restituire `null` (e non `true` o `false`) quando il valore è valido?",
        {
            "kind": "angular",
            "title": "Funzione Validatore Custom",
            "prompt": "Implementa `CustomValidationService.validatePassword(password: string)` che restituisce `{ valid: true }` se la password contiene almeno 8 caratteri e un numero, altrimenti restituisce `{ valid: false, error: 'Password debole' }`.",
            "starter": """export class CustomValidationService {
    validatePassword(password: string): { valid: boolean; error?: string } {
        // TODO: verifica lunghezza >= 8 e presenza di almeno un numero
        return { valid: false, error: "Password debole" };
    }
}""",
            "solution": """export class CustomValidationService {
    validatePassword(password: string): { valid: boolean; error?: string } {
        if (!password || password.length < 8 || !/\\d/.test(password)) {
            return { valid: false, error: "Password debole" };
        }
        return { valid: true };
    }
}""",
            "tests": [
                {"name": "Password robusta valida", "expression": "(new CustomValidationService()).validatePassword('Secret123').valid", "expected": True},
                {"name": "Password troppo corta non valida", "expression": "(new CustomValidationService()).validatePassword('Sec1').valid", "expected": False},
                {"name": "Password senza numeri non valida", "expression": "(new CustomValidationService()).validatePassword('OnlyLettersHere').valid", "expected": False},
            ],
            "hints": [
                "Usa `password.length >= 8` per la lunghezza minima.",
                "Usa l'espressione regolare `/\\d/.test(password)` per verificare la presenza di almeno una cifra numerica.",
                "Restituisci `{ valid: true }` solo se entrambe le condizioni sono soddisfatte."
            ],
            "creative_goals": ["Usa regex /\\d/ per il controllo numerico", "Fornisci un messaggio di errore chiaro"],
            "bonus_xp": 20
        }
    ),
    (
        "07_angular_forms_routing", "Validatori asincroni: verifica remota via API", 45, False,
        "Controllare unicità di email o codici fiscali interrogando il backend prima dell'invio del form.",
        "asyncvalidator;observable;timer;debounce;verifica remota;unicita",
        "I validatori asincroni restituiscono una Promise o un Observable di ValidationErrors, permettendo di interrogare un endpoint REST prima che l'utente invii il modulo.",
        """### Validatore Asincrono con Debounce:
```typescript
import { AbstractControl, AsyncValidatorFn, ValidationErrors } from '@angular/forms';
import { Observable, timer, of } from 'rxjs';
import { switchMap, map } from 'rxjs/operators';

export function uniqueEmailValidator(checkApi: (email: string) => Observable<boolean>): AsyncValidatorFn {
  return (control: AbstractControl): Observable<ValidationErrors | null> => {
    if (!control.value) return of(null);

    // Attende 300ms prima di chiamare l'API per evitare chiamate a ogni tasto
    return timer(300).pipe(
      switchMap(() => checkApi(control.value)),
      map(isTaken => isTaken ? { emailTaken: true } : null)
    );
  };
}
```""",
        "return timer(300).pipe(\n  switchMap(() => api.checkEmail(control.value)),\n  map(taken => taken ? { emailTaken: true } : null)\n);",
        """export class AsyncCheckSimulator {
    takenEmails = new Set(['admin@dev48.it', 'test@dev48.it']);
    isEmailAvailable(email: string): boolean {
        return !this.takenEmails.has(email.toLowerCase().trim());
    }
}""",
        "Eseguire chiamate HTTP all'API a ogni singolo tasto premuto senza applicare `debounceTime` o `timer` (intasando la rete del server).",
        "Quando conviene ritardare la verifica remota, e che cosa mostri mentre il controllo è pending?",
        {
            "kind": "angular",
            "title": "Verifica Disponibilità Username Asincrona",
            "prompt": "Implementa `AsyncCheckSimulator` con un `Set` di username occupati contenente 'admin' e 'root', e il metodo `isUsernameAvailable(username: string): boolean` che restituisce true se lo username è disponibile (case-insensitive), false se occupato o vuoto.",
            "starter": """export class AsyncCheckSimulator {
    private reserved = new Set(["admin", "root"]);

    isUsernameAvailable(username: string): boolean {
        // TODO: restituisci false se vuoto o presente in reserved
        return false;
    }
}""",
            "solution": """export class AsyncCheckSimulator {
    private reserved = new Set(["admin", "root"]);

    isUsernameAvailable(username: string): boolean {
        if (!username || username.trim().length === 0) return false;
        return !this.reserved.has(username.trim().toLowerCase());
    }
}""",
            "tests": [
                {"name": "Username libero disponibile", "expression": "(new AsyncCheckSimulator()).isUsernameAvailable('luca')", "expected": True},
                {"name": "Username admin riservato", "expression": "(new AsyncCheckSimulator()).isUsernameAvailable('admin')", "expected": False},
                {"name": "Username ROOT maiuscolo riservato", "expression": "(new AsyncCheckSimulator()).isUsernameAvailable('ROOT')", "expected": False},
                {"name": "Username vuoto non valido", "expression": "(new AsyncCheckSimulator()).isUsernameAvailable('   ')", "expected": False},
            ],
            "hints": [
                "Controlla prima che lo username non sia nullo o vuoto: `if (!username?.trim()) return false;`.",
                "Usa `username.trim().toLowerCase()` per il controllo case-insensitive.",
                "Usa `!this.reserved.has(clean)` per verificare se è disponibile."
            ],
            "creative_goals": ["Usa Set con ricerca O(1)", "Normalizzazione case-insensitive"],
            "bonus_xp": 20
        }
    ),
    (
        "07_angular_forms_routing", "Angular Router moderno e Lazy Loading", 45, True,
        "Configurare la navigazione a pagina singola (SPA) caricando moduli e componenti su richiesta.",
        "router;routes;loadcomponent;router-outlet;routerlink;parametri rotta",
        "L'Angular Router associa gli URL del browser ai componenti dell'applicazione, caricando il codice dei componenti solo quando l'utente visita la relativa pagina (Lazy Loading con loadComponent).",
        """### Configurazione Rotte con Lazy Loading in `app.routes.ts`:
```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'users/:id',
    loadComponent: () => import('./features/user-detail.component').then(m => m.UserDetailComponent)
  },
  { path: '**', redirectTo: 'dashboard' } // Wildcard per 404
];
```

### Nel Template:
- `<router-outlet />`: punto di montaggio in cui viene renderizzato il componente della rotta attiva.
- `<a routerLink="/dashboard" routerLinkActive="active">`: navigazione SPA senza ricaricare la pagina.""",
        "export const routes: Routes = [\n  { path: 'catalog', loadComponent: () => import('./catalog').then(m => m.CatalogComponent) }\n];",
        """export class RouteMatcher {
    isMatch(pattern: string, url: string): boolean {
        return pattern.replace(/:\\w+/g, '[^/]+') === url;
    }
}""",
        "Usare `href` standard sui link invece di `routerLink` (provoca il ricaricamento completo dell'applicazione e perdita dello stato in memoria).",
        "Qual è il vantaggio di usare `loadComponent: () => import(...)` rispetto a importare direttamente la classe del componente nelle rotte?",
        {
            "kind": "angular",
            "title": "Generatore Path Rotte SPA",
            "prompt": "Implementa `RouteMatcher.buildUserDetailPath(userId: number)` che restituisce `/users/{userId}`, e `isHome(path: string)` che restituisce true se il path è `/` oppure stringa vuota.",
            "starter": """export class RouteMatcher {
    buildUserDetailPath(userId: number): string {
        // TODO: restituisci "/users/{userId}"
        return "";
    }

    isHome(path: string): boolean {
        // TODO: restituisci true se path è "/" o ""
        return false;
    }
}""",
            "solution": """export class RouteMatcher {
    buildUserDetailPath(userId: number): string {
        return `/users/${userId}`;
    }

    isHome(path: string): boolean {
        const clean = (path ?? "").trim();
        return clean === "" || clean === "/";
    }
}""",
            "tests": [
                {"name": "Path dettaglio utente 42", "expression": "(new RouteMatcher()).buildUserDetailPath(42)", "expected": "/users/42"},
                {"name": "Path vuoto è home", "expression": "(new RouteMatcher()).isHome('')", "expected": True},
                {"name": "Path slash è home", "expression": "(new RouteMatcher()).isHome('/')", "expected": True},
                {"name": "Altro path non è home", "expression": "(new RouteMatcher()).isHome('/catalog')", "expected": False},
            ],
            "hints": [
                "Usa il template literal: ``/users/${userId}``.",
                "Per `isHome`, confronta se `clean === '' || clean === '/'`.",
                "Pulisci la stringa con `.trim()` per evitare bug con spazi."
            ],
            "creative_goals": ["Template literal ES6 sintetico", "Normalizzazione stringhe robuste"],
            "bonus_xp": 20
        }
    ),
    (
        "07_angular_forms_routing", "Route Guards funzionali: Proteggere le rotte con canActivate", 40, True,
        "Bloccare accessi non autorizzati a pagine sensibili con funzioni canActivateFn.",
        "route guard;canactivatefn;inject;router;autenticazione;protezione rotte",
        "Le Route Guards funzionali decidono se Angular può completare una navigazione e possono restituire un UrlTree di reindirizzamento. Sono un controllo del flusso UI: l'API deve applicare l'autorizzazione sul server.",
        "### Creazione di una Route Guard Funzionale in Angular:\n```typescript\nimport { inject } from '@angular/core';\nimport { CanActivateFn, Router } from '@angular/router';\nimport { AuthService } from './auth.service';\n\nexport const authGuard: CanActivateFn = (route, state) => {\n  const authService = inject(AuthService);\n  const router = inject(Router);\n\n  if (authService.isAuthenticated()) {\n    return true; // Navigazione consentita!\n  }\n\n  // Reindirizza al login memorizzando l'URL a cui voleva accedere\n  return router.createUrlTree(['/login'], { queryParams: { returnUrl: state.url } });\n};\n```\n\n### Applicazione nella Rotta:\n```typescript\n{\n  path: 'admin',\n  loadComponent: () => import('./admin.component').then(m => m.AdminComponent),\n  canActivate: [authGuard]\n}\n```\n\nIl servizio usato dalla guard, in `auth.service.ts`, rappresenta qui soltanto lo stato locale della sessione:\n```typescript\nimport { Injectable, signal } from '@angular/core';\n\n@Injectable({ providedIn: 'root' })\nexport class AuthService {\n  readonly authenticated = signal(false);\n  isAuthenticated(): boolean { return this.authenticated(); }\n}\n```\nIl login aggiorna questo stato; la sua presenza non autorizza una richiesta sul server. La rotta lazy presume un file `admin.component.ts` che esporta `AdminComponent`: nel laboratorio trovi pagine e rotte già predisposte.",
        "export const authGuard: CanActivateFn = () => {\n  const auth = inject(AuthService);\n  return auth.isAuthenticated() ? true : inject(Router).createUrlTree(['/login']);\n};",
        """export class GuardSimulator {
    checkAccess(isAuthenticated: boolean, requiredRole?: string, userRole?: string): boolean {
        if (!isAuthenticated) return false;
        if (!requiredRole) return true;
        return userRole === requiredRole;
    }
}""",
        "Restituire un semplice `false` nella guard lasciando l'utente su una schermata vuota senza feedback, invece di reindirizzarlo a `/login` con un UrlTree.",
        "Quale vantaggio offrono le guard funzionali (`CanActivateFn`) rispetto alle vecchie guard basate su classi e interfacce?",
        {
            "kind": "angular",
            "title": "Simulatore di Route Guard",
            "prompt": "Implementa `GuardSimulator.canAccess(isAuthenticated: boolean, requiredRole: string, userRole: string)` che restituisce true solo se l'utente è autenticato E (il ruolo richiesto è \"Any\" OPPURE coincide con userRole).",
            "starter": """export class GuardSimulator {
    canAccess(isAuthenticated: boolean, requiredRole: string, userRole: string): boolean {
        // TODO: verifica autenticazione e corrispondenza ruolo
        return false;
    }
}""",
            "solution": """export class GuardSimulator {
    canAccess(isAuthenticated: boolean, requiredRole: string, userRole: string): boolean {
        if (!isAuthenticated) return false;
        if (requiredRole === "Any") return true;
        return (userRole ?? "").toLowerCase() === (requiredRole ?? "").toLowerCase();
    }
}""",
            "tests": [
                {"name": "Utente non autenticato respinto", "expression": "(new GuardSimulator()).canAccess(false, 'Admin', 'Admin')", "expected": False},
                {"name": "Admin accede a rotta Admin", "expression": "(new GuardSimulator()).canAccess(true, 'Admin', 'Admin')", "expected": True},
                {"name": "Ruolo Any consente accesso", "expression": "(new GuardSimulator()).canAccess(true, 'Any', 'User')", "expected": True},
                {"name": "Ruolo non corrispondente respinto", "expression": "(new GuardSimulator()).canAccess(true, 'Admin', 'User')", "expected": False},
            ],
            "hints": [
                "Verifica prima `if (!isAuthenticated) return false;`.",
                "Se `requiredRole === 'Any'`, consenti l'accesso restituendo `true`.",
                "Altrimenti confronta i ruoli in modo case-insensitive: `userRole.toLowerCase() === requiredRole.toLowerCase()`."
            ],
            "creative_goals": ["Guard pattern a uscita rapida (early return)", "Confronto case-insensitive"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 08: Autenticazione JWT & Sicurezza Full-Stack
    # ==========================================
    (
        "08_security_fullstack", "Principi di sicurezza Web e architettura JWT", 40, True,
        "Comprendere header, payload e firma di un JWT, e valutare cosa comporta usare token senza una sessione server tradizionale.",
        "jwt;header;payload;signature;claims;revoca;bearer token",
        "Un JWT è un formato di token. Un token firmato (JWS) contiene tre parti codificate in Base64URL, ma la firma non cifra il payload. Per autenticare una richiesta, il server deve validare il token e applicare le proprie regole di autorizzazione.",
        """### Anatomia del JWT compatto firmato (JWS):
1. **Header**: dichiara il tipo di token e l'algoritmo di firma. Il server deve accettare solo gli algoritmi previsti dalla configurazione.
2. **Payload (Claims)**: contiene le affermazioni sull'identità dell'utente:
   - `sub`: identificativo utente (Subject)
   - `email`: indirizzo email
   - `role`: ruoli di autorizzazione
   - `exp`: timestamp di scadenza (Expiration)
3. **Signature (Firma crittografica)**:
   - Protegge l'integrità dei dati firmati. Il server rifiuta un token alterato solo se verifica correttamente firma, emittente, destinatario e scadenza.

Le parti sono **Base64URL, non cifrate**: chi possiede il token può leggere il payload. Un token con `exp` breve riduce la finestra di utilizzo; la revoca immediata richiede una strategia aggiuntiva.""",
        "// Il token viaggia nell'header HTTP Authorization: Bearer eyJhbGciOiJIUzI1Ni...",
        """public static class JwtHelper {
    public static string FormatBearerHeader(string token) => $"Bearer {token.Trim()}";
    public static bool HasValidParts(string token) => token.Split('.').Length == 3;
}""",
        "Mettere password o altri dati riservati nel payload; supporre che avere una firma renda valido il token senza convalidare le sue claim; dimenticare la scadenza.",
        "Perché non si devono mai memorizzare dati sensibili (come password o carte di credito) nel payload di un token JWT?",
        {
            "kind": "csharp",
            "title": "Validazione Struttura Token JWT",
            "prompt": "Implementa `JwtHelper.ValidateTokenStructure(string? token)` che restituisce true se il token contiene esattamente 3 parti separate da punti (Header, Payload, Signature) e nessuna delle parti è vuota.",
            "starter": """public static class JwtHelper {
    public static bool ValidateTokenStructure(string? token) {
        // TODO: verifica che token abbia 3 parti separate da '.' non vuote
        return false;
    }
}""",
            "solution": """using System;

public static class JwtHelper {
    public static bool ValidateTokenStructure(string? token) {
        if (string.IsNullOrWhiteSpace(token)) return false;
        var parts = token.Split('.');
        if (parts.Length != 3) return false;
        return !string.IsNullOrWhiteSpace(parts[0]) &&
               !string.IsNullOrWhiteSpace(parts[1]) &&
               !string.IsNullOrWhiteSpace(parts[2]);
    }
}""",
            "tests": [
                {"name": "Token con 3 parti valide", "expression": 'JwtHelper.ValidateTokenStructure("header.payload.signature")', "expected": True},
                {"name": "Token con 2 parti non valido", "expression": 'JwtHelper.ValidateTokenStructure("header.payload")', "expected": False},
                {"name": "Token con parte vuota non valido", "expression": 'JwtHelper.ValidateTokenStructure("header..signature")', "expected": False},
                {"name": "Token nullo non valido", "expression": "JwtHelper.ValidateTokenStructure(null)", "expected": False},
            ],
            "hints": [
                "Usa `token.Split('.')` per dividere la stringa.",
                "Verifica che `parts.Length == 3`.",
                "Controlla che ciascuna delle 3 parti non sia vuota con `!string.IsNullOrWhiteSpace(parts[i])`."
            ],
            "creative_goals": ["Controllo esaustivo delle 3 componenti", "Early return per massima efficienza"],
            "bonus_xp": 20
        }
    ),
    (
        "08_security_fullstack", "Generazione e convalida token JWT in ASP.NET Core", 45, True,
        "Configurare la validazione JWT in ASP.NET Core, seguire in un esempio locale come viene emesso un token e applicare una policy di ruolo sugli endpoint Minimal API.",
        "jwtsecuritytokenhandler;symmetricsecuritykey;requireauthorization;dotnet user-secrets;claimstype;authorization policy",
        "In un esempio didattico locale, ASP.NET Core può emettere un token dopo aver verificato credenziali dimostrative e convalidare firma, issuer, audience e scadenza sulle richieste successive. L'autenticazione stabilisce chi presenta il token; una policy decide quali ruoli possono usare un endpoint.",
        """### Prepara la chiave locale in PowerShell
Esegui i comandi nella cartella che contiene `Server.csproj`; `dotnet user-secrets init` si esegue una sola volta per progetto. Il pacchetto abilita la convalida Bearer nell'API. User Secrets mantiene una chiave di sviluppo fuori dal repository; genera una chiave casuale sul tuo computer.

```powershell
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer --version 10.0.12
dotnet user-secrets init
$jwtKey = [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
dotnet user-secrets set "Jwt:SigningKey" $jwtKey
```

### Generazione, convalida e autorizzazione in `Program.cs`
```csharp
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);
var signingKey = builder.Configuration["Jwt:SigningKey"]
    ?? throw new InvalidOperationException("Configura Jwt:SigningKey per lo sviluppo.");
var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(signingKey));
const string issuer = "dev48-local-demo";
const string audience = "dev48-local-client";

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true, ValidIssuer = issuer,
        ValidateAudience = true, ValidAudience = audience,
        ValidateIssuerSigningKey = true, IssuerSigningKey = key,
        ValidateLifetime = true,
        NameClaimType = ClaimTypes.Name,
        RoleClaimType = ClaimTypes.Role
    });
builder.Services.AddAuthorization(options =>
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin")));

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();

IResult Login(LoginRequest credentials)
{
    string? role = null;
    if (credentials.UserName == "demo") role = "Reader";
    if (credentials.UserName == "admin") role = "Admin";
    if (credentials.Password != "demo" || role is null) return Results.Unauthorized();

    var claims = new[]
    {
        new Claim(ClaimTypes.Name, credentials.UserName),
        new Claim(ClaimTypes.Role, role)
    };
    var token = new JwtSecurityToken(issuer, audience, claims,
        expires: DateTime.UtcNow.AddMinutes(15),
        signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));
    return Results.Ok(new LoginResponse(new JwtSecurityTokenHandler().WriteToken(token)));
}

app.MapPost("/api/login", Login); // pubblico: restituisce un token breve per le credenziali demo
app.MapGet("/api/profile", (ClaimsPrincipal user) => Results.Ok(new { name = user.Identity?.Name }))
    .RequireAuthorization();
app.MapGet("/api/admin", () => Results.Ok("Area amministrativa"))
    .RequireAuthorization("AdminOnly");
app.Run();

public record LoginRequest(string UserName, string Password);
public record LoginResponse(string Token);
public partial class Program { }
```

Il token demo usa una chiave HMAC condivisa. User Secrets è solo per sviluppo locale e non cifra i valori: non distribuire questa API. Le credenziali fisse e la firma didattica servono solo a seguire il flusso; per un'app reale usa un provider e flussi standard OAuth/OIDC. Consulta le guide Microsoft su [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-10.0) e [JWT bearer e flussi di autenticazione](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-10.0).""",
        """POST /api/login { \"userName\": \"demo\", \"password\": \"demo\" } -> 200 con token
GET /api/profile senza token -> 401
GET /api/profile con token Reader -> 200
GET /api/admin con token Reader -> 403
POST /api/login con userName `admin` e password `demo`, poi GET /api/admin -> 200""",
        'public static class AccessDecision {\n    public static int StatusCode(bool authenticated, string role) {\n        // Prima chiediti se esiste un’identità verificata.\n        // Poi applica il requisito di ruolo della risorsa.\n        return 200; // comportamento da correggere nell’esercizio\n    }\n}',
        "Usare questa rotta demo come sistema di login reale; salvare chiavi o token nel repository; confondere `RequireAuthorization()` (serve un utente autenticato) con una policy di ruolo; fidarsi di una guard Angular al posto della policy API.",
        "Che differenza c'è tra `RequireAuthorization()` e `RequireAuthorization(\"AdminOnly\")` e quali risposte HTTP ti aspetti?",
        {'kind': 'csharp',
 'title': 'Distinguere autenticazione e autorizzazione',
 'prompt': 'Implementa `AccessDecision.StatusCode(bool authenticated, string role)` per una risorsa Admin: '
           '401 se non autenticato, 403 se autenticato con ruolo diverso da Admin, 200 per Admin. Il '
           'confronto del ruolo è esatto. Il runner controlla questa decisione isolata; il laboratorio JWT '
           'verifica la vera policy ASP.NET Core con token firmati.',
 'starter': 'public static class AccessDecision {\n'
            '    public static int StatusCode(bool authenticated, string role) {\n'
            '        // TODO: verifica prima l’identità, poi il ruolo\n'
            '        return 200;\n'
            '    }\n'
            '}',
 'solution': 'public static class AccessDecision {\n'
             '    public static int StatusCode(bool authenticated, string role) {\n'
             '        if (!authenticated) return 401;\n'
             '        return role == "Admin" ? 200 : 403;\n'
             '    }\n'
             '}',
 'tests': [{'name': 'Anonimo senza ruolo',
            'expression': 'AccessDecision.StatusCode(false, "")',
            'expected': 401},
           {'name': 'Un ruolo dichiarato non autentica',
            'expression': 'AccessDecision.StatusCode(false, "Admin")',
            'expected': 401},
           {'name': 'Reader autenticato',
            'expression': 'AccessDecision.StatusCode(true, "Reader")',
            'expected': 403},
           {'name': 'Admin autenticato',
            'expression': 'AccessDecision.StatusCode(true, "Admin")',
            'expected': 200},
           {'name': 'Confronto esatto del ruolo',
            'expression': 'AccessDecision.StatusCode(true, "admin")',
            'expected': 403}],
 'hints': ['La verifica dell’identità deve precedere quella del ruolo.',
           'Un utente autenticato può comunque non avere il permesso richiesto.',
           'Restituisci 401 nel primo ramo, poi scegli tra 200 e 403.']}
    ),
    (
        "08_security_fullstack", "Consumo API autenticata con HttpClient e HttpInterceptor", 45, True,
        "Inviare il token Bearer nelle chiamate dirette alla propria API con un HttpInterceptorFn di Angular.",
        "httpclient;httpinterceptorfn;bearer token;authorization header;req.clone;withinterceptors",
        "Un HttpInterceptor può aggiungere `Authorization: Bearer <token>` alle richieste verso la propria API. Limitare l'interceptor all'origine attesa evita di inviare il token a server di terze parti. Il servizio d'esempio lo conserva solo in memoria: un ricaricamento lo elimina; non spostarlo in `localStorage` come scorciatoia per renderlo persistente.",
        """### Creazione di un HttpInterceptor Funzionale in Angular:
```typescript
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { SessionService } from './session.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(SessionService).token();

  const apiOrigin = 'https://localhost:5001';
  const requestOrigin = new URL(req.url, inject(DOCUMENT).baseURI).origin;
  if (token && requestOrigin === apiOrigin) {
    // La richiesta HTTP è immutabile: va clonata aggiungendo gli headers!
    const clonedReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    return next(clonedReq);
  }

    return next(req);
};
```

### Servizio della sessione in `session.service.ts`:
```typescript
import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SessionService {
  readonly token = signal<string | null>(null);
}
```
Dopo il login imposta `session.token.set(response.token)`. Un URL relativo è risolto rispetto alla pagina, non all'origine API: se client e server usano porte diverse, passa l'URL assoluto dell'API oppure configura un proxy di sviluppo.

### Registrazione in `app.config.ts`:
```typescript
provideHttpClient(withInterceptors([authInterceptor]))
```

### Che cosa significa “in memoria”
Il campo privato di `TokenStorageService` vive finché l'applicazione resta caricata; un aggiornamento della pagina lo azzera. È una scelta esplicita per l'esercizio, non un sistema completo di sessione. `localStorage` e `sessionStorage` espongono i token agli script eseguiti nella pagina: per applicazioni reali segui un flusso OAuth/OIDC e la guida di sicurezza ASP.NET Core, scegliendo il modello adatto alla tua architettura.

Riferimento: [Configure JWT bearer authentication in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-10.0).""",
        "const cloned = req.clone({\n  setHeaders: { Authorization: `Bearer ${token}` }\n});\nreturn next(cloned);",
        """export class TokenStorageService {
    private token: string | null = null;
    setToken(t: string) { this.token = t; }
    getToken(): string | null { return this.token; }
    hasToken(): boolean { return Boolean(this.token); }
}""",
        "Modificare direttamente l'oggetto `HttpRequest`; aggiungere il token a URL esterni alla propria API; trattare una guard Angular come controllo di autorizzazione lato server; usare `localStorage` come soluzione automatica per mantenere un token.",
        "Perché un interceptor dovrebbe aggiungere il Bearer token solo alle richieste dirette all'API prevista?",
        {'kind': 'angular',
 'title': 'Token e origine della richiesta',
 'prompt': 'Completa `TokenStorageService` con setToken, getToken e hasToken. Aggiungi '
           '`authorizationFor(url: string): string | null`: restituisce `Bearer <token>` soltanto se il '
           'token è presente e l’origine dell’URL è https://localhost:5001, altrimenti null. Gli URL '
           'dell’esercizio sono assoluti. Il runner verifica la selezione dell’header; il laboratorio usa un '
           'vero HttpInterceptor.',
 'starter': 'export class TokenStorageService {\n'
            '    private token: string | null = null;\n'
            '    setToken(t: string | null) { /* TODO */ }\n'
            '    getToken(): string | null { return null; }\n'
            '    hasToken(): boolean { return false; }\n'
            '    authorizationFor(url: string): string | null { return null; }\n'
            '}',
 'solution': 'export class TokenStorageService {\n'
             '    private token: string | null = null;\n'
             '    setToken(t: string | null) { this.token = t; }\n'
             '    getToken(): string | null { return this.token; }\n'
             '    hasToken(): boolean { return Boolean(this.token); }\n'
             '    authorizationFor(url: string): string | null {\n'
             '        if (!this.hasToken() || new URL(url).origin !== "https://localhost:5001") return '
             'null;\n'
             '        return `Bearer ${this.token}`;\n'
             '    }\n'
             '}',
 'tests': [{'name': 'Stato iniziale senza token',
            'expression': '(new TokenStorageService()).hasToken()',
            'expected': False},
           {'name': 'Salvataggio token valido',
            'expression': "(() => { const s = new TokenStorageService(); s.setToken('abc.123'); return "
                          's.hasToken(); })()',
            'expected': True},
           {'name': 'Lettura token corretto',
            'expression': "(() => { const s = new TokenStorageService(); s.setToken('my-token'); return "
                          's.getToken(); })()',
            'expected': 'my-token'},
           {'name': 'Salvataggio null azzera token',
            'expression': "(() => { const s = new TokenStorageService(); s.setToken('token'); "
                          's.setToken(null); return s.hasToken(); })()',
            'expected': False},
           {'name': 'Header per API configurata',
            'expression': '(() => { const s = new TokenStorageService(); s.setToken("abc"); return '
                          's.authorizationFor("https://localhost:5001/api/profile"); })()',
            'expected': 'Bearer abc'},
           {'name': 'Nessun token verso origini esterne',
            'expression': '(() => { const s = new TokenStorageService(); s.setToken("abc"); return '
                          's.authorizationFor("https://example.test/api/profile"); })()',
            'expected': None},
           {'name': 'Porta differente',
            'expression': '(() => { const s = new TokenStorageService(); s.setToken("abc"); return '
                          's.authorizationFor("https://localhost:4200/api/profile"); })()',
            'expected': None},
           {'name': 'Token assente',
            'expression': '(new '
                          'TokenStorageService()).authorizationFor("https://localhost:5001/api/profile")',
            'expected': None}],
 'hints': ['Non usare startsWith per confrontare l’origine: schema, host e porta fanno parte del confronto.',
           '`new URL(url).origin` estrae l’origine di un URL assoluto.',
           'Controlla il token e l’origine prima di costruire l’header.'],
 'creative_goals': [],
 'bonus_xp': 20}
    ),
    (
        "08_security_fullstack", "CORS, Same-Origin, XSS e CSRF: scopi distinti", 40, True,
        "Configurare una policy CORS precisa e distinguere CORS dai controlli anti-CSRF e dalla mitigazione XSS.",
        "cors;withorigins;xss;csrf;samesite;content security policy;sanitizzazione",
        "CORS permette al browser di leggere risposte cross-origin quando l'API autorizza l'origine. Non è autenticazione né protezione CSRF: il server può ricevere ed eseguire una richiesta anche se il browser poi ne blocca la risposta.",
        """### Policy CORS per un client Angular:
```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(options => {
    options.AddPolicy("AllowAngularClient", policy => {
        policy.WithOrigins("http://localhost:4200", "https://academy.dev48.it")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Con endpoint routing, applica CORS prima dell'autorizzazione.
app.UseCors("AllowAngularClient");
```

Un header `Authorization` Bearer impostato da Angular richiede che CORS consenta l'header `Authorization`, ma non richiede `AllowCredentials()`. Quest'ultimo riguarda richieste con credenziali browser, per esempio cookie. In quel caso elenca origini esplicite e abilita anche la credenziale lato client.

CORS non sostituisce autenticazione, autorizzazione o difese CSRF. Per cookie usa anche una strategia anti-CSRF appropriata. Con credenziali non riflettere origini arbitrarie e non usare wildcard `*`.""",
        "builder.Services.AddCors(options => {\n  options.AddPolicy(\"Dev48Policy\", p => p.WithOrigins(\"http://localhost:4200\").AllowAnyMethod().AllowAnyHeader());\n});",
        """public static class CorsSecurityHelper {
    public static bool IsOriginAllowed(string origin, string[] allowedOrigins) {
        return System.Array.Exists(allowedOrigins, o => string.Equals(o, origin?.Trim(), System.StringComparison.OrdinalIgnoreCase));
    }
}""",
        "Usare CORS come autenticazione o difesa CSRF; confondere un blocco del browser con un endpoint non eseguito; autorizzare origini arbitrarie per richieste con cookie.",
        "Che cosa blocca il browser quando la risposta non contiene i permessi CORS, e che cosa CORS non protegge?",
        {
            "kind": "csharp",
            "title": "Validatore di Origini CORS",
            "prompt": "Implementa `CorsSecurityHelper.IsOriginAllowed(string? origin, string[] allowedOrigins)` che restituisce true se `origin` è presente tra le origini consentite (confronto case-insensitive e pulizia spazi).",
            "starter": """using System;

public static class CorsSecurityHelper {
    public static bool IsOriginAllowed(string? origin, string[] allowedOrigins) {
        // TODO: verifica se origin fa parte di allowedOrigins
        return false;
    }
}""",
            "solution": """using System;

public static class CorsSecurityHelper {
    public static bool IsOriginAllowed(string? origin, string[] allowedOrigins) {
        if (string.IsNullOrWhiteSpace(origin) || allowedOrigins is null) return false;
        var cleanOrigin = origin.Trim();
        foreach (var allowed in allowedOrigins) {
            if (string.Equals(cleanOrigin, allowed?.Trim(), StringComparison.OrdinalIgnoreCase)) {
                return true;
            }
        }
        return false;
    }
}""",
            "tests": [
                {"name": "Origine localhost:4200 consentita", "expression": 'CorsSecurityHelper.IsOriginAllowed("http://localhost:4200", new[] { "http://localhost:4200", "https://dev48.it" })', "expected": True},
                {"name": "Origine non autorizzata respinta", "expression": 'CorsSecurityHelper.IsOriginAllowed("http://malicious.com", new[] { "http://localhost:4200" })', "expected": False},
                {"name": "Origine nulla respinta", "expression": 'CorsSecurityHelper.IsOriginAllowed(null, new[] { "http://localhost:4200" })', "expected": False},
            ],
            "hints": [
                "Gestisci i casi di input nulli: `if (string.IsNullOrWhiteSpace(origin) || allowedOrigins is null) return false;`.",
                "Cicla sulle origini ammesse e confronta con `string.Equals(..., StringComparison.OrdinalIgnoreCase)`.",
                "Le origini web non devono contenere barre finali."
            ],
            "creative_goals": ["Confronto sicuro StringComparison.OrdinalIgnoreCase", "Nessun falso positivo su origini nulle"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 09: Testing xUnit & Vitest, Architettura Pulita
    # ==========================================
    (
        "09_quality_testing", "Test unitari in C# con xUnit", 45, True,
        "Scrivere test unitari affidabili e manutenibili per i servizi e la logica di business .NET.",
        "xunit;[fact];[theory];assert;arrange act assert;red green refactor",
        "I test unitari verificano che singoli metodi o componenti producano il risultato atteso per diversi input, proteggendo il codice da regressioni durante i refactoring.",
        "### Il Pattern Arrange - Act - Assert (AAA):\nIl modello Arrange–Act–Assert rende distinguibili tre responsabilità:\n1. **Arrange (Prepara)**: inizializza le variabili, crea gli oggetti e prepara l'ambiente di test.\n2. **Act (Esegui)**: invoca il metodo sotto test con i parametri stabiliti.\n3. **Assert (Verifica)**: controlla che il valore restituito o lo stato coincida con il risultato atteso.\n\n### Esempio con xUnit:\n```csharp\nusing Xunit;\n\npublic class CalculatorTests {\n    [Fact]\n    public void Add_TwoNumbers_ReturnsCorrectSum() {\n        // 1. Arrange\n        var calc = new Calculator();\n\n        // 2. Act\n        var result = calc.Add(10, 20);\n\n        // 3. Assert\n        Assert.Equal(30, result);\n    }\n\n    [Theory]\n    [InlineData(0, false)]\n    [InlineData(-5, false)]\n    public void IsPositive_VariousInputs_ReturnsExpected(int number, bool expected) {\n        var calc = new Calculator();\n        Assert.Equal(expected, calc.IsPositive(number));\n    }\n}\n```\n\nNel progetto di test aggiungi la classe usata dall’esempio (oppure referenzia il progetto che la contiene):\n```csharp\npublic class Calculator {\n    public int Add(int a, int b) => a + b;\n    public bool IsPositive(int number) => number > 0;\n}\n```\nEsegui `dotnet test Tests/Server.Tests.csproj` dalla cartella `server/` del laboratorio Suite di Test xUnit e Vitest. Prima fai fallire un test con un difetto controllato, poi correggi il metodo e verifica di nuovo.",
        'using Xunit;\n\npublic static class Service {\n    public static int Process(int value) => value * 2;\n}\n\npublic class ServiceTests {\n    [Fact]\n    public void Calculate_ValidInput_ReturnsExpected() {\n        var result = Service.Process(5);\n        Assert.Equal(10, result);\n    }\n}',
        '// Test che espone il difetto nel metodo da correggere:\n[Theory]\n[InlineData(5, true)]\n[InlineData(0, false)]\n[InlineData(-5, false)]\npublic void Positive_rule_matches_contract(int value, bool expected) {\n    Assert.Equal(expected, NumberRules.IsPositive(value));\n}',
        "Scrivere test che dipendono dal database reale o dalla rete (rallentano la suite e falliscono a intermittenza); inserire troppe verifiche non correlate nello stesso test.",
        "Qual è la differenza fondamentale tra l'attributo `[Fact]` e `[Theory]` in xUnit?",
        {'kind': 'csharp',
 'title': 'Debugging di un caso limite scoperto da un test',
 'prompt': 'Una Theory dichiara IsPositive(5) = true, IsPositive(0) = false e IsPositive(-5) = false. Lo '
           'starter fallisce soltanto il caso zero. Correggi `NumberRules.IsPositive(int number)` senza '
           'cambiare gli esiti attesi. Poi, nel laboratorio Suite di Test xUnit e Vitest, traduci questi tre '
           'casi in InlineData: qui il runner verifica il metodo C#, non gli attributi xUnit.',
 'starter': 'public static class NumberRules {\n'
            '    public static bool IsPositive(int number) => number >= 0;\n'
            '}',
 'solution': 'public static class NumberRules {\n'
             '    public static bool IsPositive(int number) => number > 0;\n'
             '}',
 'tests': [{'name': 'Numero positivo', 'expression': 'NumberRules.IsPositive(5)', 'expected': True},
           {'name': 'Zero non positivo', 'expression': 'NumberRules.IsPositive(0)', 'expected': False},
           {'name': 'Numero negativo', 'expression': 'NumberRules.IsPositive(-5)', 'expected': False},
           {'name': 'Minimo positivo', 'expression': 'NumberRules.IsPositive(1)', 'expected': True}],
 'hints': ['Confronta il risultato del caso zero con la specifica, prima di cambiare il test.',
           'Il termine positivo esclude lo zero.',
           'La differenza è nel confronto > rispetto a >=.']}
    ),
    (
        "09_quality_testing", "Testare componenti Angular con Vitest e TestBed", 45, True,
        "Usare Vitest e TestBed per creare un componente standalone e verificare il comportamento osservabile nel DOM.",
        "vitest;testbed;componentfixture;dom;expect;change detection",
        "Vitest esegue i test; TestBed crea il contesto Angular e ComponentFixture permette di osservare il componente e il suo DOM. Un test di componente verifica ciò che vede o fa l'utente, non solo una classe costruita con `new`.",
        """### Test di un componente Standalone con TestBed:
```typescript
import { TestBed } from '@angular/core/testing';
import { CounterComponent } from './counter.component';

describe('CounterComponent', () => {
  it('mostra il valore e lo aggiorna dopo un click', async () => {
    await TestBed.configureTestingModule({ imports: [CounterComponent] }).compileComponents();
    const fixture = TestBed.createComponent(CounterComponent);
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.querySelector('[data-count]')?.textContent).toContain('0');
    element.querySelector('button')?.click();
    fixture.detectChanges();
    expect(element.querySelector('[data-count]')?.textContent).toContain('1');
  });
});
```""",
        "describe('Component', () => {\n  it('mostra il titolo nel DOM', async () => {\n    await TestBed.configureTestingModule({ imports: [MyComponent] }).compileComponents();\n    const fixture = TestBed.createComponent(MyComponent);\n    fixture.detectChanges();\n    expect(fixture.nativeElement.textContent).toContain('Home');\n  });\n});",
        """export class TestResultSummary {
    passed = signal(0);
    failed = signal(0);
    recordPass() { this.passed.update(n => n + 1); }
    recordFail() { this.failed.update(n => n + 1); }
    isAllPassed = computed(() => this.failed() === 0 && this.passed() > 0);
}""",
        "Testare solo metodi privati senza osservare il DOM; dimenticare di attivare la change detection quando serve; costruire direttamente un componente Angular che usa dipendenze Angular.",
        "Quali parti di Angular prepara TestBed quando crea un componente per il test?",
        {
            "kind": "angular",
            "title": "Riepilogo Risultati Suite di Test",
            "prompt": "Implementa `TestResultSummary` con i segnali `passed = signal(0)` e `failed = signal(0)`, i metodi `recordPass()` e `recordFail()`, e `isAllPassed` come `computed()` che restituisce true solo se failed è 0 e passed è maggiore di 0.",
            "starter": """export class TestResultSummary {
    passed = signal(0);
    failed = signal(0);
    // TODO: definisci isAllPassed con computed()

    recordPass() {
        // TODO: incrementa passed
    }

    recordFail() {
        // TODO: incrementa failed
    }
}""",
            "solution": """export class TestResultSummary {
    passed = signal(0);
    failed = signal(0);
    isAllPassed = computed(() => this.failed() === 0 && this.passed() > 0);

    recordPass() {
        this.passed.update(n => n + 1);
    }

    recordFail() {
        this.failed.update(n => n + 1);
    }
}""",
            "tests": [
                {"name": "Inizialmente isAllPassed è false", "expression": "(new TestResultSummary()).isAllPassed()", "expected": False},
                {"name": "Tutti test passati rende isAllPassed true", "expression": "(() => { const s = new TestResultSummary(); s.recordPass(); s.recordPass(); return s.isAllPassed(); })()", "expected": True},
                {"name": "Anche un solo fallimento rende isAllPassed false", "expression": "(() => { const s = new TestResultSummary(); s.recordPass(); s.recordFail(); return s.isAllPassed(); })()", "expected": False},
            ],
            "hints": [
                "Per `isAllPassed`: `computed(() => this.failed() === 0 && this.passed() > 0)`.",
                "In `recordPass`: `this.passed.update(n => n + 1);`.",
                "In `recordFail`: `this.failed.update(n => n + 1);`."
            ],
            "creative_goals": ["Tracciamento metriche con Signals", "Calcolo aggregato glitch-free con computed"],
            "bonus_xp": 20
        }
    ),
    (
        "09_quality_testing", "Principi SOLID applicati allo sviluppo Full-Stack", 45, True,
        "Applicare i principi Single Responsibility, Open/Closed, Liskov, Interface Segregation e Dependency Inversion.",
        "solid;single responsibility;open closed;liskov;interface segregation;dependency inversion",
        "I principi SOLID guidano la progettazione del software verso classi modulari, a basso accoppiamento e con responsabilità uniche, facili da mantenere ed estendere nel tempo.",
        """### I 5 Principi SOLID in breve:
1. **S - Single Responsibility Principle (SRP)**: una classe deve avere una sola ragione per cambiare (es. un componente non deve occuparsi di chiamate HTTP, delega a un Servizio).
2. **O - Open/Closed Principle (OCP)**: aperto all'estensione, chiuso alla modifica (usare interfacce o polimorfismo invece di modificare classi esistenti).
3. **L - Liskov Substitution Principle (LSP)**: le classi derivate devono poter sostituire le classi base senza rompere il comportamento del programma.
4. **I - Interface Segregation Principle (ISP)**: meglio molte interfacce piccole e specifiche che un'unica interfaccia monolitica piena di metodi non necessari.
5. **D - Dependency Inversion Principle (DIP)**: i moduli di alto livello non devono dipendere dai dettagli di basso livello; entrambi devono dipendere da astrazioni (interfacce).""",
        "public sealed record User(string Name);\n\npublic static class UserValidator {\n    public static bool IsValid(User user) => !string.IsNullOrWhiteSpace(user.Name);\n}\n\npublic interface IUserRepository {\n    void Save(User user);\n}",
        """public interface IDiscountStrategy { decimal ApplyDiscount(decimal price); }
public class NoDiscount : IDiscountStrategy { public decimal ApplyDiscount(decimal p) => p; }
public class HalfPriceDiscount : IDiscountStrategy { public decimal ApplyDiscount(decimal p) => p * 0.5m; }""",
        "Creare 'God Objects' (classi monolitiche con migliaia di righe che fanno tutto: routing, DB, validazione e UI); violare il principio di inversione delle dipendenze istanziando direttamente classi concrete.",
        "Quale principio SOLID viene violato quando una classe esegue contemporaneamente calcoli di business e interrogazioni dirette al database?",
        {
            "kind": "csharp",
            "title": "Open/Closed con Strategia di Sconto",
            "prompt": "Definisci l'interfaccia `public interface IDiscountStrategy { int Apply(int price); }` e implementa `public class PercentageDiscount : IDiscountStrategy` con costruttore `(int percent)` che riduce il prezzo di quella percentuale (es. 20% su 100 -> 80).",
            "starter": """public interface IDiscountStrategy {
    int Apply(int price);
}

// TODO: Implementa PercentageDiscount
public class PercentageDiscount : IDiscountStrategy {
    private readonly int _percent;

    public PercentageDiscount(int percent) {
        _percent = percent;
    }

    public int Apply(int price) {
        // TODO: applica lo sconto percentuale
        return price;
    }
}""",
            "solution": """public interface IDiscountStrategy {
    int Apply(int price);
}

public class PercentageDiscount : IDiscountStrategy {
    private readonly int _percent;

    public PercentageDiscount(int percent) {
        _percent = percent;
    }

    public int Apply(int price) => price - (price * _percent / 100);
}""",
            "tests": [
                {"name": "Sconto 20% su 100 restituisce 80", "expression": "(new PercentageDiscount(20)).Apply(100)", "expected": 80},
                {"name": "Sconto 50% su 50 restituisce 25", "expression": "(new PercentageDiscount(50)).Apply(50)", "expected": 25},
                {"name": "Sconto 0% restituisce prezzo invariato", "expression": "(new PercentageDiscount(0)).Apply(100)", "expected": 100},
            ],
            "hints": [
                "La formula per il prezzo scontato è `price - (price * _percent / 100)`.",
                "Tutti i calcoli sono su valori interi `int`.",
                "Puoi scrivere il metodo con espressione sintetica `=>`."
            ],
            "creative_goals": ["Pattern Strategy conforme a Open/Closed", "Calcolo preciso con formula scalare"],
            "bonus_xp": 20
        }
    ),
    (
        "09_quality_testing", "Architettura Pulita: separazione di Domain, Application e API", 45, True,
        "Organizzare una soluzione enterprise isolando entità di dominio, casi d'uso e adapter infrastrutturali.",
        "clean architecture;onion architecture;domain layer;application layer;infrastructure;dependency rule",
        "La Clean Architecture stabilisce che le regole di business e il dominio centrale non devono dipendere da nessun framework esterno, database o libreria UI. I dettagli dipendono dal dominio, mai il contrario.",
        """### I Layer della Clean Architecture:
1. **Domain (Nucleo)**: Entità pure, Value Objects, eccezioni di dominio. Zero dipendenze esterne.
2. **Application (Casi d'Uso)**: DTO, interfacce dei repository, comandi e query di business. Dipende solo dal Domain.
3. **Infrastructure**: Implementazione concreta dei repository con EF Core, invio email, client HTTP esterni. Dipende da Application e Domain.
4. **API / Presentation**: Minimal API di ASP.NET Core o frontend Angular. Riceve le richieste e delega ai casi d'uso.""",
        "API endpoint -> caso d'uso Application -> regole Domain\n\nInfrastructure implementa i contratti dichiarati verso il centro. Domain non conosce database, ASP.NET Core o Angular.",
        """using System.Threading;
using System.Threading.Tasks;

public sealed record Subject(string Name);

public interface ISubjectRepository {
    Task SaveAsync(Subject subject, CancellationToken cancellationToken);
}

public sealed class RegisterSubject(ISubjectRepository repository) {
    public Task ExecuteAsync(Subject subject, CancellationToken cancellationToken) =>
        repository.SaveAsync(subject, cancellationToken);
}""",
        "Far dipendere il Domain da EF Core o da librerie web; saltare i layer e scrivere query SQL direttamente nei componenti UI.",
        "Qual è la regola cardinale della Clean Architecture riguardo alla direzione delle dipendenze?",
        {
            "kind": "csharp",
            "title": "Verificatore Regola di Dipendenza Architetturale",
            "prompt": "Implementa `ArchitectureRules.CanReference(string fromLayer, string toLayer)` con queste regole: `Application` può dipendere solo da `Domain`; `Infrastructure` può dipendere da `Application` o `Domain`; `Api` può dipendere da `Application`; `Domain` non dipende da altri layer. Restituisci false per ogni altra coppia.",
            "starter": """public static class ArchitectureRules {
    public static bool CanReference(string fromLayer, string toLayer) {
        // TODO: implementa i controlli sulle regole di dipendenza
        return false;
    }
}""",
            "solution": """public static class ArchitectureRules {
    public static bool CanReference(string fromLayer, string toLayer) {
        if (fromLayer == "Domain") return false;
        if (fromLayer == "Application") return toLayer == "Domain";
        if (fromLayer == "Infrastructure") return toLayer == "Application" || toLayer == "Domain";
        if (fromLayer == "Api") return toLayer == "Application";
        return false;
    }
}""",
            "tests": [
                {"name": "Domain non può dipendere da Infrastructure", "expression": 'ArchitectureRules.CanReference("Domain", "Infrastructure")', "expected": False},
                {"name": "Application può dipendere da Domain", "expression": 'ArchitectureRules.CanReference("Application", "Domain")', "expected": True},
                {"name": "Application non può dipendere da API", "expression": 'ArchitectureRules.CanReference("Application", "Api")', "expected": False},
                {"name": "Infrastructure può implementare il contratto Application", "expression": 'ArchitectureRules.CanReference("Infrastructure", "Application")', "expected": True},
                {"name": "API può chiamare Application", "expression": 'ArchitectureRules.CanReference("Api", "Application")', "expected": True},
                {"name": "Layer sconosciuto rifiutato", "expression": 'ArchitectureRules.CanReference("Unknown", "Domain")', "expected": False},
            ],
            "hints": [
                "Se `fromLayer == \"Domain\"`, restituisci sempre `false`.",
                "Se `fromLayer == \"Application\"`, restituisci `toLayer == \"Domain\"`.",
                "Per tutti gli altri strati superiori puoi consentire la referenza."
            ],
            "creative_goals": ["Rigoroso rispetto della Dependency Rule", "Early return pulito"],
            "bonus_xp": 20
        }
    ),

    # ==========================================
    # MODULO 10: Laboratori Monorepo & Portfolio Creativo
    # ==========================================
    (
        "10_portfolio_monorepo", "Organizzazione Monorepo: client/ e server/", 35, True,
        "Gestire l'architettura monorepo unificando frontend Angular e backend .NET nello stesso repository.",
        "monorepo;client;server;shared contracts;git;struttura cartelle",
        "Un monorepo racchiude client e server nello stesso repository e permette di versionare insieme modifiche collegate. Dipendenze, build e contratti tra i progetti restano da configurare e verificare.",
        """### Struttura Standard di un Monorepo Full-Stack:
```text
mio-progetto/
├── client/                     # Applicazione Angular 22 Standalone
│   ├── src/app/
│   ├── package.json
│   └── tsconfig.json
├── server/                     # Web API ASP.NET Core (.NET 10)
│   ├── Program.cs
│   ├── Controllers/ o Endpoints/
│   └── Server.csproj
├── README.md                   # Documentazione di avvio e architettura
└── .gitignore
```""",
        "# Terminale 1, dalla cartella server/:\ndotnet run\n\n# Terminale 2, dalla cartella client/:\nnpm start",
        """public static class MonorepoStructureValidator {
    public static bool HasClientAndServer(bool hasClient, bool hasServer) => hasClient && hasServer;
}""",
        "Dare per scontato che il monorepo condivida automaticamente tipi o dipendenze; mantenere i manifest nei progetti corretti e verificare il contratto HTTP tra client e server.",
        "Quale vantaggio pratico offre un Monorepo per il rilascio congiunto di modifiche a client e server?",
        {
            "kind": "csharp",
            "title": "Validatore Presenza Monorepo",
            "prompt": "Implementa `MonorepoStructureValidator.IsComplete(bool hasClient, bool hasServer, bool hasReadme)` che restituisce true solo se tutte e tre le parti fondamentali sono presenti.",
            "starter": """public static class MonorepoStructureValidator {
    public static bool IsComplete(bool hasClient, bool hasServer, bool hasReadme) {
        // TODO: restituisci true se tutti i flag sono true
        return false;
    }
}""",
            "solution": """public static class MonorepoStructureValidator {
    public static bool IsComplete(bool hasClient, bool hasServer, bool hasReadme) =>
        hasClient && hasServer && hasReadme;
}""",
            "tests": [
                {"name": "Tutti i componenti presenti", "expression": "MonorepoStructureValidator.IsComplete(true, true, true)", "expected": True},
                {"name": "Client mancante", "expression": "MonorepoStructureValidator.IsComplete(false, true, true)", "expected": False},
                {"name": "Readme mancante", "expression": "MonorepoStructureValidator.IsComplete(true, true, false)", "expected": False},
            ],
            "hints": [
                "Usa l'operatore logico AND: `hasClient && hasServer && hasReadme`.",
                "Puoi scrivere il metodo con expression-body `=>`.",
                "Un progetto di portfolio richiede sempre un README esplicativo."
            ],
            "creative_goals": ["Usa expression-bodied member", "Verifica tripla simultanea"],
            "bonus_xp": 20
        }
    ),
    (
        "10_portfolio_monorepo", "Progettazione dell'esperienza utente e feedback visivo", 40, True,
        "Creare interfacce piacevoli con stati di caricamento skeleton, toast di notifica e micro-interazioni.",
        "ux;skeleton loader;toast;accessibilita;micro-interazioni;feedback visivo",
        "Per operazioni che richiedono attesa o possono fallire, un feedback chiaro aiuta a capire se l'azione è stata avviata e come è terminata.",
        """### I Tre Stati di Qualsiasi Operazione Asincrona:
1. **Pending (In Corso)**: disabilita il pulsante di submit per prevenire doppi invii e mostra un indicatore visivo.
2. **Success (Completata)**: mostra un toast o messaggio temporaneo di successo e aggiorna la lista.
3. **Error (Fallita)**: evidenzia il campo errato o mostra una notifica chiara con ProblemDetails.""",
        "<!-- Disabilitare pulsante e mostrare spinner mentre isSaving() è true -->\n<button [disabled]=\"isSaving()\">\n  @if (isSaving()) { <span>Salvataggio...</span> } @else { <span>Salva</span> }\n</button>",
        """export class UiFeedbackModel {
    status = signal('idle');
    start() { this.status.set('busy'); }
    finishSuccess() { this.status.set('success'); }
    finishError() { this.status.set('error'); }
}""",
        "Non mostrare alcuno stato di caricamento lasciando credere all'utente che il click non sia stato registrato.",
        "Quali problemi previeni disabilitando il pulsante durante una richiesta, e che cosa devi fare se fallisce?",
        {
            "kind": "angular",
            "title": "Gestore Stato UI per Feedback Visivo",
            "prompt": "Implementa `UiFeedbackModel` con il segnale `status = signal('idle')`, i metodi `start()`, `finishSuccess()`, `finishError()`, e `canInteract` come `computed()` (true solo se status non è 'busy').",
            "starter": """export class UiFeedbackModel {
    status = signal("idle");
    // TODO: definisci canInteract con computed()

    start() {
        // TODO: imposta status su 'busy'
    }

    finishSuccess() {
        // TODO: imposta status su 'success'
    }

    finishError() {
        // TODO: imposta status su 'error'
    }
}""",
            "solution": """export class UiFeedbackModel {
    status = signal("idle");
    canInteract = computed(() => this.status() !== "busy");

    start() {
        this.status.set("busy");
    }

    finishSuccess() {
        this.status.set("success");
    }

    finishError() {
        this.status.set("error");
    }
}""",
            "tests": [
                {"name": "Stato iniziale consente interazione", "expression": "(new UiFeedbackModel()).canInteract()", "expected": True},
                {"name": "Start disabilita interazione", "expression": "(() => { const m = new UiFeedbackModel(); m.start(); return m.canInteract(); })()", "expected": False},
                {"name": "finishSuccess ripristina interazione", "expression": "(() => { const m = new UiFeedbackModel(); m.start(); m.finishSuccess(); return m.canInteract(); })()", "expected": True},
            ],
            "hints": [
                "Per `canInteract`: `computed(() => this.status() !== 'busy')`.",
                "Nei metodi, usa `.set('busy')`, `.set('success')`, `.set('error')`.",
                "Questo pattern previene doppi click accidentali su form e bottoni."
            ],
            "creative_goals": ["Stato unione rigoroso", "Proprietà derivata per il controllo di abilitazione pulsanti"],
            "bonus_xp": 20
        }
    ),
    (
        "10_portfolio_monorepo", "Documentazione delle API con OpenAPI", 40, True,
        "Esporre un documento OpenAPI generato da ASP.NET Core e aggiungere metadati alle rotte.",
        "openapi;documento json;addopenapi;mapopenapi;documentazione api;route metadata",
        "OpenAPI descrive in modo leggibile da strumenti il contratto di un'API. In .NET 10 `AddOpenApi()` registra il generatore e `MapOpenApi()` espone il documento JSON; un'interfaccia web come Swagger UI o Scalar è un pacchetto aggiuntivo.",
        """### Generare il documento OpenAPI in una Minimal API .NET 10:
Nel progetto aggiungi il pacchetto di generazione:
```powershell
dotnet add package Microsoft.AspNetCore.OpenApi --version 10.0.12
```

```csharp
builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment()) {
    app.MapOpenApi(); // In .NET 10 espone /openapi/v1.json
}
```

Gli endpoint possono essere arricchiti con nome, descrizione e tag:
```csharp
app.MapGet("/api/users", () => Results.Ok(new[] { "Ada", "Luca" }))
   .WithName("ListUsers")
   .WithTags("Utenti")
   .WithSummary("Restituisce l'elenco di tutti gli utenti registrati");
```

Per provare il documento con un'interfaccia web, scegli e installa una UI separata. La UI legge lo stesso documento OpenAPI e non sostituisce i test degli endpoint.""",
        "app.MapGet(\"/api/items\", () => Results.Ok())\n   .WithTags(\"Catalogo\")\n   .WithSummary(\"Recupera tutti gli articoli\");",
        """public static class OpenApiDocHelper {
    public static string FormatEndpointTitle(string tag, string summary) => $"[{tag.Trim()}] {summary.Trim()}";
}""",
        "Non inserire descrizioni o status code attesi negli endpoint rendendo la documentazione poco utile per chi sviluppa il frontend.",
        "Quali ruoli svolgono `AddOpenApi()` e `MapOpenApi()`, e perché l'interfaccia web è un elemento separato?",
        {
            "kind": "csharp",
            "title": "Formatta Titolo Documentazione Endpoint",
            "prompt": "Implementa `OpenApiDocHelper.FormatEndpointTitle(string tag, string summary)` che restituisce `$\"[{tag.Trim()}] {summary.Trim()}\"`.",
            "starter": """public static class OpenApiDocHelper {
    public static string FormatEndpointTitle(string tag, string summary) {
        // TODO: formatta come "[Tag] Summary"
        return "";
    }
}""",
            "solution": """public static class OpenApiDocHelper {
    public static string FormatEndpointTitle(string tag, string summary) =>
        $"[{(tag ?? "").Trim()}] {(summary ?? "").Trim()}";
}""",
            "tests": [
                {"name": "Formattazione standard", "expression": 'OpenApiDocHelper.FormatEndpointTitle("Users", "Get all registered users")', "expected": "[Users] Get all registered users"},
                {"name": "Pulizia spazi bianchi", "expression": 'OpenApiDocHelper.FormatEndpointTitle("  Orders  ", "  Create order  ")', "expected": "[Orders] Create order"},
            ],
            "hints": [
                "Usa `$\"[{tag.Trim()}] {summary.Trim()}\"`.",
                "Proteggi da possibili valori nulli con `(tag ?? \"\").Trim()`.",
                "L'espressione a freccia `=>` rende il codice compatto."
            ],
            "creative_goals": ["String interpolation sintetica", "Protezione da null"],
            "bonus_xp": 20
        }
    ),
    (
        "10_portfolio_monorepo", "Presentare il progetto: Git, README professionale e Portfolio", 45, True,
        "Documentare architettura, comandi e decisioni tecniche in modo che un'altra persona possa avviare e valutare il progetto.",
        "readme professionale;architettura;compromessi tecnici;openapi;swagger;portfolio github",
        "Un README permette di avviare e comprendere il progetto. Documenta l'architettura, le decisioni tecniche prese, i comandi di avvio e le future estensioni possibili.",
        """### Sezioni Indispensabili di un README Professionale:
1. **Titolo & Badge**: nome del progetto, versione di .NET e Angular.
2. **Architettura della Soluzione**: diagramma concettuale o elenco delle tecnologie adottate.
3. **Decisioni Tecniche e Compromessi**:
   - *Perché abbiamo scelto Minimal API invece dei Controller tradizionali?*
   - *Quale stato abbiamo rappresentato con Signals e quale configurazione di change detection usa il progetto?*
   - *Come abbiamo strutturato la sicurezza con JWT e Route Guards?*
4. **Istruzioni di Setup & Avvio Rapido**: comandi esatti per eseguire backend e frontend in locale.
5. **Suite di Test**: comandi per eseguire `dotnet test` e `npm test`.""",
        "# Archivio soggetti\n\n## Architettura\n- Frontend: Angular 22 standalone; Signals per lo stato derivato della schermata.\n- Backend: API Minimal .NET 10; EF Core per l'accesso al database.\n\n## Decisioni e compromessi\n- Le query di sola lettura usano AsNoTracking dove non serve modificare le entità.\n- L'autenticazione usa JWT firmati; il server valida token e autorizzazioni.\n\n## Avvio e test\n- `dotnet test server/Tests/Server.Tests.csproj`\n- `npm test --prefix client`",
        """public static class PortfolioSummaryHelper {
    public static string FormatBadge(string tech, string version) => $"[{tech.Trim()} v{version.Trim()}]";
}""",
        "Lasciare il README di default generato dalla CLI; non menzionare quali problemi risolve il progetto o nascondere i limiti noti.",
        "Cosa non dovrebbe mai mancare nel README di un progetto open-source o di portfolio?",
        {
            "kind": "csharp",
            "title": "Generatore Badge Tecnologie per README",
            "prompt": "Implementa `PortfolioSummaryHelper.FormatBadge(string tech, string version)` che restituisce `$\"[{tech.Trim()} v{version.Trim()}]\"`.",
            "starter": """public static class PortfolioSummaryHelper {
    public static string FormatBadge(string tech, string version) {
        // TODO: restituisci "[tech vVersion]"
        return "";
    }
}""",
            "solution": """public static class PortfolioSummaryHelper {
    public static string FormatBadge(string tech, string version) =>
        $"[{(tech ?? "").Trim()} v{(version ?? "").Trim()}]";
}""",
            "tests": [
                {"name": "Badge Angular 22", "expression": 'PortfolioSummaryHelper.FormatBadge("Angular", "22")', "expected": "[Angular v22]"},
                {"name": "Badge .NET 10 con spazi", "expression": 'PortfolioSummaryHelper.FormatBadge("  .NET  ", "  10.0  ")', "expected": "[.NET v10.0]"},
            ],
            "hints": [
                "Usa l'interpolazione di stringhe: `$\"[{tech.Trim()} v{version.Trim()}]\"`.",
                "Pulisci gli spazi con `.Trim()`.",
                "I badge nei README consentono ai selezionatori di identificare immediatamente lo stack tecnologico."
            ],
            "creative_goals": ["Formattazione pulita per documentazione Markdown", "Usa expression body member"],
            "bonus_xp": 20
        }
    ),
]


def infer_code_language(source: str) -> str:
    """Sceglie l'etichetta del blocco dal contenuto, non dal modulo della lezione."""
    code = source.strip()
    if not code:
        return "text"
    if code.startswith("# README") or code.startswith("# Architettura"):
        return "markdown"
    command_lines = [line.strip() for line in code.splitlines() if line.strip()]
    if command_lines and all(
        line.startswith(("dotnet ", "node ", "npm ", "ng ", "cd ", "# Avvio", "# Per ", "# Verifica"))
        for line in command_lines
    ):
        return "bash"
    if code.startswith("<Project") or code.startswith("<?xml"):
        return "xml"
    if re.search(r"(?:^|\n)\s*[.#:]?[\w-]+\s*\{[^}]*[\w-]+\s*:\s*[^}]+;", code, re.DOTALL):
        return "css"
    if re.search(
        r"\b(?:CancellationToken|IResult|Results\.|Task(?:<|\b)|ValueTask(?:<|\b))|"
        r"\bpublic\s+(?:sealed\s+|static\s+|abstract\s+)*(?:class|interface|record)\b",
        code,
    ):
        return "csharp"
    if re.search(r"\b(interface|type|export|import|signal|computed|inject|Routes|FormGroup|effect|bootstrapApplication|Validators)\b|:\s*(string|number|boolean|unknown)\b", code):
        return "typescript"
    if re.search(r"\b(public|private|record|var|builder\.|app\.Map|using System)\b|=>\s*Results\.", code):
        return "csharp"
    if re.search(r"<\w+[\s/>]|\[[\w-]+\]=|\([\w-]+\)=|@(?:if|for|switch|defer)\b", code):
        return "html"
    if code.startswith("{") and re.search(r'^\s*"[^\"]+"\s*:', code, re.MULTILINE):
        return "json"
    return "text"


def lesson_markdown(
    module: str,
    title: str,
    summary: str,
    concepts: str,
    simple_explanation: str,
    syntax_anatomy: str,
    example: str,
    pattern_guide: str,
    pitfalls: str,
    review_question: str,
    guided_walkthrough: str,
    study_context: str,
    practice_context: str,
) -> str:
    concept_items = [f"- `{x.strip()}`" for x in concepts.split(";")]
    concept_list = "\n".join(concept_items)
    pitfall_items = [f"- {x.strip()}" for x in pitfalls.split(";")]
    pitfalls_list = "\n".join(pitfall_items)
    example_lang = infer_code_language(example)
    pattern_lang = infer_code_language(pattern_guide)
    # Early practice has a nearby syntax reference. Later modules rely on the
    # worked framework example and the exercise's own starter, so the lesson
    # does not reveal the short exercise's implementation before the attempt.
    show_pattern = module[:2] in {"00", "01", "02", "03", "04", "05"} or title in {
        "Principi SOLID applicati allo sviluppo Full-Stack",
        "Architettura Pulita: separazione di Domain, Application e API",
    }
    pattern_block = f"```{pattern_lang}\n{pattern_guide}\n```" if show_pattern else ""

    markdown = f"""# {title}

## In parole semplici

L'obiettivo di questa lezione è {summary[0].lower() + summary[1:]}

{simple_explanation}

{study_context}

## Le parole da riconoscere

{concept_list}

## Anatomia e Sintassi del Codice

{syntax_anatomy}

## Un esempio concreto

```{example_lang}
{example}
```

### Seguilo passo per passo

{guided_walkthrough}

## Pattern Guida per gli Esercizi

{practice_context}

{pattern_block}

## Dove ci si confonde spesso

{pitfalls_list}

## Domanda di verifica

> {review_question}

"""
    return re.sub(r"\n{3,}", "\n\n", markdown).rstrip() + "\n"


LABS_DATA = [
    ("lab-net-csharp-crud", "01_csharp", "CRUD in memoria con C# e LINQ", 75, "Implementa un archivio in memoria con ricerca, aggiornamento, rimozione, validazione e test unitari.", "dotnet"),
    ("lab-ts-angular-models", "02_typescript", "Modelli TypeScript e Contratti Web", 45, "Progetta un set completo di interfacce e union discriminate per un'applicazione di gestione ordini.", "angular"),
    ("lab-aspnet-minimal-api", "03_aspnet_api", "Web API con Minimal API e DTO", 60, "Costruisci da zero un servizio RESTful con Minimal API, dependency injection e validazione DTO.", "dotnet"),
    ("lab-angular-standalone", "04_angular_core", "Catalogo Standalone con Control Flow", 65, "Sviluppa una pagina catalogo con i nuovi blocchi @if, @for (track) e visualizzazione a schede.", "angular"),
    ("lab-angular-signals-state", "05_angular_signals", "Dashboard Reattiva con Angular Signals", 70, "Costruisci una dashboard di metriche che calcola totali e percentuali tramite computed(); usa effect solo per sincronizzare risorse esterne quando serve.", "angular"),
    ("lab-efcore-sqlite-db", "06_efcore", "Persistenza con EF Core e SQLite", 75, "Configura DbContext, relazioni 1:N tra soggetti e misure, e crea e applica migrazioni dalla CLI in sviluppo locale.", "dotnet"),
    ("lab-angular-reactive-forms", "07_angular_forms_routing", "Form Reattivo con Validazione Remota", 70, "Implementa un form Angular completo di controlli, validatori sincroni e verifica asincrona.", "angular"),
    ("lab-angular-routing-guard", "07_angular_forms_routing", "Navigazione SPA e Route Guard Funzionali", 60, "Configura le rotte con lazy-loading e proteggi le pagine sensibili con canActivateFn.", "angular"),
    ("lab-fullstack-jwt-auth", "08_security_fullstack", "Autenticazione JWT Full-Stack", 90, "Genera token Bearer nel backend ASP.NET Core e collegali tramite HttpInterceptor in Angular.", "monorepo"),
    ("lab-testing-xunit-vitest", "09_quality_testing", "Suite di Test xUnit e Vitest", 75, "Scrivi test unitari su metodi di business C# e test comportamentali su componenti Angular.", "monorepo"),
    ("lab-fullstack-monorepo-crud", "10_portfolio_monorepo", "Gestionale Full-Stack Monorepo", 110, "Collega client Angular Standalone e server .NET Web API con operazioni CRUD complete.", "monorepo"),
    ("lab-portfolio-enterprise", "10_portfolio_monorepo", "Progetto Finale di Portfolio Enterprise", 130, "Realizza un'applicazione completa con architettura pulita, documentazione OpenAPI, un’interfaccia comprensibile e decisioni progettuali motivate.", "monorepo"),
]

LAB_CRITERIA = {
    "lab-net-csharp-crud": (
        ["Crea o aggiorna un archivio in memoria usando classi e collezioni C#.", "Implementa ricerca, modifica e rimozione con LINQ o metodi di collezione appropriati.", "Gestisci identificativi assenti, input vuoti e collezione vuota.", "Aggiungi test xUnit per ogni operazione e per almeno un caso limite."],
        ["I metodi rispettano il risultato richiesto sui casi normali e limite.", "L'input non viene modificato quando il contratto richiede un nuovo risultato.", "I test xUnit sono piccoli e verificano un comportamento ciascuno."]
    ),
    "lab-ts-angular-models": (
        ["Definisci i DTO TypeScript per gli oggetti dell'ordine.", "Rappresenta gli stati di caricamento con una union discriminata.", "Scrivi una funzione che restringe il tipo con il campo discriminante.", "Verifica che i tipi e i casi di narrowing compilino con il TypeScript del progetto."],
        ["Campi obbligatori e facoltativi corrispondono al contratto dichiarato.", "Gli stati impossibili non sono rappresentabili nella union.", "Il controllo TypeScript passa senza ricorrere ad `any`."]
    ),
    "lab-aspnet-minimal-api": (
        ["Mappa endpoint GET, POST, PUT e DELETE per una risorsa semplice.", "Usa DTO distinti per i dati in ingresso e in uscita.", "Restituisci 200/201, 204, 400 e 404 nei casi corrispondenti.", "Aggiungi test automatici per l'endpoint di successo e gli errori previsti."],
        ["Le rotte e i codici HTTP rispettano il contratto dichiarato.", "Input mancanti o non validi non vengono salvati.", "I test coprono almeno una risposta di errore."]
    ),
    "lab-angular-standalone": (
        ["Crea un componente Angular standalone per mostrare un catalogo di schede.", "Usa `@for` con `track` per le righe e `@if` per gli stati vuoto e selezionato.", "Collega almeno un pulsante a un'azione osservabile.", "Verifica il DOM generato con TestBed e Vitest."],
        ["La lista mostra tutti gli elementi e usa una chiave stabile.", "Lo stato vuoto e lo stato selezionato sono comprensibili.", "I test verificano ciò che appare nel DOM."]
    ),
    "lab-angular-signals-state": (
        ["Rappresenta dati modificabili con `signal()`.", "Deriva totali e percentuali con `computed()`.", "Aggiungi e rimuovi elementi senza mutare la lista precedente.", "Testa valori iniziali, aggiornamenti e lista vuota."],
        ["I valori derivati riflettono lo stato corrente senza duplicare stato.", "Le operazioni su collezioni producono valori aggiornati.", "I test coprono almeno l'insieme vuoto e un aggiornamento."]
    ),
    "lab-efcore-sqlite-db": (
        ["Definisci entità e relazioni con chiavi esplicite.", "Registra `DbContext` e SQLite con dependency injection.", "Crea e applica una migrazione al database del progetto.", "Usa query asincrone e testa creazione e lettura su un database di test."],
        ["Il modello e la relazione vengono salvati e ricaricati correttamente.", "Le letture non modificanti evitano tracking quando serve.", "Il test usa un database isolato e non dipende da dati esterni."]
    ),
    "lab-angular-reactive-forms": (
        ["Crea un form standalone con controlli tipizzati e ReactiveFormsModule.", "Aggiungi validazione sincrona e messaggi per i campi non validi.", "Rappresenta lo stato pending durante una verifica remota simulata.", "Testa input vuoto, input valido e stato di invio."],
        ["Il form non si invia finché i controlli sono invalidi o pending.", "Gli errori compaiono vicino al campo e sono comprensibili.", "Il test verifica il comportamento del form, non solo la configurazione." ]
    ),
    "lab-angular-routing-guard": (
        ["Configura le rotte con `provideRouter` e un componente caricato in lazy loading.", "Aggiungi una guard funzionale che restituisce `true` o un `UrlTree`.", "Mostra la pagina richiesta o il login secondo lo stato del servizio.", "Verifica entrambe le navigazioni con test Angular."],
        ["La rotta pubblica resta raggiungibile.", "La rotta privata reindirizza chi non è autenticato.", "La lezione chiarisce che la guard migliora il flusso UI e non protegge l'API."]
    ),
    "lab-fullstack-jwt-auth": (
        ["Completa l’emissione del token nella rotta login didattica e configura la validazione di firma, issuer, audience e scadenza.", "Leggi la chiave da User Secrets o variabile d'ambiente, mai da un file committato.", "Proteggi un endpoint per utenti autenticati e uno con policy Admin; verifica 401, 403 e 200 con test.", "Aggiungi il Bearer token dal client solo verso l'origine dell'API."],
        ["Una richiesta senza token riceve 401; un ruolo Reader non accede alla rotta Admin (403); Admin accede (200).", "Il token valido è verificato dal backend e le policy di ruolo vengono applicate lì.", "Nessun segreto o token viene inserito nel repository."]
    ),
    "lab-testing-xunit-vitest": (
        ["Scrivi test xUnit per una regola di business C#.", "Scrivi test Vitest con TestBed per il comportamento visibile di un componente.", "Includi un caso valido e uno non valido per ogni area.", "Esegui i due runner separatamente e leggi il messaggio di un test fallito."],
        ["Ogni test controlla un comportamento dichiarato.", "I test Angular creano componenti con TestBed e osservano il DOM.", "Le suite si eseguono senza servizi esterni o rete."]
    ),
    "lab-fullstack-monorepo-crud": (
        ["Implementa API CRUD in ASP.NET Core e controlla gli status HTTP.", "Configura `HttpClient` Angular e un servizio tipizzato per la risorsa.", "Mostra caricamento, errore e lista vuota nel client.", "Testa API e client e documenta come avviare entrambi i processi."],
        ["Il client usa l'API reale e gestisce risposte ed errori.", "I dati non vengono duplicati in due fonti di stato indipendenti.", "Entrambe le suite di test passano con i comandi riportati nel README."]
    ),
    "lab-portfolio-enterprise": (
        ["Organizza un progetto finale con layer e responsabilità riconoscibili.", "Collega Angular a endpoint ASP.NET Core documentati con OpenAPI.", "Gestisci errori, loading e stato vuoto nel client.", "Completa README con prerequisiti, comandi, decisioni e limiti noti."],
        ["Un nuovo sviluppatore può avviare il progetto seguendo il README.", "Il backend valida input e autorizzazioni senza fidarsi del client.", "I test automatici coprono i flussi principali e un caso di errore."]
    ),
}

SIMULATIONS_DATA = [
    ("sim-csharp-30", "Pratica autonoma C# — circa 30 minuti", 30, "Ricevi una collezione di transazioni. Devi filtrarla con LINQ, calcolare totali raggruppati per categoria e gestire input non validi senza generare eccezioni non gestite.", ["Ripeti i requisiti con parole tue", "Usa record immutabili per i DTO", "Implementa filtri con LINQ senza alterare la collezione originale", "Verifica casi limite come lista vuota o valori nulli", "Spiega la complessità computazionale della soluzione"]),
    ("sim-angular-signals-45", "Pratica autonoma Angular Signals — circa 45 minuti", 45, "Costruisci un componente standalone reattivo che gestisce un carrello spesa: aggiunta, rimozione, calcolo subtotale e sconto con computed(), e salvataggio su localStorage con effect().", ["Inizializza i segnali con valori di default coerenti", "Usa computed() per i prezzi derivati evitando ricalcoli manuali", "Applica il nuovo blocco @for con clausola track obbligatoria", "Gestisci lo stato di carrello vuoto con il blocco @empty", "Dimostra il funzionamento reattivo delle modifiche"]),
    ("sim-debug-fullstack-45", "Debugging Full-Stack .NET & Angular — 45 minuti", 45, "Un'applicazione esistente non riceve i dati dal backend: analizza log C#, errori CORS del browser, status code HTTP e interceptor per correggere i bug in modo sistematico.", ["Isola se l'errore è nel server o nel client", "Controlla la configurazione della policy CORS in Program.cs", "Verifica che l'URL dell'API e le porte corrispondano", "Controlla il parsing dei tipi DTO JSON", "Esegui nuovamente i test per confermare la risoluzione"]),
    ("sim-portfolio-interview-60", "Revisione del progetto Full-Stack — circa 60 minuti", 60, "Avvia il progetto seguendo il README, segui una richiesta dal componente al database e scegli una piccola modifica da implementare. Usa il tempo come riferimento: completa il ciclo implementazione, debugging e verifica anche se richiede più di un’ora.", ["Avvia client e server usando i comandi documentati", "Segui una richiesta e descrivi dove vengono validati input e autorizzazioni", "Implementa una piccola estensione e verifica un caso valido e uno di errore", "Annota il difetto incontrato e come hai individuato la causa", "Aggiorna il README con la decisione presa e un limite ancora presente"]),
]

LEGACY_LESSON_TITLES = {
    # Conserva gli ID usati nel database locale anche quando il titolo è stato corretto.
    "CORS, Same-Origin, XSS e CSRF: scopi distinti": "CORS e protezione da vulnerabilità comuni (XSS, CSRF)",
    "Testare componenti Angular con Vitest e TestBed": "Test di componenti Angular con Vitest e Testing Library",
    "Test unitari in C# con xUnit": "Unit Test in C# con xUnit e FluentAssertions",
    "Documentazione delle API con OpenAPI": "Documentazione API con OpenAPI e Swagger UI",
}

INTERMEDIATE_LESSONS = {
    "Programmazione Asincrona: Task, async/await ed Eccezioni",
    "Generics essenziali per Collezioni e Risposte API",
    "Dependency Injection: Transient, Scoped e Singleton",
    "Validazione degli input e ProblemDetails standard",
    "Gestione globale delle eccezioni e Logging strutturato",
    "Deferrable Views: ottimizzazione con @defer",
    "Effetti collaterali controllati con effect()",
    "Comunicazione moderna tra componenti: input() e output()",
    "Introduzione a EF Core e DbContext",
    "Modellazione Entità e Relazioni 1:N e N:N",
    "Migrazioni di Database: Creazione e Applicazione",
    "Query con LINQ su Database: Tracking e AsNoTracking",
    "Scrittura atomica, Transazioni e SaveChangesAsync",
    "Validatori sincroni nativi e personalizzati",
    "Angular Router moderno e Lazy Loading",
    "Route Guards funzionali: Proteggere le rotte con canActivate",
    "Principi di sicurezza Web e architettura JWT",
    "Test unitari in C# con xUnit",
    "Testare componenti Angular con Vitest e TestBed",
    "Organizzazione Monorepo: client/ e server/",
    "Documentazione delle API con OpenAPI",
}

ADVANCED_LESSONS = {
    "Generazione e convalida token JWT in ASP.NET Core",
    "Consumo API autenticata con HttpClient e HttpInterceptor",
    "CORS, Same-Origin, XSS e CSRF: scopi distinti",
    "Principi SOLID applicati allo sviluppo Full-Stack",
    "Architettura Pulita: separazione di Domain, Application e API",
}

GUIDED_WALKTHROUGHS = {
    "Setup dell'ambiente moderno per Angular e .NET": """1. Esegui `dotnet --list-sdks`, `node --version` e `npm --version`: ogni comando controlla uno strumento diverso. Per compilare C# serve l'SDK, non basta il Runtime.
2. Lancia la CLI con `npx --yes @angular/cli@22.2.0 version`: npm scarica ed esegue la versione richiesta senza installazione globale.
3. Confronta le versioni stampate con quelle richieste dall'esercizio. Se il comando non viene trovato, riapri PowerShell dopo l'installazione e verifica il `PATH`.
4. Prova una seconda volta dopo aver aperto una nuova finestra del terminale: così distingui un problema di installazione da un `PATH` non ancora aggiornato.""",
    "Anatomia di una soluzione Full-Stack Client-Server": """1. Leggi l'URL `https://localhost:5001/api/items`: identifica protocollo, host, porta e percorso. Il browser invia la richiesta a quell'indirizzo.
2. Segui il percorso nel server: ASP.NET Core riceve la richiesta, esegue il gestore e può leggere dati prima di produrre la risposta JSON.
3. L'oggetto `{ id: 1, name: 'Item' }` è il corpo di risposta; il browser lo riceve e Angular può trasformarlo in una vista.
4. Nel codice C#, `TrimEnd('/')` e `TrimStart('/')` rimuovono barre nei punti adiacenti; prova `https://localhost:5001/` con `/api/items` e controlla l'URL risultante.""",
        "Metodo di debugging per API e Frontend": """1. Parti dal sintomo osservabile nel browser: errore JavaScript, schermata vuota o richiesta fallita. Non modificare codice ancora.
2. Apri Network e leggi URL, metodo e status code. Un `404` indica una rotta non trovata; un `500` sposta l'indagine sul server.
3. Se la richiesta non parte, controlla Console e componente Angular; se parte ma fallisce, confronta la risposta con il log del backend.
4. Nel classificatore, prova i limiti `199`, `200`, `299`, `300`, `400`, `499`, `500`, `599` e `600`: ogni `if` controlla una fascia e `return` termina il metodo appena trova quella giusta.""",
    "Il primo metodo C#: parametri, variabili e valore restituito": """1. Nella chiamata `Greeter.SayHello("Ada")`, il testo `Ada` è l'argomento che riempie il parametro `name`.
2. Dentro il metodo, la stringa viene unita a `"Ciao, "` e a `"!"`; il risultato diventa il valore della variabile locale `message`.
3. `return message` riporta `Ciao, Ada!` al punto chiamante, che lo assegna a `greeting` e lo stampa.
4. Prova un nome vuoto e poi un nome con spazi: il metodo concatena i caratteri ricevuti, non li valida né li ripulisce.""",
    "Tipi primitivi, tipi riferimento e nullable in C#": """1. Assegna `null` a `name`: con nullable reference types attivi, `string?` dichiara esplicitamente che l'assenza è prevista.
2. L'operatore `??` sceglie `"Utente Ospite"` solo quando `name` è `null`; altrimenti conserva il nome ricevuto.
3. `age` è un `int` e vale `25`; l'interpolazione inserisce entrambi i valori nella frase stampata.
4. Sostituisci `null` con `"Ada"` e controlla il risultato. Prova anche `int? age = null`: il punto interrogativo ha un ruolo diverso per un tipo valore.""",
    "Controllo di flusso, Pattern Matching e Switch Expressions": """1. Leggi insieme `role` e `isSuperUser`: la switch expression confronta la coppia, non soltanto il primo valore.
2. Il primo ramo applicabile produce la descrizione; per `("admin", true)` il risultato è `"Super Amministratore"`.
3. Il ramo `("user", _)` accetta qualunque secondo valore per l'utente. `_` significa che quel valore non serve alla decisione.
4. Prova una coppia non elencata: controlla se esiste un ramo che la gestisce o se il metodo deve rendere esplicita l'assenza di un caso valido.""",
    "Classi, Record e Costruttori Primari": """1. `new SubjectDto(1, "Mario", "Centro")` crea un record con tre proprietà inizializzate.
2. L'espressione `s1 with { Zone = "Nord" }` crea un nuovo record copiando gli altri valori e cambiando solo `Zone`.
3. `s1` conserva `"Centro"`; `s2` contiene `"Nord"`. I record confrontano i valori dichiarati, ma la copia è superficiale se una proprietà contiene un oggetto mutabile.
4. Confronta `s1` con un altro record creato con gli stessi tre valori. Poi cambia un valore e prevedi come cambia l'uguaglianza.""",
    "Collezioni moderne: List, Dictionary e Array": """1. `subjects` conserva tre nomi in ordine: una `List` si adatta quando l'elenco deve crescere o ridursi.
2. `lookup` associa la chiave intera `1` al valore `"Mario"`; `TryGetValue` prova la ricerca senza lanciare un'eccezione se la chiave manca.
3. Se la chiave esiste, `found` contiene il nome e il blocco stampa `Mario`; l'`if` non esegue il blocco per una chiave assente.
4. Cambia `1` in `99` e osserva il ramo non eseguito. Per ricerche ripetute, scegli una struttura in base alle operazioni necessarie, non solo alla complessità media.""",
    "LINQ fondamentale: Where, Select e Aggregazioni": """1. La lista iniziale contiene i numeri da 1 a 6. `Where` conserva quelli divisibili per 2: `2`, `4`, `6`.
2. `Select` trasforma ogni elemento rimasto moltiplicandolo per 2, quindi la sequenza diventa `4`, `8`, `12`.
3. `ToList()` esegue la query e materializza il risultato in una nuova lista; prima di quel punto, una query LINQ può essere valutata solo quando la enumeri.
4. Prova una lista vuota e poi rimuovi `ToList()`: descrivi quando viene eseguita la trasformazione e quante volte la enumerazione la ripete.""",
    "Programmazione Asincrona: Task, async/await ed Eccezioni": """1. `FetchDataAsync` restituisce un `Task<string>`: il chiamante riceve un'operazione da attendere, non una stringa immediata.
2. `await Task.Delay(50, ct)` sospende quel metodo fino al completamento o alla cancellazione; non blocca il thread con `.Wait()`.
3. Se il ritardo termina, il metodo restituisce `Dati per {id}`. Se il token annulla l'operazione, si verifica `OperationCanceledException`, che va trattata come cancellazione attesa.
4. Chiama il metodo con un token già annullato e poi con uno attivo. Distingui la cancellazione dagli errori imprevisti invece di catturare ogni eccezione come se fosse un successo.""",
    "TypeScript di base: variabili, funzioni e array": """1. `initialValues` è un array di numeri con valori `2` e `3`; l'annotazione `number[]` descrive il tipo degli elementi.
2. `sum` parte da `0` e il ciclo legge un valore alla volta, aggiungendolo a `total`.
3. Dopo il ciclo `total` vale `5`, quindi la funzione restituisce `5` e `console.log` lo mostra.
4. Prova `[]`: il ciclo non aggiunge nulla e il risultato resta `0`. Prova un array con tre valori per seguire tre aggiornamenti dell'accumulatore.""",
    "Tipi primitivi, Any vs Unknown e Type Inference": """1. TypeScript inferisce `age` come `number` dal valore `30`; non serve ripetere un tipo già evidente.
2. `JSON.parse` produce dati esterni: assegnarli a `unknown` impedisce di usarli come un tipo specifico prima di controllarli.
3. La condizione esclude `null` e verifica che il valore sia un oggetto. Questo esempio non dimostra però che l'oggetto contenga `id`: per quello serve una validazione del contratto.
4. Passa alla condizione una stringa, `null` e l'oggetto dell'esempio. Nota quali valori entrano nel blocco e quale controllo ulteriore servirebbe prima di leggere `id`.""",
    "Interfacce vs Type Alias e Contratti di Dati": """1. `UserDto` richiede `id` numerico e `name` testuale; `readonly` impedisce di riassegnare `id` attraverso quel tipo.
2. `role?` è facoltativo: un oggetto valido può ometterlo, ma se lo include deve fornire una stringa.
3. `Status` ammette soltanto i valori letterali `active` e `inactive`; una stringa diversa produce un errore TypeScript.
4. Aggiungi un oggetto con `role` assente e uno con `role: 7`. Poi prova `status: 'pending'` per distinguere i campi facoltativi dall'unione chiusa.""",
    "Union Discriminate e Type Narrowing": """1. Il campo `status` distingue i tre stati: `loading`, `success` ed `error`. Ogni variante espone solo i dati che le servono.
2. Con `status === 'success'`, TypeScript rende disponibile `data`; con `status === 'error'`, rende disponibile `message`.
3. Nel ramo `loading` non esiste né `data` né `message`. Una `switch` su `status` rende visibili i casi mancanti e può essere resa esaustiva con `never`.
4. Aggiungi uno stato `cancelled` con una propria proprietà e aggiorna il gestore. Controlla che non sia possibile leggere `message` da quello stato.""",
    "Generics essenziali per Collezioni e Risposte API": """1. In `PaginatedResponse<T>`, `T` rappresenta il tipo degli elementi contenuti in `items`; il totale resta un numero indipendente.
2. Quando usi `PaginatedResponse<UserDto>`, `items` diventa `UserDto[]` senza duplicare la struttura per ogni risorsa.
3. `wrapData<T>` riceve un valore e lo restituisce dentro `payload` conservando il tipo: se passa una stringa, `payload` è ancora una stringa.
4. Prova il wrapper con un numero e con un oggetto. Verifica che TypeScript segnali l'accesso a una proprietà che il tipo ricevuto non possiede.""",
    "Minimal API da zero: Program.cs e WebApplication": """1. `WebApplication.CreateBuilder(args)` prepara configurazione e servizi; `Build()` produce l'applicazione che riceverà le richieste.
2. `MapGet` associa una richiesta GET su `/api/hello` a una funzione che restituisce un risultato HTTP con un oggetto JSON.
3. `Run()` avvia il server e mantiene il processo in ascolto. La porta effettiva dipende dalla configurazione di avvio.
4. Apri l'URL completo riportato dal terminale e prova un percorso diverso. Confronta la risposta con la rotta registrata.""",
    "Dependency Injection: Transient, Scoped e Singleton": """1. Ogni riga registra un contratto (`ICache`, `IUserRepository`, `IEmailSender`) e la classe che lo implementa.
2. `Transient` crea un'istanza per ogni richiesta di servizio; `Scoped` riusa l'istanza nella richiesta web; `Singleton` mantiene un'istanza per la vita del contenitore.
3. ASP.NET Core risolve il servizio quando serve, per esempio nel costruttore di un endpoint o di un'altra classe. Il ciclo di vita influenza la condivisione dello stato.
4. Immagina due richieste HTTP e confronta cosa può essere condiviso. Non inserire una dipendenza `Scoped` in un `Singleton` senza progettare esplicitamente lo scope.""",
    "Routing, Parametri e Binding di Record DTO": """1. La rotta `/api/products/{id:int}` accetta un segmento numerico come `id`; `/api/products/abc` non soddisfa il vincolo.
2. `category` può arrivare dalla query string, ad esempio `/api/products/4?category=books`; il binding associa i valori ai parametri del gestore.
3. `Results.Ok` restituisce status 200 e un JSON con `id` e `category`. Un endpoint POST può invece ricevere un DTO dal body.
4. Prova a omettere `category`, poi invia un `id` non numerico. Osserva come cambia il binding e non confondere l'estrazione dei valori con la loro validazione.""",
    "Validazione degli input e ProblemDetails standard": """1. Il dizionario `errors` parte vuoto. Se `Email` è mancante o composta solo da spazi, il controllo registra un errore associato al campo.
2. `Results.ValidationProblem(errors)` costruisce una risposta di validazione con status 400 e struttura Problem Details.
3. Angular può leggere gli errori del body e mostrarli accanto al campo corrispondente; la risposta deve restare coerente con il contratto documentato.
4. Prova una email presente e una vuota. Per la prima il ramo di errore non deve scattare; per la seconda verifica status e nome del campo nella risposta.""",
    "Gestione globale delle eccezioni e Logging strutturato": """1. `UseExceptionHandler` registra il gestore che intercetta eccezioni non gestite nella pipeline; la sua posizione rispetto agli endpoint determina quali richieste copre.
2. `LogInformation` riceve un modello con `{UserId}` e il valore separato: il provider conserva un campo strutturato, utile per filtrare i log.
3. Un errore atteso di input va rappresentato con una risposta appropriata; il gestore globale è per errori imprevisti e non dovrebbe esporre lo stack trace al client.
4. Sostituisci il placeholder `{UserId}` con interpolazione e confronta il messaggio: la versione strutturata conserva meglio i campi interrogabili.""",
    "HTML essenziale e CSS per leggere i template Angular": """1. `<main>` racchiude il contenuto principale della pagina e `<h1>` ne identifica il titolo.
2. `label for="email"` punta all'`id="email"` dell'input: cliccare l'etichetta porta il focus al campo e uno screen reader ne legge il nome.
3. `type="email"` e `required` forniscono semantica e vincoli HTML di base; il pulsante invia il form, ma la logica Angular non è ancora presente.
4. Rimuovi temporaneamente `id` o cambia il valore di `for` e verifica perché l'associazione non funziona. Poi usa Tab e controlla che il focus resti visibile.""",
    "Progetto Angular Standalone e Bootstrap applicazione": """1. `bootstrapApplication(AppComponent, ...)` crea la radice Angular senza richiedere un modulo applicativo.
2. L'array `providers` registra servizi disponibili nell'app: `provideHttpClient()` configura `HttpClient` e `provideRouter(routes)` configura le rotte.
3. `main.ts` passa il componente radice e i provider; l'HTML iniziale deve contenere il selettore del componente, spesso `<app-root>`.
4. Togli un provider alla volta e individua l'errore che compare quando il componente tenta di usare quel servizio. Ripristinalo prima di proseguire.""",
    "Creazione di componenti Standalone con @Component": """1. `@Component` descrive il selettore e il template che Angular collega alla classe `CardComponent`.
2. Il template legge `title()` perché `title` è un Signal; le parentesi chiamano il getter del valore corrente.
3. Quando il genitore usa `<app-card>`, Angular crea il componente e mostra il titolo. Se il template usa altri componenti o pipe, il loro import va dichiarato.
4. Cambia il valore iniziale del Signal e prevedi il testo. Poi prova a leggere `title` senza parentesi e confronta il risultato col template.""",
    "Nuovo Control Flow: @if, @else, @for e @switch": """1. La condizione `users().length > 0` sceglie quale blocco del template mostrare.
2. Se la lista contiene utenti, `@for` crea una riga per ciascuno; `track user.id` associa ogni riga a una chiave stabile.
3. Se la lista è vuota, il blocco `@else` mostra `Lista vuota`. Con tre utenti, la vista produce tre `<div>`.
4. Prova una lista vuota e poi cambia un nome mantenendo lo stesso id. Il contenuto cambia, mentre l'identità stabile aiuta Angular a riutilizzare la riga appropriata.""",
    "Data Binding moderno: interpolazione, property ed event binding": """1. `[disabled]="!isValid()"` imposta la proprietà DOM `disabled` in base allo stato del componente; quando il form non è valido, il pulsante non è attivabile.
2. `(click)="onSubmit()"` ascolta un evento del browser e chiama il metodo TypeScript.
3. Nell'input, `[value]` mostra il valore del Signal `searchTerm()`; `(input)` chiama `updateSearch($event)` quando la persona scrive.
4. Simula `isValid()` prima falso e poi vero. Digita nel campo e verifica che l'handler trasferisca il nuovo testo nel componente.""",
    "Deferrable Views: ottimizzazione con @defer": """1. Prima che la vista entri nel viewport, `@placeholder` mostra un contenuto leggero al posto del grafico.
2. Quando la condizione `on viewport` si attiva, Angular carica il componente differito e sostituisce il placeholder.
3. Il caricamento ritardato può ridurre il codice iniziale solo se le dipendenze della vista sono effettivamente separabili e non vengono caricate altrove.
4. Prova `on interaction` e confronta quando parte il caricamento. Evita di differire un contenuto necessario subito o di lasciare uno stato vuoto senza indicazione.""",
    "Introduzione a signal() e aggiornamento stato con set() e update()": """1. `signal(0)` crea `count` con valore iniziale zero; `count()` legge il valore.
2. `set(5)` sostituisce il valore con cinque. `update(n => n + 1)` calcola il nuovo valore a partire da quello corrente.
3. Dopo i due aggiornamenti, `count()` restituisce `6`, che viene stampato da `console.log`.
4. Riprova con `update(n => n - 10)`: il risultato diventa negativo perché qui non esiste alcuna regola che lo impedisca. La logica dei limiti va aggiunta dove serve.""",
    "Valori derivati intelligenti con computed()": """1. `items()` restituisce `[10, 20, 30]`; `total` somma gli elementi e produce `60`.
2. `isFreeShipping` legge `total()`: dato che `60 >= 50`, il valore derivato è `true`.
3. `computed()` memorizza il risultato e ricalcola quando cambia un Signal effettivamente letto; non è il posto per chiamate HTTP o aggiornamenti di stato.
4. Aggiungi `5` agli articoli e verifica che il totale diventi `65`. Rimuovi un elemento e controlla come cambia la soglia della spedizione.""",
    "Effetti collaterali controllati con effect()": """1. L'effect legge `theme()`: questa lettura registra il Signal come dipendenza dell'effetto.
2. Quando l'effect viene creato, esegue il corpo e scrive nel log il tema corrente; una modifica successiva del Signal provoca una nuova esecuzione.
3. `console.log` è un effetto esterno, quindi è adatto a un effect. Il calcolo del nome del tema, invece, dovrebbe stare in `computed()`.
4. Cambia il tema due volte e osserva il log. Se l'effetto avvia una risorsa o un abbonamento, aggiungi una cleanup invece di crearne uno nuovo a ogni esecuzione.""",
    "Comunicazione moderna tra componenti: input() e output()": """1. `input.required<string>()` dichiara che il genitore deve fornire `title`; nel template il componente legge il valore con `title()`.
2. `output<number>()` dichiara un evento che trasporta un numero; non è un Signal che conserva lo stato.
3. `onSelect(id)` emette l'id con `selected.emit(id)`. Il genitore può ascoltarlo e decidere come aggiornare il proprio stato.
4. Prova a omettere `title` nel genitore e verifica il controllo Angular. Poi emetti un id diverso e controlla che arrivi al gestore del genitore.""",
    "Integrazione tra Signals e RxJS: toSignal e toObservable": """1. `toObservable(searchSignal)` espone le modifiche della query come un flusso RxJS.
2. `debounceTime(300)` attende una pausa di 300 ms; `switchMap` avvia la richiesta più recente e si disiscrive dal flusso precedente quando arriva un nuovo termine.
3. `toSignal(..., { initialValue: [] })` rende i risultati leggibili dal template fin da subito, prima della prima risposta.
4. Digita rapidamente due termini e poi fermati. La ricerca parte dopo la pausa; controlla inoltre errori HTTP e contesto d'iniezione prima di usare `toSignal`.""",
    "Introduzione a EF Core e DbContext": """1. `AppDbContext` eredita da `DbContext` e riceve le opzioni dal contenitore tramite il costruttore.
2. `DbSet<User> Users => Set<User>()` espone il punto di accesso tipizzato alle righe `User`; non crea da solo il database né sostituisce la configurazione del provider.
3. ASP.NET Core crea lo scope della richiesta e fornisce il contesto registrato con `AddDbContext`. Al termine dello scope, il contesto viene eliminato.
4. Segui una query da `db.Users` fino al provider SQLite configurato. Prova a registrare il contesto come singleton e spiega perché condividerlo tra richieste è pericoloso.""",
    "Modellazione Entità e Relazioni 1:N e N:N": """1. `Order` è il lato principale della relazione; `HasMany(o => o.Items)` dichiara che un ordine può avere molti articoli.
2. `WithOne(i => i.Order)` dichiara che ogni articolo appartiene a un ordine; `HasForeignKey(i => i.OrderId)` indica la colonna che conserva la chiave esterna.
3. EF Core usa la configurazione per creare lo schema e materializzare le navigation properties; le classi `Order` e `Item` devono esistere e avere chiavi valide.
4. Prova a salvare due articoli per un ordine e poi un articolo con chiave esterna inesistente. Individua quale vincolo applica il database.""",
    "Migrazioni di Database: Creazione e Applicazione": """1. `dotnet ef migrations add AddUserTable` confronta il modello corrente con lo snapshot e genera una migrazione nominata.
2. Esamina il codice generato e lo snapshot prima di applicarlo: la migrazione descrive come evolve lo schema, non è una copia di backup dei dati.
3. `dotnet ef database update` applica le migrazioni pendenti al database configurato e aggiorna la cronologia delle migrazioni.
4. Aggiungi una proprietà e genera una nuova migrazione. In produzione applica le modifiche con un passaggio di deploy controllato; evita l'applicazione automatica all'avvio.""",
    "Query con LINQ su Database: Tracking e AsNoTracking": """1. La query parte da `db.Users`, filtra le righe attive con `Where` e termina con `ToListAsync()`.
2. `AsNoTracking()` indica che EF Core non deve conservare quelle entità nel Change Tracker: è utile se la lettura non porterà a modifiche nello stesso contesto.
3. L'assenza di tracking può ridurre lavoro e memoria, ma il risultato dipende dalla query. Senza identity resolution, righe che rappresentano la stessa entità possono produrre istanze separate.
4. Seleziona un caso in cui vuoi aggiornare l'entità e confrontalo con una lettura solo per visualizzazione. Scegli in base al lavoro successivo, non al verbo HTTP.""",
    "Scrittura atomica, Transazioni e SaveChangesAsync": """1. `Add(order)` aggiunge l'ordine al Change Tracker; normalmente non invia ancora la modifica al database.
2. `await SaveChangesAsync()` invia le modifiche pendenti e, con un provider relazionale, EF Core usa di norma una transazione per rendere atomiche le modifiche di quella chiamata.
3. Se la chiamata riesce, il provider può valorizzare la chiave generata e il metodo restituisce il numero di entità interessate. La concorrenza può comunque produrre un conflitto.
4. Aggiungi due modifiche prima di salvare e poi provoca un errore di vincolo. Verifica quali modifiche vengono confermate e quando serve una transazione esplicita più ampia.""",
    "Reactive Forms: FormGroup e FormControl": """1. `fb.group` crea due controlli: `email` parte vuoto e `age` parte da `18`.
2. `Validators.required` e `Validators.email` controllano il valore email; `Validators.min(18)` controlla il minimo dell'età.
3. Il `FormGroup` aggrega valori e stato dei controlli. Un'età sotto 18 o un indirizzo non valido rende il form non valido; il template deve mostrare gli errori e impedire l'invio.
4. Confronta l'idea con il breve esempio Signal Forms: in Angular 22 è stabile e usa un modello signal; il laboratorio del corso continua con Reactive Forms per esercitare il modello esplicito.""",
    "Validatori sincroni nativi e personalizzati": """1. `minAgeValidator(18)` restituisce una funzione che Angular chiama con il controllo e il valore attuale.
2. Se il valore è almeno 18, il validatore restituisce `null`, che significa nessun errore; altrimenti restituisce un oggetto `minAge` con la soglia richiesta.
3. Il template può leggere quell'errore per mostrare un messaggio, ma `required` è un controllo separato: un campo opzionale vuoto non dovrebbe essere rifiutato per la sola età minima.
4. Prova `17`, `18` e un valore vuoto. Combina il validatore con `Validators.required` quando il campo è obbligatorio e osserva i due errori distinti.""",
    "Validatori asincroni: verifica remota via API": """1. `timer(300)` aspetta una breve pausa prima di avviare il controllo, così la verifica remota non parte a ogni singolo tasto.
2. `switchMap` passa il valore al servizio API; quando il server risponde, `map` converte `taken` in un errore Angular oppure in `null`.
3. Angular mantiene il controllo in stato `pending` mentre attende. L'invio deve restare disabilitato finché il validatore non ha terminato.
4. Prova un indirizzo disponibile, uno già usato e una modifica rapida mentre la richiesta è in corso. Gestisci anche gli errori di rete senza presentare un indirizzo come sicuramente libero.""",
    "Angular Router moderno e Lazy Loading": """1. La route associa il percorso `catalog` a una funzione che importa il file del componente solo quando la navigazione lo richiede.
2. `then(m => m.CatalogComponent)` seleziona l'export da mostrare; il componente deve comparire in un `<router-outlet>` presente nell'app.
3. Visitando `/catalog`, il Router carica il componente e mantiene la navigazione nella SPA. Un `routerLink` evita il ricaricamento completo della pagina.
4. Prova un percorso inesistente e aggiungi una route di fallback. Poi osserva nel Network quando viene scaricato il chunk del catalogo.""",
    "Route Guards funzionali: Proteggere le rotte con canActivate": """1. La guard inietta il servizio di autenticazione e legge `isAuthenticated()` prima di consentire la navigazione.
2. Se la persona è autenticata, restituisce `true`; altrimenti crea un `UrlTree` per `/login`, così il Router esegue il reindirizzamento.
3. La guard migliora il flusso dell'interfaccia, ma non è un confine di sicurezza: il backend deve autorizzare ogni richiesta protetta.
4. Prova entrambi gli stati e aggiungi un ruolo richiesto. Poi invia direttamente una richiesta HTTP all'API per verificare che il server applichi la propria autorizzazione.""",
    "Principi di sicurezza Web e architettura JWT": """1. L'header e il payload del JWT sono codificati in Base64URL: chi possiede il token può decodificarli e leggerli.
2. La firma consente al server di verificare che il token non sia stato alterato e che provenga da chi possiede la chiave; non cifra i dati.
3. Il client invia il token con `Authorization: Bearer ...`; il server controlla firma, issuer, audience e scadenza prima di usarne le claim.
4. Decodifica il payload di un token di prova e verifica che non contenga password o altri segreti. Considera come revocare un token prima della sua scadenza.""",
    "Generazione e convalida token JWT in ASP.NET Core": """1. In PowerShell inizializza User Secrets e genera una chiave casuale locale; il provider la rende leggibile da `builder.Configuration` in ambiente Development.
2. `AddJwtBearer` convalida firma, issuer, audience e scadenza. `UseAuthentication()` deve precedere `UseAuthorization()` perché prima si costruisce l'identità e poi si applicano le policy.
3. La rotta `/api/login` verifica credenziali solo dimostrative, crea claim di nome e ruolo e firma un token breve. `RequireAuthorization()` richiede un utente autenticato; `AdminOnly` controlla anche il ruolo.
4. Prova `/api/profile` senza token (401), con token Reader (200), poi `/api/admin` con Reader (403) e con Admin (200). Non distribuire questo emettitore demo: usa OAuth/OIDC per applicazioni reali.""",
    "Consumo API autenticata con HttpClient e HttpInterceptor": """1. L'interceptor legge il token dal servizio in memoria e controlla l'origine della richiesta prima di modificarla.
2. `req.clone({ setHeaders: ... })` crea una nuova richiesta con `Authorization: Bearer ...`; `HttpRequest` è immutabile.
3. Per l'API configurata, `next(cloned)` inoltra la richiesta autenticata. Per un'origine diversa o un token assente, il codice inoltra la richiesta originale.
4. Prova la chiamata alla tua API e una chiamata a un host esterno. Verifica che il token compaia solo nella prima; ricarica la pagina per osservare che questo esercizio in memoria non persiste e non copiarlo in `localStorage` senza valutare il modello di sicurezza.""",
    "CORS, Same-Origin, XSS e CSRF: scopi distinti": """1. `WithOrigins("http://localhost:4200")` dichiara quale origine browser può leggere la risposta; origine significa schema, host e porta.
2. Il browser può inviare una richiesta cross-origin e poi impedire a JavaScript di leggerne la risposta: CORS non autentica la persona né sostituisce le regole del server.
3. XSS riguarda l'esecuzione di contenuto ostile nel contesto della pagina; CSRF riguarda richieste indesiderate che sfruttano credenziali inviate automaticamente, come cookie.
4. Confronta token Bearer in header e cookie di sessione: cambia il rischio CSRF e la protezione necessaria. Non usare origini arbitrarie insieme a credenziali.""",
    "Test unitari in C# con xUnit": """1. Nella fase Arrange prepara l'input `5` e il servizio; non introdurre database o rete in un test unitario semplice.
2. La fase Act chiama `Service.Process(5)` una sola volta e conserva il risultato.
3. `Assert.Equal(10, result)` confronta il comportamento osservato con il valore atteso. Se il metodo restituisce un altro numero, xUnit indica il test fallito.
4. Prova un input limite con una seconda `[Theory]` o un altro `[Fact]`. Mantieni un solo comportamento principale per test, così un errore resta facile da diagnosticare.""",
    "Testare componenti Angular con Vitest e TestBed": """1. `TestBed.configureTestingModule({ imports: [MyComponent] })` prepara il contesto Angular e importa il componente standalone.
2. `createComponent` crea il componente; `detectChanges()` esegue il primo ciclo e aggiorna il DOM.
3. L'asserzione cerca il titolo nell'interfaccia visibile. Il test osserva ciò che la persona usa, non un metodo privato isolato.
4. Cambia un input o clicca un pulsante, attiva di nuovo la change detection e verifica il nuovo DOM. Se il componente usa servizi, fornisci un mock esplicito.""",
    "Principi SOLID applicati allo sviluppo Full-Stack": """1. Nel frammento SRP, `UserValidator` decide se i dati sono validi e `UserRepository` si occupa di salvarli: le responsabilità possono cambiare per motivi diversi.
2. La strategia `IDiscountStrategy` dell'esempio guida offre un contratto comune; `NoDiscount` ne è una implementazione concreta.
3. Il chiamante può dipendere dall'interfaccia e ricevere una strategia, invece di conoscere ogni classe concreta. Questo illustra Open/Closed e Dependency Inversion senza dimostrare da solo tutti i principi.
4. Aggiungi una strategia di sconto senza modificare il chiamante. Poi controlla che un sostituto rispetti lo stesso contratto e che l'interfaccia non obblighi classi a implementare metodi irrilevanti.""",
    "Architettura Pulita: separazione di Domain, Application e API": """1. Il Domain contiene regole e modelli centrali; non importa EF Core o ASP.NET Core.
2. Application coordina casi d'uso e dichiara le porte di cui ha bisogno; Infrastructure può implementare quelle porte usando EF Core.
3. API riceve richieste HTTP e compone i servizi. Le dipendenze puntano verso il centro: Domain non dipende dai dettagli esterni.
4. Segui una richiesta dal route handler al caso d'uso e al repository. Se trovi un `DbContext` nel Domain, sposta l'accesso al database verso Infrastructure.""",
    "Organizzazione Monorepo: client/ e server/": """1. `client/` contiene progetto Angular e manifest npm; `server/` contiene progetto ASP.NET Core e file .NET.
2. Apri un terminale nella cartella `server/` e avvia `dotnet run`; in un secondo terminale, entra in `client/` e avvia `npm start`.
3. I due processi condividono il repository e la cronologia Git, ma hanno dipendenze e comandi di avvio distinti. Il contratto HTTP deve restare coerente tra DTO C# e tipi TypeScript.
4. Cambia il nome di un campo nel backend senza aggiornare il client e osserva il mismatch. Documenta come verificare o generare il contratto condiviso.""",
    "Progettazione dell'esperienza utente e feedback visivo": """1. Quando parte il salvataggio, `isSaving()` disabilita il pulsante per evitare invii ripetuti.
2. Il template mostra `Salvataggio...` durante l'attesa e `Salva` quando l'operazione termina; la persona riceve un'indicazione visibile.
3. Al successo o all'errore, mostra un messaggio associato allo stato. Per i cambiamenti annunciabili aggiungi un'area `role="status"` o `role="alert"` con il comportamento appropriato.
4. Prova una rete lenta, un errore e un doppio click. Controlla tastiera e screen reader, non solo l'aspetto visivo.""",
    "Documentazione delle API con OpenAPI": """1. `AddOpenApi()` registra il servizio che genera il documento; `MapOpenApi()` pubblica il documento JSON, normalmente su `/openapi/v1.json`.
2. `WithTags` organizza gli endpoint e `WithSummary` aggiunge una descrizione leggibile a strumenti e persone.
3. L'interfaccia web come Swagger UI o Scalar è un pacchetto separato: il documento OpenAPI può esistere anche senza una UI interattiva.
4. Avvia l'API, apri il documento e verifica che rotta, metodo e risposta corrispondano al codice. Non inserire dati segreti nella documentazione pubblica.""",
    "Presentare il progetto: Git, README professionale e Portfolio": """1. Leggi ogni riga del README come un'affermazione verificabile: stack, comandi, decisioni e limiti devono corrispondere al progetto.
2. Descrivi Angular per lo stato e l'interfaccia, .NET per API e regole server, ed EF Core per la persistenza; specifica dove il codice è davvero eseguito.
3. Spiega un compromesso con un fatto osservabile. Signals gestisce stato reattivo; da solo non elimina Zone.js né garantisce un miglioramento prestazionale.
4. Segui i comandi di setup in una cartella pulita e verifica che il portfolio si avvii. Correggi ogni passaggio che richiede conoscenze non documentate.""",
}


REVIEW_ANSWERS = {
    "Setup dell'ambiente moderno per Angular e .NET": "Usa dotnet --list-sdks per trovare l'SDK 10 e node --version per leggere la versione Node; verifica anche npm e Angular CLI. La presenza del solo runtime .NET non dimostra che puoi compilare.",
    "Anatomia di una soluzione Full-Stack Client-Server": "Il client raccoglie l'azione, invia una richiesta HTTP e mostra la risposta. Il server valida dati e permessi, applica le regole e accede al database; il browser non deve essere la fonte delle autorizzazioni.",
    "Metodo di debugging per API e Frontend": "Controlla prima in Network se parte la richiesta e che risposta riceve, poi nei log server dove fallisce o quali dati restituisce, infine lo stato e il template Angular. Se non parte alcuna richiesta, indaga già l'evento del pulsante: non cercare un errore nel database senza evidenza.",
    "Il primo metodo C#: parametri, variabili e valore restituito": "Il parametro riceve l'argomento della chiamata; return consegna il risultato al chiamante e termina il metodo. SayHello riceve un nome e restituisce il saluto, che il chiamante può stampare o conservare.",
    "Tipi primitivi, tipi riferimento e nullable in C#": "Assegnare un tipo valore copia il valore; assegnare un riferimento copia il riferimento all'oggetto. Due riferimenti possono osservare le modifiche dello stesso oggetto; questo non significa che ogni tipo valore sia sempre sullo stack.",
    "Controllo di flusso, Pattern Matching e Switch Expressions": "La switch expression restituisce direttamente un valore scegliendo il primo pattern corrispondente. È adatta a una classificazione o un calcolo; un blocco switch può essere più leggibile quando ogni ramo esegue più istruzioni.",
    "Classi, Record e Costruttori Primari": "Un record è utile per dati con uguaglianza per valore, come un DTO, e permette una copia modificata con with. Una class è adatta a un oggetto con identità e comportamento; un record non rende immutabili gli oggetti mutabili che contiene.",
    "Collezioni moderne: List, Dictionary e Array": "Preferisci Dictionary quando cerchi spesso un elemento per una chiave univoca, per esempio la quantità di un articolo per codice. List è utile per una sequenza ordinata da attraversare; la ricerca per chiave in un Dictionary ha costo medio vicino a O(1).",
    "LINQ fondamentale: Where, Select e Aggregazioni": "Where e Select costruiscono una sequenza da enumerare: definire la query non materializza il risultato. ToList, un foreach o un'aggregazione la eseguono; enumerarla di nuovo può osservare dati cambiati.",
    "Programmazione Asincrona: Task, async/await ed Eccezioni": "Durante attese I/O realmente asincrone, await permette al thread di lavorare su altre richieste. Non rende più veloce il calcolo CPU e non elimina gli errori: occorre attendere il Task e gestire cancellazione ed eccezioni.",
    "TypeScript di base: variabili, funzioni e array": "number[] descrive un array di numeri; : number dopo la firma dichiara il tipo del risultato. Queste annotazioni sono verificate dal compilatore, non convertono valori non validi ricevuti da una API.",
    "Tipi primitivi, Any vs Unknown e Type Inference": "unknown impone di restringere il tipo prima di usarne proprietà o metodi; any disattiva quel controllo. Prima di toUpperCase, typeof value === 'string' dimostra al compilatore che il metodo esiste.",
    "Interfacce vs Type Alias e Contratti di Dati": "Una proprietà obbligatoria deve essere presente quando TypeScript controlla un oggetto conforme al tipo; una proprietà con ? può mancare e richiede di gestire undefined. Il contratto statico non valida da solo il JSON della rete.",
    "Union Discriminate e Type Narrowing": "Il discriminante collega uno stato ai dati ammessi: success porta data, mentre error porta un messaggio. Flag indipendenti permetterebbero combinazioni contraddittorie, come successo ed errore insieme.",
    "Generics essenziali per Collezioni e Risposte API": "T è un parametro di tipo: ApiResponse<User> sostituisce T con User e conserva il contratto di data. Permette di riusare una struttura senza sostituire i dati con any.",
    "Minimal API da zero: Program.cs e WebApplication": "Valuta organizzazione degli endpoint, convenzioni del team, filtri e funzionalità richieste, oltre al codice di contorno. Entrambi i modelli possono servire un'applicazione reale: nessuno garantisce da solo prestazioni migliori.",
    "Dependency Injection: Transient, Scoped e Singleton": "Scoped fornisce normalmente un DbContext per richiesta HTTP e ne limita la durata all'unità di lavoro. Non lo rende thread-safe: evita operazioni parallele sulla stessa istanza e non conservarlo in un singleton.",
    "Routing, Parametri e Binding di Record DTO": "Nome presente nel pattern della rotta, tipo del parametro e regole di binding determinano la sorgente; un record complesso può arrivare dal body JSON. FromRoute, FromQuery e FromBody rendono esplicita una scelta quando serve. Il binding non sostituisce le regole di validazione.",
    "Validazione degli input e ProblemDetails standard": "ValidationProblem fornisce una struttura coerente e un dizionario di errori per campo, che il client può visualizzare senza interpretare testo libero. Altri contratti di errore sono possibili, ma vanno documentati e gestiti in modo coerente.",
    "Gestione globale delle eccezioni e Logging strutturato": "Il messaggio interno può rivelare query, percorsi o dettagli di configurazione. Restituisci un errore pubblico comprensibile e conserva i dettagli nei log server, collegandoli alla richiesta quando possibile.",
    "HTML essenziale e CSS per leggere i template Angular": "Il for della label deve corrispondere all'id del campo. CSS cambia l'aspetto, mentre elementi e attributi conservano struttura, associazioni e significato per browser e tecnologie assistive.",
    "Progetto Angular Standalone e Bootstrap applicazione": "Il decoratore associa classe, selettore e template e dichiara negli imports le dipendenze del template. Bootstrap crea la radice; i provider applicativi registrano i servizi: sono responsabilità diverse.",
    "Creazione di componenti Standalone con @Component": "Angular non può riconoscere il figlio come dipendenza del template e normalmente segnala un elemento sconosciuto in compilazione. Aggiungi il componente agli imports del genitore, senza aggirare l'errore con uno schema permissivo.",
    "Nuovo Control Flow: @if, @else, @for e @switch": "track dichiara l'identità che collega dati e viste. Una chiave stabile permette di mantenere la riga giusta dopo aggiunte o riordini; l'indice è adatto soprattutto a una lista statica.",
    "Data Binding moderno: interpolazione, property ed event binding": "Un Signal è una funzione getter: count() legge il valore e registra la dipendenza della vista. count senza parentesi indica la funzione stessa, non il numero da mostrare.",
    "Deferrable Views: ottimizzazione con @defer": "placeholder mostra contenuto leggero prima dell'attivazione del blocco differito. loading copre invece il caricamento delle dipendenze dopo l'attivazione; un placeholder con dimensioni sensate può anche ridurre salti visivi.",
    "Introduzione a signal() e aggiornamento stato con set() e update()": "set riceve il nuovo valore; update riceve una funzione che lo calcola dal valore corrente. Per incrementare un contatore, update(value => value + 1) esplicita questa relazione.",
    "Valori derivati intelligenti con computed()": "Angular può memorizzare e rieseguire il calcolo secondo le dipendenze lette e le richieste del valore. Una funzione pura produce lo stesso risultato dagli stessi dati senza invii HTTP o modifiche esterne; quegli effetti richiedono un punto di esecuzione distinto.",
    "Effetti collaterali controllati con effect()": "computed restituisce un valore derivato da leggere; effect sincronizza un effetto esterno quando cambiano le dipendenze. Il nome del tema è un valore derivato, scriverlo nello storage è un effetto; copiare valori tra Signals con effect rischia cicli e stato duplicato.",
    "Comunicazione moderna tra componenti: input() e output()": "input restituisce un InputSignal che legge il dato fornito dal genitore. output restituisce un OutputEmitterRef per emettere eventi con emit; non è un Signal da leggere con parentesi.",
    "Integrazione tra Signals e RxJS: toSignal e toObservable": "RxJS è utile per emissioni nel tempo, debounce, cancellazione di richieste precedenti e composizione di operazioni asincrone. Un valore corrente o un totale locale si rappresentano più semplicemente con signal e computed; le conversioni collegano i due modelli.",
    "Introduzione a EF Core e DbContext": "DbContext coordina query, tracking e salvataggio delle entità configurate. Rappresenta un'unità di lavoro, non un database globale da condividere tra tutte le richieste.",
    "Modellazione Entità e Relazioni 1:N e N:N": "Una navigation property collega oggetti correlati, per esempio Order.Items. La foreign key conserva il riferimento nel modello relazionale; la navigation non garantisce che i dati correlati siano già stati caricati.",
    "Migrazioni di Database: Creazione e Applicazione": "La tabella registra quali migrazioni sono già state applicate a quel database. EF può così applicare soltanto quelle pendenti; la cronologia non è una copia di backup dei dati.",
    "Query con LINQ su Database: Tracking e AsNoTracking": "AsNoTracking è adatto a entità lette per visualizzazione senza salvarne modifiche nel contesto. Rinunci al rilevamento automatico delle modifiche e all'identity resolution del tracking; il beneficio va valutato sulla query concreta.",
    "Scrittura atomica, Transazioni e SaveChangesAsync": "Restituisce un Task<int> il cui risultato conta le voci di stato scritte, non un ID e non necessariamente il numero di righe SQL. Per una chiave generata dal database leggi la proprietà dell'entità dopo il salvataggio.",
    "Reactive Forms: FormGroup e FormControl": "Reactive Forms definisce controlli e validatori esplicitamente in TypeScript; Template-Driven Forms costruisce il modello soprattutto attraverso direttive nel template. Il primo approccio facilita il controllo di form articolati e i test del modello; entrambi richiedono feedback accessibile.",
    "Validatori sincroni nativi e personalizzati": "Il contratto è ValidationErrors oppure null: null indica assenza di errori, un oggetto ne descrive i codici. true e false non rispettano quel contratto e non permettono ad Angular di associare i messaggi ai campi.",
    "Validatori asincroni: verifica remota via API": "Un ritardo può ridurre le richieste mentre la persona digita; updateOn blur è un'altra scelta. Durante pending mostra la verifica in corso e impedisci l'invio se la regola lo richiede. Un errore di rete non dimostra che il valore sia disponibile.",
    "Angular Router moderno e Lazy Loading": "L'import dinamico permette di caricare il codice del componente quando la navigazione lo richiede, riducendo il lavoro iniziale quando quella pagina non serve. Introduce un caricamento successivo, da valutare secondo l'esperienza utente.",
    "Route Guards funzionali: Proteggere le rotte con canActivate": "Una funzione esprime direttamente la decisione e usa inject per ottenere servizi, con meno codice di contorno. Il beneficio è organizzativo: l'autorizzazione deve comunque essere verificata dall'API.",
    "Principi di sicurezza Web e architettura JWT": "Il payload del token firmato usato qui è codificato, non cifrato: chi possiede il token può leggerlo. La firma protegge l'integrità; non rende riservati password o altri dati inseriti nel payload.",
    "Generazione e convalida token JWT in ASP.NET Core": "RequireAuthorization richiede un'identità autenticata; AdminOnly richiede anche il ruolo Admin. Per queste rotte, senza token valido ottieni 401, con Reader sulla rotta Admin 403, con Admin 200. La policy del server è distinta dalla guard Angular.",
    "Consumo API autenticata con HttpClient e HttpInterceptor": "Il Bearer token permette a chi lo possiede di presentare la sessione: inviarlo a un host esterno lo espone. Confronta l'origine completa, compresa la porta, e risolvi gli URL relativi rispetto al documento prima di decidere se aggiungere l'header.",
    "CORS, Same-Origin, XSS e CSRF: scopi distinti": "Il browser impedisce al codice della pagina di leggere una risposta cross-origin non autorizzata. Questo non sostituisce autenticazione, autorizzazione o protezione CSRF; una richiesta può essere eseguita dal server anche se poi la lettura della risposta è bloccata.",
    "Test unitari in C# con xUnit": "Fact descrive un caso senza dati parametrizzati; Theory esegue lo stesso test su più insiemi di dati, per esempio InlineData. Per una regola numerica includi zero e un valore negativo oltre al caso normale.",
    "Testare componenti Angular con Vitest e TestBed": "TestBed prepara il contesto Angular con import e provider e crea una fixture del componente. La fixture permette di attivare change detection e osservare il DOM; le dipendenze esterne possono essere sostituite con mock espliciti.",
    "Principi SOLID applicati allo sviluppo Full-Stack": "La responsabilità singola è compromessa quando calcolo e persistenza cambiano per ragioni diverse nella stessa classe. Un caso d'uso può coordinarli, delegando le regole e l'accesso ai dati a responsabilità riconoscibili; non occorre una classe per ogni istruzione.",
    "Architettura Pulita: separazione di Domain, Application e API": "Le dipendenze dei layer di business puntano verso le regole centrali: Domain non dipende da EF Core o ASP.NET Core. Infrastructure implementa contratti del centro; il punto di composizione può conoscerne le implementazioni per registrarle.",
    "Organizzazione Monorepo: client/ e server/": "Una modifica collegata a client e server può essere revisionata e versionata nella stessa storia. Il monorepo non condivide automaticamente tipi, dipendenze o processi di build e non garantisce da solo il rilascio simultaneo.",
    "Progettazione dell'esperienza utente e feedback visivo": "Disabilitare l'invio e mostrare lo stato in corso evita duplicazioni accidentali e rende visibile l'attesa. Ripristina l'interazione anche quando la richiesta fallisce; il server deve comunque gestire correttamente richieste ripetute.",
    "Documentazione delle API con OpenAPI": "AddOpenApi registra i servizi che generano la descrizione, MapOpenApi espone il documento JSON. Una UI come Swagger UI o Scalar visualizza quel documento ed è un'integrazione separata, non il documento stesso.",
    "Presentare il progetto: Git, README professionale e Portfolio": "Documenta scopo, prerequisiti, comandi riproducibili per avvio e test, configurazione locale, decisioni e limiti noti. Un'altra persona deve poter avviare il progetto senza conoscere la tua macchina; non inserire segreti o token nel README.",
}

STUDY_CONNECTIONS = {
    "Setup dell'ambiente moderno per Angular e .NET": ([], "Il percorso procede da metodi e dati a endpoint HTTP, componenti, stato, database e integrazione. I laboratori sono il punto in cui proverai framework e browser reali. Le sessioni finali servono a consolidare il lavoro; il tempo indicato è una stima, non una soglia di valutazione."),
    "Il primo metodo C#: parametri, variabili e valore restituito": ([], "Per eseguire l'esempio fuori dall'editor, crea un progetto con `dotnet new console -n FirstMethod`, entra con `cd FirstMethod`, sostituisci `Program.cs` con il codice dell'esempio ed esegui `dotnet run`. Nell'editor dell'esercizio scrivi soltanto la classe richiesta: il runner fornisce il chiamante."),
    "TypeScript di base: variabili, funzioni e array": ([], "Qui impari funzioni e array prima di usarli nei componenti. Il runner breve esegue la logica rimuovendo le annotazioni: nel laboratorio Modelli TypeScript e Contratti Web userai anche il compilatore per verificare i tipi."),
    "Minimal API da zero: Program.cs e WebApplication": (["Il primo metodo C#: parametri, variabili e valore restituito", "Anatomia di una soluzione Full-Stack Client-Server"], "Crea un progetto con `dotnet new web -n FirstApi`, entra con `cd FirstApi` e sostituisci `Program.cs` con l'esempio. Avvia con `dotnet run --urls http://localhost:5000`, poi apri `http://localhost:5000/api/hello`. Il terminale resta occupato dal server; usa una seconda finestra per le richieste e Ctrl+C per fermarlo. Il laboratorio Web API con Minimal API e DTO estenderà questa risposta a operazioni CRUD."),
    "Dependency Injection: Transient, Scoped e Singleton": (["Classi, Record e Costruttori Primari", "Minimal API da zero: Program.cs e WebApplication"], "La scelta del ciclo di vita dipende dallo stato del servizio. Un repository che usa DbContext deve restare nella richiesta; un singleton condiviso richiede stato sicuro per accessi concorrenti. Evita di scegliere Singleton soltanto per risparmiare istanze."),
    "Progetto Angular Standalone e Bootstrap applicazione": (["TypeScript di base: variabili, funzioni e array", "HTML essenziale e CSS per leggere i template Angular"], "Le basi di `signal()` e `computed()` precedono questa lezione: nei componenti useremo subito valori reattivi. Ripassale dai richiami qui sotto se necessario. Nel laboratorio Catalogo Standalone con Control Flow i file sono `src/main.ts`, `src/app/app.ts` e `src/app/app.config.ts`; gli esempi con `AppComponent` usano un nome illustrativo, da adattare all'export del tuo file."),
    "Nuovo Control Flow: @if, @else, @for e @switch": (["Introduzione a signal() e aggiornamento stato con set() e update()", "Valori derivati intelligenti con computed()"], "Il modello TypeScript prepara i dati; il template decide che cosa mostrare. Nel laboratorio Catalogo Standalone con Control Flow verifica lista, stato vuoto e selezione nel DOM: il conteggio corretto nell'esercizio breve da solo non dimostra che il template funzioni."),
    "Introduzione a signal() e aggiornamento stato con set() e update()": (["TypeScript di base: variabili, funzioni e array"], "Puoi leggere questa lezione prima del bootstrap Angular: l'esercizio breve richiede soltanto una classe e i valori reattivi. La registrazione del componente e il rendering verranno provati nel laboratorio Angular. Nel codice reale importa `signal` da `@angular/core`; l'editor breve lo mette a disposizione tramite un mock."),
    "Valori derivati intelligenti con computed()": (["Introduzione a signal() e aggiornamento stato con set() e update()"], "Un totale dipende dagli elementi: mantenere due valori modificabili separati obbliga a sincronizzarli. Il laboratorio Dashboard Reattiva con Angular Signals verifica l'aggiornamento dei totali quando la lista cambia."),
    "Integrazione tra Signals e RxJS: toSignal e toObservable": (["Valori derivati intelligenti con computed()", "Effetti collaterali controllati con effect()"], "Un Observable descrive emissioni nel tempo; `subscribe` avvia l'ascolto e `unsubscribe` lo interrompe. `pipe` compone operatori; `switchMap` sostituisce l'ascolto della richiesta precedente. Le richieste HttpClient partono alla sottoscrizione. `toSignal` e `toObservable` vanno creati in un contesto di iniezione, per esempio nei campi di un componente. La conversione è utile per ricerca remota e flussi asincroni; per un totale locale basta `computed`."),
    "Introduzione a EF Core e DbContext": (["LINQ fondamentale: Where, Select e Aggregazioni", "Dependency Injection: Transient, Scoped e Singleton"], "Il laboratorio Persistenza con EF Core e SQLite usa soggetti e misure: ritroverai lo stesso contesto nel gestionale full-stack. Il contesto segue l'unità di lavoro; non condividerlo tra richieste o operazioni parallele."),
    "Reactive Forms: FormGroup e FormControl": (["Data Binding moderno: interpolazione, property ed event binding"], "Il laboratorio Form Reattivo con Validazione Remota collega le regole allo stato reale dei controlli. La panoramica Signal Forms è facoltativa: puoi proseguire con Reactive Forms senza implementare un secondo form."),
    "Consumo API autenticata con HttpClient e HttpInterceptor": (["Generazione e convalida token JWT in ASP.NET Core", "Interfacce vs Type Alias e Contratti di Dati"], "Prima dell'interceptor serve una richiesta reale: `provideHttpClient()` registra il servizio, `inject(HttpClient)` lo ottiene e `http.get<Profile>(url).subscribe(...)` avvia la GET. Il tipo `Profile` descrive il risultato atteso ma non valida il JSON ricevuto. Nel laboratorio Autenticazione JWT Full-Stack collegherai la sessione all'header; nel Gestionale Full-Stack Monorepo seguirai il caricamento dei dati."),
    "Architettura Pulita: separazione di Domain, Application e API": (["Dependency Injection: Transient, Scoped e Singleton", "Principi SOLID applicati allo sviluppo Full-Stack"], "Usa questa separazione quando regole e integrazioni cambiano in modo indipendente. Un CRUD piccolo può iniziare con cartelle e servizi nello stesso progetto: creare quattro progetti subito aggiunge configurazione senza necessariamente migliorare lo studio. Angular comunica con l'API via HTTP e non è un assembly dipendente da Domain. L'esercizio considera i riferimenti tra layer di business; il punto di composizione dell'API può conoscere Infrastructure per registrare le implementazioni."),
    "Organizzazione Monorepo: client/ e server/": (["Minimal API da zero: Program.cs e WebApplication", "Progetto Angular Standalone e Bootstrap applicazione"], "Ora collega il contesto dei soggetti: GET `/api/subjects` restituisce la lista, POST crea, PUT modifica e DELETE rimuove. Nel laboratorio Gestionale Full-Stack Monorepo completa prima la lettura dal server, poi collega al servizio i comandi di modifica della UI. Le suite separate non dimostrano da sole la comunicazione tra i due processi: prova anche un'operazione dal browser."),
}


def study_context(title: str, mandatory: bool, lesson_files: dict[str, str]) -> str:
    prerequisites, context = STUDY_CONNECTIONS.get(title, ([], ""))
    if title == "Progetto Angular Standalone e Bootstrap applicazione":
        prerequisites = prerequisites + [
            "Introduzione a signal() e aggiornamento stato con set() e update()",
            "Valori derivati intelligenti con computed()",
        ]
    parts = []
    if not mandatory:
        parts.append("Approfondimento facoltativo: puoi riprenderlo dopo aver completato la pratica essenziale del modulo.")
    if prerequisites:
        links = [f"[{item}]({lesson_files[item]})" for item in prerequisites]
        parts.append("Da conoscere: " + "; ".join(links) + ".")
    if context:
        parts.append(context)
    return "### Nel percorso\n\n" + "\n\n".join(parts) if parts else ""


def practice_context(module: str, exercise: dict) -> str:
    if exercise["kind"] == "reflection":
        return "Annota ciò che osservi sul tuo computer. Il confronto automatico è concettuale: non esegue i comandi al posto tuo."
    if module in {"00_fondamenti", "00_orientamento", "01_csharp", "02_typescript"}:
        return "Usa il frammento come riferimento iniziale. Prima di aprire gli indizi, prova a prevedere un caso della consegna; dopo la soluzione, riscrivi il passaggio che ti mancava."
    framework = "Angular" if exercise["kind"] in {"angular", "typescript"} else ".NET"
    return (f"La pratica breve isola una regola e non avvia l'applicazione {framework}. "
            "Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. "
            "Nel laboratorio del modulo verifica anche il comportamento del framework.")


def lesson_difficulty(title: str, mandatory: bool) -> str:
    if not mandatory:
        return "approfondimento"
    if title in ADVANCED_LESSONS:
        return "avanzato"
    if title in INTERMEDIATE_LESSONS:
        return "intermedio"
    return "base"


def build() -> None:
    LESSONS_DOTNET.mkdir(parents=True, exist_ok=True)
    module_counts: dict[str, int] = {}
    lessons = []
    exercises = []
    flashcards = []

    # Compute references before rendering; IDs still follow the original authored
    # sequence, independently from the study order.
    lesson_files = {}
    reference_counts: dict[str, int] = {}
    for topic in TOPICS:
        module, title = topic[:2]
        reference_counts[module] = reference_counts.get(module, 0) + 1
        id_title = LEGACY_LESSON_TITLES.get(title, title)
        lesson_id = f"net-{module[:2]}-{reference_counts[module]:02d}-{slugify(id_title)[:35]}"
        lesson_files[title] = f"{lesson_id}.md"

    for index, topic in enumerate(TOPICS):
        (
            module, title, minutes, mandatory, summary, concepts,
            simple_exp, syntax_anatomy, example, pattern_guide,
            pitfalls, review_q, code_ex
        ) = topic

        module_counts[module] = module_counts.get(module, 0) + 1
        id_title = LEGACY_LESSON_TITLES.get(title, title)
        lesson_id = f"net-{module[:2]}-{module_counts[module]:02d}-{slugify(id_title)[:35]}"
        body_file = f"lessons_dotnet/{lesson_id}.md"

        if title not in GUIDED_WALKTHROUGHS:
            raise ValueError(f"Manca la guida passo per passo per la lezione: {title}")

        content_md = lesson_markdown(
            module, title, summary, concepts, simple_exp, syntax_anatomy,
            example, pattern_guide, pitfalls, review_q, GUIDED_WALKTHROUGHS[title],
            study_context(title, mandatory, lesson_files), practice_context(module, code_ex)
        )
        (CONTENT / body_file).write_text(content_md, encoding="utf-8")

        keywords = [x.strip() for x in concepts.split(";")]
        lessons.append({
            "id": lesson_id, "module": module, "title": title,
            "minutes": minutes, "difficulty": lesson_difficulty(title, mandatory),
            "mandatory": mandatory, "objectives": keywords[:4],
            "summary": summary, "body_file": body_file,
        })

        # Esercizio 1: Richiamo concettuale guidato
        recall_id = f"ex-{lesson_id}-recall"
        k1 = keywords[0] if keywords else "concetto"
        recall_solution = (
            f"Concetto di riferimento: `{k1}`.\n\n{REVIEW_ANSWERS[title]}\n\n"
            f"Un caso o errore da tenere presente: {pitfalls.split(';')[0].strip()}"
        )
        exercises.append({
            "id": recall_id, "lesson_id": lesson_id, "title": f"Richiamo Concettuale: {title}", "kind": "reflection",
            "difficulty": "breve", "minutes": 8, "xp": 15,
            "prompt": f"{review_q}\n\nRispondi con un esempio o una previsione sul codice della lezione e usa il termine `{k1}`. Il controllo cerca soltanto questo termine: confronta il ragionamento con il modello, anche se risulta superato.",
            "starter": "", "solution": recall_solution,
            "hints": [
                f"Definisci chiaramente il ruolo di `{k1}` nel contesto di questa lezione.",
                "Collega il concetto a un passaggio concreto dell'esempio.",
                "Concludi spiegando un possibile errore da evitare o una verifica osservabile."
            ],
            "tests": [
                {"name": f"menziona {k1}", "alternatives": [k1]},
            ],
            "explanation": "Il controllo automatico non interpreta il significato della risposta. Dopo aver superato il controllo dei termini, confronta la spiegazione con questo modello e correggi eventuali imprecisioni.",
            "creative_goals": [],
            "bonus_xp": 0
        })

        # Esercizio 2: Pratica di Codice Contestuale e Scaffoldata
        practice_id = f"ex-{lesson_id}-practice"
        exercises.append({
            "id": practice_id,
            "lesson_id": lesson_id,
            "title": f"Pratica: {code_ex['title']}",
            "kind": code_ex["kind"],
            "difficulty": "media",
            "minutes": 18,
            "xp": code_ex.get("xp", 20),
            "prompt": code_ex["prompt"],
            "starter": code_ex["starter"],
            "solution": code_ex["solution"],
            "hints": code_ex["hints"],
            "tests": code_ex["tests"],
            "explanation": "Confronta ogni passaggio con i requisiti del prompt. Verifica quali input vengono gestiti e che cosa restituisce ciascun caso di test.",
            "creative_goals": code_ex.get("creative_goals", ["Usa sintassi pulita ed espressiva"]),
            "bonus_xp": 0
        })

        # 3 Flashcards mirate per lezione
        flashcards.extend([
            {
                "id": f"fc-{lesson_id}-1", "module": module,
                "question": f"Qual è il principio cardine di **{title}**?",
                "answer": simple_exp
            },
            {
                "id": f"fc-{lesson_id}-2", "module": module,
                "question": review_q,
                "answer": recall_solution
            },
            {
                "id": f"fc-{lesson_id}-3", "module": module,
                "question": f"Quale errore comune bisogna prevenire con **{title}**?",
                "answer": f"L'errore più comune è: {pitfalls.split(';')[0].strip()}."
            }
        ])

    ordered_titles = INITIAL_LESSON_SEQUENCE + [
        topic[1] for topic in TOPICS if topic[1] not in INITIAL_LESSON_SEQUENCE
    ]
    signals_intro = [
        "Introduzione a signal() e aggiornamento stato con set() e update()",
        "Valori derivati intelligenti con computed()",
    ]
    for title in signals_intro:
        ordered_titles.remove(title)
    angular_start = ordered_titles.index("Progetto Angular Standalone e Bootstrap applicazione")
    ordered_titles[angular_start:angular_start] = signals_intro
    study_order = {title: index for index, title in enumerate(ordered_titles)}
    lessons.sort(key=lambda item: study_order[item["title"]])
    lesson_positions = {lesson["id"]: index for index, lesson in enumerate(lessons)}
    exercises.sort(key=lambda item: lesson_positions[item["lesson_id"]])

    # Laboratori
    labs = []
    for lab_id, module, title, minutes, desc, template in LABS_DATA:
        requirements, rubric = LAB_CRITERIA[lab_id]
        labs.append({
            "id": lab_id, "module": module, "title": title, "minutes": minutes, "difficulty": "laboratorio",
            "description": desc,
            "requirements": requirements,
            "rubric": rubric,
            "workspace_template": template,
            "creative_goals": [],
            "bonus_xp": 0
        })

    # Simulazioni
    simulations = []
    for sim_id, title, minutes, brief, checklist in SIMULATIONS_DATA:
        simulations.append({
            "id": sim_id, "title": title, "minutes": minutes, "brief": brief, "checklist": checklist
        })

    estimated_minutes = sum(
        item["minutes"]
        for collection in (lessons, exercises, labs, simulations)
        for item in collection
    )
    catalog_data = {
        "meta": {
            "name": "DEV//48 — Angular & .NET Enterprise Academy",
            "track_id": "dotnet-angular",
            "version": "3.0",
            "estimated_hours": f"{estimated_minutes / 60:.1f}",
            "language": "it"
        },
        "modules": [{"id": m[0], "order": m[1], "title": m[2], "description": m[3]} for m in MODULES],
        "lessons": lessons,
        "exercises": exercises,
        "labs": labs,
        "flashcards": flashcards,
        "simulations": simulations
    }

    target_catalog = CONTENT / "catalog_dotnet_angular.json"
    target_catalog.write_text(json.dumps(catalog_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Catalog 'catalog_dotnet_angular.json' successfully generated!")
    print(f"- Lezioni: {len(lessons)}")
    print(f"- Esercizi: {len(exercises)}")
    print(f"- Laboratori: {len(labs)}")
    print(f"- Flashcards: {len(flashcards)}")
    print(f"- Simulazioni: {len(simulations)}")


if __name__ == "__main__":
    build()
