from pathlib import Path

from dev48.models import Catalog
from tools.generate_content import PLAIN_EXPLANATIONS


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_meets_promised_volume():
    catalog = Catalog(ROOT / "content")
    assert len(catalog.lessons) >= 45
    assert len(catalog.exercises) >= 80
    assert len(catalog.labs) >= 12
    assert len(catalog.flashcards) >= 150
    assert len(catalog.simulations) >= 4


def test_catalog_is_valid_and_ids_are_unique():
    catalog = Catalog(ROOT / "content")
    assert catalog.validate() == []
    all_ids = [x.id for x in catalog.lessons + catalog.exercises + catalog.labs + catalog.flashcards + catalog.simulations]
    assert len(all_ids) == len(set(all_ids))


def test_every_lesson_has_two_exercises_and_substantial_markdown():
    catalog = Catalog(ROOT / "content")
    for lesson in catalog.lessons:
        assert len(catalog.exercises_for(lesson.id)) >= 2
        body = catalog.lesson_body(lesson)
        assert len(body) >= 1_500
        assert "## Dove ci si confonde spesso" in body
        assert "## Domanda di verifica" in body


def test_editorial_copy_is_natural_and_topic_specific():
    catalog = Catalog(ROOT / "content")
    banned_phrases = (
        "collegalo a un comportamento osservabile",
        "È uno dei concetti centrali:",
        "Spiega operativamente il tema",
        "mantenendo il comportamento osservabile semplice",
    )
    all_text = (ROOT / "content" / "catalog.json").read_text(encoding="utf-8")
    for lesson in catalog.lessons:
        body = catalog.lesson_body(lesson)
        assert body.startswith(f"# {lesson.title}\n\n## In parole semplici")
        assert PLAIN_EXPLANATIONS[lesson.title] in body
        assert "L'obiettivo di questa lezione è " in body
    for phrase in banned_phrases:
        assert phrase not in all_text
        assert all(phrase not in catalog.lesson_body(lesson) for lesson in catalog.lessons)
    for exercise in catalog.exercises:
        if exercise.kind == "short":
            assert len(exercise.solution) >= 220
            assert "esempio" in (exercise.prompt + exercise.solution).lower()
