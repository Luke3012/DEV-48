from pathlib import Path

from dev48.models import Catalog
from dev48.runners import run_exercise, run_javascript


ROOT = Path(__file__).resolve().parents[1]


def test_every_official_short_solution_passes():
    catalog = Catalog(ROOT / "content")
    failures = []
    for exercise in catalog.exercises:
        result = run_exercise(exercise, exercise.solution, ROOT)
        if not result.passed:
            failures.append((exercise.id, result.output, result.details))
    assert failures == []


def test_wrong_javascript_is_rejected():
    result = run_javascript(
        "function add(a,b){ return 0; }",
        ({"name":"somma","expression":"add(2,3)","expected":5},),
    )
    assert not result.passed
    assert result.score == 0


def test_javascript_timeout_is_stopped():
    result = run_javascript("while(true) {}", ({"name": "non deve terminare", "expression": "true", "expected": True},))
    assert not result.passed
    assert "Tempo scaduto" in result.output


def test_every_official_dotnet_angular_solution_passes():
    catalog = Catalog(ROOT / "content", track="dotnet-angular")
    failures = []
    for exercise in catalog.exercises:
        result = run_exercise(exercise, exercise.solution, ROOT)
        if not result.passed:
            failures.append((exercise.id, result.output, result.details))
    assert failures == []


def test_csharp_runner_detects_compiler_error():
    from dev48.runners import run_csharp
    result = run_csharp("public class Bad { public static int Broken( => 123; }", ({"name": "test", "expression": "1", "expected": 1},))
    assert not result.passed
    assert "CS" in result.output


def test_angular_signals_runner():
    from dev48.runners import run_angular
    code = """
    export class Counter {
        count = signal(10);
        double = computed(() => this.count() * 2);
        inc() { this.count.update(x => x + 1); }
    }
    """
    tests = (
        {"name": "initial", "expression": "(new Counter()).count()", "expected": 10},
        {"name": "computed double", "expression": "(new Counter()).double()", "expected": 20},
    )
    result = run_angular(code, tests)
    assert result.passed
    assert result.score == 100


def test_theory_check_discloses_that_it_checks_terms_only():
    from dev48.runners import run_semantic_text
    result = run_semantic_text(
        "This answer uses signal and computed, but does not explain them.",
        ({"name": "signal", "alternatives": ["signal"]}, {"name": "computed", "alternatives": ["computed"]}),
    )
    assert result.passed
    assert "non che la spiegazione sia corretta" in result.output


def test_typescript_comment_text_does_not_satisfy_code_requirement():
    from dev48.runners import run_typescript
    result = run_typescript(
        "// export interface OrderDto { id: number }\nconst answer = 1;",
        ({"name": "OrderDto", "mode": "contains", "value": "export interface OrderDto"},),
    )
    assert not result.passed


def test_typescript_url_strings_are_not_stripped_as_comments():
    from dev48.runners import run_typescript
    result = run_typescript(
        'const endpoint: string = "https://api.example.test/subjects";',
        ({"name": "endpoint", "mode": "contains", "value": "https://api.example.test/subjects"},),
    )
    assert result.passed


def test_angular_runner_does_not_accept_markup_as_a_solution():
    from dev48.runners import run_angular
    result = run_angular(
        "<div>counter</div>",
        ({"name": "increment", "mode": "contains", "value": ".update("},),
    )
    assert not result.passed
    assert "Errore di sintassi" in result.output or "Errore di sintassi" in "\n".join(result.details)

