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
    result = run_javascript("while(true) {}", ())
    assert not result.passed
    assert "Tempo scaduto" in result.output

