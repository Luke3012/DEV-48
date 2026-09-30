from pathlib import Path
import re

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


def test_catalog_rejects_unknown_track_and_missing_track_catalog(tmp_path):
    import pytest

    with pytest.raises(ValueError, match="Traccia sconosciuta"):
        Catalog(ROOT / "content", track="amazon-oa-typo")
    with pytest.raises(FileNotFoundError, match="non trovato"):
        Catalog(tmp_path, track="amazon-sde-oa")


def test_amazon_lesson_examples_follow_the_selected_coding_language():
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    lesson = catalog.lesson_by_id["sde-l-sliding-window"]
    source = (ROOT / "content" / lesson.body_file).read_text(encoding="utf-8")

    python_body = catalog.lesson_body(lesson, "python")
    cpp_body = catalog.lesson_body(lesson, "cpp")

    assert "**Versione Python**" in source and "**Versione C++**" in source
    assert "def max_sum_k" in python_body
    assert "def longest_at_most_k_distinct" in python_body
    assert "static_cast<int>(nums.size())" not in python_body
    assert "long long max_sum_k" in cpp_body
    assert "int longest_at_most_k_distinct" in cpp_body
    assert "def max_sum_k" not in cpp_body
    assert "**Esempio in Python**" in python_body
    assert "**Esempio in C++**" in cpp_body

    for item in catalog.lessons:
        catalog.lesson_body(item, "python")
        catalog.lesson_body(item, "cpp")


def test_every_lesson_has_two_exercises_and_reviewable_markdown():
    catalog = Catalog(ROOT / "content")
    for lesson in catalog.lessons:
        assert len(catalog.exercises_for(lesson.id)) >= 2
        body = catalog.lesson_body(lesson)
        assert "## Un esempio concreto" in body
        assert "## Prova tu" in body
        assert body.count("```") >= 2 and body.count("```") % 2 == 0
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
        assert "Chiudi la pagina per un minuto e ripeti tre cose" not in body
        assert "## Controllo rapido" not in body
    for phrase in banned_phrases:
        assert phrase not in all_text
        assert all(phrase not in catalog.lesson_body(lesson) for lesson in catalog.lessons)
    for exercise in catalog.exercises:
        if exercise.kind == "reflection":
            assert exercise.xp == 0
            assert "confronta" in exercise.prompt.lower()
            assert "controllo" in exercise.prompt.lower()


def test_javascript_react_progression_prerequisites_and_practice():
    import re
    from tools.js_react_notes import GUIDES, REVIEW_ANSWERS

    catalog = Catalog(ROOT / "content")
    positions = {lesson.title: i for i, lesson in enumerate(catalog.lessons)}
    by_title = {lesson.title: lesson for lesson in catalog.lessons}
    cards = {card.id: card for card in catalog.flashcards}
    assert positions["Funzioni e responsabilità"] < positions["Scope, const, let e closure"]
    assert by_title["Moduli ed organizzazione del codice"].mandatory
    assert not by_title["Generics essenziali"].mandatory
    assert not by_title["Presentare una pipeline AI multimodale"].mandatory
    # Reordered units retain the IDs already persisted by earlier releases.
    assert by_title["Scope, const, let e closure"].id == "01-02-scope-const-let-e-closure"
    assert by_title["Funzioni e responsabilità"].id == "01-03-funzioni-e-responsabilita"
    expected_functions = {
        "Valori, tipi e confronti": "classifyValue", "Scope, const, let e closure": "createCounter",
        "Funzioni e responsabilità": "fullName", "Array: map, filter, find e some": "activeNames",
        "Oggetti, destructuring e spread": "moveUser", "Immutabilità e operazioni CRUD": "updateSubject",
        "Reduce, Set e Map": "sumActiveChecks", "Errori e validazione": "parsePositive",
    }
    for title, name in expected_functions.items():
        practice = next(e for e in catalog.exercises_for(by_title[title].id) if e.id.endswith("-practice"))
        assert name in practice.prompt and f"function {name}" in practice.solution
    for lesson in catalog.lessons:
        body = catalog.lesson_body(lesson)
        for target in re.findall(r"\]\((\d\d-[^)]+\.md)\)", body):
            assert (ROOT / "content" / "lessons" / target).is_file(), (lesson.id, target)
        for prerequisite in GUIDES.get(lesson.title, {}).get("prerequisites", []):
            assert positions[prerequisite] < positions[lesson.title]
        assert REVIEW_ANSWERS[lesson.title] == cards[f"fc-{lesson.id}-2"].answer
    practices = [e for e in catalog.exercises if e.id.startswith("ex-05-") and e.id.endswith("-practice")]
    assert len({e.solution for e in practices}) == len(practices)
    assert all("non esegue React" in e.prompt for e in practices if e.kind == "react")


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
        headings = re.findall(r"(?m)^## .+$", body)
        assert len(headings) >= 3, lesson.id
        assert len(headings) == len(set(headings)), lesson.id
        # Chapters may be short or long; the course should not pad every topic
        # to the same word count. Keep only a basic guard against empty output.
        assert len(body.split()) >= 120, lesson.id
        assert len(catalog.exercises_for(lesson.id)) == 2, lesson.id
        guided_sections = re.findall(r"(?ms)^### [^\n]+\n(.*?)(?=^### |^## |\Z)", body)
        walkthroughs_for_lesson = [
            section for section in guided_sections
            if len(re.findall(r"(?m)^\d+\. .+$", section)) == 4 and len(section.strip()) >= 250
        ]
        assert walkthroughs_for_lesson, lesson.id
        walkthrough = walkthroughs_for_lesson[-1]
        steps = re.findall(r"(?m)^\d+\. .+$", walkthrough)
        assert len(steps) == 4, lesson.id
        assert len(set(steps)) == 4, lesson.id
        walkthroughs.append("\n".join(steps))

    assert len(set(walkthroughs)) == len(catalog.lessons)
    assert len({re.findall(r"(?m)^## .+$", body)[0] for body in markdown}) >= 8
    positions = {lesson.title: index for index, lesson in enumerate(catalog.lessons)}
    assert positions["Introduzione a signal() e aggiornamento stato con set() e update()"] < positions["Progetto Angular Standalone e Bootstrap applicazione"]
    assert positions["Valori derivati intelligenti con computed()"] < positions["Nuovo Control Flow: @if, @else, @for e @switch"]
    for body in markdown:
        assert "Non dare per scontato di conoscere i termini" not in body
        assert "## Controllo rapido" not in body
        for target in re.findall(r"\]\((net-[^)]+\.md)\)", body):
            assert (ROOT / "content" / "lessons_dotnet" / target).is_file()
    assert all("colloquio" not in item.title.lower() for item in catalog.simulations)
    clean_architecture = next(
        body for lesson, body in zip(catalog.lessons, markdown, strict=True)
        if lesson.title == "Architettura Pulita: separazione di Domain, Application e API"
    )
    assert "Build-time: Infrastructure → Application / Domain" in clean_architecture
    assert "composition root" in clean_architecture
    assert "Angular resta un processo separato" in clean_architecture

    lesson_bodies = {lesson.title: body for lesson, body in zip(catalog.lessons, markdown, strict=True)}
    all_lessons = "\n".join(markdown)
    assert "Signal Forms è stabile e inclusa nel pacchetto `@angular/forms`" in all_lessons
    assert "from '@angular/forms/signals'" in all_lessons
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
    assert "`NgModule` resta supportato" in all_lessons
    assert "i decoratori `@Input()` e `@Output()` restano supportati" in all_lessons
    assert "può ridurre il codice iniziale solo se" in all_lessons
    assert "sostituiscono i vecchi decoratori" not in all_lessons
    assert "Glitch-Free" not in all_lessons
    assert "La pratica breve isola una regola e non avvia l'applicazione" not in all_lessons
    assert "Nel laboratorio del modulo verifica anche il comportamento del framework" not in all_lessons

    csharp_switch = lesson_bodies["Controllo di flusso, Pattern Matching e Switch Expressions"]
    assert 'if (status == "open")' in csharp_switch
    assert "DaysWaiting: >= 3" in csharp_switch and '_ => "Stato non riconosciuto"' in csharp_switch
    linq = lesson_bodies["LINQ fondamentale: Where, Select e Aggregazioni"]
    assert "foreach (var user in users)" in linq
    assert all(token in linq for token in (".Where(", ".OrderBy(", ".Select(", ".ToList()"))
    async_lesson = lesson_bodies["Programmazione Asincrona: Task, async/await ed Eccezioni"]
    assert "Task<string>" in async_lesson and "CancellationToken" in async_lesson
    assert "non significa avviare automaticamente un nuovo thread" in async_lesson

    angular_bootstrap = lesson_bodies["Progetto Angular Standalone e Bootstrap applicazione"]
    assert all(name in angular_bootstrap for name in ("src/index.html", "src/main.ts", "src/app/app.ts", "src/app/app.config.ts"))
    assert "NullInjectorError" in angular_bootstrap and "provideHttpClient()" in angular_bootstrap
    control_flow = lesson_bodies["Nuovo Control Flow: @if, @else, @for e @switch"]
    assert "@for" in control_flow and "@empty" in control_flow and "track user.id" in control_flow
    binding = lesson_bodies["Data Binding moderno: interpolazione, property ed event binding"]
    assert all(token in binding for token in ("{{ username }}", "[value]", "(click)", "[(ngModel)]"))
    signal_lesson = lesson_bodies["Introduzione a signal() e aggiornamento stato con set() e update()"]
    assert "count = 0" in signal_lesson and "signal(0)" in signal_lesson
    assert "asReadonly()" in signal_lesson and "update(value => value + 1)" in signal_lesson
    computed = lesson_bodies["Valori derivati intelligenti con computed()"]
    assert "computed(()" in computed and "items" in computed and "duplic" in computed.lower()
    rxjs = lesson_bodies["Integrazione tra Signals e RxJS: toSignal e toObservable"]
    assert all(token in rxjs for token in ("toObservable", "switchMap", "HttpClient", "Observable<User[]>", "status: 'loading'", "status: 'error'"))
    assert "user.model.ts" in rxjs and "UserService" in rxjs

    ef_intro = lesson_bodies["Introduzione a EF Core e DbContext"]
    assert all(token in ef_intro for token in ("DbSet", "SQLite", "AddDbContext", "DbContext"))
    ef_tracking = lesson_bodies["Query con LINQ su Database: Tracking e AsNoTracking"]
    assert all(token in ef_tracking for token in ("Unchanged", "Modified", "DetectChanges()", "SaveChangesAsync", "AsNoTracking"))
    forms = lesson_bodies["Reactive Forms: FormGroup e FormControl"]
    assert all(token in forms for token in ("FormControl", "FormGroup", "touched", "dirty", "pending", "Signal Forms"))
    router = lesson_bodies["Angular Router moderno e Lazy Loading"]
    assert all(token in router for token in ("router-outlet", "query", "loadComponent", "routerLink"))
    guard = lesson_bodies["Route Guards funzionali: Proteggere le rotte con canActivate"]
    assert "UrlTree" in guard and "backend" in guard
    api_binding = lesson_bodies["Routing, Parametri e Binding di Record DTO"]
    api_validation = lesson_bodies["Validazione degli input e ProblemDetails standard"]
    assert "CreateUserRequest" in api_binding and "Results.Created" in api_binding
    assert "Results.ValidationProblem" not in api_binding
    assert "Results.ValidationProblem" in api_validation and '"status": 400' in api_validation
    assert "body malformato" in api_validation

    migrations = lesson_bodies["Migrazioni di Database: Creazione e Applicazione"]
    assert all(token in migrations for token in ("dotnet tool restore", "dotnet restore", "migrations script --idempotent", "__EFMigrationsHistory"))
    assert "--global dotnet-ef" not in migrations and "EnsureCreated" in migrations
    xunit = lesson_bodies["Test unitari in C# con xUnit"]
    assert "// Arrange" in xunit and "// Act" in xunit and "// Assert" in xunit
    assert "public partial class Program" in xunit and "WebApplicationFactory<Program>" in xunit
    openapi = lesson_bodies["Documentazione delle API con OpenAPI"]
    assert "TypedResults.Ok" in openapi and "MapOpenApi()" in openapi
    assert "Swagger UI o Scalar" in openapi and "non sostituisce i test" in openapi

    interceptor = lesson_bodies["Consumo API autenticata con HttpClient e HttpInterceptor"]
    assert "Authorization: `Bearer ${token}`" in interceptor
    assert "instanceof HttpResponse" in interceptor and "risalgono la stessa catena" in interceptor
    cors = lesson_bodies["CORS, Same-Origin, XSS e CSRF: scopi distinti"]
    assert all(token in cors for token in ("schema, host e porta", "non autentica", "CSRF"))
    jwt_lesson = lesson_bodies["Generazione e convalida token JWT in ASP.NET Core"]
    assert all(token in jwt_lesson for token in ("401", "403", "AdminOnly", "UseAuthentication()", "UseAuthorization()"))

    monorepo = lesson_bodies["Organizzazione Monorepo: client/ e server/"]
    assert all(token in monorepo for token in ("UserListComponent", "UserService", "HttpClient GET /api/users", "AddScoped<UserService>", "DbContext", "SQLite", "UserResponse", "JSON HTTP 200"))
    assert "Observable<UserDto[]>" in monorepo and "role=\"status\"" in monorepo

    for lesson, body in zip(catalog.lessons, markdown, strict=True):
        fences = [line for line in body.splitlines() if line.startswith("```")]
        assert len(fences) >= 2 and len(fences) % 2 == 0, lesson.id

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



def test_course_scaffolds_explain_practice_and_preserve_learner_work(tmp_path):
    import json
    from dev48.workspace import ensure_lab_workspace

    catalog = Catalog(ROOT / "content", track="dotnet-angular")
    for lab in catalog.labs:
        workspace = ensure_lab_workspace(tmp_path, lab)
        guide = workspace / "README.md"
        assert "## Come affrontare questo laboratorio" in guide.read_text(encoding="utf-8")
        guide.write_text("Appunti personali", encoding="utf-8")
        sources = list(workspace.glob("server/*.cs")) + list(workspace.glob("client/src/app/*.ts"))
        learner_file = sources[0]
        learner_file.write_text("// codice personale", encoding="utf-8")
        ensure_lab_workspace(tmp_path, lab)
        assert guide.read_text(encoding="utf-8") == "Appunti personali"
        assert learner_file.read_text(encoding="utf-8") == "// codice personale"

    server = tmp_path / "lab-efcore-sqlite-db" / "server"
    manifest = json.loads((server / ".config/dotnet-tools.json").read_text(encoding="utf-8"))
    assert "dotnet-ef" in manifest["tools"]
    assert "Microsoft.EntityFrameworkCore.Design" in (server / "Server.csproj").read_text(encoding="utf-8")


def test_amazon_sde_oa_course_has_independent_mapped_content():
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    assert catalog.track == "amazon-sde-oa"
    assert (len(catalog.lessons), len(catalog.exercises), len(catalog.labs), len(catalog.flashcards)) == (44, 67, 6, 160)
    assert (len(catalog.simulations), len(catalog.work_scenarios), len(catalog.work_style)) == (4, 36, 8)
    # A candidate must judge the actions rather than infer ranking from a stable label.
    assert {scenario.recommended_order[-1] for scenario in catalog.work_scenarios} == set("ABCD")
    for scenario in catalog.work_scenarios:
        assert [option["id"] for option in scenario.options] == list("ABCD")
        assert sorted(scenario.recommended_order) == list("ABCD")
    assert {item.difficulty for item in catalog.exercises} == {"easy", "medium", "hard"}
    assert sum(item.difficulty == "easy" for item in catalog.exercises) == 22
    assert sum(item.difficulty == "medium" for item in catalog.exercises) == 35
    assert sum(item.difficulty == "hard" for item in catalog.exercises) == 10
    assert all(set(item.variants) == {"python", "cpp"} for item in catalog.exercises)
    assert all(item.id == "sde-e-language-trial" or (item.no_ai and item.no_internet and item.timed) for item in catalog.exercises)
    for scenario in catalog.work_scenarios:
        option_texts = [option["text"] for option in scenario.options]
        assert len(option_texts) == len(set(option_texts)) == 4
        assert all("{focus}" not in text for text in option_texts)
        assert all(option["reasoning"] for option in scenario.options)
        assert scenario.learning_focus
    scenarios = {item.id: item for item in catalog.work_scenarios}
    assert "cache" in " ".join(option["text"] for option in scenarios["sde-ws-05"].options).casefold()
    assert "zero" in " ".join(option["text"] for option in scenarios["sde-ws-16"].options).casefold()
    assert "tastiera" in " ".join(option["text"] for option in scenarios["sde-ws-17"].options).casefold()
    assert "alert" in " ".join(option["text"] for option in scenarios["sde-ws-22"].options).casefold()
    assert "fuso" in " ".join(option["text"] for option in scenarios["sde-ws-25"].options).casefold()
    api_options = " ".join(option["text"] for option in scenarios["sde-ws-31"].options).casefold()
    assert "limite" in api_options or "soglia" in api_options
    assert "simultanee" in " ".join(option["text"] for option in scenarios["sde-ws-23"].options).casefold()
    assert "annullati" in " ".join(option["text"] for option in scenarios["sde-ws-15"].options).casefold()
    assert "migrazione" in " ".join(option["text"] for option in scenarios["sde-ws-28"].options).casefold()
    assert "stima" in " ".join(option["text"] for option in scenarios["sde-ws-36"].options).casefold()
    assert len(catalog.study_plan) == 6
    planned = [lesson_id for day in catalog.study_plan for lesson_id in day["lesson_ids"]]
    planned += [lesson_id for day in catalog.study_plan for choice in day.get("choices", [])
                for branch in choice["options"].values() for lesson_id in branch.get("lesson_ids", [])]
    assert len(planned) == len(set(planned)) == len(catalog.lessons)
    planned_exercises = [exercise_id for day in catalog.study_plan for exercise_id in day.get("exercise_ids", [])]
    assert len(planned_exercises) == len(set(planned_exercises))
    assert {"sde-l-binary-variants", "sde-l-binary-answer"} <= {item.id for item in catalog.lessons}
    assert catalog.exercise_by_id["sde-e-trapping-rainwater"].lesson_id == "sde-l-two-pointers"
    assert catalog.exercise_by_id["sde-e-max-depth"].lesson_id == "sde-l-recursion"
    assert catalog.exercise_by_id["sde-e-climbing-stairs"].lesson_id == "sde-l-dp-memoization"
    combination_sum = catalog.exercise_by_id["sde-e-combination-sum"]
    assert "2^n" not in combination_sum.explanation
    assert "target" in combination_sum.explanation and "output" in combination_sum.explanation
    stairs = catalog.exercise_by_id["sde-e-climbing-stairs"]
    assert all("64 bit" not in case["name"] for case in stairs.tests)
    assert {simulation.kind for simulation in catalog.simulations} == {"coding", "repository", "full_mock"}
    assert catalog.simulations[-1].minutes == 100
    assert "possono variare per ruolo e paese" in catalog.meta["assessment_note"]
    assert catalog.meta["estimated_core_hours"] < catalog.meta["estimated_hours"]
    assert all("O(" in item.explanation for item in catalog.exercises)
    assert catalog.validate() == []


def test_amazon_repo_scaffolds_create_only_missing_files(tmp_path):
    from dev48.workspace import ensure_lab_workspace
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    for lab in catalog.labs:
        workspace = ensure_lab_workspace(tmp_path, lab)
        assert (workspace / "README.md").is_file()
        assert any(workspace.rglob("*.test.js")) or any(workspace.rglob("*.cpp"))
        assert not (workspace / "solution.js").exists()
        assert not (workspace / "solution.test.js").exists()
        assert not (workspace / "SOLUTION.md").exists()
        if lab.workspace_template == "amazon_cpp":
            assert not (workspace / "package.json").exists()
    final_test = tmp_path / "lab-amazon-mock-repository" / "test" / "routes.test.js"
    before = final_test.read_text(encoding="utf-8")
    ensure_lab_workspace(tmp_path, catalog.labs[-1])
    assert final_test.read_text(encoding="utf-8") == before
