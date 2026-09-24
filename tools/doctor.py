from __future__ import annotations

from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def line(ok: bool, label: str, detail: str) -> bool:
    status = "OK" if ok else "ERRORE"
    print(f"[{status:6}] {label}: {detail}")
    return ok


def command_version(command: str, args: list[str]) -> tuple[bool, str]:
    executable = shutil.which(command)
    if not executable:
        return False, "comando non trovato nel PATH"
    try:
        result = subprocess.run(
            [executable, *args], capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="replace",
        )
        detail = (result.stdout or result.stderr).strip().splitlines()[0]
        return result.returncode == 0, detail
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)


def main() -> int:
    print("DEV//48 — diagnostica locale\n")
    checks: list[bool] = []
    checks.append(line(sys.version_info >= (3, 11), "Python", sys.version.split()[0]))

    try:
        import textual
        checks.append(line(True, "Textual", textual.__version__))
    except Exception as error:
        checks.append(line(False, "Textual", f"non importabile: {error}"))

    for command, args, required in (
        ("dotnet", ["--version"], True),
        ("node", ["--version"], True),
        ("npm", ["--version"], True),
        ("git", ["--version"], False),
        ("code", ["--version"], False),
    ):
        ok, detail = command_version(command, args)
        suffix = "" if required else " (opzionale)"
        checks.append(line(ok or not required, command + suffix, detail))

    try:
        from dev48.models import Catalog
        for track_id, track_label in [("dotnet-angular", "Angular & .NET"), ("web-js-react", "JS & React")]:
            catalog = Catalog(ROOT / "content", track=track_id)
            errors = catalog.validate()
            counts = (
                f"{len(catalog.lessons)} lezioni, {len(catalog.exercises)} esercizi, "
                f"{len(catalog.labs)} lab, {len(catalog.flashcards)} flashcard, "
                f"{len(catalog.simulations)} simulazioni"
            )
            checks.append(line(not errors, f"Catalogo ({track_label})", counts if not errors else "; ".join(errors)))
    except Exception as error:
        checks.append(line(False, "Catalogo", str(error)))

    try:
        (ROOT / "data").mkdir(exist_ok=True)
        (ROOT / "workspace").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "data") as directory:
            database = Path(directory) / "check.sqlite3"
            connection = sqlite3.connect(database)
            connection.execute("CREATE TABLE check_ok(value INTEGER)")
            connection.close()
        checks.append(line(True, "Scrittura locale", "data/ e workspace/ disponibili"))
    except Exception as error:
        checks.append(line(False, "Scrittura locale", str(error)))

    try:
        from dev48.runners import run_javascript
        result = run_javascript("function add(a,b){return a+b}", ({"name": "add", "expression": "add(2,3)", "expected": 5},))
        checks.append(line(result.passed, "Runner JavaScript", result.output.splitlines()[0]))
    except Exception as error:
        checks.append(line(False, "Runner JavaScript", str(error)))

    try:
        from dev48.runners import run_csharp
        result_cs = run_csharp("public class S { public static int Add(int a, int b) => a + b; }", ({"name": "add", "expression": "S.Add(2,3)", "expected": 5},))
        checks.append(line(result_cs.passed, "Runner .NET C#", result_cs.output.splitlines()[0]))
    except Exception as error:
        checks.append(line(False, "Runner .NET C#", str(error)))

    passed = all(checks)
    print("\nRISULTATO:", "tutto pronto." if passed else "serve correggere almeno un controllo obbligatorio.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
