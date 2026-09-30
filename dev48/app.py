from __future__ import annotations

from pathlib import Path
from time import monotonic
import asyncio
import json
import hashlib
import re

from textual import events, on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from rich.cells import cell_len
from rich.text import Text as RichText
from textual.widgets import (
    Button, Collapsible, DataTable, Footer, Header, Input, Label, Markdown,
    ProgressBar, Static, TextArea,
)

from .database import InstanceLock, ProgressStore
from .models import Catalog, Exercise, Lab, Lesson, Simulation, TRACK_DEFINITIONS, WorkScenario, WorkStylePrompt
from .runners import run_exercise, run_lab_tests
from .workspace import ensure_lab_workspace, install_lab_dependencies, open_vscode


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = PROJECT_ROOT / "content"
DATA_ROOT = PROJECT_ROOT / "data"
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"

CODE_EDITOR_KINDS = frozenset({
    "angular", "cpp", "csharp", "css", "html", "javascript", "python", "react", "sql", "typescript",
})
BRACE_INDENT_LANGUAGES = frozenset({
    "angular", "cpp", "csharp", "css", "javascript", "react", "typescript",
})


def _code_context_at(source: str, offset: int, language: str) -> str:
    """Return whether an offset is in code, a string, or a comment."""
    state = "code"
    quote = ""
    raw_end = ""
    verbatim = False
    multiline = False
    index = 0
    end = min(max(offset, 0), len(source))

    while index < end:
        if state == "line_comment":
            if source[index] == "\n":
                state = "code"
            index += 1
            continue
        if state == "block_comment":
            if source.startswith("*/", index):
                state = "code"
                index += 2
            else:
                index += 1
            continue
        if state == "raw_string":
            if source.startswith(raw_end, index):
                state = "code"
                index += len(raw_end)
            else:
                index += 1
            continue
        if state == "string":
            character = source[index]
            if verbatim and quote == '"' and source.startswith('""', index):
                index += 2
                continue
            if not verbatim and character == "\\":
                index += 2
                continue
            if character == quote:
                state = "code"
                quote = ""
                verbatim = False
            elif character == "\n" and not multiline:
                # Recover from an unfinished ordinary string at the next line.
                state = "code"
                quote = ""
            index += 1
            continue

        if source.startswith("//", index):
            state = "line_comment"
            index += 2
            continue
        if source.startswith("/*", index):
            state = "block_comment"
            index += 2
            continue
        if language == "cpp" and source.startswith('R"', index):
            opening_paren = source.find("(", index + 2)
            if opening_paren >= 0:
                delimiter = source[index + 2:opening_paren]
                if len(delimiter) <= 16 and not any(char.isspace() or char in "()\\" for char in delimiter):
                    raw_end = ")" + delimiter + '"'
                    state = "raw_string"
                    index = opening_paren + 1
                    continue
        if language == "csharp" and source[index] == '"':
            quote_count = 1
            while index + quote_count < len(source) and source[index + quote_count] == '"':
                quote_count += 1
            if quote_count >= 3:
                raw_end = '"' * quote_count
                state = "raw_string"
                index += quote_count
                continue
        character = source[index]
        if language in {"javascript", "react", "typescript", "angular"} and character == "`":
            state = "string"
            quote = character
            multiline = True
        elif character in "\"'":
            state = "string"
            quote = character
            verbatim = language == "csharp" and character == '"' and index > 0 and source[index - 1] == "@"
            multiline = verbatim
        index += 1

    if state in {"line_comment", "block_comment"}:
        return "comment"
    if state != "code":
        return "string"
    return "code"


def _code_prefix_end(source: str, start: int, end: int, language: str) -> int:
    """Ignore a trailing C-style comment when checking a line's final token."""
    index = start
    while index < end:
        if source.startswith("//", index) and _code_context_at(source, index, language) == "code":
            return index
        if source.startswith("/*", index) and _code_context_at(source, index, language) == "code":
            close = source.find("*/", index + 2, end)
            if close < 0 or not source[close + 2:end].strip(" \t"):
                return index
            index = close + 2
            continue
        index += 1
    return end


def _dedent_one_level(indentation: str, width: int) -> str:
    """Remove one indentation level from leading spaces and tabs."""
    target = max(1, width)
    columns = 0
    index = 0
    while index < len(indentation) and columns < target:
        character = indentation[index]
        if character == "\t":
            columns += target - (columns % target)
        elif character == " ":
            columns += 1
        else:
            break
        index += 1
    return indentation[index:] if columns >= target else indentation


class CodeTextArea(TextArea):
    """TextArea with automatic indentation for programming code."""

    def __init__(self, *args, brace_indentation: bool = False, brace_language: str = "", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.brace_indentation = brace_indentation
        self.brace_language = brace_language

    @on(events.Key)
    def _handle_code_indentation(self, event: events.Key) -> None:
        if self.read_only:
            return

        selection = self.selection
        start, end = selection
        insertion_location = min(start, end)
        row, column = insertion_location
        lines = self.text.split("\n")
        line = lines[row]

        if event.key == "enter":
            indentation = line[:len(line) - len(line.lstrip(" \t"))]
            continuation = indentation
            if self.brace_indentation:
                source = self.text
                line_start = sum(len(item) + 1 for item in lines[:row])
                cursor_offset = line_start + column
                prefix_end = _code_prefix_end(source, line_start, cursor_offset, self.brace_language)
                prefix = source[line_start:prefix_end].rstrip(" \t")
                if prefix.endswith("{"):
                    brace_offset = line_start + len(prefix) - 1
                    if _code_context_at(source, brace_offset, self.brace_language) == "code":
                        continuation += " " * max(1, self.indent_width)
            event.stop()
            event.prevent_default()
            self.replace("\n" + continuation, start, end, maintain_selection_offset=False)
            return

        if event.character != "}" or not self.brace_indentation or not selection.is_empty:
            return
        if line.strip(" \t"):
            return

        source = self.text
        line_start = sum(len(item) + 1 for item in lines[:row])
        cursor_offset = line_start + column
        if _code_context_at(source, cursor_offset, self.brace_language) != "code":
            return
        indentation = line
        outdented = _dedent_one_level(indentation, self.indent_width)
        event.stop()
        event.prevent_default()
        self.replace(outdented + "}", (row, 0), (row, len(line)), maintain_selection_offset=False)


def exercise_progress_id(exercise: Exercise, language: str = "python") -> str:
    return f"{exercise.id}@{language}" if exercise.variants else exercise.id


def split_exercise_progress_id(item_id: str) -> tuple[str, str | None]:
    if "@" not in item_id:
        return item_id, None
    exercise_id, language = item_id.rsplit("@", 1)
    return exercise_id, language


def exercise_started_setting_key(progress_id: str) -> str:
    return f"exercise_started:{progress_id}"


class FooterHint(Static):
    """A compact, clickable key hint used by the adaptive footer."""

    DEFAULT_CSS = """
    FooterHint {
        width: auto;
        height: 1;
        min-width: 0;
        padding: 0 1;
        margin-right: 1;
        color: #91a4c7;
        background: #182238;
        text-wrap: nowrap;
    }
    FooterHint.-disabled {
        text-style: dim;
    }
    FooterHint.-wrapped {
        width: 100%;
        height: auto;
        text-wrap: wrap;
    }
    """

    def __init__(self, key: str, key_display: str, description: str, action: str, *, disabled: bool = False, tooltip: str = "", wrapped: bool = False) -> None:
        self.key = key
        self.key_display = key_display
        self.description = description
        self.action = action
        self._disabled = disabled
        super().__init__(classes=("-disabled" if disabled else "") + (" -wrapped" if wrapped else ""))
        if tooltip:
            self.tooltip = tooltip

    def render(self) -> RichText:
        parts = [(self.key_display, "bold #67e8f9")]
        if self.description:
            parts.append((" " + self.description, "#91a4c7"))
        return RichText.assemble(*parts)

    def on_mouse_down(self, event: events.MouseDown) -> None:
        event.stop()
        if self._disabled:
            self.app.bell()
        else:
            self.app.simulate_key(self.key)


class AdaptiveFooter(Footer):
    """Display every active shortcut, wrapping hints to fit the terminal."""

    DEFAULT_CSS = """
    AdaptiveFooter {
        layout: vertical;
        dock: bottom;
        width: 100%;
        height: auto;
        min-height: 1;
        overflow: hidden hidden;
        scrollbar-size: 0 0;
        background: $footer-background;
    }
    AdaptiveFooter .footer-row {
        width: 100%;
        height: auto;
        min-height: 1;
        layout: horizontal;
    }
    """

    def compose(self) -> ComposeResult:
        if not self._bindings_ready:
            return

        active_bindings = self.screen.active_bindings
        visible: list[tuple[Binding, bool, str]] = []
        actions: set[str] = set()
        for _node, binding, enabled, tooltip in active_bindings.values():
            if not binding.show or binding.action in actions:
                continue
            if binding.key == self.app.COMMAND_PALETTE_BINDING:
                continue
            actions.add(binding.action)
            visible.append((binding, enabled, tooltip))

        if self.show_command_palette and self.app.ENABLE_COMMAND_PALETTE:
            palette = active_bindings.get(self.app.COMMAND_PALETTE_BINDING)
            if palette:
                _node, binding, enabled, tooltip = palette
                if binding.action not in actions:
                    visible.append((binding, enabled, tooltip or binding.tooltip or binding.description))

        width = self.size.width or self.app.size.width
        width = max(1, width)
        entries: list[tuple[Binding, str, str, bool, str, int]] = []
        for binding, enabled, tooltip in visible:
            key_display = self.app.get_key_display(binding)
            description = binding.description
            rendered_width = cell_len(key_display) + (cell_len(description) + 1 if description else 0) + 3
            entries.append((binding, key_display, description, enabled, tooltip, rendered_width))

        rows: list[list[tuple[Binding, str, str, bool, str, int]]] = []
        current: list[tuple[Binding, str, str, bool, str, int]] = []
        current_width = 0
        for entry in entries:
            entry_width = entry[5]
            if current and current_width + entry_width > width:
                rows.append(current)
                current = []
                current_width = 0
            if entry_width > width:
                if current:
                    rows.append(current)
                    current = []
                    current_width = 0
                rows.append([entry])
            else:
                current.append(entry)
                current_width += entry_width
        if current:
            rows.append(current)

        for row in rows:
            with Horizontal(classes="footer-row"):
                for binding, key_display, description, enabled, tooltip, entry_width in row:
                    yield FooterHint(
                        binding.key,
                        key_display,
                        description,
                        binding.action,
                        disabled=not enabled,
                        tooltip=tooltip or binding.tooltip or binding.description,
                        wrapped=entry_width > width,
                    )

    def on_resize(self, event: events.Resize) -> None:
        self.refresh(recompose=True)


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
        *((str(index), f"select_track({index - 1})", definition.name)
          for index, definition in enumerate(TRACK_DEFINITIONS, 1)),
        ("left", "previous_track", "Sinistra"),
        ("right", "next_track", "Destra"),
        ("up", "previous_track", "Precedente"),
        ("down", "next_track", "Successivo"),
        ("escape", "quit", "Esci"),
    ]

    def __init__(self, return_to_previous: bool = False) -> None:
        super().__init__()
        self.return_to_previous = return_to_previous

    def compose(self) -> ComposeResult:
        active = getattr(self.app.catalog, "track", TRACK_DEFINITIONS[0].id)
        catalogs = {definition.id: Catalog(CONTENT_ROOT, track=definition.id) for definition in TRACK_DEFINITIONS}
        yield Header(show_clock=True)
        with Vertical(id="track-selection-page"):
            yield Static(
                "[bold #67e8f9]DEV//48[/]  [#38bdf8]—[/]  [bold #a78bfa]PERCORSI DI STUDIO[/]\n"
                "[#91a4c7]Scegli un percorso. Puoi riaprire questa schermata dalla Dashboard con Ctrl+T.[/]",
                id="track-hero",
            )
            with ScrollableContainer(id="track-card-list"):
                for index, definition in enumerate(TRACK_DEFINITIONS, 1):
                    catalog = catalogs[definition.id]
                    active_class = " active-card" if active == definition.id else ""
                    points = "\n".join(
                        f"[{definition.color}]◆[/] {point}" for point in definition.card_points
                    )
                    yield Vertical(
                        Static(
                            f"[bold {definition.color}]{definition.card_label}[/]  "
                            f"[bold #ffffff]{definition.card_heading}[/]\n"
                            f"[#cbd5e1]{definition.card_subtitle}[/]",
                            classes="card-header",
                        ),
                        Static(
                            f"{points}\n\n[#91a4c7]{len(catalog.lessons)} lezioni · "
                            f"{len(catalog.exercises)} esercizi · {len(catalog.labs)} laboratori · "
                            f"{len(catalog.flashcards)} flashcard[/]",
                            classes="card-desc",
                        ),
                        Button(f"▶ SCEGLI [Tasto {index}]", id=f"btn-track-{definition.id}"),
                        id=f"track-card-{definition.id}",
                        classes="track-card" + active_class,
                    )

            available_keys = ", ".join(str(index) for index in range(1, len(TRACK_DEFINITIONS) + 1))
            yield Static(
                f"[#91a4c7]Usa [bold #67e8f9]{available_keys}[/], le frecce e Invio, oppure seleziona una card.[/]",
                id="track-instruction",
            )
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        self._track_buttons = [self.query_one(f"#btn-track-{item.id}", Button) for item in TRACK_DEFINITIONS]
        active = getattr(self.app.catalog, "track", TRACK_DEFINITIONS[0].id)
        index = next((index for index, item in enumerate(TRACK_DEFINITIONS) if item.id == active), 0)
        self._track_button_index = index
        self.set_focus(self._track_buttons[index])

    def action_select_track(self, index: int) -> None:
        if 0 <= int(index) < len(TRACK_DEFINITIONS):
            self.choose_track(TRACK_DEFINITIONS[int(index)].id)

    def action_previous_track(self) -> None:
        self._track_button_index = (self._track_button_index - 1) % len(self._track_buttons)
        self.set_focus(self._track_buttons[self._track_button_index])

    def action_next_track(self) -> None:
        self._track_button_index = (self._track_button_index + 1) % len(self._track_buttons)
        self.set_focus(self._track_buttons[self._track_button_index])

    def action_quit(self) -> None:
        if self.return_to_previous:
            self.app.pop_screen()
        else:
            self.app.exit()

    def choose_track(self, track: str) -> None:
        self.app.store.set_active_track(track)
        self.app.catalog = Catalog(CONTENT_ROOT, track=track)
        self.app.sync_app_title()
        self.app.pop_screen()
        if not isinstance(self.app.screen, DashboardScreen):
            self.app.push_screen(DashboardScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        for definition in TRACK_DEFINITIONS:
            if event.button.id == f"btn-track-{definition.id}":
                self.choose_track(definition.id)
                return


class DashboardScreen(Screen):
    BINDINGS = [
        ("left", "previous_control", "Precedente"),
        ("right", "next_control", "Successivo"),
        ("up", "previous_control", "Precedente"),
        ("down", "next_control", "Successivo"),
        ("ctrl+t", "select_track", "Scegli percorso"),
    ]

    def compose(self) -> ComposeResult:
        stats = self.app.stats()
        track_title = self.app.catalog.track_definition.card_heading
        yield Header(show_clock=True)
        with Vertical(classes="page", id="dashboard-page"):
            with ScrollableContainer(id="dashboard-content"):
                yield Static(
                    f"[bold #67e8f9]DEV//48[/]  [#34d399]{track_title}[/]  [#91a4c7]· Ctrl+T per scegliere percorso[/]\n"
                    "Impara, sperimenta e costruisci. Riparti esattamente da dove eri rimasto.",
                    classes="hero",
                )
                with Horizontal(classes="stats-row"):
                    yield Static(f"[bold #67e8f9]{stats['percent']}%[/]\nPROGRESSO", id="dashboard-percent", classes="stat-card")
                    yield Static(f"[bold #a78bfa]{stats['xp']}[/]\nXP", id="dashboard-xp", classes="stat-card")
                    yield Static(f"[bold #34d399]{stats['completed_lessons']}[/]/{stats['total_lessons']}\nLEZIONI", id="dashboard-lessons", classes="stat-card")
                    yield Static(f"[bold #fbbf24]{stats['completed_exercises']}[/]/{stats['total_exercises']}\nESERCIZI", id="dashboard-exercises", classes="stat-card last")
                yield Label("PROGRESSO COMPLESSIVO", classes="muted")
                yield ProgressBar(total=100, show_eta=False, id="overall-progress")
                yield Static(self.app.learning_plan_markup(), id="learning-plan", classes="panel")
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
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        self.refresh_dashboard()
        self.set_focus(self.query_one("#continue", Button))

    def on_screen_resume(self, event: events.ScreenResume) -> None:
        self.refresh_dashboard()

    def refresh_dashboard(self) -> None:
        stats = self.app.stats()
        self.query_one("#dashboard-percent", Static).update(f"[bold #67e8f9]{stats['percent']}%[/]\nPROGRESSO")
        self.query_one("#dashboard-xp", Static).update(f"[bold #a78bfa]{stats['xp']}[/]\nXP")
        self.query_one("#dashboard-lessons", Static).update(
            f"[bold #34d399]{stats['completed_lessons']}[/]/{stats['total_lessons']}\nLEZIONI"
        )
        self.query_one("#dashboard-exercises", Static).update(
            f"[bold #fbbf24]{stats['completed_exercises']}[/]/{stats['total_exercises']}\nESERCIZI"
        )
        self.query_one("#overall-progress", ProgressBar).update(progress=stats["percent"])
        self.query_one("#learning-plan", Static).update(self.app.learning_plan_markup())

        last_label = self.app.last_item_title()
        next_label = self.app.next_step_title()
        last_text = f"[bold #67e8f9]PROSSIMO PASSO[/]  {next_label}\n"
        last_text += (
            f"[bold #34d399]ULTIMA SCHERMATA[/]  {last_label}"
            if last_label
            else "[#91a4c7]ULTIMA SCHERMATA  Nessuna: il percorso è pronto per iniziare.[/]"
        )
        self.query_one("#last-item", Static).update(last_text)

        continue_button = self.query_one("#continue", Button)
        continue_button.label = "▶ PROSSIMO PASSO" if last_label else "▶ INIZIA"
        resume_button = self.query_one("#resume", Button)
        resume_button.label = "↩ ULTIMA SCHERMATA" if last_label else "↩ NESSUNA SCHERMATA"
        resume_button.disabled = not bool(last_label)

    def action_previous_control(self) -> None:
        self.focus_previous()

    def action_next_control(self) -> None:
        self.focus_next()

    def action_select_track(self) -> None:
        self.app.open_track_selection()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        actions = {
            "resume": self.app.resume_last,
            "continue": self.app.continue_course,
            "curriculum": lambda: self.app.push_screen(CurriculumScreen()),
            "labs": lambda: self.app.push_screen(LabsScreen()),
            "flashcards": lambda: self.app.push_screen(FlashcardsScreen()),
            "challenges": lambda: self.app.push_screen(ChallengesScreen()),
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
        yield AdaptiveFooter()

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
            title = f"[G{lesson.recommended_day}] {lesson.title}" if lesson.recommended_day else lesson.title
            table.add_row(state, modules[lesson.module], title, str(lesson.minutes), lesson.difficulty, key=lesson.id)

    def on_input_changed(self, event: Input.Changed) -> None:
        self.refresh_rows(event.value)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.app.push_screen(LessonScreen(str(event.row_key.value)))

    def action_back(self) -> None:
        self.app.pop_screen()


class ReviewScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(
                "[bold #67e8f9]REVISIONE DEGLI ERRORI[/]\n"
                "Riapri i tentativi ancora irrisolti; separa gli esercizi passati dopo avere letto la soluzione.",
                classes="hero",
            )
            yield DataTable(cursor_type="row", zebra_stripes=True, id="table")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        table = self.query_one("#table", DataTable)
        table.add_columns("Stato", "Esercizio", "Tentativi", "ID")
        exercise_ids = {
            exercise_progress_id(item, self.app.coding_language)
            for item in self.app.catalog.exercises
        }
        for item in self.app.store.review_items(exercise_ids):
            exercise_id, language = split_exercise_progress_id(item["item_id"])
            exercise = self.app.catalog.exercise_by_id.get(exercise_id)
            if not exercise:
                continue
            label = "DA RIPROVARE" if item["kind"] == "failed" else "DOPO SOLUZIONE"
            title = exercise.title + (f" · {language.upper()}" if language else "")
            table.add_row(label, title, str(item["attempts"]), exercise_id, key=item["item_id"])
        self.set_focus(table)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        exercise_id, language = split_exercise_progress_id(str(event.row_key.value))
        if language in {"python", "cpp"}:
            self.app.coding_language = language
        self.app.push_screen(ExerciseScreen(exercise_id))

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
        pending_exercises = [
            item for item in self.app.catalog.exercises_for(lesson.id)
            if exercise_progress_id(item, self.app.coding_language) not in completed
        ]
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
        yield AdaptiveFooter()

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
        target = next((item for item in exercises if exercise_progress_id(item, self.app.coding_language) not in completed), None)
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
        ("l", "toggle_language", "Lingua"),
        ("ctrl+right", "next_exercise", "Successivo"),
    ]
    tracked_type = "exercise"

    def __init__(self, exercise_id: str) -> None:
        super().__init__()
        self.exercise_id = exercise_id
        self.tracked_id = exercise_id
        self.theory_open = False
        self.coding_language = self.app.coding_language
        self.remaining = 0
        self.timer_running = False

    @property
    def exercise(self) -> Exercise:
        return self.app.catalog.exercise_by_id[self.exercise_id]

    @property
    def variant(self) -> dict:
        return self.exercise.variants.get(self.coding_language, {})

    @property
    def progress_id(self) -> str:
        return exercise_progress_id(self.exercise, self.coding_language)

    @property
    def active_kind(self) -> str:
        return str(self.variant.get("kind", self.exercise.kind))

    def content_for_language(self, field: str, fallback: str = "") -> str:
        return str(self.variant.get(field, getattr(self.exercise, field, fallback)))

    def compose(self) -> ComposeResult:
        ex = self.app.catalog.exercise_by_id[self.exercise_id]
        state = self.app.store.get(self.progress_id)
        initial = state.get("answer") or self.content_for_language("starter")
        language = {"javascript":"javascript","react":"javascript","typescript":"typescript","csharp":"csharp","angular":"typescript","html":"html","css":"css","sql":"sql","python":"python","cpp":"cpp"}.get(self.active_kind)
        reward = "autovalutazione · nessun XP" if ex.kind == "reflection" else f"{ex.xp} XP"
        scope_note = {
            "csharp": "Il runner compila il codice ed esegue i casi dichiarati nell'esercizio; non garantisce ogni possibile comportamento.",
            "angular": "Il runner prova la logica TypeScript con piccoli mock: non avvia Angular, non compila i template, non esegue tsc e non controlla il DOM. Usa i laboratori per provare un progetto Angular reale.",
            "typescript": "Il controllo verifica la sintassi eseguibile e i requisiti indicati; non sostituisce `tsc` né un progetto Angular completo.",
            "html": "Il controllo verifica struttura e requisiti testuali; non esegue il rendering in un browser.",
            "css": "Il controllo verifica requisiti testuali; non esegue il rendering o la resa responsive in un browser.",
            "reflection": "Questa autoverifica cerca i termini richiesti; non valuta il significato. Confronta la spiegazione con il modello.",
            "python": "Python gira in un processo separato con test, timeout e output limitato. Il processo non è isolato dal sistema operativo e può accedere a file o rete.",
            "cpp": "Il sorgente C++20 viene compilato e provato contro più asserzioni, con timeout e output limitato. Il processo non è isolato dal sistema operativo e può accedere a file o rete.",
        }.get(self.active_kind, "Il runner mostra i controlli automatici previsti per questo esercizio.")
        tags = []
        if ex.no_ai:
            tags.append("NO AI")
        if ex.no_internet:
            tags.append("NO INTERNET")
        if ex.timed:
            tags.append("TIMED")
        tag_text = (" · " + " · ".join(tags)) if tags else ""
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]{ex.title}[/]\n[#91a4c7]{self.active_kind.upper()} · {ex.minutes} min · {reward} · tentativi: {state.get('attempts', 0)}{tag_text}[/]", classes="hero")
            if ex.timed:
                yield Static("", id="exercise-timer", classes="stat-card")
            with Horizontal(id="exercise-layout"):
                with Vertical(id="exercise-left"):
                    with ScrollableContainer(id="exercise-prompt", can_focus=True):
                        yield Collapsible(
                            Static(f"[bold #a78bfa]Come funziona il controllo:[/] {scope_note}", id="exercise-scope"),
                            title="Controlli automatici",
                            collapsed=True,
                            id="exercise-scope-details",
                        )
                        yield Markdown(assessment_prompt(ex) if ex.timed else ex.prompt)
                        if ex.creative_goals:
                            goals_txt = "\n".join(f"- ★ {g}" for g in ex.creative_goals)
                            yield Static(f"\n[bold #34d399]Estensioni facoltative · non valutate automaticamente[/]\n{goals_txt}", classes="panel")
                    with ScrollableContainer(id="theory-scroll", can_focus=True):
                        yield Static("[bold #a78bfa]TEORIA DELLA LEZIONE[/]\nF1 apre o richiude la teoria senza perdere risposta, cursore o punto di lettura. ESC torna prima all'esercizio; da lì puoi rientrare nella lezione al punto in cui l'avevi lasciata.", classes="panel")
                        yield Markdown(self.app.catalog.lesson_body(self.app.catalog.lesson_by_id[ex.lesson_id]), id="theory-markdown")
                with Vertical(id="exercise-right"):
                    if self.active_kind in CODE_EDITOR_KINDS:
                        yield CodeTextArea(
                            initial,
                            language=language,
                            show_line_numbers=True,
                            id="editor",
                            brace_indentation=self.active_kind in BRACE_INDENT_LANGUAGES,
                            brace_language=self.active_kind,
                        )
                    else:
                        yield TextArea(initial, language=language, show_line_numbers=True, id="editor")
                    with ScrollableContainer(id="result-scroll", can_focus=True):
                        yield Static("", id="result")
            with Horizontal(id="exercise-actions", classes="actions"):
                yield Button("▶ ESEGUI [F5]", id="run", classes="primary")
                if ex.variants:
                    yield Button(f"⌘ LINGUA: {self.coding_language.upper()} [L]", id="language")
                if ex.timed:
                    yield Button("⏱ AVVIO", id="exercise-timer-button", disabled=True)
                yield Button("◇ INDIZIO [H]", id="hint")
                yield Button("⌁ SOLUZIONE", id="solution", classes="warning")
                yield Button("→ PROSSIMO", id="next")
                yield Button("📖 TEORIA [F1]", id="theory")
                yield Button("← LEZIONE", id="back")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        self.tracked_id = self.progress_id
        super().on_mount()
        self.query_one("#theory-scroll", ScrollableContainer).display = False
        self.query_one("#result-scroll", ScrollableContainer).display = False
        self.set_focus(self.query_one("#editor", TextArea))
        if self.exercise.timed:
            self.remaining = self.exercise.minutes * 60
            self.timer_running = True
            self.set_interval(1, self.tick_timer)
            self.render_timer()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id != "editor":
            return
        self.mark_exercise_started(event.text_area.text)

    def mark_exercise_started(self, answer: str | None = None, *, attempted: bool = False) -> None:
        if attempted or (answer is not None and answer != self.content_for_language("starter")):
            key = exercise_started_setting_key(self.progress_id)
            if self.app.store.get_setting(key) != "1":
                self.app.store.set_setting(key, "1")

    def tick_timer(self) -> None:
        if not self.timer_running or self.remaining <= 0:
            return
        self.remaining -= 1
        self.render_timer()
        if self.remaining == 0:
            self.timer_running = False
            self.app.notify("Tempo di pratica terminato. Puoi ancora rivedere il tuo tentativo.", severity="warning")

    def render_timer(self) -> None:
        if not self.exercise.timed:
            return
        minutes, seconds = divmod(self.remaining, 60)
        state = "IN CORSO" if self.timer_running else "TERMINATO"
        self.query_one("#exercise-timer", Static).update(f"[bold #67e8f9]{minutes:02d}:{seconds:02d}[/] · {state}")
        button = self.query_one("#exercise-timer-button", Button)
        button.label = f"⏱ {minutes:02d}:{seconds:02d}"

    def action_toggle_language(self) -> None:
        if not self.exercise.variants:
            return
        available = list(self.exercise.variants)
        try:
            index = available.index(self.coding_language)
        except ValueError:
            index = 0
        answer = self.editor_value()
        self.mark_exercise_started(answer)
        self.app.store.save_answer(self.progress_id, "exercise", answer)
        self.coding_language = available[(index + 1) % len(available)]
        self.app.coding_language = self.coding_language
        self.app.store.set_setting("amazon_coding_language", self.coding_language)
        editor = self.query_one("#editor", TextArea)
        state = self.app.store.get(self.progress_id)
        editor.text = state.get("answer") or self.content_for_language("starter")
        editor.language = {"python": "python", "cpp": "cpp"}.get(self.active_kind)
        self.query_one("#language", Button).label = f"⌘ LINGUA: {self.coding_language.upper()} [L]"
        self.app.notify(f"Prossimi esercizi in {self.coding_language.upper()}")

    def editor_value(self) -> str:
        return self.query_one("#editor", TextArea).text

    def update_result(self, content: str) -> None:
        result_scroll = self.query_one("#result-scroll", ScrollableContainer)
        self.query_one("#result", Static).update(content)
        result_scroll.display = True
        result_scroll.scroll_home(animate=False, force=True)

    def action_save(self) -> None:
        answer = self.editor_value()
        self.mark_exercise_started(answer)
        self.app.store.save_answer(self.progress_id, "exercise", answer)
        self.app.notify("Risposta salvata")

    def action_toggle_theory(self) -> None:
        answer = self.editor_value()
        self.mark_exercise_started(answer)
        self.app.store.save_answer(self.progress_id, "exercise", answer)
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
        self.mark_exercise_started(answer, attempted=True)
        result = run_exercise(self.exercise, answer, PROJECT_ROOT, language=self.coding_language)
        earned_xp = 0 if self.exercise.kind == "reflection" else int(self.exercise.xp * result.score / 100)
        attempts = self.app.store.record_attempt(self.progress_id, "exercise", answer, result.passed, earned_xp)
        icon = "✓" if result.passed else "✗"
        color = "#34d399" if result.passed else "#fb7185"
        details = "\n".join(result.details)
        if self.exercise.kind == "reflection":
            matches = sum(item.startswith("✓") for item in result.details)
            label = f"AUTOVERIFICA · {matches}/{len(result.details)} termini presenti"
            self.update_result(f"[bold #fbbf24]{label}[/]\nLa checklist non valuta il significato. Confronta la spiegazione con il modello.\n\n{details}")
        else:
            self.update_result(f"[bold {color}]{icon} {result.score}%[/]\n{result.output}\n\n{details}")
        if result.passed and self.exercise.kind == "reflection":
            self.app.notify("Autoverifica completata · confronta la risposta con il modello.", title="Richiamo")
        elif result.passed:
            self.app.notify(f"Esercizio superato · +{self.exercise.xp} XP", title="Ottimo")
        elif attempts >= 2:
            self.app.notify("La soluzione completa è ora sbloccata.", severity="warning")

    def action_hint(self) -> None:
        state = self.app.store.get(self.progress_id)
        level = min(int(state.get("hint_level", 0)) + 1, len(self.exercise.hints))
        self.app.store.set_hint(self.progress_id, level)
        hints = "\n".join(f"{i}. {hint}" for i, hint in enumerate(self.exercise.hints[:level], 1))
        self.update_result(f"[bold #fbbf24]INDIZI {level}/{len(self.exercise.hints)}[/]\n{hints}")

    def show_solution(self) -> None:
        state = self.app.store.get(self.progress_id)
        if int(state.get("attempts", 0)) < self.exercise.solution_after_attempts:
            remaining = self.exercise.solution_after_attempts - int(state.get("attempts", 0))
            self.update_result(f"[bold #fbbf24]SOLUZIONE BLOCCATA[/]\nServono ancora {remaining} tentativi reali. Usa H per un indizio.")
            return
        self.app.store.mark_solution_viewed(self.progress_id)
        solution = self.content_for_language("solution")
        text = f"SOLUZIONE COMMENTATA · {self.coding_language.upper()}\n\n{solution}\n\n{self.exercise.explanation}"
        self.update_result(text)

    def action_next_exercise(self) -> None:
        self.next_exercise()

    def next_exercise(self) -> None:
        if self.app.store.get(self.progress_id).get("status") != "completed":
            self.app.notify("Supera questo esercizio prima di passare al prossimo passo.", severity="warning")
            return
        exercises = self.app.catalog.exercises_for(self.exercise.lesson_id)
        completed = self.app.store.completed_ids()
        target = next((item for item in exercises if exercise_progress_id(item, self.coding_language) not in completed), None)
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
        actions = {"run":self.run_current,"hint":self.action_hint,"solution":self.show_solution,"next":self.next_exercise,"theory":self.action_toggle_theory,"back":self.action_back,"language":self.action_toggle_language}
        if event.button.id in actions:
            actions[event.button.id]()


class LabsScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static("[bold #67e8f9]LABORATORI[/]\nProgetti più lunghi, workspace persistente e test reali.", classes="hero")
            yield DataTable(cursor_type="row", zebra_stripes=True, id="table")
        yield AdaptiveFooter()

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
        return self.app.catalog.lab_by_id[self.lab_id].for_repository_language(
            self.app.store.get_setting("amazon_repository_language", "node"))

    def compose(self) -> ComposeResult:
        lab = self.lab
        requirements = "\n".join(f"- [ ] {x}" for x in lab.requirements)
        rubric = "\n".join(f"- {x}" for x in lab.rubric)
        creative = ""
        if lab.creative_goals:
            goals = "\n".join(f"- ★ {x}" for x in lab.creative_goals)
            creative = f"\n\n## Estensioni facoltative (autovalutazione)\n{goals}"
        verification = {
            "amazon_node": "L'app esegue la suite Node.js (`npm test`) presente nel workspace.",
            "amazon_cpp": "L'app compila ed esegue la suite C++20 con GCC o Clang.",
        }.get(
            lab.workspace_template,
            "L'app esegue la suite xUnit e/o Angular presente nel workspace.",
        )
        dependency_action = "↓ VERIFICA C++20" if lab.workspace_template == "amazon_cpp" else "↓ INSTALLA DIPENDENZE"
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]{lab.title}[/]\n[#91a4c7]{lab.minutes} min · {lab.difficulty}[/]", classes="hero")
            with ScrollableContainer(id="lab-scroll", can_focus=True):
                yield Markdown(f"## Brief\n\n{lab.description}\n\n## Requisiti\n\n{requirements}\n\n## Rubrica\n\n{rubric}{creative}\n\n> **Verifica automatica:** {verification} Un esito verde conferma quei test; rileggi la rubrica per i criteri non coperti. Il workspace non viene sovrascritto quando riapri l'app.")
                yield Static("Pronto.", id="lab-result", classes="panel")
            with Horizontal(classes="actions"):
                yield Button("▣ APRI VS CODE", id="open", classes="primary")
                yield Button(dependency_action, id="install")
                yield Button("▶ ESEGUI TEST", id="test", classes="success")
                if lab.repository_variants:
                    yield Button(f"STACK: {self.app.store.get_setting('amazon_repository_language', 'node').upper()}", id="repository-language")
                elif lab.workspace_template in {"amazon_cpp", "amazon_node"}:
                    yield Button("USA QUESTO STACK", id="choose-stack")
                yield Button("← LAB", id="back")
        yield AdaptiveFooter()

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
        if event.button.id == "repository-language":
            language = "cpp" if self.app.store.get_setting("amazon_repository_language", "node") == "node" else "node"
            self.app.store.set_setting("amazon_repository_language", language)
            self.app.pop_screen()
            self.app.push_screen(LabScreen(self.lab_id))
        elif event.button.id == "choose-stack":
            language = "cpp" if self.lab.workspace_template == "amazon_cpp" else "node"
            self.app.store.set_setting("amazon_repository_language", language)
            result.update(f"Stack repository scelto: {language.upper()}. Il piano e i mock useranno questa scelta.")
        elif event.button.id == "open":
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
        yield AdaptiveFooter()

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
        yield AdaptiveFooter()

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
            yield Static(
                "[bold #67e8f9]SIMULAZIONI E COMPORTAMENTO[/]\n"
                "DSA e repository a tempo, scenari Work Simulation e familiarizzazione Work Style.",
                classes="hero",
            )
            yield DataTable(cursor_type="row", zebra_stripes=True, id="table")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        table = self.query_one("#table", DataTable)
        table.add_columns("Tipo", "Attività", "Minuti", "Descrizione")
        for sim in self.app.catalog.simulations:
            table.add_row("Full Mock" if sim.kind == "full_mock" else "Simulazione", sim.title, str(sim.minutes), sim.brief, key=sim.id)
        table.add_row("Review", "Errori e soluzioni consultate", "—", "Riprendi gli esercizi da rivedere.", key="review")
        for scenario in self.app.catalog.work_scenarios:
            table.add_row("Work Simulation", scenario.title, "—", scenario.brief, key=scenario.id)
        if self.app.catalog.work_style:
            table.add_row("Work Style", "Familiarizzazione e autovalutazione", "15", "Leggi con calma, rispondi in modo coerente e personale.", key="work-style")
        self.set_focus(table)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        item_id = str(event.row_key.value)
        simulation = next((item for item in self.app.catalog.simulations if item.id == item_id), None)
        if simulation:
            if simulation.kind == "full_mock":
                self.app.push_screen(FullMockScreen(simulation))
            elif simulation.kind == "coding":
                self.app.push_screen(CodingSimulationScreen(simulation))
            else:
                self.app.push_screen(SimulationScreen(simulation))
            return
        scenario = next((item for item in self.app.catalog.work_scenarios if item.id == item_id), None)
        if scenario:
            self.app.push_screen(WorkScenarioScreen(scenario))
        elif item_id == "work-style":
            self.app.push_screen(WorkStyleScreen())
        elif item_id == "review":
            self.app.push_screen(ReviewScreen())

    def action_back(self) -> None:
        self.app.pop_screen()


class WorkScenarioScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro"), ("ctrl+s", "submit", "Valuta la classifica")]

    def __init__(self, scenario: WorkScenario) -> None:
        super().__init__()
        self.scenario = scenario

    def compose(self) -> ComposeResult:
        options = "\n\n".join(f"**{item['id']}.** {item['text']}" for item in self.scenario.options)
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #67e8f9]{self.scenario.title}[/]\n[#91a4c7]Work Simulation · ragionamento prima della risposta[/]", classes="hero")
            with ScrollableContainer(id="scenario-scroll", can_focus=True):
                yield Markdown(f"## Situazione\n\n{self.scenario.brief}\n\n## Possibili risposte\n\n{options}")
                yield Static("Ordina tutte le opzioni dalla più efficace alla meno efficace. È un confronto ragionato, non un punteggio ufficiale.", classes="panel")
                yield TextArea("", id="scenario-answer", show_line_numbers=False)
                yield Markdown("", id="scenario-feedback", classes="panel")
            with Horizontal(classes="actions"):
                yield Button("▣ CONFRONTA RAGIONAMENTO [CTRL+S]", id="submit", classes="primary")
                yield Button("← SCENARI", id="back")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        state = self.app.store.get(self.scenario.id)
        answer = state.get("answer", "")
        revision = self.app.store.get_setting(f"scenario_revision:{self.scenario.id}", "")
        if answer and revision != self.answer_revision():
            self.query_one("#scenario-feedback", Markdown).update(
                "Le alternative sono cambiate dall'ultimo tentativo. La risposta precedente resta nel progresso; "
                "formula una nuova classifica per queste opzioni."
            )
        else:
            self.query_one("#scenario-answer", TextArea).text = answer
        self.set_focus(self.query_one("#scenario-answer", TextArea))

    def answer_revision(self) -> str:
        content = [self.scenario.brief, [(item["id"], item["text"]) for item in self.scenario.options]]
        return hashlib.sha256(json.dumps(content, ensure_ascii=False).encode("utf-8")).hexdigest()

    def feedback_text(self, answer: str) -> str:
        order = " > ".join(self.scenario.recommended_order)
        notes = "\n\n".join(
            f"**{item['id']} · {item['effectiveness']}**\n{item['reasoning']}"
            for item in sorted(self.scenario.options, key=lambda option: self.scenario.recommended_order.index(option["id"]))
        )
        principles = ", ".join(self.scenario.principles)
        learning_focus = (
            f"\n\nFilo conduttore: {self.scenario.learning_focus}."
            if self.scenario.learning_focus else ""
        )
        return (
            f"La tua classifica: {answer}\nLettura di confronto: {order}\n\n{notes}\n\nPrincipi in gioco: {principles}. "
            "La scelta dipende dal contesto: confronta impatto, reversibilità, evidenza e comunicazione prima di decidere."
            f"{learning_focus}"
        )

    def action_submit(self) -> None:
        answer = self.query_one("#scenario-answer", TextArea).text.strip().upper().replace(",", ">")
        ranked = [part.strip() for part in answer.split(">") if part.strip()]
        expected_ids = {item["id"] for item in self.scenario.options}
        if len(ranked) != len(expected_ids) or set(ranked) != expected_ids:
            self.query_one("#scenario-feedback", Static).update(
                f"Scrivi ogni lettera una sola volta, per esempio: {' > '.join(item['id'] for item in self.scenario.options)}"
            )
            return
        self.app.store.set_setting(f"scenario_revision:{self.scenario.id}", self.answer_revision())
        self.app.store.record_attempt(self.scenario.id, "work-scenario", answer, True, 0)
        self.query_one("#scenario-feedback", Markdown).update(self.feedback_text(answer))

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self.action_submit()
        elif event.button.id == "back":
            self.action_back()


class WorkStyleScreen(Screen):
    BINDINGS = [("escape", "back", "Indietro"), ("ctrl+s", "save", "Salva"), ("left", "previous", "Precedente"), ("right", "next", "Successivo")]

    def __init__(self) -> None:
        super().__init__()
        self.index = 0

    @property
    def prompt(self) -> WorkStylePrompt:
        return self.app.catalog.work_style[self.index]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static("[bold #67e8f9]WORK STYLE · FAMILIARIZZAZIONE[/]\nNessun punteggio e nessuna risposta da imitare: usa esempi veri e mantieni coerenza.", classes="hero")
            with ScrollableContainer(id="work-style-scroll", can_focus=True):
                yield Static("", id="work-style-title", classes="panel")
                yield Markdown("", id="work-style-prompt")
                yield TextArea("", id="work-style-answer", show_line_numbers=False)
                yield Static("Non è un test di personalità: non cercare di ottimizzare una risposta modello. Salva soltanto le note che ti aiutano a riflettere.", classes="panel")
            with Horizontal(classes="actions"):
                yield Button("← PRECEDENTE", id="previous")
                yield Button("SALVA [CTRL+S]", id="save", classes="primary")
                yield Button("SUCCESSIVO →", id="next")
                yield Button("← SFIDE", id="back")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        self.render_prompt()
        self.set_focus(self.query_one("#work-style-answer", TextArea))

    def render_prompt(self) -> None:
        state = self.app.store.get(self.prompt.id)
        self.query_one("#work-style-title", Static).update(f"{self.index + 1}/{len(self.app.catalog.work_style)} · {self.prompt.title}")
        self.query_one("#work-style-prompt", Markdown).update(self.prompt.prompt + "\n\n" + "\n".join(f"- {item}" for item in self.prompt.reflection_prompts))
        self.query_one("#work-style-answer", TextArea).text = state.get("answer", "")

    def action_save(self) -> None:
        answer = self.query_one("#work-style-answer", TextArea).text
        self.app.store.save_answer(self.prompt.id, "work-style", answer)
        self.app.notify("Nota salvata senza punteggio.")

    def action_previous(self) -> None:
        self.action_save()
        self.index = (self.index - 1) % len(self.app.catalog.work_style)
        self.render_prompt()

    def action_next(self) -> None:
        self.action_save()
        self.index = (self.index + 1) % len(self.app.catalog.work_style)
        self.render_prompt()

    def action_back(self) -> None:
        self.action_save()
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        {"previous": self.action_previous, "save": self.action_save, "next": self.action_next, "back": self.action_back}.get(event.button.id, lambda: None)()


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
                yield Markdown(f"## Brief\n\n{self.simulation.brief}\n\n## Checklist\n\n{checklist}\n\n## Regola\n\nSegui le condizioni indicate nella traccia e nel tuo invito reale. Per questa simulazione, usa il timer come tempo indipendente e non trasferire i minuti inutilizzati.")
            with Horizontal(classes="actions"):
                yield Button("▶ AVVIA / PAUSA [SPAZIO]", id="toggle", classes="primary")
                yield Button("↺ RESET", id="reset")
                if self.simulation.repository_lab_id:
                    yield Button("▣ APRI REPOSITORY", id="open-repo")
                    yield Button("▶ ESEGUI TEST", id="run-repo")
                    yield Button(f"STACK: {self.app.store.get_setting('amazon_repository_language', 'node').upper()}", id="repository-language")
                yield Button("← SIMULAZIONI", id="back")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        super().on_mount()
        self.set_interval(1, self.tick)
        self.render_timer()
        self.set_focus(self.query_one("#lab-scroll", ScrollableContainer))

    def action_next_control(self) -> None:
        buttons = [
            self.query_one("#toggle", Button),
            self.query_one("#reset", Button),
        ]
        if self.simulation.repository_lab_id:
            buttons.extend([self.query_one("#open-repo", Button), self.query_one("#run-repo", Button)])
        buttons.append(self.query_one("#back", Button))
        try:
            idx = buttons.index(self.focused)
            self.set_focus(buttons[(idx + 1) % len(buttons)])
        except (ValueError, TypeError):
            self.set_focus(buttons[0])

    def action_previous_control(self) -> None:
        buttons = [
            self.query_one("#toggle", Button),
            self.query_one("#reset", Button),
        ]
        if self.simulation.repository_lab_id:
            buttons.extend([self.query_one("#open-repo", Button), self.query_one("#run-repo", Button)])
        buttons.append(self.query_one("#back", Button))
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

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "toggle":
            self.action_toggle()
        elif event.button.id == "repository-language" and not self.running:
            language = "cpp" if self.app.store.get_setting("amazon_repository_language", "node") == "node" else "node"
            self.app.store.set_setting("amazon_repository_language", language)
            self.query_one("#repository-language", Button).label = f"STACK: {language.upper()}"
        elif event.button.id == "reset":
            self.remaining = self.simulation.minutes * 60
            self.running = False
            self.render_timer()
        elif event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id in {"open-repo", "run-repo"}:
            lab = self.app.catalog.lab_by_id[self.simulation.repository_lab_id].for_repository_language(
                self.app.store.get_setting("amazon_repository_language", "node"))
            workspace = ensure_lab_workspace(self.app.workspace_root, lab)
            if event.button.id == "open-repo":
                _ok, message = open_vscode(workspace)
                self.app.notify(message)
            else:
                result = await asyncio.to_thread(run_lab_tests, workspace)
                self.app.notify(result.output, title="Test repository")


def assessment_prompt(exercise: Exercise) -> str:
    """Keep the task contract, withholding the teaching-only pattern label."""
    return re.sub(r"^\*\*Pattern:\*\*[^\n]*\n\n", "", exercise.prompt, count=1)


class CodingSimulationScreen(TimedScreen):
    """Timed single-file coding practice without hint or solution reveal."""
    BINDINGS = [("escape", "back", "Indietro"), ("space", "toggle", "Avvia"), ("f5", "run", "Esegui test"), ("l", "toggle_language", "Lingua prima dell'avvio")]
    tracked_type = "simulation"

    def __init__(self, simulation: Simulation) -> None:
        super().__init__()
        self.simulation = simulation
        self.tracked_id = simulation.id
        self.exercise_id = simulation.coding_exercise_id
        self.remaining = simulation.minutes * 60
        self.running = False
        self.started = False

    @property
    def exercise(self) -> Exercise:
        return self.app.catalog.exercise_by_id[self.exercise_id]

    @property
    def language(self) -> str:
        return self.app.coding_language if self.app.coding_language in self.exercise.variants else next(iter(self.exercise.variants), "python")

    def variant(self, language: str | None = None) -> dict:
        return self.exercise.variants.get(language or self.language, {})

    def progress_id(self, language: str | None = None) -> str:
        return exercise_progress_id(self.exercise, language or self.language)

    def compose(self) -> ComposeResult:
        variant = self.variant()
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #fbbf24]{self.simulation.title}[/] · NO AI · NO INTERNET\n{self.exercise.title}", classes="hero")
            yield Static("", id="coding-sim-timer", classes="stat-card")
            with ScrollableContainer(id="coding-sim-prompt", can_focus=True):
                yield Markdown(assessment_prompt(self.exercise))
                yield Static("Durante il timer non ci sono hint o soluzione. Usa il runner soltanto per controllare il codice.", classes="panel")
            yield CodeTextArea(
                variant.get("starter", self.exercise.starter),
                language=self.language,
                show_line_numbers=True,
                id="coding-sim-editor",
                brace_indentation=self.language in BRACE_INDENT_LANGUAGES,
                brace_language=self.language,
            )
            with ScrollableContainer(id="coding-sim-result", can_focus=True):
                yield Static("", id="coding-sim-output", classes="panel")
            with Horizontal(classes="actions"):
                yield Button("▶ AVVIA [SPAZIO]", id="toggle", classes="primary")
                yield Button(f"▶ ESEGUI [{self.language.upper()}] [F5]", id="run", disabled=True)
                yield Button(f"⌘ LINGUA: {self.language.upper()} [L]", id="language")
                yield Button("↺ RESET TIMER", id="reset")
                yield Button("← SIMULAZIONI", id="back")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#coding-sim-result", ScrollableContainer).display = False
        self.query_one("#coding-sim-prompt", ScrollableContainer).display = False
        self.query_one("#coding-sim-editor", TextArea).display = False
        self.set_interval(1, self.tick)
        self.render_timer()
        self.set_focus(self.query_one("#toggle", Button))

    def render_timer(self) -> None:
        minutes, seconds = divmod(self.remaining, 60)
        state = "IN CORSO" if self.running else "IN PAUSA"
        self.query_one("#coding-sim-timer", Static).update(f"[bold #67e8f9]{minutes:02d}:{seconds:02d}[/] · {state}")

    def tick(self) -> None:
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.render_timer()
            if self.remaining == 0:
                self.running = False
                self.query_one("#coding-sim-editor", TextArea).read_only = True
                self.query_one("#run", Button).disabled = True
                self.app.notify("Tempo terminato. Puoi rivedere il tentativo e i test.", severity="warning")

    def action_toggle(self) -> None:
        if not self.started:
            self.started = True
            self.running = True
            self.query_one("#coding-sim-prompt", ScrollableContainer).display = True
            self.query_one("#coding-sim-editor", TextArea).display = True
            self.query_one("#run", Button).disabled = False
            for button_id in ("toggle", "language", "reset"):
                self.query_one(f"#{button_id}", Button).disabled = True
            self.render_timer()

    async def action_run(self) -> None:
        if not self.running:
            return
        answer = self.query_one("#coding-sim-editor", TextArea).text
        self.app.store.save_answer(self.progress_id(), "exercise", answer)
        result = await asyncio.to_thread(run_exercise, self.exercise, answer, PROJECT_ROOT, self.language)
        self.app.store.record_attempt(self.progress_id(), "exercise", answer, result.passed, result.score)
        self.query_one("#coding-sim-output", Static).update(f"{result.score}%\n{result.output}\n" + "\n".join(result.details))
        self.query_one("#coding-sim-result", ScrollableContainer).display = True

    def action_toggle_language(self) -> None:
        if self.started:
            return
        available = list(self.exercise.variants)
        if len(available) < 2:
            return
        editor = self.query_one("#coding-sim-editor", TextArea)
        next_language = available[(available.index(self.language) + 1) % len(available)]
        self.app.coding_language = next_language
        self.app.store.set_setting("amazon_coding_language", next_language)
        variant = self.variant(next_language)
        editor.text = variant.get("starter", self.exercise.starter)
        editor.language = next_language
        self.query_one("#language", Button).label = f"⌘ LINGUA: {next_language.upper()} [L]"
        self.query_one("#run", Button).label = f"▶ ESEGUI [{next_language.upper()}] [F5]"

    def action_reset(self) -> None:
        if self.started:
            return
        self.running = False
        self.remaining = self.simulation.minutes * 60
        self.render_timer()

    def action_back(self) -> None:
        self.app.pop_screen()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "toggle":
            self.action_toggle()
        elif event.button.id == "run":
            await self.action_run()
        elif event.button.id == "language":
            self.action_toggle_language()
        elif event.button.id == "reset":
            self.action_reset()
        elif event.button.id == "back":
            self.action_back()


class FullMockScreen(TimedScreen):
    """Sequential 40 + 60 minute practice; the coding clock never rolls over."""
    BINDINGS = [("escape", "attempt_back", "Bloccato durante il mock"), ("f5", "run_coding", "Esegui test")]
    tracked_type = "simulation"

    def __init__(self, simulation: Simulation) -> None:
        super().__init__()
        self.simulation = simulation
        self.tracked_id = simulation.id
        self.phase = 0
        self.remaining = 40 * 60
        self.running = False
        self.started = False
        self.coding_language = self.app.coding_language
        self.workspace_path: Path | None = None

    @property
    def exercise(self) -> Exercise:
        return self.app.catalog.exercise_by_id[self.simulation.coding_exercise_id]

    @property
    def lab(self) -> Lab:
        lab = self.app.catalog.lab_by_id[self.simulation.repository_lab_id]
        return lab.for_repository_language(self.app.store.get_setting("amazon_repository_language", "node"))

    def repository_prompt_text(self) -> str:
        return (
            "## Repository · 60 minuti\n\n"
            "Apri il progetto e parti dal README. Avvia la suite di test, osserva le failure e segui il dato "
            "attraverso i file pertinenti. Formula un'ipotesi verificabile alla volta, applica una modifica "
            "circoscritta e riesegui la suite completa. Usa i contratti esistenti come riferimento; annota "
            "eventuali incertezze invece di allargare il cambiamento.\n\n"
            "Il timer parte da 60:00 anche se hai consegnato prima la sezione coding."
        )

    def variant_value(self, key: str) -> str:
        variant = self.exercise.variants.get(self.coding_language, {})
        return str(variant.get(key, getattr(self.exercise, key, "")))

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="page"):
            yield Static(f"[bold #fbbf24]{self.simulation.title}[/]\n40 minuti di coding · poi stop · 60 minuti di repository", classes="hero")
            yield Static("", id="mock-timer", classes="stat-card")
            with ScrollableContainer(id="mock-coding-prompt", can_focus=True):
                yield Static("La prima sezione ha un solo problema e un limite autonomo di 40 minuti. Non consultare gli hint o la soluzione.", classes="panel")
                yield Markdown(assessment_prompt(self.exercise))
            with ScrollableContainer(id="mock-repository-prompt", can_focus=True):
                yield Markdown(self.repository_prompt_text())
            yield CodeTextArea(
                self.variant_value("starter"),
                language=self.coding_language,
                show_line_numbers=True,
                id="mock-editor",
                brace_indentation=self.coding_language in BRACE_INDENT_LANGUAGES,
                brace_language=self.coding_language,
            )
            yield Static("", id="mock-result", classes="panel")
            with Horizontal(classes="actions", id="mock-actions"):
                yield Button("▶ AVVIA CODING · 40:00", id="start", classes="primary")
                yield Button(f"REPOSITORY: {self.app.store.get_setting('amazon_repository_language', 'node').upper()}", id="repository-language")
                yield Button(f"▶ TEST CODING [{self.coding_language.upper()}] [F5]", id="run-coding", disabled=True)
                yield Button("STOP · PASSA ALLA REPOSITORY", id="finish-coding", disabled=True)
                yield Button("▣ APRI VS CODE", id="open-repository", disabled=True)
                yield Button("▶ TEST REPOSITORY", id="run-repository", disabled=True)
                yield Button("CONCLUDI MOCK", id="finish-mock", disabled=True, classes="success")
        yield AdaptiveFooter()

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#mock-coding-prompt", ScrollableContainer).display = False
        self.query_one("#mock-repository-prompt", ScrollableContainer).display = False
        self.query_one("#mock-editor", TextArea).display = False
        self.query_one("#mock-result", Static).display = False
        self.set_interval(1, self.tick)
        self.render_timer()
        self.set_focus(self.query_one("#start", Button))

    @property
    def locked(self) -> bool:
        return self.started and self.phase < 2

    def action_attempt_back(self) -> None:
        if self.locked:
            self.app.notify("Il mock è sequenziale: completa la sezione in corso prima di uscire.", severity="warning")
        else:
            self.app.pop_screen()

    def tick(self) -> None:
        if not self.running or self.remaining <= 0:
            return
        self.remaining -= 1
        self.render_timer()
        if self.remaining == 0:
            if self.phase == 0:
                self.start_repository()
                self.app.notify("Stop alla sezione coding. Ora hai 60 minuti autonomi per la repository.", severity="warning")
            else:
                self.finish_mock()

    def render_timer(self) -> None:
        minutes, seconds = divmod(self.remaining, 60)
        names = {0: "CODING QUESTION", 1: "CODE REPOSITORY", 2: "MOCK CONCLUSO"}
        state = "IN CORSO" if self.running else "IN PAUSA"
        self.query_one("#mock-timer", Static).update(
            f"[bold #67e8f9]{names[self.phase]} · {minutes:02d}:{seconds:02d}[/] · {state}"
        )

    async def action_run_coding(self) -> None:
        if self.phase != 0 or not self.started or not self.running:
            return
        answer = self.query_one("#mock-editor", TextArea).text
        result = await asyncio.to_thread(run_exercise, self.exercise, answer, PROJECT_ROOT, language=self.coding_language)
        if self.phase != 0:
            return
        self.query_one("#mock-result", Static).update(f"{result.score}%\n{result.output}\n" + "\n".join(result.details))
        self.query_one("#mock-result", Static).display = True

    def start_coding(self) -> None:
        if self.started:
            return
        self.started = True
        self.running = True
        self.query_one("#mock-coding-prompt", ScrollableContainer).display = True
        self.query_one("#mock-editor", TextArea).display = True
        self.query_one("#start", Button).disabled = True
        self.query_one("#repository-language", Button).disabled = True
        self.query_one("#run-coding", Button).disabled = False
        self.query_one("#finish-coding", Button).disabled = False
        self.render_timer()
        self.set_focus(self.query_one("#mock-editor", TextArea))

    def start_repository(self) -> None:
        self.phase = 1
        self.running = True
        self.remaining = 60 * 60
        self.query_one("#mock-coding-prompt", ScrollableContainer).display = False
        self.query_one("#mock-editor", TextArea).display = False
        self.query_one("#mock-result", Static).display = False
        self.query_one("#mock-repository-prompt", ScrollableContainer).display = True
        self.workspace_path = ensure_lab_workspace(self.app.workspace_root, self.lab)
        self.query_one("#finish-coding", Button).disabled = True
        self.query_one("#open-repository", Button).disabled = False
        self.query_one("#run-repository", Button).disabled = False
        self.render_timer()
        self.set_focus(self.query_one("#mock-repository-prompt", ScrollableContainer))

    async def run_repository(self) -> None:
        if self.phase != 1 or not self.workspace_path:
            return
        result = await asyncio.to_thread(run_lab_tests, self.workspace_path)
        self.query_one("#mock-result", Static).update(result.output)
        self.query_one("#mock-result", Static).display = True
        self.app.store.record_attempt(self.lab.id, "lab", str(self.workspace_path), result.passed, 100 if result.passed else 0)

    def finish_mock(self) -> None:
        self.phase = 2
        self.running = False
        self.remaining = 0
        self.query_one("#finish-coding", Button).disabled = True
        self.query_one("#open-repository", Button).disabled = True
        self.query_one("#run-repository", Button).disabled = True
        self.query_one("#finish-mock", Button).disabled = False
        self.app.store.record_attempt(self.simulation.id, "simulation", "full mock completato", True, 0)
        self.render_timer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.start_coding()
        elif event.button.id == "repository-language" and not self.started:
            language = "cpp" if self.app.store.get_setting("amazon_repository_language", "node") == "node" else "node"
            self.app.store.set_setting("amazon_repository_language", language)
            self.query_one("#repository-language", Button).label = f"REPOSITORY: {language.upper()}"
        elif event.button.id == "run-coding":
            await self.action_run_coding()
        elif event.button.id == "finish-coding" and self.phase == 0:
            self.start_repository()
        elif event.button.id == "open-repository" and self.workspace_path:
            _ok, message = open_vscode(self.workspace_path)
            self.app.notify(message)
        elif event.button.id == "run-repository":
            asyncio.create_task(self.run_repository())
        elif event.button.id == "finish-mock" and self.phase == 2:
            self.app.pop_screen()


    def action_dashboard(self) -> None:
        if self.locked:
            self.app.notify("Completa la sezione del mock in corso prima di tornare alla Dashboard.", severity="warning")
            return
        self.app.pop_screen()


class Dev48App(App):
    TITLE = TRACK_DEFINITIONS[0].window_title
    SUB_TITLE = TRACK_DEFINITIONS[0].window_subtitle
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("ctrl+d", "dashboard", "Dashboard", priority=True),
        Binding("ctrl+t", "switch_track", "Scegli percorso", priority=True),
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
            active_track = self.store.get_active_track(TRACK_DEFINITIONS[0].id)
            self.catalog = Catalog(CONTENT_ROOT, track=active_track)
            self.coding_language = self.store.get_setting("amazon_coding_language", "python")
            self.sync_app_title()
        except Exception:
            self.lock.release()
            raise
        errors = self.catalog.validate()
        if errors:
            raise RuntimeError("Catalogo non valido:\n" + "\n".join(errors))

    def sync_app_title(self) -> None:
        definition = self.catalog.track_definition
        self.title = definition.window_title
        self.sub_title = definition.window_subtitle

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
        track_item_ids = {item.id for item in self.catalog.lessons}
        track_item_ids.update(exercise_progress_id(item, self.coding_language) for item in self.catalog.exercises)
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
        if self.catalog.study_plan:
            lines.append("\n[bold #fbbf24]PIANO ESSENZIALE · 6 GIORNI[/]")
            planned_minutes = 0
            for day in self.catalog.study_plan:
                day = dict(day)
                for choice in day.get("choices", []):
                    language = self.coding_language if choice["setting"] == "coding_language" else self.store.get_setting("amazon_repository_language", "node")
                    branch = choice["options"][language]
                    for field in ("lesson_ids", "lab_ids"):
                        day[field] = day.get(field, []) + branch.get(field, [])
                    day["practice_minutes"] = int(day.get("practice_minutes", 0)) + int(branch.get("practice_minutes", 0))
                lesson_ids = day.get("lesson_ids", [])
                exercise_ids = day.get("exercise_ids", [])
                lab_ids = day.get("lab_ids", [])
                simulation_ids = day.get("simulation_ids", [])
                scenario_ids = day.get("scenario_ids", [])
                style_ids = day.get("work_style_ids", [])
                lesson_items = [self.catalog.lesson_by_id[item_id] for item_id in lesson_ids if item_id in self.catalog.lesson_by_id]
                exercise_items = [self.catalog.exercise_by_id[item_id] for item_id in exercise_ids if item_id in self.catalog.exercise_by_id]
                lab_items = [self.catalog.lab_by_id[item_id] for item_id in lab_ids if item_id in self.catalog.lab_by_id]
                simulation_items = [next(item for item in self.catalog.simulations if item.id == item_id) for item_id in simulation_ids if any(item.id == item_id for item in self.catalog.simulations)]
                day_minutes = sum(item.minutes for item in lesson_items + exercise_items + lab_items + simulation_items) + int(day.get("practice_minutes", 0))
                planned_minutes += day_minutes
                day_done = sum(item.id in completed for item in lesson_items)
                day_done += sum(exercise_progress_id(item, self.coding_language) in completed for item in exercise_items)
                day_total = len(lesson_items) + len(exercise_items)
                hours, minutes_left = divmod(day_minutes, 60)
                lesson_text = " · ".join(item.title for item in lesson_items)
                exercise_text = " · ".join(item.title for item in exercise_items)
                optional_text = " · ".join(
                    [item.title for item in lab_items]
                    + [item.title for item in simulation_items]
                    + [f"scenario {item_id.removeprefix('sde-ws-')}" for item_id in scenario_ids]
                    + [f"work style {item_id.removeprefix('sde-style-')}" for item_id in style_ids]
                )
                lines.append(
                    f"\n[G{day['day']}] {day['title']} · {hours}h {minutes_left:02d}m · {day_done}/{day_total} lezioni/esercizi"
                    f"\n[#cbd5e1]Lezioni: {lesson_text}[/]"
                    + (f"\n[#cbd5e1]Esercizi: {exercise_text}[/]" if exercise_text else "")
                    + (f"\n[#91a4c7]Pratica: {optional_text}[/]" if optional_text else "")
                    + f"\n[#91a4c7]Recall: {day.get('flashcard_minutes', 0)} min flashcard · {day.get('review_minutes', 0)} min error review[/]"
                )
            lines.append(f"\n[#91a4c7]Carico essenziale pianificato: {planned_minutes//60}h {planned_minutes%60:02d}m. Gli esercizi, laboratori e simulazioni restanti sono ripassi facoltativi nel curriculum.[/]")
        lines.append("\n[#91a4c7]◆ obbligatorio   · approfondimento   Ctrl+T cambia traccia   Ctrl+K curriculum   Ctrl+G glossario[/]")
        return "".join(lines)

    def action_switch_track(self) -> None:
        if isinstance(self.screen, FullMockScreen) and self.screen.locked:
            self.notify("La selezione del percorso resta chiusa durante il mock sequenziale.", severity="warning")
            return
        self.open_track_selection()

    def open_track_selection(self) -> None:
        if not isinstance(self.screen, TrackSelectionScreen):
            self.push_screen(TrackSelectionScreen(return_to_previous=True))

    def last_item_title(self) -> str:
        last = self.store.get_setting("last_item")
        if last in self.catalog.lesson_by_id:
            return self.catalog.lesson_by_id[last].title
        exercise_id, language = split_exercise_progress_id(last)
        if exercise_id in self.catalog.exercise_by_id:
            exercise = self.catalog.exercise_by_id[exercise_id]
            suffix = f" · {language.upper()}" if language else ""
            return exercise.title + suffix
        if last in self.catalog.lab_by_id:
            return self.catalog.lab_by_id[last].title
        simulation = next((item for item in self.catalog.simulations if item.id == last), None)
        return simulation.title if simulation else ""

    def exercise_has_started(self, exercise: Exercise, language: str) -> bool:
        progress_id = exercise_progress_id(exercise, language)
        if self.store.get_setting(exercise_started_setting_key(progress_id)) == "1":
            return True

        state = self.store.get(progress_id)
        if int(state.get("attempts", 0)) > 0:
            return True
        answer = state.get("answer")
        if answer is None:
            return False
        variant = exercise.variants.get(language, {})
        starter = str(variant.get("starter", exercise.starter))
        return str(answer) != starter

    def next_step(self) -> tuple[str, Lesson | Exercise] | None:
        completed = self.store.completed_ids()
        for lesson in (item for item in self.catalog.lessons if item.mandatory):
            if lesson.id not in completed:
                return "lesson", lesson
            exercises = self.catalog.exercises_for(lesson.id)
            for index, exercise in enumerate(exercises):
                if exercise_progress_id(exercise, self.coding_language) not in completed:
                    last_item = self.store.get_setting("last_item")
                    if (
                        index == 0
                        and last_item == exercise_progress_id(exercise, self.coding_language)
                        and not self.exercise_has_started(exercise, self.coding_language)
                    ):
                        return "lesson", lesson
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
        exercise_id, language = split_exercise_progress_id(last)
        if exercise_id in self.catalog.exercise_by_id:
            exercise = self.catalog.exercise_by_id[exercise_id]
            if language in exercise.variants:
                self.coding_language = language
                self.store.set_setting("amazon_coding_language", language)
            self.push_screen(ExerciseScreen(exercise_id))
            return
        if last in self.catalog.lab_by_id:
            self.push_screen(LabScreen(last))
            return
        simulation = next((item for item in self.catalog.simulations if item.id == last), None)
        if simulation:
            if simulation.kind == "full_mock":
                self.push_screen(FullMockScreen(simulation))
            elif simulation.kind == "coding":
                self.push_screen(CodingSimulationScreen(simulation))
            else:
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
        if isinstance(self.screen, FullMockScreen) and self.screen.locked:
            self.notify("Completa la sezione del mock in corso prima di tornare alla Dashboard.", severity="warning")
            return
        # Lo stack contiene sempre la schermata Textual predefinita sotto la
        # dashboard; preserviamo entrambe e chiudiamo soltanto le viste aperte.
        while len(self.screen_stack) > 2:
            self.pop_screen()

    def action_curriculum(self) -> None:
        if isinstance(self.screen, FullMockScreen) and self.screen.locked:
            self.notify("Il curriculum resta chiuso durante il mock sequenziale.", severity="warning")
            return
        self.push_screen(CurriculumScreen())

    def action_glossary(self) -> None:
        if isinstance(self.screen, FullMockScreen) and self.screen.locked:
            self.notify("Il glossario resta chiuso durante il mock sequenziale.", severity="warning")
            return
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
