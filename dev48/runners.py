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
import sys
import threading

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


def run_exercise(
    exercise: Exercise,
    answer: str,
    project_root: Path,
    language: str = "python",
) -> RunResult:
    variant = exercise.variants.get(language)
    kind = str(variant.get("kind", language)) if variant else exercise.kind
    tests = tuple(variant.get("tests", ())) if variant else exercise.tests
    if kind == "python":
        result = run_python(answer, tests)
    elif kind == "cpp":
        result = run_cpp(answer, tests)
    elif kind == "csharp":
        result = run_csharp(answer, tests)
    elif exercise.kind == "angular":
        result = run_angular(answer, tests)
    elif exercise.kind == "typescript":
        result = run_typescript(answer, tests)
    elif exercise.kind == "javascript":
        result = run_javascript(answer, tests)
    elif exercise.kind == "sql":
        result = run_sql(answer, tests)
    elif exercise.kind in {"html", "css"}:
        result = run_markup(answer, tests)
    elif exercise.kind in {"quiz", "short", "reflection", "architecture", "git"}:
        result = run_semantic_text(answer, tests)
    elif exercise.kind == "react":
        result = run_react_check(answer, tests)
    else:
        result = RunResult(False, 0, "Tipo di esercizio non supportato.", ())

    return result


def _run_process_limited(
    command: list[str],
    cwd: str | Path,
    timeout: float,
    env: dict[str, str] | None = None,
) -> tuple[int, str, str, bool, bool]:
    """Run a child process with a wall-clock and combined output cap."""
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    output_lock = threading.Lock()
    captured = {"stdout": bytearray(), "stderr": bytearray()}
    total_bytes = 0
    output_limited = threading.Event()

    def drain(name: str, stream) -> None:
        nonlocal total_bytes
        while True:
            chunk = stream.read(4096)
            if not chunk:
                return
            with output_lock:
                remaining = max(0, MAX_OUTPUT - total_bytes)
                if remaining:
                    captured[name].extend(chunk[:remaining])
                total_bytes += len(chunk)
                if len(chunk) > remaining:
                    output_limited.set()
            if output_limited.is_set() and process.poll() is None:
                process.kill()

    readers = [
        threading.Thread(target=drain, args=(name, stream), daemon=True)
        for name, stream in (("stdout", process.stdout), ("stderr", process.stderr))
    ]
    for reader in readers:
        reader.start()
    timed_out = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
    for reader in readers:
        reader.join(timeout=2)
    stdout = bytes(captured["stdout"]).decode("utf-8", errors="replace")
    stderr = bytes(captured["stderr"]).decode("utf-8", errors="replace")
    if output_limited.is_set():
        stderr += "\n… output interrotto al limite configurato"
    return process.returncode or 0, stdout, stderr, timed_out, output_limited.is_set()


def run_python(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    """Execute Python interview solutions against behavioral expressions."""
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())
    harness = r'''import json, pathlib, sys, traceback

source_path, tests_path = map(pathlib.Path, sys.argv[1:])
tests = json.loads(tests_path.read_text(encoding="utf-8"))
scope = {"__name__": "__dev48_solution__"}

def report(value):
    sys.__stdout__.write("DEV48_RESULT:" + json.dumps(value, ensure_ascii=False) + "\n")

try:
    source = source_path.read_text(encoding="utf-8")
    exec(compile(source, str(source_path), "exec"), scope)
except BaseException as error:
    report({"fatal": type(error).__name__ + ": " + str(error), "trace": traceback.format_exc(limit=5)})
    raise SystemExit(2)

results = []
for test in tests:
    try:
        actual = eval(test["expression"], scope)
        expected = test.get("expected")
        results.append({"name": test.get("name", "Test"), "passed": actual == expected,
                        "actual": actual, "expected": expected})
    except BaseException as error:
        results.append({"name": test.get("name", "Test"), "passed": False,
                        "error": type(error).__name__ + ": " + str(error),
                        "trace": traceback.format_exc(limit=3), "expected": test.get("expected")})
report({"results": results})
'''
    with TemporaryDirectory(prefix="dev48_py_") as temporary:
        root = Path(temporary)
        source_file = root / "solution.py"
        test_file = root / "tests.json"
        harness_file = root / "runner.py"
        source_file.write_text(source, encoding="utf-8")
        test_file.write_text(json.dumps(tests, ensure_ascii=False), encoding="utf-8")
        harness_file.write_text(harness, encoding="utf-8")
        try:
            code, stdout, stderr, timed_out, limited = _run_process_limited(
                [sys.executable, str(harness_file), str(source_file), str(test_file)],
                cwd=root,
                timeout=6,
                env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
            )
        except OSError as error:
            return RunResult(False, 0, f"Impossibile avviare il runner Python: {error}", ())
    if timed_out:
        return RunResult(False, 0, "Tempo scaduto: il codice Python ha superato il limite di 6 secondi.", ())
    marker = next((line for line in reversed(stdout.splitlines()) if line.startswith("DEV48_RESULT:")), "")
    if not marker:
        detail = (stderr or stdout).strip()
        if limited:
            detail = "Il processo ha superato il limite di output. " + detail
        return RunResult(False, 0, f"Errore di sintassi o esecuzione Python:\n{detail or 'Il processo non ha prodotto risultati.'}", ())
    try:
        payload = json.loads(marker.removeprefix("DEV48_RESULT:"))
    except json.JSONDecodeError:
        return RunResult(False, 0, "Il runner Python non ha prodotto un risultato leggibile.", ())
    if "fatal" in payload:
        prefix = "Errore di sintassi Python" if payload["fatal"].startswith("SyntaxError:") else "Errore di esecuzione Python"
        return RunResult(False, 0, f"{prefix}:\n{payload.get('trace', payload['fatal'])}", ())
    results = payload.get("results", [])
    passed_count = sum(bool(result.get("passed")) for result in results)
    details = []
    for result in results:
        if result.get("passed"):
            details.append(f"✓ {result.get('name', 'Test')}")
        else:
            actual = result.get("error", repr(result.get("actual")))
            details.append(f"✗ {result.get('name', 'Test')} — ottenuto {actual}; atteso {result.get('expected')!r}")
    score = int(100 * passed_count / max(1, len(results)))
    user_output = "\n".join(line for line in stdout.splitlines() if not line.startswith("DEV48_RESULT:"))
    summary = f"{passed_count}/{len(results)} test Python superati"
    if stderr.strip():
        summary += "\n\n" + _trim(stderr)
    if user_output.strip():
        summary += "\n\nOutput del programma:\n" + _trim(user_output)
    return RunResult(passed_count == len(results), score, summary, tuple(details))


def run_cpp(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    """Compile C++20 code and evaluate boolean assertions in a temporary directory."""
    if not tests:
        return RunResult(False, 0, "Questo esercizio non ha verifiche automatiche configurate.", ())
    compiler = next((shutil.which(name) for name in ("g++", "clang++") if shutil.which(name)), None)
    if not compiler:
        return RunResult(False, 0, "Compilatore C++ non trovato: installa GCC o Clang per eseguire questa soluzione.", ())
    expressions = [test.get("assertion", "") for test in tests]
    if any(not expression for expression in expressions):
        return RunResult(False, 0, "Test C++ incompleto: manca un'asserzione comportamentale.", ())
    harness = [
        "#include <iostream>",
        "#include <exception>",
        source,
        "\nint main() {",
    ]
    for index, expression in enumerate(expressions):
        harness.append(
            f'  try {{ std::cout << "DEV48_RESULT:{index}:" << (static_cast<bool>({expression}) ? 1 : 0) << "\\n"; }} '
            f'catch (const std::exception& error) {{ std::cout << "DEV48_RUNTIME:{index}:" << error.what() << "\\n"; }} '
            f'catch (...) {{ std::cout << "DEV48_RUNTIME:{index}:unknown\\n"; }}'
        )
    harness.append("  return 0;\n}")
    with TemporaryDirectory(prefix="dev48_cpp_") as temporary:
        root = Path(temporary)
        source_file = root / "solution.cpp"
        binary_file = root / ("solution.exe" if os.name == "nt" else "solution")
        source_file.write_text("\n".join(harness), encoding="utf-8")
        try:
            code, stdout, stderr, timed_out, limited = _run_process_limited(
                [compiler, "-std=c++20", "-O0", str(source_file), "-o", str(binary_file)],
                cwd=root,
                timeout=30,
                env={**os.environ, "NO_COLOR": "1"},
            )
        except OSError as error:
            return RunResult(False, 0, f"Impossibile avviare il compilatore C++: {error}", ())
        if timed_out:
            return RunResult(False, 0, "Tempo scaduto durante la compilazione C++ (30 secondi).", ())
        if code != 0 or not binary_file.is_file():
            detail = _trim(stderr or stdout or "Il compilatore non ha creato l'eseguibile.")
            return RunResult(False, 0, f"Errore del compilatore C++:\n{detail}", ())
        try:
            code, stdout, stderr, timed_out, limited = _run_process_limited(
                [str(binary_file)], cwd=root, timeout=6, env={**os.environ, "NO_COLOR": "1"},
            )
        except OSError as error:
            return RunResult(False, 0, f"Impossibile avviare il programma C++: {error}", ())
    if timed_out:
        return RunResult(False, 0, "Tempo scaduto: il codice C++ ha superato il limite di 6 secondi.", ())
    if limited:
        return RunResult(False, 0, "Output C++ oltre il limite consentito.", ())
    markers = {}
    runtime_errors = {}
    for line in stdout.splitlines():
        if line.startswith("DEV48_RESULT:"):
            parts = line.split(":", 2)
            if len(parts) == 3 and parts[1].isdigit():
                markers[int(parts[1])] = parts[2] == "1"
        elif line.startswith("DEV48_RUNTIME:"):
            parts = line.split(":", 2)
            if len(parts) == 3 and parts[1].isdigit():
                runtime_errors[int(parts[1])] = parts[2]
    if code != 0:
        return RunResult(False, 0, f"Errore di esecuzione C++:\n{_trim(stderr or stdout or f'codice di uscita {code}')}", ())
    details = []
    for index, test in enumerate(tests):
        if markers.get(index, False):
            details.append(f"✓ {test.get('name', f'Test {index + 1}')}")
        else:
            error = runtime_errors.get(index)
            suffix = f" — {error}" if error else (" — nessun risultato" if index not in markers else "")
            details.append(f"✗ {test.get('name', f'Test {index + 1}')}{suffix}")
    passed_count = sum(markers.get(index, False) for index in range(len(tests)))
    score = int(100 * passed_count / max(1, len(tests)))
    summary = f"{passed_count}/{len(tests)} test C++20 superati"
    if stderr.strip():
        summary += "\n\n" + _trim(stderr)
    return RunResult(passed_count == len(tests), score, summary, tuple(details))


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
    if target == "all" and (workspace / "CMakeLists.txt").is_file():
        return run_cpp_lab_tests(workspace)
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
            returncode, stdout, stderr, timed_out, output_limited = _run_process_limited(
                [dotnet, "test", str(test_project), "--nologo", "-v", "q"],
                cwd=server_dir, timeout=90,
            )
            if timed_out:
                return RunResult(False, 0, "Test backend .NET interrotti dopo 90 secondi.", ())
            ran_anything = True
            if returncode != 0 or output_limited:
                all_passed = False
            outputs.append(f"[Test Backend .NET]\n{stdout}\n{stderr}")
        except OSError as error:
            return RunResult(False, 0, f"Impossibile avviare dotnet test: {error}", ())

    # Progetto Angular Client (npm test)
    client_dir = workspace / "client" if (workspace / "client").is_dir() else None
    if client_dir and target in ("all", "client", "frontend"):
        npm = shutil.which("npm")
        if not npm:
            return RunResult(False, 0, "npm non trovato nel PATH.", ())
        try:
            returncode, stdout, stderr, timed_out, output_limited = _run_process_limited(
                [npm, "test"], cwd=client_dir, timeout=90,
            )
            if timed_out:
                return RunResult(False, 0, "Test frontend interrotti dopo 90 secondi.", ())
            ran_anything = True
            if returncode != 0 or output_limited:
                all_passed = False
            outputs.append(f"[Test Frontend Angular]\n{stdout}\n{stderr}")
        except OSError as error:
            return RunResult(False, 0, f"Impossibile avviare npm test: {error}", ())

    if not ran_anything:
        # Small JavaScript/React exercises use a root package instead of a
        # server/client monorepo. A targeted server/client run must not pass
        # by silently falling back to another project.
        if target == "all" and (workspace / "package.json").exists():
            npm = shutil.which("npm")
            if not npm:
                return RunResult(False, 0, "npm non trovato nel PATH.", ())
            try:
                returncode, stdout, stderr, timed_out, output_limited = _run_process_limited(
                    [npm, "test"], cwd=workspace, timeout=90,
                )
            except OSError as error:
                return RunResult(False, 0, f"Impossibile avviare npm test: {error}", ())
            if timed_out:
                return RunResult(False, 0, "Test del progetto interrotti dopo 90 secondi.", ())
            output = _trim(stdout + "\n" + stderr)
            if output_limited:
                return RunResult(False, 0, output + "\nSuite interrotta al limite di output.", ())
            return RunResult(returncode == 0, 100 if returncode == 0 else 0, output, ())
        return RunResult(False, 0, "Nessun progetto .NET o npm/Angular rilevato nel workspace.", ())

    combined_output = _trim("\n\n".join(outputs))
    score = 100 if all_passed else 0
    return RunResult(all_passed, score, combined_output, ())


def run_cpp_lab_tests(workspace: Path) -> RunResult:
    compiler = next((shutil.which(name) for name in ("g++", "clang++") if shutil.which(name)), None)
    if not compiler:
        return RunResult(False, 0, "Compilatore C++ non trovato: installa GCC o Clang per eseguire i test del laboratorio.", ())
    source_files = sorted((workspace / "src").glob("*.cpp"))
    test_files = sorted((workspace / "tests").glob("*.cpp"))
    if not source_files or not test_files:
        return RunResult(False, 0, "Repository C++ incompleta: servono file .cpp in src/ e tests/.", ())
    with TemporaryDirectory(prefix="dev48_cpp_lab_") as temporary:
        executable = Path(temporary) / ("lab-tests.exe" if os.name == "nt" else "lab-tests")
        command = [
            compiler, "-std=c++20", "-O0", "-Wall", "-Wextra",
            "-I", str(workspace / "include"),
            *(str(path) for path in source_files),
            *(str(path) for path in test_files),
            "-o", str(executable),
        ]
        try:
            compile_code, compile_stdout, compile_stderr, timed_out, output_limited = _run_process_limited(
                command, cwd=workspace, timeout=30, env={**os.environ, "NO_COLOR": "1"},
            )
        except OSError as error:
            return RunResult(False, 0, f"Impossibile avviare il compilatore C++: {error}", ())
        if timed_out:
            return RunResult(False, 0, "Compilazione C++ interrotta dopo 30 secondi.", ())
        if output_limited:
            detail = _trim(compile_stdout + "\n" + compile_stderr)
            return RunResult(False, 0, f"Output della compilazione oltre il limite configurato:\n{detail}", ())
        if compile_code != 0 or not executable.is_file():
            detail = _trim(compile_stderr or compile_stdout or "Nessun eseguibile prodotto.")
            return RunResult(False, 0, f"Errore del compilatore C++:\n{detail}", ())
        try:
            returncode, stdout, stderr, timed_out, output_limited = _run_process_limited(
                [str(executable)], cwd=workspace, timeout=10, env={**os.environ, "NO_COLOR": "1"},
            )
        except OSError as error:
            return RunResult(False, 0, f"Impossibile avviare i test C++: {error}", ())
        if timed_out:
            return RunResult(False, 0, "Test C++ interrotti dopo 10 secondi.", ())
    output = _trim(stdout + ("\n" + stderr if stderr else ""))
    if output_limited:
        return RunResult(False, 0, output + "\nTest C++ interrotti al limite di output.", ())
    return RunResult(
        returncode == 0,
        100 if returncode == 0 else 0,
        output or f"Suite C++ terminata con codice {returncode}.",
        (),
    )
