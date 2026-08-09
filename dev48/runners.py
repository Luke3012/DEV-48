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


def run_exercise(exercise: Exercise, answer: str, project_root: Path) -> RunResult:
    if exercise.kind == "javascript":
        return run_javascript(answer, exercise.tests)
    if exercise.kind == "sql":
        return run_sql(answer, exercise.tests)
    if exercise.kind in {"html", "css"}:
        return run_markup(answer, exercise.tests)
    if exercise.kind in {"quiz", "short", "architecture", "git"}:
        return run_text(answer, exercise.tests)
    if exercise.kind in {"react", "typescript"}:
        return run_react_check(answer, exercise.tests)
    return RunResult(False, 0, "Tipo di esercizio non supportato.", ())


def run_javascript(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    node = shutil.which("node")
    if not node:
        return RunResult(False, 0, "Node.js non trovato nel PATH.", ())
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
        if mode == "tag":
            passed = value in parser.tags
        elif mode == "attribute":
            tag, attribute = value.split(":", 1)
            passed = any(current == tag and attribute in attrs for current, attrs in parser.attributes)
        elif mode == "regex":
            passed = bool(re.search(test["value"], source, re.IGNORECASE | re.DOTALL))
        elif mode == "not_contains":
            passed = value not in lowered
        else:
            passed = value in lowered
        passed_count += int(passed)
        details.append(("✓ " if passed else "✗ ") + test["name"])
    score = int(100 * passed_count / max(1, len(tests)))
    return RunResult(passed_count == len(tests), score, f"{passed_count}/{len(tests)} requisiti rilevati", tuple(details))


def run_text(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    normalized = re.sub(r"\s+", " ", source.strip().lower())
    details: list[str] = []
    passed_count = 0
    for test in tests:
        alternatives = test.get("alternatives") or [test.get("value", "")]
        passed = any(str(term).lower() in normalized for term in alternatives)
        passed_count += int(passed)
        details.append(("✓ " if passed else "✗ ") + test["name"])
    if not tests:
        passed_count = int(len(normalized) >= 30)
        tests = ({"name": "Risposta sufficientemente articolata"},)
        details = ["✓ Risposta registrata" if passed_count else "✗ Scrivi almeno 30 caratteri"]
    score = int(100 * passed_count / max(1, len(tests)))
    return RunResult(passed_count == len(tests), score, "Valutazione per concetti chiave: rileggi comunque la risposta modello.", tuple(details))


def run_react_check(source: str, tests: tuple[dict[str, Any], ...]) -> RunResult:
    # Gli esercizi brevi verificano costrutti essenziali; i laboratori usano Vitest nel workspace.
    return run_markup(source, tests)


def run_lab_tests(workspace: Path) -> RunResult:
    npm = shutil.which("npm")
    if not npm:
        return RunResult(False, 0, "npm non trovato nel PATH.", ())
    if not (workspace / "package.json").exists():
        return RunResult(False, 0, "Il laboratorio non contiene package.json.", ())
    command = [npm, "test", "--", "--run"]
    try:
        process = subprocess.run(command, cwd=workspace, capture_output=True, text=True, timeout=90, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return RunResult(False, 0, "Test interrotti dopo 90 secondi.", ())
    output = _trim(process.stdout + "\n" + process.stderr)
    return RunResult(process.returncode == 0, 100 if process.returncode == 0 else 0, output, ())
