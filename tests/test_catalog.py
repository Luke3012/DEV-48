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


def test_dotnet_angular_course_is_complete_and_explicit_about_its_checks():
    catalog = Catalog(ROOT / "content", track="dotnet-angular")
    assert (len(catalog.lessons), len(catalog.exercises), len(catalog.flashcards), len(catalog.labs), len(catalog.simulations)) == (53, 106, 159, 12, 4)
    assert catalog.validate() == []
    assert [lesson.title for lesson in catalog.lessons[:4]] == [
        "Setup dell'ambiente moderno per Angular e .NET",
        "Il primo metodo C#: parametri, variabili e valore restituito",
        "Anatomia di una soluzione Full-Stack Client-Server",
        "Metodo di debugging per API e Frontend",
    ]
    assert {lesson.difficulty for lesson in catalog.lessons} == {"base", "intermedio", "avanzato", "approfondimento"}
    assert next(x for x in catalog.lessons if x.title == "Introduzione a signal() e aggiornamento stato con set() e update()").difficulty == "base"
    assert next(x for x in catalog.lessons if x.title == "Architettura Pulita: separazione di Domain, Application e API").difficulty == "avanzato"
    markdown = []
    walkthroughs = []
    for lesson in catalog.lessons:
        body = catalog.lesson_body(lesson)
        markdown.append(body)
        assert len(body.split()) >= 500, lesson.id
        for heading in (
            "## In parole semplici", "## Le parole da riconoscere", "## Anatomia e Sintassi del Codice",
            "## Un esempio concreto", "### Seguilo passo per passo", "## Pattern Guida per gli Esercizi",
            "## Dove ci si confonde spesso", "## Domanda di verifica",
        ):
            assert heading in body, (lesson.id, heading)
        assert len(catalog.exercises_for(lesson.id)) == 2, lesson.id
        walkthrough = body.split("### Seguilo passo per passo\n", 1)[1].split("\n## Pattern Guida per gli Esercizi", 1)[0]
        steps = [line for line in walkthrough.splitlines() if line[:1].isdigit() and ". " in line]
        assert len(steps) == 4, lesson.id
        assert len(set(steps)) == 4, lesson.id
        assert len(walkthrough) >= 250, lesson.id
        walkthroughs.append(walkthrough)

    assert len(set(walkthroughs)) == len(catalog.lessons)
    clean_architecture = next(
        body for lesson, body in zip(catalog.lessons, markdown, strict=True)
        if lesson.title == "Architettura Pulita: separazione di Domain, Application e API"
    )
    assert "```csharp\nusing System.Threading;" in clean_architecture

    all_lessons = "\n".join(markdown)
    assert "Signal Forms sono incluse in `@angular/forms/signals`" in all_lessons
    jwt_lesson = next(body for lesson, body in zip(catalog.lessons, markdown, strict=True) if lesson.title == "Generazione e convalida token JWT in ASP.NET Core")
    assert 'dotnet user-secrets init' in jwt_lesson
    assert 'new JwtSecurityTokenHandler().WriteToken(token)' in jwt_lesson
    assert 'RequireAuthorization("AdminOnly")' in jwt_lesson
    assert "flussi standard OAuth/OIDC" in jwt_lesson
    forms_lesson = next(lesson for lesson in catalog.lessons if lesson.title == "Reactive Forms: FormGroup e FormControl")
    forms_practice = next(item for item in catalog.exercises_for(forms_lesson.id) if item.id.endswith("-practice"))
    assert forms_practice.kind == "typescript"
    assert "solo la regola TypeScript" in forms_practice.prompt
    debug_lesson = next(lesson for lesson in catalog.lessons if lesson.title == "Metodo di debugging per API e Frontend")
    classifier = next(item for item in catalog.exercises_for(debug_lesson.id) if item.id.endswith("-practice"))
    tested_statuses = {int(item["expression"].split("(")[-1].split(")")[0]) for item in classifier.tests}
    assert tested_statuses == {199, 200, 299, 300, 400, 499, 500, 599, 600}
    catalog_text = (ROOT / "content" / "catalog_dotnet_angular.json").read_text(encoding="utf-8").lower()
    assert "utility types" not in catalog_text
    assert "@Component(...)" not in all_lessons
    assert 'app.MapGet("/api/users", () => ...)' not in all_lessons
    assert "// Disabilitare pulsante" not in all_lessons
    assert "Angular 19" not in all_lessons
    assert ".NET 8/10" not in all_lessons
    assert "eliminando Zone.js" not in all_lessons
    assert "NgModule resta supportato" in all_lessons
    assert "i decoratori `@Input()` e `@Output()` restano supportati" in all_lessons
    assert "può ridurre lavoro e memoria" in all_lessons
    assert "sostituiscono i vecchi decoratori" not in all_lessons
    assert "Glitch-Free" not in all_lessons

    for lesson, body in zip(catalog.lessons, markdown, strict=True):
        assert len([line for line in body.splitlines() if line.startswith("```")]) >= 4, lesson.id

    reflections = [item for item in catalog.exercises if item.kind == "reflection"]
    assert len(reflections) == len(catalog.lessons) + 1
    assert all(item.xp in {0, 15} and item.bonus_xp == 0 and not item.creative_goals for item in reflections)
    assert all(("controllo" in item.prompt.lower() or "autoverifica" in item.prompt.lower()) and "confronta" in item.prompt.lower() for item in reflections)
    setup = next(lesson for lesson in catalog.lessons if lesson.title == "Setup dell'ambiente moderno per Angular e .NET")
    setup_practice = next(item for item in catalog.exercises_for(setup.id) if item.title == "Pratica: Prova pratica della toolchain")
    assert setup_practice.kind == "reflection" and setup_practice.xp == 0
    assert "non esegue il terminale" in setup_practice.prompt
    assert all(item.tests for item in catalog.exercises if item.kind != "reflection")

    referenced_lessons = {(ROOT / "content" / lesson.body_file).resolve() for lesson in catalog.lessons}
    markdown_files = {path.resolve() for path in (ROOT / "content" / "lessons_dotnet").glob("*.md")}
    assert markdown_files == referenced_lessons
