from __future__ import annotations

from pathlib import Path
from time import monotonic
import asyncio
import json

from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import (
    Button, DataTable, Footer, Header, Input, Label, Markdown,
    ProgressBar, Static, TextArea,
)

from .database import InstanceLock, ProgressStore
from .models import Catalog, Exercise, Lab, Lesson, Simulation
from .runners import run_exercise, run_lab_tests
from .workspace import ensure_lab_workspace, install_lab_dependencies, open_vscode


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = PROJECT_ROOT / "content"
DATA_ROOT = PROJECT_ROOT / "data"
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"


GLOSSARY = {
    "Angular Standalone": "Architettura Angular moderna priva di NgModule: i componenti dichiarano direttamente dipendenze e template.",
    "API": "Contratto con cui due componenti software comunicano. Definisce operazioni, input, output ed errori.",
    "ASP.NET Core": "Framework open-source multipiattaforma di Microsoft per la creazione di Web API e servizi cloud ad alte prestazioni.",
    "Async/await": "Sintassi per comporre Promise o Task mantenendo leggibile il flusso asincrono.",
    "Autenticazione": "Verifica chi è l'utente. È distinta dall'autorizzazione, che stabilisce cosa può fare.",
    "C#": "Linguaggio moderno, fortemente tipizzato e orientato agli oggetti, con supporto avanzato per pattern matching, record e async.",
    "CORS": "Regola applicata dal browser alle richieste cross-origin. Non sostituisce autenticazione o autorizzazione.",
    "Closure": "Funzione che conserva accesso allo scope lessicale in cui è stata creata.",
    "Component": "Unità Angular o React che descrive una parte della UI a partire da stato e input.",
    "Controlled input": "Campo form il cui valore proviene dallo state e viene aggiornato tramite evento.",
    "CRUD": "Create, Read, Update, Delete: operazioni fondamentali sulle entità.",
    "DbContext": "Classe principale di Entity Framework Core che rappresenta una sessione con il database relazionale.",
    "Effect": "Sincronizzazione o side-effect dopo il render; in Angular effect() reagisce alle variazioni dei segnali.",
    "Entity Framework Core": "ORM ufficiale di .NET che astrae tabelle e relazioni del database in classi C# tipizzate.",
    "Foreign key": "Vincolo che collega una riga a una chiave di un'altra tabella.",
    "Immutabilità": "Creare un nuovo valore invece di modificare quello precedente; rende prevedibili gli aggiornamenti di stato.",
    "IPC": "Inter-process communication. In Electron collega renderer, preload e main process.",
    "JOIN": "Operazione SQL che combina righe correlate di più tabelle.",
    "JWT": "JSON Web Token: standard per l'autenticazione stateless basata su token compatti firmati digitalmente.",
    "Key React": "Identificatore stabile tra elementi fratelli, usato per riconciliare una lista.",
    "LINQ": "Language Integrated Query: sintassi dichiarativa di C# per interrogare e trasformare collezioni e database.",
    "Middleware": "Funzione nel percorso request/response che applica logica trasversale o prepara la richiesta.",
    "Minimal API": "Modello moderno e sintetico di ASP.NET Core per definire endpoint HTTP con elevate prestazioni.",
    "Promise": "Oggetto che rappresenta il futuro completamento o fallimento di un'operazione asincrona.",
    "Props": "Input di un componente forniti dal genitore e non modificabili dal figlio.",
    "RAG": "Recupero di informazioni pertinenti prima della generazione per aggiungere contesto a un modello.",
    "REST": "Stile di API orientato a risorse e semantica HTTP.",
    "Signals": "Primitiva reattiva moderna di Angular (signal, computed, effect) che traccia le modifiche allo stato in modo granulare.",
    "State": "Memoria locale di un componente che, quando aggiornata, provoca un aggiornamento reattivo.",
    "Transaction": "Gruppo di operazioni database atomico: riesce interamente oppure viene annullato.",
    "Type narrowing": "Riduzione di una union TypeScript mediante controlli che provano quale variante è presente.",
    "xUnit": "Framework moderno e standard di unit testing per .NET, guidato da attributi [Fact] e [Theory].",
    "XSS": "Esecuzione di contenuto non fidato nel browser; si mitiga con escaping e API sicure.",
}


class TimedScreen(Screen):
    tracked_id: str = ""
    tracked_type: str = "screen"

    def on_mount(self) -> None:
        self._entered_at = monotonic()
        if self.tracked_id:
            self.app.store.set_setting("last_item", self.tracked_id)

    def on_unmount(self) -> None:
        store = getattr(self.app, "store", None)
        if self.tracked_id and store:
            store.add_time(self.tracked_id, self.tracked_type, int(monotonic() - self._entered_at))


class TrackSelectionScreen(Screen):
    BINDINGS = [
        ("1", "select_dotnet", "Angular & .NET"),
        ("2", "select_react", "JS & React"),
        ("left", "previous_track", "Sinistra"),
        ("right", "next_track", "Destra"),
        ("up", "previous_track", "Precedente"),
        ("down", "next_track", "Successivo"),
        ("escape", "quit", "Esci"),
    ]

    def compose(self) -> ComposeResult:
        active = getattr(self.app.catalog, "track", "dotnet-angular")
        dotnet_catalog = Catalog(CONTENT_ROOT, track="dotnet-angular")
        react_catalog = Catalog(CONTENT_ROOT, track="web-js-react")
        yield Header(show_clock=True)
        with Vertical(id="track-selection-page"):
            yield Static(
                "[bold #67e8f9]DEV//48[/]  [#38bdf8]—[/]  [bold #a78bfa]ENTERPRISE WEB ACADEMY[/]\n"
                "[#91a4c7]Benvenuto! Scegli il tuo percorso di studio per iniziare (o premi Invio per confermare):[/]",
                id="track-hero",
            )
            with Horizontal(id="track-cards-row"):
                with Vertical(id="track-card-dotnet", classes="track-card" + (" active-card" if active == "dotnet-angular" else "")):
                    yield Static("[bold #34d399]PERCORSO 01[/]\n[bold #67e8f9]ANGULAR & .NET ENTERPRISE[/]", classes="card-header")
                    yield Static(
                        "[bold #ffffff]Stack Enterprise Moderno da Zero[/]\n\n"
                        "[#34d399]◆[/] [bold]C# 14[/] · Record, Pattern Matching & LINQ\n"
                        "[#34d399]◆[/] [bold]ASP.NET Core[/] · Minimal API & Dependency Injection\n"
                        "[#34d399]◆[/] [bold]Entity Framework Core[/] · SQLite & Migrazioni\n"
                        "[#34d399]◆[/] [bold]Angular Standalone[/] · Control Flow (@if, @for)\n"
                        "[#34d399]◆[/] [bold]Signals[/] · Stato reattivo e valori derivati\n"
                        "[#34d399]◆[/] [bold]Laboratori Monorepo[/] · client/ (Angular) + server/ (.NET)\n\n"
                        f"[#38bdf8]◆[/] [#91a4c7]{len(dotnet_catalog.lessons)} lezioni · {len(dotnet_catalog.exercises)} esercizi · {len(dotnet_catalog.flashcards)} flashcard[/]",
                        classes="card-desc",
                    )
                    yield Button("▶ SCEGLI ANGULAR & .NET [Tasto 1]", id="btn-dotnet", classes="primary")

                with Vertical(id="track-card-react", classes="track-card" + (" active-card" if active == "web-js-react" else "")):
                    yield Static("[bold #a78bfa]PERCORSO 02[/]\n[bold #f472b6]JAVASCRIPT & REACT ACADEMY[/]", classes="card-header")
                    yield Static(
                        "[bold #ffffff]Full-Stack Web Standard da Zero[/]\n\n"
                        "[#a78bfa]◆[/] [bold]JavaScript Moderno[/] · ES2024, Closure & Async/Await\n"
                        "[#a78bfa]◆[/] [bold]HTML & CSS[/] · Semantica, Flexbox, Grid & Responsive\n"
                        "[#a78bfa]◆[/] [bold]TypeScript[/] · Contratti di tipo & Generics\n"
                        "[#a78bfa]◆[/] [bold]React 19[/] · Componenti, Hooks, Form & Stato\n"
                        "[#a78bfa]◆[/] [bold]Backend Node.js[/] · Route, Servizi & SQLite SQL\n"
                        "[#a78bfa]◆[/] [bold]Testing Vitest[/] · Testing Library & TDD\n\n"
                        f"[#38bdf8]◆[/] [#91a4c7]{len(react_catalog.lessons)} lezioni · {len(react_catalog.exercises)} esercizi · {len(react_catalog.flashcards)} flashcard[/]",
                        classes="card-desc",
                    )
                    yield Button("▶ SCEGLI JS & REACT [Tasto 2]", id="btn-react", classes="success")

            yield Static(
                "[#91a4c7]Premi [bold #67e8f9]1[/] o [bold #f472b6]2[/], oppure seleziona con le frecce e premi [bold Invio]. "
                "Potrai cambiare traccia in qualsiasi momento premendo [bold #34d399]Ctrl+T[/] nella Dashboard.[/]",
                id="track-instruction",
            )
        yield Footer()

    def on_mount(self) -> None:
        active = getattr(self.app.catalog, "track", "dotnet-angular")
        if active == "dotnet-angular":
            self.set_focus(self.query_one("#btn-dotnet", Button))
        else:
            self.set_focus(self.query_one("#btn-react", Button))

    def action_select_dotnet(self) -> None:
        self.choose_track("dotnet-angular")

    def action_select_react(self) -> None:
        self.choose_track("web-js-react")

    def action_previous_track(self) -> None:
        self.set_focus(self.query_one("#btn-dotnet", Button))

    def action_next_track(self) -> None:
        self.set_focus(self.query_one("#btn-react", Button))

    def action_quit(self) -> None:
        self.app.exit()

    def choose_track(self, track: str) -> None:
        self.app.store.set_active_track(track)
        self.app.catalog = Catalog(CONTENT_ROOT, track=track)
        self.app.sync_app_title()
        self.app.pop_screen()
        self.app.push_screen(DashboardScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-dotnet":
            self.choose_track("dotnet-angular")
        elif event.button.id == "btn-react":
            self.choose_track("web-js-react")


class DashboardScreen(Screen):
    BINDINGS = [
        ("left", "previous_control", "Precedente"),
        ("right", "next_control", "Successivo"),
        ("up", "previous_control", "Precedente"),
        ("down", "next_control", "Successivo"),
        ("ctrl+t", "switch_track", "Cambia Traccia"),
    ]

    def compose(self) -> ComposeResult:
        stats = self.app.stats()
        track_title = "ANGULAR & .NET ENTERPRISE" if getattr(self.app.catalog, "track", "") == "dotnet-angular" else "JAVASCRIPT & REACT ACADEMY"
        yield Header(show_clock=True)
        with Vertical(classes="page", id="dashboard-page"):
            with ScrollableContainer(id="dashboard-content"):
                yield Static(
                    f"[bold #67e8f9]DEV//48[/]  [#34d399]{track_title}[/]  [#91a4c7]· Ctrl+T per cambiare traccia[/]\n"
                    "Impara, sperimenta e costruisci. Riparti esattamente da dove eri rimasto.",
                    classes="hero",
                )
                with Horizontal(classes="stats-row"):
                    yield Static(f"[bold #67e8f9]{stats['percent']}%[/]\nPROGRESSO", classes="stat-card")
                    yield Static(f"[bold #a78bfa]{stats['xp']}[/]\nXP", classes="stat-card")
                    yield Static(f"[bold #34d399]{stats['completed_lessons']}[/]/{stats['total_lessons']}\nLEZIONI", classes="stat-card")
                    yield Static(f"[bold #fbbf24]{stats['completed_exercises']}[/]/{stats['total_exercises']}\nESERCIZI", classes="stat-card last")
                yield Label("PROGRESSO COMPLESSIVO", classes="muted")
                yield ProgressBar(total=100, show_eta=False, id="overall-progress")
                yield Static(self.app.learning_plan_markup(), classes="panel")
                last_label = self.app.last_item_title()
                next_label = self.app.next_step_title()
                yield Static(
                    f"[bold #67e8f9]PROSSIMO PASSO[/]  {next_label}\n"
                    + (f"[bold #34d399]ULTIMA SCHERMATA[/]  {last_label}" if last_label else "[#91a4c7]ULTIMA SCHERMATA  Nessuna: il percorso è pronto per iniziare.[/]"),
                    id="last-item", classes="resume-info",
                )
            with Horizontal(classes="actions", id="dashboard-actions"):
                yield Button(
                    "▶ INIZIA" if not last_label else "▶ PROSSIMO PASSO",
                    id="continue", classes="primary",
                )
                yield Button(
                    "↩ ULTIMA SCHERMATA" if last_label else "↩ NESSUNA SCHERMATA",
                    id="resume", classes="success", disabled=not bool(last_label),
                )
                yield Button("▦ CURRICULUM", id="curriculum")
                yield Button("⚒ LAB", id="labs")
                yield Button("◈ FLASHCARD", id="flashcards")
                yield Button("◎ SFIDE", id="challenges")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#overall-progress", ProgressBar).update(progress=self.app.stats()["percent"])
        self.set_focus(self.query_one("#continue", Button))

    def action_previous_control(self) -> None:
        self.focus_previous()

    def action_next_control(self) -> None:
        self.focus_next()

    def action_switch_track(self) -> None:
        self.app.action_switch_track()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        actions = {
            "resume": self.app.resume_last,
            "continue": self.app.continue_course,
            "curriculum": lambda: self.app.push_screen(CurriculumScreen()),
            "labs": lambda: self.app.push_screen(LabsScreen()),
            "flashcards": lambda: self.app.push_screen(FlashcardsScreen()),
            "challenges": lambda: self.app.push_screen(ChallengesScreen()),
            "track": self.app.action_switch_track,
        }
        if event.button.id in actions:
            actions[event.button.id]()


class CurriculumScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro"), ("/", "search", "Cerca")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static("[bold #67e8f9]CURRICULUM[/]  Cerca e apri con Enter", classes="hero")
            yield Input(placeholder="Cerca titolo, modulo o obiettivo…", id="search")
            yield DataTable(cursor_type="row", zebra_stripes=True, id="table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#table", DataTable)
        table.add_columns("Stato", "Modulo", "Lezione", "Min", "Livello")
        self.refresh_rows("")
        self.set_focus(table)

    def action_search(self) -> None:
        self.set_focus(self.query_one("#search", Input))

    def refresh_rows(self, query: str) -> None:
        table = self.query_one("#table", DataTable)
        table.clear()
        completed = self.app.store.completed_ids()
        modules = {item["id"]: item["title"] for item in self.app.catalog.modules}
        needle = query.casefold().strip()
        for lesson in self.app.catalog.lessons:
            haystack = " ".join([lesson.title, modules[lesson.module], lesson.summary, *lesson.objectives]).casefold()
            if needle and needle not in haystack:
                continue
            state = "✓" if lesson.id in completed else ("◆" if lesson.mandatory else "·")
            table.add_row(state, modules[lesson.module], lesson.title, str(lesson.minutes), lesson.difficulty, key=lesson.id)

    def on_input_changed(self, event: Input.Changed) -> None:
        self.refresh_rows(event.value)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.app.push_screen(LessonScreen(str(event.row_key.value)))

    def action_back(self) -> None:
        self.app.pop_screen()


class LessonScreen(TimedScreen):
    BINDINGS = [
        ("escape", "back", "Indietro"),
        ("ctrl+s", "complete", "Completa"),
        ("left", "previous_control", "Sinistra"),
        ("right", "next_control", "Destra"),
        ("enter", "activate", "Conferma"),
    ]
    tracked_type = "lesson"

    def __init__(self, lesson_id: str) -> None:
        super().__init__()
        self.lesson_id = lesson_id
        self.tracked_id = lesson_id

    @property
    def lesson(self) -> Lesson:
        return self.app.catalog.lesson_by_id[self.lesson_id]

    def compose(self) -> ComposeResult:
        lesson = self.app.catalog.lesson_by_id[self.lesson_id]
        completed = self.app.store.completed_ids()
        lesson_done = lesson.id in completed
        pending_exercises = [item for item in self.app.catalog.exercises_for(lesson.id) if item.id not in completed]
        if not lesson_done:
            advance_label = "✓ COMPLETA E VAI AGLI ESERCIZI"
        elif pending_exercises:
            advance_label = "▶ VAI AL PROSSIMO ESERCIZIO"
        else:
            advance_label = "→ VAI ALLA PROSSIMA LEZIONE"
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]{lesson.title}[/]\n[#91a4c7]{lesson.minutes} min · {lesson.difficulty}[/]", classes="hero")
            with ScrollableContainer(id="lesson-scroll", can_focus=True):
                yield Markdown(self.app.catalog.lesson_body(lesson), id="lesson-markdown")
            with Horizontal(classes="actions"):
                yield Button(advance_label, id="advance", classes="primary")
                yield Button("← CURRICULUM", id="back")
        yield Footer()

    def on_mount(self) -> None:
        super().on_mount()
        self.set_focus(self.query_one("#lesson-scroll", ScrollableContainer))

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_complete(self) -> None:
        self.complete_and_advance()

    def action_next_control(self) -> None:
        advance = self.query_one("#advance", Button)
        back = self.query_one("#back", Button)
        if self.focused == advance:
            self.set_focus(back)
        else:
            self.set_focus(advance)

    def action_previous_control(self) -> None:
        advance = self.query_one("#advance", Button)
        back = self.query_one("#back", Button)
        if self.focused == back:
            self.set_focus(advance)
        else:
            self.set_focus(back)

    def action_activate(self) -> None:
        if isinstance(self.focused, Button):
            self.focused.press()
        else:
            self.complete_and_advance()

    def complete(self) -> None:
        self.app.store.complete_lesson(self.lesson_id)
        self.app.notify("Lezione completata · +20 XP", title="Progresso")

    def complete_and_advance(self) -> None:
        if self.app.store.get(self.lesson_id).get("status") != "completed":
            self.complete()
        exercises = self.app.catalog.exercises_for(self.lesson_id)
        completed = self.app.store.completed_ids()
        target = next((item for item in exercises if item.id not in completed), None)
        if target:
            self.app.push_screen(ExerciseScreen(target.id))
        else:
            self.app.continue_course()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "advance":
            self.complete_and_advance()
        elif event.button.id == "back":
            self.app.pop_screen()


class ExerciseScreen(TimedScreen):
    BINDINGS = [
        ("escape", "back", "Indietro"), ("f5", "run", "Esegui"),
        ("h", "hint", "Indizio"), ("ctrl+s", "save", "Salva"),
        ("f1", "toggle_theory", "Teoria"),
        ("ctrl+right", "next_exercise", "Successivo"),
    ]
    tracked_type = "exercise"

    def __init__(self, exercise_id: str) -> None:
        super().__init__()
        self.exercise_id = exercise_id
        self.tracked_id = exercise_id
        self.theory_open = False

    @property
    def exercise(self) -> Exercise:
        return self.app.catalog.exercise_by_id[self.exercise_id]

    def compose(self) -> ComposeResult:
        ex = self.app.catalog.exercise_by_id[self.exercise_id]
        state = self.app.store.get(ex.id)
        initial = state.get("answer") or ex.starter
        language = {"javascript":"javascript","react":"javascript","typescript":"typescript","csharp":"csharp","angular":"typescript","html":"html","css":"css","sql":"sql"}.get(ex.kind)
        reward = "autovalutazione · nessun XP" if ex.kind == "reflection" else f"{ex.xp} XP"
        scope_note = {
            "csharp": "Il runner compila il codice ed esegue i casi dichiarati nell'esercizio; non garantisce ogni possibile comportamento.",
            "angular": "Il runner prova la logica TypeScript con piccoli mock: non avvia Angular, non compila i template, non esegue tsc e non controlla il DOM. Usa i laboratori per provare un progetto Angular reale.",
            "typescript": "Il controllo verifica la sintassi eseguibile e i requisiti indicati; non sostituisce `tsc` né un progetto Angular completo.",
            "html": "Il controllo verifica struttura e requisiti testuali; non esegue il rendering in un browser.",
            "css": "Il controllo verifica requisiti testuali; non esegue il rendering o la resa responsive in un browser.",
            "reflection": "Questa autoverifica cerca i termini richiesti; non valuta il significato. Confronta la spiegazione con il modello.",
        }.get(ex.kind, "Il runner mostra i controlli automatici previsti per questo esercizio.")
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]{ex.title}[/]\n[#91a4c7]{ex.kind.upper()} · {ex.minutes} min · {reward} · tentativi: {state.get('attempts', 0)}[/]", classes="hero")
            with Horizontal(id="exercise-layout"):
                with Vertical(id="exercise-left"):
                    with ScrollableContainer(id="exercise-prompt", can_focus=True):
                        yield Static(f"[bold #a78bfa]Come funziona il controllo:[/] {scope_note}", id="exercise-scope", classes="panel")
                        yield Markdown(ex.prompt)
                        if ex.creative_goals:
                            goals_txt = "\n".join(f"- ★ {g}" for g in ex.creative_goals)
                            yield Static(f"\n[bold #34d399]Estensioni facoltative · non valutate automaticamente[/]\n{goals_txt}", classes="panel")
                        yield Static("\n[bold #a78bfa]Regola[/]\nProva autonomamente. F5 esegue; H mostra un indizio. La soluzione si sblocca dopo due fallimenti.", classes="panel")
                    with ScrollableContainer(id="theory-scroll", can_focus=True):
                        yield Static("[bold #a78bfa]TEORIA DELLA LEZIONE[/]\nF1 apre o richiude la teoria senza perdere risposta, cursore o punto di lettura. ESC torna prima all'esercizio; da lì puoi rientrare nella lezione al punto in cui l'avevi lasciata.", classes="panel")
                        yield Markdown(self.app.catalog.lesson_body(self.app.catalog.lesson_by_id[ex.lesson_id]), id="theory-markdown")
                with Vertical(id="exercise-right"):
                    yield TextArea(initial, language=language, show_line_numbers=True, id="editor")
                    yield Static("Pronto. Scrivi la soluzione e premi F5.", id="result")
            with Horizontal(id="exercise-actions", classes="actions"):
                yield Button("▶ ESEGUI [F5]", id="run", classes="primary")
                yield Button("◇ INDIZIO [H]", id="hint")
                yield Button("⌁ SOLUZIONE", id="solution", classes="warning")
                yield Button("→ PROSSIMO", id="next")
                yield Button("📖 TEORIA [F1]", id="theory")
                yield Button("← LEZIONE", id="back")
        yield Footer()

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#theory-scroll", ScrollableContainer).display = False
        self.set_focus(self.query_one("#editor", TextArea))

    def editor_value(self) -> str:
        return self.query_one("#editor", TextArea).text

    def action_save(self) -> None:
        self.app.store.save_answer(self.exercise.id, "exercise", self.editor_value())
        self.app.notify("Risposta salvata")

    def action_toggle_theory(self) -> None:
        self.app.store.save_answer(self.exercise.id, "exercise", self.editor_value())
        self.theory_open = not self.theory_open
        prompt = self.query_one("#exercise-prompt", ScrollableContainer)
        theory = self.query_one("#theory-scroll", ScrollableContainer)
        prompt.display = not self.theory_open
        theory.display = self.theory_open
        button = self.query_one("#theory", Button)
        button.label = "↩ ESERCIZIO [F1]" if self.theory_open else "📖 TEORIA [F1]"
        self.query_one("#back", Button).label = "↩ ESERCIZIO" if self.theory_open else "← LEZIONE"
        if self.theory_open:
            self.set_focus(theory)
        else:
            self.set_focus(self.query_one("#editor", TextArea))

    def action_run(self) -> None:
        self.run_current()

    def run_current(self) -> None:
        answer = self.editor_value()
        result = run_exercise(self.exercise, answer, PROJECT_ROOT)
        earned_xp = 0 if self.exercise.kind == "reflection" else int(self.exercise.xp * result.score / 100)
        attempts = self.app.store.record_attempt(self.exercise.id, "exercise", answer, result.passed, earned_xp)
        icon = "✓" if result.passed else "✗"
        color = "#34d399" if result.passed else "#fb7185"
        details = "\n".join(result.details)
        if self.exercise.kind == "reflection":
            matches = sum(item.startswith("✓") for item in result.details)
            label = f"AUTOVERIFICA · {matches}/{len(result.details)} termini presenti"
            self.query_one("#result", Static).update(f"[bold #fbbf24]{label}[/]\nLa checklist non valuta il significato. Confronta la spiegazione con il modello.\n\n{details}")
        else:
            self.query_one("#result", Static).update(f"[bold {color}]{icon} {result.score}%[/]\n{result.output}\n\n{details}")
        if result.passed and self.exercise.kind == "reflection":
            self.app.notify("Autoverifica completata · confronta la risposta con il modello.", title="Richiamo")
        elif result.passed:
            self.app.notify(f"Esercizio superato · +{self.exercise.xp} XP", title="Ottimo")
        elif attempts >= 2:
            self.app.notify("La soluzione completa è ora sbloccata.", severity="warning")

    def action_hint(self) -> None:
        state = self.app.store.get(self.exercise.id)
        level = min(int(state.get("hint_level", 0)) + 1, len(self.exercise.hints))
        self.app.store.set_hint(self.exercise.id, level)
        hints = "\n".join(f"{i}. {hint}" for i, hint in enumerate(self.exercise.hints[:level], 1))
        self.query_one("#result", Static).update(f"[bold #fbbf24]INDIZI {level}/{len(self.exercise.hints)}[/]\n{hints}")

    def show_solution(self) -> None:
        state = self.app.store.get(self.exercise.id)
        if int(state.get("attempts", 0)) < 2:
            remaining = 2 - int(state.get("attempts", 0))
            self.query_one("#result", Static).update(f"[bold #fbbf24]SOLUZIONE BLOCCATA[/]\nServono ancora {remaining} tentativi reali. Usa H per un indizio.")
            return
        text = f"SOLUZIONE COMMENTATA\n\n{self.exercise.solution}\n\n{self.exercise.explanation}"
        self.query_one("#result", Static).update(text)

    def action_next_exercise(self) -> None:
        self.next_exercise()

    def next_exercise(self) -> None:
        if self.app.store.get(self.exercise.id).get("status") != "completed":
            self.app.notify("Supera questo esercizio prima di passare al prossimo passo.", severity="warning")
            return
        exercises = self.app.catalog.exercises_for(self.exercise.lesson_id)
        completed = self.app.store.completed_ids()
        target = next((item for item in exercises if item.id not in completed), None)
        if target:
            self.app.switch_screen(ExerciseScreen(target.id))
            return
        self.app.action_dashboard()
        self.app.continue_course()

    def action_back(self) -> None:
        if self.theory_open:
            self.action_toggle_theory()
            return
        self.action_save()
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        actions = {"run":self.run_current,"hint":self.action_hint,"solution":self.show_solution,"next":self.next_exercise,"theory":self.action_toggle_theory,"back":self.action_back}
        if event.button.id in actions:
            actions[event.button.id]()


class LabsScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static("[bold #67e8f9]LABORATORI[/]\nProgetti più lunghi, workspace persistente e test reali.", classes="hero")
            yield DataTable(cursor_type="row", zebra_stripes=True, id="table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#table", DataTable)
        table.add_columns("Laboratorio", "Modulo", "Min", "Descrizione")
        for lab in self.app.catalog.labs:
            table.add_row(lab.title, lab.module, str(lab.minutes), lab.description, key=lab.id)
        self.set_focus(table)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.app.push_screen(LabScreen(str(event.row_key.value)))

    def action_back(self) -> None:
        self.app.pop_screen()


class LabScreen(TimedScreen):
    BINDINGS = [
        ("escape", "back", "Indietro"),
        ("left", "previous_control", "Sinistra"),
        ("right", "next_control", "Destra"),
        ("enter", "activate", "Conferma"),
    ]
    tracked_type = "lab"

    def __init__(self, lab_id: str) -> None:
        super().__init__()
        self.lab_id = lab_id
        self.tracked_id = lab_id

    @property
    def lab(self) -> Lab:
        return self.app.catalog.lab_by_id[self.lab_id]

    def compose(self) -> ComposeResult:
        lab = self.app.catalog.lab_by_id[self.lab_id]
        requirements = "\n".join(f"- [ ] {x}" for x in lab.requirements)
        rubric = "\n".join(f"- {x}" for x in lab.rubric)
        creative = ""
        if lab.creative_goals:
            goals = "\n".join(f"- ★ {x}" for x in lab.creative_goals)
            creative = f"\n\n## Estensioni facoltative (autovalutazione)\n{goals}"
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]{lab.title}[/]\n[#91a4c7]{lab.minutes} min · {lab.difficulty}[/]", classes="hero")
            with ScrollableContainer(id="lab-scroll", can_focus=True):
                yield Markdown(f"## Brief\n\n{lab.description}\n\n## Requisiti\n\n{requirements}\n\n## Rubrica\n\n{rubric}{creative}\n\n> **Verifica automatica:** l'app esegue la suite xUnit e/o Angular presente nel workspace. Un esito verde conferma quei test; rileggi la rubrica per i criteri non coperti. Il workspace non viene sovrascritto quando riapri l'app.")
                yield Static("Pronto.", id="lab-result", classes="panel")
            with Horizontal(classes="actions"):
                yield Button("▣ APRI VS CODE", id="open", classes="primary")
                yield Button("↓ INSTALLA DIPENDENZE", id="install")
                yield Button("▶ ESEGUI TEST", id="test", classes="success")
                yield Button("← LAB", id="back")
        yield Footer()

    def on_mount(self) -> None:
        super().on_mount()
        self.set_focus(self.query_one("#lab-scroll", ScrollableContainer))

    def action_next_control(self) -> None:
        buttons = [
            self.query_one("#open", Button),
            self.query_one("#install", Button),
            self.query_one("#test", Button),
            self.query_one("#back", Button),
        ]
        try:
            idx = buttons.index(self.focused)
            self.set_focus(buttons[(idx + 1) % len(buttons)])
        except (ValueError, TypeError):
            self.set_focus(buttons[0])

    def action_previous_control(self) -> None:
        buttons = [
            self.query_one("#open", Button),
            self.query_one("#install", Button),
            self.query_one("#test", Button),
            self.query_one("#back", Button),
        ]
        try:
            idx = buttons.index(self.focused)
            self.set_focus(buttons[(idx - 1) % len(buttons)])
        except (ValueError, TypeError):
            self.set_focus(buttons[-1])

    def action_activate(self) -> None:
        if isinstance(self.focused, Button):
            self.focused.press()
        else:
            self.set_focus(self.query_one("#open", Button))

    def workspace(self) -> Path:
        return ensure_lab_workspace(self.app.workspace_root, self.lab)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        result = self.query_one("#lab-result", Static)
        if event.button.id == "open":
            ok, message = open_vscode(self.workspace())
            result.update(message)
        elif event.button.id == "install":
            result.update("Installazione in corso… può richiedere alcuni minuti al primo avvio.")
            ok, message = await asyncio.to_thread(install_lab_dependencies, self.workspace())
            result.update(("[bold #34d399]COMPLETATA[/]\n" if ok else "[bold #fb7185]ERRORE[/]\n") + message)
        elif event.button.id == "test":
            result.update("Test in esecuzione…")
            test_result = await asyncio.to_thread(run_lab_tests, self.workspace())
            status_text = "[bold #34d399]TEST SUPERATI[/]\n" if test_result.passed else "[bold #fb7185]TEST FALLITI[/]\n"
            score = 100 if test_result.passed else 0
            result.update(status_text + test_result.output)
            self.app.store.record_attempt(self.lab.id, "lab", str(self.workspace()), test_result.passed, score)
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()


class FlashcardsScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro"), ("space", "flip", "Risposta"), ("right", "next", "Avanti"), ("left", "previous", "Indietro")]

    def __init__(self) -> None:
        super().__init__()
        self.index = 0
        self.flipped = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]FLASHCARD[/]\n{len(self.app.catalog.flashcards)} domande per il recupero attivo. Spazio mostra la risposta.", classes="hero")
            yield Static("", id="card", classes="panel")
            with Horizontal(classes="actions"):
                yield Button("← PRECEDENTE", id="previous")
                yield Button("MOSTRA RISPOSTA", id="flip", classes="primary")
                yield Button("SUCCESSIVA →", id="next")
        yield Footer()

    def on_mount(self) -> None:
        self.render_card()
        self.set_focus(self.query_one("#flip", Button))

    def render_card(self) -> None:
        card = self.app.catalog.flashcards[self.index]
        answer = f"\n\n[bold #34d399]RISPOSTA[/]\n{card.answer}" if self.flipped else "\n\n[#91a4c7]Formula la risposta ad alta voce prima di premere Spazio.[/]"
        self.query_one("#card", Static).update(f"[#a78bfa]{self.index+1}/{len(self.app.catalog.flashcards)} · {card.module.upper()}[/]\n\n[bold]{card.question}[/]{answer}")

    def action_flip(self) -> None:
        self.flipped = not self.flipped
        self.render_card()

    def action_next(self) -> None:
        self.index = (self.index + 1) % len(self.app.catalog.flashcards)
        self.flipped = False
        self.render_card()

    def action_previous(self) -> None:
        self.index = (self.index - 1) % len(self.app.catalog.flashcards)
        self.flipped = False
        self.render_card()

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        {"flip":self.action_flip,"next":self.action_next,"previous":self.action_previous}.get(event.button.id, lambda: None)()


class GlossaryScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro"), ("/", "search", "Cerca")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static("[bold #67e8f9]GLOSSARIO[/]", classes="hero")
            yield Input(placeholder="Cerca un termine…", id="search")
            with ScrollableContainer(id="glossary-scroll", can_focus=True):
                yield Markdown("", id="glossary")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_terms("")
        self.set_focus(self.query_one("#glossary-scroll", ScrollableContainer))

    def action_search(self) -> None:
        self.set_focus(self.query_one("#search", Input))

    def refresh_terms(self, query: str) -> None:
        needle = query.casefold()
        items = [(term, definition) for term, definition in GLOSSARY.items() if needle in (term + definition).casefold()]
        self.query_one("#glossary", Markdown).update("\n\n".join(f"## {term}\n\n{definition}" for term, definition in items) or "Nessun termine trovato.")

    def on_input_changed(self, event: Input.Changed) -> None:
        self.refresh_terms(event.value)

    def action_back(self) -> None:
        self.app.pop_screen()


class ChallengesScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static("[bold #67e8f9]SIMULAZIONI[/]\nCronometro, brief e checklist. Parla mentre ragioni.", classes="hero")
            yield DataTable(cursor_type="row", zebra_stripes=True, id="table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#table", DataTable)
        table.add_columns("Simulazione", "Minuti", "Brief")
        for sim in self.app.catalog.simulations:
            table.add_row(sim.title, str(sim.minutes), sim.brief, key=sim.id)
        self.set_focus(table)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        sim = next(item for item in self.app.catalog.simulations if item.id == str(event.row_key.value))
        self.app.push_screen(SimulationScreen(sim))

    def action_back(self) -> None:
        self.app.pop_screen()


class SimulationScreen(TimedScreen):
    BINDINGS = [
        ("escape", "back", "Indietro"),
        ("space", "toggle", "Avvia/Pausa"),
        ("left", "previous_control", "Sinistra"),
        ("right", "next_control", "Destra"),
        ("enter", "activate", "Conferma"),
    ]
    tracked_type = "simulation"

    def __init__(self, simulation: Simulation) -> None:
        super().__init__()
        self.simulation = simulation
        self.tracked_id = simulation.id
        self.remaining = simulation.minutes * 60
        self.running = False

    def compose(self) -> ComposeResult:
        checklist = "\n".join(f"- [ ] {item}" for item in self.simulation.checklist)
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]{self.simulation.title}[/]", classes="hero")
            yield Static("", id="timer", classes="stat-card")
            with ScrollableContainer(id="lab-scroll", can_focus=True):
                yield Markdown(f"## Brief\n\n{self.simulation.brief}\n\n## Checklist\n\n{checklist}\n\n## Regola\n\nNiente IA durante il timer. Puoi consultare documentazione tecnica e prendere appunti, ma prova a completare la sfida in autonomia.")
            with Horizontal(classes="actions"):
                yield Button("▶ AVVIA / PAUSA [SPAZIO]", id="toggle", classes="primary")
                yield Button("↺ RESET", id="reset")
                yield Button("← SIMULAZIONI", id="back")
        yield Footer()

    def on_mount(self) -> None:
        super().on_mount()
        self.set_interval(1, self.tick)
        self.render_timer()
        self.set_focus(self.query_one("#lab-scroll", ScrollableContainer))

    def action_next_control(self) -> None:
        buttons = [
            self.query_one("#toggle", Button),
            self.query_one("#reset", Button),
            self.query_one("#back", Button),
        ]
        try:
            idx = buttons.index(self.focused)
            self.set_focus(buttons[(idx + 1) % len(buttons)])
        except (ValueError, TypeError):
            self.set_focus(buttons[0])

    def action_previous_control(self) -> None:
        buttons = [
            self.query_one("#toggle", Button),
            self.query_one("#reset", Button),
            self.query_one("#back", Button),
        ]
        try:
            idx = buttons.index(self.focused)
            self.set_focus(buttons[(idx - 1) % len(buttons)])
        except (ValueError, TypeError):
            self.set_focus(buttons[-1])

    def action_activate(self) -> None:
        if isinstance(self.focused, Button):
            self.focused.press()
        else:
            self.action_toggle()

    def tick(self) -> None:
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.render_timer()
        if self.remaining == 0 and self.running:
            self.running = False
            self.app.notify("Tempo terminato. Completa la checklist e valuta il risultato.", severity="warning")

    def render_timer(self) -> None:
        minutes, seconds = divmod(self.remaining, 60)
        state = "IN CORSO" if self.running else "IN PAUSA"
        self.query_one("#timer", Static).update(f"[bold #67e8f9]{minutes:02d}:{seconds:02d}[/]\n{state}")

    def action_toggle(self) -> None:
        self.running = not self.running
        self.render_timer()

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "toggle":
            self.action_toggle()
        elif event.button.id == "reset":
            self.remaining = self.simulation.minutes * 60
            self.running = False
            self.render_timer()
        elif event.button.id == "back":
            self.app.pop_screen()


class Dev48App(App):
    TITLE = "DEV//48 — Enterprise Web Academy"
    SUB_TITLE = "Angular & .NET / Full-Stack · Studio intensivo offline"
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("ctrl+d", "dashboard", "Dashboard", priority=True),
        Binding("ctrl+k", "curriculum", "Curriculum", priority=True),
        Binding("ctrl+g", "glossary", "Glossario", priority=True),
        Binding("ctrl+q", "quit", "Esci", priority=True),
    ]

    def __init__(self, data_root: Path = DATA_ROOT, workspace_root: Path = WORKSPACE_ROOT, select_track: bool = True) -> None:
        super().__init__()
        self.data_root = data_root
        self.workspace_root = workspace_root
        self.select_track = select_track
        self.lock = InstanceLock(self.data_root / ".dev48.lock")
        if not self.lock.acquire():
            raise RuntimeError("DEV//48 è già aperto in un'altra finestra.")
        try:
            self.store = ProgressStore(self.data_root)
            self.workspace_root.mkdir(parents=True, exist_ok=True)
            active_track = self.store.get_active_track("dotnet-angular")
            self.catalog = Catalog(CONTENT_ROOT, track=active_track)
            self.sync_app_title()
        except Exception:
            self.lock.release()
            raise
        errors = self.catalog.validate()
        if errors:
            raise RuntimeError("Catalogo non valido:\n" + "\n".join(errors))

    def sync_app_title(self) -> None:
        track = getattr(self.catalog, "track", "dotnet-angular")
        if track == "dotnet-angular":
            self.title = "DEV//48 — Angular & .NET Enterprise Academy"
            self.sub_title = ".NET 10 · Minimal API · EF Core · Angular 22 Signals"
        else:
            self.title = "DEV//48 — Web Development Academy"
            self.sub_title = "JavaScript · React 19 · Node.js · SQL"

    def on_mount(self) -> None:
        self.update_compact_mode(self.size.height)
        self.sync_app_title()
        if self.select_track:
            self.push_screen(TrackSelectionScreen())
        else:
            self.push_screen(DashboardScreen())

    def on_resize(self, event: events.Resize) -> None:
        self.update_compact_mode(event.size.height)

    def update_compact_mode(self, height: int) -> None:
        self.set_class(height < 24, "compact-height")

    def stats(self) -> dict:
        track_item_ids = {item.id for item in self.catalog.lessons + self.catalog.exercises}
        return self.store.stats(len(self.catalog.lessons), len(self.catalog.exercises), track_item_ids)

    def learning_plan_markup(self) -> str:
        completed = self.store.completed_ids()
        required = [item for item in self.catalog.lessons if item.mandatory]
        done = sum(item.id in completed for item in required)
        minutes = sum(item.minutes for item in required)
        bars = int(20 * done / max(1, len(required)))
        track_name = self.catalog.meta.get("name", "DEV//48")
        lines = [f"[bold #a78bfa]PERCORSO: {track_name}[/]"]
        lines.append(f"\n[{'█' * bars}{'░' * (20-bars)}]  {done}/{len(required)} lezioni essenziali · {minutes//60}h {minutes%60:02d}m")
        lines.append(f"\n{len(self.catalog.modules)} moduli · {len(self.catalog.labs)} laboratori · {len(self.catalog.simulations)} sfide pratiche")
        lines.append("\n[#91a4c7]◆ obbligatorio   · approfondimento   Ctrl+T cambia traccia   Ctrl+K curriculum   Ctrl+G glossario[/]")
        return "".join(lines)

    def action_switch_track(self) -> None:
        new_track = "web-js-react" if getattr(self.catalog, "track", "") == "dotnet-angular" else "dotnet-angular"
        self.store.set_active_track(new_track)
        self.catalog = Catalog(CONTENT_ROOT, track=new_track)
        self.sync_app_title()
        track_label = self.catalog.meta.get("name", new_track)
        self.notify(f"Passato a: {track_label}", title="Traccia Attiva Aggiornata")
        self.action_dashboard()
        if len(self.screen_stack) > 1:
            self.pop_screen()
        self.push_screen(DashboardScreen())

    def last_item_title(self) -> str:
        last = self.store.get_setting("last_item")
        if last in self.catalog.lesson_by_id:
            return self.catalog.lesson_by_id[last].title
        if last in self.catalog.exercise_by_id:
            return self.catalog.exercise_by_id[last].title
        if last in self.catalog.lab_by_id:
            return self.catalog.lab_by_id[last].title
        simulation = next((item for item in self.catalog.simulations if item.id == last), None)
        return simulation.title if simulation else ""

    def next_step(self) -> tuple[str, Lesson | Exercise] | None:
        completed = self.store.completed_ids()
        for lesson in (item for item in self.catalog.lessons if item.mandatory):
            if lesson.id not in completed:
                return "lesson", lesson
            for exercise in self.catalog.exercises_for(lesson.id):
                if exercise.id not in completed:
                    return "exercise", exercise
        return None

    def next_step_title(self) -> str:
        step = self.next_step()
        if not step:
            return "Percorso obbligatorio completato: passa a laboratori e simulazioni."
        kind, item = step
        prefix = "Lezione" if kind == "lesson" else "Esercizio"
        return f"{prefix}: {item.title}"

    def resume_last(self) -> None:
        last = self.store.get_setting("last_item")
        if last in self.catalog.lesson_by_id:
            self.push_screen(LessonScreen(last))
            return
        if last in self.catalog.exercise_by_id:
            self.push_screen(ExerciseScreen(last))
            return
        if last in self.catalog.lab_by_id:
            self.push_screen(LabScreen(last))
            return
        simulation = next((item for item in self.catalog.simulations if item.id == last), None)
        if simulation:
            self.push_screen(SimulationScreen(simulation))
            return
        self.notify("Non c'è ancora un ultimo punto da riprendere.", severity="warning")

    def continue_course(self) -> None:
        step = self.next_step()
        if not step:
            self.notify("Percorso obbligatorio completato. Ora scegli un laboratorio o una simulazione.", title="Sprint completato")
            return
        kind, item = step
        if kind == "lesson":
            self.push_screen(LessonScreen(item.id))
        else:
            self.push_screen(ExerciseScreen(item.id))

    def action_dashboard(self) -> None:
        # Lo stack contiene sempre la schermata Textual predefinita sotto la
        # dashboard; preserviamo entrambe e chiudiamo soltanto le viste aperte.
        while len(self.screen_stack) > 2:
            self.pop_screen()

    def action_curriculum(self) -> None:
        self.push_screen(CurriculumScreen())

    def action_glossary(self) -> None:
        self.push_screen(GlossaryScreen())

    def on_exit_app(self) -> None:
        self.shutdown_resources()

    def shutdown_resources(self) -> None:
        store = getattr(self, "store", None)
        if store:
            store.close()
            self.store = None
        lock = getattr(self, "lock", None)
        if lock:
            lock.release()

    def exit(self, *args, **kwargs):
        self.shutdown_resources()
        return super().exit(*args, **kwargs)
