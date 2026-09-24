from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import json
import os
import re
import shutil
import sqlite3
import subprocess

from .models import Exercise


MAX_OUTPUT = 12_000


@dataclass(frozen=True)
class RunResult:
    passed: bool
    score: int
    output: str
    details: tuple[str, ...]


def _trim(value: str) -> str:
    if len(value) <= MAX_OUTPUT:
        return value
    return value[:MAX_OUTPUT] + "\n… output interrotto per sicurezza"


def _strip_js_comments(source: str) -> str:
    """Remove line and block comments without treating comment markers in strings as comments."""
    result: list[str] = []
    index = 0
    quote: str | None = None
    escaped = False
    line_comment = False
    block_comment = False
    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""
        if line_comment:
            if char == "\n":
                result.append(char)
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and following == "/":
                block_comment = False
                index += 2
            else:
                if char == "\n":
                    result.append(char)
                index += 1
            continue
        if quote:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char in {"'", '"', "`"}:
            quote = char
            result.append(char)
            index += 1
            continue
        if char == "/" and following == "/":
            line_comment = True
            index += 2
            continue
        if char == "/" and following == "*":
            block_comment = True
            index += 2
            continue
        result.append(char)
        index += 1
    return "".join(result)


def run_exercise(exercise: Exercise, answer: str, project_root: Path) -> RunResult:
    if exercise.kind == "csharp":
        result = run_csharp(answer, exercise.tests)
    elif exercise.kind == "angular":
        result = run_angular(answer, exercise.tests)
    elif exercise.kind == "typescript":
        result = run_typescript(answer, exercise.tests)
    elif exercise.kind == "javascript":
        result = run_javascript(answer, exercise.tests)
    elif exercise.kind == "sql":
        result = run_sql(answer, exercise.tests)
    elif exercise.kind in {"html", "css"}:
        result = run_markup(answer, exercise.tests)
    elif exercise.kind in {"quiz", "short", "reflection", "architecture", "git"}:
        result = run_semantic_text(answer, exercise.tests)
    elif exercise.kind == "react":
        result = run_react_check(answer, exercise.tests)
    else:
        result = RunResult(False, 0, "Tipo di esercizio non supportato.", ())

    return result


def run_csharp(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    """Compila C# con il SDK .NET 10 ed esegue le asserzioni comportamentali."""
    dotnet = shutil.which("dotnet")
    if not dotnet:
        return RunResult(False, 0, "dotnet CLI non trovato nel PATH. Installa .NET SDK 10 per compilare e verificare C#.", ())
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())

    # Costruzione harness Program.cs
    harness_code = [
        "using System;",
        "using System.Collections.Generic;",
        "using System.Linq;",
        "using System.Text.Json;",
        "using System.Threading.Tasks;",
        "",
        "// Codice utente",
        source,
        "",
        "class __Dev48Harness",
        "{",
        "    public static void Main()",
        "    {",
        "        var __results = new List<Dictionary<string, object?>>();",
    ]

    for i, test in enumerate(tests):
        name = json.dumps(test.get("name", f"Test {i+1}"), ensure_ascii=False)
        expression = test.get("expression", "")
        expected = json.dumps(test.get("expected"), ensure_ascii=False)

        if test.get("mode") == "regex":
            pattern = json.dumps(test.get("value", ""))
            harness_code.append(f"""
        try {{
            bool __ok = System.Text.RegularExpressions.Regex.IsMatch({json.dumps(source)}, {pattern}, System.Text.RegularExpressions.RegexOptions.IgnoreCase);
            __results.Add(new Dictionary<string, object?> {{ {{"name", {name}}}, {{"passed", __ok}}, {{"actual", __ok}}, {{"expected", true}} }});
        }} catch (Exception ex) {{
            __results.Add(new Dictionary<string, object?> {{ {{"name", {name}}}, {{"passed", false}}, {{"error", ex.Message}}, {{"expected", true}} }});
        }}""")
        elif expression:
            expected_str = json.dumps(str(test.get("expected")))
            harness_code.append(f"""
        try {{
            var __actual = ({expression});
            object? __actualObj = __actual;
            string __actualJson = JsonSerializer.Serialize(__actual);
            string __expectedJson = {json.dumps(expected)};
            bool __passed = __actualJson == __expectedJson || (__actualObj?.ToString() == {expected_str});
            __results.Add(new Dictionary<string, object?> {{ {{"name", {name}}}, {{"passed", __passed}}, {{"actual", __actualObj}}, {{"expected", {expected}}} }});
        }} catch (Exception ex) {{
            __results.Add(new Dictionary<string, object?> {{ {{"name", {name}}}, {{"passed", false}}, {{"error", ex.ToString()}}, {{"expected", {expected}}} }});
        }}""")

    harness_code.extend([
        "        Console.WriteLine(\"DEV48_RESULT:\" + JsonSerializer.Serialize(__results));",
        "    }",
        "}",
    ])

    with TemporaryDirectory(prefix="dev48_cs_") as temp:
        temp_path = Path(temp)
        csproj = temp_path / "exercise.csproj"
        csproj.write_text("""<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <WarningLevel>0</WarningLevel>
  </PropertyGroup>
</Project>""", encoding="utf-8")

        program = temp_path / "Program.cs"
        program.write_text("\n".join(harness_code), encoding="utf-8")

        try:
            process = subprocess.run(
                [dotnet, "run", "--project", str(temp_path)],
                cwd=temp, capture_output=True, text=True, timeout=12,
                encoding="utf-8", errors="replace",
                env={**os.environ, "DOTNET_NOLOGO": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1"},
            )
        except subprocess.TimeoutExpired:
            return RunResult(False, 0, "Tempo scaduto: l'esecuzione C# ha superato il tempo limite.", ())

    stdout = _trim(process.stdout)
    stderr = _trim(process.stderr)
    marker = next((line for line in reversed(stdout.splitlines()) if line.startswith("DEV48_RESULT:")), "")

    if not marker:
        # Errore di compilazione o crash a runtime
        error_lines = [l for l in (stderr + "\n" + stdout).splitlines() if "error CS" in l or "Exception" in l or "Unhandled" in l]
        err_msg = "\n".join(error_lines[:6]) if error_lines else (stderr or stdout or "Errore di compilazione o esecuzione C#.")
        return RunResult(False, 0, f"Errore del compilatore C#:\n{err_msg}", ())

    try:
        results = json.loads(marker.removeprefix("DEV48_RESULT:"))
    except json.JSONDecodeError:
        return RunResult(False, 0, "Impossibile decodificare i risultati dei test C#.", ())

    details = []
    passed_count = 0
    for r in results:
        passed = bool(r.get("passed"))
        passed_count += int(passed)
        name = r.get("name", "Test")
        if passed:
            details.append(f"✓ {name}")
        else:
            actual = r.get("error") or repr(r.get("actual"))
            details.append(f"✗ {name} — ottenuto {actual}; atteso {r.get('expected')!r}")

    score = int(100 * passed_count / max(1, len(results)))
    user_output = "\n".join(line for line in stdout.splitlines() if not line.startswith("DEV48_RESULT:") and "Benvenuti" not in line)
    summary = f"{passed_count}/{len(results)} test C# superati"
    if user_output.strip():
        summary += "\n\nOutput del programma:\n" + user_output.strip()

    return RunResult(passed_count == len(results), score, summary, tuple(details))


def run_angular(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    """Esegue la logica TypeScript degli esercizi Angular con piccoli mock dei Signals."""
    node = shutil.which("node")
    if not node:
        return RunResult(False, 0, "Node.js non trovato: la logica dell'esercizio Angular non è stata eseguita.", ())
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())

    # Runtime harness con mock dei Signals e Component Angular
    harness = """
const __dev48Results = [];
function signal(initialValue) {
  let val = initialValue;
  const s = () => val;
  s.set = (v) => { val = v; };
  s.update = (fn) => { val = fn(val); };
  s.asReadonly = () => () => val;
  return s;
}
function computed(fn) {
  return () => fn();
}
function effect(fn) {
  try { fn(); } catch(e) {}
}
function input(initial) {
  return signal(initial);
}
function output() {
  const listeners = [];
  return { emit: (val) => listeners.forEach(listener => listener(val)), subscribe: (listener) => listeners.push(listener) };
}
function Component(opts) {
  return function(target) { target.__componentMetadata = opts; return target; };
}
function inject(token) { return {}; }

function __dev48Check(name, fn, expected) {
  try {
    const actual = fn();
    const passed = JSON.stringify(actual) === JSON.stringify(expected) || actual === expected;
    __dev48Results.push({ name, passed, actual, expected });
  } catch (error) {
    __dev48Results.push({ name, passed: false, error: String(error), expected });
  }
}
"""
    # Gli esercizi isolano logica e stato: non avviano il runtime Angular né il DOM.
    uncommented_source = _strip_js_comments(source)
    clean_source = re.sub(r"import\s+\{[^}]*\}\s+from\s+['\"]@angular/core['\"];?", "", uncommented_source)

    test_calls = []
    for test in tests:
        name = json.dumps(test.get("name", "Test"), ensure_ascii=False)
        expected = json.dumps(test.get("expected"), ensure_ascii=False)
        if "expression" in test:
            test_calls.append(f"__dev48Check({name}, () => ({test['expression']}), {expected});")
        elif test.get("mode") == "regex":
            if not test.get("value"):
                return RunResult(False, 0, f"Verifica senza criterio: {test.get('name', 'senza nome')}.", ())
            pattern = json.dumps(test.get("value"))
            test_calls.append(f"__dev48Check({name}, () => new RegExp({pattern}, 'i').test({json.dumps(clean_source)}), true);")
        elif test.get("mode") == "contains":
            if not test.get("value"):
                return RunResult(False, 0, f"Verifica senza criterio: {test.get('name', 'senza nome')}.", ())
            val = json.dumps(test.get("value", "").lower())
            test_calls.append(f"__dev48Check({name}, () => {json.dumps(clean_source.lower())}.includes({val}), true);")
        elif test.get("mode") == "not_contains":
            if not test.get("value"):
                return RunResult(False, 0, f"Verifica senza criterio: {test.get('name', 'senza nome')}.", ())
            val = json.dumps(test.get("value", "").lower())
            test_calls.append(f"__dev48Check({name}, () => !{json.dumps(clean_source.lower())}.includes({val}), true);")
        else:
            return RunResult(False, 0, f"Verifica non supportata: {test.get('name', 'senza nome')}.", ())

    script_content = f"{harness}\n{clean_source}\n" + "\n".join(test_calls) + "\nconsole.log('DEV48_RESULT:' + JSON.stringify(__dev48Results));"

    with TemporaryDirectory(prefix="dev48_ng_") as temp:
        script = Path(temp) / "angular_test.mts"
        script.write_text(script_content, encoding="utf-8")
        try:
            process = subprocess.run(
                [node, "--no-warnings", "--experimental-strip-types", str(script)], cwd=temp, capture_output=True, text=True,
                timeout=5, encoding="utf-8", errors="replace",
                env={**os.environ, "NO_COLOR": "1"},
            )
        except subprocess.TimeoutExpired:
            return RunResult(False, 0, "Tempo scaduto durante l'esecuzione Angular/JS.", ())

    stdout = _trim(process.stdout)
    stderr = _trim(process.stderr)
    if process.returncode != 0:
        detail = stderr or stdout or "Il processo è terminato con un errore."
        return RunResult(False, 0, f"Errore di sintassi o esecuzione nel modello TypeScript/Signals:\n{detail}", ())
    marker = next((line for line in reversed(stdout.splitlines()) if line.startswith("DEV48_RESULT:")), "")

    if not marker:
        detail = stderr or stdout or "Il processo non ha prodotto risultati."
        return RunResult(False, 0, f"Errore di sintassi o esecuzione nel modello TypeScript/Signals:\n{detail}", ())

    try:
        results = json.loads(marker.removeprefix("DEV48_RESULT:"))
    except json.JSONDecodeError:
        return RunResult(False, 0, "Il runner non ha prodotto un risultato leggibile.", ())

    details = []
    passed_count = 0
    for r in results:
        passed = bool(r.get("passed"))
        passed_count += int(passed)
        name = r.get("name", "Test")
        if passed:
            details.append(f"✓ {name}")
        else:
            actual = r.get("error") or repr(r.get("actual"))
            details.append(f"✗ {name} — ottenuto {actual}; atteso {r.get('expected')!r}")

    score = int(100 * passed_count / max(1, len(results)))
    summary = (
        f"{passed_count}/{len(results)} controlli superati sulla logica TypeScript. "
        "I mock non verificano template, DOM o runtime Angular."
    )
    return RunResult(passed_count == len(results), score, summary, tuple(details))


def run_typescript(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    """Verifica la sintassi eseguibile e i contratti dichiarati; non sostituisce tsc."""
    node = shutil.which("node")
    if not node:
        return RunResult(False, 0, "Node.js non trovato: non è possibile controllare la sintassi TypeScript.", ())
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())

    # I commenti di esempio o TODO non devono soddisfare un requisito del codice.
    clean_source = _strip_js_comments(source)
    dynamic_tests = all("expression" in test for test in tests)
    harness = """
const __dev48Results = [];
function __dev48Check(name, fn, expected) {
  try {
    const actual = fn();
    const passed = JSON.stringify(actual) === JSON.stringify(expected) || actual === expected;
    __dev48Results.push({ name, passed, actual, expected });
  } catch (error) {
    __dev48Results.push({ name, passed: false, error: String(error), expected });
  }
}
"""
    test_calls: list[str] = []
    for test in tests:
        name = json.dumps(test.get("name", "Test"), ensure_ascii=False)
        if "expression" in test:
            expected = json.dumps(test.get("expected"), ensure_ascii=False)
            test_calls.append(f"__dev48Check({name}, () => ({test['expression']}), {expected});")
        elif test.get("mode") in {"contains", "not_contains", "regex"}:
            value = str(test.get("value", ""))
            if not value:
                return RunResult(False, 0, f"Verifica senza criterio: {test.get('name', 'senza nome')}.", ())
            if test["mode"] == "contains":
                predicate = f"{json.dumps(clean_source.lower())}.includes({json.dumps(value.lower())})"
            elif test["mode"] == "not_contains":
                if re.fullmatch(r"[a-zA-Z_$][\w$]*", value):
                    predicate = f"!new RegExp({json.dumps(r'(?<![\\w])' + re.escape(value) + r'(?![\\w])')}, 'i').test({json.dumps(clean_source)})"
                else:
                    predicate = f"!{json.dumps(clean_source.lower())}.includes({json.dumps(value.lower())})"
            else:
                predicate = f"new RegExp({json.dumps(value)}, 'i').test({json.dumps(clean_source)})"
            test_calls.append(f"__dev48Check({name}, () => {predicate}, true);")
        else:
            return RunResult(False, 0, f"Verifica non supportata: {test.get('name', 'senza nome')}.", ())

    with TemporaryDirectory(prefix="dev48_ts_") as temp:
        script = Path(temp) / "exercise.ts"
        # Le prove solo strutturali hanno comunque parsing TypeScript; le funzioni
        # sono eseguite quando la scheda definisce casi di input e output.
        script.write_text(
            f"{clean_source}\n{harness}\n" + "\n".join(test_calls) +
            "\nconsole.log('DEV48_RESULT:' + JSON.stringify(__dev48Results));\n",
            encoding="utf-8",
        )
        try:
            process = subprocess.run(
                [node, "--no-warnings", "--experimental-strip-types", str(script)],
                cwd=temp, capture_output=True, text=True, timeout=5,
                encoding="utf-8", errors="replace", env={**os.environ, "NO_COLOR": "1"},
            )
        except subprocess.TimeoutExpired:
            return RunResult(False, 0, "Tempo scaduto durante il controllo TypeScript.", ())

        stdout, stderr = _trim(process.stdout), _trim(process.stderr)
    if process.returncode != 0:
        detail = stderr or stdout or "Il processo è terminato con un errore."
        return RunResult(False, 0, f"Errore di sintassi o esecuzione TypeScript:\n{detail}", ())
    marker = next((line for line in reversed(stdout.splitlines()) if line.startswith("DEV48_RESULT:")), "")
    if not marker:
        detail = stderr or stdout or "Il processo non ha prodotto risultati."
        return RunResult(False, 0, f"Errore di sintassi o esecuzione TypeScript:\n{detail}", ())
    try:
        results = json.loads(marker.removeprefix("DEV48_RESULT:"))
    except json.JSONDecodeError:
        return RunResult(False, 0, "Il runner non ha prodotto un risultato leggibile.", ())

    details = tuple(
        f"✓ {item['name']}" if item["passed"] else
        f"✗ {item['name']} — ottenuto {item.get('error') or repr(item.get('actual'))}; atteso {item.get('expected')!r}"
        for item in results
    )
    passed_count = sum(bool(item["passed"]) for item in results)
    score = int(100 * passed_count / max(1, len(results)))
    scope = "test funzionali" if dynamic_tests else "requisiti del codice"
    summary = (
        f"{passed_count}/{len(results)} {scope} superati. "
        "Il runner controlla sintassi eseguibile e requisiti dichiarati, ma non esegue tsc."
    )
    return RunResult(passed_count == len(results), score, summary, details)


def run_javascript(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    node = shutil.which("node")
    if not node:
        return RunResult(False, 0, "Node.js non trovato nel PATH.", ())
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())
    harness = """
const __dev48Results = [];
function __dev48Equal(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}
function __dev48Check(name, fn, expected) {
  try {
    const actual = fn();
    __dev48Results.push({name, passed: __dev48Equal(actual, expected), actual, expected});
  } catch (error) {
    __dev48Results.push({name, passed: false, error: String(error), expected});
  }
}
"""
    for test in tests:
        expected = json.dumps(test.get("expected"), ensure_ascii=False)
        harness += f"\n__dev48Check({json.dumps(test['name'])}, () => ({test['expression']}), {expected});"
    harness += "\nconsole.log('DEV48_RESULT:' + JSON.stringify(__dev48Results));\n"
    with TemporaryDirectory(prefix="dev48_js_") as temp:
        script = Path(temp) / "exercise.mjs"
        script.write_text(source + "\n" + harness, encoding="utf-8")
        try:
            process = subprocess.run(
                [node, str(script)], cwd=temp, capture_output=True, text=True,
                timeout=5, encoding="utf-8", errors="replace",
                env={**os.environ, "NO_COLOR": "1"},
            )
        except subprocess.TimeoutExpired:
            return RunResult(False, 0, "Tempo scaduto: il codice ha superato 5 secondi. Controlla i cicli.", ())
    stdout = _trim(process.stdout)
    stderr = _trim(process.stderr)
    if process.returncode != 0:
        detail = stderr or stdout or "Il processo è terminato con un errore."
        return RunResult(False, 0, f"Errore di sintassi o esecuzione TypeScript:\n{detail}", ())
    marker = next((line for line in reversed(stdout.splitlines()) if line.startswith("DEV48_RESULT:")), "")
    if not marker:
        message = stderr or stdout or "Il processo non ha prodotto risultati."
        return RunResult(False, 0, message, ())
    try:
        results = json.loads(marker.removeprefix("DEV48_RESULT:"))
    except json.JSONDecodeError:
        return RunResult(False, 0, "Impossibile leggere il risultato dei test.", ())
    details = []
    for result in results:
        if result["passed"]:
            details.append(f"✓ {result['name']}")
        else:
            actual = result.get("error", repr(result.get("actual")))
            details.append(f"✗ {result['name']} — ottenuto {actual}; atteso {result.get('expected')!r}")
    passed_count = sum(bool(item["passed"]) for item in results)
    score = int(100 * passed_count / max(1, len(results)))
    user_output = "\n".join(line for line in stdout.splitlines() if not line.startswith("DEV48_RESULT:"))
    summary = f"{passed_count}/{len(results)} test superati"
    if user_output.strip():
        summary += "\n\nOutput personale:\n" + user_output
    return RunResult(passed_count == len(results), score, summary, tuple(details))


def run_sql(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    schema = """
    CREATE TABLE subjects(id INTEGER PRIMARY KEY, name TEXT NOT NULL, zone TEXT NOT NULL, active INTEGER NOT NULL, checks INTEGER NOT NULL);
    INSERT INTO subjects VALUES
      (1,'Mario Rossi','Centro',1,4), (2,'Anna Bianchi','Nord',0,7),
      (3,'Paolo Verdi','Centro',1,2), (4,'Sara Neri','Sud',1,9);
    CREATE TABLE measures(id INTEGER PRIMARY KEY, subject_id INTEGER NOT NULL REFERENCES subjects(id), type TEXT NOT NULL, start_date TEXT NOT NULL, end_date TEXT);
    INSERT INTO measures VALUES
      (1,1,'Obbligo','2026-01-10',NULL), (2,3,'Controllo','2026-02-01','2026-06-01'), (3,4,'Obbligo','2026-03-15',NULL);
    """
    try:
        db.executescript(schema)
        cursor = db.execute(source.strip().rstrip(";"))
        rows = [list(row) for row in cursor.fetchall()]
        columns = [item[0] for item in cursor.description] if cursor.description else []
    except sqlite3.Error as error:
        db.close()
        return RunResult(False, 0, f"Errore SQLite: {error}", ())
    details: list[str] = []
    passed_count = 0
    for test in tests:
        expected = test.get("expected")
        mode = test.get("mode", "rows")
        actual: Any = rows if mode == "rows" else columns
        passed = actual == expected
        passed_count += int(passed)
        details.append(("✓ " if passed else "✗ ") + test["name"] + ("" if passed else f" — ottenuto {actual!r}"))
    db.close()
    score = int(100 * passed_count / max(1, len(tests)))
    preview = json.dumps({"columns": columns, "rows": rows}, ensure_ascii=False, indent=2)
    return RunResult(passed_count == len(tests), score, _trim(preview), tuple(details))


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.attributes: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag.lower())
        self.attributes.append((tag.lower(), dict(attrs)))


def run_markup(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    source = re.sub(r"/\*.*?\*/|<!--.*?-->", "", source, flags=re.DOTALL)
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())
    parser = StructureParser()
    try:
        parser.feed(source)
    except Exception as error:
        return RunResult(False, 0, f"Markup non analizzabile: {error}", ())
    details: list[str] = []
    passed_count = 0
    lowered = source.lower()
    for test in tests:
        mode = test.get("mode", "contains")
        value = str(test.get("value", "")).lower()
        if not value:
            return RunResult(False, 0, f"Verifica senza criterio: {test.get('name', 'senza nome')}.", ())
        if mode == "tag":
            passed = value in parser.tags
        elif mode == "attribute":
            tag, attribute = value.split(":", 1)
            passed = any(current == tag and attribute in attrs for current, attrs in parser.attributes)
        elif mode == "label_for":
            matching_inputs = {
                attrs.get("id") for current, attrs in parser.attributes if current == "input"
            }
            passed = any(
                current == "label" and attrs.get("for") == value and value in matching_inputs
                for current, attrs in parser.attributes
            )
        elif mode == "regex":
            passed = bool(re.search(test["value"], source, re.IGNORECASE | re.DOTALL))
        elif mode == "not_contains":
            passed = value not in lowered
        else:
            passed = value in lowered
        passed_count += int(passed)
        details.append(("✓ " if passed else "✗ ") + test["name"])
    score = int(100 * passed_count / max(1, len(tests)))
    return RunResult(
        passed_count == len(tests), score,
        f"{passed_count}/{len(tests)} controlli di struttura o testo superati; non viene eseguito il rendering nel browser.",
        tuple(details),
    )


TECHNICAL_SYNONYMS = {
    "signal": ["signal", "signals", "segnale", "segnali"],
    "inject": ["inject", "dependency injection", "injection", "iniezione delle dipendenze"],
    "record": ["record", "record class", "record struct"],
    "linq": ["linq", "where", "select"],
    "async": ["async", "await", "task", "asincrono", "asincrona"],
    "middleware": ["middleware", "pipeline middleware"],
    "jwt": ["jwt", "json web token"],
    "routing": ["router", "routing", "route guard", "rotte"],
    "efcore": ["ef core", "entity framework core", "dbcontext", "migrazione"],
}


def run_semantic_text(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    """Controllo trasparente dei termini richiesti; non valuta la correttezza semantica."""
    normalized = re.sub(r"\s+", " ", source.strip().lower())
    details: list[str] = []
    passed_count = 0

    for test in tests:
        alternatives = list(test.get("alternatives") or [test.get("value", "")])
        expanded_alternatives = {a.lower() for a in alternatives if a}
        for term in alternatives:
            term_l = term.lower()
            if term_l in TECHNICAL_SYNONYMS:
                expanded_alternatives.update(TECHNICAL_SYNONYMS[term_l])

        passed = any(
            re.search(rf"(?<![\w]){re.escape(term)}(?![\w])", normalized) is not None
            for term in expanded_alternatives
        )
        passed_count += int(passed)
        if passed:
            details.append(f"✓ {test['name']}")
        else:
            hint = f" (prova a menzionare '{alternatives[0]}' o un concetto correlato)" if alternatives else ""
            details.append(f"✗ {test['name']}{hint}")

    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha criteri di verifica configurati.", ())

    score = int(100 * passed_count / max(1, len(tests)))
    summary = (
        "Controllo dei termini richiesti: verifica solo che compaiano nella risposta, "
        "non che la spiegazione sia corretta. Confrontala con il modello prima di proseguire."
    )
    return RunResult(passed_count == len(tests), score, summary, tuple(details))


def run_text(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    """Mantenuta per retro-compatibilità diretta con test suite esistente."""
    return run_semantic_text(source, tests)


def run_react_check(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    return run_markup(source, tests)


def run_lab_tests(workspace: Path, target: str = "all") -> RunResult:
    """Esegue i test del laboratorio supportando progetti .NET (server/), Angular (client/) o Monorepo misti."""
    outputs: list[str] = []
    all_passed = True
    ran_anything = False

    # Progetto .NET Server (xUnit / dotnet test)
    server_dir = workspace / "server" if (workspace / "server").is_dir() else (workspace if any(workspace.glob("*.csproj")) or any(workspace.glob("*.sln")) else None)
    if server_dir and target in ("all", "server", "backend"):
        dotnet = shutil.which("dotnet")
        if not dotnet:
            return RunResult(False, 0, "dotnet CLI non trovato nel PATH.", ())
        test_project = server_dir / "Tests" / "Server.Tests.csproj"
        if not test_project.is_file():
            test_projects = list(server_dir.glob("*Tests.csproj"))
            if len(test_projects) == 1:
                test_project = test_projects[0]
            else:
                return RunResult(False, 0, "Progetto di test xUnit non trovato: nessun test è stato eseguito.", ())
        try:
            proc = subprocess.run(
                [dotnet, "test", str(test_project), "--nologo", "-v", "q"],
                cwd=server_dir, capture_output=True, text=True, timeout=90,
                encoding="utf-8", errors="replace",
            )
            ran_anything = True
            if proc.returncode != 0:
                all_passed = False
            outputs.append(f"[Test Backend .NET]\n{proc.stdout}\n{proc.stderr}")
        except subprocess.TimeoutExpired:
            return RunResult(False, 0, "Test backend .NET interrotti dopo 90 secondi.", ())

    # Progetto Angular Client (npm test)
    client_dir = workspace / "client" if (workspace / "client").is_dir() else (workspace if (workspace / "package.json").is_file() else None)
    if client_dir and target in ("all", "client", "frontend"):
        npm = shutil.which("npm")
        if not npm:
            return RunResult(False, 0, "npm non trovato nel PATH.", ())
        try:
            proc = subprocess.run(
                [npm, "test"],
                cwd=client_dir, capture_output=True, text=True, timeout=90,
                encoding="utf-8", errors="replace",
            )
            ran_anything = True
            if proc.returncode != 0:
                all_passed = False
            outputs.append(f"[Test Frontend Angular]\n{proc.stdout}\n{proc.stderr}")
        except subprocess.TimeoutExpired:
            return RunResult(False, 0, "Test frontend interrotti dopo 90 secondi.", ())

    if not ran_anything:
        # Small JavaScript/React exercises use a root package instead of a
        # server/client monorepo. A targeted server/client run must not pass
        # by silently falling back to another project.
        if target == "all" and (workspace / "package.json").exists():
            npm = shutil.which("npm")
            if not npm:
                return RunResult(False, 0, "npm non trovato nel PATH.", ())
            try:
                proc = subprocess.run([npm, "test"], cwd=workspace, capture_output=True, text=True, timeout=90, encoding="utf-8", errors="replace")
            except subprocess.TimeoutExpired:
                return RunResult(False, 0, "Test del progetto interrotti dopo 90 secondi.", ())
            output = _trim(proc.stdout + "\n" + proc.stderr)
            return RunResult(proc.returncode == 0, 100 if proc.returncode == 0 else 0, output, ())
        return RunResult(False, 0, "Nessun progetto .NET o npm/Angular rilevato nel workspace.", ())

    combined_output = _trim("\n\n".join(outputs))
    score = 100 if all_passed else 0
    return RunResult(all_passed, score, combined_output, ())
